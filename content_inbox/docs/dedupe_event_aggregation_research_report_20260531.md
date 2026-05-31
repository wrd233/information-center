# 去重与事件聚合能力深度调研报告

Status: historical diagnosis. It explains prior failure modes; current implementation policy lives in `event_aggregation_operational_v3.md`.

生成日期: 2026-05-31

## 摘要

本报告调研 `content_inbox` 当前在 item 去重、事件聚合、事件对象生成方面的实际能力。调研依据包括代码路径审计、默认大库 `data/content_inbox.sqlite3` 的只读统计、合成基准测试、以及 semantic signature/candidate 模块的对照实验。

核心结论是：当前系统已经具备基础 item 去重能力，并且历史上曾经尝试过 embedding/LLM/semantic 多种聚合形态；但当前 console operational pipeline 实际接入的是 lightweight 标题规则，无法稳定完成“现实世界事件”的去重与聚合。事件层的主要缺口不是某一个阈值，而是缺少清晰的事件语义分层：eventness、event identity、relation decision、evidence、incremental value 和 cluster materialization 没有形成统一闭环。

## 一阶目标

去重和事件聚合需要服务的目标不是“减少列表长度”，而是把大量来源中的信息转化为可消费的事件情报。

一个合格系统应回答以下问题：

1. 这条 item 是事件、事件线索、主题讨论、教程、日报、广告、社交碎片，还是低质内容？
2. 如果是事件，它的主体、对象、动作和时间窗口是什么？
3. 两条 item 的关系是什么：同一内容重复、近重复、同一事件新增事实、同一事件不同角度、同主题不同事件、同产品不同阶段、无关？
4. 对同一事件，哪些 item 是 source material，哪些只是重复报道，哪些提供新增事实？
5. 合并后的 event 是否值得进入简报、报告或人工审核？

因此，能力边界应分成两层：

- **Item 去重**：识别同一原始内容或同一条 RSS entry 的重复出现。
- **事件聚合**：识别不同来源、不同标题、不同语言表达下的同一现实世界事件。

这两层不能混用。URL/GUID/title-date 命中应折叠 item；actor/product/action/time/evidence 命中才应进入 event 聚合。

## 当前实现路径

### Item 写入去重

主要路径：

```text
ContentAnalyzeRequest
  -> normalize_content()
  -> build_dedupe_key()
  -> InboxStore.get_by_dedupe_key()
  -> insert or mark_seen_with_latest()
```

关键文件：

- `app/processor.py`
- `app/dedupe.py`
- `app/storage.py`

`build_dedupe_key()` 的优先级：

1. HTTP/HTTPS URL
2. source identity + GUID
3. source identity + normalized title + published date
4. source identity + title + content hash
5. source identity + title

重复命中后，系统更新：

- `seen_count`
- `last_seen_at`
- `latest_raw_json`
- `latest_seen_summary`

这说明 item 去重已经在写入阶段发生。

### 后置 dedupe stage

主要路径：

```text
api_run_pipeline_stage(stage="dedupe")
  -> item_ids_for_run()
  -> run_dedupe_stage()
  -> dedupe_groups / dedupe_group_items
```

当前后置 dedupe 只对已存在的 `inbox_items` 重新按 dedupe key 分组。但由于真正重复已经在写入阶段被折叠成同一个 item，后置 dedupe 通常只能看到单成员 group，难以解释重复来源。

### 当前 console 事件聚合

主要路径：

```text
api_runs_create(real_write)
  -> execute_run()
  -> generate_information_objects()
```

或者：

```text
api_run_pipeline_stage(stage="semantic"/"clusters"/"events"/"review")
  -> generate_information_objects()
```

`generate_information_objects()` 当前做了以下事情：

- 轻量抽取实体关键词
- 创建 `semantic_extractions`
- 按 source category 创建 topic
- 用 `normalized_title(title)` 对 item 分组
- 每组创建 `event_clusters`
- 每组创建 `cluster_items`
- 每组创建 `events`
- 每组创建 `review_queue`

这条路径的核心问题是：它把“规范化标题相同”当成主要事件聚合依据。

### 语义聚合模块

仓库中另有更完整的 semantic 路线：

- `app/semantic/signatures.py`
- `app/semantic/candidates.py`
- `app/semantic/relations.py`
- `app/semantic/clusters.py`
- `app/semantic/cluster_policy.py`

这套模块已经包含：

- event signature
- semantic level
- actor/product/action/time bucket
- candidate score
- generic overlap suppression
- thread/content/reject 分层
- cluster attach eligibility
- LLM 裁决接口

但这套能力没有进入当前 console operational pipeline，因此默认操作台看到的还是 lightweight 结果。

## 默认大库只读统计

数据库：`content_inbox/data/content_inbox.sqlite3`

规模：

| 表/对象 | 数量 |
|---|---:|
| rss_sources | 151 |
| rss_ingest_runs | 763 |
| inbox_items | 3278 |
| event_clusters | 1257 |
| cluster_items | 207 |
| events | 198 |
| review_queue | 226 |
| item_cards | 90 |
| item_relations | 86 |
| cluster_cards | 10 |
| llm_call_logs | 86 |

RSS source 状态：

| 状态 | 数量 |
|---|---:|
| active | 150 |
| broken | 1 |

Item 去重信号：

| 指标 | 值 |
|---|---:|
| items | 3278 |
| seen_count > 1 的 item | 861 |
| max seen_count | 10 |
| avg seen_count | 1.62 |
| total seen_count | 5315 |

这表明写入时 dedupe 已经折叠了大量重复出现。但 `dedupe_groups` 为 0，说明后置解释层缺失。

Cluster 结构：

| created_by | clusters | multi_clusters | avg_items | max_items |
|---|---:|---:|---:|---:|
| legacy | 1052 | 34 | 1.03 | 3 |
| lightweight_rule | 198 | 2 | 1.01 | 2 |
| rule | 7 | 0 | 1.00 | 1 |

Cluster 完整性：

| 指标 | 值 |
|---|---:|
| event_clusters | 1257 |
| clusters_without_cluster_items | 1052 |
| item_count_mismatch | 0 |

这说明大多数 legacy cluster 缺少可解释 item 链路。它们可能来自旧 embedding/LLM 路径，能看到标题和摘要，但难以追溯“哪些 item 为什么被合并”。

Cluster relation 统计：

| primary_relation | same_event | decision_source | 数量 |
|---|---:|---|---:|
| same_topic | 0 | lightweight_rule | 196 |
| new_info | 1 | rule | 7 |
| same_event | 1 | lightweight_rule | 4 |

Events：

| event_type | status | 数量 |
|---|---|---:|
| unknown | needs_review | 198 |

事件对象当前缺少类型化和摘要质量，难以作为简报材料。

`clustering_json`：

| relation | 数量 |
|---|---:|
| skipped_low_value | 1969 |
| new_event | 1052 |
| embedding_failed | 217 |
| incremental_update | 28 |
| duplicate | 6 |
| disabled | 5 |
| uncertain | 1 |

该统计反映旧 `cluster_content()` embedding 路线曾经运行，但有 217 次 embedding failure，且大多数 item 被跳过或新建事件，真正 incremental/duplicate 很少。

## Signature 扫描

对默认大库 3278 条 item 只读运行 `extract_event_signature()`：

| semantic_level | 数量 |
|---|---:|
| reject | 1703 |
| thread_signature | 884 |
| event_signature | 672 |
| content_signature | 19 |

Exact signature 分组：

| 指标 | 数量 |
|---|---:|
| signature_groups | 631 |
| multi_signature_groups | 24 |
| items_in_multi_signature_groups | 56 |

Exact title 分组：

| 指标 | 数量 |
|---|---:|
| exact_title_groups | 3214 |
| multi_exact_title_groups | 33 |
| items_in_multi_exact_title_groups | 97 |

观察：

- Signature exact 精度更高，但召回不足。
- Exact title 覆盖更多重复标题，但容易混入泛标题、低质内容、站点模板和非事件。
- 大库真实内容包含大量社交碎片、低价值条目、泛标题、成人/垃圾内容，事件聚合前必须先做 eventness 与 source/content quality gate。

## 合成对照实验

测试集：86 条合成样例，覆盖：

- URL tracking 去重
- HTTP/HTTPS scheme 差异
- GUID 去重
- 同源标题日期去重
- 跨来源同事件改写
- 中英文标题变体
- 泛标题误合并
- digest/roundup/market wrap 非事件
- 同主题不同事件

结果：

| 方法 | Precision | Recall | F1 |
|---|---:|---:|---:|
| 当前 lightweight 完全标题 | 54.5% | 30.0% | 38.7% |
| semantic signature 精确匹配 | 100.0% | 45.0% | 62.1% |
| semantic candidate high | 68.8% | 55.0% | 61.1% |
| semantic candidate medium+ | 8.9% | 55.0% | 15.4% |

解释：

- 完全标题规则同时低召回和中等误合并。
- Signature exact 高精度，但无法覆盖标题改写、别名、跨语言、长产品名变体。
- Candidate high 提高召回，但仍会把 digest/generic title 错当事件。
- Candidate medium 误报暴增，说明 medium 只能进 review，不能自动聚合。

## 主要失败模式

### 失败模式 1：标题改写导致漏合并

同一事件在不同媒体中的标题通常不会完全一致。例如：

- `OpenAI launches GPT-5.5 for coding agents`
- `OpenAI rolls out GPT-5.5 model aimed at coding agents`
- `OpenAI GPT 5.5 model launches for software agents`

当前 lightweight 规则会拆成多个 cluster。

### 失败模式 2：泛标题导致误合并

例如：

- `Breaking: Major update announced`
- `AI Daily Briefing: OpenAI, Anthropic, Nvidia updates`
- `Market wrap: AI stocks rally`
- `Tweet`
- 纯 emoji / 短标题

这些标题相同并不代表同一事件。

### 失败模式 3：非事件被创建为事件

Digest、newsletter、market wrap、教程、观点、社交转发和低信号内容不应该直接成为 event。当前 lightweight 路径没有 eventness gate，因此会产生大量“候选事件”噪音。

### 失败模式 4：item 去重与事件聚合边界混乱

写入阶段的 dedupe 折叠了重复 item，但后置 dedupe stage 没有解释 `seen_count` 和来源重复链路。事件聚合又用标题分组，导致用户难以判断“这是 item 重复、报道重复，还是事件增量”。

### 失败模式 5：legacy cluster 缺少证据链

大库中 1052 个 legacy cluster 没有 `cluster_items`，这会导致：

- 无法解释聚合依据。
- 无法回放和评估。
- 无法给 review UI 提供证据。
- 无法安全迁移到新的 event schema。

### 失败模式 6：事件对象字段过薄

当前 operational events 统一为：

- `event_type=unknown`
- `status=needs_review`
- summary 模板化
- importance 近似按成员数量
- confidence 低且粗糙

这无法支持高质量 briefing/report。

## 根因分析

根因不是“聚类阈值不合适”，而是系统缺少事件聚合所需的多层语义模型。

### 1. 缺少 eventness gate

没有先判断 item 是否适合成为事件。结果是非事件内容也被 materialize 成 event。

### 2. 缺少稳定 event identity

完全标题不是事件身份。事件身份应至少包含：

```text
actor + product/object + action + time_bucket
```

并结合 source/evidence 做置信度判断。

### 3. 别名和产品名规范化不足

真实数据中常见：

- `GPT-5.5` / `GPT 5.5`
- `DeepSeek` / `深度求索`
- `EU` / `European Commission`
- `Codex` / `OpenAI/Codex`
- 长产品名与短产品名混用

没有 alias map 会让 signature exact 召回不足。

### 4. 负特征不足

Digest、generic title、same account boilerplate、wide time window、topic-only overlap 应当强力降权或拒绝自动合并。

### 5. 自动合并和 review 没有分层

High confidence same-event 可以自动合并；medium 和 uncertain 应进入 review。当前 lightweight 没有这个分层。

### 6. 数据模型历史债

legacy clusters、embedding clustering、operational event objects 没有统一证据链。新的改造需要兼顾迁移和回放。

## 能力评估

| 能力 | 当前状态 | 风险 |
|---|---|---|
| URL/GUID/title-date item 去重 | 基本可用 | HTTP/HTTPS 可配置归一化不足；解释层弱 |
| 写入时重复折叠 | 可用 | 重复来源不可视 |
| 后置 dedupe group | 弱 | 重复已折叠后只剩单成员 group |
| 完全标题聚合 | 可用但不可靠 | 漏合并和误合并都明显 |
| semantic signature | 有潜力 | 未接入 console；召回不足 |
| candidate scorer | 有潜力 | medium 噪音大，需 review 分层 |
| event object | 弱 | 类型、摘要、证据不足 |
| review queue | 有基础 | review payload 需要更具体证据 |
| briefing/report 支撑 | 弱 | event 数据质量不足 |

## 调研结论

当前系统最应该保留的是写入时 item dedupe 和已有 semantic 模块的方向；最应该替换的是 console pipeline 中的完全标题事件聚合。下一阶段不是简单调阈值，而是把事件聚合拆成可评估、可解释、可回放的 pipeline。

推荐目标：

- Item 去重保持高精度，补充解释。
- Event 聚合先保证自动合并 precision，再逐步提高 recall。
- 所有自动合并必须有证据链。
- 所有 medium/uncertain 进入 review。
- Event object 必须能支撑 briefing/report。
