#!/usr/bin/env python3
"""Ingest latest concert_events_*.json into Meilisearch.

Usage examples:
  # use defaults (http://localhost:7700, no api key)
  python scripts/ingest_meilis.py

  # specify directory and API key
  MEILI_API_KEY=xxx python scripts/ingest_meilis.py --dir data/raw/underdog

  python scripts/ingest_meilis.py --file data/raw/underdog/concert_events_20250922_183046.json --meili-url http://localhost:7700 --api-key xxx

The script will ensure every document has an 'id' (adds sequential ids if missing).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import List

try:
    import meilisearch
except Exception as e:
    print("Please install the meilisearch Python client (pip install meilisearch)")
    raise


def find_latest(basepath: str = "concert_events", directory: str = ".") -> str | None:
    pattern = os.path.join(directory, f"{basepath}_*.json")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def load_events(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Expected JSON file to contain a list of event objects")
    return data


def ensure_ids(docs: List[dict]) -> List[dict]:
    out = []
    next_id = 1
    for d in docs:
        if d.get("id") is None:
            # create a numeric id
            d = dict(d)
            d["id"] = next_id
            next_id += 1
        out.append(d)
    return out


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default=".", help="Directory to search for latest concert_events_*.json")
    p.add_argument("--file", help="Explicit file to ingest (overrides --dir)")
    p.add_argument("--meili-url", default=os.getenv("MEILI_URL", "http://localhost:7700"))
    p.add_argument("--api-key", default=os.getenv("MEILI_API_KEY"))
    p.add_argument("--index", default="events", help="Meilisearch index name")
    args = p.parse_args(argv)

    if args.file:
        path = args.file
    else:
        path = find_latest(directory=args.dir)

    if not path or not os.path.exists(path):
        print(f"No event JSON found (looked at {args.dir}). Use --file to point to a file.")
        sys.exit(2)

    print(f"Loading events from {path}")
    events = load_events(path)
    events = ensure_ids(events)

    print(f"Connecting to Meilisearch at {args.meili_url}")
    client = meilisearch.Client(args.meili_url, args.api_key)
    index = client.index(args.index)

    print(f"Indexing {len(events)} documents into index '{args.index}' (primary_key='id')")
    res = index.add_documents(events, primary_key="id")
    print("Add documents response:", res)

    # Configure attributes (follow existing notebook pattern)
    print("Updating searchable, filterable and sortable attributes")
    index.update_searchable_attributes(["band", "location", "status_kind", "status_raw"])
    index.update_filterable_attributes(["location", "status_kind", "price_eur", "date", "band"])
    index.update_sortable_attributes(["price_eur", "date"])

    print(f"✅ Indexed {len(events)} events into Meilisearch (index={args.index})")


if __name__ == "__main__":
    main()
