# Phase 1.3c Prompt Contract Repair Recommendations

## Problem

The 300-run had 31 final LLM failures, all from deepseek-v4-flash JSON parse errors. 28 of 31 failures were in `item_relation` stage, where the model must output structured JSON for multiple item pairs.

## Repair Recommendations by Priority

### P0: Fix JSON Output Reliability (addresses 29/31 failures)

1. **Strict JSON mode**: Ensure API calls use `response_format: { type: "json_object" }` or equivalent for deepseek-v4-flash
2. **Reduce batch size**: The `short` prompt variant batches 8-9 pairs per call. Reduce to 4-5 pairs max to reduce output complexity and truncation risk
3. **Increase max_tokens**: The current output token limits may be too low for 8-pair batches — increase by 50%
4. **Add JSON repair fallback**: Already have `json_repair_used` field but `json_repair` stage had 0 calls — the repair path may not be triggered properly for these error types
5. **Add explicit JSON formatting example** in prompt: Show the exact JSON structure expected with correct quoting

### P1: Schema Relaxation for Better Parsing (addresses 2/31 schema validation failures)

1. Accept both string and list for `new_information` and `same_event_evidence` fields
2. Auto-coerce single strings to list in post-processing

### P2: Retry Strategy Improvements

Current retry stats from metrics:
- repair_retry_count: 31 (one per failure)
- single_retry_success_count: 15 (about half succeed on retry)
- split_retry_success_count: 0

Recommendations:
1. **Split retry for item_relation failures**: When a batch of 8 pairs fails JSON parse, split into 2 batches of 4
2. **Increase retry count**: Allow 2 retries for JSON parse errors before marking as final failure
3. **Temperature reduction on retry**: Lower temperature to 0.0 on retry for more deterministic JSON output

### P3: Model Selection

If json repair and retry improvements don't resolve:
1. Try `deepseek-v4` (non-flash) for item_relation — slower but more reliable JSON
2. Consider adding a JSON-only validation pass before accepting LLM output
3. Add `json_repair` tool fallback for unterminated strings (autoclose quotes)

## Failure Category → Fix Mapping

| Failure Category | Count | Primary Fix |
|---|---|---|
| json_unterminated_string | 18 | Increase max_tokens + split retry |
| json_empty_or_non_json_output | 5 | Strict JSON mode + retry |
| json_missing_comma | 3 | JSON repair fallback |
| json_unquoted_property | 3 | JSON repair fallback |
| schema_validation_error | 2 | Schema relaxation (string→list coerce) |
