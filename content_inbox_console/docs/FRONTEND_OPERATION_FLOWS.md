# Frontend Operation Flows

## 主闭环

```text
确认环境安全
  -> 准备 / 导入 source
  -> 创建 dry-run
  -> 确认 dry-run 不写库
  -> 执行 real-write
  -> 查看 run 结果
  -> 执行 pipeline
  -> 处理 review queue
  -> 查看 event / briefing / report / agent query
  -> 按需清空某部分数据重新开始
```

## 环境安全

入口：`/environment`

用户可以查看：

- API base。
- DB identity / label / path / schema。
- `is_fresh_database`。
- `legacy_business_fallback=false`。
- Legacy DB path / exists / size / mtime / sha256。
- source/item/run counts。
- real-write gate 状态。
- 健康检查。

## Source 生命周期

入口：`/sources`

支持：

- 新增单个 source。
- check source，展示 parse 状态、duplicate、sample count。
- 批量粘贴导入 source。
- 导入 preview / commit。
- 搜索和状态过滤。
- source detail、编辑、archive、restore。
- 批量 enable / disable / archive / delete preview/commit。
- JSON / CSV / OPML export。
- 进入 Run Wizard。

archive/delete 是软归档，不物理删除历史 items。

## Run Wizard

入口：`/runs/new`

支持：

- 环境确认。
- selected sources / all active sources。
- published_from / published_to / timezone。
- max_sources、max_items_per_source、max_total_items。
- source_timeout_seconds、run_timeout_minutes。
- dry-run / real-write。
- run preview。
- start run 后进入 detail。

dry-run 不写 items。real-write 需要后端 `CONTENT_INBOX_ENABLE_REAL_RUNS=1`。

## Run Detail 与 Pipeline

入口：`/runs/{run_id}`

展示：

- run status、mode、source progress、events timeline。
- inserted / duplicate / failed。
- items from run。
- cancel、briefing、report、pipeline stage 按钮。

pipeline stage：

```text
dedupe -> semantic -> clusters -> events -> review -> briefing -> report
```

当前 semantic/clusters/events/review 是 lightweight v1，用于完成前端闭环；更完整的 LLM pipeline 仍可在后端继续演进。

## Review / Event / Briefing / Report / Agent Query

入口：

- `/events`
- `/review-queue`
- `/briefings`
- `/reports`
- `/agent-query`

Review Queue 支持 pending/resolved/dismissed 过滤，支持 resolve/dismiss。Event/Cluster detail 展示可读摘要、supporting items 和原始 JSON 折叠区。Agent Query 支持 human / markdown / compact / json context preview。
