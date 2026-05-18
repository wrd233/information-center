# Phase 1.3c Final Summary

## Verdict
NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE

## What Changed
- Hardened product/actor validation for random tokens, URL/domain fragments, date/price-only fragments, generic AI terms, and sentence fragments while preserving known valid products.
- Added targeted Chinese adoption/product extraction for Anthropic/Claude and expanded Chinese trigger behavior from the delta benchmark.
- Reduced relation LLM cost by suppressing reject/content pairs and converting weak deterministic lanes to rule decisions.
- Compact relation cards and prompt schema reduced item-relation JSON failures materially.
- Added Phase 1.3c delta benchmark fixture tests.

## Files Modified
- app/semantic/signatures.py
- app/semantic/candidates.py
- app/semantic/relations.py
- app/semantic/schemas.py
- app/semantic/evaluate.py
- prompts/item_relation_v3.md
- tests/fixtures/semantic_phase1_3c_delta_benchmark.jsonl
- tests/test_semantic_phase1_3c_delta.py

## Fixture Results
- Focused semantic fixtures: 47 passed, 1 skipped.
- Full suite: 250 passed, 11 skipped.

## Live Evaluation Results
| Run | Path | Key result |
| 80 dry-run | outputs/semantic_eval/api_xgo_ing_phase1_3c_focused_80_20260518_085340 | Chinese 0.5, garbage 0, failures 2, clusters undefined |
| 300 dry-run | outputs/semantic_eval/api_xgo_ing_phase1_3c_full_300_20260518_085900 | Chinese 0.5143, garbage 0, failures 8, clusters undefined, suspect undefined |
| Scoped rehearsal | outputs/semantic_eval/api_xgo_ing_phase1_3c_rehearsal_real_20260518_092400 | REAL WRITE attempted; backup created; FAILED scope audit due source_profiles outside scope |

## Before / After Metrics
| Metric | 1.3b 300 | 1.3c 300 |
| chinese_event_detection_rate | 0.3846 | 0.5143 |
| accepted_garbage_product_count | >0 | 0 |
| final_failures | 31 | 8 |
| item_relation_json_failures | 28 | 3 |
| tokens_per_item | 2923.8 | 2250.98 |
| item_relation_token_share | 0.615 | 0.421 |
| effective_multi_item_clusters | 2 |  |
| suspect_multi_item_clusters | 0 |  |
| must_run_skip_count | 0 | 0 |
| pair_conflicts | 0 |  |

## Readiness Gates
Dry-run hard gates passed on the fresh 300-item run. The real-write rehearsal gate failed because source profile recomputation wrote outside the allowed api.xgo.ing scope.

## Real DB Writes
- ingest-source-scope: NO
- semantic --write-real-db: YES, 30-item scoped rehearsal command only
- scoped rehearsal: RUN, but FAILED safety audit
- backup path: /Users/wangrundong/work/infomation-center/content_inbox/data/backups/content_inbox_semantic_phase1_3_20260518_092401.sqlite3
- rollback: `cp /Users/wangrundong/work/infomation-center/content_inbox/data/backups/content_inbox_semantic_phase1_3_20260518_092401.sqlite3 /Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3`

## Remaining Blockers
- Scope source profile recomputation to selected api.xgo.ing sources before any future real write. Current rehearsal changed 318 source_profiles outside api.xgo.ing.
- Make the rehearsal readiness report distinguish real-write success from dry-run sample quality, then rerun a clean 20-50 item rehearsal.

## Recommended Next Step
Patch `recompute_source_profiles` or evaluation orchestration so real-write rehearsals recompute only sampled/source-scoped profiles, restore from backup if desired, then rerun the 30-item rehearsal.
