# content_inbox_console 前端交互逻辑完整手册

## 一、系统架构总览

```text
浏览器 (localhost:8788)                   后端 API (localhost:8787)
┌─────────────────────────┐              ┌──────────────────────────┐
│ content_inbox_console   │   HTTP/JSON  │ content_inbox            │
│ (FastAPI + Jinja2)      │ ──────────> │ (FastAPI + SQLite)       │
│                         │ <────────── │                          │
│ 纯前端，无数据库访问      │              │ 持有 SQLite，所有业务逻辑  │
└─────────────────────────┘              └──────────────────────────┘
```

- **Console 前端** :8788 — 服务端渲染的 Jinja2 模板，通过 `BackendClient` (httpx) 调用后端 API。**不持有任何数据库连接**。
- **后端 API** :8787 — 所有数据操作、业务逻辑的唯一入口。返回统一 envelope：`{ok, data, error, meta}`。
- **CSS 框架**: Pico CSS v2 (CDN) + 自定义 `app.css` (548行)
- **JS**: HTMX 2.0.4 已加载但当前未使用，所有交互走传统 form POST + 服务端 redirect

### 后端 API 分组

| 分组 | 路径前缀 | 用途 |
|------|---------|------|
| 环境管理 | `/api/environment/**` | 数据库发现、切换、健康检查、元数据 |
| 数据清理 | `/api/environment/reset/**` | 预览/执行各级别的数据重置 |
| Source 管理 | `/api/sources/**` | CRUD、导入导出、批量操作 |
| Run 管理 | `/api/runs/**` | 创建、预览、启动、监控、取消 |
| Item 查询 | `/api/items/**` | 列表、详情、原始内容、语义数据 |
| 去重 | `/api/dedupe-groups/**` | 去重组查看和管理 |
| 聚类 | `/api/clusters/**` | 事件聚类，可提升为 event |
| 事件 | `/api/events/**` | 事件查看、审核 |
| 实体/关系/声明 | `/api/entities/**`, `/api/relations/**`, `/api/claims/**` | 语义提取对象 |
| 主题 | `/api/topics/**` | 主题和关联条目 |
| 时间线 | `/api/timeline` | 事件时间线 |
| 审核队列 | `/api/review-queue/**` | 待审核项管理 |
| 证据 | `/api/evidence/**` | 语义提取作为证据 |
| 简报 | `/api/briefings/**` | 每日/每周简报生成和查看 |
| 报告 | `/api/reports/**` | 报告生成和查看 |
| 保存视图 | `/api/saved-views/**` | 视图保存和管理 |
| Agent 查询 | `/api/agent-query/preview` | LLM 查询上下文打包 |
| 健康检查 | `/health` | 数据库路径、AI 配置、向量支持 |

---

## 二、核心概念解释

### 2.1 Fresh DB vs Legacy DB

系统区分两种数据库：

| | Fresh DB | Legacy DB (content_inbox.sqlite3) |
|---|---|---|
| **路径** | `data/environments/<label>/content_inbox.db` | `data/content_inbox.sqlite3` |
| **定位** | 隔离的工作环境，可安全重置 | 主数据库 / 历史数据 |
| **is_fresh_database** | `true` | `true`（当前实现） |
| **危险操作** | 允许 reset | 允许（当前实现） |
| **来源** | 通过 `/environment/init-fresh` 创建 | 历史遗留 |

当前实现中，两者都是合法的工作数据库，`is_fresh_database` 均为 `true`。

### 2.2 Dry-run vs Real-write

Run 有两种模式：

| | dry-run | real-write |
|---|---|---|
| **写入数据库** | 不写入 | 写入 items |
| **需要 gate** | 不需要 | 需要 `CONTENT_INBOX_ENABLE_REAL_RUNS=1` |
| **用途** | 验证 source 可访问性、评估抓取范围 | 实际采集内容 |

### 2.3 统一 API Envelope

所有后端响应格式：

```json
{
  "ok": true,
  "data": { /* 实际数据 */ },
  "error": null,
  "meta": {}
}
```

错误时：
```json
{
  "ok": false,
  "data": null,
  "error": {"code": "ERROR_CODE", "message": "人类可读描述", "details": {}},
  "meta": {}
}
```

Console 端 `err(response)` 提取 `code: message` 用于页面顶部红色横幅展示。

---

## 三、页面布局结构

### 3.1 全局骨架 (base.html)

```text
┌────────────────────────────────────────────┐
│ 导航栏 (nav.html)                          │
│ brand: information-center 作战台            │
│ pill groups: 作战首页 | 开始使用 | 信息消费  │
│             | 维护 | 高级(折叠)             │
├────────────────────────────────────────────┤
│ 环境条 (env-strip)                         │
│ [数据库选择器 ▼] real-write: ON/OFF        │
│ Sources: N  Items: N  Runs: N              │
├────────────────────────────────────────────┤
│ 错误横幅 (error-banner) — 仅在出错时显示     │
│ 错误消息 + Backend API 地址                │
├────────────────────────────────────────────┤
│ {% block content %}                        │
│   页面具体内容                              │
│ {% endblock %}                             │
└────────────────────────────────────────────┘
```

**环境条 (`env-strip`)**：每个页面都显示，包含：
- **数据库选择器** (`db_selector.html`) — 下拉菜单列出所有可用数据库，选中立即切换
- **real-write 状态** — 绿色 `ON` 或黄色 `OFF`
- **统计数字** — Sources / Items / Runs 数量

**错误横幅**：当 `error` 或 `error_reason` 变量非空时显示，红色左边框。

### 3.2 导航结构 (nav.html)

| 分组 | 链接 | 路由 | 说明 |
|------|------|------|------|
| **作战首页** | 作战首页 | `/dashboard` | 仪表盘 |
| **开始使用** | 环境 | `/environment` | 查看/切换数据库 |
| | Sources | `/sources` | 管理 RSS 源 |
| | 创建 Run | `/runs/new` | 创建新的采集运行 |
| | Runs | `/runs` | 运行历史 |
| **信息消费** | 事件 | `/events` | 查看事件 |
| | 待审核 | `/review-queue` | 审核队列 |
| | Briefing | `/briefings` | 简报 |
| | Report | `/reports` | 报告 |
| | Agent | `/agent-query` | LLM 查询 |
| **维护** | 数据清理 | `/reset` | 数据重置 |
| | 设置 | `/settings` | 静态设置页 |
| **高级** (折叠) | Items | `/items` | 条目列表 |
| | Dedupe | `/dedupe-groups` | 去重组 |
| | Clusters | `/clusters` | 聚类 |
| | Entities | `/entities` | 实体 |
| | Relations | `/relations` | 关系 |
| | Claims | `/claims` | 声明 |
| | Topics | `/topics` | 主题 |
| | Timeline | `/timeline` | 时间线 |
| | Evidence | `/evidence` | 证据 |
| | Views | `/saved-views` | 保存的视图 |

**高亮逻辑**：每个模板设置 `active_page` 变量（如 `dashboard`、`sources`、`runs`），nav.html 据此添加 `class="active"`。

---

## 四、页面交互详解

### 4.1 作战首页 (Dashboard) — `/dashboard`

**页面目的**：一站式的状态概览和下一步行动指导。

**后端 API 调用**（并行发起 7 个请求）：

| API | 参数 | 用途 |
|-----|------|------|
| `GET /api/environment` | — | 环境信息（DB path、is_fresh、统计数字） |
| `GET /api/sources` | `limit=8` | 最近的 sources |
| `GET /api/runs` | `limit=8` | 最近的 runs |
| `GET /api/events` | `limit=6` | 最近的 events |
| `GET /api/review-queue` | `limit=6` | 待审核项 |
| `GET /api/briefings/daily` | — | 每日简报 |
| `GET /api/reports` | — | 报告 |

**下一步行动逻辑**（`next_actions` 生成规则）：

```text
if 不是 Fresh DB:
    → "先确认环境" — 当前不是 Fresh DB，危险操作已禁用
elif 没有任何 source:
    → "导入 source" — 从这里开始准备信息入口
elif 没有任何 run:
    → "创建 dry-run" — 已有 source，先 dry-run 验证抓取范围
elif 最后一次 run 是 dry_run 且成功:
    → "执行 real-write" — dry-run 已完成，确认后可用相同 source 范围写入
elif 最后一次 run 是 real_write 且有 events:
    → "处理 review queue" — 已有 event/review，建议人工确认候选事件
elif 最后一次 run 是 real_write:
    → "执行 pipeline" — real-write 完成后继续 dedupe/semantic/events
if 有待审核项:
    → "进入待审核" — 当前有 N 条待处理 review
if 有 events 但没有 briefing:
    → "生成 briefing" — 已有 event，可以生成每日简报
```

**页面区域**：
1. **Hero 面板**：标题 "作战首页" + 环境指示
2. **统计网格**：Sources / Items / Runs / Pending Reviews 卡片
3. **下一步操作卡片**：最多 4 张可点击卡片，每张有标题、描述和跳转按钮
4. **最近 Run 摘要**：最后一次 run 的状态、进度
5. **待审核预览**：最近 6 条 review
6. **最近简报/报告/事件**：各取最近条目

---

### 4.2 环境页 (Environment) — `/environment`

**页面目的**：查看当前数据库的完整身份信息、Legacy DB 的校验信息、健康检查结果，以及创建新 Fresh DB 或执行数据清理。

**后端 API 调用**：
| API | 用途 |
|-----|------|
| `GET /api/environment` | 环境快照 + Legacy DB 文件证明 |
| `GET /api/environment/health` | 健康检查项列表 |

**显示内容**：

```
环境信息：
  database_id:     db_7ea51ae22001
  database_label:  content_inbox
  database_path:   /path/to/content_inbox.sqlite3
  is_fresh_database: true
  environment_kind: fresh
  real_runs_enabled: false
  source_count / item_count / run_count

Legacy DB 证明：
  path:    /path/to/content_inbox.sqlite3
  exists:  true
  size:    113 MB
  sha256:  401746f7...

健康检查：
  ✓ database_exists
  ✓ fresh_database
  ✓ not_legacy_default
  ✗ real_runs_enabled (需要 CONTENT_INBOX_ENABLE_REAL_RUNS=1)
```

**操作**：
- **创建新 Fresh DB**：POST `/environment/init-fresh`，输入 label，创建 `data/environments/<label>/content_inbox.db` 并切换
- **进入数据清理**：跳转到 `/reset`

**数据库切换风险**：页面顶部环境条中的数据库选择器可在任意页面切换，切换后页面刷新，当前工作数据库立即改变。

---

### 4.3 数据库选择器 (db_selector.html) — 全局组件

**渲染位置**：`base.html` 的环境条内，每个页面都显示。

**数据来源**：`render()` 函数自动调用 `GET /api/environment/databases`，返回 `{databases: [...]}`。

**每个数据库条目**：
```json
{
  "label": "content_inbox",       // 显示名称
  "path": "/app/data/content_inbox.sqlite3",
  "size": 113274880,
  "last_modified": "2026-05-18T03:04:53",
  "is_current": true,             // 当前选中的数据库
  "is_legacy": false,            // 是否标记为 Legacy
  "exists": true                  // 文件是否存在
}
```

**数据库发现逻辑**（后端 `discover_databases()`）：
1. 扫描 `data/content_inbox.sqlite3`（label: `content_inbox`）
2. 扫描 `data/environments/<label>/content_inbox.db`（label: 目录名）
3. 扫描 `/data/environments/<label>/content_inbox.db`（Docker 路径）

**切换过程**：
1. 用户在下拉菜单选择数据库 → `onchange="this.form.submit()"`
2. `POST /environment/switch` 发送 `database_path` 到 console
3. Console 转发 `POST /api/environment/switch` 到后端
4. 后端验证文件是有效的 SQLite 数据库
5. 创建新 `InboxStore`，更新 `settings.database_path`
6. 返回环境快照，console 重定向回来源页面

---

### 4.4 Sources 管理 — `/sources`

**页面目的**：管理 RSS 源的全生命周期。

**后端 API 调用**：`GET /api/sources?status=&keyword=&limit=200`

**功能区域**：

#### a) 新增单个 Source
1. 输入 Feed URL → `POST /sources/check`
2. 后端尝试解析 feed：验证 URL、检查重复、返回 sample titles
3. 展示检查结果：是否有效、是否重复、最新条目预览
4. 用户确认 → `POST /sources/add` → 创建 source

#### b) 批量导入
1. 选择格式（URLs / JSON / CSV / OPML）、粘贴内容
2. `POST /sources/import/preview` → 展示分类：new / exists / duplicate_in_file
3. `POST /sources/import/commit` → 批量创建

#### c) Source 列表
- 搜索：按 keyword 过滤
- 状态过滤：active / disabled / archived / error
- 批量操作：勾选 → enable / disable / archive / delete (均支持 preview → commit)

#### d) 导出
- `POST /sources/export` → JSON / CSV / OPML 格式

#### e) Source 详情 (`/sources/{source_id}`)
- 编辑表单：name、category、URL、status、priority、tags、notes
- 归档/恢复按钮
- 最近的 items 列表
- 审计日志

**批量操作流程**：
```text
勾选 sources → 选择 action → POST /sources/bulk (preview=1)
→ 展示影响预览 (affected sources、risk_level)
→ POST /sources/bulk/commit (operation_id) → 执行
```

---

### 4.5 Run 创建向导 — `/runs/new`

**页面目的**：5 步创建 RSS 采集运行。

**后端 API 调用**：
| API | 用途 |
|-----|------|
| `GET /api/environment` | 确认当前环境 |
| `GET /api/sources?status=active&limit=500` | 加载活跃 sources 供选择 |

**5 个步骤**：

```
Step 1: 环境确认
  → 显示当前 DB path、is_fresh_database、real-write gate 状态

Step 2: Source 选择
  → 勾选要抓取的 sources（卡片式复选框）
  → 或全选所有活跃 sources

Step 3: 时间范围
  → published_from (可选)
  → published_to (可选)
  → 时区: Asia/Shanghai

Step 4: 限制参数
  → max_sources: 最多处理几个 source (默认 20)
  → max_items_per_source: 每个 source 最多取几条 (默认 20)
  → max_total_items: 总共最多取几条 (默认 200)
  → source_timeout_seconds: 单个 source 超时 (默认 30)
  → run_timeout_minutes: 整个 run 超时 (默认 30)

Step 5: 模式选择
  → dry-run: 不写入数据库，仅统计
  → real-write: 写入数据库 (需要 gate 开启)
```

**提交流程**：
```text
填写表单 → POST /runs/preview → 展示影响范围预览
→ 确认 → POST /runs/start → 创建 run → 跳转到 /runs/{run_id}
```

**Preview 数据**：
```json
{
  "mode": "dry_run",
  "source_count": 5,
  "sources": [{"source_id", "source_name", "status"}, ...],
  "will_write_items": false,
  "risk_level": "low",
  "requires_confirmation": false,
  "database": { /* environment_snapshot */ }
}
```

---

### 4.6 Run 详情与 Pipeline — `/runs/{run_id}`

**页面目的**：查看运行状态、执行 pipeline 阶段。

**后端 API 调用**：
| API | 用途 |
|-----|------|
| `GET /api/runs/{run_id}/summary` | 综合摘要（run + sources + events + pipeline status） |
| `GET /api/runs/{run_id}/events` | 运行事件流 |
| `GET /api/runs/{run_id}/items` | 此 run 采集的 items |

**页面区域**：

1. **统计网格**：status、mode、source 数、new items、duplicates、failures
2. **Pipeline 阶段表**：

```text
阶段        状态        操作
dedupe      pending     [运行]
semantic    pending     [运行]
clusters    pending     [运行]
events      pending     [运行]
review      pending     [运行]
briefing    pending     [运行]
report      pending     [运行]
```

每个阶段的按钮 POST 到 `/runs/{run_id}/pipeline/{stage}`。

3. **Source 进度表**：每个 source 的状态、items、errors
4. **事件时间线**：按时间顺序的 run events
5. **Items 列表**：此 run 采集的 items

**Pipeline 阶段说明**：

| 阶段 | 做什么 |
|------|--------|
| `dedupe` | 基于 dedupe_key/URL/title 创建去重组 |
| `semantic` | 轻量级语义提取（实体、主题、关系） |
| `clusters` | 事件聚类 |
| `events` | 从聚类生成候选事件 |
| `review` | 生成审核队列条目 |
| `briefing` | 生成每日简报 |
| `report` | 生成运行报告 |

**其他操作**：
- **Cancel**：`POST /runs/{run_id}/cancel` — 设置取消标志，运行线程在 source 间检查
- **Rollback preview/commit**：软回滚 run 产生的数据

---

### 4.7 数据清理 (Reset) — `/reset`

**页面目的**：安全地清空部分或全部数据。

**后端 API 调用**：
| API | 用途 |
|-----|------|
| `GET /api/environment` | 当前环境 |
| `GET /api/environment/reset-options` | 可用清理级别 |
| `GET /api/runs?limit=40` | 用于 run-scoped 清理 |
| `GET /api/sources?limit=200` | 用于 source-scoped 清理 |

**7 个清理级别**：

| 级别 | 清理内容 | 保留内容 | 风险 |
|------|---------|---------|------|
| `clear_runs_items_keep_sources` | runs、items、pipeline 输出 | sources、DB 身份 | high |
| `clear_all_sources_and_content` | 所有 sources 和内容 | schema、身份、审计 | critical |
| `clear_pipeline_outputs_keep_items` | dedupe、semantic、clusters、events 等 | sources、runs、items | medium |
| `clear_outputs_keep_events` | briefings、reports、saved views | 其他一切 | low |
| `clear_by_run_id` | 指定 run 及其独占 items 和下游 | 其他 runs、共享 items | high |
| `clear_by_source_id` | 指定 source 的 items 和下游 | 其他 sources | high |
| `create_new_fresh_db` | 切换到全新 Fresh DB | 旧数据库文件 | low |

**安全机制**：
```text
所有 reset 必须:
  1. preview-first: POST /environment/reset/preview → 展示影响范围
  2. confirmation: 必须输入确认文本 (如 "RESET")
  3. 后端再次验证 is_fresh_database
```

**Run-scoped 清理智能逻辑**：
- item 仅由该 run 引入 → 删除 item + 下游输出
- item 被多个 run 共享 → 仅删除该 run link，保留 item

---

### 4.8 审核队列 (Review Queue) — `/review-queue`

**页面目的**：人工审核候选事件。

**后端 API 调用**：`GET /api/review-queue?status=pending`

**状态过滤**：pending / resolved / dismissed

**操作**：
- `POST /review-queue/{review_id}/resolve` (status=resolved) → 确认
- `POST /review-queue/{review_id}/dismiss` (status=dismissed) → 忽略

---

### 4.9 简报 (Briefings) — `/briefings`

**后端 API 调用**：`GET /api/briefings/daily`

**操作**：`POST /briefings/daily/generate` → 生成新的每日简报

简报内容包含：近期事件摘要、待审核数量、markdown 格式正文。

---

### 4.10 报告 (Reports) — `/reports`

**后端 API 调用**：`GET /api/reports`

**操作**：`POST /reports/generate` → 选择报告类型 (summary / source_health / event) 生成

---

### 4.11 Agent 查询 — `/agent-query`

**页面目的**：为 LLM Agent 打包上下文数据。

**交互**：
1. 输入查询关键词
2. 选择输出格式：human / markdown / compact / json
3. `POST /api/agent-query/preview` → 返回匹配的 items 在不同格式下的展示
4. 展示 context_pack（items 摘要）、使用的 sources 列表

---

### 4.12 高级调试页 (统一模式)

以下页面使用 `simple_list.html` 通用模板：

| 页面 | 路由 | 后端 API |
|------|------|----------|
| Items | `/items` | `GET /api/items` (支持 run_id、keyword 过滤) |
| Dedupe Groups | `/dedupe-groups` | `GET /api/dedupe-groups` |
| Clusters | `/clusters` | `GET /api/clusters` |
| Events | `/events` | `GET /api/events` |
| Entities | `/entities` | `GET /api/entities` |
| Relations | `/relations` | `GET /api/relations` |
| Claims | `/claims` | `GET /api/claims` |
| Topics | `/topics` | `GET /api/topics` |
| Timeline | `/timeline` | `GET /api/timeline` |
| Evidence | `/evidence` | `GET /api/evidence` |
| Saved Views | `/saved-views` | `GET /api/saved-views` |

**详情页**使用 `object_detail.html`：`/clusters/{id}`、`/events/{id}`，展示 title、summary、status/confidence、supporting items、promote-to-event 按钮（仅 clusters）、原始 JSON 折叠区。

Item 详情 (`/items/{item_id}`) 使用 `item_detail.html`：canonical JSON、语义数据、实体列表。

---

## 五、数据流图

### 5.1 页面渲染流程

```text
浏览器请求 GET /dashboard
  │
  ▼
console route: dashboard(request)
  │
  ├─> BackendClient.get("/api/environment")
  ├─> BackendClient.get("/api/sources", {limit: 8})
  ├─> BackendClient.get("/api/runs", {limit: 8})
  ├─> BackendClient.get("/api/events", {limit: 6})
  ├─> BackendClient.get("/api/review-queue", {limit: 6})
  ├─> BackendClient.get("/api/briefings/daily")
  └─> BackendClient.get("/api/reports")
  │
  ▼
render(request, "ops/dashboard.html", context)
  │
  ├─> 自动注入: request, api_base
  ├─> 自动注入: environment (来自 GET /api/environment)
  ├─> 自动注入: databases (来自 GET /api/environment/databases)
  ├─> 自动注入: error_reason (来自 query params)
  └─> 合并 context 中的: environment, sources, runs, events, reviews, ...
  │
  ▼
Jinja2 渲染 base.html + ops/dashboard.html
  │
  ▼
HTML 响应返回浏览器
```

### 5.2 render() 函数的自动注入

`render()` 是 console 的核心渲染函数，每次调用自动：

1. 注入 `request` 和 `api_base` 到模板上下文
2. 如果 context 中没有 `environment` → 调用 `GET /api/environment` 获取
3. 如果 context 中没有 `databases` → 调用 `GET /api/environment/databases` 获取
4. 如果 context 中没有 `error_reason` → 从 query params 读取（用于 redirect 后的错误展示）
5. 使用 `Templates.TemplateResponse` 渲染

这意味着**环境条和数据库选择器在每个页面自动可用**，无需手动注入。

### 5.3 表单提交流程

```text
用户在页面填写表单 → 点击提交
  │
  ▼
POST /some/action (form data)
  │
  ▼
console route: async def some_action(request):
  form = await form_fields(request)  ← 解析 application/x-www-form-urlencoded
  payload = {构造 JSON payload}
  response = client(request).post("/api/...", payload)
  │
  ├─ 成功 → RedirectResponse("/target/page", 303)
  └─ 失败 → RedirectResponse("/source/page?error=错误消息", 303)
  │
  ▼
浏览器跟随重定向，GET 目标页面
  │
  ▼
render() 从 query params 读取 error → 显示在 error-banner 中
```

---

## 六、环境变量与配置链路

### 6.1 Console 前端 (content_inbox_console)

| 环境变量 | 默认值 | 作用 |
|---------|--------|------|
| `CONTENT_INBOX_CONSOLE_HOST` | `127.0.0.1` | Console 监听地址 |
| `CONTENT_INBOX_CONSOLE_PORT` | `8788` | Console 监听端口 |
| `CONTENT_INBOX_FRONTEND_API_BASE` | `http://127.0.0.1:8787` | 后端 API 地址 |
| `CONTENT_INBOX_CONSOLE_PAGE_SIZE` | `50` | 分页大小 |

### 6.2 后端 API (content_inbox)

| 环境变量 | 默认值 | 作用 |
|---------|--------|------|
| `CONTENT_INBOX_DB_PATH` | config.py 计算 | 数据库路径（最高优先级） |
| `CONTENT_INBOX_DB` | config.py 计算 | 数据库路径（次优先级） |
| `CONTENT_INBOX_HOST` | `127.0.0.1` | API 监听地址 |
| `CONTENT_INBOX_PORT` | `8787` | API 监听端口 |
| `CONTENT_INBOX_ENABLE_REAL_RUNS` | `0` | 允许 real-write run |
| `CONTENT_INBOX_ENVIRONMENT` | `fresh` | 环境标识 |

### 6.3 数据库路径决策链

```text
CONTENT_INBOX_DB_PATH 环境变量
  ↓ (如果未设置)
CONTENT_INBOX_DB 环境变量
  ↓ (如果未设置)
config.py 默认逻辑:
  1. data/content_inbox.sqlite3 (如果文件存在)
  2. data/environments/fresh_default/content_inbox.db (兜底)
```

**Docker 环境**：docker-compose.yml 不再硬编码 `CONTENT_INBOX_DB_PATH`，数据库路径由 `.env` 文件中的 `CONTENT_INBOX_DB` 或代码默认值决定。卷挂载为 `./data:/app/data`。

---

## 七、完整用户工作流

### 7.1 首次使用

```text
1. 访问 http://localhost:8788 → 重定向到 /dashboard
2. Dashboard 显示 "导入 source" → 点击进入 /sources
3. 添加 RSS sources:
   a. 单个添加: 输入 URL → check → 确认 → add
   b. 批量导入: 粘贴 URLs → preview → commit
4. 返回 Dashboard → 显示 "创建 dry-run"
5. 进入 /runs/new → 选择 sources → dry-run → preview → start
6. Dry-run 完成 → Dashboard 显示 "执行 real-write"
7. 修改 .env 设置 CONTENT_INBOX_ENABLE_REAL_RUNS=1，重启后端
8. 再次创建 run → 选择 real-write → start
9. Run 完成后 → 执行 pipeline 阶段 (dedupe → semantic → clusters → events → review)
10. 处理 review queue → resolve/dismiss 候选事件
11. 生成 briefing / report
12. 使用 agent-query 查询上下文
```

### 7.2 日常使用

```text
1. Dashboard 查看状态
2. 根据需要: 添加新 source / 创建新 run
3. 执行 pipeline 各阶段
4. 处理 review queue
5. 查看 briefings / events / reports
```

### 7.3 重新开始

```text
1. /reset → 选择清理级别
2. preview → 确认影响范围
3. 输入确认文本 → commit
4. 或: /environment → 创建新 Fresh DB → 切换
```

---

## 八、错误处理

### 8.1 前端错误处理

| 场景 | 处理方式 |
|------|---------|
| 后端返回 `ok: false` | `err()` 提取 `code: message`，页面顶部红色横幅 |
| 后端连接失败 | `BackendClient` 捕获所有异常，返回 `BACKEND_UNAVAILABLE` |
| 数据库切换失败 | Redirect 到 `/?error=错误消息`，由 error_reason 展示 |

### 8.2 后端错误码（常见）

| 错误码 | HTTP 状态 | 含义 |
|--------|----------|------|
| `MISSING_DATABASE_PATH` | 400 | 未提供 database_path |
| `DATABASE_NOT_FOUND` | 400 | 数据库文件不存在 |
| `INVALID_DATABASE` | 400 | 无法作为 SQLite 打开 |
| `FRESH_DB_REQUIRED` | 400 | 操作需要 Fresh DB |
| `UNSAFE_OPERATION_REQUIRES_CONFIRMATION` | 400 | 危险操作需要确认文本 |
| `INVALID_RESET_LEVEL` | 400 | 无效的清理级别 |
| `RUN_ID_REQUIRED` | 400 | run-scoped 清理需要 run_id |
| `SOURCE_ID_REQUIRED` | 400 | source-scoped 清理需要 source_id |
| `SOURCE_NOT_FOUND` | 404 | Source 不存在 |
| `RUN_NOT_FOUND` | 404 | Run 不存在 |
| `ITEM_NOT_FOUND` | 404 | Item 不存在 |
| `OPERATION_NOT_FOUND` | 404 | 预览操作过期 |
| `SOURCE_DUPLICATE` | 409 | Source 已存在 |
| `NO_SOURCES_SELECTED` | 400 | Run 没有选择 source |
| `INVALID_RUN_MODE` | 400 | 无效的 run mode |
| `BACKEND_UNAVAILABLE` | — | 前端无法连接后端 |

---

## 九、关键设计决策

1. **无前端数据库访问**：Console 是纯前端，所有数据通过 API。安全边界由后端控制。
2. **Preview-first 模式**：所有危险操作（reset、import、bulk）都先 preview 再 commit。
3. **服务端渲染 + 传统表单**：不使用 SPA 架构，所有页面通过服务端渲染 + form POST + redirect。
4. **HTMX 已加载未使用**：`base.html` 加载了 HTMX，但当前没有任何 `hx-*` 属性，为未来渐进增强预留。
5. **任务导航而非对象导航**：一级导航按用户任务分组（开始使用 → 信息消费 → 维护），对象浏览器放入"高级"折叠区。
6. **环境条常驻**：数据库选择器和统计数字在每个页面顶部可见，切换数据库不需要导航到特定页面。
7. **统一 envelope**：前端和后端之间通过 `{ok, data, error, meta}` 协议通信，错误处理统一。
