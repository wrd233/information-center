# json_repair_v1

Version: 1

## Task

Repair malformed JSON from a previous model response so it conforms to the requested schema.

## Input Variables

- `task_name`
- `schema_description`
- `invalid_output`
- `validation_error`

## Output

Return only repaired JSON. Do not wrap in Markdown.

## Rules

- Repair syntax, types, missing required fields, and enum values.
- Do not introduce new facts.
- Do not change semantic judgments except where needed to map invalid enums to allowed values.
- If information is unavailable, use an empty string, empty list, `false`, or `null` as appropriate to the schema.

## Semantic Quality Checks

- Repaired JSON is parseable.
- Required fields exist.
- Allowed enums are respected.
