# RSS Ingest Run History

Registered-source ingest records run history in SQLite:

- `rss_ingest_runs`: one row per run.
- `rss_ingest_run_sources`: one row per source processed in a run.

Run IDs use UTC timestamp plus source id. Source ingest writes a running row first, then replaces it with success or failure summary. The per-source row preserves status, duration, structured error code, retryability, item counts, and incremental sync details.

APIs:

```bash
curl -s 'http://127.0.0.1:8787/api/rss/runs?limit=20&offset=0'
curl -s http://127.0.0.1:8787/api/rss/runs/<run_id>
curl -s http://127.0.0.1:8787/api/rss/runs/<run_id>/sources
```

CLI:

```bash
PYTHONPATH=. python -m app.cli runs list --json
PYTHONPATH=. python -m app.cli runs get <run_id> --json
PYTHONPATH=. python -m app.cli runs sources <run_id> --json
```
