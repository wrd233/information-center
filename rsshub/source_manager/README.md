# RSS Source Manager

RSS Source Manager is a small standalone service under `rsshub/source_manager/` for managing RSS source facts. It manages three source types:

- `rsshub`: local RSSHub routes such as `/bilibili/user/video/123456`.
- `wechat`: feeds served by the local `wechat-rss` service.
- `native`: ordinary RSS or Atom feed URLs.

It is not a reader, AI briefing system, review queue, scheduler, or `content_inbox_console` page. `content_inbox` can use this service later as a downstream API client, but this module does not import or depend on `content_inbox`.

## Persistence

The default and primary database is:

```text
rsshub/source_manager/data/source_manager.sqlite3
```

The service creates the file if it is missing and reuses it on later starts. There is no reset API or reset UI.

## Install

```bash
cd /Users/wangrundong/work/infomation-center/rsshub/source_manager
python3 -m pip install -r requirements.txt
cd frontend && npm install
```

## Development

```bash
cd /Users/wangrundong/work/infomation-center/rsshub/source_manager
scripts/dev.sh
```

Development addresses:

```text
FastAPI: http://127.0.0.1:8010/api/v1
Vite UI: http://127.0.0.1:5173
Docs:    http://127.0.0.1:8010/docs
```

## Daily Start

Build the frontend once:

```bash
scripts/build_frontend.sh
```

Then start the single FastAPI service:

```bash
scripts/start.sh
```

Daily addresses:

```text
UI:      http://127.0.0.1:8010
API:     http://127.0.0.1:8010/api/v1
Docs:    http://127.0.0.1:8010/docs
```

`start.sh` prints the absolute database path on startup.

## Core API

- Source CRUD: `/api/v1/sources`
- Check: `POST /api/v1/sources/{source_id}/check`
- Fetch: `POST /api/v1/sources/{source_id}/fetch`
- Batch check/fetch: `/api/v1/sources/check-batch`, `/api/v1/sources/fetch-batch`
- Rating adjustments: `/api/v1/sources/{source_id}/rating-adjustments`
- CSV import/export: `/api/v1/imports/csv/*`, `/api/v1/exports/csv`
- OPML import/export: `/api/v1/imports/opml/*`, `/api/v1/exports/opml`
- Read-only settings: `/api/v1/settings`

## Import

CSV and OPML imports are preview-first:

1. Call `/api/v1/imports/csv/preview` or `/api/v1/imports/opml/preview`.
2. Review new/duplicate/failed rows.
3. Call `/api/v1/imports/csv/commit` or `/api/v1/imports/opml/commit`.
4. Optionally run batch check for the created source IDs.

CSV import uses clean fields only. Existing sources are skipped by default.

## Design

See [docs/design_v1.md](docs/design_v1.md) for guardrails, schema, API boundaries, and the phase-one validation matrix.

