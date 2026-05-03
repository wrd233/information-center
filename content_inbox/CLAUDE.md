# Claude Code Guide For content_inbox

## Responsibility

`content_inbox` is the active content-processing module. It receives RSS feeds or manually supplied content items, standardizes them, deduplicates them, optionally screens them with an OpenAI-compatible chat model, clusters related events with embeddings, stores results in SQLite, and exposes APIs for querying the inbox.

It is not a reader UI, push system, Obsidian archive, video transcription service, or full task queue.

## Core Processing Chain

```text
RSS URL or content payload
  -> ContentAnalyzeRequest
  -> normalize_content
  -> build_dedupe_key
  -> SQLite dedupe lookup
  -> screen_content when screen=true
  -> cluster_content when configured and scores qualify
  -> SQLite insert/update
  -> API response or inbox query
```

RSS and single-content inputs share `process_content`; RSS first converts feed entries to content requests.

## Core Files

- `app/server.py`: FastAPI app, `/health`, `/api/content/analyze`, `/api/rss/analyze`, `/api/rss/analyze-batch`, and `/api/inbox`.
- `app/models.py`: Pydantic request/response and normalized content models.
- `app/rss.py` and `app/rss_runner.py`: RSS/Atom fetching, entry parsing, and per-source analysis.
- `app/processor.py`: normalization, dedupe key creation, screening, clustering, and storage orchestration.
- `app/screener.py`: chat-completions screening, prompt calls, schema handling, and score policy.
- `app/embedding.py`: OpenAI-compatible embedding client.
- `app/clusterer.py`: event clustering, duplicate/incremental decisions, and notification decisions.
- `app/storage.py`: SQLite schema, dedupe, item persistence, cluster persistence, and inbox queries.
- `app/batch_runner.py`: service-side multi-source RSS batch handling with source-level concurrency.
- `scripts/run_rss_sources_to_content_inbox.py`: external batch runner that selects RSS sources, calls the API, supports resume/dry-run, and writes reports.

## API And Service Startup

Local development:

```bash
cd content_inbox
PYTHONPATH=. python3 -m app.server
```

Default service address:

```text
http://127.0.0.1:8787
```

Docker, only after user confirmation:

```bash
cd content_inbox
docker compose up -d --build
docker compose ps
docker compose down
```

The compose file reads `.env`, sets `CONTENT_INBOX_DB=/data/content_inbox.sqlite3`, and mounts `./data:/data`. Do not read `.env` or inspect `data/`.

## Batch Script

The batch script can be used for planning and controlled RSS processing:

```bash
python3 scripts/run_rss_sources_to_content_inbox.py --dry-run
```

Important behavior:

- Default RSS source CSV is `rsshub/rss_opml/rss_sources.csv`.
- Default output directory is `content_inbox/outputs`.
- Run artifacts are written under `content_inbox/outputs/runs/rss_run_*`.
- `--concurrency` controls concurrent sources; the default is `1`.
- `--resume` continues the latest run with `run_state.json`.
- `--skip-known-failed` consults prior run failures.
- Real runs call the local API and can mutate the SQLite database. Ask before running them.

## Config And Prompts

- `config/content_inbox.yaml`: LLM, screening, score policy, embedding, clustering, and notification tuning.
- `config/reading_needs.yaml`: user-facing reading needs used by matching and inbox views.
- `config/watch_topics.yaml`: long-running topics/keywords for matching.
- `prompts.yaml`: required prompt blocks: `basic_screening`, `need_matching`, and `incremental`.
- `.env`: local secret/runtime configuration. Never read it.

## Tests

Primary command:

```bash
cd content_inbox
PYTHONPATH=. pytest -q
```

Focused tests:

```bash
PYTHONPATH=. pytest -q tests/test_api.py
PYTHONPATH=. pytest -q tests/test_reading_needs.py
PYTHONPATH=. pytest -q tests/test_run_rss_sources_script.py
```

## Notes And Risks To Verify

- README examples mention `CONTENT_INBOX_DEEPSEEK_BASE_URL`, while `app/config.py` gives `CONTENT_INBOX_OPENAI_BASE_URL` precedence over `CONTENT_INBOX_DEEPSEEK_BASE_URL`. Check env precedence before changing model config.
- `config/content_inbox.yaml` has model/base URL defaults, but environment variables can override them at runtime.
- Docker uses `.env` and `./data`; local Python startup loads `content_inbox/.env` and defaults the DB to `content_inbox/data/content_inbox.sqlite3`.
- Embedding dimensions must match the SQLite vec table. Changing embedding model or dimensions may require a controlled data migration.
- Batch runs and service calls can create or update local runtime data. Use dry-run first and ask before real processing.

## Modification Rules

- Do not modify business logic without first explaining the plan and affected files.
- Do not change `prompts.yaml`, RSS source CSVs, Docker configuration, or runtime paths unless explicitly requested.
- Do not read or modify `data/**` or `outputs/runs/**`.
- Keep API behavior compatible unless the user asks for a breaking change.
- Preserve source-internal RSS ordering and be careful with global dedupe/cluster state.
- Add or update focused tests when changing processing, API, config loading, batch behavior, or storage logic.
