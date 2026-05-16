# content_inbox Full Refactor Design

## Goals

`content_inbox` is the deterministic content ingestion and retrieval kernel. The refactor keeps the existing API success paths while making these contracts explicit:

- `rss_sources` is the RSS source registry and future scheduler source of truth.
- Registered-source ingest writes source health and run history.
- Agent integrations use `python -m app.cli ... --json` or HTTP APIs, not runner stdout.
- `screen=false` remains deterministic and does not require LLM or embedding configuration.

## Module Boundaries

- `app.server`: FastAPI routes and response envelopes.
- `app.storage`: SQLite schema, inbox item persistence, source/run stores.
- `app.rss_ingest`: registered source ingest orchestration and run result construction.
- `app.query`: inbox date/time/view query semantics.
- `app.dedupe`: dedupe v2 key construction.
- `app.rss_normalize`: RSS entry normalization helpers.
- `app.source_importer`: CSV source import parsing.
- `app.source_backfill`: backfill existing inbox items with `source_id/feed_url`.
- `app.cli`: Agent-facing CLI parameter parsing and JSON stdout.

## Compatibility

The old endpoints remain available:

- `POST /api/content/analyze`
- `POST /api/rss/analyze`
- `POST /api/rss/analyze-batch`
- `GET /api/inbox`

New behavior is additive except dedupe v2 for newly inserted items. Existing rows keep their stored dedupe keys.
