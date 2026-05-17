# Phase 1.3 Readiness Report

- verdict: NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE
- ready: False

## Gates

- PASS heuristic_fallback_rate: value=0.0 threshold=< 0.1 reason=heuristic emergency fallback must stay low
- PASS parse_failure_fallback_rate: value=0.0 threshold=< 0.03 reason=parse failures must not dominate cards
- PASS budget_skip_fallback_rate: value=0.0 threshold=< 0.05 reason=budget fallback must not starve candidate-bearing cards
- PASS skipped_must_run_candidates: value=0 threshold=0 reason=must-run candidates are protected
- PASS pair_relation_conflicts: value=0 threshold=0 reason=canonical pair verdicts cannot conflict
- PASS db_lock_errors: value=0 threshold=0 reason=no DB lock errors
- PASS event_signature_valid_rate: value=1.0 threshold=>= 0.6 reason=signatures are concrete enough
- FAIL chinese_event_detection_rate: value=0.2 threshold=>= 0.5 reason=Chinese event-like items must not all be rejected
- PASS accepted_garbage_product_count: value=0 threshold=0 reason=URL/date/number/long-fragment products must be rejected
- FAIL effective_multi_item_clusters: value=0 threshold=>= 1 reason=dry-run produced useful same-event clusters
- PASS suspect_multi_item_clusters: value=0 threshold=0 reason=no suspect multi-item clusters accepted
- FAIL small_scoped_real_write_rehearsal: value=False threshold=True reason=production readiness requires a scoped write rehearsal

## Blockers

[
  {
    "name": "chinese_event_detection_rate",
    "passed": false,
    "reason": "Chinese event-like items must not all be rejected",
    "threshold": ">= 0.5",
    "value": 0.2
  },
  {
    "name": "effective_multi_item_clusters",
    "passed": false,
    "reason": "dry-run produced useful same-event clusters",
    "threshold": ">= 1",
    "value": 0
  },
  {
    "name": "small_scoped_real_write_rehearsal",
    "passed": false,
    "reason": "production readiness requires a scoped write rehearsal",
    "threshold": true,
    "value": false
  }
]
