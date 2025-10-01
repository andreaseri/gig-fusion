#!/usr/bin/env python3
"""Index the latest concert_events_*.json directly into Meilisearch.

This script finds the most recent `concert_events_*.json` (or uses a provided
file) and adds the documents to the Meilisearch `events` index using the
`meilisearch` Python client.

Usage examples:
  python reindex.py --path data/raw/underdog
  python reindex.py --file data/raw/underdog/concert_events_20250922_184039.json \
      --meili-url http://localhost:7700 --api-key "$MEILI_API_KEY"
"""
import argparse
import glob
import json
import os
import sys
from pathlib import Path
import uuid

import meilisearch


def find_latest(basepath="concert_events", directory="."):
    pattern = os.path.join(directory, f"{basepath}_*.json")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_ids(docs):
    # Ensure each document has an 'id' field (Meilisearch primary key)
    for d in docs:
        if "id" not in d or d.get("id") in (None, ""):
            d["id"] = str(uuid.uuid4())
    return docs

def drop_all(meili_url, api_key, index_name="events"):
    client = meilisearch.Client(meili_url, api_key)
    try:
        client.delete_index(index_name)
        print("Old index deleted.")
    except Exception:
        print("Index did not exist, skipping delete.")

def index_to_meili(events, meili_url, api_key, index_name="events", primary_key="id"):
    client = meilisearch.Client(meili_url, api_key)
    index = client.index(index_name)

    # Add documents
    resp = index.add_documents(events, primary_key=primary_key)

    # Update common attributes used in the notebooks
    try:
        index.update_searchable_attributes(["band", "location", "description", "venue"])  # example
        index.update_filterable_attributes(["location", "status_kind", "price_eur", "date", "band"])
        index.update_sortable_attributes(["date", "price_eur"])
        index.update_faceting_settings({"maxValuesPerFacet": 1000})  # example
    except Exception:
        # non-fatal if the server rejects attribute updates (older meili versions)
        pass

    return resp


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", help="Path to a specific JSON file to index")
    group.add_argument("--path", help="Directory to search for concert_events_*.json", default=".")

    parser.add_argument("--meili-url", help="Meilisearch URL", default=os.getenv("MEILI_URL", "http://localhost:7700"))
    parser.add_argument("--api-key", help="Meilisearch API key", default=os.getenv("MEILI_API_KEY", None))
    parser.add_argument("--index", help="Meilisearch index name", default="events")
    args = parser.parse_args()

    # print("Arguments:", args)
    # exit(0)
    
    if args.file:
        candidate = args.file
        if not os.path.exists(candidate):
            print(f"File not found: {candidate}")
            sys.exit(2)
        latest = candidate
    else:
        candidate = args.path
        if os.path.isdir(candidate):
            latest = find_latest(directory=candidate)
        else:
            # treat as file path or pattern
            if os.path.exists(candidate):
                latest = candidate
            else:
                latest = find_latest(directory=os.path.dirname(candidate) or ".", basepath=Path(candidate).stem)

    if not latest:
        print("No concert_events_*.json files found.")
        sys.exit(2)

    print(f"Found file: {latest}")
    events = load_json(latest)
    if not isinstance(events, list):
        print("Expected JSON file to contain a list of event objects.")
        sys.exit(2)

    print(f"Loaded {len(events)} events")
    events = ensure_ids(events)

    meili_url = args.meili_url
    api_key = args.api_key
    if api_key is None:
        print("Warning: no MEILI API key provided; attempting unauthenticated connection")

    print(f"Drop all")
    drop_all(meili_url, api_key)
    print(f"Indexing into Meilisearch at {meili_url} -> index '{args.index}'")
    res = index_to_meili(events, meili_url, api_key, index_name=args.index, primary_key="id")
    print("Meilisearch response:", res)


if __name__ == "__main__":
    main()
