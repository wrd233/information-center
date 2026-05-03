# Claude Code Project Guide

## Project Positioning

This repository is a local personal information center. It currently contains several independent modules:

- `content_inbox/`: the active mainline. A FastAPI service that ingests RSS feeds or single content items, normalizes and deduplicates them, optionally screens them with an OpenAI-compatible LLM, clusters events with embeddings, stores results in SQLite, and exposes inbox query APIs.
- `rsshub/`: local RSSHub-related configuration, OPML/CSV source management, and helper scripts.
- `wechat-rss/`: WeChat RSS service/deployment files and local runtime data.
- `Video Transcript API/`: audio/video transcript API experiments and tests.

## Current Priority Mainline

Treat `content_inbox/` as the primary development surface unless the user explicitly asks for another module. Its current flow is:

```text
RSS feed or single content item
  -> parse/extract
  -> normalize
  -> dedupe
  -> AI screening
  -> embedding/event clustering
  -> SQLite storage
  -> inbox/report query
```

## Important Directories

- `content_inbox/app/`: FastAPI routes, RSS parsing, processing, screening, embeddings, clustering, and SQLite storage.
- `content_inbox/scripts/`: batch RSS submission tooling.
- `content_inbox/config/`: non-secret tuning files for scoring, reading needs, and watch topics.
- `content_inbox/docs/`: implementation notes and decision records.
- `content_inbox/tests/`: pytest coverage for APIs, reading needs, and batch scripts.
- `content_inbox/data/`: local SQLite/runtime data. Do not read or modify unless the user explicitly asks.
- `content_inbox/outputs/runs/`: historical batch run artifacts. Do not read, clean, move, or overwrite.
- `rsshub/rss_opml/`: RSS source CSV/OPML tooling. Do not change source CSVs unless explicitly requested.

## Common Local Commands

Run these from `content_inbox/` unless noted:

```bash
python3 -m pip install -r requirements.txt
PYTHONPATH=. python3 -m app.server
docker compose up -d --build
docker compose ps
docker compose down
PYTHONPATH=. pytest -q
```

Useful read-only checks from the repository root:

```bash
git status --short
git diff --stat
find . -maxdepth 3 -type f
```

Candidate command, verify before using for real work:

```bash
python3 content_inbox/scripts/run_rss_sources_to_content_inbox.py --dry-run
```

The batch script can create run artifacts under `content_inbox/outputs/runs/` and can call the local service. Do not run real large RSS batches without user confirmation.

## Testing And Verification

Primary test command:

```bash
cd content_inbox
PYTHONPATH=. pytest -q
```

For configuration edits:

```bash
python3 -m json.tool .claude/settings.json >/dev/null
```

For service-level checks, first confirm the user wants the service started:

```bash
curl -s http://127.0.0.1:8787/health
```

## Claude Code Working Principles

- Read this file, relevant README/docs, and the target module before editing.
- Give a short plan before changing files.
- Keep changes narrow. Do not perform whole-repository rewrites or unrelated refactors.
- Prefer existing patterns, tests, and scripts over inventing new structure.
- Do not read `.env`, `.env.*`, secrets, tokens, credentials, keys, or real runtime data.
- Do not operate directly on production-like local data or historical output runs.
- Ask before writes, tests that mutate data, Docker operations, network calls, or real batch processing.
- Never use permission bypass mode for this project.

## Paths Not To Modify Casually

- `.env`, `.env.*`, and any file/path containing `secret`, `token`, `credential`, or `key`.
- `content_inbox/data/**`
- `content_inbox/outputs/runs/**`
- `wechat-rss/data/**`
- `rsshub/rss_opml/rss_sources.csv`
- `content_inbox/prompts.yaml`
- Docker files and compose files, unless explicitly requested.

## Delivery Format After Each Change

Report:

1. Files changed.
2. What changed and why.
3. Verification commands run and their results.
4. Risks, assumptions, or commands not run.
5. Any manual confirmation needed from the user.
