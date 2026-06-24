# export_package_v1

Version: 1

## Task

Review an export evidence package for clarity, evidence chain, duplication handling, and unsupported claims. The final Markdown is assembled by code from database evidence.

## Input Variables

- `object_type`
- `object_snapshot`
- `materials`
- `structure_or_center_description`

## Output JSON Schema

```json
{
  "quality_notes": ["string"],
  "missing_evidence": ["string"],
  "duplication_warnings": ["string"],
  "open_questions": ["string"]
}
```

## Rules

- Do not create the final export text from scratch.
- Do not add facts not present in materials.
- Focus on evidence quality and gaps.

## Semantic Quality Checks

- References are traceable.
- Duplicates are identified.
- No URL materials are clearly marked.
