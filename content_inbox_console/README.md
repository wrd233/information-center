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
| Dashboard | `/dashboard` | Overview: source counts, item stats, recent activity |
| Items | `/items` | Filterable, paginated inbox item list with detail view |
| Sources | `/sources` | RSS source registry with status filters and detail view |
| Runs | `/runs` | Ingest run history with detail and per-source breakdown |
| Clusters | `/clusters` | Event cluster list with detail view |

## Quick Start

### Local (without Docker)

```bash
cd content_inbox_console
pip install -r requirements.txt
# Adjust CONTENT_INBOX_CONSOLE_DB if your content_inbox data is elsewhere
export CONTENT_INBOX_CONSOLE_DB=../content_inbox/data/content_inbox.sqlite3
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

Open http://localhost:8788

### Docker

```bash
cd content_inbox_console
docker compose up --build
```

Open http://localhost:8788

The Docker compose mounts `../content_inbox/data` (database) and `../content_inbox/outputs/runs` (run history) as read-only volumes.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTENT_INBOX_CONSOLE_DB` | `content_inbox/data/content_inbox.sqlite3` | Path to the SQLite database |
| `CONTENT_INBOX_CONSOLE_HOST` | `127.0.0.1` | Server bind address |
| `CONTENT_INBOX_CONSOLE_PORT` | `8788` | Server port |
| `CONTENT_INBOX_CONSOLE_PAGE_SIZE` | `50` | Items per page |
| `CONTENT_INBOX_CONSOLE_DB_TIMEOUT` | `5` | SQLite connection timeout (seconds) |
| `CONTENT_INBOX_CONSOLE_OUTPUTS` | _auto-detected from DB path_ | Path to run outputs directory |

## Specifying the Database Path

The database path can be relative (resolves from repo root) or absolute:

```bash
# Relative to repo root
export CONTENT_INBOX_CONSOLE_DB=content_inbox/data/content_inbox.sqlite3

# Absolute path
export CONTENT_INBOX_CONSOLE_DB=/home/user/mydata/inbox.sqlite3

# Docker: always absolute inside the container
CONTENT_INBOX_CONSOLE_DB=/data/content_inbox.sqlite3
```

## Specifying the Outputs/Runs Path

By default, the console derives `outputs/runs/` relative to the database file. Override with:

```bash
export CONTENT_INBOX_CONSOLE_OUTPUTS=/path/to/content_inbox/outputs/runs
```

## Common Issues

### Can't find database

The console shows a red error banner on every page if the database file doesn't exist. Check:
- The `CONTENT_INBOX_CONSOLE_DB` path is correct.
- In Docker, the volume mount `../content_inbox/data:/data:ro` points to the right directory.

### Database schema mismatch

The console introspects table columns at startup. If `content_inbox` adds new columns, the console handles them gracefully (missing columns return `null`). If `content_inbox` removes or renames columns used in list queries, the console may need updates.

### No run history

The Runs page shows an empty state. This is normal if you haven't run any batch ingestion yet. Run `content_inbox/scripts/run_rss_sources_to_content_inbox.py` to populate.

### Pages show empty

If the database exists but all tables are empty, the console shows friendly empty states with hints. No data = nothing to show.

## Current Limitations (v0.1.0)

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
