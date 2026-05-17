# Phase 1.3 Final Summary

## Verdict

**NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE**

No real semantic DB write or scoped write rehearsal was run because readiness gates failed.

## Key Outcomes

- Final prompt-fix live run: 20 items, 11 calls, 35301 tokens (1765.05 tokens/item), zero LLM errors.
- Larger recall run: 80 items, 141955 tokens (1774.438 tokens/item), no must-run skips, no pair conflicts.
- Item-card emergency heuristic fallback stayed at 0 in the successful live runs; deterministic minimal cards are now tracked separately.
- Candidate priority is no longer inflated into must-run; low-only relation sets and weak cluster seeds are skipped with evidence.
- Relation canonicalization and action mapping are implemented for duplicate, near_duplicate, related_with_new_info, same_product_different_event, same_thread, different, and uncertain.

## Remaining Blockers
- event_signature_valid_rate: value `0.0`, threshold `>= 0.7`.
- effective_multi_item_clusters: value `0`, threshold `>= 1`.
- small_scoped_real_write_rehearsal: value `False`, threshold `True`.

## Real DB Writes

- ingest-source-scope: NO
- semantic --write-real-db: NO
- backup paths: none created; no real write was attempted
- rollback: restore from pre-existing DB backup if manually writing outside this run; no rollback needed for this phase output

## Report Files

- semantic_quality_report.md
- semantic_quality_summary.json
- phase1_3_readiness_report.md
- phase1_3_complexity_control_report.md
- event_signature_quality_report.md/json
- cost_quality_metrics.json
