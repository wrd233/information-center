# REAL_RUN_READINESS_REPORT

Generated: 2026-05-18

## 1. Implementation Summary

This delivery keeps `content_inbox_console` as the single main frontend and completes the operational loop requested in the correction prompt:

```text
Fresh DB -> clear/reset -> add/import sources -> select sources
-> configure published_at range and limits -> dry-run -> live run detail
-> prove dry-run writes no items -> real-write -> items from run
-> pipeline stages -> clusters/events/review -> briefing/report/export
-> reset again -> legacy DB checksum unchanged
```

The console is now API-driven through the new `/api/*` envelope contract. It does not read SQLite directly and does not fill empty Fresh DB pages from Legacy DB data.

## 2. Database Paths And Safety Proof

Default Fresh DB path:

```text
/Users/wangrundong/work/infomation-center/content_inbox/data/environments/fresh_default/content_inbox.db
```

Browser validation used an isolated Fresh DB environment:

```text
/Users/wangrundong/work/infomation-center/content_inbox/data/environments/fresh_browser_validation/content_inbox.db
```

That validation environment was reset through the console and then removed from the working tree after verification. The runtime default remains `fresh_default`.

Legacy DB path:

```text
/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3
```

Legacy DB before browser validation:

```text
SHA256 = 401746f7cb5d6a8008e18dd7be476b572e1de7e238d3494076a92051745f8f9b
size   = 113274880
mtime  = May 18 11:04:53 2026
```

Legacy DB after browser validation:

```text
SHA256 = 401746f7cb5d6a8008e18dd7be476b572e1de7e238d3494076a92051745f8f9b
size   = 113274880
mtime  = May 18 11:04:53 2026
```

Result: Legacy DB was not modified. The new console diagnostics explicitly report `legacy_business_fallback = false`.

## 3. content_inbox_console Upgrade

- Project path: `/Users/wangrundong/work/infomation-center/content_inbox_console`
- Upgrade style: in-place rebuild, no parallel frontend project.
- Stack: FastAPI + Jinja + HTMX + CSS + backend API client.
- API client: `content_inbox_console/app/backend_client.py`
- Main router: `content_inbox_console/app/routes/ops.py`
- Main UI templates: `content_inbox_console/templates/ops/*`
- Docker service identity: `content-inbox-console`
- Old direct-SQL fallback pages are not registered in the main route path.
- All main console pages use backend APIs instead of direct SQLite reads.

## 4. Schema And API Surface

The backend initializes an idempotent operational schema with:

```text
system_metadata, sources, inbox_items, ingest_runs, ingest_run_sources,
ingest_run_events, item_run_links, source_operation_audit, audit_log,
operation_previews, dedupe_groups, dedupe_group_items, semantic_extractions,
event_clusters, cluster_items, events, event_items, entities, item_entities,
relations, claims, topics, topic_items, topic_events, review_queue,
saved_views, briefings, reports
```

Primary API groups:

```text
/api/environment
/api/environment/reset-options
/api/environment/reset/preview
/api/environment/reset/commit
/api/environment/fresh-db/preview
/api/environment/fresh-db/create
/api/sources
/api/sources/check
/api/sources/import/preview
/api/sources/import/commit
/api/sources/export
/api/sources/bulk/preview
/api/sources/bulk/commit
/api/runs
/api/runs/preview
/api/runs/{run_id}/events
/api/runs/{run_id}/sources
/api/runs/{run_id}/items
/api/runs/{run_id}/pipeline/{stage}
/api/runs/{run_id}/briefing
/api/runs/{run_id}/report
/api/items, /api/dedupe-groups, /api/clusters, /api/events
/api/entities, /api/relations, /api/claims, /api/topics, /api/timeline
/api/review-queue, /api/evidence, /api/briefings, /api/reports
/api/saved-views, /api/agent-query/preview
```

All new APIs use:

```json
{ "ok": true, "data": {}, "error": null, "meta": {} }
```

## 5. Data Reset And Clean State

Implemented reset APIs and UI on the Environment page.

Reset levels:

| Level | UI label | Effect |
|---|---|---|
| `clear_runs_items_keep_sources` | 清空运行结果，保留 Sources | Clears runs, items, run events, dedupe, semantic, clusters, events, review, briefings, reports, while preserving source registry and DB identity. |
| `clear_all_sources_and_content` | 清空 Sources 和所有内容 | Clears sources plus all run/content/semantic/report objects, while preserving schema and system metadata. |
| `create_new_fresh_db` | 新建 Fresh DB 环境 | Creates a new fresh DB path and initializes schema/metadata. |

Safety behavior:

- Reset is preview-first.
- Commit requires `confirmation = RESET`.
- Reset is disabled when `is_fresh_database` is false.
- Preview shows DB path, counts, affected tables, and `legacy_db_affected = false`.
- Commit writes `environment_reset_committed` audit data with before/after counts.
- The console refreshes Environment/Dashboard/Sources/Runs/Items state after reset.

## 6. Source Management

The Sources page now supports:

- Add a single source with title/feed URL/site/category/tags/status/notes.
- Check/preview a source before add.
- Import pasted source lines with preview and commit.
- JSON/CSV/OPML export.
- Search/filter/sort/page source list.
- Source detail and edit.
- Enable, disable, archive/delete, restore.
- Bulk preview and commit for enable/disable/archive/delete/recheck/export/run.
- Run selected sources by sending selected source IDs into the Run Wizard.

Deletes use soft archive semantics by default. The Chinese UI explains that archive/delete does not physically remove historical items.

## 7. Run Wizard And Run Detail

The Run Wizard now includes:

1. Environment confirmation with Fresh DB identity, path, counts, and real-write status.
2. Source range selection with source checkboxes and all-active support.
3. `published_from`, `published_to`, and timezone fields.
4. Limits: `max_sources`, `max_items_per_source`, `max_total_items`, `source_timeout_seconds`, `run_timeout_minutes`.
5. Mode selection: `dry-run` or `real-write`.
6. Preview with DB path, source count, limits, max possible items, write behavior, Legacy DB impact, cancel/rollback notes.
7. Start and redirect to Run Detail.

Run Detail shows:

- status, mode, database path
- source progress
- current run events and item events
- inserted/duplicate/filtered/failed counts
- error aggregation through run events
- cancel button
- items from this run
- pipeline action buttons
- briefing/report generation buttons

Real-write is disabled with a Chinese explanation unless `CONTENT_INBOX_ENABLE_REAL_RUNS=1`.

## 8. Pipeline And Information Consumption

Run Detail exposes real API-backed pipeline controls:

```text
dedupe
semantic
clusters
events
review
briefing
report
```

Pipeline events are written to the run event store, including:

```text
dedupe_started, dedupe_completed, semantic_started, semantic_completed,
cluster_completed, event_completed, review_queue_generated,
briefing_generated, report_generated
```

Information pages use real stored data:

- Items: filter by run/source/time and view raw/canonical/semantic links.
- Dedupe Groups: heuristic URL/title grouping and review hooks.
- Clusters: generated from real items, with member items and review/dismiss actions.
- Events: generated from clusters, with supporting items and review/dismiss actions.
- Entities/Relations/Claims/Topics/Timeline: backed by lightweight extraction and schema tables.
- Review Queue: generated from low-confidence/event-candidate objects and resolvable.
- Briefings: daily/weekly generation from events/review.
- Reports: generated and persisted as Markdown/JSON-compatible records.
- Agent Query: previews human/markdown/JSON/compact context packs from real items/events.

## 9. Depth Of Implementation

| Module | Status | Depth |
|---|---|---|
| Environment | Implemented | Fresh DB identity, health, diagnostics, reset, legacy checksum proof. |
| Sources | Implemented | Add/check/import/export/edit/archive/restore/bulk/run selected. |
| Runs | Implemented | Wizard, preview, dry-run, real-write, events, items, cancel, report. |
| Items | Implemented | Real item list/detail filters and run/source links. |
| Dedupe | Implemented with real data | Heuristic grouping and stage trigger. |
| Semantic Extraction | Implemented with real data | Lightweight rule extraction, evidence, low/medium confidence. |
| Clusters | Implemented with real data | Generated from item groupings, review/dismiss/manual event creation. |
| Events | Implemented with real data | Generated from clusters, detail/supporting item views. |
| Entities | Implemented with real data | Rule-extracted entities linked to items. |
| Relations | Partially implemented with real data | Tables/API/review hooks present; extraction is lightweight. |
| Claims | Partially implemented with real data | Tables/API/review hooks present; richer claim extraction remains future work. |
| Topics | Implemented with real data | Source category/topic links and topic views. |
| Timeline | Implemented with real data | Event timeline endpoint/page. |
| Review Queue | Implemented | Generated review records and resolve/dismiss. |
| Evidence | Implemented | Semantic/audit-backed evidence endpoint and empty states. |
| Briefings | Implemented | Daily/weekly generation and console view/export. |
| Reports | Implemented | Run/source/event-style report records and export views. |
| Agent Query | Implemented | Context preview in multiple formats. |

## 10. Chinese UI

The main console UI is now Chinese-first:

- Navigation
- Dashboard
- Environment / Fresh DB diagnostics
- Reset preview/commit
- Source add/import/bulk/detail
- Run Wizard
- Run Preview
- Run Detail
- Items, clusters, events, review queue
- Briefings, reports, agent query, settings

Project terms are intentionally mixed as requested: `source`, `run`, `dry-run`, `real-write`, `item`, `cluster`, `event`, `review queue`, `briefing`, `agent query`, `Fresh DB`, `Legacy DB`.

Known residue: low-level API fields and stored status codes remain English by design because they are identifiers.

## 11. Old Data Investigation

The earlier “old data visible in the frontend” risk was addressed by:

- Removing main-console direct SQLite reads.
- Removing source/file-run fallback from the main UI path.
- Making `/api/*` use the configured Fresh DB only.
- Showing DB identity and counts in the global header.
- Adding Environment diagnostics for API base, DB path, DB ID, Fresh DB flag, Legacy DB checksum, and fallback status.
- Adding reset controls so polluted `fresh_default` test data can be cleared from the UI.

Current behavior: an empty Fresh DB stays empty until the user explicitly adds/imports sources. Legacy DB is diagnostic-only and is not used as business data fallback.

## 12. Frontend Operational Validation

Manual browser validation was completed through `content_inbox_console` at:

```text
http://127.0.0.1:8788
```

Backend used:

```text
CONTENT_INBOX_DB_PATH=data/environments/fresh_browser_validation/content_inbox.db
CONTENT_INBOX_ENABLE_REAL_RUNS=1
CONTENT_INBOX_ENVIRONMENT=fresh
```

Validation steps completed:

1. Opened Environment page and confirmed Chinese Fresh DB diagnostics.
2. Verified counts started at 0 sources / 0 items / 0 runs.
3. Ran reset preview and commit from the console.
4. Imported a fixture source through source import preview/commit.
5. Confirmed source count became 1.
6. Opened Run Wizard and selected the source checkbox.
7. Configured conservative limits and ran dry-run preview.
8. Started dry-run and verified Run Detail events completed with no committed items.
9. Repeated source selection for `real-write`.
10. Ran real-write preview and start.
11. Verified Run Detail showed 2 inserted items.
12. Opened Items page and confirmed items from the run.
13. Triggered dedupe, semantic, briefing, and report actions from Run Detail.
14. Opened Clusters, Events, Briefings, Reports, and Agent Query pages and verified real data-backed output.
15. Returned to Environment and ran `clear_all_sources_and_content`.
16. Confirmed counts returned to 0 / 0 / 0.
17. Rechecked Legacy DB checksum, size, and mtime; unchanged.

## 13. Automated Verification

Backend focused operational API tests:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox
PYTHONPATH=. pytest -q tests/test_ops_api.py
```

Result:

```text
9 passed
```

Backend full suite:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox
PYTHONPATH=. pytest -q
```

Result after rerun:

```text
259 passed, 11 skipped
```

Note: the first full run hit one known concurrent RSS runner timing failure; the same test passed immediately when rerun in isolation, and the full suite then passed.

Console tests:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox_console
pytest -q
```

Result:

```text
4 passed
```

Docker compose config checks:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox
docker compose config

cd /Users/wangrundong/work/infomation-center/content_inbox_console
docker compose config
```

Both compose configs rendered successfully.

## 14. Startup And Operation

Backend:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox
CONTENT_INBOX_DB_PATH=data/environments/fresh_default/content_inbox.db \
CONTENT_INBOX_ENABLE_REAL_RUNS=0 \
CONTENT_INBOX_ENVIRONMENT=fresh \
PYTHONPATH=. python3 -m app.server
```

Console:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox_console
CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \
python3 -m app.main
```

Open:

```text
http://127.0.0.1:8788
```

For real-write testing:

```bash
CONTENT_INBOX_ENABLE_REAL_RUNS=1
```

Then restart the backend.

## 15. How To Repeat The Clean-State Flow

1. Open `http://127.0.0.1:8788/environment`.
2. Confirm the global header shows `Fresh DB`.
3. Choose reset level `清空 Sources 和所有内容`.
4. Click preview.
5. Type `RESET`.
6. Commit reset.
7. Open Sources and add/import sources.
8. Use source checkboxes and click run selected sources.
9. Configure source range, published time range, limits, and mode.
10. Preview dry-run.
11. Start dry-run and watch Run Detail events.
12. Confirm Items count is still unchanged for dry-run.
13. Enable real-write and start a real-write run.
14. View items from run.
15. Trigger pipeline stages or generate briefing/report.
16. Reset again to return to a clean Fresh DB.

## 16. Legacy Cleanup And Compatibility Decisions

- New console routes are API-driven and do not use old SQLite fallback pages.
- The main UI no longer reads observed source files or historical output runs.
- Legacy DB is never used as automatic fallback.
- Existing old backend endpoints may remain where cheap, but they are not the main console contract.
- Current CLI workflow remains practical; obsolete API behavior was not preserved if it conflicted with the Fresh DB/run/event/audit model.
- Future legacy migration should be explicit: preview legacy sources first, then commit into Fresh DB through source import APIs.

## 17. Known Limits

- Ingest execution is still local-process/background-thread based, not a durable distributed queue.
- Dedupe, relations, and claims are lightweight rule-based v1 implementations.
- Auth and permissions are not implemented; this remains a local/trusted-network console.
- Full Docker image builds were not run in this pass; compose config validation passed.
- UI is now operational and Chinese-first, but it is not yet a polished component-system rewrite.

## 18. Files Changed

Key implementation files:

```text
content_inbox/app/ops_api.py
content_inbox/tests/test_ops_api.py
content_inbox_console/app/routes/ops.py
content_inbox_console/static/css/app.css
content_inbox_console/templates/base.html
content_inbox_console/templates/components/nav.html
content_inbox_console/templates/ops/*.html
content_inbox_console/tests/test_api.py
REAL_RUN_READINESS_REPORT.md
```
