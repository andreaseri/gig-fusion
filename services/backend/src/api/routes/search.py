from typing import List, Optional, Dict
from datetime import datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from ..services.meili import MeiliClient


class SearchRequest(BaseModel):
    q: Optional[str] = Field("", description="Search query")
    filter: Optional[str] = Field(None, description="Filter string for Meilisearch")
    facets: Optional[List[str]] = Field(None, description="Facet fields to return")
    sort: Optional[List[str]] = Field(None, description="Sort order, e.g. ['date:desc']")
    limit: int = Field(default=100, description="Limit number of results", ge=1, le=1000)


class SearchResponse(BaseModel):
    hits: List[dict]
    offset: int
    limit: int
    estimated_total_hits: int
    facets: Optional[dict] = None


router = APIRouter(prefix="/search")


@router.get("", response_model=SearchResponse)
def search(
    q: str = Query(""),
    filter: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    weekday: Optional[str] = Query(None, description="Optional comma-separated weekdays to filter (mon,tue,...)")
):
    meili = MeiliClient()
    # Default facets from ingest.ipynb

    opts = {"limit": limit,
            "facets": ["location", "status_kind", "price_eur", "date", "band"]}
    if filter:
        opts["filter"] = filter
    if sort:
        opts["sort"] = sort.split(",")

    print(f"Search Meilisearch: q={q!r}, opts={opts}")

    res = meili.search(q or "", opts)

    # Build a weekday distribution from the returned hits (server-side)
    hits = res.get("hits", [])
    weekday_map: Dict[int, str] = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}

    # Optionally filter hits by weekday(s) before computing final facets/hits
    if weekday:
        wanted = set([w.strip().lower() for w in weekday.split(',') if w.strip()])
        filtered_hits = []
        for h in hits:
            d = None
            try:
                d = datetime.fromisoformat(str(h.get("date")))
            except Exception:
                try:
                    d = datetime.strptime(str(h.get("date"))[:10], "%Y-%m-%d")
                except Exception:
                    d = None
            if d is None:
                continue
            if weekday_map.get(d.weekday()) in wanted:
                filtered_hits.append(h)
        hits = filtered_hits
    # Recompute weekday counts and other facet distributions from the (possibly filtered) hits
    weekday_counts: Dict[str, int] = {}
    # Prepare containers for facet counts we want to recompute when a weekday filter is applied
    recompute_keys = ["location", "status_kind", "price_eur", "date", "band"]
    recomputed_facets: Dict[str, Dict[str, int]] = {k: {} for k in recompute_keys}

    for h in hits:
        try:
            d = datetime.fromisoformat(str(h.get("date")))
        except Exception:
            try:
                d = datetime.strptime(str(h.get("date"))[:10], "%Y-%m-%d")
            except Exception:
                d = None
        if d:
            key = weekday_map.get(d.weekday(), "")
            if key:
                weekday_counts[key] = weekday_counts.get(key, 0) + 1

        # Recompute other facets from the hit values
        for fk in recompute_keys:
            val = h.get(fk)
            if val is None:
                continue
            # Normalize price/date values to strings for distribution keys
            if fk == "price_eur":
                sval = str(val)
            elif fk == "date":
                # use date part YYYY-MM-DD so Meilisearch-style date buckets align
                s = str(val)
                sval = s[:10]
            else:
                sval = str(val)
            recomputed_facets[fk][sval] = recomputed_facets[fk].get(sval, 0) + 1

    # Use the original facetDistribution as a base, but override with recomputed distributions
    base_facets = res.get("facetDistribution") or {}
    merged_facets = {**base_facets}
    # Only override with recomputed data for keys we care about (so weekday selection affects them)
    for k in recompute_keys:
        merged_facets[k] = recomputed_facets.get(k, {})

    # normalize response for the Pydantic model
    response = {
        "hits": hits,
        "offset": res.get("offset", 0),
        "limit": res.get("limit", limit),
        "estimated_total_hits": res.get("estimatedTotalHits", 0),
        "facets": {
            **merged_facets,
            "weekday": weekday_counts,
        },
    }
    return response
