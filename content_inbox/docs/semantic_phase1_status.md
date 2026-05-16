# Semantic Phase 1 Status

## Implemented

- Idempotent semantic tables and light `inbox_items` status columns.
- Item cards with batch generation and heuristic fallback.
- Item-item relations with deterministic rules and one-new-item/many-candidates LLM judging.
- Item-cluster relations with one-new-item/many-candidates LLM judging.
- Cluster card patch/rebuild with versioning.
- Cluster lifecycle statuses: `active`, `cooling`, `archived`, `reopened`, `merged`.
- Source profile recompute with priority suggestions.
- Review queue approve/reject.
- Semantic CLI and backend-only `/api/semantic/*` endpoints.
- Live DeepSeek smoke with temporary DB default.

## Phase 1 Test Results

- `PYTHONPATH=. pytest -q tests/test_semantic_phase1.py`
  - Result: `9 passed, 1 skipped`
- `PYTHONPATH=. pytest -q`
  - Result: `212 passed, 11 skipped`

## Phase 1 Live DeepSeek Sanitized Summary

Live smoke command:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic live-smoke all --limit 3 --max-calls 10
```

Summary:

- Real DB write: `false`
- Temporary DB: `true`
- Model: `deepseek-v4-flash`
- Calls succeeded: `9`
- Calls failed: `0`
- Token totals:
  - `item_card`: 1 call, 2461 tokens
  - `item_relation`: 3 calls, 5124 tokens, 1408 cache-hit tokens
  - `item_cluster_relation`: 2 calls, 4802 tokens, 640 cache-hit tokens
  - `cluster_card_patch`: 3 calls, 6140 tokens, 512 cache-hit tokens

## Phase 1.1 Corrections

- `source_profiles.llm_total_tokens` no longer receives the global `llm_call_logs` total for every source.
- Token attribution now uses `llm_call_logs.source_id`, `llm_call_logs.item_id -> inbox_items`, and `llm_call_logs.cluster_id -> cluster_items -> inbox_items` when available.
- Unattributable historical LLM calls are not assigned to each source.
- `source_material_rate` is separated from `new_event_rate`.
- `source_profiles.source_item_rate` remains as a compatibility alias for source-material rate in Phase 1.1.
- `evaluate` CLI writes Markdown and JSON quality reports.
- `evaluate` defaults to temporary evaluation DB writes unless `--db-path` and `--write-real-db` are both supplied.
- Evaluate defaults are wider for real-data assessment: `--max-calls 100`, `--token-budget 200000`, `--concurrency 4`.
- Concurrent DeepSeek calls are enabled for item-card batches and item-item relation judging.

## Deferred / Deviations

- Vector indexes for `item_cards` and `cluster_cards` are still deferred.
- Strict tool-call mode is deferred; current implementation uses JSON Output, Pydantic validation, and one repair retry.
- Full cluster merge/split workflow is not implemented.
- Console UI integration is not implemented.
- Production-scale full DB semantic processing has not been run.

## Risks And Manual Confirmations

- Real RSS semantic quality still needs human review before writing to the real DB.
- Source profile metrics need more data before priority suggestions should be trusted.
- Candidate recall is lexical/entity based; larger runs should add vector recall.
- Prompt wording should be iterated from real false positives and false negatives.
- Always run `evaluate --dry-run` before `--write-real-db`.

## Follow-ups

- Add item/cluster vector indexes for candidate recall.
- Add a small labeled eval set for relation quality.
- Add source-level token attribution coverage for batched item-card calls.
- Add cluster merge/split governance after relation quality stabilizes.
