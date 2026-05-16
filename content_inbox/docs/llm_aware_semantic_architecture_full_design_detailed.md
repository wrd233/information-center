# LLM-aware 语义信息处理系统完成体设计文档

> 适用项目：`information-center / content_inbox`  
> 文档定位：长期完成体架构设计  
> 设计主题：在 RSS 信息抓取、基础去重、事件聚合、信源画像与 LLM 调度中引入大模型，并通过语义对象、关系表、卡片层、缓存、路由和人工治理保持系统长期可用。  
> 当前结论：本系统不是“把所有 RSS item 丢给大模型处理”，而是一个 **LLM-aware 的信息研究辅助系统**：原始信息稳定入库，规则和向量先行处理，大模型在关键语义判断点介入，其结果再沉淀为事件簇、关系、卡片和信源画像，反过来优化未来的大模型调用。

---

## 0. 背景与目标

### 0.1 现有系统的问题

当前 `content_inbox` 已经具备 RSS 抓取、基础入库、source registry、run history、基础 dedupe 等能力。它解决了最基础的问题：

> 能不能把大量 RSS 源中的信息抓下来，并稳定保存起来？

但当 RSS 源数量达到数百个、每天进入的信息达到成百上千条后，系统会遇到更高层的问题：

1. **重复信息过多**  
   不同 RSS 源、新闻站、博客、聚合源可能在讲同一件事，甚至大量转述同一份官方公告。

2. **相似但不完全重复的信息难以处理**  
   标题不同、语言不同、链接不同，但内容几乎相同；或者同一事件下有些文章只是复述，有些文章有新增事实和分析。

3. **事件级组织不足**  
   用户真正关心的通常不是“某一篇文章”，而是“这件事发生了什么、有哪些来源讲了它、哪篇最值得看”。

4. **信源长期价值没有沉淀**  
   某些源长期重复、搬运、低增量；某些源虽然产量不高，但经常提供一手体验、原始材料或深度分析。系统需要逐渐识别这种差异。

5. **LLM 调用成本和限制需要被控制**  
   如果每条 item 都全文调用大模型，不仅成本高，而且容易触发调用限制。系统必须把大模型视为有限资源，而不是默认流水线。

### 0.2 完成体目标

完成体系统的目标是：

> 在保持 RSS 抓取和原始入库稳定的前提下，建立一个面向信息研究的语义处理层。该层能够识别 item 与 item 的重复/近重复关系，识别 item 与 event cluster 的事件归属关系，维护 cluster_card 与 source_profile，并通过 source_profile 与历史 LLM 产出收益动态调度未来的大模型调用。

完成体应具备以下能力：

1. **稳定抓取与事实层入库**
   - RSS / 网页 / 手动链接 / 未来外部输入统一形成 `inbox_items`。
   - 原始事实层尽量稳定，不被 LLM 覆盖。

2. **轻量语义卡片**
   - 为所有 item 生成轻量 `item_card`。
   - 高价值 item 可生成完整 `item_card`。

3. **第二层基础去重**
   - 识别 `exact_duplicate`、`near_duplicate`、`derived_duplicate`、`same_event_new_info`、`different`、`uncertain`。
   - 保守折叠，不物理删除 item。

4. **第三层事件聚合**
   - 判断 item 是否属于已有事件簇。
   - 区分重复报道、新增事实、独立分析、一手体验、背景补充、后续事件、同主题不同事件等角色。

5. **事件簇维护**
   - 维护 `event_clusters` 与 `cluster_cards`。
   - 支持生命周期：`active`、`cooling`、`archived`、`reopened`、`merged`。
   - 支持增量 patch 与周期性重整。

6. **信源画像**
   - 从 item-level `source_signal` 聚合到 source-level `source_profile`。
   - 维护 `llm_priority`、`llm_yield_score`、重复率、增量价值、报告价值等指标。

7. **LLM 调用路由**
   - 规则能做的，不交给 LLM。
   - Embedding 负责召回候选。
   - LLM 负责关系裁判。
   - Source profile 反向影响未来 LLM 调用优先级。

8. **可追溯、可重算、可治理**
   - 所有 LLM 输出必须结构化、版本化、可审计。
   - 支持人工修正：merge/split/detach/reassign/approve/rerun。
   - 支持 review queue。

---

## 1. 第一性原理：为什么要设计这些语义对象

### 1.1 信息系统的核心问题不是“存储更多信息”

如果系统只是不断抓取更多 RSS item，那么它最终会变成一个更大的信息堆。用户真正需要的是：

> 在大量信息中发现“值得注意的事情”、筛选“值得阅读的材料”、沉淀“值得长期跟踪的信源”。

因此，系统的核心不是“抓得更多”，而是：

1. 把重复和低增量内容折叠起来。
2. 把同一事件的多源信息组织起来。
3. 从同一事件中找出最有价值的代表内容。
4. 从长期历史中发现高价值信源。
5. 把有限 LLM 调用分配给最值得处理的信息。

### 1.2 item、event、cluster、source 的本质区别

| 概念 | 本质 | 系统对象 | 典型问题 |
|---|---|---|---|
| item | 单条具体信息 | `inbox_items` | 这条信息是什么、来自哪里？ |
| item_card | item 的压缩语义表示 | `item_cards` | 这条信息用较少 token 如何表达？ |
| event | 现实中的具体事情 | 语义概念 | 现实中发生了什么？ |
| cluster | 系统中的事件容器 | `event_clusters` | 哪些 item 在讲同一件事？ |
| cluster_card | cluster 的压缩语义状态 | `cluster_cards` | 这个事件目前的核心事实和视角是什么？ |
| relation | 对象之间的关系 | `item_relations` / `cluster_items` | 是否重复、是否同事件、有何贡献？ |
| source | 信息来源 | `sources` / `rss_sources` | 信息来自哪里？ |
| source_profile | 信源长期画像 | `source_profiles` | 这个源以后值得调用 LLM 吗？ |
| topic | 长期主题 | `topics`，可后续扩展 | 这属于哪个长期领域？ |
| thread | 事件发展线索 | `cluster_relations` / 未来 `threads` | 这些事件是否构成一条后续链？ |

### 1.3 为什么要有 card 层

直接把原始全文传给 LLM 有几个问题：

1. token 消耗大；
2. 同一内容会被重复处理；
3. 不同 prompt 对原文理解不稳定；
4. 后续关系判断缺少统一输入；
5. 缓存命中率低。

因此系统需要把原始 item 先压缩成 card：

> 原始 item 是事实记录，item_card 是后续语义判断的标准输入。

完成体中应形成三类核心 card：

1. `item_card`：单条 item 的压缩语义卡片；
2. `cluster_card`：事件簇的压缩状态卡片；
3. `source_profile`：信源长期画像卡片。

这三类 card 共同构成 LLM-aware 系统的“低 token 语义层”。

---

## 2. 分层架构

完成体架构建议分为九层。

```text
输入与事实层
  ↓
规则预处理与硬去重层
  ↓
语义卡片层
  ↓
向量召回层
  ↓
策略网关层
  ↓
第二层 item-item relation 判断
  ↓
第三层 item-cluster relation 判断
  ↓
写回与画像更新层
  ↓
人工治理与评估层
```

### 2.1 输入与事实层

目标：

> 稳定获取信息，并保存最原始、最可信、可回溯的事实记录。

核心对象：

- `inbox_items`
- `sources` / `rss_sources`
- `rss_ingest_runs`
- `rss_ingest_run_sources`

事实层必须具备以下原则：

1. 原始 item 不应被 LLM 直接覆盖。
2. 入库前只做确定性处理和必要清洗。
3. LLM 失败不应阻塞 RSS 抓取。
4. 语义处理状态可以异步更新。
5. 原始数据可用于未来重算。

### 2.2 规则预处理与硬去重层

目标：

> 处理确定性问题，减少不必要的大模型调用。

典型规则：

- URL canonicalization；
- GUID 匹配；
- canonical_url 匹配；
- content_hash 匹配；
- title_hash 辅助匹配；
- language detection；
- published_at 标准化；
- source_id 识别；
- 内容长度检查；
- 广告/促销/低信息量初筛。

如果规则能够确定 `exact_duplicate`，系统应直接写入 relation 并折叠展示，不调用 LLM。

### 2.3 语义卡片层

目标：

> 将原始 item 转换为统一、短小、可复用、可缓存的语义对象。

核心对象：

- `item_cards`
- `cluster_cards`
- `source_profiles`

完成体应支持两级 `item_card`：

1. **轻量 item_card**
   - 所有 item 默认生成。
   - 主要用于 embedding、候选召回、基础关系判断。
   - 优先使用规则 + DeepSeek Flash。

2. **完整 item_card**
   - 仅对高价值或不确定 item 生成。
   - 包含更完整的 key_facts、key_opinions、cited_sources、source_signal 等。
   - 可用 Flash，也可在高价值任务中用 Pro。

### 2.4 向量召回层

目标：

> 从海量历史 item / cluster 中找出少量候选，供 LLM 裁判。

召回对象：

- 历史 item cards；
- 历史 cluster cards。

召回方式：

- item embedding index；
- cluster embedding index；
- 时间窗口过滤；
- source 过滤；
- 主实体过滤；
- cluster 状态过滤。

原则：

> Embedding 负责召回，不负责最终裁判。

### 2.5 策略网关层

目标：

> 判断某条 item 是否需要 LLM、需要哪一级 LLM、需要哪些候选上下文。

策略网关综合以下因素：

- 是否规则命中；
- item 相似度；
- cluster 相似度；
- source priority；
- source llm_yield；
- item 内容长度；
- 是否有 cited_sources；
- 是否疑似新事件；
- 是否来自高价值源；
- 是否属于热点 cluster；
- 是否存在 conflicting candidates；
- 是否已经有 relation cache。

输出路由：

| 路由 | 适用场景 | Token 强度 |
|---|---|---|
| `skip_llm` | 确定重复、低价值、禁用源普通 item | 极低 |
| `cheap_item_card` | 轻量 card 生成 | 低 |
| `item_relation_batch` | 疑似近重复，第二层裁判 | 中 |
| `cluster_relation_batch` | 事件归属，第三层裁判 | 中~高 |
| `strong_model_review` | 高价值复杂判断、归档总结、人工审核报告 | 高~极高 |

### 2.6 第二层 item-item relation 判断

目标：

> 判断新 item 与历史 item 的关系，解决“是不是已经出现过或只是重复表达”的问题。

第二层处理的是 **item-item relation**。

它不负责：

- 生成 cluster 摘要；
- 维护 topic；
- 删除 item；
- 把同事件但有新增信息的 item 丢弃。

### 2.7 第三层 item-cluster relation 判断

目标：

> 判断新 item 是否属于已有 cluster，以及它对该 cluster 的贡献是什么。

第三层处理的是 **item-cluster relation**。

它需要区分：

- 同事件；
- 同主题但非同事件；
- follow-up event；
- 重复报道；
- 新增事实；
- 新增分析；
- 一手体验；
- 背景补充；
- 低价值观点。

### 2.8 写回与画像更新层

目标：

> 将 LLM 判断转化为稳定的数据库对象，并更新长期画像。

写回对象：

- `item_relations`
- `cluster_items`
- `event_clusters`
- `cluster_cards`
- `source_signals`
- `source_profiles`
- `llm_call_logs`
- `review_queue`

原则：

1. LLM 输出不能直接等于数据库事实。
2. 系统根据 schema、置信度、规则优先级和状态机执行写回。
3. 所有写回应可追溯、可重算。

### 2.9 人工治理与评估层

目标：

> 保持系统长期语义一致，纠正误判，控制 LLM 调度策略。

治理能力：

- merge cluster；
- split cluster；
- detach item；
- reassign item；
- mark relation；
- approve source upgrade；
- approve source downgrade；
- disable source LLM；
- enable source LLM；
- rerun semantic；
- rebuild cluster card；
- review uncertain cases。

---

## 3. 核心语义对象设计

### 3.1 `inbox_items`：事实层 item

定位：

> 系统抓取到的单条原始信息，是事实层对象。

设计原则：

1. 尽量保持当前表稳定。
2. 不把大量 LLM 派生字段塞入 `inbox_items`。
3. 可以保留少量状态字段，以便快速查询。

建议字段类别：

- 标识字段：`id`、`source_id`；
- 原始元数据：`title`、`url`、`guid`、`author`；
- 规范化字段：`canonical_url`、`language`；
- 时间字段：`published_at`、`fetched_at`、`created_at`；
- 内容字段：`raw_summary`、`raw_content`；
- 指纹字段：`content_hash`、`title_hash`；
- 轻量状态：`semantic_status`、`dedupe_status`、`primary_cluster_id`（可选冗余）。

`primary_cluster_id` 只是查询优化，不应该替代 `cluster_items`。

### 3.2 `item_cards`：压缩语义层

定位：

> 对 item 的标准化语义压缩表示，是后续 LLM 判断和 embedding 的核心输入。

完成体 schema 建议：

```text
item_cards
- id
- item_id
- card_version
- card_level: light / full
- model
- prompt_version
- input_fingerprint
- canonical_title
- language
- event_hint
- entities
- key_facts
- key_opinions
- content_role
- cited_sources
- short_summary
- embedding_text
- confidence
- warnings
- created_at
- updated_at
```

#### 3.2.1 `event_hint` 的语义

`event_hint` 是 item 自己暗示的“它在讲什么事”，不是 cluster 归属结论。

例如：

```text
event_hint = "OpenAI 发布 GPT-5.5 并加强 Codex 能力"
```

该字段用于候选召回和 prompt 输入，不能直接作为 cluster ID。

#### 3.2.2 `key_facts` 与 `key_opinions` 必须分离

这可以防止模型把观点当事实。

- `key_facts`：可验证、可交叉引用的事实；
- `key_opinions`：作者判断、预测、立场、评价。

#### 3.2.3 `content_role`

完成体 content_role 可包括：

| role | 含义 |
|---|---|
| `source_material` | 原始材料、官方公告、论文、release note、原始数据 |
| `report` | 报道、新闻、转述 |
| `analysis` | 分析、解释、判断 |
| `firsthand` | 一手体验、实测、现场反馈 |
| `commentary` | 评论、观点、立场表达 |
| `aggregator` | 聚合、导航、周报、链接集合 |
| `low_signal` | 低信息量、广告、重复摘要、噪音 |

### 3.3 `item_relations`：第二层关系表

定位：

> 描述 item 与 item 之间的关系。

#### 3.3.1 收缩后的 primary relation

为降低复杂度，完成体建议将第二层 primary relation 收缩为：

| primary_relation | 含义 | 默认动作 |
|---|---|---|
| `exact_duplicate` | 确定完全重复，包括同 URL/GUID/hash/canonical URL | 折叠 |
| `near_duplicate` | 高度近似重复，事实点几乎一致，无明显新增 | 折叠 |
| `derived_duplicate` | 翻译、改写、摘要、搬运等派生重复，无实质新增 | 折叠 |
| `same_event_new_info` | 同一事件，但提供了新事实、新分析或一手体验 | 保留，进入第三层 |
| `different` | 不重复，且不是同一具体事件 | 保留 |
| `uncertain` | 信息不足或判断冲突 | 保留，进入 review queue |

这里将原先的 `translation`、`rewrite`、`summary_of` 收缩进 `derived_duplicate`，减少枚举膨胀。

#### 3.3.2 secondary_roles

如果需要保留更细信息，使用 `secondary_roles`：

```text
translation
rewrite
summary
syndicated
mirror
cross_language
same_source_repost
possible_ai_rewrite
```

示例：

```json
{
  "primary_relation": "derived_duplicate",
  "secondary_roles": ["translation", "summary"],
  "should_fold": true
}
```

#### 3.3.3 item_relations 字段

```text
item_relations
- id
- item_a_id
- item_b_id
- primary_relation
- secondary_roles
- confidence
- should_fold
- canonical_item_id
- new_information
- reason
- evidence
- decision_source: rule / llm_flash / llm_pro / human
- llm_call_id
- prompt_version
- created_at
- updated_at
```

### 3.4 `event_clusters`：事件容器

定位：

> 系统中表示“同一具体事件”的容器。

字段：

```text
event_clusters
- id
- title
- status: active / cooling / archived / reopened / merged
- topic_ids
- thread_id nullable
- first_seen_at
- last_seen_at
- last_major_update_at
- item_count
- representative_item_id
- source_material_item_id
- cluster_card_id
- created_by: rule / llm_flash / llm_pro / human
- confidence
- merged_into_cluster_id nullable
- created_at
- updated_at
```

cluster 不等于 topic。cluster 是具体事件容器，topic 是长期领域。

### 3.5 `cluster_items`：第三层关系表

定位：

> 描述 item 在 cluster 中的角色和贡献。

#### 3.5.1 收缩后的 primary relation

第三层 primary relation 建议收缩为：

| primary_relation | 含义 | 是否更新 cluster_card |
|---|---|---|
| `source_material` | 原始来源、官方材料、权威材料 | 是 |
| `duplicate_report` | 重复报道或低增量转述 | 否 |
| `new_info` | 新事实、重要补充、背景上下文 | 是，视价值 |
| `interpretation` | 分析、解释、评论、预测 | 视价值 |
| `firsthand` | 一手体验、实测、现场反馈 | 是，视价值 |
| `follow_up_event` | 相关后续事件，通常应新建 cluster 并关联 | 不直接并入原 cluster |
| `same_topic_only` | 同主题但不是同一事件 | 否 |
| `unrelated` | 无关 | 否 |
| `uncertain` | 不确定 | 否，进入 review |

这里将原先的 `new_fact`、`background_context` 收进 `new_info`，将 `new_analysis`、`opinion_only` 收进 `interpretation`，降低枚举数量。

#### 3.5.2 secondary_roles

第三层可用 secondary_roles 保留细节：

```text
new_fact
background_context
new_analysis
opinion_only
source_quote
data_point
benchmark
case_study
risk_signal
user_feedback
contrarian_view
```

示例：

```json
{
  "primary_relation": "interpretation",
  "secondary_roles": ["new_analysis", "contrarian_view"],
  "incremental_value": 4,
  "should_update_cluster_card": true
}
```

#### 3.5.3 显式语义维度

第三层必须强制输出：

```text
same_event: true / false
same_topic: true / false
follow_up_event: true / false
```

原因：

- 同事件不等于重复；
- 同主题不等于同事件；
- follow-up event 不应该被粗暴塞进原 cluster。

#### 3.5.4 cluster_items 字段

```text
cluster_items
- id
- cluster_id
- item_id
- primary_relation
- secondary_roles
- same_event
- same_topic
- follow_up_event
- confidence
- incremental_value
- report_value
- should_update_cluster_card
- should_notify
- reason
- evidence
- llm_call_id
- decision_source
- created_at
- updated_at
```

### 3.6 `cluster_cards`：事件簇卡片

定位：

> 事件簇的当前压缩语义状态。

完成体 schema：

```text
cluster_cards
- id
- cluster_id
- card_version
- model
- prompt_version
- input_fingerprint
- cluster_title
- event_type
- main_entities
- core_facts
- known_angles
- representative_items
- source_material_items
- open_questions
- follow_up_clusters
- same_topic_clusters
- first_seen_at
- last_major_update_at
- confidence
- created_at
- updated_at
```

#### 3.6.1 更新策略

不应每加入一条 item 就全量重写 cluster_card。

策略：

| 新 item 类型 | 动作 | Token 强度 |
|---|---|---|
| `duplicate_report` | 不更新核心摘要 | 无/极低 |
| `interpretation` 且低价值 | 可不更新或延迟 patch | 极低/低 |
| `new_info` | 增量 patch | 中 |
| `source_material` | 增量 patch，可能更新代表源 | 中 |
| `firsthand` 且高价值 | 增量 patch | 中 |
| 高价值 cluster 归档 | 全量重整 | 高 |
| 人工修正后 | 重整或 patch | 中~高 |

推荐：

> 日常增量 patch + 周期性重整，而不是每条 item 都全量重写。

### 3.7 `source_signals` 与 `source_profiles`

#### 3.7.1 source_signal

`source_signal` 是单条 item 处理时产生的信源贡献信号。

```text
source_signals
- id
- source_id
- item_id
- cluster_id nullable
- originality_delta
- duplicate_signal
- incremental_value
- report_value
- firsthand_value
- citation_quality
- source_role
- llm_call_id
- created_at
```

#### 3.7.2 source_profile

`source_profile` 是长期聚合画像。

```text
source_profiles
- source_id
- total_items
- llm_processed_items
- duplicate_rate
- near_duplicate_rate
- derived_duplicate_rate
- same_event_new_info_rate
- new_cluster_rate
- incremental_value_avg
- report_value_avg
- firsthand_value_avg
- source_material_rate
- representative_item_rate
- citation_quality_avg
- llm_total_tokens
- llm_high_value_outputs
- llm_yield_score
- llm_priority
- review_status
- last_reviewed_at
- updated_at
```

#### 3.7.3 llm_priority

```text
new_source_under_evaluation
high
normal
low
disabled_for_llm
pending_review
```

原则：

1. source 升级为 high 应进入人工审核；
2. source 降级为 disabled_for_llm 应进入人工审核；
3. low 可以自动建议，但最好仍可 CLI 审核；
4. disabled_for_llm 不意味着不抓取，只是不再为普通 item 单独调用 LLM。

---

## 4. 语义处理流程

### 4.1 总流程

```text
1. RSS / 网页 / 手动输入进入
2. 原始 item 入库
3. 规则预处理与硬去重
4. 生成轻量 item_card
5. embedding 召回相似 item / cluster
6. 策略网关决定是否调用 LLM
7. 第二层 item-item relation 判断
8. 第三层 item-cluster relation 判断
9. 写回 relation / cluster / card / signal / log
10. 更新 source_profile
11. 必要时进入 review_queue
```

### 4.2 为什么选择“先入库，后语义处理”

系统采用：

> 方案 B：先入库，后语义处理。

原因：

1. RSS 抓取必须稳定，不应被 LLM API 失败拖垮。
2. LLM 调用有速率限制、成本、失败、超时等不确定性。
3. 语义处理可以重试、批处理、暂停、回放。
4. 历史 item 可以 backfill。
5. Semantic worker 可以独立调度和扩展。

因此：

```text
ingest pipeline：轻、稳、快
semantic pipeline：可重试、可调度、可审计
```

### 4.3 第二层详细流程

```text
new item
  ↓
规则硬去重
  ↓
如果 same_url / same_guid / same_hash / same_canonical_url 命中
  → 写 item_relation = exact_duplicate
  → 折叠展示
  → 不调用 LLM
  ↓
如果未命中
  → 读取或生成 item_card
  → embedding 查 top-k 相似历史 item
  → 候选过滤
  → LLM 批量判断 item-item relation
  → 写 item_relations
  → 对 same_event_new_info 进入第三层
```

### 4.4 第三层详细流程

```text
new item_card
  ↓
embedding 查 top-k candidate clusters
  ↓
候选精简
  - 时间窗
  - 主实体重合
  - cluster 状态
  - 相似度
  - source_profile
  ↓
LLM 批量判断 item-cluster relation
  ↓
action:
  - attach_to_cluster
  - create_new_cluster
  - uncertain
  ↓
relation:
  - source_material
  - duplicate_report
  - new_info
  - interpretation
  - firsthand
  - follow_up_event
  - same_topic_only
  - unrelated
  - uncertain
  ↓
写 cluster_items / event_clusters / cluster_relations / review_queue
  ↓
必要时 patch cluster_card
```

---

## 5. LLM 调用设计

### 5.1 模型选型

当前项目中第一版采用 DeepSeek V4 系列：

- 默认与核心任务：`deepseek-v4-flash`
- 少量最关键任务：`deepseek-v4-pro`

DeepSeek API 支持 OpenAI 兼容格式；base URL 使用 `https://api.deepseek.com`。模型文档显示 DeepSeek V4 包含 `deepseek-v4-flash` 与 `deepseek-v4-pro`，支持 JSON Output、Tool Calls、1M context 等能力。实际项目中应沿用当前已有 API key 配置位置，不在文档中写入密钥。

### 5.2 模型分级策略

| 任务 | 默认模型 | 升级到 Pro 的条件 |
|---|---|---|
| 轻量 item_card | Flash | 高价值源 + 需要完整 card |
| 第二层疑似重复判断 | Flash | 跨语言复杂、候选冲突、低置信度 |
| 第三层 item-cluster 判断 | Flash | 重大事件、候选 cluster 冲突、follow-up ambiguity |
| cluster_card 增量 patch | Flash | 高价值 cluster 或多次冲突 |
| cluster_card 全量重整 | Pro | 归档、高价值专题、人工触发 |
| source 升降级报告 | Flash/Pro | 禁用 LLM、升级 high 等高风险状态 |
| review_queue 解释 | Pro | 人工复核要求高可信解释 |

第一阶段可以先放宽 Pro 使用，以观察效果；完成体应逐渐根据 llm_yield 与评估结果降本。

### 5.3 JSON Output 与结构化约束

所有 LLM 调用必须要求 JSON 输出，并进行 schema validation。

必须记录：

- `task_type`
- `model`
- `prompt_version`
- `schema_version`
- `input_fingerprint`
- `raw_output`
- `parsed_output`
- `status`
- `usage`
- `cost_estimate`
- `latency_ms`

如果 JSON 解析失败：

1. 重试一次；
2. 降级为 `uncertain`；
3. 写入 `llm_call_logs`；
4. 必要时进入 `review_queue`。

### 5.4 一次调用放入更多候选的 token trick

为了减少调用次数，可以将多个候选放入一次 LLM 调用。

#### 第二层 batch

输入：

```json
{
  "task": "item_item_relation_batch",
  "new_item_card": {},
  "candidate_item_cards": [
    {},
    {},
    {}
  ],
  "hard_signals": {}
}
```

输出：

```json
{
  "relations": [
    {
      "candidate_item_id": "...",
      "primary_relation": "...",
      "secondary_roles": [],
      "confidence": 0.0,
      "should_fold": true,
      "reason": "..."
    }
  ]
}
```

#### 第三层 batch

输入：

```json
{
  "task": "item_cluster_relation_batch",
  "new_item_card": {},
  "candidate_clusters": [
    {
      "cluster_id": "...",
      "cluster_card": {},
      "representative_item_cards": []
    }
  ],
  "source_profile_summary": {}
}
```

输出：

```json
{
  "decision": {
    "action": "attach_to_cluster | create_new_cluster | uncertain",
    "cluster_id": "...",
    "primary_relation": "...",
    "secondary_roles": [],
    "same_event": true,
    "same_topic": true,
    "follow_up_event": false,
    "confidence": 0.0
  }
}
```

原则：

1. 一次调用中候选不宜过多；
2. 第二层默认 top 3-5 candidate items；
3. 第三层默认 top 3 candidate clusters；
4. 每个 cluster 默认只放 1-3 个 representative item cards；
5. 使用稳定字段顺序提高缓存命中；
6. 大部分判断使用 card，不使用全文。

### 5.5 Context caching 设计

为提高缓存命中率：

1. prompt 模板保持稳定；
2. schema 文本保持稳定；
3. 字段顺序固定；
4. 枚举说明固定；
5. candidate cards 尽量短且确定；
6. source_profile summary 只放必要字段；
7. 不在 prompt 中加入随机描述。

---

## 6. Cluster 生命周期与边界

### 6.1 状态机

```text
active → cooling → archived
   ↑         ↓
reopened ← 重大后续
merged   ← 人工或高置信合并
```

| 状态 | 含义 |
|---|---|
| `active` | 最近仍有新事实、新分析或高价值补充 |
| `cooling` | 近期只有重复报道或低增量补充 |
| `archived` | 长时间无重大新增，进入归档 |
| `reopened` | 归档后出现明确后续 |
| `merged` | 被合并进其他 cluster |

### 6.2 时间窗口建议

默认建议：

- `active`：最近 3 天有新事实/高价值分析；
- `cooling`：最近 7-14 天无重大新增，但仍可能有重复报道；
- `archived`：超过 30 天无重大新增；
- `reopened`：归档后出现高置信 follow-up 或同一事件重大更新。

这些阈值可配置，并可按 topic 调整。

### 6.3 同事件、同主题、后续事件边界

#### 同事件 same_event

同一现实事实、同一核心动作、同一时间窗口、同一主要实体。

例：

- 官方公告：OpenAI 发布 GPT-5.5；
- 媒体报道：OpenAI unveils GPT-5.5；
- 开发者实测：GPT-5.5 发布后实测表现。

其中实测可以作为同一事件下的 `firsthand` 或 `interpretation`。

#### 同主题 same_topic_only

同属一个领域，但不是同一现实事实。

例：

- OpenAI 发布 GPT-5.5；
- Anthropic 发布 Claude 新版本。

它们同属 AI 模型发布主题，但不是同一事件。

#### 后续事件 follow_up_event

由原事件引发，但具有新的事实变化、时间点或发展阶段。

例：

- A：OpenAI 发布 GPT-5.5；
- B：GPT-5.5 API 出现大规模故障；
- C：OpenAI 修复该故障。

B 应新建 cluster，并与 A 建立 `follow_up` 或 `same_topic` 关系。C 可能属于 B 的同事件后续，或作为新的修复事件，视粒度而定。

### 6.4 follow-up 判断规则

如果新 item 满足以下条件，更倾向 `follow_up_event`：

1. 有新的时间点；
2. 有新的动作或状态变化；
3. 不是对原事件的报道或分析；
4. 与原事件因果相关；
5. 原 cluster 已进入 cooling/archived；
6. 加入原 cluster 会污染 core_facts。

---

## 7. Source Profile 与 LLM 调度

### 7.1 为什么 source_profile 是完成体核心

LLM 调用不应只由单条 item 决定，也要由历史源表现决定。

目标：

> 每一次 LLM 调用都产生可复用的 source_signal；source_signal 聚合成 source_profile；source_profile 反过来影响未来 LLM 调度。

### 7.2 升降级规则

#### new_source_under_evaluation → normal

条件：

- 已处理达到最小样本数；
- 没有明显低质量；
- duplicate_rate 不高；
- 至少有少量非重复内容。

#### normal → high

建议条件：

- `incremental_value_avg` 高；
- `report_value_avg` 高；
- `representative_item_rate` 高；
- `source_material_rate` 或 `firsthand_value_avg` 高；
- `llm_yield_score` 高。

必须进入 `pending_review`，经 CLI 批准后升级。

#### normal → low

建议条件：

- 重复率持续偏高；
- LLM 处理后多为 `duplicate_report` 或 `derived_duplicate`；
- `incremental_value_avg` 低；
- `llm_yield_score` 低。

可自动建议，建议仍进入 review queue。

#### low → disabled_for_llm

建议条件：

- 长期低 yield；
- 调用 LLM 几乎没有新信息；
- 多次被判断为重复或低信号；
- 人工确认不值得单独解析。

必须进入人工审核。

#### low / disabled_for_llm → normal

恢复条件：

- 抽样复检出现高价值内容；
- 被多个高质量源引用；
- 人工恢复。

### 7.3 disabled_for_llm 不等于停止抓取

低质量源仍可继续抓取，因为它们可能：

- 反映传播热度；
- 偶尔提供早期信号；
- 引用更好的源头；
- 作为事件扩散证据。

但普通 item 不再单独调用 LLM，只在特定条件下抽样或触发处理。

---

## 8. 人工治理与一致性保持

### 8.1 优先级规则

当系统判断冲突时，优先级为：

```text
human_verified
> deterministic_rule
> llm_pro_high_confidence
> llm_flash_high_confidence
> heuristic
```

### 8.2 必需治理操作

完成体至少应支持：

```text
merge-clusters
split-cluster
detach-item
reassign-item
mark-relation
approve-source-upgrade
approve-source-downgrade
disable-source-llm
enable-source-llm
rerun-item-semantic
rebuild-cluster-card
```

### 8.3 review_queue 场景

进入 review_queue 的场景：

- LLM 输出 `uncertain`；
- 多个候选 cluster 分数接近；
- source 升级 high；
- source 禁用 LLM；
- cluster merge/split 建议；
- follow-up ambiguity；
- prompt/model 升级对历史结果产生冲突；
- 用户手动标记问题。

### 8.4 语义漂移防护

机制：

1. schema validation；
2. prompt versioning；
3. input_fingerprint；
4. output logging；
5. confidence thresholds；
6. relation precedence；
7. periodic reindex；
8. cluster merge/split/detach；
9. review queue；
10. evaluation set。

---

## 9. CLI 与 API 完成体方向

### 9.1 CLI

建议命令族：

```text
semantic process --limit N
semantic process-item ITEM_ID
semantic backfill-cards --since DAYS
semantic show-item ITEM_ID
semantic show-relations ITEM_ID
semantic show-cluster CLUSTER_ID
semantic list-clusters --status active
semantic rebuild-cluster-card CLUSTER_ID
semantic show-source-profile SOURCE_ID
semantic recompute-source-profiles
semantic list-review
semantic approve-review REVIEW_ID
semantic reject-review REVIEW_ID
semantic merge-clusters A B
semantic detach-item ITEM_ID --cluster CLUSTER_ID
semantic reassign-item ITEM_ID --cluster CLUSTER_ID
```

### 9.2 API

未来 console 可使用：

```text
GET /api/semantic/items/{id}
GET /api/semantic/items/{id}/relations
GET /api/semantic/clusters
GET /api/semantic/clusters/{id}
GET /api/semantic/sources/{id}/profile
GET /api/semantic/review
POST /api/semantic/process
POST /api/semantic/review/{id}/approve
POST /api/semantic/review/{id}/reject
POST /api/semantic/clusters/{id}/rebuild-card
```

---

## 10. 验收指标

### 10.1 第二层

- 精确重复识别率；
- 近重复准确率；
- 误折叠率；
- `uncertain` 比例；
- LLM 调用比例；
- 平均每条 item token 消耗；
- 折叠后用户可见重复减少比例。

### 10.2 第三层

- cluster 纯度；
- 同事件召回率；
- 误聚类率；
- 错误新建 cluster 比例；
- follow-up 判断准确率；
- 代表内容选择质量；
- cluster_card 更新准确率。

### 10.3 LLM 调度

- source llm_yield；
- 高价值 item 命中率；
- 低价值源 LLM 调用下降比例；
- high priority source 的高价值产出比例；
- disabled_for_llm 源误伤率。

### 10.4 工程运行

- semantic pending 队列长度；
- LLM 调用失败率；
- JSON 解析失败率；
- 重试成功率；
- 平均处理延迟；
- review queue 积压量。

---

## 11. 完成体总结

完成体的核心不是“LLM 做分类”，而是建立一个长期自我改进的信息处理闭环：

```text
item 入库
  ↓
card 压缩
  ↓
embedding 召回
  ↓
LLM 判断 relation
  ↓
写回 cluster 与 source signal
  ↓
更新 source profile
  ↓
优化未来 LLM 调度
  ↓
人工治理纠偏
```

一句话总结：

> LLM 不只是判断信息，也帮助系统学会以后如何少调用 LLM、把 LLM 用在更值得的信息上。

---

## 附录 A：完成体的推荐落地原则

1. `inbox_items` 是事实层，不承载大量派生语义。
2. 所有 item 应至少拥有轻量 `item_card`。
3. 第二层处理 item-item relation，第三层处理 item-cluster relation。
4. relation 使用 `primary_relation + secondary_roles`。
5. cluster 是事件容器，不等于 topic。
6. source_profile 从 item-level signal 聚合，不让 LLM 直接给 source 终局评分。
7. LLM 输出必须 JSON 化、版本化、可审计。
8. 规则先行，embedding 召回，LLM 裁判。
9. Pro 模型只用于高价值、高风险、高不确定性任务。
10. 低价值源不停止抓取，但降低 LLM 调用优先级。
11. 所有高风险状态变化进入 review queue。
12. 必须提供 CLI 治理入口。

---

## 附录 B：Phase 1 落地补充（2026-05-16）

第一阶段实现采用“RSS ingest 先入库，semantic CLI/API 后处理”的方式。现有事实层 `inbox_items` 不承载大量 LLM 字段；LLM 派生结果进入 `item_cards`、`item_relations`、`cluster_items`、`cluster_cards`、`source_profiles`、`llm_call_logs` 和 `review_queue`。

DeepSeek 调用策略：

- 复用现有 OpenAI-compatible 配置和 key 读取方式；
- 语义 live 调用需显式开启 `CONTENT_INBOX_LLM_ENABLE_LIVE=1`；
- live smoke 默认写临时 SQLite DB；
- 写真实 DB 需要同时传入 `--db-path` 和 `--write-real-db`；
- 使用 `response_format={"type":"json_object"}`；
- 使用 Pydantic validation 和一次 JSON repair retry；
- 记录 prompt/schema version、model、input_fingerprint、token usage、cache token 字段（如 API 返回）、raw output、parsed JSON、错误和耗时。

第一阶段 relation enum 已收缩为：

- item-item: `duplicate`、`near_duplicate`、`related_with_new_info`、`different`、`uncertain`
- item-cluster: `source_material`、`repeat`、`new_info`、`analysis`、`experience`、`context`、`follow_up`、`same_topic`、`unrelated`、`uncertain`

`source_profile` 自动升降级不直接执行，只产生 `priority_suggestion` 和 `review_queue`。只有人工 approve 或 CLI `source set-priority` 会修改 `llm_priority`。
