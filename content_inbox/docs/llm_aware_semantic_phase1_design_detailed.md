# LLM-aware 语义处理第一阶段详细设计文档

> 适用项目：`information-center / content_inbox`  
> 文档定位：第一阶段实施设计  
> 本阶段目标：在不破坏现有 RSS 抓取和基础入库能力的前提下，完成 LLM-aware 语义层的第一版闭环。  
> 实施原则：本阶段功能范围有限，但每个进入范围的功能都要做完整、可运行、可测试、可通过 CLI 查看和治理。

---

## 0. 本阶段范围总览

用户确认的第一阶段范围：

```text
P0：保持当前 RSS 抓取和基础入库稳定
P1：所有 item 生成轻量 item_card
P2：第二层 item-item relation 可用
P3：第三层 item-cluster relation 可用
P4：cluster_card 可增量更新
P5：source_profile 只做基础统计和 LLM priority
```

架构选择：

```text
方案 B：先入库，后语义处理
```

数据分层选择：

```text
inbox_items 尽量保持稳定，作为事实层
cluster_items 存 item-cluster 关系
item_relations 存 item-item 关系
item_cards / cluster_cards 存派生语义
source_profiles 存信源长期统计与 LLM priority
```

模型选择：

```text
默认模型：deepseek-v4-flash
核心任务：deepseek-v4-flash
少量最核心 / 高价值 / 高不确定任务：deepseek-v4-pro
```

第一阶段可以对强模型使用稍微放宽，以观察效果，但必须保留调用日志、token 统计和后续降本空间。

---

## 1. 第一阶段设计目标

### 1.1 不是要做完整智能信息中心

本阶段不追求：

- 完整 topic 图谱；
- 完整 thread 系统；
- 自动生成研究报告；
- 高级前端审核台；
- 全量历史数据一次性高质量聚类；
- 完整信源发现网络；
- 完美代表内容选择。

本阶段要做的是：

> 建立可运行、可观测、可治理的语义处理骨架，并让第二层去重、第三层聚合、cluster_card、source_profile 形成闭环。

### 1.2 本阶段必须完成的能力

#### P0：RSS 抓取和入库稳定

- 不破坏现有 ingest 成功路径。
- 不改变旧 API 的基本行为。
- LLM 处理失败不影响 RSS 抓取。
- 原始 item 始终可入库。

#### P1：所有 item 生成轻量 item_card

- 新 item 入库后进入 semantic pending 队列。
- semantic worker 为每个 item 生成轻量 card。
- item_card 可重算、可版本化、可用作 embedding_text。
- 高价值 item 可升级为更完整 card，但不是 P1 必需。

#### P2：第二层 item-item relation 可用

- 基于规则 + embedding + LLM 判断新 item 与历史 item 的关系。
- 能写入 `item_relations`。
- 能折叠 exact / near / derived duplicate。
- 能保留 `same_event_new_info` 并送入第三层。
- 不物理删除任何 item。

#### P3：第三层 item-cluster relation 可用

- 能根据 item_card 查候选 cluster。
- 能用 LLM 判断 attach / create / uncertain。
- 能写入 `cluster_items`。
- 能新建 `event_clusters`。
- 能处理 follow-up event 和 same_topic_only 的边界。

#### P4：cluster_card 可增量更新

- 新 cluster 创建时生成初始 cluster_card。
- 当 item 提供新信息或高价值贡献时，patch cluster_card。
- duplicate_report 不应触发核心摘要更新。
- cluster_card 可通过 CLI 重建。

#### P5：source_profile 做基础统计和 LLM priority

- 记录 item-level source_signal。
- 聚合 source_profile。
- 计算 basic llm_yield_score。
- 根据规则建议 high / normal / low / disabled_for_llm / pending_review。
- 通过 CLI 查看和审核 source 状态变化。

---

## 2. 处理架构

### 2.1 采用异步 semantic pipeline

第一阶段采用：

```text
RSS 抓取 / item 入库
  ↓
semantic pending
  ↓
semantic worker
  ↓
item_card / item_relations / cluster_items / cluster_cards / source_profiles
```

禁止将 LLM 调用放在 RSS 抓取同步路径中。

原因：

1. RSS 抓取必须稳定；
2. LLM 有速率限制和失败可能；
3. semantic 处理需要重试；
4. 后续可批处理；
5. 历史数据可 backfill。

### 2.2 semantic_status

在 `inbox_items` 中可以增加少量状态字段，或用独立任务表记录。

推荐最小状态：

```text
semantic_status:
- pending
- processing
- processed
- skipped
- failed
```

可选字段：

```text
semantic_error
semantic_attempts
last_semantic_at
```

如果不希望改动 `inbox_items`，也可以用 `semantic_jobs` 表承载。

### 2.3 semantic worker 的基本流程

```text
1. 拉取 pending item
2. 确认该 item 是否已有 item_card
3. 没有则生成轻量 item_card
4. 规则硬去重
5. embedding 召回 candidate item
6. 第二层 LLM 判断 item-item relation
7. 如果不是折叠终点，embedding 召回 candidate cluster
8. 第三层 LLM 判断 item-cluster relation
9. 写回 cluster relation / 创建 cluster / 更新 cluster_card
10. 记录 source_signal
11. 定期或本轮结束后 recompute source_profile
```

---

## 3. 第一阶段数据表设计

> 本节是实施设计，不要求完全照搬字段名，但对象边界必须保持一致。

### 3.1 `item_cards`

定位：

> item 的轻量压缩语义卡片。

第一阶段 schema：

```text
item_cards
- id
- item_id
- card_version
- card_level               # light / full，第一阶段默认 light
- model                    # deepseek-v4-flash / rule / heuristic
- prompt_version
- input_fingerprint
- canonical_title
- language
- event_hint
- entities                 # JSON array
- content_role             # enum
- short_summary
- embedding_text
- confidence
- warnings                 # JSON array
- created_at
- updated_at
```

可选但推荐保留：

```text
key_facts                  # JSON array，可为空
key_opinions               # JSON array，可为空
cited_sources              # JSON array，可为空
```

第一阶段 `item_card` 的原则：

1. 所有新 item 都生成 light card；
2. light card 不追求完整事实抽取；
3. 必须能用于 embedding；
4. 必须能用于 LLM relation 判断；
5. 必须有 input_fingerprint，避免重复生成。

### 3.2 content_role 枚举

第一阶段使用：

```text
source_material
report
analysis
firsthand
commentary
aggregator
low_signal
unknown
```

说明：

| content_role | 含义 |
|---|---|
| `source_material` | 原始材料、官方公告、论文、release note、原始数据 |
| `report` | 新闻报道、事实转述 |
| `analysis` | 分析、解释、判断 |
| `firsthand` | 一手体验、实测、现场反馈 |
| `commentary` | 评论、立场、观点 |
| `aggregator` | 聚合、周报、导航 |
| `low_signal` | 低信息量、广告、重复摘要 |
| `unknown` | 无法判断 |

### 3.3 `item_relations`

定位：

> 第二层 item-item relation。

第一阶段 schema：

```text
item_relations
- id
- item_a_id                 # new item
- item_b_id                 # candidate historical item
- primary_relation
- secondary_roles           # JSON array
- confidence
- should_fold
- canonical_item_id
- new_information           # JSON array
- reason
- evidence                  # JSON array
- decision_source           # rule / llm_flash / llm_pro / human
- llm_call_id nullable
- prompt_version
- created_at
- updated_at
```

#### 3.3.1 primary_relation 枚举

第一阶段采用收缩版：

```text
exact_duplicate
near_duplicate
derived_duplicate
same_event_new_info
different
uncertain
```

解释：

| relation | 含义 | 默认动作 |
|---|---|---|
| `exact_duplicate` | 同 URL/GUID/hash/canonical URL 等确定重复 | 折叠 |
| `near_duplicate` | 高度近似重复，无明显新增 | 折叠 |
| `derived_duplicate` | 翻译、改写、摘要、搬运等派生重复 | 折叠 |
| `same_event_new_info` | 同一事件但有新增事实/分析/体验 | 保留并进入第三层 |
| `different` | 不重复，且不是同一事件 | 保留 |
| `uncertain` | 不确定 | 保留并进入 review queue |

#### 3.3.2 secondary_roles

第一阶段可选：

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

secondary_roles 用于解释 `derived_duplicate` 或补充细节，不参与主流程分支。

### 3.4 `event_clusters`

定位：

> 事件簇，代表一件具体事件。

第一阶段 schema：

```text
event_clusters
- id
- title
- status                  # active / cooling / archived / reopened / merged
- first_seen_at
- last_seen_at
- last_major_update_at
- item_count
- representative_item_id nullable
- source_material_item_id nullable
- cluster_card_id nullable
- created_by              # llm_flash / llm_pro / human / rule
- confidence
- merged_into_cluster_id nullable
- created_at
- updated_at
```

第一阶段可以暂不实现完整 topic/thread 表，但可保留关系扩展空间。

### 3.5 `cluster_items`

定位：

> 第三层 item-cluster relation。

第一阶段 schema：

```text
cluster_items
- id
- cluster_id
- item_id
- primary_relation
- secondary_roles          # JSON array
- same_event
- same_topic
- follow_up_event
- confidence
- incremental_value        # 0-5
- report_value             # 0-5
- should_update_cluster_card
- should_notify
- reason
- evidence                 # JSON array
- llm_call_id nullable
- decision_source
- created_at
- updated_at
```

#### 3.5.1 primary_relation 枚举

第一阶段采用收缩版：

```text
source_material
duplicate_report
new_info
interpretation
firsthand
follow_up_event
same_topic_only
unrelated
uncertain
```

说明：

| relation | 含义 | 默认动作 |
|---|---|---|
| `source_material` | 原始材料、官方来源、权威材料 | 挂 cluster，更新 card |
| `duplicate_report` | 重复报道或低增量转述 | 挂 cluster，不更新核心摘要 |
| `new_info` | 新事实、数据、背景补充 | 挂 cluster，视价值更新 card |
| `interpretation` | 分析、解释、观点、预测 | 挂 cluster，视价值更新 card |
| `firsthand` | 一手体验、实测、现场反馈 | 挂 cluster，更新或标记角度 |
| `follow_up_event` | 相关后续事件 | 通常新建 cluster 并关联 |
| `same_topic_only` | 同主题但非同一事件 | 不挂原 cluster 或仅建立弱关系 |
| `unrelated` | 无关 | 不挂 cluster |
| `uncertain` | 不确定 | review queue |

#### 3.5.2 secondary_roles

第一阶段可选：

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

### 3.6 `cluster_cards`

定位：

> cluster 的当前压缩语义状态。

第一阶段 schema：

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
- main_entities             # JSON array
- core_facts                # JSON array
- known_angles              # JSON array
- representative_items      # JSON array
- source_material_items     # JSON array
- open_questions            # JSON array
- first_seen_at
- last_major_update_at
- confidence
- created_at
- updated_at
```

第一阶段不要求完整 follow_up_clusters，但可以预留 JSON 字段或后续 cluster_relations。

### 3.7 `source_signals`

定位：

> 单条 item 对 source_profile 的增量信号。

Schema：

```text
source_signals
- id
- source_id
- item_id
- cluster_id nullable
- originality_delta         # -2..2
- duplicate_signal          # boolean
- incremental_value         # 0..5
- report_value              # 0..5
- firsthand_value           # 0..5
- citation_quality          # 0..5
- source_role               # source_material / reporter / analyst / firsthand / aggregator / repeater / unknown
- llm_call_id nullable
- created_at
```

### 3.8 `source_profiles`

定位：

> source 级长期画像与 LLM 调度优先级。

Schema：

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
- llm_priority              # new_source_under_evaluation / high / normal / low / disabled_for_llm / pending_review
- review_status             # none / pending_upgrade / pending_downgrade / pending_disable / approved
- last_reviewed_at nullable
- updated_at
```

### 3.9 `llm_call_logs`

定位：

> 所有 LLM 调用的审计记录。

Schema：

```text
llm_call_logs
- id
- task_type
- model
- prompt_version
- schema_version
- input_fingerprint
- input_token_estimate
- output_token_estimate
- cost_estimate nullable
- latency_ms nullable
- status                  # success / failed / parse_failed / timeout
- raw_output
- parsed_output
- error
- item_id nullable
- cluster_id nullable
- source_id nullable
- created_at
```

### 3.10 `review_queue`

定位：

> 人工审核队列。

Schema：

```text
review_queue
- id
- review_type
- target_type              # item_relation / cluster_relation / cluster / source_profile
- target_id
- reason
- suggested_action
- payload
- status                   # pending / approved / rejected / resolved
- created_at
- resolved_at nullable
```

---

## 4. LLM Prompt 设计原则

第一阶段提示词要精心设计。每个任务一个 prompt，不要混合过多目标。

### 4.1 共同原则

所有 prompt 必须：

1. 明确任务边界；
2. 强制 JSON 输出；
3. 明确枚举值；
4. 明确“不要删除 item”；
5. 明确“同事件不等于重复，同主题不等于同事件”；
6. 要求输出 `confidence` 和 `reason`；
7. 要求不确定时输出 `uncertain`；
8. 使用固定字段顺序；
9. 提供简短 JSON 示例；
10. 限制输出长度。

### 4.2 Prompt 1：轻量 item_card 生成

输入：

```text
title
url
source_name
published_at
raw_summary
raw_content excerpt
```

输出：

```json
{
  "canonical_title": "...",
  "language": "zh",
  "event_hint": "...",
  "entities": [],
  "content_role": "report",
  "short_summary": "...",
  "embedding_text": "...",
  "confidence": 0.0,
  "warnings": []
}
```

要求：

- `embedding_text` 应短而稳定；
- 不要编造未出现事实；
- 如果信息不足，warnings 添加 `content_too_short`；
- `short_summary` 控制在较短长度。

### 4.3 Prompt 2：第二层 item-item relation batch

输入：

```json
{
  "new_item_card": {},
  "candidate_item_cards": [],
  "hard_signals": {}
}
```

输出：

```json
{
  "relations": [
    {
      "candidate_item_id": "...",
      "primary_relation": "exact_duplicate | near_duplicate | derived_duplicate | same_event_new_info | different | uncertain",
      "secondary_roles": [],
      "confidence": 0.0,
      "should_fold": false,
      "canonical_item_id": null,
      "new_information": [],
      "reason": "...",
      "evidence": []
    }
  ],
  "best_relation": {
    "candidate_item_id": "...",
    "primary_relation": "...",
    "confidence": 0.0
  }
}
```

关键规则：

- `same_event_new_info` 不折叠；
- `derived_duplicate` 可使用 secondary_roles 解释；
- 不确定时输出 `uncertain`；
- 不允许输出未定义枚举。

### 4.4 Prompt 3：第三层 item-cluster relation batch

输入：

```json
{
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
  "action": "attach_to_cluster | create_new_cluster | uncertain",
  "cluster_id": null,
  "primary_relation": "source_material | duplicate_report | new_info | interpretation | firsthand | follow_up_event | same_topic_only | unrelated | uncertain",
  "secondary_roles": [],
  "same_event": false,
  "same_topic": false,
  "follow_up_event": false,
  "confidence": 0.0,
  "incremental_value": 0,
  "report_value": 0,
  "should_update_cluster_card": false,
  "should_notify": false,
  "new_facts": [],
  "new_angles": [],
  "reason": "...",
  "evidence": []
}
```

关键规则：

- same_topic_only 不能挂入原 cluster 作为同事件；
- follow_up_event 通常新建 cluster 并建立关联；
- duplicate_report 通常不更新 core_facts；
- new_info/source_material/firsthand 高价值时更新 cluster_card；
- 不确定时进入 review_queue。

### 4.5 Prompt 4：cluster_card patch

输入：

```json
{
  "old_cluster_card": {},
  "new_item_card": {},
  "cluster_relation": {}
}
```

输出：

```json
{
  "patch_type": "no_update | incremental_patch | rebuild_recommended",
  "updated_fields": {
    "cluster_title": null,
    "core_facts_add": [],
    "known_angles_add": [],
    "representative_items_add": [],
    "source_material_items_add": [],
    "open_questions_add": []
  },
  "reason": "...",
  "confidence": 0.0
}
```

规则：

- duplicate_report 通常 `no_update`；
- new_info/source_material/firsthand 可 patch；
- 如果旧 card 与新事实冲突，输出 `rebuild_recommended`。

### 4.6 Prompt 5：source review suggestion

输入：

```json
{
  "source_profile": {},
  "recent_source_signals": [],
  "recent_relations_summary": {}
}
```

输出：

```json
{
  "suggested_priority": "high | normal | low | disabled_for_llm | pending_review",
  "review_required": true,
  "reason": "...",
  "evidence": [],
  "risk": "low | medium | high"
}
```

该 prompt 用于 source 升降级建议，不应直接自动执行高风险状态变化。

---

## 5. LLM 调用次数收敛策略

### 5.1 基本策略

1. 规则命中不调用 LLM。
2. 所有 LLM 调用尽量基于 card，不读全文。
3. 第二层和第三层都采用 batch candidates。
4. Flash 默认处理核心任务。
5. Pro 只用于高价值、高风险、高不确定性场景。
6. 使用 input_fingerprint 防止重复调用。
7. 使用 relation cache 避免重复判断。
8. 使用 source_profile 降低低收益源调用频率。
9. 对低优先级源做抽样复检，而不是完全永久禁用。
10. cluster_card 采用增量 patch，不每次全量重写。

### 5.2 一次调用放入多个候选

这是第一阶段必须实现或预留的 trick。

第二层：

```text
new item + top 3-5 candidate item_cards
```

第三层：

```text
new item + top 3 candidate cluster_cards
每个 cluster 放 1-3 个 representative_item_cards
```

好处：

- 减少 API 调用次数；
- 让模型在候选之间比较；
- 提高 best_relation / best_cluster 的判断质量；
- 更利于 context caching。

风险：

- 输入过长；
- 候选过多导致模型分心；
- JSON 输出更复杂。

控制：

- candidate 数量可配置；
- 输入过长时降级为 top 1-2；
- 输出必须 schema validation；
- 失败时拆分重试。

### 5.3 token 强度估计

| 阶段 | Token 强度 |
|---|---|
| RSS 入库 | 无/极低 |
| URL/GUID/hash 去重 | 极低 |
| item_card light | 低 |
| embedding 召回 | 低 |
| 第二层 relation batch | 中 |
| 第二层疑难/跨语言 | 高 |
| 第三层 cluster relation | 中~高 |
| cluster_card patch | 中 |
| cluster_card rebuild | 高 |
| source_profile 聚合 | 极低 |
| source review report | 中~高 |
| CLI 查询 | 极低 |

---

## 6. Cluster 生命周期第一阶段实现

### 6.1 状态

第一阶段实现：

```text
active
cooling
archived
reopened
merged
```

### 6.2 状态转换

默认规则：

```text
active → cooling:
  最近 7 天无 new_info/source_material/firsthand/高价值 interpretation

cooling → archived:
  最近 30 天无重大新增

archived → reopened:
  新 item 被高置信判断为同事件重大后续，或人工触发

any → merged:
  人工 merge 或高置信 merge 建议通过审核
```

第一阶段可以将自动状态转换做成 CLI 或 batch job：

```text
semantic update-cluster-statuses
```

### 6.3 archived cluster 是否参与召回

默认：

- active/cooling 参与常规召回；
- archived 只在相似度很高或 source 高价值时参与；
- merged 不参与召回，指向 merged_into_cluster_id。

### 6.4 follow-up event 边界细化

判断为 `follow_up_event` 的条件：

1. 与候选 cluster 有明确因果或延续关系；
2. 但有新的时间点、动作或状态变化；
3. 新 item 不是单纯报道/分析原事件；
4. 直接并入原 cluster 会污染 core_facts；
5. 更适合作为新 cluster，并通过 cluster_relation 关联。

第一阶段如果尚未实现 `cluster_relations` 表，可以：

- 新建 cluster；
- 在 new cluster 的 card 或 metadata 中记录 `related_cluster_id`；
- review_queue 中记录 follow-up 建议。

---

## 7. Source Profile 第一阶段实现

### 7.1 source_signal 产生时机

每次 LLM 完成第二层或第三层判断后，尽量生成 source_signal：

- 如果 item 是 duplicate/derived，duplicate_signal = true；
- 如果 item 是 same_event_new_info / new_info / firsthand / source_material，则 incremental/report/firsthand 评分较高；
- 如果 item 成为 representative/source_material，则 source profile 后续加权。

### 7.2 source_profile 聚合任务

提供 CLI：

```text
semantic recompute-source-profiles
```

或在每轮 semantic batch 后自动聚合本轮受影响 source。

### 7.3 llm_yield_score 初版

可先用简单公式：

```text
llm_yield_score =
  0.35 * normalized(incremental_value_avg)
+ 0.25 * normalized(report_value_avg)
+ 0.20 * representative_item_rate
+ 0.10 * source_material_rate
+ 0.10 * firsthand_value_avg_normalized
- 0.25 * duplicate_rate
```

第一阶段不要求公式完美，但必须：

1. 可配置；
2. 可解释；
3. CLI 可展示组成项；
4. 不要只依赖 LLM 主观评分。

### 7.4 自动升降级规则

#### high 建议

条件示例：

```text
llm_processed_items >= 10
llm_yield_score >= 0.70
incremental_value_avg >= 3.5
duplicate_rate <= 0.35
```

动作：

```text
review_status = pending_upgrade
review_queue 创建 source_upgrade
```

#### low 建议

```text
llm_processed_items >= 20
llm_yield_score <= 0.30
duplicate_rate >= 0.65
incremental_value_avg <= 1.5
```

动作：

```text
review_status = pending_downgrade
```

#### disabled_for_llm 建议

```text
llm_processed_items >= 50
llm_yield_score <= 0.20
duplicate_rate >= 0.80
连续多轮无高价值输出
```

动作：

```text
review_status = pending_disable
必须人工批准
```

### 7.5 CLI 审核能力

必须实现：

```text
semantic list-source-profiles
semantic show-source-profile SOURCE_ID
semantic list-source-reviews
semantic approve-source-upgrade REVIEW_ID
semantic approve-source-downgrade REVIEW_ID
semantic approve-source-disable REVIEW_ID
semantic reject-source-review REVIEW_ID
semantic set-source-llm-priority SOURCE_ID high|normal|low|disabled_for_llm
```

---

## 8. CLI 第一阶段需求

### 8.1 处理类

```text
semantic process --limit N
semantic process-item ITEM_ID
semantic backfill-cards --limit N
semantic retry-failed --limit N
```

### 8.2 查询类

```text
semantic show-item-card ITEM_ID
semantic show-item-relations ITEM_ID
semantic show-cluster CLUSTER_ID
semantic list-clusters --status active
semantic show-source-profile SOURCE_ID
semantic list-review
```

### 8.3 治理类

```text
semantic rebuild-cluster-card CLUSTER_ID
semantic merge-clusters CLUSTER_A CLUSTER_B
semantic detach-item ITEM_ID --cluster CLUSTER_ID
semantic reassign-item ITEM_ID --cluster CLUSTER_ID
semantic mark-item-relation ITEM_A ITEM_B RELATION
semantic update-cluster-statuses
```

### 8.4 source_profile 类

见上一节。

### 8.5 输出要求

CLI 输出应能直接辅助判断：

- relation 是什么；
- 置信度多少；
- 为什么这么判断；
- 是否调用了 LLM；
- 使用了哪个模型；
- source 当前优先级；
- 是否需要人工审核。

---

## 9. Console 前端参考方向

用户已在原项目中加入有前端的 console，虽然不完善。本阶段后端设计应为 console 提供基础数据。

优先支持的 API/数据能力：

1. 查看 item_card；
2. 查看 item 的重复关系；
3. 查看 item 所属 cluster；
4. 查看 cluster_card；
5. 查看 cluster 下 item 列表与 relation；
6. 查看 source_profile；
7. 查看 review_queue；
8. 批准/拒绝 source 升降级；
9. 执行 cluster rebuild 或 item reassign。

本阶段不强制完成高级 UI，但 API/CLI 输出应考虑 console 复用。

---

## 10. 测试与验收

### 10.1 单元测试

必须覆盖：

- item_card schema validation；
- item_relation enum validation；
- cluster_relation enum validation；
- source_profile 公式；
- cluster lifecycle 状态转换；
- LLM JSON parse failure；
- prompt output validation；
- relation 行为映射。

### 10.2 集成测试

至少覆盖：

1. 新 item 入库后生成 item_card；
2. same_url 命中 exact_duplicate，不调用 LLM；
3. 相似 item 调用第二层 LLM，写入 item_relations；
4. same_event_new_info 进入第三层；
5. 第三层 create_new_cluster；
6. 第三层 attach_to_cluster；
7. duplicate_report 不更新 cluster_card；
8. new_info 更新 cluster_card；
9. source_profile 聚合；
10. source 降级建议进入 review_queue；
11. CLI 能查看 source_profile；
12. LLM 失败不影响 item 入库。

### 10.3 回归测试样本

建议构造测试 fixtures：

#### 第二层样本

- 同 URL 重复；
- GUID 重复；
- URL 参数不同但 canonical 相同；
- 中文翻译英文原文；
- 改写但无新增；
- 摘要型重复；
- 同事件但有新增事实；
- 同主题不同事件；
- 不确定短文本。

#### 第三层样本

- 官方公告 + 多媒体转述；
- 官方公告 + 开发者实测；
- 原事件 + 后续故障；
- 同主题不同公司发布；
- 背景补充；
- 观点评论；
- 一手体验；
- source_material。

### 10.4 验收标准

本阶段完成后应满足：

1. 现有 RSS 抓取测试全部通过；
2. 所有新 item 可进入 semantic pending；
3. 所有 processed item 有 item_card；
4. item_relations 可写入并查询；
5. event_clusters 可创建；
6. cluster_items 可写入并查询；
7. cluster_card 可创建和 patch；
8. source_profile 可聚合；
9. source priority 可通过 CLI 查看和修改；
10. LLM 调用日志完整；
11. 失败可重试；
12. CLI 可完成基本治理操作；
13. 文档更新完整。

---

## 11. 第一阶段实现顺序建议

### Step 1：数据库迁移

新增表：

```text
item_cards
item_relations
event_clusters
cluster_items
cluster_cards
source_signals
source_profiles
llm_call_logs
review_queue
```

尽量不破坏旧表。

### Step 2：语义配置

新增配置项：

```text
DEEPSEEK_API_KEY
DEEPSEEK_BASE_URL
DEEPSEEK_MODEL_FLASH=deepseek-v4-flash
DEEPSEEK_MODEL_PRO=deepseek-v4-pro
SEMANTIC_LLM_ENABLED
SEMANTIC_MAX_CANDIDATE_ITEMS
SEMANTIC_MAX_CANDIDATE_CLUSTERS
SEMANTIC_USE_PRO_FOR_HIGH_VALUE
```

密钥使用项目当前已有位置，不硬编码。

### Step 3：LLM client 与 JSON validation

- OpenAI-compatible client；
- JSON output；
- retry；
- timeout；
- call log；
- parse validation。

### Step 4：item_card 生成

- rule fallback；
- flash model；
- input_fingerprint；
- schema validation；
- embedding_text。

### Step 5：embedding / 候选召回

如果当前已有 embedding 能力则复用。若没有，先用简单文本相似度/SQLite 查询作为 fallback，并保留向量接口。

### Step 6：第二层 relation

- 规则 exact_duplicate；
- candidate item 检索；
- LLM batch；
- item_relations 写入；
- 行为映射。

### Step 7：第三层 cluster

- candidate cluster 检索；
- LLM batch；
- create/attach/uncertain；
- cluster_items 写入；
- event_clusters 创建。

### Step 8：cluster_card

- 创建初始 card；
- patch card；
- rebuild CLI。

### Step 9：source_profile

- source_signal；
- profile 聚合；
- priority 建议；
- review queue。

### Step 10：CLI 与测试

- 查询；
- 处理；
- 治理；
- source 审核；
- 回归测试。

---

## 12. 第一阶段完成后的系统状态

完成后，系统应达到：

```text
RSS 信息稳定入库
  ↓
每条 item 有轻量语义卡片
  ↓
相似 item 能被识别为重复/近重复/派生重复/同事件新增
  ↓
同事件 item 能被挂到事件簇
  ↓
事件簇有可更新的 cluster_card
  ↓
信源有基础画像和 LLM priority
  ↓
CLI 可查看、处理、审核、修正
```

这意味着第一阶段不只是“跑了几个 LLM prompt”，而是搭起了后续信息价值评分、代表内容选择、潜在信源发现、报告生成的基础语义骨架。

---

## 附录 A：本阶段不做但必须预留的能力

1. 完整 topic 系统；
2. 完整 thread 表；
3. 高级 source discovery；
4. 自动报告生成；
5. 高级前端审核台；
6. 复杂图谱；
7. 全量历史事件重建；
8. 多模型评测框架；
9. 代表内容自动排序的完整版本；
10. 跨渠道消息统一。

---

## 附录 B：最重要的实现提醒

1. 不要把 LLM 同步塞进 RSS ingest。
2. 不要把大量派生字段塞进 `inbox_items`。
3. 不要物理删除重复 item。
4. 不要让 LLM 输出自由文本作为最终结构。
5. 不要让 source 自动禁用 LLM 而无审核。
6. 不要把 same_topic 当 same_event。
7. 不要把 follow_up_event 粗暴塞进原 cluster。
8. 不要每加入一条 item 就全量重写 cluster_card。
9. 不要丢失 llm_call_logs。
10. 不要只做代码，不补文档和测试。

---

## 附录 C：Phase 1 实现说明（2026-05-16）

实际实现采用 `app/semantic/` 作为后端实现目录，并通过 `python -m content_inbox.semantic` 暴露 CLI。现有 RSS ingest、screening、embedding clusterer 和 console UI 均保持兼容；语义层是后处理管线。

item-item `primary_relation` 为 `duplicate`、`near_duplicate`、`related_with_new_info`、`different`、`uncertain`。item-cluster `primary_relation` 为 `source_material`、`repeat`、`new_info`、`analysis`、`experience`、`context`、`follow_up`、`same_topic`、`unrelated`、`uncertain`。

所有 relation 都采用 `primary_relation` 单选、`secondary_roles` 多选。`primary_relation` 控制流程分支；`secondary_roles` 只用于补充标注、source_signal、展示和统计。

迁移在 `app/storage.py::InboxStore.init_schema()` 中幂等执行。现有 `event_clusters` 作为 canonical cluster 表被扩展，没有替换；新增表包括 `item_cards`、`item_relations`、`cluster_items`、`cluster_cards`、`cluster_relations`、`source_signals`、`source_profiles`、`llm_call_logs`、`review_queue`。

`inbox_items` 仅新增轻量字段：`semantic_status`、`primary_cluster_id`、`semantic_error`、`semantic_attempts`、`last_semantic_at`。

DeepSeek 调用采用 JSON Output、Pydantic validation、一次 JSON repair retry；第一阶段未强制 tool-calls strict mode。Live smoke 默认写临时 SQLite DB。只有同时传入 `--db-path` 和 `--write-real-db` 才写指定真实 DB。

本阶段没有修改 console UI、模板、样式或交互。新增后端 API 使用 `/api/semantic/*`，供未来 console 接入。
