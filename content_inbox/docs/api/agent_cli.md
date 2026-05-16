# Agent CLI

The formal Agent CLI is:

```bash
PYTHONPATH=. python -m app.cli <command> --json
```

Contract:

- stdout is always JSON.
- stderr may contain human-readable errors.
- success exits `0`.
- failure exits non-zero and still writes a JSON error envelope to stdout.

Common commands:

```bash
PYTHONPATH=. python -m app.cli inbox --today --tz Asia/Shanghai --json
PYTHONPATH=. python -m app.cli inbox --created-from 2026-05-16T00:00:00Z --created-to 2026-05-16T23:59:59Z --json
PYTHONPATH=. python -m app.cli sources list --status active --json
PYTHONPATH=. python -m app.cli sources ingest <source_id> --screen false --json
PYTHONPATH=. python -m app.cli sources import-csv --csv ../rsshub/rss_opml/rss_sources.csv --dry-run --json
PYTHONPATH=. python -m app.cli sources backfill-items --dry-run --json
PYTHONPATH=. python -m app.cli runs list --json
```

Do not parse `scripts/run_rss_sources_to_content_inbox.py` stdout for Agent queries. That script is a batch runner and report generator.
