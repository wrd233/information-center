# Phase 1.3b Final Summary

## Verdict
NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE

## What Changed
- Implemented four-level semantic signatures and Chinese/English action triggers.
- Added Phase 1.3b fixture tests and stable fixture copies.
- Added semantic-level-aware candidate lanes and cluster seed restrictions.
- Added `event_signature_v1` prompt for the LLM-backed signature pass contract.

## Fixture Results
- Signature/relation/cluster fixtures: passing.
- Benchmark fixture FNR: 0.1739
- Benchmark fixture FPR: 0.0
- Benchmark Chinese event detection: 0.75

## Live Evaluation Results
- 20-item smoke: {'path': 'outputs/semantic_eval/api_xgo_ing_phase1_3b_smoke_20_20260517_233206', 'items': 20, 'tokens_per_item': 2201.35, 'event_signature_valid_rate': 1.0, 'chinese_event_detection_rate': 0.2, 'effective_multi_item_clusters': 0, 'suspect_multi_item_clusters': 0, 'pair_conflicts': 0, 'final_failures': 0}
- 80-item live dry-run: {'path': 'outputs/semantic_eval/api_xgo_ing_phase1_3b_live_80_20260517_233426', 'items': 80, 'tokens_per_item': 2720.95, 'event_signature_valid_rate': 1.0, 'chinese_event_detection_rate': 0.3214, 'effective_multi_item_clusters': 1, 'suspect_multi_item_clusters': 0, 'pair_conflicts': 9, 'final_failures': 9}
- 300-item live dry-run: {'path': 'outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600', 'items': 300, 'tokens_per_item': 2923.8, 'event_signature_valid_rate': 0.9821, 'valid_signature_rate_total_items': 0.3667, 'chinese_event_detection_rate': 0.3846, 'effective_multi_item_clusters': 2, 'suspect_multi_item_clusters': 0, 'pair_conflicts': 0, 'must_run_skip_count': 0, 'relations': {'different': 624, 'near_duplicate': 12, 'related_with_new_info': 1, 'same_product_different_event': 90, 'same_thread': 11, 'uncertain': 3}, 'final_failures': 31, 'parse_failures': 2, 'rate_limit_errors': 0, 'db_lock_errors': 0, 'actual_tokens': 877140, 'actual_calls': 220}

## Readiness Gates
Dry-run gates did not all pass. The generated 300-run readiness gate failed Chinese event detection; manual inspection also found accepted garbage-product examples in the 300-run evidence.

## Real DB Writes
- ingest-source-scope: NO
- semantic --write-real-db: NO
- scoped rehearsal: NOT RUN
- backup paths: none

## Key Metrics
- event_signature_valid_rate: 0.9821
- benchmark FNR/FPR: 0.1739 / 0.0
- chinese_event_detection_rate: 0.3846
- effective_multi_item_clusters: 2
- suspect_multi_item_clusters: 0
- tokens_per_item: 2923.8
- must_run_skip_count: 0
- pair_conflicts: 0

## Remaining Blockers
- Chinese event detection below gate.
- Garbage-product validation needs rerun after final validator tightening.
- Unit cost above target and 31 final LLM failures in 300 run.

## Recommended Next Step
Rerun a focused 80-item validation after the final validator tightening, then reduce relation prompt failure rate before any scoped real write.
