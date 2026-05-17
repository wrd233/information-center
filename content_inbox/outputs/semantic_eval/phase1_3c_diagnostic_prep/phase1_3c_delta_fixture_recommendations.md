# Phase 1.3c Delta Fixture Recommendations

The delta benchmark has 30 rows. Recommended fixture additions:

## Signature Fixture Additions

Add 30 rows to `tests/fixtures/semantic_signature_benchmark_phase1_3b.jsonl`:

- **delta_001**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'weak_action_without_entity'
- **delta_002**: Chinese false negative: likely_false_negative_thread. ['semantic_level_thread_signature']
- **delta_003**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'semantic_level_reject']
- **delta_004**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'semantic_level_reject']
- **delta_005**: Chinese false negative: likely_false_negative_thread. ['semantic_level_thread_signature']
- **delta_006**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'weak_action_without_entity'
- **delta_007**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'semantic_level_reject']
- **delta_008**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'weak_action_without_entity',
- **delta_009**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'semantic_level_reject']
- **delta_010**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'semantic_level_reject']
- **delta_011**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'semantic_level_reject']
- **delta_012**: Garbage product_or_model: 'sow0e7ym' — random_alphanumeric_token
- **delta_013**: Garbage product_or_model: 'May 4th' — contains_date_fragment, is_month_day_phrase
- **delta_014**: Garbage actor: 'google' — random_alphanumeric_token
- **delta_015**: Garbage actor: 'cursor' — random_alphanumeric_token

## Integration Test Cases

1. **Chinese FN regression**: Verify Chinese items with event triggers get event_signature not reject
2. **Garbage product regression**: Verify URL fragments, random tokens, dates are rejected as products
3. **Valid product protection**: Verify known products survive validator tightening
4. **Cluster member regression**: Verify cluster members maintain correct signatures

## What NOT to Add

- Don't hard-code item IDs/titles — use semantic patterns
- Don't overfit to 300-run specific items
- Focus on rule-based tests: trigger coverage, validator patterns, level classification
