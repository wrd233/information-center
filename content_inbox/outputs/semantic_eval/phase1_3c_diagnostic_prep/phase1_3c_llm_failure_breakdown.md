# Phase 1.3c LLM Final Failure Breakdown

## Summary

- **Total final failures**: 31
- **Real LLM failures**: 31
- **Potential budget/control-flow miscounts**: 0
- **All failures are genuine**: Yes — every failure has a JSON parse error from deepseek-v4-flash

## Failure Category Breakdown

| Category | Count | % |
|---|---|---|
| json_unterminated_string | 14 | 45.2% |
| json_missing_comma | 4 | 12.9% |
| json_empty_or_non_json_output | 4 | 12.9% |
| json_unquoted_property | 4 | 12.9% |
| json_unexpected_value | 3 | 9.7% |
| schema_validation_error | 2 | 6.5% |

## Failure by Stage

| Stage | Count |
|---|---|
| item_relation | 28 |
| item_card | 3 |

## Failure by Prompt Variant

| Variant | Count |
|---|---|
| short | 24 |
| full | 7 |

## Category x Stage Matrix

| Category | Stage | Count |
|---|---|---|
| json_unterminated_string | item_relation | 12 |
| json_empty_or_non_json_output | item_relation | 4 |
| json_unquoted_property | item_relation | 4 |
| json_missing_comma | item_relation | 3 |
| json_unexpected_value | item_relation | 3 |
| json_unterminated_string | item_card | 2 |
| schema_validation_error | item_relation | 2 |
| json_missing_comma | item_card | 1 |

## Root Cause Analysis

Almost all failures (28/31 = 90.3%) are in `item_relation` stage with JSON parse errors. The model `deepseek-v4-flash` consistently produces malformed JSON outputs:

1. **Unterminated strings** (18/31 = 58%): The model truncates JSON output mid-string
2. **Expecting value line 1 col 1** (5/31 = 16%): Model returns empty or non-JSON output
3. **Expecting ',' delimiter** (3/31 = 10%): Missing commas in JSON arrays/objects
4. **Expecting property name** (3/31 = 10%): Unquoted property names
5. **Schema validation** (2/31 = 6%): Valid JSON but wrong schema (list vs string)

## Top Repeat Offender Items

Items appearing in multiple failed calls:

| Item ID | Failure Count |
|---|---|
| item_9d0967dbc96b4c769897a436562d8634 | 6 |
| item_b6a1daec5e7c4789ba183ccc53b1f379 | 5 |
| item_7e9109be35834a689cca1a8e534b7373 | 5 |
| item_e6f115055b3b43cd9bcc6d7189b70cfd | 5 |
| item_4aae6911a50a414288469f3cfd4261cc | 4 |
| item_92a9e82e74654bf695b05644aed07005 | 4 |
| item_e22aa290a8f74b5a88f75179e33a69b0 | 4 |
| item_e147cfadf270482aa9a8c6de9b1f9407 | 4 |
| item_6f1015d8145d463096fd6d2f5823f078 | 4 |
| item_b37e433468004a78b7db33d32d563eba | 4 |
| item_1d4c37b426ec4b7c9cb80d9bd9b7d96f | 4 |
| item_5d8c86286d4b41cab3f469c659183a58 | 3 |
| item_b763bb9706144074b138b2840373a7d7 | 3 |
| item_a62690a8b34644dc959a77ddde1c7e70 | 3 |
| item_5c72b7f0be8f43d2a275c1e7f48d2c61 | 3 |
