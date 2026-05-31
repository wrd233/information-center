# Semantic Schema Reference

Status: canonical current reference. Keep this file aligned with SQLite schema changes in `app/storage.py`.

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
- `event_candidate_pairs`: operational candidate audit trail, including priority, lane, relation outcome, evidence fields, LLM call id, schema version, creator, and input fingerprint.

Review apply fields:

- `review_queue.applied_at`: set when a review decision produced a pipeline side effect.
- `review_queue.applied_action`: short action name such as `event_relation_approved` or `eventness_rejected`.
- `review_queue.apply_result_json`: replayable result payload with affected event, cluster, item, or source profile identifiers.

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
- `discovery_value_avg` measures how often a source seeds trusted events or clusters.
- `fact_value_avg` measures source-material, official, cited-fact, or core-fact contribution.
- `incremental_value_avg` measures new-fact contribution to existing events.
- `interpretation_value_avg` measures analysis, context, risk, market, technical, or contrarian contribution.
- `duplicate_noise_rate` measures duplicate, near-duplicate, and repeat contribution.
- `non_event_noise_rate` measures digest, generic, low-signal, and content-only eventness rejections.
- `review_acceptance` measures accepted minus rejected review feedback normalized by review volume.
- `llm_total_tokens` is attributed from `llm_call_logs.source_id`, `llm_call_logs.item_id`, or `llm_call_logs.cluster_id` when available. Unattributed historical calls remain unassigned.
