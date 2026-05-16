# Scheduler Boundary

`content_inbox` does not include a scheduler. A future scheduler should treat it as an API-backed execution kernel:

1. Read active sources from `GET /api/rss/sources?status=active`.
2. Skip `paused`, `disabled`, and `broken` sources unless an operator explicitly requests `force` or `test`.
3. Trigger source ingest through `POST /api/rss/sources/{source_id}/ingest`.
4. Inspect run history through `GET /api/rss/runs` and `GET /api/rss/runs/{run_id}/sources`.

The scheduler should not write SQLite directly. CSV files are import inputs only, not runtime truth.
