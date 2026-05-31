# 去重与事件聚合实施记录

生成日期: 2026-06-01

## 基线回答

1. 当前 item-level dedupe 已经基本可用：写入阶段通过 `build_dedupe_key()` 和 `InboxStore.get_by_dedupe_key()` 折叠 URL、source+GUID、source+title+date、source+title+content hash 等重复项，并维护 `seen_count`、`last_seen_at`、`latest_raw_json`、`latest_seen_summary`。离线评估仍显示 HTTP/HTTPS scheme 差异召回不足，处理时 duplicate pair F1 为 85.7%。
2. 当前后置 dedupe stage 解释能力弱，因为真实重复已在写入时折叠成单条 `inbox_items`，旧 stage 只按 dedupe key 重新分组现存 item，通常只能得到单成员 group，不能解释重复出现次数、raw/latest 变体和来源链路。
3. 当前 console pipeline 不能稳定代表真实事件聚合，因为 `generate_information_objects()` 旧实现以 `normalized_title(title)` 为聚合键，会漏掉标题改写的同事件，也会把 digest、market wrap、泛标题和低信号内容创建为 event。
4. 仓库已有 semantic signature / candidate / relation 能力在 `app.semantic.signatures`、`app.semantic.candidates`、`app.semantic.relations`、`app.semantic.clusters`。它们包含 actor/product/action/time signature、candidate priority、负特征和 relation policy，但此前没有接入 `/api/runs` operational pipeline。
5. 本轮优先改造 operational pipeline 的 dedupe explanation、eventness gate、signature 接入、candidate pair 记录、high-confidence relation materialization 和 event object 生成；暂不做完整 LLM relation 裁决、source 长期评分、attention-aware ranking、legacy cluster 全量迁移和 briefing/report 重写。

## 本轮改造

- `run_dedupe_stage()` 现在基于 `seen_count`、`raw_json`、`latest_raw_json`、`latest_seen_summary` 生成解释性 `dedupe_groups.evidence_json`，包含 dedupe key/method、canonical item、seen count、source count、URL/GUID/source variants、first/last seen。
- `generate_information_objects()` 改为 `operational_event_pipeline_v2`：先写 eventness 和 signature，再只让 concrete event signature 进入候选与 materialization。
- 非事件 gate 覆盖 digest/newsletter/roundup/market wrap、tutorial/opinion/case study、ad/spam、pure link/short low-signal。非 `event` item 进入 `eventness_review`，不自动创建 event。
- 新增 `event_candidate_pairs`，记录 run_id、item pair、candidate score、priority、lane、features、disqualifiers、status。
- 新增 `config/event_aliases.json`，并接入 `app.semantic.signatures`，支持 actor/product/action alias 的配置化扩展。
- relation decision 只对 `must_run` / `high` 且没有 hard disqualifier 的 same-event candidate 自动合并；`medium` / low-confidence same-topic 写 review；suppressed/non-event 不 materialize。
- 新 cluster/event 使用 `created_by=operational_v2_rule`、`schema_version=operational_v2`、signature/eventness/member evidence、cluster_items relation/confidence/evidence、event `primary_cluster_id` 和具体 summary。

## 保留与降级

- 保留 `normalize_content()`、`build_dedupe_key()`、写入时 dedupe、legacy cluster/event 表和已有 semantic 模块。
- 降级旧 lightweight title grouping：`generate_information_objects()` 不再以 normalized title 作为事件主键，也不再为每个 item 无条件创建 event。
- legacy 数据不被迁移、不覆盖；新写入通过 `created_by`、`schema_version`、`run_id` evidence 与旧数据区分。

## 不做事项

- 不做完整 LLM pair 裁决。
- 不做全量 historical DB rebuild 或真实大库写入。
- 不做 source 长期价值评分、阅读推荐排序、事件评论区 UI。
- 不重写 briefing/report，仅让 event 对象更可消费。

## 如何运行

```bash
cd content_inbox
PYTHONPATH=. pytest -q
PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
```

真实写入仍应只在 Fresh DB 或明确范围内执行。默认大库和 legacy cluster 不应被本轮逻辑直接迁移。
