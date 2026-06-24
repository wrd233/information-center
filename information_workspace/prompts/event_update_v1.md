# event_update_v1

Version: 1

## Task

Update an official Event center description only when new materials add meaningful facts, changes, conflicts, or open questions.

## Input Variables

- `event`
- `current_center_description`
- `new_materials`
- `user_focus`

## Output JSON Schema

```json
{
  "has_meaningful_update": true,
  "center_description": {
    "main_thread": "string",
    "known_facts": ["string"],
    "recent_changes": ["string"],
    "open_questions": ["string"]
  },
  "update_reason": "string",
  "supporting_material_ids": ["string"],
  "no_new_info_material_ids": ["string"],
  "conflict_notes": ["string"]
}
```

## Rules

- Preserve user focus and user judgments.
- Do not rewrite the center description unless the new materials justify it.
- Keep the center description short and structured.
- Record no-new-info material IDs separately.

## Semantic Quality Checks

- Every recent change has supporting material.
- Open questions are uncertainty, not invented speculation.
- Conflicts are marked instead of flattened.
