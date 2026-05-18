# content_inbox_console

`content_inbox_console` is the main frontend Operational Console for `content_inbox`.

It no longer uses hidden direct SQLite fallbacks for the main UI. It calls the backend `/api/*` contract through `app/backend_client.py`.

## Start

Backend:

```bash
cd ../content_inbox
CONTENT_INBOX_DB_PATH=data/environments/fresh_default/content_inbox.db \
CONTENT_INBOX_ENABLE_REAL_RUNS=0 \
PYTHONPATH=. python3 -m app.server
```

Console:

```bash
cd content_inbox_console
CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

Open http://127.0.0.1:8788.

## Core Flow

1. Environment: confirm fresh DB and legacy DB proof.
2. Sources: import preview and commit.
3. Runs: create selected-source dry-run.
4. Runs: create real-write only when backend has `CONTENT_INBOX_ENABLE_REAL_RUNS=1`.
5. Run Detail: observe events, source progress, and items.
6. Information: inspect items, clusters, events, review queue, briefings, reports, and agent query.

## Docker

```bash
cd content_inbox_console
docker compose up --build
```

The console expects the backend at `CONTENT_INBOX_FRONTEND_API_BASE`.
