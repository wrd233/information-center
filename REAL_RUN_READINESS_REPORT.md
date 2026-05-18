# REAL_RUN_READINESS_REPORT

Generated: 2026-05-18

## 1. Implementation Summary

This delivery rebuilds the content-inbox mainline around a fresh database, a new `/api/*` backend contract, run/event/audit tracking, and an upgraded `content_inbox_console`.

Implemented core closed loop:

```text
fresh DB -> source import preview/commit -> selected-source dry-run
-> dry-run no item write proof -> selected-source real-write
-> run events/progress -> items from run -> lightweight semantic objects
-> clusters/events/review -> daily briefing -> report export
-> legacy DB unchanged proof
```

## 2. New Database Path

New default DB:

```text
/Users/wangrundong/work/infomation-center/content_inbox/data/environments/fresh_default/content_inbox.db
```

New DB final proof:

```text
SHA256 = 953a2a2049f561218db939f29c2e2c9a815111a949a46ad621aa02420b0c0713
size   = 487424
mtime  = May 18 11:08:52 2026
```

## 3. Old Database Path And Unchanged Proof

Legacy DB:

```text
/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3
```

Measured before final E2E validation:

```text
SHA256 = 401746f7cb5d6a8008e18dd7be476b572e1de7e238d3494076a92051745f8f9b
size   = 113274880
mtime  = May 18 11:04:53 2026
```

Measured after final E2E validation:

```text
SHA256 = 401746f7cb5d6a8008e18dd7be476b572e1de7e238d3494076a92051745f8f9b
size   = 113274880
mtime  = May 18 11:04:53 2026
```

Result: unchanged during final verification. Real validation used the fresh DB path above.

## 4. Schema And Migration State

`InboxStore.init_schema()` now creates the operational schema idempotently:

- `system_metadata`
- `ingest_run_events`
- `item_run_links`
- `source_operation_audit`
- `audit_log`
- `operation_previews`
- `dedupe_groups`, `dedupe_group_items`
- `semantic_extractions`
- `events`, `event_items`
- `entities`, `item_entities`
- `relations`, `claims`
- `topics`, `topic_items`, `topic_events`
- `saved_views`, `briefings`, `reports`

The existing tested item/source/run storage remains underneath the new API, but the new `/api/*` contract is the primary surface.

## 5. content_inbox_console Upgrade

- Frontend project path: `/Users/wangrundong/work/infomation-center/content_inbox_console`
- Upgrade style: in-place rebuild.
- New parallel frontend directories: none.
- Technology: FastAPI + Jinja + HTMX + small API client.
- API client: `content_inbox_console/app/backend_client.py`
- Main route module: `content_inbox_console/app/routes/ops.py`
- Docker service: `content-inbox-console`
- Old direct-SQL routes/templates: retained on disk for reference but no longer registered as the main UI.
- How to verify new console: open `/dashboard`; navigation includes Environment, Sources, Runs, Information, Dedupe, Clusters, Events, Entities, Relations, Claims, Topics, Timeline, Review Queue, Briefings, Reports, Agent Query, Settings.

## 6. Frontend Pages

Implemented:

- Dashboard
- Environment
- Sources and source detail
- Source import preview/commit
- Ingest Runs
- Run Creation Wizard
- Run Preview
- Run Detail
- Information / Items and item detail
- Dedupe Groups
- Clusters and cluster detail
- Events and event detail
- Entities
- Relations
- Claims
- Topics
- Timeline
- Review Queue
- Briefings
- Reports
- Agent Query
- Settings

## 7. Backend API List

Primary new API groups:

- `GET /api/environment`
- `POST /api/environment/init-fresh`
- `GET /api/environment/health`
- `GET /api/environment/report`
- `/api/sources`, import preview/commit/export, bulk operations
- `/api/runs`, preview, detail, sources, events, items, summary, report, cancel, rollback
- `/api/items`, raw, dedupe, semantic
- `/api/dedupe-groups`
- `/api/clusters`
- `/api/events`
- `/api/entities`
- `/api/relations`
- `/api/claims`
- `/api/topics`
- `/api/timeline`
- `/api/review-queue`
- `/api/evidence`
- `/api/briefings`
- `/api/saved-views`
- `/api/agent-query/preview`
- `/api/reports`

All new APIs use `{ ok, data, error, meta }`.

## 8. Source Management

Implemented:

- List/search/filter sources.
- Import preview/commit for URLs, CSV, JSON, OPML.
- Export JSON/CSV/OPML.
- Add, patch, archive.
- Bulk enable/disable/archive/delete/recheck/run.
- Audit logging for source operations.

Deletes default to archive/soft delete semantics.

## 9. Run Creation And Real-Time Observation

Implemented:

- Selected-source run config.
- Dry-run and real-write.
- Published-at time range filtering.
- Limits: max sources, max items per source, max total items.
- Run preview.
- Run events with `after_seq`.
- SSE endpoint at `/api/runs/{run_id}/stream`.
- Source progress rows.
- Item run links.
- Cancel request.
- Rollback preview and soft rollback commit.

Dry-run writes run/event records but no items.

## 10. Information Consumption Layer

Depth by module:

| Module | Status | Notes |
|---|---|---|
| Environment | Implemented | Fresh DB metadata, health, legacy checksum proof |
| Sources | Implemented | Preview/commit/export/bulk/audit |
| Runs | Implemented | Preview, dry-run, real-write, events, items, report, rollback |
| Items | Implemented | List/detail/run filter/raw/semantic links |
| Dedupe | Partially implemented with real data | Tables/API/manual review hooks; heuristic grouping can be expanded |
| Semantic Extraction | Implemented | Lightweight rule extractor with evidence and low confidence |
| Clusters | Implemented | Real item grouping into `event_clusters` and `cluster_items` |
| Events | Implemented | Candidate events from clusters and manual create from cluster |
| Entities | Implemented | Rule-extracted terms linked to items |
| Relations | Partially implemented with real data | API/table/review hooks present; richer extraction is future work |
| Claims | Partially implemented with real data | API/table present; richer claim extraction is future work |
| Topics | Implemented | Source category topic links |
| Timeline | Implemented | Event timeline endpoint/page |
| Review Queue | Implemented | Generated event candidate reviews and resolve endpoint |
| Evidence | Implemented | Semantic extraction and audit-backed evidence endpoints |
| Briefings | Implemented | Daily/weekly generation from events/reviews |
| Reports | Implemented | Persisted Markdown report generation |
| Agent Query | Implemented | Item-backed compact/human/markdown/JSON context preview |

## 11. Automated Tests

Backend:

```text
cd content_inbox
PYTHONPATH=. pytest -q
254 passed, 11 skipped
```

Console:

```text
cd content_inbox_console
pytest -q
3 passed
```

Focused new backend tests cover:

- Fresh environment API.
- Source import preview/commit.
- Dry-run no item writes.
- Real-write selected source and item links.
- Published-at filtering.
- Run events.
- Event/briefing/report generation in E2E smoke.

## 12. Manual Verification

Executed a fixture E2E against the fresh DB:

```text
source_id    = fixture-readiness-fixture
dry_run_id   = run_20260518_110852_8101a30c
real_run_id  = run_20260518_110852_4a5be1f3
run_items    = {'total': 2, 'returned': 2}
briefing_id  = brief_daily_1a31d91828a2
report_id    = report_b61fc3661b89
```

Docker compose config checks:

```text
content_inbox_compose_ok
content_inbox_console_compose_ok
```

## 13. Startup

Backend:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox
CONTENT_INBOX_DB_PATH=data/environments/fresh_default/content_inbox.db \
CONTENT_INBOX_ENABLE_REAL_RUNS=0 \
PYTHONPATH=. python3 -m app.server
```

Console:

```bash
cd /Users/wangrundong/work/infomation-center/content_inbox_console
CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

Open:

```text
http://127.0.0.1:8788
```

Docker:

```bash
cd content_inbox
docker compose up --build

cd ../content_inbox_console
docker compose up --build
```

## 14. How To Use The Closed Loop

1. Open Environment and confirm `is_fresh_database = true`.
2. Open Sources.
3. Paste source lines as `feed_url, source_name, category`.
4. Click Import Preview.
5. Commit import.
6. Open Runs -> New Run.
7. Enter selected source IDs.
8. Configure published_at range and limits.
9. Preview dry-run.
10. Start dry-run.
11. Confirm Run Detail shows events and no committed items.
12. Restart backend with `CONTENT_INBOX_ENABLE_REAL_RUNS=1`.
13. Preview real-write.
14. Start real-write.
15. View Run Detail events and items.
16. Open Information, Clusters, Events, Review Queue.
17. Generate Daily Briefing.
18. Generate Report.
19. Re-check Environment legacy DB checksum proof.

## 15. Legacy Cleanup and Compatibility Decisions

- `content_inbox_console` no longer registers old direct-SQL page routers as the main UI.
- File-run fallback and observed-source fallback are removed from the main navigation path.
- Console no longer fills fresh DB pages with legacy DB content.
- Existing old backend paths remain where cheap, but the new `/api/*` envelope contract is the main backend surface.
- Existing current CLI tests still pass as part of the full backend suite.
- Legacy DB migration/fallback was not implemented by design. Future legacy data migration should be explicit: build an import preview from legacy sources, then commit into fresh DB.

## 16. Known Limits

- Real run execution is functional and can run synchronously or background-threaded, but it is not a distributed task queue.
- Dedupe/relation/claim extraction is intentionally lightweight in v1.
- Auth/permissions are not implemented; this remains a local/trusted-network console.
- UI is operational and dense, not a polished design-system rewrite.
- Docker build was not fully executed; compose config validation passed.

## 17. Next Suggestions

- Add a durable task worker for long-running ingest.
- Add richer LLM semantic extraction behind an explicit budget/safety gate.
- Add graph visualization for entity/relation/event exploration.
- Add stronger source health scoring trends.
- Add explicit legacy source import preview from old DB as a separate, user-triggered workflow.
