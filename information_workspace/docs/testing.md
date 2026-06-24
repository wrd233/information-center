# Testing

## Purpose

Testing proves behavior with real commands, API calls, reports, traces, and export files.

## Report Directory

Every validation run writes:

```text
outputs/test_runs/<timestamp>/summary.md
```

Final validation additionally writes `final_validation_report.md`.

## Commands

```bash
PYTHONPATH=. pytest -q
python3 scripts/run_api_smoke.py --allow-mock-llm
python3 frontend/smoke_frontend.py --allow-mock-llm
python3 fixtures/synthetic_materials/validate_synthetic_materials.py fixtures/synthetic_materials/synthetic_materials_500.jsonl
python3 scripts/run_real_deepseek_validation.py --all-light --import-sample
python3 scripts/final_validation.py
```

Mock LLM flags are for unit/smoke stability only. They must be reported as mock and cannot justify READY.

## Required Coverage

Backend tests cover schema initialization, upload validation, source type enum, URL optionality, run creation, run steps, dedupe, ignore/restore, search, details, Event candidate/promote, Topic creation/refresh, exports, and synthetic cleanup.

API smoke covers actual HTTP calls for upload, run process, run detail, Material search/detail, Event, Topic, and export.

Frontend smoke covers homepage, upload, run detail, search, material detail, add to Topic, create Event, candidate promotion, Topic refresh, and Markdown export.

## DeepSeek Validation

Final READY requires real DeepSeek light understanding, Event, Topic, prompt_eval traces, semantic quality review, and prompt iteration evidence. If the key is missing or calls fail, status is PARTIAL or BLOCKED.

`scripts/final_validation.py` now scans output traces and requires successful real `provider=deepseek` traces for `light_understanding`, `event_candidate`, and `topic_structure`.

## Prompt Eval

Prompt eval reports must cover applicable synthetic groups and record expected count, actual count, skipped groups, semantic issues, prompt versions, and trace paths.

## Export Checks

Export validation opens generated Markdown and checks AI-use instructions, snapshot, references, source appendices, duplicate/similar handling, unreferenced supplemental materials, Event-expanded evidence, and no URL markers.

## Leak Checks

Validation searches reports and traces for `DEEPSEEK_API_KEY`, `Authorization`, `.env`, and obvious key patterns. Real keys must not appear in git diff, outputs, trace files, or API responses.

## Verdicts

`READY` requires every hard gate to pass. `PARTIAL` means usable work exists but one or more required gates are incomplete. `BLOCKED` means progress requires external input such as a valid API key, network access, or user confirmation.
