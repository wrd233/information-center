# event_candidate_v1

Version: 1

## Task

Group current run materials into broad candidate Events representing external developments.

## Input Variables

- `run_id`
- `materials`
- `active_events`

## Output JSON Schema

```json
{
  "candidates": [
    {
      "title": "string",
      "material_ids": ["string"],
      "reason": "string",
      "confidence": 0.0,
      "possible_existing_event_id": "string|null",
      "doubts": ["string"]
    }
  ]
}
```

## Rules

- Candidate discovery should favor recall, but avoid grouping unrelated or noise-only materials.
- Background articles can support a candidate but should not become an Event without a development.
- Do not invent an Event that the materials do not support.
- Record doubts when materials are weakly related, conflicting, or mostly background.

## Semantic Quality Checks

- Same-event materials are grouped.
- Weakly related materials are not forced into one candidate.
- Noise is excluded unless needed to explain a false positive.
- Conflicting reports remain visible as doubts.
