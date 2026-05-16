# Architecture: content_inbox_console

## Directory Structure

```
content_inbox_console/
├── app/
│   ├── __init__.py           # Package marker
│   ├── main.py               # FastAPI app factory, lifespan, static files
│   ├── config.py             # Environment-based settings
│   ├── repository.py         # ConsoleRepository — all SQL read queries
│   ├── dependencies.py       # FastAPI dependency injection (db connection, etc.)
│   └── routes/
│       ├── __init__.py       # Router registration
│       ├── dashboard.py      # /dashboard, /api/dashboard/stats
│       ├── items.py          # /items, /items/rows, /items/{id}
│       ├── sources.py        # /sources, /sources/rows, /sources/{id}
│       ├── runs.py           # /runs, /runs/rows, /runs/{id}
│       └── clusters.py       # /clusters, /clusters/{id}
├── templates/                # Jinja2 templates (server-side rendering)
│   ├── base.html             # Main layout (PicoCSS + HTMX + nav)
│   ├── dashboard.html        # Dashboard page
│   ├── items/                # Item list, HTMX rows, detail
│   ├── sources/              # Source list, HTMX rows, detail
│   ├── runs/                 # Run list, HTMX rows, detail
│   ├── clusters/             # Cluster cards, detail
│   └── components/           # Reusable: nav, badges, pagination, error states
├── static/css/app.css        # Custom CSS on top of PicoCSS
├── tests/                    # pytest test suite
├── Dockerfile                # python:3.11-slim container
├── docker-compose.yml        # Volume mounts for DB + outputs
└── docs/ARCHITECTURE.md      # This file
```

## Backend Modules

### config.py — Settings
Loads configuration from environment variables with sensible defaults. The database path can be relative (resolved from repo root) or absolute.

### repository.py — ConsoleRepository
All database access lives here. Key design choices:
- **Per-method connection**: each method receives a `sqlite3.Connection` from the caller (via FastAPI dependency injection).
- **Column introspection**: at first access, `PRAGMA table_info` is queried and cached per table. Queries only SELECT columns that actually exist.
- **JSON parsing**: `screening_json`, `clustering_json`, `tags_json`, etc. are parsed to Python objects before returning. Malformed JSON returns `{}` or `[]` with a logged warning.
- **Read-only**: connections are opened with `PRAGMA query_only = 1`.

### dependencies.py
FastAPI dependency functions:
- `get_db_connection()` — opens a read-only SQLite connection per request, closes it after.
- `verify_db_available()` — checks database existence at startup.

### routes/
Each module handles one domain. Routes return HTML (Jinja2 templates) or HTML fragments (HTMX partials). Key patterns:
- Full pages check `db_available` flag and pass error state to templates.
- HTMX row endpoints (`/items/rows`, etc.) return only `<tr>` elements.
- Filter forms use `hx-get` + `hx-target` for partial updates.

## Frontend Architecture

### Rendering Strategy
Server-side rendering with Jinja2. HTMX provides interactivity:
- **Filter forms**: `hx-get` on change/submit replaces table bodies.
- **Pagination**: links fire `hx-get` to row endpoints.
- **No JavaScript build step**: HTMX loaded from CDN, PicoCSS from CDN.

### CSS
PicoCSS provides base styling (classless semantic HTML). `app.css` adds:
- Status badge colors (green/yellow/red/gray).
- Error/warning/empty state banners.
- Stats card grid.
- Cluster card layout.
- Sticky navigation.
- Table horizontal scroll.

### Template Hierarchy
```
base.html (PicoCSS + HTMX + nav)
├── dashboard.html
├── items/list.html → items/_rows.html (HTMX partial)
├── items/detail.html
├── sources/list.html → sources/_rows.html (HTMX partial)
├── sources/detail.html
├── runs/list.html → runs/_rows.html (HTMX partial)
├── runs/detail.html
├── clusters/list.html
└── clusters/detail.html
```

## Data Flow

```
Browser
  │  GET /dashboard
  ▼
FastAPI route (dashboard.py)
  │  Depends(get_db_connection) → sqlite3.Connection (read-only)
  │  request.app.state.repository → ConsoleRepository
  ▼
ConsoleRepository
  │  count_sources(conn), count_items(conn), ...
  │  PRAGMA table_info → cached columns → safe SELECT
  ▼
dicts/lists
  │
  ▼
Jinja2 template (dashboard.html)
  │  Renders HTML with data
  ▼
Browser (HTML page with HTMX)
  │  User interacts with filters/pagination
  │  hx-get → route → repository → HTMX partial → DOM update
  ▼
Updated table body (no full page reload)
```

## Integration Boundary with content_inbox

### What We Read From

| Source | How Accessed | Mount |
|--------|-------------|-------|
| SQLite database | `sqlite3.connect()` read-only | Docker: `../content_inbox/data:/data:ro` |
| Run outputs | File system reads | Docker: `../content_inbox/outputs/runs:/workspace/content_inbox/outputs/runs:ro` |

### What We Do NOT Do

- Do NOT import `content_inbox` Python modules.
- Do NOT call `content_inbox` API endpoints (the service may not be running).
- Do NOT write to the database.
- Do NOT trigger ingestion or screening.

### Why Direct SQLite Access (Not API)

1. The console should work even when `content_inbox` service is not running.
2. Direct `sqlite3` reads are fast and avoid network overhead for a local tool.
3. The `content_inbox` API doesn't expose all the fields the console needs (like `screening_json` internals).
4. Schema introspection makes the console resilient to `content_inbox` evolution.

### Future Abstraction

If `content_inbox` gains a comprehensive read API, the repository layer could be refactored to use HTTP calls instead of direct SQLite. The `ConsoleRepository` class is the single abstraction boundary — routes never touch SQL.

## Database Schema Dependency

The console depends on these tables existing:

| Table | Critical Columns (must exist) | Optional Columns (graceful fallback) |
|-------|------------------------------|--------------------------------------|
| `inbox_items` | item_id, title, source_name, created_at | screening_json, clustering_json, source_id, feed_url, embedding_*, latest_* |
| `rss_sources` | source_id, source_name, feed_url, status | failure_count, consecutive_failure_count, last_*_count, last_duration_ms, tags_json |
| `rss_ingest_runs` | run_id, status, started_at | duration_ms, *_count columns, error_*, request_json |
| `rss_ingest_run_sources` | id, run_id, status | source_id, *_count columns, incremental_*, warnings_json |
| `event_clusters` | cluster_id, cluster_title, item_count | entities_json, embedding_model |

If critical columns are missing, the page will still render but show "null" or "-" for those values. The console never fails due to missing columns.
