# User Guide

## What This Is

`information_workspace` is a local workbench for turning screened information into reusable Material, Event, Topic, and export assets.

## Start

```bash
cd information_workspace
python3 -m app.main
```

Open `http://127.0.0.1:8788/`.

## Configure DeepSeek

Create local `.env` from `.env.example` and fill `DEEPSEEK_API_KEY`. Do not paste the key into UI fields, documents, reports, or prompts.

## Upload Materials

Use the Upload view for a single item or JSONL batch. Upload returns an ingest run. Open the run detail and process it if auto-process is disabled.

## Run Detail

The run page shows each processing step, counts, errors, material IDs, candidate Event IDs, and trace/report paths. Failed LLM steps show an error summary.

## Search Library

Use the Material search view to find by keyword, source type, synthetic flag, noise, or ignored status. Results show title, source, time, summary/snippet, facets, and reference counts.

## Material Detail

The detail view emphasizes original text. It also shows URL or no-link status, light understanding, duplicate/similar relations, run source, Event/Topic references, and trace path.

Available actions: ignore/restore, reprocess light understanding, add to Topic, create Event, and export.

## Events

Candidate Events are shown separately from official Events. Promote a candidate when it represents a real external development. Ignoring a candidate does not ignore its materials.

Official Event detail shows the center description, recent changes, open questions, material references, and related Topics.

## Topics

Create a Topic with title, goal, and organization requirements. Add materials from search or detail. Refresh structure to produce a candidate structure; confirm it only after review. Local refresh can update one node with a specific instruction.

## Export

Use export buttons on Material, Event, or Topic pages. The system writes Markdown evidence packages under `outputs/exports/` and returns the file path.

## Reports

Status and recent reports are linked from the homepage, README, and STATUS. Generated reports live under `outputs/test_runs/` and `outputs/prompt_evals/`.
