# Semantic Schema Reference

New tables:

- `item_cards`: current/versioned semantic card per item.
- `item_relations`: second-layer item-item relation.
- `cluster_items`: third-layer item-cluster relation.
- `cluster_cards`: current/versioned event cluster card.
- `cluster_relations`: follow-up/same-topic links between clusters.
- `source_signals`: item-level source value signals.
- `source_profiles`: source-level LLM priority profile.
- `llm_call_logs`: auditable semantic LLM call logs.
- `review_queue`: pending human review actions.

`inbox_items` additions are intentionally light: `semantic_status`, `primary_cluster_id`, `semantic_error`, `semantic_attempts`, `last_semantic_at`.

Relation shape:

```json
{"primary_relation":"single enum","secondary_roles":["optional tags"]}
```

Item-item primary enum:

```text
duplicate, near_duplicate, related_with_new_info, different, uncertain
```

Item-cluster primary enum:

```text
source_material, repeat, new_info, analysis, experience, context, follow_up, same_topic, unrelated, uncertain
```

Source profile metric notes:

- `source_material_rate` measures original/authoritative material rate.
- `new_event_rate` measures new event contribution rate.
- `source_item_rate` is retained as a compatibility alias for source-material rate in Phase 1.1.
- `llm_total_tokens` is attributed from `llm_call_logs.source_id`, `llm_call_logs.item_id`, or `llm_call_logs.cluster_id` when available. Unattributed historical calls remain unassigned.
