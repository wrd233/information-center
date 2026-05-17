# Phase 1.3b Complexity Delta

```json
{
  "modules_added": [
    "tests/test_semantic_signature_fixtures.py",
    "tests/test_semantic_relation_fixtures.py",
    "tests/test_semantic_cluster_fixtures.py"
  ],
  "modules_modified": [
    "app/semantic/signatures.py",
    "app/semantic/candidates.py",
    "app/semantic/relation_policy.py",
    "app/semantic/cluster_policy.py",
    "app/semantic/clusters.py",
    "app/semantic/evaluate.py",
    "app/semantic/readiness.py",
    "app/semantic/config.py",
    "app/semantic/schemas.py",
    "app/semantic/relations.py"
  ],
  "prompt_versions_active": [
    "item_card_v1",
    "item_relation_v3",
    "item_cluster_relation_v3",
    "cluster_card_patch_v1",
    "event_signature_v1"
  ],
  "active_relation_labels": [
    "near_duplicate",
    "related_with_new_info",
    "same_product_different_event",
    "same_thread",
    "different",
    "low_signal",
    "uncertain"
  ],
  "active_thresholds": {
    "event_signature_valid_rate": ">=0.6",
    "chinese_event_detection_rate": ">=0.5",
    "effective_multi_item_clusters": ">=1",
    "suspect_multi_item_clusters": "0",
    "must_run_skip_count": "0",
    "pair_conflicts": "0"
  },
  "remaining_complexity_debt": [
    "LLM-backed signature extraction prompt exists but the production pipeline still relies mostly on deterministic extraction plus item-card LLM context.",
    "Product validation still allowed garbage products in the completed 300 run before the final tightening patch; rerun required.",
    "Candidate volume remains high at 8996 generated pairs for 300 items."
  ]
}
```
