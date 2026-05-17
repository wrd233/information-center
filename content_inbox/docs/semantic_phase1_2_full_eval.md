# Semantic Phase 1.2 Full Evaluation

## Goal

Phase 1.2 focuses on real-data evaluation and iteration for AI-related RSS sources, especially sources or item URLs containing `api.xgo.ing`.

The goal is not production writes. The goal is to learn whether the Phase 1 semantic layer can produce useful item cards, duplicate/near-duplicate relations, event clusters, cluster cards, and source profiles on a realistic AI information stream.

## Safety

Live DeepSeek calls require:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1
```

Real database writes require:

```bash
--db-path PATH --write-real-db
```

Without `--write-real-db`, `evaluate` reads from the source DB and writes semantic outputs to a temporary evaluation DB. Reports are written to the selected output directory.

## Source Scope

Use either:

```bash
--source-url-prefix api.xgo.ing
```

or:

```bash
--source-filter api.xgo.ing
```

The filter checks `feed_url`, item `url`, `source_id`, `source_name`, and source category fields where available.

## Sample Modes

`evaluate` supports:

- `recent`: latest items.
- `duplicate_candidates`: title/entity-adjacent order to stress item-item relation.
- `cluster_candidates`: time/source/topic-adjacent order to stress clustering.
- `source_scope_full`: ordered pass over the selected source scope.
- `mixed`: source-grouped mixed sanity sample.

Example:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path data/content_inbox.sqlite3 \
  --source-url-prefix api.xgo.ing \
  --sample-mode mixed \
  --limit 50 \
  --max-calls 100 \
  --max-candidates 5 \
  --concurrency 4 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```

## Concurrency

`--concurrency` currently applies to:

- item-card batch calls;
- item-item relation calls.

Cluster attachment and cluster-card patch orchestration remain conservative because they mutate shared event-cluster state. Start with `1`, `2`, and `4`; increase only if DeepSeek latency and SQLite writes remain stable.

## Report Outputs

Each run writes:

```text
semantic_quality_report.md
semantic_quality_summary.json
```

The report includes:

1. Run Metadata
2. Source Scope
3. Input Sample Summary
4. Item Card Quality
5. Item-Item Relation Quality
6. Item-Cluster Relation Quality
7. Cluster Quality Samples
8. Source Profile Results
9. Token / Latency / Cache Summary
10. Concurrency Summary
11. Errors / Fallbacks / Retries
12. Prompt Iteration Notes
13. Manual Review Suggestions
14. Readiness Assessment
15. Recommendations

## Current Limits

- No vector index yet; recall is `lexical/entity/time/source hybrid`.
- Prompt iteration notes are recorded in the report, but no automatic before/after optimizer is implemented.
- Strong model usage is available via `--strong-model`, mainly for cluster-card patch samples.
- `--write-real-db` is not recommended until several dry-runs have been manually reviewed.

## Recommended Stages

Small sanity:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path data/content_inbox.sqlite3 \
  --source-url-prefix api.xgo.ing \
  --sample-mode mixed \
  --limit 20 \
  --max-calls 30 \
  --concurrency 1 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```

Duplicate-focused:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path data/content_inbox.sqlite3 \
  --source-url-prefix api.xgo.ing \
  --sample-mode duplicate_candidates \
  --limit 50 \
  --max-calls 80 \
  --concurrency 2 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```

Cluster-focused:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path data/content_inbox.sqlite3 \
  --source-url-prefix api.xgo.ing \
  --sample-mode cluster_candidates \
  --limit 80 \
  --max-calls 120 \
  --concurrency 2 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```

Source-scope full dry-run:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path data/content_inbox.sqlite3 \
  --source-url-prefix api.xgo.ing \
  --sample-mode source_scope_full \
  --limit 200 \
  --max-calls 300 \
  --concurrency 2 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```
