#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$ROOT/data/source_manager.sqlite3"

echo "RSS Source Manager"
echo "DB: $DB"
echo "API: http://127.0.0.1:8010/api/v1"
echo "UI:  http://127.0.0.1:8010"

cd "$ROOT"
PYTHONPATH="$ROOT" python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8010

