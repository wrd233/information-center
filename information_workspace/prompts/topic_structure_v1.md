# topic_structure_v1

Version: 1

## Task

Generate a candidate Topic structure around the user's goal and organization requirements using Topic materials and referenced Events.

## Input Variables

- `topic`
- `current_structure`
- `materials`
- `new_materials_since_refresh`
- `referenced_events`
- `user_constraints`

## Output JSON Schema

```json
{
  "structure": {
    "title": "string",
    "nodes": [
      {
        "id": "string",
        "title": "string",
        "items": [
          {
            "type": "fact|opinion|idea|material|to_verify",
            "text": "string",
            "material_ids": ["string"]
          }
        ],
        "children": []
      }
    ]
  },
  "material_groups": [
    {"name": "string", "material_ids": ["string"], "reason": "string"}
  ],
  "verification_points": ["string"],
  "conflict_points": ["string"],
  "notes": "string"
}
```

## Rules

- Reorganize around the user's goal, not around source order.
- Do not treat user thoughts as facts.
- Do not invent evidence. Use material IDs for support.
- Keep node/item types to the allowed set.
- Existing user-edited structure is protected; generate a candidate, not an overwrite.

## Semantic Quality Checks

- Structure is useful for the stated goal.
- Claims have material support where possible.
- Conflicts and weak evidence are marked as to-verify or conflict points.
