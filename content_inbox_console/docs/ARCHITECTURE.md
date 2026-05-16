# Architecture: content_inbox_console

## Directory Structure

```
content_inbox_console/
├── app/
│   ├── __init__.py               # Package marker
│   ├── main.py                   # FastAPI app factory, lifespan, static files
│   ├── config.py                 # Environment-based settings
│   ├── repository.py             # ConsoleRepository — main SQL read queries
│   ├── dependencies.py           # FastAPI dependency injection
│   ├── repositories/             # Compatibility layer (v0.2.0+)
│   │   ├── __init__.py
│   │   ├── diagnostics.py        # DB introspection, table counts, warnings
│   │   ├── observed_sources.py   # Derive sources from inbox_items metadata
│   │   └── file_runs.py          # Scan outputs/runs/ for run reports on disk
│   └── routes/
│       ├── __init__.py           # Router registration
│       ├── dashboard.py          # /dashboard, /api/dashboard/stats
│       ├── items.py              # /items, /items/rows, /items/{id}
│       ├── sources.py            # /sources, /sources/rows, /sources/{id}
│       ├── runs.py               # /runs, /runs/rows, /runs/{id}
│       ├── clusters.py           # /clusters, /clusters/{id}
│       └── diagnostics.py        # /api/diagnostics
├── templates/                    # Jinja2 templates (server-side rendering)
│   ├── base.html                 # Main layout (PicoCSS + HTMX + nav)
│   ├── dashboard.html            # Dashboard with registered/observed split
│   ├── items/                    # Item list, HTMX rows, detail
│   ├── sources/                  # Source list (with observed fallback), detail
│   ├── runs/                     # Run list (with file fallback), detail
│   ├── clusters/                 # Cluster cards, detail
│   └── components/               # Reusable: nav, badges, pagination, error states
├── static/css/app.css            # Custom CSS on top of PicoCSS
├── tests/                        # pytest test suite
├── Dockerfile                    # python:3.11-slim container
├── docker-compose.yml            # Volume mounts for DB + outputs
├── README.md
└── docs/ARCHITECTURE.md          # This file
```

## Backend Modules

### config.py — Settings
Loads configuration from environment variables. The database path can be relative (resolved from repo root) or absolute. The outputs path defaults to `<db_parent>/outputs/runs`.

### repository.py — ConsoleRepository
All database access for the main tables (inbox_items, rss_sources, rss_ingest_runs, rss_ingest_run_sources, event_clusters). Key design choices:
- **Per-method connection**: each method receives a `sqlite3.Connection` from the caller.
- **Column introspection**: `PRAGMA table_info` cached per table. Queries only SELECT columns that exist.
- **JSON parsing**: screened JSON fields parsed to Python objects. Malformed JSON returns `{}` with logged warning.
- **Read-only**: connections opened with `PRAGMA query_only = 1`.

### repositories/diagnostics.py — DiagnosticsRepository
Standalone functions (not class-based) for database introspection:
- `get_db_diagnostics(path)` — checks if DB file exists/is readable, lists expected tables with counts.
- `get_outputs_diagnostics(path)` — checks outputs path existence, counts run directories.
- `compute_warnings(db_diag, outputs_diag)` — cross-references table counts to flag inconsistencies (e.g., "rss_sources empty but inbox_items has data").

### repositories/observed_sources.py — Observed Source Fallback
Derives source identity from `inbox_items` columns when `rss_sources` is empty. Priority order for source key:
```
source_id → source_name → feed_url → url domain
```
Functions:
- `get_source_identity_columns(conn)` — introspects which columns exist.
- `count_observed_sources(conn)` — distinct source count.
- `list_observed_sources(conn, keyword, limit, offset)` — paginated observed source list with stats (item_count, latest_item_at, example_title).
- `list_observed_source_items(conn, key, limit, offset)` — items belonging to an observed source.

### repositories/file_runs.py — File Run Fallback
Scans `outputs/runs/` for directories matching `rss_run_*`, `*ingest*`, or `live_*` patterns. Functions:
- `count_file_runs(path)` — count of run directories.
- `list_file_runs(path, limit, offset)` — returns entries with directory name, mtime, report availability, and parsed metrics from `final_report.md`.
- `get_file_run_detail(path, run_dir_name)` — single file run detail with full report content.

**Security**: all file access is validated to stay within the configured `outputs_path`. Path traversal attempts (e.g., `../../`) are rejected by `_resolve_safe_path()`.

## Data Flow

```
Browser
  │  GET /sources
  ▼
FastAPI route (sources.py)
  │  ├─ Try repo.list_sources() → rss_sources table
  │  └─ If empty → observed_sources.list_observed_sources() → inbox_items
  ▼
Compatibility Repositories
  │  diagnostics: PRAGMA + COUNT queries
  │  observed_sources: GROUP BY source_name with introspection
  │  file_runs: os.scandir + report parsing
  ▼
Jinja2 template
  │  renders registered + observed sources sections
  │  contextual empty state messages
  ▼
Browser (HTML with HTMX)
```

## Integration Boundary with content_inbox

### What We Read From

| Source | How Accessed | Mount |
|--------|-------------|-------|
| SQLite database | `sqlite3.connect()` read-only | Docker: `../content_inbox/data:/data:ro` |
| Run outputs | File system reads (path-safe) | Docker: `../content_inbox/outputs/runs:/outputs/runs:ro` |

### What We Do NOT Do

- Do NOT import `content_inbox` Python modules.
- Do NOT call `content_inbox` API endpoints.
- Do NOT write to the database.
- Do NOT trigger ingestion or screening.

### Why Direct SQLite + File Access (Not API)

1. The console works even when `content_inbox` service is not running.
2. Direct reads are fast for a local tool.
3. The content_inbox API doesn't expose all fields (screening_json internals, source registry details).
4. Schema introspection makes the console resilient to content_inbox evolution.
5. File system scanning provides fallback when DB tables are empty but artifacts exist.

## Compatibility Layer Design (v0.2.0)

### Problem
Old ingest paths wrote items to `inbox_items` with `source_name` embedded directly, without populating `rss_sources` or `rss_ingest_runs`. This causes the console to show "Total Sources: 0" despite having thousands of items.

### Solution
Three fallback layers:
1. **Observed Sources**: when `rss_sources` is empty, derive sources from `inbox_items` metadata columns.
2. **File Runs**: when `rss_ingest_runs` is empty, scan `outputs/runs/` for run directories with report files.
3. **Diagnostics**: `/api/diagnostics` endpoint reveals the full picture — which tables exist, their counts, and any inconsistencies.

### Why Not Modify content_inbox Core Code
- Keeps the console independent and deployable without touching the ingest pipeline.
- Handles historical/legacy data without requiring data migration.
- Avoids coupling the read-only viewer to the write-path logic.

## Database Schema Dependency

| Table | Critical Columns (must exist) | Optional Columns (graceful fallback) |
|-------|------------------------------|--------------------------------------|
| `inbox_items` | item_id, title, source_name, created_at | screening_json, clustering_json, source_id, feed_url, embedding_*, latest_* |
| `rss_sources` | source_id, source_name, feed_url, status | failure_count, consecutive_failure_count, last_*_count, last_duration_ms, tags_json |
| `rss_ingest_runs` | run_id, status, started_at | duration_ms, *_count columns, error_*, request_json |
| `rss_ingest_run_sources` | id, run_id, status | source_id, *_count columns, incremental_*, warnings_json |
| `event_clusters` | cluster_id, cluster_title, item_count | entities_json, embedding_model |
