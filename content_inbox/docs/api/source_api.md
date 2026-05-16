# RSS Source API

## Register

```http
POST /api/rss/sources
```

`source_id` is optional. If omitted, the server generates a stable ASCII id from source metadata and feed URL.

## List

```http
GET /api/rss/sources
```

Filters: `status`, `category`, `tag`, `keyword`, `priority_min`, `priority_max`, `has_error`, `retryable`, `last_success_before`, `last_failure_after`, `sort`, `limit`, `offset`.

## Get

```http
GET /api/rss/sources/{source_id}?include_recent_items=true
```

Returns `source`, `health`, optional `latest_ingest`, and optional `recent_items`.

## Update

```http
PATCH /api/rss/sources/{source_id}
```

Patchable fields include source display metadata, feed URL, status, priority, tags, notes, and config. `source_id` is immutable.

## Soft Delete

```http
DELETE /api/rss/sources/{source_id}
```

Sets `status=disabled`; items and run history are retained.

## Ingest

```http
POST /api/rss/sources/{source_id}/ingest
```

Supported fields: `force`, `dry_run`, `test`, `screen`, `limit`, `incremental_mode`, `probe_limit`, `new_source_initial_limit`, `old_source_no_anchor_limit`, `stop_on_first_existing`, and `process_order`.

Failures return the structured envelope:

```json
{"ok": false, "error": {"error_code": "source_disabled", "message": "RSS source is disabled", "retryable": false}}
```
