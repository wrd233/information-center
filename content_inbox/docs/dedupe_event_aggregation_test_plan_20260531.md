# 去重与事件聚合测试方案报告

生成日期: 2026-05-31

## 目的

本测试方案用于持续评估 `content_inbox` 的 item 去重、事件聚合、事件对象生成和下游简报/报告质量。它既服务当前诊断，也服务后续改造的回归验证。

测试目标：

1. 发现 item 去重漏判和误判。
2. 发现事件聚合漏合并和误合并。
3. 验证 eventness gate 是否阻止非事件内容进入 event。
4. 验证 signature/candidate/relation pipeline 是否可解释。
5. 验证 event object 是否足以支撑 briefing/report。
6. 验证大库迁移或 rebuild 不破坏旧数据。

## 测试分层

```text
unit tests
  -> deterministic fixture tests
  -> synthetic benchmark
  -> large DB readonly diagnostics
  -> dry-run rebuild evaluation
  -> small real-write canary
  -> manual review audit
```

每一层回答不同问题。

| 层级 | 目的 | 是否写库 | 是否需要 LLM/API |
|---|---|---:|---:|
| Unit | 函数行为正确 | 否 | 否 |
| Fixture | 固定样例回归 | 临时库 | 否 |
| Synthetic benchmark | 聚合质量指标 | 临时库 | 否 |
| Large DB readonly | 真实分布诊断 | 否 | 否 |
| Dry-run rebuild | 迁移前评估 | 否 | 可选 |
| Canary write | 小范围真实写入验证 | Fresh DB | 可选 |
| Manual audit | 人类质量确认 | 可选 | 可选 |

## 指标体系

### Item 去重指标

| 指标 | 定义 | 合格线 |
|---|---|---:|
| duplicate pair precision | 预测重复 pair 中真实重复比例 | >= 0.98 |
| duplicate pair recall | 真实重复 pair 被识别比例 | >= 0.95 |
| duplicate pair F1 | precision/recall 综合 | >= 0.96 |
| URL canonicalization recall | tracking/fragment/scheme 归一化命中 | >= 0.98 |
| GUID recall | 同 source GUID 命中 | >= 0.99 |
| title-date precision | 同源同日同标题命中准确率 | >= 0.95 |
| dedupe explanation coverage | seen_count>1 item 有解释比例 | >= 0.90 |

### Eventness 指标

| 指标 | 定义 | 合格线 |
|---|---|---:|
| eventness precision | 自动判为 event 的真实事件比例 | >= 0.90 |
| eventness recall | 真实事件被识别比例 | >= 0.75 |
| non-event rejection precision | digest/thread/content/low-signal 判断准确率 | >= 0.90 |
| digest false event rate | digest/roundup 被建 event 比率 | <= 0.02 |
| low-signal false event rate | 短标题/纯链接/emoji 被建 event 比率 | <= 0.01 |

### Event signature 指标

| 指标 | 定义 | 合格线 |
|---|---|---:|
| actor extraction accuracy | 主体抽取准确率 | >= 0.85 |
| product extraction accuracy | 产品/对象抽取准确率 | >= 0.80 |
| action accuracy | 动作分类准确率 | >= 0.80 |
| signature exact precision | exact signature 预测同事件准确率 | >= 0.98 |
| signature exact recall | exact signature 覆盖真实同事件 pair | >= 0.45 初期，>= 0.70 长期 |
| alias normalization hit rate | 已配置 alias 命中率 | >= 0.95 |

### Candidate 和 relation 指标

| 指标 | 定义 | 合格线 |
|---|---|---:|
| candidate high precision | high 自动候选真实同事件比例 | >= 0.95 |
| candidate high recall | high 覆盖真实同事件比例 | >= 0.60 初期 |
| candidate medium precision | medium 真实有价值比例 | >= 0.40 |
| auto-merge precision | 自动合并准确率 | >= 0.95 |
| auto-merge recall | 自动合并覆盖率 | >= 0.50 初期 |
| same-event pair F1 | 同事件 pair 总体 F1 | >= 0.80 |
| same-topic false merge rate | 同主题不同事件误合并率 | <= 0.03 |
| generic title false merge rate | 泛标题误合并率 | <= 0.02 |

### Cluster 和 event object 指标

| 指标 | 定义 | 合格线 |
|---|---|---:|
| cluster evidence coverage | cluster item 都有 evidence | >= 0.95 |
| cluster item_count consistency | item_count 与 cluster_items 一致 | >= 0.99 |
| event_type known rate | 非 unknown event_type 比例 | >= 0.80 |
| event summary specific rate | 摘要非模板且含主体动作对象 | >= 0.85 |
| event confidence calibrated | 高置信错误率低 | 人工抽样通过 |
| review payload completeness | review 有足够证据 | >= 0.90 |

### Briefing/report 指标

| 指标 | 定义 | 合格线 |
|---|---|---:|
| briefing event coverage | 高价值事件进入简报比例 | >= 0.80 |
| briefing noise rate | 非事件/低质内容进入简报比例 | <= 0.05 |
| report structure score | 标题/分区/统计/证据完整性 | >= 0.85 |
| report actionability | 是否能指导人工审核和后续操作 | 人工抽样通过 |

## 测试数据集

### Synthetic benchmark

当前脚本：`scripts/evaluate_ops_quality.py`

覆盖样例：

- URL tracking 参数
- URL fragment
- HTTP/HTTPS scheme 差异
- GUID 重复
- 同源同标题同日期
- 跨来源同事件标题改写
- 中英文同事件
- 泛标题不同事件
- digest/roundup/market wrap 非事件
- 同主题不同事件
- background noise

当前规模：86 条合成 item。

建议扩展到 200+ 条，按类别分层：

| 类别 | 建议数量 |
|---|---:|
| URL/GUID/title-date duplicate | 30 |
| Same event multi-source | 40 |
| Same event cross-language | 20 |
| Same topic different event | 30 |
| Same product different stage | 25 |
| Digest/roundup/market wrap | 20 |
| Low-signal social fragments | 20 |
| Spam/adult/ad content | 20 |
| Policy/funding/security/benchmark specialized | 30 |

### Large DB readonly

默认库：`data/content_inbox.sqlite3`

用途：

- 真实 source/item 分布
- seen_count 分布
- legacy cluster 结构债
- signature coverage
- title group 噪音
- event_type 覆盖

只读扫描，不修改库。

### Manual gold set

建议新增人工标注文件：

```text
content_inbox/tests/fixtures/event_aggregation_gold.jsonl
```

每行格式：

```json
{
  "case_id": "openai_gpt55_001",
  "items": [
    {
      "item_id": "item_a",
      "title": "...",
      "url": "...",
      "source_name": "...",
      "published_at": "..."
    }
  ],
  "gold_event_id": "event_openai_gpt55_release",
  "eventness": "event",
  "event_type": "release",
  "actor": "OpenAI",
  "product": "GPT-5.5",
  "action": "release",
  "should_auto_merge": true,
  "notes": ""
}
```

Relation gold:

```json
{
  "item_a_id": "item_a",
  "item_b_id": "item_b",
  "relation": "same_event_new_info",
  "same_event": true,
  "same_topic": true,
  "should_auto_merge": true,
  "new_facts": ["..."],
  "disqualifiers": []
}
```

## 测试脚本

### Existing scripts

`scripts/evaluate_ops_quality.py`

用途：

- 临时库合成 benchmark
- 评估处理时去重
- 评估 lightweight event 聚合
- 评估 event object 和 output 质量

命令：

```bash
cd content_inbox
PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
```

输出：

- `docs/ops_quality_eval_20260531.md`

`scripts/diagnose_event_aggregation.py`

用途：

- 对照 lightweight、signature exact、candidate high、candidate medium
- 读取默认大库做只读结构统计
- 生成根因报告

命令：

```bash
cd content_inbox
PYTHONPATH=. python3 scripts/diagnose_event_aggregation.py
```

输出：

- `docs/event_aggregation_deep_diagnostic_20260531.md`

### Proposed scripts

建议新增：

```text
scripts/evaluate_dedupe_explanation.py
scripts/evaluate_eventness.py
scripts/evaluate_event_signature.py
scripts/evaluate_relation_decisions.py
scripts/evaluate_rebuild_dry_run.py
```

每个脚本都应支持：

- `--fixture`
- `--db`
- `--limit`
- `--json`
- `--report`
- `--fail-on-threshold`

示例：

```bash
PYTHONPATH=. python3 scripts/evaluate_event_signature.py \
  --fixture tests/fixtures/event_aggregation_gold.jsonl \
  --report docs/evaluation/event_signature_eval.md \
  --fail-on-threshold
```

## Unit 测试清单

### Dedupe

测试文件建议：

```text
tests/test_event_dedupe_explanation.py
```

用例：

- URL tracking 参数去重。
- URL fragment 去重。
- HTTP/HTTPS 可配置归一化。
- 同 source GUID 去重。
- 不同 source 相同 GUID 不误合并。
- 同源同标题同日去重。
- 同标题不同日期不去重。
- 无 URL/GUID 的 content hash 去重。
- `seen_count` 更新。
- `latest_raw_json` 更新。
- dedupe explanation 生成。

### Eventness

测试文件建议：

```text
tests/test_eventness_classifier.py
```

用例：

- 产品发布判为 event。
- 融资判为 event。
- 政策发布判为 event。
- 安全事件判为 event。
- 日报/周报判为 digest。
- market wrap 判为 digest/thread。
- 教程判为 content。
- 观点分析判为 content/thread。
- 纯链接/emoji 判为 low_signal。
- 广告/成人/垃圾内容判为 ad/low_signal。

### Signature

测试文件建议：

```text
tests/test_event_signature.py
```

用例：

- OpenAI GPT-5.5 别名归一。
- DeepSeek/深度求索别名归一。
- EU/European Commission 归一。
- 发布/上线/rollout 归一到 release/availability。
- funding/financing/raises 归一。
- actor/product/action/time bucket 构造 signature。
- 无 actor/product 的 thread 不生成 event signature。

### Candidate

测试文件建议：

```text
tests/test_event_candidates.py
```

用例：

- exact signature 进入 must_run。
- actor+product+action+time close 进入 high。
- 同主题不同事件进入 medium/review。
- generic-only overlap suppress。
- wide time window suppress。
- digest title suppress。
- same source boilerplate suppress。

### Relation

测试文件建议：

```text
tests/test_event_relation_decisions.py
```

用例：

- same URL -> item_duplicate。
- same event repeat -> same_event_repeat。
- same event new facts -> same_event_new_info。
- same event new angle -> same_event_new_angle。
- same topic different event -> same_topic_different_event。
- same product different stage -> same_product_different_event。
- uncertain -> review。

### Materialization

测试文件建议：

```text
tests/test_event_cluster_materialization.py
```

用例：

- high same_event 自动 attach。
- new event 创建 cluster。
- non-event 不创建 event。
- medium 写 review。
- cluster_items 有 evidence。
- event item_count 一致。
- event summary 具体。
- event_type 非 unknown。

## Integration 测试

### 临时库合成 run

流程：

1. 创建临时 SQLite。
2. 插入 synthetic sources/items。
3. 跑 dedupe。
4. 跑 eventness。
5. 跑 signature。
6. 跑 candidate。
7. 跑 relation。
8. materialize cluster/event。
9. 评估指标。

验收：

- 无 schema error。
- 无非事件自动建 event。
- auto-merge precision 达标。
- review_queue 数量合理。

### 默认大库只读扫描

流程：

1. 读取 `data/content_inbox.sqlite3`。
2. 统计表数量。
3. 统计 cluster integrity。
4. 跑 signature scan。
5. 输出报告。

验收：

- 不写数据库。
- 能输出 `clusters_without_cluster_items`。
- 能输出 signature coverage。
- 能输出 title group 噪音样例。

### Dry-run rebuild

流程：

1. 对默认库只读读取 item。
2. 使用新 pipeline dry-run 生成 would-be clusters。
3. 不写入。
4. 与 legacy/lightweight 对比。

输出：

- would_create_clusters
- would_attach_items
- would_review_items
- would_reject_non_events
- estimated precision via gold subset

## Manual Audit

每轮改造后抽样人工审核。

### 抽样策略

每类至少 20 条：

- auto-merged same_event
- high candidate
- medium review
- rejected non-event
- digest/roundup
- same product different event
- legacy cluster migration sample
- high-value briefing events

### 审核问题

对每个 cluster：

1. 是否真的是同一现实事件？
2. 是否混入了同主题不同事件？
3. 是否漏掉明显同事件 item？
4. representative item 是否合理？
5. event summary 是否准确？
6. event_type 是否正确？
7. confidence 是否校准？
8. 是否应进入 briefing？

### 审核输出

```json
{
  "cluster_id": "...",
  "verdict": "correct|over_merged|under_merged|non_event|uncertain",
  "severity": "P0|P1|P2|P3",
  "notes": "...",
  "recommended_action": "split|merge|reject|edit_summary|accept"
}
```

## Regression Gates

### Blocking gates

适合 CI 或提交前阻断：

- unit tests pass
- no schema error
- item dedupe precision >= 0.98 on fixture
- non-event hard negative cases pass
- auto-merge hard negative cases pass

### Non-blocking quality gates

适合报告但不阻断：

- same-event pair F1
- eventness recall
- candidate medium precision
- briefing/report quality score

### Release gates

上线前必须达标：

- auto-merge precision >= 0.95
- digest/generic false positive <= 0.02
- event_type known rate >= 0.80
- event summary specific rate >= 0.85
- manual audit P0 = 0

## 报告格式

每次评估报告应包含：

1. 数据集版本。
2. 代码版本或 git SHA。
3. 数据库路径和只读/写入模式。
4. 指标表。
5. 失败样例。
6. 根因分类。
7. 与上次评估的差异。
8. 推荐修复优先级。
9. 原始 JSON 指标。

## 本地命令

当前可用：

```bash
cd content_inbox
PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
PYTHONPATH=. python3 scripts/diagnose_event_aggregation.py
python3 -m py_compile scripts/evaluate_ops_quality.py scripts/diagnose_event_aggregation.py
PYTHONPATH=. pytest -q tests/test_ops_api.py
```

建议新增后：

```bash
PYTHONPATH=. pytest -q tests/test_event_dedupe_explanation.py
PYTHONPATH=. pytest -q tests/test_eventness_classifier.py
PYTHONPATH=. pytest -q tests/test_event_signature.py
PYTHONPATH=. pytest -q tests/test_event_candidates.py
PYTHONPATH=. pytest -q tests/test_event_relation_decisions.py
PYTHONPATH=. pytest -q tests/test_event_cluster_materialization.py
PYTHONPATH=. python3 scripts/evaluate_rebuild_dry_run.py --db data/content_inbox.sqlite3 --report docs/evaluation/rebuild_eval.md
```

## 测试数据版本管理

建议目录：

```text
content_inbox/tests/fixtures/event_aggregation/
  synthetic_items_v1.jsonl
  gold_relations_v1.jsonl
  hard_negatives_v1.jsonl
  alias_cases_v1.jsonl
  manual_audit_samples_v1.jsonl
```

每次修改规则时：

1. 新增失败样例到 fixture。
2. 不删除旧样例。
3. 给样例添加 `source_issue_id` 或 `notes`。
4. 报告中记录 fixture version。

## 问题分级

| 级别 | 定义 | 示例 |
|---|---|---|
| P0 | 自动误合并，严重污染事件 | 两个无关事件被合成一个高价值 event |
| P1 | 非事件进入简报或报告 | digest/广告/垃圾内容进入 briefing |
| P2 | 明显漏合并 | 同一发布事件拆成多个 event |
| P3 | 摘要/类型/置信度不佳 | event_type 不准、summary 太泛 |

P0/P1 应阻断发布。P2/P3 可进入 backlog，但需要跟踪趋势。

## 推荐执行节奏

### 每次代码改动

- Unit tests
- Synthetic benchmark
- py_compile

### 每次 pipeline 改动

- Large DB readonly diagnostics
- Manual audit 20-50 clusters
- Compare previous report

### 每次准备真实写入

- Dry-run rebuild
- Backup Fresh DB
- Canary write <= 50 items
- Review queue audit

### 每次发布前

- Full synthetic benchmark
- Default large DB readonly scan
- Manual audit >= 100 samples
- Report sign-off

## 当前基线

截至 2026-05-31：

Synthetic benchmark：

- process dedupe F1: 85.7%
- event clustering F1: 21.1%
- event_type known rate: 0.0%
- event summary specific rate: 0.0%
- non-event candidate rate: 100.0%

Deep diagnostic：

- lightweight F1: 38.7%
- signature exact F1: 62.1%
- candidate high F1: 61.1%
- candidate medium+ F1: 15.4%

Default large DB:

- rss_sources: 151
- inbox_items: 3278
- seen_count > 1 items: 861
- event_clusters: 1257
- clusters_without_cluster_items: 1052
- event_signature items: 672
- multi_signature_groups: 24

这些数字应作为后续改造对比基线。

## 完成定义

测试方案完成落地时，应满足：

- 有可重复的合成 benchmark。
- 有默认大库只读诊断。
- 有人工 gold relation fixture。
- 有单元测试覆盖 dedupe/eventness/signature/candidate/relation/materialization。
- 有清晰质量门。
- 每次改进都能回答“指标是否变好，失败样例是否减少，是否引入新的误合并”。

