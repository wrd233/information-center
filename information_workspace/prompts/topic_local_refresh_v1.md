# topic_local_refresh_v1

Version: 1

## Task

Generate a candidate replacement for one Topic node using that node's current content, relevant materials, optional new materials, and a natural-language instruction.

## Input Variables

- `topic`
- `node`
- `node_constraint`
- `include_new_materials`
- `materials`

## Output JSON Schema

```json
{
  "node": {
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
  },
  "applied_constraint": "string",
  "verification_points": ["string"],
  "notes": "string"
}
```

## Rules

- Refresh only the requested node and its children.
- Respect the node constraint.
- Mark unsupported or conflicting claims as `to_verify`.
- Do not update the whole Topic structure directly.

## Semantic Quality Checks

- Candidate stays inside node scope.
- Important new material is either incorporated or explained.
- User wording is not overwritten without reason.
