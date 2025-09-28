#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/start-frontend.sh
#
# Environment overrides:
#   VITE_BACKEND_URL - backend URL used by frontend (defaults to http://127.0.0.1:8000)
#

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$REPO_ROOT/services/frontend"

VITE_BACKEND_URL="${VITE_BACKEND_URL:-http://127.0.0.1:8000}"

echo "Starting frontend in $FRONTEND_DIR"
echo "Using VITE_BACKEND_URL=$VITE_BACKEND_URL"

cd "$FRONTEND_DIR"
if [ ! -d node_modules ]; then
  echo "Running npm install..."
  npm install
fi

export VITE_BACKEND_URL
exec npm run dev
