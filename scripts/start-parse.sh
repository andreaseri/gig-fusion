#!/usr/bin/env bash
set -euo pipefail

# SCRAPER_OUTPUT_DIR="data/raw/underdog" ./scripts/start-parse.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH="${PYTHON_PATH:-$REPO_ROOT/.conda/bin/python}"

SCRAPER_RUN="$REPO_ROOT/services/scraper/scripts/run_scraper.py"

echo "Running parser with python: $PYTHON_PATH"
exec "$PYTHON_PATH" "$SCRAPER_RUN" "$@"

