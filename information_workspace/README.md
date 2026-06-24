# information_workspace

## What It Is

`information_workspace` is an independent information workbench in this repository. It accepts screened materials through an API, stores them in a long-term Material library, processes ingest runs, creates Event and Topic workspaces, and exports Markdown evidence packages for deeper analysis.

## What It Is Not

It is not a submodule of `content_inbox`, not an RSS reader, and not a demo frontend over hard-coded data. The backend, frontend, API, SQLite database, prompts, synthetic corpus, tests, and reports are independent.

## Quick Start

```bash
cd information_workspace
python3 -m app.main
```

The backend serves the API and the static frontend at `http://127.0.0.1:8788/`.

## Configure DeepSeek `.env`

Copy `.env.example` to local `.env` and fill only local secrets:

```bash
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-v4-flash
```

Never commit `.env`, API keys, trace outputs, databases, or generated reports.

## Import Synthetic Materials

```bash
cd information_workspace
python3 fixtures/synthetic_materials/generate_synthetic_materials.py
python3 fixtures/synthetic_materials/validate_synthetic_materials.py fixtures/synthetic_materials/synthetic_materials_500.jsonl
python3 scripts/import_synthetic.py --file fixtures/synthetic_materials/synthetic_materials_500.jsonl --auto-process
```

The import script calls the same upload/process API used by the frontend and external agents.

## Run Processing Pipeline

```bash
curl -s -X POST http://127.0.0.1:8788/api/runs/<run_id>/process
```

The run detail API and frontend show each step, counts, logs, material IDs, candidate Event IDs, and trace/report paths.

## Run `prompt_eval`

```bash
cd information_workspace
python3 scripts/prompt_eval.py --task light_understanding --fixture-file fixtures/synthetic_materials/synthetic_materials_500.jsonl --limit 20
```

By default prompt evaluation expects a real DeepSeek key. Test-only mock mode must be explicit and cannot count as final READY validation.

For the READY gate, run the real validation helper after local `.env` is configured:

```bash
python3 scripts/run_real_deepseek_validation.py --all-light --import-sample
python3 scripts/final_validation.py
```

## Run Tests

```bash
cd information_workspace
PYTHONPATH=. pytest -q
python3 scripts/run_api_smoke.py --allow-mock-llm
python3 frontend/smoke_frontend.py --allow-mock-llm
```

## View Reports

- Current status: [`STATUS.md`](STATUS.md)
- Latest final validation: `outputs/test_runs/20260624T193217669321Z/final_validation_report.md`
- Latest test run summary: `outputs/test_runs/20260624T193217669321Z/summary.md`
- Latest real DeepSeek validation: `outputs/test_runs/20260624T185342712666Z/real_deepseek_validation.md`
- Latest API smoke: `outputs/test_runs/20260624T193218398341Z/summary.md`
- Latest frontend smoke: `outputs/test_runs/20260624T193218660Z/frontend_smoke_summary.md`
- Latest prompt evals with real DeepSeek:
  - light understanding: `outputs/prompt_evals/20260624T185342712834Z/summary.md`
  - Event candidate: `outputs/prompt_evals/20260624T190729729247Z/summary.md`
  - Topic structure: `outputs/prompt_evals/20260624T190945023363Z/summary.md`
- Latest export sample: `outputs/exports/20260624T193218436883Z/topic_API_Smoke_Topic.md`
- Synthetic corpus report: [`fixtures/synthetic_materials/REPORT.md`](fixtures/synthetic_materials/REPORT.md)

## Documentation Map

- Requirements: [`docs/requirements.md`](docs/requirements.md)
- Design: [`docs/design.md`](docs/design.md)
- API: [`docs/api.md`](docs/api.md)
- LLM prompts: [`docs/llm-prompts.md`](docs/llm-prompts.md)
- Synthetic corpus: [`docs/synthetic-corpus.md`](docs/synthetic-corpus.md)
- Testing: [`docs/testing.md`](docs/testing.md)
- User guide: [`docs/user-guide.md`](docs/user-guide.md)
- Operations: [`docs/operations.md`](docs/operations.md)
- Decisions: [`docs/decisions.md`](docs/decisions.md)

## Current Status

Current status is `READY`. Final validation passed with DeepSeek configured, 520 fixture rows imported through the upload API, 507 de-duplicated synthetic materials in SQLite, and 507 successful real DeepSeek `light_understanding` results. The full API import run IDs are `run_3a68120a8cc54c68`, `run_5edfe16837c84728`, `run_a5208735ea2e4992`, and `run_20854593620d4078`.
