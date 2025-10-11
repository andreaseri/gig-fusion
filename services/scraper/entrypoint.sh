#!/bin/sh
set -e

# use args from docker run command
# Allow overriding via environment variables at runtime (docker run -e ...)
# If the env vars are set in the image or via `docker run -e`, use them as defaults.
MEILI_URL="${MEILI_URL:-}"
MEILI_API_KEY="${MEILI_API_KEY:-}"
DATA_PATH="${DATA_PATH:-/data/raw/underdog}"
while [ $# -gt 0 ]; do
  case "$1" in
    --meili-url)
      MEILI_URL="$2"
      shift 2
      ;;
    --api-key)
      MEILI_API_KEY="$2"
      shift 2
      ;;
    --path)
      DATA_PATH="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Run the scraper and then reindex the data
python3 /scripts/run_scraper.py --path "$DATA_PATH"
python3 /scripts/run_reindex.py --meili-url "$MEILI_URL" --api-key "$MEILI_API_KEY" --path "$DATA_PATH"