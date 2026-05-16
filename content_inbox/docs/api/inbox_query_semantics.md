# Inbox Query Semantics

`GET /api/inbox` supports created-time, published-time, view, and pagination filters.

## Time

- `date=today` without `tz` preserves the legacy UTC today behavior and returns `filters.resolved_timezone="UTC"`.
- `date=today&tz=Asia/Shanghai` resolves the local date in that timezone and converts the boundary to UTC.
- `from` and `to` remain compatibility aliases for `created_from` and `created_to`.
- `published_from` and `published_to` filter `published_at` separately from `created_at`.

## Views

- `view=all`: include ignored and silent items.
- `view=readable`: exclude ignored, keep silent.
- `view=recommended`: exclude ignored and silent; defaults suggested actions to read/save/transcribe/review.
- `view=notifications`: exclude ignored and silent; defaults notification decisions to full/incremental push.

## Stats

Responses include Agent-friendly pagination stats:

```json
{
  "matched_before_post_filters": 100,
  "matched_after_post_filters": 20,
  "returned": 20,
  "limit": 20,
  "offset": 0
}
```
