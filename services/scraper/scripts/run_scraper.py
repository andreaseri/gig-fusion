import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Tuple
import musicbrainzngs
import time
import logging
from musicbrainzngs.musicbrainz import NetworkError
import json
import os
from typing import Optional
import argparse
from datetime import datetime

# set a stable user agent once at import time
musicbrainzngs.set_useragent("UnderdogEventsParser", "1.0")

logger = logging.getLogger(__name__)

URL = "https://underdogrecordstore.de/vorverkauf"

def _retry_call(func, *args, retries: int = 3, base_delay: float = 0.5, **kwargs):
    """Helper to call a musicbrainzngs function with retries on NetworkError.

    Returns the function result on success, or ``None`` if all retries failed due
    to network errors.
    """
    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except NetworkError as e:
            if attempt >= retries:
                logger.warning("NetworkError calling %s: %s (attempt %d/%d)",
                               getattr(func, "__name__", str(func)), e, attempt, retries)
                return None
            # exponential backoff
            sleep_for = base_delay * (2 ** (attempt - 1))
            time.sleep(sleep_for)


def get_band_info(name: str, max_genres=3):
    """Fetch band members and genres from MusicBrainz by artist name.

    This function will retry network failures up to 3 times and will gracefully
    skip (return empty lists) if MusicBrainz cannot be reached. It will also
    attempt safer include sets if the server rejects the `genres` include.
    """

    # Step 1: Search for artist (with retries on network errors)
    result = _retry_call(musicbrainzngs.search_artists, artist=name)
    if not result or not result.get("artist-list"):
        return {"members": [], "genres": []}

    # Pick the best match
    count = len(result["artist-list"])

    print(f"MusicBrainz search for '{result["artist-list"]}' returned {count} artists")

    if count > 1:
        return {"members": [], "genres": []}

    artist = result["artist-list"][0]
    mbid = artist["id"]

    # Step 2: Attempt to fetch detailed info. Try includes with genres first,
    # fall back to safer include sets if the server complains, and retry on
    # transient network errors up to 3 times per attempt.
    artist_data = None

    try:
        data = _retry_call(musicbrainzngs.get_artist_by_id, mbid, includes=["artist-rels", "tags"])
        artist_data = data.get("artist")
        
    except Exception as e:
        logger.warning("Unexpected error fetching artist %s: %s", name, e)
        return {"members": [], "genres": []}

    if not artist_data:
        return {"members": [], "genres": []}

    # Extract members
    members = []
    for rel in artist_data.get("artist-relation-list", []):
        if rel.get("type") == "member of band":
            members.append(rel.get("artist", {}).get("name"))
    members = list(dict.fromkeys(members))  # remove duplicates

    # Extract genres/tags
    tags = sorted(
        artist_data.get("tag-list", []),
        key=lambda t: int(t.get("count", 0)),
        reverse=True
    )
    genres = [t["name"] for t in tags[:max_genres]]
    # genres = [t.get("name") for t in artist_data.get("tag-list", []) if t.get("name")]

    return {"members": members, "genres": genres}

def get_lines_from_page(url: str) -> List[str]:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text("\n", strip=True)
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def fetch_locations_from_headings(lines: List[str]) -> List[str]:
    return [ln[:-1].strip() for ln in lines if ln.endswith(":")]


def build_event_pattern():
    return re.compile(
        r"""
        ^\s*
        (?P<date>\d{2}\.\d{2}\.)\s+                 # DD.MM.
        (?P<band>.+?)                               # band (lazy)
        (?=                                         # band boundary
            (?:\s+@\s|                              # '@ location' ahead
               \s+[*]?(?:ab\s*)?\d+(?:[.,]\d{1,2})?\s*€? |  # or price
               \s*(?:$|\(|Ausverkauft|Verlegt)      # or EOL/paren/status
            )
        )
        (?:\s+@\s*
            (?P<location>.+?)                       # @ location (digits allowed)
            (?=                                     # location boundary
               (?:\s+[*]?(?:ab\s*)?\d+(?:[.,]\d{1,2})?\s*€? |
                  \s*(?:$|\(|Ausverkauft|Verlegt)
               )
            )
        )?
        (?:\s+[*]?(?:ab\s*)?
            (?P<price>\d+(?:[.,]\d{1,2})?)\s*€?     # optional price
        )?
        (?:\s*(?P<status_text>(?:Ausverkauft!?|[Vv]erlegt)[^\n]*))?  # full status text
        """,
        re.VERBOSE | re.UNICODE,
    )


# status helpers
ARTICLES = r"(?:die|den|das|dem|der)\s+"
PREPS = r"(?:in|nach|vom|von)\s+"

STATUS_PATTERNS = [
    (re.compile(r"\bausverkauft!?$", re.I), "ausverkauft"),
    (re.compile(r"\babgesagt!?$", re.I), "abgesagt"),
    (re.compile(r"\bverlegt\b.*", re.I), "verlegt"),
]


def parse_status(line: str, known_locs: List[str]) -> Tuple[str, str, str]:
    status_kind, new_location, status_raw = "", "", ""

    for pat, kind in STATUS_PATTERNS:
        m = pat.search(line)
        if not m:
            continue
        status_kind = kind
        status_raw = m.group(0).strip()
        break

    # If status is 'verlegt' (moved), try to extract the new location from the status text
    if status_kind == "verlegt":
        status_raw = re.sub(r"^[Vv]erlegt", "verlegt", status_raw)
        s = status_raw
        # always start "verlegt" in lowercase
        # remove leading "verlegt" and any following preposition/article
        for loc in sorted(known_locs, key=len, reverse=True):
            if re.search(rf"\b{re.escape(loc)}\b", s, flags=re.I):
                new_location = loc
                break
        if not new_location:
            mm = re.search(r"(?:in|nach|vom|von\s+(?:die|den|das|dem|der))?\s*(?P<loc>[^,(]+)", s, re.I)
            if mm:
                new_location = mm.group("loc").strip()

    # Default to 'verfügbar' when no explicit status was detected.
    if not status_kind:
        status_kind = "verfügbar"

    return status_kind, new_location, status_raw



def fetch_events() -> List[dict]:
    lines = get_lines_from_page(URL)
    known_locations = fetch_locations_from_headings(lines)
    event_re = build_event_pattern()

    now = datetime.now()
    events = []
    section = None

    for line in lines:
        if line.endswith(":"):
            section = line[:-1].strip()
            continue

        if section == "Underdog Shows":
            continue
        
        m = event_re.match(line)
        if not m:
            continue

        gd = m.groupdict()
        date = gd["date"]
        band = (gd["band"] or "").strip()
        at_loc = (gd.get("location") or "").strip()
        price_raw = gd.get("price")
        status_text = gd.get("status_text") or ""

        location = at_loc if at_loc else (section or "")

        d = datetime.strptime(date + str(now.year), "%d.%m.%Y")

        tmp_date = date
        tmp_date = tmp_date.strip()
        if tmp_date.endswith("."):
            tmp_date = tmp_date[:-1]

        e_day, e_month = map(int, tmp_date.split("."))
        n_day, n_month = now.day, now.month

        if (e_month, e_day) < (n_month, n_day):
            # more than 3 month in the past
            if (now - d).days > 90:
                # future
                if e_month > n_month or (e_month == n_month and e_day >= n_day):
                    # increasing month, this year
                    pass
                else:
                    # smaller month, assume next year
                    d = d.replace(year=now.year + 1)
            else:
                # past
                if e_month > n_month:
                    d = d.replace(year=now.year - 1)
                else:
                    pass
        else:
            pass

        # print(f"Parsed DATE: {date} -> converted to: {d.date()}")

        price_eur = float(price_raw.replace(",", ".")) if price_raw else None

        status_kind, new_location, status_raw = parse_status(line, known_locations)

        # info = get_band_info(band)

        # time.sleep(0.2)

        # print(f"Parsed event: {d.date()} - {band} @ {location} "
        #       f"{'(new loc: ' + new_location + ')' if new_location else ''} "
        #       f"{'(price: ' + str(price_eur) + ' EUR)' if price_eur else ''} "
        #       f"{'(status: ' + status_kind + ')' if status_kind else ''} "
        #       f"{'(members: ' + ', '.join(info['members']) + ')' if info['members'] else ''} "
        #       f"{'(genres: ' + ', '.join(info['genres']) + ')' if info['genres'] else ''}")

        # set empty members and genres
        info = { "members": [], "genres": [] }

        events.append({
            "origin": line,
            "date": d,
            "band": band,
            "location": location,
            "price_eur": price_eur,
            "status_kind": status_kind,
            "new_location": new_location,
            "status_raw": status_raw,
            "section": section,
            "members": info["members"],
            "genres": info["genres"]
        })

    events.sort(key=lambda x: x["date"])
    return events

def save_events(events, basepath: str = "concert_events", path: Optional[str] = None) -> str:
    """Save events to a timestamped JSON file.

    - basepath: base filename used when `path` is a directory or not provided.
    - path: optional. If a file path is provided (endswith .json) it will be used
      directly. If a directory path is provided, the file will be created inside
      that directory using the basepath + timestamp. If omitted, file is created
      in current working directory.

    Returns the full path to the written file.
    """
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    if path:
        # If user passed a directory, create file inside it
        if os.path.isdir(path) or path.endswith(os.path.sep):
            os.makedirs(path, exist_ok=True)
            filename = os.path.join(path, f"{basepath}_{ts}.json")
        else:
            # treat path as a file path; ensure parent dir exists
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            # if path has no .json extension, append timestamp
            if not path.lower().endswith('.json'):
                filename = f"{path}_{ts}.json"
            else:
                filename = path
    else:
        filename = f"{basepath}_{ts}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(events)} events to {filename}")
    return filename

def isoify(events):
    out = []
    for e in events:
        ee = dict(e)
        if isinstance(ee.get("date"), (datetime,)):
            ee["date"] = ee["date"].isoformat()
        out.append(ee)
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Directory to save the output JSON file", default=os.getenv("SCRAPER_OUTPUT_DIR") or os.getenv("SCRAPER_OUTPUT_PATH"))
    args = parser.parse_args()

    events = fetch_events()
    events = isoify(events)

    if args.path:
        save_events(events, basepath="concert_events", path=args.path)
    else:
        save_events(events, basepath="concert_events")

if __name__ == "__main__":
    main()
