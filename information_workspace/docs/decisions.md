# Decisions

This file records lightweight ADRs for `information_workspace`. Each decision is binding until superseded by a later ADR.

## ADR-001: Create A Parallel `information_workspace`

Status: Accepted

Context: The existing `content_inbox` module is historical input infrastructure and should not constrain the new high-level workbench.

Decision: Create `information_workspace/` at the repository root, parallel to `content_inbox/`.

Reason: The new system needs its own API, database, frontend, prompts, and validation flow.

Consequences: Existing modules may be referenced for context but are not runtime dependencies.

Validation: Repository layout and imports must show no dependency on `content_inbox` internals.

## ADR-002: Fully Independent Runtime

Status: Accepted

Context: The workbench needs independent deployability and verification.

Decision: Build independent backend, frontend, API, SQLite database, tests, prompts, fixtures, and outputs.

Reason: Independence prevents old schemas and UI assumptions from leaking into the new workspace.

Consequences: All features need local docs, scripts, and tests.

Validation: Backend starts from `information_workspace`, frontend assets live under `frontend/`, and the database is under `data/`.

## ADR-003: API-First Input With Ingest Runs

Status: Accepted

Context: Future schedulers, agents, and people must submit data through one contract.

Decision: Single and batch uploads create ingest runs and return `run_id`; processing is explicit and step-based.

Reason: Runs make validation, dedupe, LLM traces, Event candidates, and failures auditable.

Consequences: Frontend upload and scripts call the same API instead of writing SQLite directly.

Validation: Synthetic import and smoke tests use upload/process APIs.

## ADR-004: Single SQLite Business Database

Status: Accepted

Context: First release should be locally operable without a multi-service data stack.

Decision: Store business state in one SQLite database, defaulting to `data/information_workspace.db`.

Reason: SQLite is enough for Material, Event, Topic, export, and run metadata in the first version.

Consequences: Synthetic data must be marked and cleanable because it can share the same database.

Validation: Schema initialization is idempotent and schema version is queryable.

## ADR-005: Outputs Hold Reports And Traces

Status: Accepted

Context: Test runs, prompt evals, and full LLM traces can be large and may contain sensitive context.

Decision: Store reports and traces in `outputs/`, not in the business database.

Reason: The database keeps business state; artifacts remain easy to inspect and ignore from git.

Consequences: Database rows store trace/report paths and summaries only.

Validation: `.gitignore` excludes outputs and tests assert trace paths are external files.

## ADR-006: Real DeepSeek For Business LLM

Status: Accepted

Context: Mock semantic output cannot validate the actual information workflow.

Decision: Use DeepSeek with default model `deepseek-v4-flash` for business LLM calls.

Reason: Final READY requires real model output, semantic checks, and prompt iteration evidence.

Consequences: Missing API key causes business LLM steps to fail clearly. Test fakes are explicit and cannot count as READY.

Validation: LLM summaries record provider/model/prompt/trace and reports distinguish `deepseek` from `mock`.

## ADR-007: Versioned Prompt Files

Status: Accepted

Context: Prompt quality is part of the product, not hidden implementation detail.

Decision: Store prompts in `prompts/`, each with version, input contract, output schema, constraints, and quality checks.

Reason: Prompt eval and reprocess reports need stable prompt identities.

Consequences: Code loads prompt files and records version/hash metadata.

Validation: Tests verify prompt files exist and can be loaded.

## ADR-008: Schema-Bound LLM Output With Repair

Status: Accepted

Context: LLM output may be invalid, incomplete, or semantically unsafe.

Decision: JSON tasks parse, validate, run semantic checks, and use bounded repair/retry before state writes.

Reason: Invalid or invented results must not silently enter business state.

Consequences: Failed LLM steps are visible in run logs and traces.

Validation: Tests cover invalid facets and repair failure boundaries.

## ADR-009: Minimal Fields And Field Review

Status: Accepted

Context: The first schema should support behavior without premature taxonomy.

Decision: Keep Material understanding in compact JSON and limit facets to `news`, `article`, `opinion`, `technical`, `noise`, `uncertain`.

Reason: Extra fields require clear writers, readers, pages, APIs, prompts, and tests.

Consequences: No entity, keyword, sentiment, stance, or topic-label columns in v1.

Validation: Schema inspection and tests reject unsupported facets.

## ADR-010: 500+ Synthetic Materials As Test Asset

Status: Accepted

Context: The workflow needs broad, repeatable coverage before real daily use.

Decision: Maintain `fixtures/synthetic_materials/synthetic_materials_500.jsonl` with metadata for fixture group, purpose, expected behavior, and synthetic flag.

Reason: Stable fixtures support API, pipeline, Event, Topic, export, and prompt_eval regression checks.

Consequences: Generated materials must not pretend to be real news.

Validation: Validator enforces count, schema, grouping, lengths, duplicates, no-url, missing-time, and domain coverage.

## ADR-011: Documentation First

Status: Accepted

Context: The goal requires docs, implementation, and tests to agree.

Decision: Maintain README, STATUS, and docs before and during implementation.

Reason: READY depends on current operating instructions and validation evidence.

Consequences: Every implementation phase updates docs and STATUS.

Validation: Final validation checks docs against commands and APIs.

## ADR-012: Honest READY / PARTIAL / BLOCKED

Status: Accepted

Context: The goal explicitly forbids pretending a partial build is done.

Decision: Mark final status `READY` only when all hard gates pass; otherwise `PARTIAL` or `BLOCKED`.

Reason: Missing LLM, frontend, synthetic, export, or report validation changes real readiness.

Consequences: STATUS and test reports must list unfinished work and skipped checks.

Validation: Final report includes the verdict and evidence paths.
