# Semantic Phase 1.1 Quality Evaluation

## Goal

Phase 1.1 evaluates the LLM-aware semantic layer on real RSS items without turning the evaluation into a production-scale semantic run.

The evaluation is designed to answer:

- Are item cards useful and compact?
- Are item-item relations conservative enough?
- Are item-cluster relations separating same-event, same-topic, and follow-up cases?
- Are cluster cards readable?
- Are source profile suggestions directionally useful?
- How many DeepSeek calls and tokens are needed for a controlled sample?

## Safety Model

Live DeepSeek calls and real DB writes are separately gated.

Live calls require:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1
```

and a configured DeepSeek key via existing project config or:

```bash
CONTENT_INBOX_DEEPSEEK_API_KEY
DEEPSEEK_API_KEY
```

Real DB writes require both:

```bash
--db-path PATH
--write-real-db
```

Without `--write-real-db`, the evaluator reads from the source DB and writes semantic results into a temporary evaluation DB.

## Command

Dry-run evaluation on a real DB sample:

```bash
PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path content_inbox/data/content_inbox.sqlite3 \
  --limit 500 \
  --max-calls 100 \
  --max-candidates 5 \
  --batch-size 5 \
  --concurrency 4 \
  --live \
  --dry-run \
  --output content_inbox/outputs/semantic_eval
```

Small live smoke:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --limit 30 \
  --max-calls 20 \
  --max-candidates 3 \
  --concurrency 4 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```

Real DB write, only after reviewing dry-run output:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path content_inbox/data/content_inbox.sqlite3 \
  --limit 200 \
  --max-calls 80 \
  --concurrency 4 \
  --live \
  --write-real-db \
  --output content_inbox/outputs/semantic_eval
```

## Outputs

Each run writes:

```text
semantic_quality_report.md
semantic_quality_summary.json
```

under:

```text
content_inbox/outputs/semantic_eval/<run_id>/
```

The report includes run metadata, input sample summary, item card results, relation results, cluster quality review suggestions, source profile results, token summaries, errors/fallbacks, and recommendations.

## Quotas And Concurrency

Phase 1.1 defaults are intentionally looser than the first smoke test:

- `evaluate --max-calls` defaults to `100`.
- `evaluate --token-budget` defaults to `200000`.
- `evaluate --concurrency` defaults to `4`.
- `live-smoke --max-calls` defaults to `50`.

Concurrency is applied to item-card batch calls and item-item relation calls. Item-cluster writes and cluster-card patch orchestration remain conservative because they mutate shared event-cluster state. Increase `--concurrency` gradually if the DeepSeek account and network can sustain it.

Recommended local fast sample:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path content_inbox/data/content_inbox.sqlite3 \
  --limit 100 \
  --max-calls 200 \
  --token-budget 400000 \
  --concurrency 8 \
  --live \
  --dry-run \
  --output /tmp/content_inbox_semantic_eval
```

## Source Profile Metric Notes

- `source_material_rate`: fraction of source signals with source-role `source_material`.
- `new_event_rate`: fraction of source signals that contributed to new event creation.
- `source_item_rate`: retained as a compatibility alias for source-material rate in Phase 1.1.
- `llm_total_tokens`: attributed only when `llm_call_logs` has `source_id`, `item_id`, or `cluster_id` linkage. Historical unattributed calls are not copied into every source.

## Deferred Items

- Vector recall for item/cluster candidates.
- Strict tool calls.
- Full merge/split workflow.
- Console UI integration.
- Production-scale semantic processing.
