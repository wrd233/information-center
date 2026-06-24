# Operations

## Purpose

This document explains local runtime configuration, database operations, output cleanup, synthetic cleanup, and safety checks.

## Configuration

Use local `.env`:

```text
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-v4-flash
INFORMATION_WORKSPACE_DB_PATH=./data/information_workspace.db
INFORMATION_WORKSPACE_OUTPUTS_DIR=./outputs
```

Never commit `.env`.

## Start Backend And Frontend

```bash
cd information_workspace
python3 -m app.main
```

The backend serves API routes under `/api` and the frontend at `/`.

## Database

Default path:

```text
data/information_workspace.db
```

Schema initialization is idempotent and runs at service startup. Schema version is available through health/status APIs.

## Backup

Stop writes, then copy the SQLite file:

```bash
cp data/information_workspace.db data/information_workspace.backup.db
```

## Reset

For local development only, stop the service and remove the database file. The next startup recreates schema.

## Clean Synthetic Data

```bash
python3 scripts/cleanup_synthetic.py
```

The command removes synthetic runs/material links where safe and reports protected references.

## Outputs

Generated reports, traces, exports, and smoke logs live under `outputs/`. They are ignored by git. Remove old output directories only when you no longer need validation evidence.

## Common Failures

- Missing DeepSeek key: business LLM steps fail clearly; tests may use explicit mock mode.
- Invalid source type: upload item is marked failed.
- Invalid LLM JSON or illegal facet: repair/retry runs; persistent failure marks step failed.
- Referenced material ignore: ignore may be rejected to avoid breaking Event/Topic references.

## Real DeepSeek Validation

After configuring local `.env`, run:

```bash
PYTHONPATH=. python3 scripts/run_real_deepseek_validation.py --all-light --import-sample
PYTHONPATH=. python3 scripts/final_validation.py
```

The first command writes a real validation report and trace samples. The second command requires successful real DeepSeek traces for required tasks before READY can be claimed.

## Leak Checks

Before sharing reports or committing:

```bash
git status --short
rg -n "DEEPSEEK_API_KEY|Authorization|sk-[A-Za-z0-9]" information_workspace --glob '!data/**' --glob '!outputs/**'
```

Do not inspect or print `.env`. Do not commit `data/` or `outputs/`.
