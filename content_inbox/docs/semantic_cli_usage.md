# Semantic CLI Usage

Run from `content_inbox/`:

```bash
PYTHONPATH=. python -m content_inbox.semantic cards --limit 100
PYTHONPATH=. python -m content_inbox.semantic dedupe --limit 100
PYTHONPATH=. python -m content_inbox.semantic cluster --limit 100
PYTHONPATH=. python -m content_inbox.semantic patch-cluster-card CLUSTER_ID
PYTHONPATH=. python -m content_inbox.semantic rebuild-cluster-card CLUSTER_ID
PYTHONPATH=. python -m content_inbox.semantic clusters list --status active
PYTHONPATH=. python -m content_inbox.semantic clusters show CLUSTER_ID
PYTHONPATH=. python -m content_inbox.semantic clusters update-status
PYTHONPATH=. python -m content_inbox.semantic source-profiles recompute
PYTHONPATH=. python -m content_inbox.semantic source suggestions
PYTHONPATH=. python -m content_inbox.semantic source profile SOURCE_ID
PYTHONPATH=. python -m content_inbox.semantic source set-priority SOURCE_ID high
PYTHONPATH=. python -m content_inbox.semantic review list
PYTHONPATH=. python -m content_inbox.semantic review approve REVIEW_ID
PYTHONPATH=. python -m content_inbox.semantic review reject REVIEW_ID
```

Use `--db-path` to target a non-default SQLite DB. Live LLM calls need `--live` on processing commands and `CONTENT_INBOX_LLM_ENABLE_LIVE=1`.

Evaluate a real-data sample without writing semantic results to the real DB:

```bash
PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path content_inbox/data/content_inbox.sqlite3 \
  --limit 500 \
  --max-calls 100 \
  --max-candidates 5 \
  --concurrency 4 \
  --live \
  --dry-run \
  --output content_inbox/outputs/semantic_eval
```

Only `--db-path PATH --write-real-db` allows writing to the real DB.

Concurrency:

- `--concurrency` controls concurrent DeepSeek calls for item-card batches and item-item relation judging.
- Default evaluate concurrency is `4`.
- Cluster attachment and cluster-card patch orchestration remain conservative to avoid concurrent event-cluster writes.

Live smoke defaults to a temporary DB:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python -m content_inbox.semantic live-smoke all --limit 3 --max-calls 10
```

Writing a real DB during live smoke requires both:

```bash
--db-path /path/to/content_inbox.sqlite3 --write-real-db
```
