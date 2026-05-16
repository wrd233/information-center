# RSS Source Registry And Agent CLI Design

The registry design makes `rss_sources` the durable source of truth for RSS ingestion. CSV and OPML files are import inputs; runtime ingestion should use the Source API.

Key contracts:

- `source_id` is stable and immutable.
- `active` sources can be scheduled and manually ingested.
- `paused` and `broken` sources require `force` or `test` for manual ingest.
- `disabled` sources are soft-deleted and rejected by default.
- Source ingest returns a stable `run` object and writes run history.
- Structured errors use `error.error_code` and `error.retryable`.
- Agent calls should use `python -m app.cli ... --json`, whose stdout is pure JSON.

See:

- `docs/api/source_api.md`
- `docs/api/agent_cli.md`
- `docs/design/run_history.md`
- `docs/operations/source_import.md`
- `docs/operations/runner_usage.md`
