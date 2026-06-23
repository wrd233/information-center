# RSS Source Manager Design v2

## 1. Context / v1 使用体验问题

v1 的 source check/fetch 能完成基础工作，但批量操作是同步返回，用户只能等最后结果；单行操作也缺少明确反馈。真实源数量增加后，抓取耗时、失败源诊断、慢源观察和下游 API 契约稳定性都需要更清楚的产品边界。

## 2. Goals / v2 目标

- 把 batch check/fetch 升级为持久化 `batch_run`。
- 让批量运行可轮询、可观测、可软取消。
- 保留源级并发模型，加入全局/adapter 并发限制和 timeout 配置。
- 让 check/fetch/batch item 响应包含轻量结构化字段。
- 改善前端行级 loading、黄色提示条、两段式全选和取消体验。
- 用后端/API 测试守住长期产品能力。
- 对真实非微信源做 API-first 验收，并输出报告到 `~/Downloads`。

## 3. Non-goals / 仍然不做什么

v2 不做登录、权限、token、scheduler、Celery、Redis Queue、WebSocket、SSE、报告管理页面、下载中心、复杂调参 UI、自动源治理、自动 disabled、自动修改 rating、自动导入新源、前端测试框架、Playwright/E2E、AI/LLM/briefing/review/event/semantic。

## 4. Batch Run Model

旧批量接口保留路径但改为异步语义：

```text
POST /api/v1/sources/check-batch
POST /api/v1/sources/fetch-batch
```

返回 `batch_run_id`、状态 URL、items URL 和建议轮询间隔。新增：

```text
GET  /api/v1/batch-runs/{batch_run_id}
GET  /api/v1/batch-runs/{batch_run_id}/items
POST /api/v1/batch-runs/{batch_run_id}/cancel
```

`batch_runs` 记录 action、状态、总数、pending/running/succeeded/failed/skipped/cancelled 计数、时间、耗时和 options。`batch_run_items` 在创建时写入固定 source 快照，并记录每个 source 的状态、耗时、HTTP 信息、错误类型、失败阶段和 entries 计数。

启动时发现历史遗留 `pending/running/cancelling` run，会做最小恢复：`cancelling` 变 `cancelled`，其他未完成 run 变 `failed`，未完成 item 标记 `process_restarted`。不做任务恢复系统。

## 5. UI Interaction Updates

- 单源 check/fetch 和 batch item running 时，表格行显示轻量 wave/shimmer。
- 对应按钮在运行时 disabled，并显示旋转图标。
- 黄色提示条在 batch 轮询时显示总数、运行中、成功、失败、跳过和耗时。
- batch running 时提供 Stop 按钮，调用软取消接口。
- 表头 checkbox 先选择当前页；当前页全选后显示“选择当前筛选结果中的全部 N 个源”；选择全部筛选后可清除选择。
- 执行批量检查、批量抓取、批量编辑前用确认框说明影响源数量。

## 6. Performance Optimization Plan

产品保留源级并发，不引入全 async 重写。配置包含：

```yaml
timeouts:
  default:
    connect_seconds: 3
    read_seconds: 8
    total_seconds: 12
  rsshub:
    connect_seconds: 3
    read_seconds: 10
    total_seconds: 15
  native:
    connect_seconds: 3
    read_seconds: 8
    total_seconds: 12
  wechat:
    connect_seconds: 3
    read_seconds: 15
    total_seconds: 20

concurrency:
  default_max_concurrent_sources: 7
  hard_limit: 20
  adapters:
    rsshub: 7
    native: 7
    wechat: 2
```

真实源验收阶段按 7/10/14/20 做临时并发矩阵。只有在总耗时明显下降、失败/timeout 不明显增加、RSSHub/SQLite/UI 没有异常时，才把保守最优值写回配置。

## 7. API Contract Enhancements

单源 check/fetch 返回轻量 envelope：

```text
ok, source, timing, counts, result, error
```

失败时 `error` 至少包含：

```text
error_type, message, http_status, retryable, failure_stage
```

支持的错误类型包括 timeout、DNS/连接、HTTP、parse、RSSHub route、empty_feed、source_busy、process_restarted 和 unknown_error。支持的 failure_stage 包括 resolve_url、connect、read、http_status、parse_feed、parse_entry、persist、unknown。

为了兼容 v1 调用方，check 仍保留 `feed_url/status/entry_count/checked_at` 顶层字段，fetch 仍保留 `fetch_run` 顶层字段。

## 8. Product Tests

长期保留的测试位于 `tests/test_core.py`，覆盖：

- ensure_schema 不清空旧数据。
- check 不触发 broken，fetch 按原规则触发 broken/recover。
- entries/fetch_runs/fetch_run_entries 原有语义。
- import/export/rating 原有语义。
- batch_run source_ids 快照和异步 API。
- filter 快照和 progress 统计。
- soft cancel 将 pending items 标记 cancelled。
- timeout config adapter override。
- error envelope 和 source_busy。

## 9. Real Source Acceptance Test

真实源验收只测试当前 Source Manager 主库中 `source_type != wechat` 的已有源，不自动导入 `rss_opml` 新源，不自动 disabled 失败源，不自动修改 rating/category/tags/notes，不 reset/清库/换库，不持久化 raw。

验收以 API 为主：调用 Source Manager API，记录响应时间、batch_run 进度、字段完整度、entries 可用性。SQLite 只做只读辅助核对 entries/fetch_runs/batch_run_items 和 raw 未持久化。

真实 fetch 允许写入正常 entries、fetch_runs、fetch_run_entries，并按 v1 规则更新 source 健康字段。报告必须明确说明这一点。

## 10. Manual Frontend Acceptance Checklist

```text
打开 UI
单源 fetch 时，当前行出现 wave/shimmer 动画
单源 check 时，当前行出现 loading 状态
batch fetch 后，黄色提示条每 1 秒更新统计
batch check 后，黄色提示条每 1 秒更新统计
batch 运行时可以点击取消
取消后不再启动新的源，pending items 变 cancelled
表头 checkbox 先选择当前页
提示可选择当前筛选结果中的全部源
点击后选中全部筛选结果源
批量操作前显示将影响的源数量
失败源在列表中能看见失败状态或错误入口
settings/health 能看到 db_path/config/app started_at/version 信息
```

当前状态：planned。已通过 frontend build/typecheck，但未进行人工浏览器验收。

## 11. Validation Matrix

| 能力 | 验收方式 | 状态 | 备注 |
|---|---|---|---|
| batch_run schema | pytest + ensure_schema | done | 新增 batch_runs / batch_run_items |
| source_ids 快照 | pytest | done | 创建时写入 batch_run_items |
| filter 快照 | pytest | done | 后端创建时解析 |
| check-batch/fetch-batch 异步语义 | pytest/TestClient | done | 立即返回 batch_run_id |
| batch status/items API | pytest/TestClient | done | 支持轮询 |
| soft cancel | pytest/TestClient | done | pending items cancelled |
| 单源 source_busy | pytest | done | check/fetch 共享 source lock |
| timeout adapter override | pytest | done | config.yaml + AppConfig |
| 错误 envelope | pytest | done | check/fetch 结构化 |
| 原有 fetch/check/import/export/rating 语义 | pytest | done | 兼容测试保留 |
| 前端 build/typecheck | npm build | done | 无前端自动测试 |
| 前端手动验收 | 人工打开 UI | planned | 尚未人工点击确认 |
| 真实源 API 验收 | 临时脚本/API | done | 143 个非微信源，均为 native |
| 并发矩阵 7/10/14/20 | 临时脚本/API | done | 保守最优选择 10 |
| Downloads 报告 | 文件检查 | done | Markdown + 4 个 CSV 已输出 |
| 登录/权限/scheduler/WebSocket | 代码检查 | intentionally_not_done | v2 non-goals |
| 报告管理 UI/下载中心 | 代码检查 | intentionally_not_done | v2 non-goals |

## 12. Decision Log

- V2-D001: batch check/fetch 直接替换为持久化 batch_run 异步语义。
- V2-D002: 使用 SQLite + ensure_schema，不引入 Alembic。
- V2-D003: batch_run 创建时固定 source 快照。
- V2-D004: 软取消不强杀 running 请求，只阻止新 source work 并取消 pending item。
- V2-D005: 保留源级并发，加入全局和 adapter 并发限制。
- V2-D006: timeout 使用 config.yaml，不进 UI。
- V2-D007: check/fetch 响应做轻量 envelope，同时保留 v1 顶层兼容字段。
- V2-D008: 前端只做轻量提示条和行级反馈，不做任务面板。
- V2-D009: 真实源验收临时代码不得提交项目，报告输出到 `~/Downloads`。
