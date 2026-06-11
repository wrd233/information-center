# Inbox Operating Loop

`content_inbox` now exposes a daily/manual Inbox Operating Loop for registry-based RSS ingestion and review.

## Runtime Source Of Truth

- Runtime runs read active sources only from SQLite `rss_sources`.
- CSV/OPML/URL lists are import inputs only. They are not read by the scheduler or manual inbox loop.
- Full loop runs are stored in `rss_ingest_runs` with `source_mode = registry_full`.

## Manual Runs

Use the console page:

```text
content_inbox_console /inbox-loop
```

Or call the API:

```bash
curl -s -X POST http://127.0.0.1:8787/api/inbox-loop/runs \
  -H 'Content-Type: application/json' \
  -d '{"run_synchronously": true, "limits": {"max_items_per_source": 20}}'
```

Manual runs share the same kernel as scheduled runs. They:

- acquire a DB-backed registry-full run lock;
- skip by default if a successful or partial-success full run completed within `CONTENT_INBOX_MANUAL_RUN_GRACE_MINUTES`;
- use per-source `until_existing` incremental fetch;
- continue after individual source failures;
- run deterministic post-processing after ingest when items were linked.

Set `"force": true` to bypass recent-run protection.

## Scheduler

Default scheduler config:

```text
CONTENT_INBOX_SCHEDULER_ENABLED=1
CONTENT_INBOX_DAILY_RUN_TIME=06:00
CONTENT_INBOX_DAILY_RUN_TZ=Asia/Shanghai
CONTENT_INBOX_DAILY_RUN_RECOVER_MISSED=1
```

On service startup, if the configured local run time has already passed and no successful or partial-success registry-full run exists for that local day, the scheduler triggers one recovery run. If real runs are not enabled, it records `real_runs_disabled` and does not write.

Scheduler state is visible at:

```text
GET /api/inbox-loop/status
```

## Summary And Confidence

Run summaries are available at:

```text
GET /api/inbox-loop/runs/{run_id}/summary
GET /api/inbox-loop/runs/{run_id}/diagnostics
GET /api/inbox-loop/runs/{run_id}/operating-view
```

Confidence rules:

- `high`: source success rate >= 95% and no high-priority source failed.
- `medium`: source success rate >= 80%.
- `low`: source success rate < 80% or multiple/core failures.
- `failed`: no active sources or run kernel/registry failure without usable success.

`partial_success` is usable, but the summary includes failed source digest and confidence reasons.

## Triage, Ledger, Context Packs

Agent triage is bounded and defaults to no network access:

```text
GET  /api/inbox-loop/triage-packets
POST /api/inbox-loop/agent-decisions
GET  /api/inbox-loop/decision-ledger
```

Allowed decisions are:

```text
surface, research, silent, noise, merge_suggest, do_not_merge
```

Context packs:

```text
GET /api/context-packs/daily_brief
GET /api/context-packs/review_decisions
GET /api/context-packs/research_object?target_type=event&target_id=...
```

Console routes:

- `/inbox-loop`: scheduler/latest-run/manual-run/summary/diagnostics/operating view.
- `/triage`: packet review, decision writeback, ledger, daily/review context pack JSON.
- `/runs/{run_id}` and object detail pages show decision ledger entries when present.

