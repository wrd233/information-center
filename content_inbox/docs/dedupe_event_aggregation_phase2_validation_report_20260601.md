# Phase 2 去重与事件聚合验证报告

Status: historical validation baseline. Use `event_aggregation_operational_v3.md` for current checkpoint policy and active targets.

生成日期: 2026-06-01

## 验证命令

```bash
cd content_inbox
PYTHONPATH=. pytest -q
PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
```

## 指标变化

Full regression: `271 passed, 11 skipped`.

| 指标 | Phase 1 | Phase 2 | 状态 |
|---|---:|---:|---|
| process dedupe precision | 100.0% | 100.0% | 保持 |
| process dedupe recall | 75.0% | 100.0% | 提升 |
| process dedupe F1 | 85.7% | 100.0% | 达标 |
| same-event precision | 100.0% | 100.0% | 保持 |
| same-event recall | 25.0% | 27.3% | 小幅提升，未达标 |
| same-event F1 | 40.0% | 42.9% | 小幅提升，未达标 |
| auto-merge precision | 100.0% | 100.0% | 达标 |
| digest/generic false event rate | 0.0% | 0.0% | 达标 |
| medium review rate | 未统计 | 100.0% | 达标 |
| alias hit count | 未统计 | 17 | 已可观测 |

## Candidate 诊断

- candidate counts by priority: `{'low': 7, 'medium': 1, 'high': 1, 'must_run': 1}`
- candidate counts by lane: `{'exploratory_recall': 4, 'same_thread': 3, 'same_event_recall': 2, 'exact_signature_alias': 1}`
- candidate counts by status: `{'review': 8, 'auto_merge': 2}`
- disqualifier counts: `{}`

## 结论

本轮达成 P1：URL canonicalization 让 process dedupe F1 从 85.7% 提升到 100.0%。P2/P3 有小幅收益：alias exact signature lane 提升了可解释召回，但 same-event recall 仍远低于 75% 门槛。

Precision 没有回退：same-event precision 与 auto-merge precision 仍为 100.0%，digest/generic false event rate 仍为 0.0%。这符合“先不误合并”的安全要求。

## 风险与缺口

- Same-event recall 仍不足，跨语言、标题大幅改写、same_event_new_info 仍需要结构化 LLM 或 review apply 补召回。
- 当前 alias registry 覆盖面还小，需要从 review case 扩充。
- Review apply 最小闭环尚未实现，medium/uncertain 仍主要是诊断与人工入口。
- Briefing/report 质量仍未达标。

## 数据安全

本轮未触碰 `content_inbox/data/**`，未执行默认大库真实写入。验证使用 pytest 临时库和 `scripts/evaluate_ops_quality.py` 的合成临时库。
