#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH="${PYTHON_PATH:-$REPO_ROOT/.conda/bin/python}"

MEILI_URL="${MEILI_URL:-http://localhost:7700}"
API_KEY="${API_KEY:-tiMpun-mipvy5-tehxiw}"

REINDEX_RUN="$REPO_ROOT/services/scraper/scripts/run_reindex.py"

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 --path <dir> | --file <file>"
  echo "Example: $0 --path data/raw/underdog"
  exit 1
fi

args=("$@")

echo "Running reindex with python: $PYTHON_PATH"
exec "$PYTHON_PATH" "$REINDEX_RUN" --meili-url "$MEILI_URL" --api-key "$API_KEY" "${args[@]}"
