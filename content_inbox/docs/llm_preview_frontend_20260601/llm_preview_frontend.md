# LLM Preview Frontend Environment — 验收文档

**日期:** 2026-06-01
**轮次:** LLM Preview Environment + Frontend Review Experience
**状态:** READY

---

## 1. 本轮目标

建立一个安全、可重复、可前端查看的 **LLM Preview 环境**，让用户能够在前端看到 live DeepSeek 参与后的成果，包括 LLM proposals、review queue、event clusters、briefing/report preview，并判断这些结果是否真正有用。

## 2. Preview 环境设计

```text
真实 DB (只读) → build_llm_preview_env.py → preview DB
                                              ├── 复制采样数据
                                              ├── 运行 v3 流水线
                                              ├── LLM proposal-only (可选)
                                              ├── 生成 manifest + report
                                              └── review queue 可查看
                                                  
Backend → CONTENT_INBOX_DB_PATH=preview DB → 只读真实 DB，只写 preview DB
Console → CONTENT_INBOX_FRONTEND_API_BASE=backend → 代理 API 调用
```

## 3. 为什么不直接写真实 DB

- Preview 环境是完全隔离的 — 所有 LLM proposal、关系判定、聚类操作都只发生在 `preview_db_only` 模式下。
- 真实 DB 在任何情况下都不会被写入（通过文件完整性校验 + 写入路径控制双重保障）。
- Auto-merge 在任何时候都是禁用的（`auto_merge_enabled: false`）。
- 只有通过 scoped real-write rehearsal 验证通过后，才会考虑对真实 DB 进行受控写入。

## 4. 使用的数据范围

- **真实 DB:** `data/content_inbox.sqlite3`（约 3278 条 item，469 个 source）
- **采样模式:** `event_hotspots`（优先选取多来源覆盖的热点事件）
- **采样限制:** 40 条（可通过 `--limit` 调整到 100）
- **采样时间:** 基于 `published_at` 倒排 + event hotspot key 分组

## 5. DeepSeek Live API 使用情况

| 指标 | 状态 |
|---|---|
| Provider | deepseek-v4-flash |
| 是否使用 | 可选（通过 CONTENT_INBOX_LLM_ENABLE_LIVE=1 控制） |
| 调用模式 | proposal-only（不自动合并） |
| 最大调用数 | 20（可配置） |
| 模式 | candidate_discovery, signature_repair, relation_judge, cluster_proposal |
| Schema 校验 | 启用（所有 LLM 输出都通过 Pydantic schema 验证） |

> **注意:** 本轮未实际运行 live DeepSeek 调用，原因是需要有效的 API key 配置。LLM live 路径已在代码中完整实现并通过 mock 测试，在 API key 可用时只需设置 `CONTENT_INBOX_LLM_ENABLE_LIVE=1` 即可运行。

## 6. LLM Calls 统计

通过 mock LLM 测试验证的统计结构：

| 指标 | 预期值 |
|---|---|
| Calls attempted | 0-20 |
| Calls succeeded | 取决于 API 可用性 |
| Calls failed | 取决于 API 可用性 |
| Schema valid | 等于 succeeded |
| Schema invalid | 0 |
| Proposals generated | 取决于内容质量 |

## 7. Preview DB 路径

```
content_inbox/data/environments/llm_preview/content_inbox.db
```

## 8. Preview Manifest 路径

```
content_inbox/data/environments/llm_preview/preview_manifest.json
```

Manifest 包含字段：source_db, preview_db, created_at, sample_mode, limit, sampled_items, real_db_item_count, real_db_source_count, llm_enabled, llm_provider, max_llm_calls, llm_calls_succeeded, llm_calls_failed, llm_calls_schema_invalid, llm_modes_run, llm_proposals, review_queue_pending, event_count, cluster_count, total_llm_calls, write_mode, auto_merge_enabled, sample_item_ids, warnings.

## 9. Backend 启动命令

### 构建 Preview DB

```bash
cd content_inbox

# 基础构建（不含 LLM）
PYTHONPATH=. python3 scripts/build_llm_preview_env.py \
  --source-db data/content_inbox.sqlite3 \
  --preview-db data/environments/llm_preview/content_inbox.db \
  --reset-preview \
  --limit 40 \
  --sample-mode event_hotspots

# 含 Live LLM 构建
CONTENT_INBOX_LLM_ENABLE_LIVE=1 \
CONTENT_INBOX_LLM_PROVIDER=deepseek \
PYTHONPATH=. python3 scripts/build_llm_preview_env.py \
  --source-db data/content_inbox.sqlite3 \
  --preview-db data/environments/llm_preview/content_inbox.db \
  --reset-preview \
  --limit 40 \
  --sample-mode event_hotspots \
  --enable-live-llm \
  --max-llm-calls 20
```

### 启动 Backend 指向 Preview DB

```bash
cd content_inbox
CONTENT_INBOX_DB_PATH=data/environments/llm_preview/content_inbox.db \
CONTENT_INBOX_ENABLE_REAL_RUNS=0 \
PYTHONPATH=. python3 -m app.server
```

Backend 启动后会在 `http://127.0.0.1:8787` 监听，访问 `/health` 可确认 DB path。

## 10. Frontend 启动命令

```bash
cd content_inbox_console
CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \
uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload
```

## 11. 前端应该看哪些页面

| 页面 | URL | 要看什么 |
|---|---|---|
| 环境页 | http://127.0.0.1:8788/environment | 确认显示 "🧪 LLM Preview"，DB path 指向 preview DB |
| 作战首页 | http://127.0.0.1:8788/dashboard | 顶部显示 LLM Preview 标识，侧边栏有 Preview 验收链接 |
| 待审核 | http://127.0.0.1:8788/review-queue | LLM proposal 类型标签、关系标签、置信度、证据折叠、风险标记 |
| 事件 | http://127.0.0.1:8788/events | 事件列表及关联条目 |
| 聚合线索 | http://127.0.0.1:8788/clusters | 聚合线索列表及来源 |
| 简报 | http://127.0.0.1:8788/briefings | 简报内容及预览环境提示 |
| 报告 | http://127.0.0.1:8788/reports | 报告内容及预览环境提示 |
| Preview 验收 | http://127.0.0.1:8788/preview-checklist | 验收清单：环境信息、LLM 状态、流水线统计、10 项检查 |

## 12. 如何确认没有被旧数据污染

1. 检查环境页面的 DB path 是否指向 `llm_preview` 目录。
2. 侧边栏和顶部显示 "🧪 LLM Preview" 标识。
3. 页面顶部不显示信息源数量和条目数量与真实库匹配（preview 库采样数据较少）。
4. 真实 DB 文件 (`data/content_inbox.sqlite3`) 的修改时间未变。
5. Preview 验收清单页面的 "来源 DB" 和 "Preview DB" 路径不同。

## 13. 如何确认连接的是 Preview DB

- **Backend:** `/health` 端点返回的 `database_path` 指向 `data/environments/llm_preview/content_inbox.db`。
- **Frontend:** 所有页面顶部显示 "🧪 LLM Preview" 标签。
- **API:** `GET /api/environment` 返回 `preview_manifest` 字段。

## 14. 当前前端能展示哪些 LLM 成果

| LLM 成果 | 展示位置 | 展示能力 |
|---|---|---|
| 候选发现 (candidate_discovery) | Review Queue | ✅ 类型标签、confidence、evidence、risk_flags |
| 签名修复 (signature_repair) | Review Queue | ✅ 类型标签、confidence、evidence、risk_flags |
| 关系判定 (relation_judge) | Review Queue | ✅ 类型标签、关系标签 (same_event/update/related/…)、confidence、evidence |
| 聚合建议 (cluster_proposal) | Review Queue | ✅ 类型标签 |
| Event Clusters | Clusters 页 | ✅ 聚合线索列表、关联条目 |
| Events | Events 页 | ✅ 事件列表、confidence、关联条目 |
| Briefing | Briefings 页 | ✅ 简报内容、preview 环境提示 |
| Report | Reports 页 | ✅ 报告内容、preview 环境提示 |
| LLM 调用日志 | API only | ✅ GET /api/semantic/llm-call-logs |
| Preview Manifest | Environment 页 + Checklist 页 | ✅ 完整展示 |

### 新增前端展示能力

1. **环境标识:** 顶部和侧边栏显示 "🧪 LLM Preview"，环境页显示详细 preview 信息。
2. **Review Queue 改进:**
   - LLM proposal 类型标签（候选发现/签名修复/关系判定/聚合建议）
   - 关系标签（同一事件/更新/背景/关联/不同事件/不确定）
   - 置信度展示（高/中/低 + 百分比）
   - 风险标记（risk_flags 红色标签）
   - 证据折叠区（展开查看 evidence 列表）
   - 来源筛选（LLM 生成 / 规则生成）
3. **筛选功能:** 
   - 按状态筛选（待处理/已处理/已忽略）
   - 按来源筛选（LLM / 规则）
4. **Preview 验收清单:** 独立页面，包含 10 项检查 + 环境信息 + LLM 状态 + 决策指引
5. **Briefing/Report:** 页面顶部显示来自 LLM Preview 环境的提示。
6. **Events/Clusters:** 页面顶部显示事件/聚合线索数量统计。

## 15. 仍然展示不了哪些信息

- **LLM 调用实时监控:** 当前 LLM 调用是通过 `llm_call_logs` 表记录的，前端只能通过 API 查询，没有实时 websocket 推送。
- **Event 详情中的 LLM evidence:** `GET /api/events/{event_id}` 返回的 event 数据中 `evidence_json` 字段已经存在，但前端 object_detail 页面未完整渲染 evidence 内容（仅在 debug panel 中可见）。
- **Cluster 卡片的 LLM 生成内容:** cluster_cards 表中有 LLM 生成的事件标题、核心事实等，但前端 simple_list/object_detail 模板中可能未完全展示。
- **Item 级别的 LLM 卡片:** item_cards 表中的 canonical_title、short_summary 等 LLM 生成内容未在前端 items 页面单独展示。

## 16. 测试命令与结果

```bash
cd content_inbox

# 全部测试
PYTHONPATH=. pytest -q
# 结果: 319 passed, 11 skipped

# 新增 LLM Preview 测试
PYTHONPATH=. pytest tests/test_llm_preview_env.py -q
# 结果: 16 passed

# 质量评估
PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
# 结果: 全部阈值通过 (8/8)

# 验证 build 脚本可导入
PYTHONPATH=. python3 -c "import scripts.build_llm_preview_env; print('OK')"
# 结果: OK

# 验证 ops_api 可导入
PYTHONPATH=. python3 -c "from app.ops_api import router; print('OK')"
# 结果: OK

# 验证 console 可导入
cd content_inbox_console && PYTHONPATH=. python3 -c "from app.routes.ops import router; print('OK')"
# 结果: OK
```

## 17. 是否建议进入 scoped real-write rehearsal

**当前状态: 暂不推荐**

原因:
1. 本轮未实际运行 live DeepSeek（API key 未配置），无法评估 LLM proposal 质量。
2. 需要先用真实 API 运行一次 live LLM preview（`CONTENT_INBOX_LLM_ENABLE_LIVE=1`），通过前端验收清单验证所有 10 项通过后，再考虑进入 rehearsal。
3. 建议流程：运行 live LLM → 验收清单全部通过 → scoped real-write rehearsal（仅 1-2 个 source）。

## 18. 剩余风险

1. **LLM 质量未验证:** 未用真实 API 运行，无法确认 LLM proposal 的准确性和实用性。
2. **前端单页渲染性能:** 当前前端使用 Jinja2 服务端渲染，大量数据时可能较慢（但当前采样 40 条不存在此问题）。
3. **embedding 未启用:** 聚类基于规则/LLM，未使用向量相似度（已在设计中预留 sqlite_vec）。
4. **briefing/report 内容有限:** 当前 briefing 模板较简单，基于事件标题拼接，未使用 LLM 润色。
5. **前端交互有限:** 当前没有实时刷新、批量操作、拖拽排序等高级交互。

## 19. 下一步建议

1. **配置 DeepSeek API key 并运行 live LLM preview**（设置 CONTENT_INBOX_LLM_ENABLE_LIVE=1，运行 build_llm_preview_env.py --enable-live-llm --max-llm-calls 20）。
2. **使用前端验收清单评估 LLM 成果**（打开 /preview-checklist 逐项检查）。
3. **如果质量达标:** 进入 Task 下一步 — scoped real-write rehearsal（选择 1-2 个 source，小范围写入验证）。
4. **如果质量不达标:** 调优 prompts、调整 score_policy、增加样本量后重新运行。
5. **后续可改进:** event 详情页展示 LLM evidence、cluster 卡片展示 LLM 生成内容、增加 LLM 调用实时监控面板。

---

**文件路径:** `content_inbox/docs/llm_preview_frontend_20260601.md`
**生成时间:** 2026-06-01
