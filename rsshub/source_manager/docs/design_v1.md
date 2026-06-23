# RSS Source Manager Design v1

## 1. Context / 背景

The repository already has local RSSHub deployment files, an OPML/CSV workspace, a separate `wechat-rss` service, and a larger `content_inbox` ingestion system. RSS Source Manager sits near `rsshub/` as a focused source registry and health ledger.

It is deliberately independent from `content_inbox`: old code can inform implementation choices, but this module does not import old application packages, read old SQLite databases, or join the old console.

## 2. Goals / 第一阶段目标

- Manage `rsshub`, `wechat`, and `native` RSS/Atom sources.
- Provide source CRUD, status, category, tags, notes, and `rating`.
- Use a single SQLite database at `rsshub/source_manager/data/source_manager.sqlite3`.
- Support preview-first CSV and OPML import.
- Support clean/full CSV export and profile-based OPML export.
- Separate `check` from formal `fetch`.
- Save lightweight entry history and fetch run history.
- Provide a small React/Vite management UI with three top-level tabs.
- Provide backend core tests.

## 3. Non-goals & Guardrails / 第一阶段硬边界

First phase intentionally does not implement:

- Login, permissions, token/session, or user roles.
- Automatic scheduler or background recurring jobs.
- AI/LLM, semantic review, event clustering, briefing, or content consumption views.
- Raw feed XML, raw entry JSON, content HTML, full text, or large original fields in the database.
- `content_inbox_console` integration.
- Reading or writing the `content_inbox` database.
- Multiple fresh/dev/test/legacy databases.
- Web UI or API reset for the main database.
- A large dashboard, complex taxonomy tree, tag management system, or frontend E2E tests.

Any future change that crosses these guardrails should first update this document and be treated as a later phase.

## 4. Architecture / 架构关系

```text
React UI
  -> FastAPI /api/v1
    -> services
      -> adapters: RSSHub / WeChat / Native
      -> SQLite repositories
        -> data/source_manager.sqlite3
```

Development runs FastAPI on `127.0.0.1:8010` and Vite on `127.0.0.1:5173`. Daily mode builds React and lets FastAPI serve `frontend/dist` from `127.0.0.1:8010`.

## 5. Data Model / 数据模型

Tables:

- `sources`: source facts, user fields, adapter identity, health fields, and fetch counters.
- `entries`: lightweight entry history keyed by `source_id + identity_key`.
- `fetch_runs`: one row per formal fetch.
- `fetch_run_entries`: scan association table for each fetch run.
- `import_runs`: commit-level import history.
- `rating_adjustments`: API-driven rating deltas.

All tables have creation/update timestamps where useful. Schema is created with `ensure_schema`; there is no Alembic migration layer.

## 6. Source Types / 源类型模型

- `rsshub`: identity is `adapter_id + route_path`; default adapter is `rsshub_local`.
- `wechat`: identity is Source Manager `source_id`, with optional `wechat_identity` fields such as `nickname`, `mp_id`, `biz`, `fakeid`, and `feed_url`.
- `native`: identity is normalized `feed_url`; code still routes through `NativeAdapter`.

External APIs and URLs use stable `source_id` values like `src_8f3k2m9q1z0a`; there are no slugs.

## 7. Check / Fetch Semantics

`check` verifies feed access and parseability. It updates only:

- `last_checked_at`
- `last_check_status`
- `last_check_error`

It does not write entries, fetch runs, `consecutive_failures`, or `active -> broken` transitions.

`fetch` is the formal ingestion observation. It writes `fetch_runs`, `entries`, and `fetch_run_entries`, updates health fields, and participates in status flow:

- `active` after 3 consecutive fetch failures becomes `broken`.
- `broken` after a successful fetch becomes `active`.
- `paused` and `disabled` do not auto-resume.
- The system never auto-disables a source.

Fetch scans up to 50 entries and stops after 10 consecutive existing entries.

## 8. Import / Export Rules

CSV and OPML imports are preview-first. Commit records an `import_runs` row and does not store the original uploaded file content.

CSV import uses clean fields:

```text
display_name, source_type, category, tags, rating, status, adapter_id,
route_path, feed_url, original_feed_url, notes
```

System observation fields are ignored. Imported `broken` or unknown statuses become `paused`.

CSV export supports `clean` and `full`. OPML export supports `local`, `lan`, `tailscale`, and `original` profiles. Disabled sources are not exported to OPML by default.

## 9. Rating Model

`rating` is an integer from 0 to 100, defaulting to 50. It is a human value score, not source health.

It can be changed directly through source PATCH or indirectly through:

```text
POST /api/v1/sources/{source_id}/rating-adjustments
```

Reasons are fixed: `manual_adjustment`, `useful_discovery`, `duplicate_noise`, `low_value_content`, `fetch_unstable`, `recovered_quality`. Check/fetch never auto-adjust rating.

## 10. UI Model / 前端心智模型

Top-level navigation has only:

- 源列表
- 导入导出
- 设置

The source list is the home screen. It includes a compact health summary, search/filter controls, source table, source actions, and minimal batch editing. Source detail shows metadata, health, recent entries, and recent fetch runs. Settings is read-only.

## 11. API Surface / API 边界

All application APIs live under `/api/v1`:

```text
GET    /sources
POST   /sources
GET    /sources/{source_id}
PATCH  /sources/{source_id}
DELETE /sources/{source_id}
POST   /sources/{source_id}/check
POST   /sources/{source_id}/fetch
POST   /sources/check-batch
POST   /sources/fetch-batch
POST   /sources/{source_id}/rating-adjustments
POST   /imports/opml/preview
POST   /imports/opml/commit
POST   /imports/csv/preview
POST   /imports/csv/commit
GET    /exports/opml
GET    /exports/csv
GET    /settings
```

FastAPI `/docs` and `/openapi.json` remain enabled.

## 12. Persistence / 单一数据库原则

Default DB:

```text
rsshub/source_manager/data/source_manager.sqlite3
```

The file is created if absent, reused if present, and never cleared at startup. `SOURCE_MANAGER_DB_PATH` can override this for advanced tests or isolated runs, but the documented path remains the main path. Startup scripts and the settings page show the active database path.

## 13. Validation Matrix / 第一阶段验收矩阵

| 能力 | 第一阶段要求 | 验收方式 | 状态 | 备注 |
|---|---|---|---|---|
| 单一数据库 | 只使用 `source_manager.sqlite3` | 启动日志和设置页显示 DB path | done | 无 reset |
| Source CRUD | 支持 rsshub/wechat/native | API + UI 创建编辑停用 | done | 删除为 disabled |
| CSV 导入 | preview + commit | API/UI 导入 clean 字段 | done | 默认 skip |
| OPML 导入 | preview + commit | API/UI 导入 OPML | done | 支持重复检测 |
| CSV 导出 | clean/full | 下载文件检查字段 | done | clean 默认 |
| OPML 导出 | profile | local/original 导出 | done | disabled 默认不导出 |
| check | 不写 entry 历史 | API/UI 验证 | done | 不触发 broken |
| fetch | 写 entries/fetch_runs | DB/API/UI 验证 | done | 不保存 raw |
| batch check | 默认 active+broken | API/UI 验证 | done | 可包含 paused |
| batch fetch | 默认 active | API/UI 验证 | done | hard limit 10 |
| rating | 0-100 + adjustment API | pytest/API 验证 clamp | done | 不自动评分 |
| React UI | 三个顶级导航 | Vite build | done | 源列表/导入导出/设置 |
| 设置页 | 只读 | 显示 DB/config/adapters | done | 不可编辑 |
| 测试 | 后端核心单测 | pytest | done | 无前端/E2E |
| 登录权限 | 第一阶段不做 | 代码和 UI 检查 | intentionally_not_done | 本机绑定 |
| scheduler | 第一阶段不做 | 代码检查 | intentionally_not_done | 手动/API 触发 |
| AI/LLM | 第一阶段不做 | 代码检查 | intentionally_not_done | 无模型依赖 |

## 14. Decision Log / 决策记录

- D001: Source Manager is independent from `content_inbox`; old code is reference only.
- D002: The module lives under `rsshub/source_manager/` but does not modify RSSHub itself.
- D003: Persistence uses one SQLite DB at `data/source_manager.sqlite3`.
- D004: No reset API or reset UI is provided.
- D005: No login, auth, session, token, or user role system in phase one.
- D006: No scheduler in phase one; operations are manual/API-triggered.
- D007: `check` and `fetch` are separate operations with separate side effects.
- D008: Raw feed, raw entry, content HTML, and full text are not stored.
- D009: Lightweight entry history is stored for source health and incremental fetch.
- D010: Fetch uses `scan_limit + existing_streak`, not stop-on-first-existing.
- D011: Rating is 0-100 and never automatically changed by check/fetch.
- D012: CSV and OPML import are preview-first.
- D013: React + FastAPI is used for a small independent management UI.
- D014: Schema management uses `ensure_schema`, not Alembic.
- D015: Backend core tests cover IDs, schema, status flow, entry identity, import/export, and rating.

