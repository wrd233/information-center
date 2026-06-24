# Requirements

## Purpose

This document defines the required behavior of `information_workspace` and maps it to the goal pack. It is the product boundary for implementation and validation.

## Scope

The system stores screened information materials, processes ingest runs, applies light LLM understanding, creates Event and Topic workspaces, supports search and detail views, exports Markdown evidence packs, and leaves test/prompt traces under `outputs/`.

## Non-Goals

- Reusing `content_inbox` database, schema, API, or frontend.
- Replacing RSSHub/source management.
- Adding PostgreSQL, Redis, vector databases, or complex graph models in v1.
- Treating test mocks as business validation.

## Material Library

Materials are the long-term base unit. Required upload fields are `title`, `content_text`, `source_name`, and `source_type`. URL is optional. Source type is limited to `rss`, `web`, `wechat`, `upload`, `document`, `agent`, `api`, or `unknown`.

Materials store raw facts separately from interpretation. LLM understanding is compact JSON with `summary`, `content_facets`, `importance_reason`, and `uncertainties`.

## Ingest Runs

Single and batch uploads create ingest runs. Runs expose ordered steps: `validate_input`, `dedupe_compress`, `persist_materials`, `light_understanding`, `similarity_marking`, `candidate_events`, `active_event_matching`, and `finalize_run`.

Every step records status, counts, timing, messages, errors, and key decisions.

## LLM

Business LLM calls use real DeepSeek with model `deepseek-v4-flash`. Missing keys fail clearly. Unit tests may use explicit mock mode, and reports must label mock results.

## Events

Events represent external developments. States are `candidate`, `official`, and `sleeping`. Candidates are generated from run materials, promoted or ignored by users, and official Events have a compact center description with facts, recent changes, and open questions.

## Topics

Topics are user-goal containers with title, goal, organization requirements, material flow, current structure, latest candidate structure, and local refresh support. Structure refreshes produce candidates and do not overwrite user work until confirmed.

## Search And Details

The long-term library is search-first, with recent materials as support. Search supports keywords, status filters, synthetic filters, source type filters, and multi-select actions. Material details show original text first, plus source, URL/no-link status, light understanding, relations, Event/Topic references, run source, and trace path.

## Export

Material, Event, and Topic exports generate Markdown evidence packages under `outputs/exports/`. Exports include AI-use instructions, snapshots, structures or center descriptions, references, user judgments, conflicts, duplicate handling, and full source appendices.

## Frontend

The frontend lives under `frontend/` and only calls backend APIs. It must support upload, run detail, Material search/detail, ignore/restore, Event candidate and official workflows, Topic material flow and structure refresh, exports, and report links.

## Synthetic Corpus

At least 500 synthetic materials are maintained in JSONL, marked `synthetic=true`, grouped by content type and system behavior, validated by script, imported through the upload API, and used by prompt_eval and smoke checks.

## Testing And READY

READY requires passing backend tests, API smoke, frontend smoke, real DeepSeek semantic checks, prompt_eval coverage, synthetic import/validation, export checks, no key leakage, current docs, and STATUS. Otherwise the verdict must be PARTIAL or BLOCKED.
