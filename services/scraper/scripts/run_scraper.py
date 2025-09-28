import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.normpath(os.path.join(THIS_DIR, '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from datetime import datetime
from scraper.parsers.underdog import fetch_events
from scraper.output import save_events

def isoify(events):
    out = []
    for e in events:
        ee = dict(e)
        if isinstance(ee.get("date"), (datetime,)):
            ee["date"] = ee["date"].isoformat()
        out.append(ee)
    return out

def main():
    import os

    out_dir = os.getenv("SCRAPER_OUTPUT_DIR") or os.getenv("SCRAPER_OUTPUT_PATH")

    events = fetch_events()
    events = isoify(events)
    if out_dir:
        save_events(events, basepath="concert_events", path=out_dir)
    else:
        save_events(events, basepath="concert_events")

if __name__ == "__main__":
    main()
