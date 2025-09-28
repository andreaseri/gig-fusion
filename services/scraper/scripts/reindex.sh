#!/usr/bin/env bash
set -euo pipefail

# Wrapper to run the Python reindex script with the explicit Meilisearch API key
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON_PATH="${PYTHON_PATH:-$REPO_ROOT/.conda/bin/python}"

MEILI_URL="${MEILI_URL:-http://localhost:7700}"
API_KEY="${API_KEY:-tiMpun-mipvy5-tehxiw}"

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 --path <dir> | --file <file>"
  echo "Example: $0 --path data/raw/underdog"
  exit 1
fi

args=("$@")

exec "$PYTHON_PATH" "$REPO_ROOT/services/scraper/scripts/reindex.py" --meili-url "$MEILI_URL" --api-key "$API_KEY" "${args[@]}"
