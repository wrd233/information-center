# RSS Source Registry And Agent CLI Design

## Scope

This design adds first-class RSS source registration, source status, structured source ingest results, structured RSS errors, and a formal Agent-facing CLI. It intentionally does not change LLM screening quality logic, `/api/inbox?date=today` API timezone semantics, fallback dedupe rules, or `preserve_source_entry_order` behavior.

## Source Registry

RSS sources are stored in SQLite table `rss_sources`. Each source has a stable `source_id`, display metadata, original and normalized feed URLs, status, tags, notes, source-level config, and the latest ingest health/result fields.

Supported status values:

| status | Meaning |
|---|---|
| `active` | Normal source. |
| `paused` | Temporarily paused by operator. |
| `disabled` | Soft-disabled; source ingest rejects by default. |
| `broken` | Known broken or needs manual review. |

New `inbox_items` rows can persist `source_id` and `feed_url`. Older rows may have these fields empty.

## Source API

Register:

```bash
curl -s http://127.0.0.1:8787/api/rss/sources \
  -H 'content-type: application/json' \
  -d '{
    "source_id":"rsshub-36kr",
    "source_name":"36氪",
    "source_category":"科技/商业",
    "feed_url":"http://rsshub:1200/36kr/news/latest",
    "status":"active",
    "priority":2,
    "tags":["tech","business"],
    "config":{"incremental_mode":"until_existing","screen":false}
  }'
```

List:

```bash
curl -s 'http://127.0.0.1:8787/api/rss/sources?status=active&category=科技&limit=100'
```

Get, update, and soft-disable:

```bash
curl -s http://127.0.0.1:8787/api/rss/sources/rsshub-36kr
curl -s -X PATCH http://127.0.0.1:8787/api/rss/sources/rsshub-36kr \
  -H 'content-type: application/json' \
  -d '{"status":"paused","priority":4}'
curl -s -X DELETE http://127.0.0.1:8787/api/rss/sources/rsshub-36kr
```

## Source Ingest

Registered-source ingest reuses the existing RSS analyze path, but source metadata and config are read from `rss_sources`, and source health fields are updated after success or failure.

```bash
curl -s http://127.0.0.1:8787/api/rss/sources/rsshub-36kr/ingest \
  -H 'content-type: application/json' \
  -d '{
    "screen":false,
    "incremental_mode":"until_existing",
    "probe_limit":20,
    "new_source_initial_limit":5,
    "old_source_no_anchor_limit":20
  }'
```

The response contains a stable `run` object with `run_id`, status, timing, retryability, stats, and incremental details.

## Structured Errors

RSS source and ingest errors use:

```json
{
  "ok": false,
  "error": {
    "error_code": "rss_parse_error",
    "message": "failed to parse feed",
    "retryable": false,
    "source_id": "rsshub-36kr",
    "feed_url": "http://rsshub:1200/36kr/news/latest"
  }
}
```

Core codes include `source_not_found`, `source_conflict`, `source_disabled`, `rss_fetch_timeout`, `rss_fetch_http_error`, `rss_fetch_not_found`, `rss_fetch_connection_error`, `rss_parse_error`, `rss_empty_feed`, `content_processing_error`, `storage_error`, and `unknown_error`.

## Agent CLI

Use `python -m app.cli` for Agent-facing calls. In JSON mode, stdout is pure JSON and human-readable errors go to stderr.

Inbox:

```bash
PYTHONPATH=. python -m app.cli inbox --json --limit 20
PYTHONPATH=. python -m app.cli inbox --json --today --tz Asia/Shanghai --limit 20
PYTHONPATH=. python -m app.cli inbox --json --keyword AI --source "36氪" --limit 10
```

Sources:

```bash
PYTHONPATH=. python -m app.cli sources list --json
PYTHONPATH=. python -m app.cli sources get rsshub-36kr --json
PYTHONPATH=. python -m app.cli sources register --source-id rsshub-36kr --name 36氪 --feed-url http://rsshub:1200/36kr/news/latest --json
PYTHONPATH=. python -m app.cli sources update rsshub-36kr --status paused --json
PYTHONPATH=. python -m app.cli sources ingest rsshub-36kr --json --screen false
```

`scripts/run_rss_sources_to_content_inbox.py` remains a batch runner and reporting tool. Agents should not parse its stdout as a stable JSON query interface.
