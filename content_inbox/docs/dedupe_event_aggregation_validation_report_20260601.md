# 去重与事件聚合验证报告

生成日期: 2026-06-01

## 验证命令

```bash
cd content_inbox
PYTHONPATH=. pytest -q
PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
```

## 结果

- Unit/API regression: `266 passed, 11 skipped`
- Offline dry-run diagnostic: completed, report refreshed at `docs/ops_quality_eval_20260531.md`
- Diagnostic does not read real runtime data; it uses a temporary SQLite database and synthetic fixtures.

## 当前指标

来自 `scripts/evaluate_ops_quality.py`:

| 指标 | 当前值 | 门槛 | 状态 |
|---|---:|---:|---|
| process dedupe pair F1 | 85.7% | 95% | 未达标 |
| same-event pair F1 | 40.0% | 80% | 未达标 |
| same-event recall | 25.0% | 75% | 未达标 |
| event_type known rate | 100.0% | 70% | 达标 |
| event summary specific rate | 100.0% | 80% | 达标 |
| entity recall | 97.1% | 70% | 达标 |
| digest/generic false event behavior | synthetic non-event candidate rate 0.0% | <= 2% | 达标 |

## 质量解释

本轮改造优先高精度，当前 dry-run 结果显示 false positive pair 降为 0，非事件不再自动建 event，event_type 和 summary 不再是模板/unknown。代价是 recall 明显下降：只有 concrete signature 能自动 materialize，标题改写、别名不足、跨语言和 medium candidate 仍大量进入 review 或被拒绝。

## 覆盖确认

- Dedupe explanation: `seen_count > 1` item 会生成包含 key/method/seen/source/variant 的 evidence payload。
- Eventness: digest/generic/low-signal fixture 不创建 event，并写 `eventness_review`。
- Signature: concrete event item 会写入 `semantic_extractions.normalized_output_json.signature`。
- Candidate: pair evidence 写入 `event_candidate_pairs`，包含 priority、lane、features、disqualifiers。
- Relation/cluster/event: high-confidence same-event 才自动 materialize；`cluster_items` 带 relation/confidence/evidence；`events` 带 `primary_cluster_id` 和 evidence。

## 风险与缺口

- Candidate/relation recall 仍不足，same-event pair F1 未达标。
- HTTP/HTTPS scheme dedupe 仍未补齐，process dedupe F1 未达标。
- LLM relation path 尚未接入，medium/uncertain 只进入 review，不自动判定。
- Run report/briefing 仍是旧模板，质量分未达标。
- Alias registry 已有 `config/event_aliases.json` 起步，但覆盖面还很小，需要按真实 review case 扩充。

## 写入与回滚

新写入使用 `created_by=operational_v2_rule`、`schema_version=operational_v2`、`run_id` evidence 和 `input_fingerprint`。Fresh DB 可直接重跑；真实库中可按 run_id、created_by、schema_version 定位本轮影响。默认大库未迁移，未执行真实大库写入。

下一轮建议先提升 signature alias/config 和 candidate high recall，再为 medium/high-uncertain 接入结构化 LLM relation decision。
