# FRONTEND_REBUILD_REPORT

Generated: 2026-05-28

## Summary

This rebuild keeps `content_inbox_console` as the single frontend and turns it into a low-cognitive-load operational console. The frontend is API-driven, Chinese-first, Fresh DB focused, and exposes source/run/pipeline/review/output/reset flows end to end.

## Cleaned Residue

Removed the unregistered direct-SQL viewer implementation:

```text
content_inbox_console/app/repository.py
content_inbox_console/app/dependencies.py
content_inbox_console/app/repositories/*
content_inbox_console/app/routes/dashboard.py
content_inbox_console/app/routes/items.py
content_inbox_console/app/routes/sources.py
content_inbox_console/app/routes/runs.py
content_inbox_console/app/routes/clusters.py
content_inbox_console/app/routes/diagnostics.py
content_inbox_console/templates/dashboard.html
content_inbox_console/templates/items/*
content_inbox_console/templates/sources/*
content_inbox_console/templates/runs/*
content_inbox_console/templates/clusters/*
```

The console no longer has observed-source fallback or file-run fallback in the code tree. The only registered router is `app.routes.ops`.

## New Information Architecture

```text
作战首页
开始使用：环境 / Fresh DB, Source 管理, 创建 Run, Run 观察
信息消费：事件中心, 待审核, Briefing, Report, Agent Query
维护与重开：数据清理 / 重新开始, 设置
高级调试：Items, Dedupe Groups, Clusters, Entities, Relations, Claims, Topics, Timeline, Evidence, Saved Views
```

## Backend API Additions

Extended `/api/environment/reset/preview` and `/api/environment/reset/commit` with:

- `clear_pipeline_outputs_keep_items`
- `clear_outputs_keep_events`
- `clear_by_run_id`
- `clear_by_source_id`

Also expanded `/api/environment/reset-options` to return human-readable labels, clears/keeps/risk/confirmation metadata.

## Safety

- reset disabled when `is_fresh_database=false`.
- all reset commits require exact confirmation.
- scoped run reset preserves shared items.
- scoped source reset protects other source items.
- commit writes audit.
- Legacy DB remains proof-only and returns `legacy_db_affected=false`.

## Tests

Run on 2026-05-28:

```text
cd content_inbox
PYTHONPATH=. pytest -q tests/test_ops_api.py
13 passed

cd ../content_inbox_console
PYTHONPATH=. pytest -q
4 passed
```

## Known Lightweight v1 Areas

- semantic / clusters / events / review generation in ops API remains lightweight rule-based for console closure.
- source-scoped reset marks mixed-source clusters/events as `stale`; future work can add queued recompute after cleanup.
- authentication/authorization remains out of scope.
