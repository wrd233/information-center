# API

Base URL: `http://127.0.0.1:8788/api`

All APIs return JSON unless an export file is served separately. No API returns `.env`, API keys, or Authorization headers.

## Health

`GET /health`

Returns app name, version, database path, outputs path, configured model, whether a DeepSeek key appears configured, started time, and status summary.

## Upload Materials

`POST /materials`

Creates one ingest run with one item.

Request fields: `title`, `content_text`, `source_name`, `source_type`, optional `url`, `external_id`, `published_at`, `author`, `upstream_score`, `upstream_reason`, `metadata`, `raw_payload`, and `auto_process`.

`POST /materials/batch`

Creates one ingest run with multiple items. Invalid items are recorded on the run while valid items remain usable.

## Runs

`GET /runs`

Returns recent ingest run summaries, newest first. Used by the dashboard and run list.

`GET /runs/{run_id}`

Returns run status, counts, steps, logs, material IDs, candidate Event IDs, and trace/report path summaries.

`POST /runs/{run_id}/process`

Advances the run through validation, dedupe, persist, light understanding, similarity marking, Event candidate generation, active Event matching, and finalization.

`POST /runs/{run_id}/reprocess-light`

Re-runs light understanding for materials in the run. Debug mode writes a comparison report.

## Materials

`GET /materials`

Keyword and filter search. Query parameters include `q`, `run_id`, `include_ignored`, `include_noise`, `synthetic`, and `source_type`.

`GET /materials/{material_id}`

Returns original text, source, URL/no-link status, light understanding, duplicate/similar relations, Event/Topic references, run source, ignored/noise state, and trace path.

`POST /materials/{material_id}/ignore`

Soft-ignore a Material unless it would break protected references.

`POST /materials/{material_id}/restore`

Restore an ignored Material. This does not re-run Event or Topic processing.

`POST /materials/{material_id}/reprocess-light`

Re-runs light understanding for one Material and stores a new trace.

## Events

`GET /events?status=candidate|official|sleeping&include_sleeping=false`

Lists Events. Candidate Events are separate from official Events.

`POST /events/from-materials`

Creates an Event from selected material IDs and optional user focus.

`POST /events/{event_id}/promote`

Promotes a candidate to official and generates a minimum center description.

`POST /events/{event_id}/ignore-candidate`

Ignores the candidate without ignoring its materials.

`GET /events/{event_id}`

Returns center description, user focus, materials, updates, no-new-info support, related Topics, state, and log summary.

## Topics

`POST /topics`

Creates a Topic with title, goal, organization requirements, and optional initial material IDs.

`GET /topics`

Lists Topics with pinned-first, recent-updated sorting.

`GET /topics/{topic_id}`

Returns goal, organization requirements, material flow, current structure, candidate structure, unincorporated count, and referenced Events.

`POST /topics/{topic_id}/materials`

Adds Material IDs or Event IDs to a Topic material flow.

`POST /topics/{topic_id}/refresh-structure`

Uses DeepSeek to generate a candidate structure. It does not overwrite current structure.

`POST /topics/{topic_id}/confirm-candidate`

Replaces current structure with the latest candidate.

`POST /topics/{topic_id}/local-refresh`

Generates a candidate update for one node with optional natural-language constraints.

## Exports

`POST /exports/material`

Exports one or more materials as Markdown.

`POST /exports/event/{event_id}`

Exports Event center description, references, updates, and source appendices.

`POST /exports/topic/{topic_id}`

Exports Topic structure, referenced materials, supplemental materials, and expanded Event evidence.

## Prompt Eval

`POST /prompt-eval`

Runs a prompt-eval task over selected IDs, run ID, or synthetic fixture filters. Reports are written under `outputs/prompt_evals/<timestamp>/`.
