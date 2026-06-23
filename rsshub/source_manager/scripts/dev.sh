#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "RSS Source Manager dev"
echo "API: http://127.0.0.1:8010/api/v1"
echo "UI:  http://127.0.0.1:5173"

PYTHONPATH="$ROOT" python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8010 &
API_PID=$!
trap 'kill "$API_PID" 2>/dev/null || true' EXIT

cd "$ROOT/frontend"
npm run dev

