# Synthetic Materials Fixture

This directory contains a stable synthetic corpus for `information_workspace`.

## Files

- `synthetic_materials_500.jsonl`: stable upload fixture with at least 500 materials.
- `generate_synthetic_materials.py`: deterministic generator for rebuilding the fixture.
- `validate_synthetic_materials.py`: validator for schema, grouping, distribution, duplicates, and coverage.
- `REPORT.md`: generated coverage report.

## Required Fields

Each JSONL line is a Material upload object with:

- `title`
- `content_text`
- `source_name`
- `source_type`
- `metadata`

Optional fields include `url`, `external_id`, `published_at`, `author`, `upstream_score`, and `upstream_reason`.

## Metadata

Every item has:

```json
{
  "synthetic": true,
  "fixture_group": "multi_day_event",
  "test_purpose": ["event_candidate", "event_update"],
  "expected_behavior": "cluster with materials sharing event_key",
  "generated_by": "codex_goal_04"
}
```

## Import

Import through the real upload API path:

```bash
python3 scripts/import_synthetic.py --file fixtures/synthetic_materials/synthetic_materials_500.jsonl --auto-process
```

## Validate

```bash
python3 fixtures/synthetic_materials/validate_synthetic_materials.py fixtures/synthetic_materials/synthetic_materials_500.jsonl
```
