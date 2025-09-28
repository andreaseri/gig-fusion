#!/usr/bin/env bash
set -euo pipefail

# Top-level parse wrapper — runs the scraper's run_scraper.py
 #
 # Usage examples:
 # 1) Run parser writing output to default location:
 #    ./scripts/start-parse.sh --output-dir data/raw/underdog
 #
 # 2) Run parser and specify an alternate python executable:
 #    PYTHON_PATH="/usr/bin/python3" ./scripts/start-parse.sh --output-dir data/raw/underdog
 #
 # 3) Run parser and pipe output to a specific file (if the underlying script supports it):
 #    ./scripts/start-parse.sh --output-dir data/raw/underdog
 #
 # Notes:
 #  - The `run_scraper.py` script under `services/scraper/scripts/` is executed; review its flags for more control.
 #  - Ensure network access and credentials for any external scrapers used by the parser.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH="${PYTHON_PATH:-$REPO_ROOT/.conda/bin/python}"

SCRAPER_RUN="$REPO_ROOT/services/scraper/scripts/run_scraper.py"

echo "Running parser with python: $PYTHON_PATH"
exec "$PYTHON_PATH" "$SCRAPER_RUN" "$@"

