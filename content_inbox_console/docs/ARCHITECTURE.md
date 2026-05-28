# Architecture: API-driven Operational Console

`content_inbox_console` 是现有 FastAPI + Jinja + HTMX 前端的原地重构版本。当前主路径只有一个数据来源：`CONTENT_INBOX_FRONTEND_API_BASE` 指向的 `content_inbox` 后端 API。

## 当前目录

```text
content_inbox_console/
  app/
    main.py              FastAPI app factory
    config.py            host/port/API base 配置
    backend_client.py    统一 envelope API client
    routes/ops.py        所有 console 页面路由
  templates/
    base.html
    components/nav.html  任务导航 + 高级调试折叠导航
    ops/*.html           Dashboard、Environment、Sources、Runs、Reset、消费页
  static/css/app.css     统一低心智负担后台视觉
  tests/test_api.py      route rendering + API mock 测试
```

## 已废弃并清理的旧架构

历史版本曾包含 direct SQLite viewer：

```text
app/repository.py
app/dependencies.py
app/repositories/*
app/routes/dashboard.py/items.py/sources.py/runs.py/clusters.py/diagnostics.py
templates/items|sources|runs|clusters/*
templates/dashboard.html
```

这些文件已经删除。不要重新注册 direct-SQL route，不要恢复 observed source fallback 或 file-run fallback。Fresh DB 与 Legacy DB 的业务边界必须由后端 API 显式表达。

## API 约定

前端只接受统一 envelope：

```json
{ "ok": true, "data": {}, "error": null, "meta": {} }
```

错误展示规则：

- 页面顶部显示中文摘要。
- `error.details` 或原始 JSON 放入折叠区。
- 不向普通用户裸露 traceback。

## 后端边界

Console 依赖后端这些 API group：

```text
/api/environment
/api/environment/health
/api/environment/reset-options
/api/environment/reset/preview
/api/environment/reset/commit
/api/sources*
/api/runs*
/api/items
/api/dedupe-groups
/api/clusters
/api/events
/api/entities / relations / claims / topics / timeline
/api/review-queue
/api/evidence
/api/briefings
/api/reports
/api/saved-views
/api/agent-query/preview
```

## 安全模型

- Console 不持有 DB path 写权限，也不打开 SQLite。
- Fresh DB identity、DB path、Legacy DB proof 都由后端 `/api/environment` 返回。
- Legacy DB 只出现在 checksum/mtime/size 证明中。
- reset preview/commit 由后端验证 `is_fresh_database`。
- real-write 由后端 `CONTENT_INBOX_ENABLE_REAL_RUNS=1` gate 控制。

## UI 架构

一级导航从对象导航改为任务导航：

```text
作战首页
开始使用：环境 / Source / Run
信息消费：Events / Review / Briefing / Report / Agent Query
维护与重开：Reset / Settings
高级调试：Items / Dedupe / Clusters / Entities / Relations / Claims / Topics / Timeline / Evidence / Saved Views
```

页面模板复用这些模式：Page Header、Status Strip、Stat Card、Next Action Card、Preview Panel、Danger Zone、Data Table、Raw JSON Collapse、Audit/Event Timeline。
