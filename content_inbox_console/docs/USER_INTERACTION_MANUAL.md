# content_inbox_console 用户交互手册

本文档从用户视角出发，逐页描述 content_inbox_console 前端中**每一个可见元素和可交互控件**，包括：它是什么、它在哪、点击/输入后会发生什么。

---

## 全局元素（每个页面都出现）

### 导航栏

页面最顶部，深色半透明背景，始终固定（sticky）。

**左侧 Brand 区**：
- 显示 "information-center"（加粗）+ 下方 "作战台"（小字大写）。
- 纯文本，不可点击。

**右侧导航链接区**，分为 5 组，每组是一个圆角卡片状容器：

| 分组 | 包含链接 | 点击后跳转 |
|------|---------|-----------|
| 作战首页 | 作战首页 | `/dashboard` |
| 开始使用 | 环境 | `/environment` |
| | Sources | `/sources` |
| | 创建 Run | `/runs/new` |
| | Runs | `/runs` |
| 信息消费 | 事件 | `/events` |
| | 待审核 | `/review-queue` |
| | Briefing | `/briefings` |
| | Report | `/reports` |
| | Agent | `/agent-query` |
| 维护 | 数据清理 | `/reset` |
| | 设置 | `/settings` |
| 高级 ▼ | Items | `/items` |
| | Dedupe | `/dedupe-groups` |
| | Clusters | `/clusters` |
| | Entities | `/entities` |
| | Relations | `/relations` |
| | Claims | `/claims` |
| | Topics | `/topics` |
| | Timeline | `/timeline` |
| | Evidence | `/evidence` |
| | Views | `/saved-views` |

- 当前所在页面的链接高亮（绿色）。
- "高级"是一个折叠菜单（点击展开/收起），展开后显示 10 个调试页面链接，竖向排列。

### 环境信息条

导航栏下方，浅色背景的一行横条，左侧有绿色竖线（如果当前数据库不是 Fresh DB 则变为红色）。

**数据库选择器**（左侧）：
- 标签文字："数据库"
- 一个下拉菜单 `<select>`，列出所有发现的数据库文件
- 每个选项显示：数据库标签名（如 `content_inbox`、`fresh_default`）+ 如果文件不存在则显示 `[缺失]`
- 当前正在使用的数据库默认选中
- **选择任意数据库后页面立即自动提交并刷新**（`onchange="this.form.submit()"`），无需额外点击按钮
- 切换后的行为：后端打开新的 SQLite 文件，更新环境元数据，写审计日志，然后浏览器重定向回切换前所在页面

**环境元数据区**（右侧）：
- `real-write: ON`（绿色徽章）或 `real-write: OFF`（黄色徽章）— 指示当前是否可以执行真实写库的 run
- `Sources: N` — 当前数据库中的 source 数量
- `Items: N` — 当前数据库中的 item 数量
- `Runs: N` — 当前数据库中的 run 数量
- 以上均为纯文本展示，不可交互

### 错误横幅

只在出错时出现。红色左边框，白色背景。
- 显示错误代码和消息（中文）
- 下方小字显示后端 API 地址
- 例如："BACKEND_UNAVAILABLE: 无法连接到后端 API" 或 "INVALID_DATABASE: Cannot open as SQLite database: ..."
- 不可手动关闭，解决错误后刷新页面即消失

---

## 作战首页（Dashboard）— `/dashboard`

### 页面标题区（Hero Panel）

- 大字标题："从 source 到 briefing 的下一步作战台"
- 副标题说明页面用途
- 两个按钮：
  - **"准备 / 导入 source"**（主按钮，实心绿）— 点击跳转 `/sources`
  - **"创建 run"**（次按钮，空心）— 点击跳转 `/runs/new`

### 统计卡片（Stats Grid）

4 个卡片横向排列：

1. **环境安全**
   - 大数字：显示 "安全" 或 "需确认"
   - 小字：`Legacy DB affected: false`
   - 不可点击，纯状态展示

2. **Sources**
   - 大数字：当前 source 总数
   - 小字：其中 active 状态的数量
   - 不可点击

3. **Items**
   - 大数字：当前 item 总数
   - 小字："当前 Fresh DB"
   - 不可点击

4. **Runs**
   - 大数字：当前 run 总数
   - 小字：real-write 是否启用（"已启用" / "未启用"）
   - 不可点击

### real-write 警告横幅

仅当 `real_runs_enabled` 为 false 时显示。黄色/琥珀色左边框。
- 标题："real-write 未启用。"
- 说明：需要在后端设置 `CONTENT_INBOX_ENABLE_REAL_RUNS=1` 并重启
- 不包含可点击按钮，纯提示

### 下一步建议区（Next Actions）

左侧卡片，标题 "下一步建议"。

- 如果没有建议：显示空状态文字 "当前没有明显阻塞。可以查看事件中心、生成 briefing，或进入数据清理重新开始。"
- 如果有建议：每条建议是一个卡片行，包含：
  - **标签**（加粗）：如 "导入 source"、"创建 dry-run"、"执行 real-write"、"处理 review queue"
  - **描述文字**：说明为什么需要做这一步
  - **"去处理" 按钮**：点击跳转到对应页面（如 `/sources`、`/runs/new`、`/review-queue`）

### 最近 Run 区

右侧卡片，标题 "最近 run"。

- 如果没有 run：显示空状态 "暂无 run。先导入 source，再创建 dry-run。"
- 如果有 run：以定义列表展示：
  - `run_id`：可点击的代码文本，跳转到 `/runs/{run_id}`
  - `状态 / mode`：如 `success / dry_run`
  - `inserted / duplicate / failed`：三个数字
  - `started_at`：启动时间

### 待处理 Review Queue 区

左侧卡片，标题 "待处理 review queue"。

- 如果没有待处理项：空状态文字，提示 pipeline 生成 event 后这里会出现人工确认任务
- 如果有：表格显示每条 review 的 `review_type`、`target_type:target_id`、和一个 **"处理"** 链接 → 跳转 `/review-queue`

### 最近 Briefing / Report 区

右侧卡片，标题 "最近 briefing / report"。

- 显示最近一条 briefing 的标题（或 "暂无"）
- 显示最近一条 report 的标题（或 "暂无"）
- 两个链接：**"查看 briefing"** → `/briefings`、**"查看 report"** → `/reports`

### 最近 Events 区

左侧卡片，标题 "最近 Events"。

- 如果没有 events：空状态文字
- 如果有：紧凑卡片列表，每条显示：
  - **标题**（可点击链接） → `/events/{event_id}`
  - 摘要文字（或 "暂无摘要"）
  - 状态标签（chip），如 `active`、`needs_review`

### 环境提示区

右侧卡片，标题 "环境提示"。

- 显示当前 API base 地址（代码字体）
- 显示 Fresh DB 路径（代码字体）
- 显示 DB ID（代码字体）
- **"需要清空某部分数据重新开始？进入数据清理页"** — 可点击链接 → `/reset`

---

## 环境页（Environment）— `/environment`

### 页面标题区

- 标题："环境 / Fresh DB"
- 说明文字
- 两个按钮：
  - **"刷新"** → 重新加载当前页面
  - **"数据清理 / 重新开始"** → `/reset`

### 非空库警告

仅当数据库中有数据时显示。黄色横幅。
- 显示当前 sources、items、runs 数量
- 提示可以使用数据重置回到干净状态

### 当前 Fresh DB 信息卡

左侧卡片，以定义列表展示：
- `database_id`：数据库唯一 ID（代码字体）
- `database_label`：标签名
- `database_path`：文件路径（代码字体）
- `schema_version`：如 `operational_v1`
- `environment_kind`：如 `fresh`
- `is_fresh_database`：`True` 或 `False`
- `source / item / run`：三个统计数字
- `real-write`：启用状态及设置说明
- `legacy fallback`："否" 或 "是，需排查"
- `最近 reset`：最后重置时间或 "暂无"

全部为只读展示。

### Legacy DB 只读证明卡

右侧卡片，展示 `content_inbox.sqlite3` 的文件校验信息：
- `path`：文件路径
- `exists`：是否存在
- `size`：文件大小（字节）
- `modified_at`：最后修改时间
- `sha256`：SHA-256 校验和（小号代码字体）

全部为只读展示。

### 健康检查表

全宽卡片，4 行表格：

| 检查项 | 可能的状态 | 说明 |
|--------|-----------|------|
| `database_exists` | 通过 / 需要处理 | 数据库文件路径 |
| `fresh_database` | 通过 / 需要处理 | 数据库标签 |
| `not_legacy_default` | 通过 | 提示 content_inbox.sqlite3 是默认主数据库 |
| `real_runs_enabled` | 通过 / 需要处理 | 提示需要设置环境变量 |

### 数据清理入口卡

左侧卡片，红色左边框（danger-zone）。
- 说明 reset 已移到独立页面
- **"进入数据清理页"** 按钮 → `/reset`

### 新建 Fresh DB 环境卡

右侧卡片。
- 说明文字：创建一个全新的 Fresh DB 并切换
- **表单**：
  - 文本输入框 `database_label`：新环境名称（占位符：`fresh_YYYYMMDD_HHMMSS`）
  - **"新建并切换 Fresh DB"** 提交按钮
- 提交行为：`POST /environment/init-fresh` → 后端在 `data/environments/<label>/content_inbox.db` 创建新数据库 → 切换 → 重定向回 `/environment`

---

## Source 管理页（Sources）— `/sources`

### 页面标题区

- 标题："Source 管理"
- 说明文字
- **"选择 sources 创建 run"** 按钮 → `/runs/new`

### 新增单个 Source 区

左侧卡片，标题 "新增单个 source"。

**表单字段**（`POST /sources/check`）：
1. `source_name`：文本输入，占位符 "示例：OpenAI Blog"
2. `feed_url`：文本输入，占位符 "https://example.com/feed.xml"
3. `site_url`：文本输入，占位符 "https://example.com"
4. `source_category`：文本输入，占位符 "AI/产品"
5. **"检查 source"** 提交按钮

**点击"检查 source"后的行为**：
- 页面刷新，下方展开一个折叠区（`<details open>`），显示检查结果的 JSON：
  - `valid`：是否有效
  - `parse_ok`：是否成功解析
  - `duplicate`：是否与已有 source 重复
  - `sample_titles`：feed 中最近的条目标题
  - `sample_item_count`：样本数量
  - `latest_published_at`：最新发布时间
- 如果检查通过且不重复，在检查结果下方出现**第二个表单**（`POST /sources/add`）：
  - 隐藏字段：自动带入 source_name、feed_url、category
  - `tags`：文本输入，逗号分隔
  - `notes`：多行文本输入（2 行）
  - **"确认新增 source"** 提交按钮
  - 点击后创建 source，重定向回 `/sources`

### 批量导入 Sources 区

右侧卡片，标题 "批量导入 sources"。

**表单字段**（`POST /sources/import/preview`）：
1. `format`：下拉选择 — 每行 URL / CSV text / JSON text / OPML text
2. `content`：多行文本输入（7 行），占位符提示格式
3. **"Preview 导入"** 提交按钮

**点击"Preview 导入"后的行为**：
- 页面刷新，下方出现"Source Import Preview"区域，包含：
  - 统计摘要：总数、新增、已存在、文件内重复
  - **"Commit 导入"** 按钮 → `POST /sources/import/commit`
  - 预览表格：每行的状态、名称、分类、URL
- 点击 Commit 后执行实际导入，重定向回 `/sources`

### 导出 Sources 区

全宽卡片，标题 "导出 Sources"。

- 下拉选择 `format`：JSON / CSV / OPML
- **"导出当前 source registry"** 按钮 → `POST /sources/export`
- 点击后页面刷新，下方出现导出结果折叠区，显示格式、数量和导出内容

### Source 列表区

全宽卡片，标题 "Source 列表"。

**搜索/过滤栏**（`GET /sources`）：
1. `keyword`：文本输入，搜索 source 名称或 URL
2. `status`：下拉选择 — 任意状态 / active / disabled / broken / archived
3. **"搜索 / 刷新"** 按钮

**Source 表格**（如果列表非空）：
- 表头：选择 | source_id | 名称 | 状态 | 最近 run | URL
- 每行：
  - **复选框**：勾选以进行批量操作
  - **source_id**：可点击链接 → `/sources/{source_id}`
  - 名称：纯文本
  - 状态：纯文本
  - 最近 run_id：纯文本
  - URL：代码字体，纯文本

**批量操作区**（表格下方）：
1. `action`：下拉选择 — 启用 / 禁用 / 归档删除 / 删除归档 / 导出选中
2. **"Preview 批量操作"** 按钮 → `POST /sources/bulk` (preview=1)
   - 点击后页面刷新，出现黄色预览横幅，显示：
     - 操作类型、影响 source 数量、是否影响 Legacy DB
     - **"确认执行批量操作"** 按钮 → `POST /sources/bulk/commit`
     - 受影响的 sources JSON 预览
3. **"去 Run 向导选择 sources"** 按钮 → `/runs/new`

**空状态**：如果没有任何 source，显示 "当前 Fresh DB 没有 sources。请新增或批量导入。"

---

## Source 详情页 — `/sources/{source_id}`

### 页面标题区

- 标题："Source Detail / {source_name}"
- 副标题：feed URL（代码字体）
- 两个按钮：
  - **"归档/删除"** → `POST /sources/{source_id}/archive`（软归档）
  - **"恢复启用"** → `POST /sources/{source_id}/restore`（从归档恢复）

### 编辑 Source 区

左侧卡片，标题 "编辑 source"。

**表单字段**（`POST /sources/{source_id}/edit`）：
1. `source_name`：文本输入，当前值预填
2. `source_category`：文本输入，当前值预填
3. `feed_url`：文本输入，当前值预填
4. `status`：下拉选择 — active / disabled / broken / archived，当前值选中
5. `priority`：数字输入，当前值预填（默认 3）
6. `tags`：文本输入，逗号分隔，当前值预填
7. `notes`：多行文本，当前值预填
8. **"保存修改"** 提交按钮 → 保存后重定向回详情页

### Source 原始状态区

右侧卡片，标题 "Source 原始状态"。
- JSON 格式化展示 source 对象的完整数据
- 只读，不可编辑

### 最近 Items 区

左侧卡片，标题 "最近 Items"。
- 如果没有 items：空状态 "暂无 items。"
- 如果有：表格显示每条 item 的标题（可点击 → `/items/{item_id}`）和发布时间

### 审计日志区

右侧卡片，标题 "Audit Log"。
- JSON 格式化展示操作审计记录
- 只读

---

## Runs 列表页 — `/runs`

### 页面标题区

- 标题："Ingest Runs"
- 说明文字
- **"New Run"** 按钮 → `/runs/new`

### Run 表格

如果没有 run：空状态 "No runs yet."

表头：Run | Status | Mode | Sources | New | Started

每行：
- **run_id**：可点击链接 → `/runs/{run_id}`
- 其余列为只读文本：status（如 success/failed/running）、mode（dry_run/real_write）、source 数、新增 item 数、启动时间

---

## Run 创建向导 — `/runs/new`

这是一个 5 步向导，所有步骤在同一个表单中（`POST /runs/preview`）。

### Step 1：确认环境

- 显示当前 Fresh DB 路径（代码字体）
- 显示 database_id、source/item/run 统计
- 如果 real-write 未启用：黄色警告文字，提示设置环境变量
- 纯信息展示，无可交互控件

### Step 2：选择 Source 范围

- `scope_type`：下拉选择
  - "手动选择 selected sources"（默认）
  - "全部 active sources"
  - "失败 sources"
- **Source 复选框网格**：
  - 每个活跃 source 显示为一个可勾选的卡片
  - 卡片内容：source 名称（加粗）、source_id（代码字体）、分类
  - 可勾选任意数量
- 如果没有 active sources：空状态 "没有 active sources。请先到 Source 管理页面新增或导入。"

### Step 3：published_at 时间范围

- 说明文字："时间范围用于过滤 RSS 返回的 items"
- `published_from`：文本输入，格式如 `2026-05-01T00:00:00+08:00`
- `published_to`：文本输入，格式如 `2026-05-18T23:59:59+08:00`
- 两个字段并排显示

### Step 4：限制参数 limits

5 个数字输入并排显示：
1. `max_sources`：默认 20
2. `max_items_per_source`：默认 20
3. `max_total_items`：默认 200
4. `source_timeout_seconds`：默认 30
5. `run_timeout_minutes`：默认 30

### Step 5：选择模式

- `mode`：下拉选择
  - "dry-run（不写入 items）"（默认）
  - "real-write（真实写入当前 Fresh DB）" — 如果 real-write 未启用则灰色不可选
- 说明文字："real-write 会向当前 Fresh DB 写入新的 items"

### 提交按钮

**"Step 6：Preview Run"** — 点击后 `POST /runs/preview`，跳转到 Run 预览页。

---

## Run 预览页 — `/runs/preview`

### 页面标题

- 标题："Run Preview / 运行预览"
- 副标题："启动前请确认影响范围。"

### 影响范围卡

如果 preview 成功，左侧卡片以定义列表展示：
- `模式`：dry_run 或 real_write
- `source 数量`：数字
- `是否写入数据库`：true 或 false
- `风险等级`：low 或 high
- `影响 Legacy DB`：固定显示 "否"
- `可 cancel`：固定显示 "是"
- `rollback`：说明支持 soft rollback

### 数据库信息卡

右侧卡片，JSON 格式展示当前数据库的环境快照。

### Sources 列表

全宽卡片，JSON 格式展示即将抓取的 sources 列表。

### 启动按钮

**"Step 7：Start Run / 启动 {mode}"** — `POST /runs/start`

- 点击后将 payload JSON 提交到后端
- 后端创建 run 记录（状态 `running`）
- 如果是 real-write 且 `CONTENT_INBOX_ENABLE_REAL_RUNS` 未开启 → 返回错误
- 成功 → 重定向到 `/runs/{run_id}`

### 失败状态

如果 preview 为空：空状态 "Preview 失败，请返回 Run 向导检查参数。"

---

## Run 详情页 — `/runs/{run_id}`

### 页面标题区

- 小字标签："Run 观察"
- 标题："Run Detail"
- 副标题：`run_id` · mode · status（代码字体）
- 按钮行：
  - **"Cancel run"**（次按钮）→ `POST /runs/{run_id}/cancel`
  - **"生成 Briefing"** → `POST /runs/{run_id}/briefing`
  - **"生成 Report"** → `POST /runs/{run_id}/report`
  - **"清除此 run 结果"**（次按钮，链接样式）→ `/reset`

### Dry-run 提示横幅

仅当 mode 为 `dry_run` 时显示。黄色左边框。
- 说明 dry-run 不写入 items，item count 为 0 是预期结果
- **"用相同思路创建 real-write"** 按钮 → `/runs/new`

### Real-write 提示

仅当 mode 为 `real_write` 时显示。
- 说明 real-write 已进入写库路径
- 建议后续运行 pipeline、处理 review queue

### 统计卡片

4 个卡片：
1. **状态**：大数字显示 run 状态，小字显示 mode
2. **Sources**：选中数 / 成功数 / 失败数
3. **Inserted**：写入的 item 数
4. **Duplicate / Failed**：重复数 / 失败数

### Pipeline 处理闭环表

全宽卡片。7 行表格：

| 阶段 | 状态（chip 标签） | 说明 | 操作按钮 |
|------|------------------|------|---------|
| dedupe | pending/completed | 发现重复组 | **"运行 dedupe"** |
| semantic | pending/completed | 抽取 entities/claims/evidence | **"运行 semantic"** |
| clusters | pending/completed | 生成 cluster | **"运行 clusters"** |
| events | pending/completed | 生成 event | **"运行 events"** |
| review | pending/completed | 生成待审核项 | **"运行 review"** |
| briefing | pending/completed | 生成简报 | **"运行 briefing"** |
| report | pending/completed | 生成报告 | **"运行 report"** |

每个阶段的 **"运行 {stage}"** 按钮 → `POST /runs/{run_id}/pipeline/{stage}`，点击后执行该阶段并刷新页面。

### Source 进度表

左侧卡片，标题 "Source Progress"。
- 表头：source | 状态 | fetched | inserted | duplicate | failed/error
- 每行显示一个 source 的处理统计
- 如果没有数据：空状态提示

### Run Events 时间线

右侧卡片，标题 "Run Events 时间线"。
- 按时间顺序显示 run event 流
- 每条格式：`#序号` `事件类型` `消息内容`
- 自动滚动到最新事件

### Items from this run

全宽卡片。
- 如果没有 items：空状态，区分 dry-run（预期无 item）和 real-write（需排查）
- 如果有：表格 — 标题（可点击 → `/items/{item_id}`）| Source 名 | 发布时间

---

## 数据清理页（Reset）— `/reset`

### 页面标题区

- 小字标签："维护与重开"
- 标题："数据清理 / 重新开始"
- 说明：所有操作 preview-first，只影响当前 Fresh DB
- **"查看环境证明"** 按钮 → `/environment`

### 禁用提示

如果当前不是 Fresh DB（`reset_enabled` 为 false），显示红色错误横幅：
- "当前数据库不是 Fresh DB，reset 已禁用。"
- 此时所有 Preview 按钮变为灰色不可点击（`disabled`）

### 安全边界卡

左侧卡片：
- 以定义列表展示：Fresh DB 状态、DB path、DB ID、Legacy affected（固定 false）、当前数据量

### 确认规则卡

右侧卡片：
- 说明全局清理需输入 `RESET`
- run/source 清理需输入 `RESET <run_id>` 或 `RESET <source_id>`
- 多个 source 使用 `RESET SOURCES`

### 清理选项卡片（7 张，网格排列）

每张卡片代表一种清理级别：

**卡片通用结构**：
- **标题**（加粗）：如 "清空运行结果，保留 Sources"
- **风险标签**（chip）：`high` / `medium` / `low` / `critical`，颜色不同
- **说明文字**：描述这个级别做什么
- **折叠详情**（`<details>`）：点击展开显示 — 清空哪些表、保留哪些表、Legacy DB affected: false
- **操作表单**：

**针对不同级别的特殊表单控件**：

1. `clear_runs_items_keep_sources` — 无额外参数，直接 **"Preview 影响"** 按钮
2. `clear_all_sources_and_content` — 无额外参数，直接 **"Preview 影响"** 按钮
3. `clear_pipeline_outputs_keep_items` — 无额外参数，直接 **"Preview 影响"** 按钮
4. `clear_outputs_keep_events` — 无额外参数，直接 **"Preview 影响"** 按钮
5. `clear_by_run_id` — 额外显示：
   - 下拉选择 `run_id`：列出所有 run（格式：`run_id · status · new_items_count`）
   - **"Preview 影响"** 按钮
6. `clear_by_source_id` — 额外显示：
   - 下拉选择 `source_ids`：列出所有 source（格式：`source_name · status`）
   - 复选框 `archive_sources`："commit 时同时 archive source"
   - **"Preview 影响"** 按钮
7. `create_new_fresh_db` — 无额外参数，直接 **"Preview 影响"** 按钮

### 预览面板

点击任意 **"Preview 影响"** 后，页面下方出现红色左边框面板：

- 标题："Reset Preview / 清空影响预览" + 风险标签
- 描述文字
- 4 个统计卡片：
  - Legacy DB affected（固定 false）
  - DB path
  - **确认文本**（大号代码字体，如 `RESET`、`RESET run_xxx`）— 用户需要在下方输入这个文本
  - 受影响的表数量
- 影响摘要 JSON（如果有）
- **高级详情折叠区**：完整的 preview JSON
- **确认表单**：
  - 隐藏字段：`operation_id`、`level`、`run_id`（如有）、`source_ids`（如有）、`archive_sources`（如有）
  - `confirmation`：文本输入，占位符为确认文本
  - **"Commit reset"** 提交按钮 → `POST /reset/commit`

**点击 Commit reset 后**：
- 后端验证确认文本是否匹配
- 不匹配 → 返回错误
- 匹配 → 执行清理，写审计日志，重定向回 `/reset`

---

## 待审核页（Review Queue）— `/review-queue`

### 页面标题区

- 小字标签："信息消费"
- 标题："Review Queue / 待审核"
- 说明：人工纠偏入口
- **状态过滤器**（右侧，`GET /review-queue`）：
  - 下拉选择 `status`：pending / resolved / dismissed
  - **"过滤"** 按钮 → 页面刷新，显示对应状态的 review

### Review 卡片列表

如果没有 review：空状态 "当前没有 {status} review。完成 real-write 并运行 events/review stage 后，这里会出现候选项。"

每条 review 显示为一张卡片：

- **标题**：`review_type`（如 `event_candidate`）+ 状态 chip
- **原因**：`reason` 字段（或 "需要人工确认。"）
- **目标**：`target_type:target_id`（代码字体）
- **操作按钮行**：
  - 如果目标是 `event` → **"查看 event"** 链接（次按钮样式）→ `/events/{target_id}`
  - 如果目标是 `cluster` → **"查看 cluster"** 链接（次按钮样式）→ `/clusters/{target_id}`
  - **"Resolve"**（主按钮）→ `POST /review-queue/{review_id}/resolve`，标记为 resolved，刷新页面
  - **"Dismiss"**（次按钮）→ `POST /review-queue/{review_id}/dismiss`，标记为 dismissed，刷新页面
- **折叠详情**：展开显示完整 review JSON

---

## 简报页（Briefings）— `/briefings`

### 页面标题区

- 标题："Briefing 简报"
- 说明文字
- **"生成 Daily Briefing"** 按钮 → `POST /briefings/daily/generate`，生成后刷新页面

### 简报列表

如果没有简报：空状态 "暂无 briefing。请先执行 real-write 或生成 event/review。"

每条简报显示为一张卡片：
- **标题**（加粗）
- **正文**：markdown 格式，等宽字体展示

---

## 报告页（Reports）— `/reports`

### 页面标题区

- 标题："Report 报告"
- 说明文字

### 生成表单

- `report_type`：下拉选择 — Summary / Source Health / Event
- **"生成 Report"** 按钮 → `POST /reports/generate`

### 报告列表

如果没有报告：空状态 "暂无 reports。"

每条报告显示为一张卡片：
- **标题**（加粗）
- **正文**：markdown 格式，等宽字体展示

---

## Agent 查询页 — `/agent-query`

### 页面标题区

- 小字标签："信息消费"
- 标题："Agent Query"
- 说明：输入问题，预览 agent 的 context pack

### 查询表单（`GET /agent-query`）

- `query`：文本输入，占位符 "今天 AI / agent 方向发生了什么？"
- `format`：下拉选择 — human / markdown / compact / json
- **"Preview context"** 按钮

### 查询结果

如果没有输入 query：空状态 "输入 query 后可以预览 context pack。这里不会执行外部 LLM，只是组装上下文。"

输入 query 并提交后：

左侧卡片 — **可复制上下文**：
- 根据选择的格式显示内容（等宽字体）：
  - `human` 格式：人类可读的列表
  - `markdown` 格式：Markdown 链接列表
  - `compact` 格式：紧凑格式
  - `json` 格式：JSON

右侧卡片 — **使用了哪些 items/events/sources**：
- 如果没有匹配：空状态
- 如果有：表格 — 标题（可点击 → `/items/{item_id}`）| 发布时间

**高级折叠区**：展开显示完整的 context pack JSON

---

## 高级调试页（统一模板 simple_list.html）

以下页面共享同一套交互模式：`/items`、`/dedupe-groups`、`/clusters`、`/events`、`/entities`、`/relations`、`/claims`、`/topics`、`/timeline`、`/evidence`、`/saved-views`

### 页面标题区

- 小字标签："高级调试"
- 标题：对应页面名称（如 "Clusters"、"Events"）
- 说明文字

### 对象列表

**Items 页面特殊**（`/items`）— 额外有搜索栏：
- `run_id`：文本输入
- `keyword`：文本输入
- **"筛选"** 按钮 → `GET /items`，页面刷新

如果没有数据：空状态 "暂无 {title} 数据。通常需要先完成 real-write 并运行对应 pipeline stage。"

每条对象显示为一张卡片：
- **标题**（加粗，可点击）：
  - 如果是 event → `/events/{event_id}`
  - 如果是 cluster → `/clusters/{cluster_id}`
  - 如果是 item → `/items/{item_id}`
  - 其他类型 → 纯文本
- **摘要**：event_summary / cluster_summary / topic_summary / reason / summary / "暂无摘要。"
- **标签行**：
  - 状态 chip（如有）
  - confidence chip（如有）
  - 对象 ID（代码字体）
- **折叠详情**（`<details>`）：展开显示完整 JSON

---

## 对象详情页（统一模板 object_detail.html）

用于：`/clusters/{cluster_id}`、`/events/{event_id}`

### 页面标题区

- 小字标签："详情"
- 标题：页面名称
- 说明文字

### Event 详情（如果是 event）

- **标题**（加粗）
- **摘要**文字
- 状态 chip + confidence chip + event_id（代码字体）
- **Supporting items 表格**（如有）：标题（可点击 → `/items/{item_id}`）| 发布时间
- 如果没有 supporting items：空状态

### Cluster 详情（如果是 cluster）

- **标题**（加粗）
- **摘要**文字
- 状态 chip + confidence chip + cluster_id（代码字体）
- **"promote cluster to event"** 按钮 → `POST /clusters/{cluster_id}/create-event`，将聚类提升为事件
- **Cluster items 表格**（如有）：标题（可点击 → `/items/{item_id}`）| 发布时间

### 原始 JSON 折叠区

页面底部，展开显示完整的 API 响应 JSON。

---

## Item 详情页 — `/items/{item_id}`

### 页面标题区

- 标题：item 标题（或 item_id）
- 副标题：item_id（代码字体）

### Canonical 区

左侧卡片，标题 "Canonical"。
- JSON 格式展示 item 的规范化数据
- 只读

### Semantic 区

右侧卡片，两个区块：
- **Semantic**：JSON 格式展示语义提取数据
- **Entities**：JSON 格式展示关联实体
- 均只读

---

## 设置页（Settings）— `/settings`

### 页面标题区

- 标题："Settings"
- 副标题："Console runtime settings."

### 设置信息

单张卡片，定义列表：
- `Backend API`：后端 API 地址（代码字体）
- `Frontend`：固定 "content_inbox_console"

纯信息展示，无可交互控件。

---

## 数据库切换器（全局组件，环境条内）

### 位置

每个页面顶部的环境信息条左侧。

### 外观

- 标签："数据库"
- 下拉选择框

### 选项内容

下拉菜单列出所有发现的 SQLite 数据库文件：

- **`content_inbox`**：`data/content_inbox.sqlite3`（主数据库）
- **`fresh_default`**：`data/environments/fresh_default/content_inbox.db`（默认 Fresh DB）
- 其他 `data/environments/<label>/content_inbox.db` 实例
- 不存在的文件后缀标注 `[缺失]`
- 当前使用的数据库默认选中

### 交互行为

1. 用户点击下拉菜单，选择一个不同的数据库
2. `onchange` 事件立即触发表单提交（无需点击按钮）
3. `POST /environment/switch`，携带 `database_path`
4. Console 转发 `POST /api/environment/switch` 到后端
5. 后端：
   - 验证路径、验证是有效 SQLite 文件
   - 创建新的数据库连接
   - 更新环境元数据
   - 写审计日志 `database_switched`
6. 浏览器重定向回切换前所在页面
7. 页面重新渲染，环境条更新为新数据库的统计信息

### 错误情况

- 如果数据库路径无效 → 重定向到 `/?error=INVALID_DATABASE: ...`
- 错误横幅出现在页面顶部

---

## 导航交互

### 主导航

- 点击任意导航链接 → 浏览器发出 GET 请求 → 页面完全刷新
- 当前高亮的链接即为所在页面
- 无 AJAX，无局部刷新

### 高级菜单

- 点击 "高级 ▼" → 展开折叠菜单，显示 10 个调试链接
- 再次点击 → 收起
- 纯 CSS 实现（`<details>` 元素），无 JavaScript

---

## 表单提交流程总结

所有表单提交遵循同一模式：

```text
用户填写表单 → 点击提交按钮
  → POST 到 console 路由
  → console 调用后端 API
  → 成功：302 重定向（回到来源页或结果页）
  → 失败：302 重定向（回到来源页，URL 带 ?error=错误消息）
  → 页面完全刷新
```

没有 AJAX、没有局部更新、没有客户端状态管理。每次操作都是一次完整的请求-响应-重定向-渲染循环。

---

## 视觉反馈

| 场景 | 视觉表现 |
|------|---------|
| 当前导航页 | 链接高亮（绿色） |
| 环境安全 | 环境条左侧绿色竖线 |
| 环境不安全（非 Fresh DB） | 环境条左侧红色竖线 |
| 警告信息 | 黄色/琥珀色左边框横幅 |
| 错误信息 | 红色左边框横幅 |
| 危险操作区 | 红色左边框卡片 |
| 空状态 | 虚线边框、半透明背景、居中文字 |
| 风险等级 high | 红色 chip 标签 |
| 风险等级 medium | 黄色 chip 标签 |
| 风险等级 critical | 深红色 chip 标签 |
| 风险等级 low | 默认色 chip 标签 |
| real-write ON | 绿色 pill 徽章 |
| real-write OFF | 黄色 pill 徽章 |
| 禁用按钮 | 灰色、不可点击 |
| 主按钮 | 实心绿色背景 |
| 次按钮 | 空心、绿色边框 |
| 数据卡片 | 白色圆角卡片、底部阴影、hover 阴影加深 |
