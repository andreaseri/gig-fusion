#!/usr/bin/env bash
set -euo pipefail

# Top-level reindex wrapper — runs the scraper's reindex.sh (which calls reindex.py)
#
# Usage examples:
# 1) Index the most recent files from the underdog raw output directory (uses default dev key):
#    ./scripts/start-reindex.sh --path data/raw/underdog
#
# 2) Index a single file explicitly:
#    ./scripts/start-reindex.sh --file data/raw/underdog/concert_events_20250922_184039.json
#
# 3) Provide the Meilisearch API key via env var (recommended for CI or one-off overrides):
#    API_KEY="tiMpun-mipvy5-tehxiw" ./scripts/start-reindex.sh --path data/raw/underdog
#
# 4) Full explicit CLI with custom Meili URL:
#    API_KEY="tiMpun-mipvy5-tehxiw" ./scripts/start-reindex.sh --path data/raw/underdog --meili-url http://localhost:7700
#
# Notes:
#  - The script defaults to using the repo's `.conda/bin/python` (override with `PYTHON_PATH`).
#  - The underlying `services/scraper/scripts/reindex.sh` sets a default dev API key; prefer
#    setting `API_KEY` in your environment for reproducible runs.
#  - Ensure a Meilisearch instance is running at `MEILI_URL`/`--meili-url` before running.


REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$REPO_ROOT/services/scraper/scripts/reindex.sh"

if [ ! -x "$SCRIPT" ]; then
  echo "Expected $SCRIPT to exist and be executable."
  exit 2
fi

exec "$SCRIPT" "$@"
