# Data Reset And Safety

数据清理入口：`/reset`

所有 reset 都是 preview-first + commit confirmation。后端会拒绝 `is_fresh_database=false` 的 reset。所有 preview/commit 都返回 `legacy_db_affected=false`，commit 写入 `audit_log`。

## Scope

| scope | 清空 | 保留 | 确认文本 |
|---|---|---|---|
| `clear_runs_items_keep_sources` | runs、run events、item links、items、dedupe、semantic、clusters/events、review、briefings/reports | sources、DB identity、system metadata、audit | `RESET` |
| `clear_all_sources_and_content` | sources 和所有 run/content/pipeline/output 对象 | schema、DB identity、system metadata、audit | `RESET` |
| `clear_pipeline_outputs_keep_items` | dedupe、semantic、clusters/events、entities/relations/claims/topics/timeline、review、briefings/reports | sources、runs、run events、item_run_links、inbox_items | `RESET` |
| `clear_outputs_keep_events` | briefings、reports、saved views | sources、runs、items、clusters/events、review | `RESET` |
| `clear_by_run_id` | 指定 run、run events、source progress、run links、该 run 独占 items 及其下游输出 | sources、其他 runs、共享 items | `RESET <run_id>` |
| `clear_by_source_id` | 指定 source 的 items、run links、下游输出，可选 archive source | 其他 sources/items、DB identity | `RESET <source_id>` 或 `RESET SOURCES` |
| `create_new_fresh_db` | 切换当前工作 DB | Legacy DB、旧 Fresh DB 文件 | `RESET` |

## Run-scoped 安全策略

`clear_by_run_id` 会分析 `item_run_links`：

- item 仅由该 run 引入：删除 item 和该 item 的 downstream outputs。
- item 被多个 run 关联：只删除该 run link，不删除 item。
- run events、run source progress、run row 会被删除。

## Source-scoped 安全策略

`clear_by_source_id` 会只选择目标 source 的 items 和 links。其他 source 的数据不应被删除。若 UI 勾选 archive，source 会被软归档。

当前 lightweight v1 对跨 source 混合 cluster/event 的策略是删除目标 source item 的 downstream 关系；若 cluster/event 仍有其他 source 的 item，会标记为 `stale` 而不是删除。未来可在后端 pipeline 中增加自动重算任务。

## 禁止事项

- 不允许前端直接修改 Legacy DB。
- 不允许前端绕过 real-write gate。
- 不允许没有 preview 的危险 commit。
- 不允许用 Legacy DB 作为业务 fallback。
- 不提交运行时 DB、缓存、临时输出。
