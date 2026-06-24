# Design

## Purpose

This document describes the architecture, data flow, and module boundaries for `information_workspace`.

## Architecture

The project is a self-contained FastAPI backend, SQLite business database, static API-connected frontend, prompt assets, synthetic fixtures, and output artifact directories.

```text
frontend/ -> HTTP API -> app/ services -> SQLite data/
                         app/ LLM client -> DeepSeek -> outputs/llm_traces/
scripts/ -> same API/service paths -> outputs/test_runs/ and prompt_evals/
fixtures/synthetic_materials/ -> upload API -> ingest runs -> materials
```

## Backend Modules

- `app/config.py`: environment and path settings.
- `app/db.py`: SQLite connection, schema initialization, migrations.
- `app/schemas.py`: Pydantic request/response models and enums.
- `app/llm.py`: prompt loading, DeepSeek/mock clients, schema validation, traces.
- `app/service.py`: Material, run, Event, Topic, export, and prompt_eval business logic.
- `app/main.py`: FastAPI routes and frontend static serving.

## Data Flow

1. Upload API receives one or many Material inputs.
2. API creates an ingest run and raw run items.
3. Process API advances run steps.
4. Validation checks required fields and source type.
5. Dedupe chooses primary materials and records duplicate/similar relations.
6. Persist writes unique materials to SQLite.
7. Light understanding calls DeepSeek when configured, validates JSON, writes trace and compact result.
8. Candidate Event generation groups run materials and records candidates.
9. Active Event matching evaluates official Events and records updates or no-new-info support.
10. Finalize summarizes counts, trace paths, material IDs, candidate IDs, and errors.

## SQLite Scope

SQLite stores business state only: runs, run items, steps/logs, materials, relations, LLM summaries, Events, Event materials/updates, Topics, Topic materials, and export records. Reports and full traces stay in `outputs/`.

## LLM Chain

Prompts are loaded from `prompts/`. Each JSON task records prompt file, version/hash, model, provider, input IDs, rendered prompt, raw output, parse/validation status, repair attempts, semantic check, final status, and trace path.

## Prompt Eval Chain

`scripts/prompt_eval.py` samples materials from an ingest run, explicit IDs, or synthetic fixture groups. It runs the selected prompt task, stores traces under `outputs/prompt_evals/<timestamp>/llm_traces/`, and writes coverage plus semantic quality notes.

## Synthetic Corpus Chain

`generate_synthetic_materials.py` creates stable JSONL fixtures. `validate_synthetic_materials.py` verifies count, fields, groups, purposes, content lengths, duplicates, no URL, missing time, and domain ratio. `scripts/import_synthetic.py` uploads through the API and optionally processes the returned run.

## Event Model

Candidate and official Events share one table. Status controls behavior. Official Events keep short center descriptions and material references. Event updated time changes only for meaningful changes or user operations.

## Topic Model

Topics keep a material flow plus current and candidate structures. Refreshes use DeepSeek and generate candidates. Confirmation replaces the current structure. Local refresh operates on a selected node and records constraints.

## Why Not `content_inbox`

The old module uses its own ingestion, schema, and purpose. This workspace needs a new Material contract and workbench semantics, so no code path imports or writes `content_inbox` state.
