# content_inbox_console

A read-only web dashboard for visualizing the [content_inbox](../content_inbox/) RSS ingestion service state.

## What It Is

`content_inbox_console` provides a browser-based observation console for your RSS information center. It reads the existing SQLite database and run history directly — no changes to `content_inbox` core code.

## Relationship with content_inbox

- **Reads** the `content_inbox` SQLite database (mounted as a read-only volume in Docker).
- **Reads** run outputs from `content_inbox/outputs/runs/`.
- **Does NOT** modify the database or trigger ingestion (first version is read-only).
- **Does NOT** call any LLM API.

## Implemented Pages

| Page | Route | Description |
|------|-------|-------------|
| Dashboard | `/dashboard` | Overview: registered/observed sources, DB/file runs, item stats, recent activity |
| Items | `/items` | Filterable, paginated inbox item list with detail view |
| Sources | `/sources` | RSS source registry with status filters, observed source fallback, detail view |
| Runs | `/runs` | Ingest run history with DB/file fallback, detail with per-source breakdown |
| Clusters | `/clusters` | Event cluster list with detail view |
| Diagnostics | `/api/diagnostics` | JSON: table counts, schema info, data consistency warnings |

## Registered Sources vs Observed Sources

The console distinguishes two kinds of source information:

### Registered Sources
Sources stored in the `rss_sources` table. These are explicitly managed via the content_inbox source registry API or OPML import flow. They have status, priority, fetch history, and error tracking.

### Observed Sources
Sources derived from `inbox_items` metadata (the `source_name`, `source_id`, or `feed_url` columns). These appear when historical items were ingested without populating the source registry — a common state for databases created by older ingest paths.

When the `rss_sources` registry is empty but inbox items contain source metadata, the console automatically shows observed sources. The Dashboard distinguishes both counts, and the Sources page displays observed sources with a contextual explanation.

## DB Runs vs File Runs

### Database Runs
Ingest run records stored in the `rss_ingest_runs` table. These are created by new-registry-aware ingest flows and include per-source breakdowns in `rss_ingest_run_sources`.

### File Runs
Run reports on disk under `outputs/runs/` (directories like `rss_run_*` or `live_*` containing `final_report.md` or `report.md`). The console scans this directory and displays file-based runs when the `rss_ingest_runs` table is empty.

## Quick Start

### Local (without Docker)

```bash
cd content_inbox_console
pip install -r requirements.txt
export CONTENT_INBOX_CONSOLE_DB=../content_inbox/data/content_inbox.sqlite3
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

### Docker

```bash
cd content_inbox_console
docker compose up --build
```

Open http://localhost:8788

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTENT_INBOX_CONSOLE_DB` | `content_inbox/data/content_inbox.sqlite3` | Path to the SQLite database |
| `CONTENT_INBOX_CONSOLE_HOST` | `127.0.0.1` | Server bind address |
| `CONTENT_INBOX_CONSOLE_PORT` | `8788` | Server port |
| `CONTENT_INBOX_CONSOLE_PAGE_SIZE` | `50` | Items per page |
| `CONTENT_INBOX_CONSOLE_DB_TIMEOUT` | `5` | SQLite connection timeout (seconds) |
| `CONTENT_INBOX_CONSOLE_OUTPUTS` | _auto-detected from DB path_ | Path to run outputs directory |

## Diagnostics API

Verify which database the console is reading and detect data consistency issues:

```bash
curl http://localhost:8788/api/diagnostics | python3 -m json.tool
```

Returns:
- `database.db_path`, `database.db_exists`, `database.db_readable`
- `database.tables` — each expected table with `exists` and `count`
- `outputs.outputs_path`, `outputs.outputs_exists`, `outputs.run_directory_count`
- `warnings` — list of detected inconsistencies (e.g., "rss_sources is empty but inbox_items has 2497 rows")

## Common Issues

### Why are Items showing but Sources is 0?

This is the most common state for databases created before the source registry was introduced:
- `inbox_items` has data (with `source_name` embedded on each item)
- `rss_sources` is empty (registry never populated)

The console handles this by showing **observed sources** derived from inbox item metadata. Check the Sources page — it will list observed sources automatically.

**Fix**: Run the content_inbox OPML/source import flow against this database to populate `rss_sources`.

### Why are outputs/runs present but DB Runs is 0?

Historical runs may have written reports to `outputs/runs/` without recording rows in `rss_ingest_runs`. The console falls back to showing **file runs** from disk.

### Dashboard shows warnings

Warnings appear when the console detects inconsistencies between tables. Common warnings:
- "rss_sources is empty but inbox_items has N rows" → data predates the registry
- "rss_ingest_runs is empty but outputs/runs contains N run directories" → runs were done with old scripts

### Can't find database

Check `CONTENT_INBOX_CONSOLE_DB` and Docker volume mounts. Use `/api/diagnostics` to verify the resolved path.

### Mounted wrong database

If you see unexpected data, your `CONTENT_INBOX_CONSOLE_DB` or Docker volume may be pointing to a different SQLite file (e.g., a test database). Compare with:
```bash
sqlite3 content_inbox/data/content_inbox.sqlite3 "SELECT 'inbox_items', count(*) FROM inbox_items UNION ALL SELECT 'rss_sources', count(*) FROM rss_sources"
```

### Outputs path not mounted

In Docker, the `../content_inbox/outputs/runs:/outputs/runs:ro` volume must exist on the host. If `outputs/runs/` doesn't exist locally, the file runs feature will show empty.

## Current Limitations (v0.2.0)

- **Read-only**: cannot trigger ingestion or modify sources from the console.
- **No LLM**: no AI summaries, recommendations, or chat.
- **No event aggregation**: event clusters are listed but the console doesn't compute new ones.
- **No auth**: no login system — intended for local/trusted network use.
- **No real-time updates**: pages are static; refresh to see new data. HTMX provides partial updates for filters/pagination.

## Future Directions

- Add "Fetch Now" per-source button (calls content_inbox API).
- Add source pause/resume controls.
- Add dashboard auto-refresh with HTMX polling.
- Add source health trends over time.
- Add item bookmarking or reading list.
- Add basic auth for non-local access.
