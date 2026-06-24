# Synthetic Corpus

## Purpose

The synthetic corpus gives repeatable coverage for Material ingestion, dedupe, LLM light understanding, Event candidates, Topic structures, exports, frontend flows, and prompt evaluation.

## Fixture

Stable fixture path:

```text
fixtures/synthetic_materials/synthetic_materials_500.jsonl
```

Current generated count: 520 materials.

Each line is a Material upload object with required fields and metadata:

```json
{
  "synthetic": true,
  "fixture_group": "multi_day_event",
  "test_purpose": ["event_candidate", "event_update"],
  "expected_behavior": "cluster with related synthetic event"
}
```

## Coverage

The generator covers content types `news`, `article`, `opinion`, `technical`, `noise`, and `uncertain`, plus system behavior groups such as exact duplicate, near duplicate, multi-source same event, multi-day event, conflicting reports, weakly related event, no URL, missing time, Topic structure refresh, and export evidence.

About 70 percent of items are in AI/LLM/agent workflow, RSS/information systems, observability, port logistics, software architecture, and technical news domains. About 30 percent are broader topics.

## Commands

```bash
python3 fixtures/synthetic_materials/generate_synthetic_materials.py
python3 fixtures/synthetic_materials/validate_synthetic_materials.py fixtures/synthetic_materials/synthetic_materials_500.jsonl
python3 scripts/import_synthetic.py --file fixtures/synthetic_materials/synthetic_materials_500.jsonl --auto-process
```

## Reports

- Stable corpus report: `fixtures/synthetic_materials/REPORT.md`
- Test-run copy: `outputs/test_runs/<timestamp>/synthetic_corpus_report.md`

## Cleaning Synthetic Data

Use:

```bash
python3 scripts/cleanup_synthetic.py
```

The command calls service cleanup logic for synthetic Materials, ingest runs, Event candidates, Topic links, and export rows where possible. It reports remaining references if user-created entities depend on synthetic data.
