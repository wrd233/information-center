# 去重与事件聚合模块全量改进说明书

生成日期: 2026-05-31

## 目标

本说明书定义 `content_inbox` 去重与事件聚合能力的目标架构、改造范围、数据模型、处理流程、API/console 接入、迁移策略和验收标准。

目标不是重写整个系统，而是在现有能力上形成一条可解释、可回放、可评估的事件处理链路：

```text
item normalization
  -> item dedupe
  -> eventness classification
  -> event signature extraction
  -> candidate generation
  -> relation decision
  -> cluster materialization
  -> event object generation
  -> review / briefing / report
```

## 设计原则

### 高精度优先

自动合并错误的成本高于漏合并。系统应优先保证 auto-merge precision，召回不足可以通过 review 队列和人工确认补足。

建议策略：

- `auto_merge`: only high-confidence same-event
- `review`: medium/uncertain/same-topic
- `reject`: digest/generic/low-signal/non-event

### 去重和聚合分层

Item 去重解决“同一内容是否重复出现”。事件聚合解决“不同内容是否描述同一现实事件”。两者的数据结构和指标应分开。

### 证据链优先

每个 dedupe group、cluster item、event relation 都必须能回答：

- 为什么合并？
- 哪些字段命中？
- 哪些负特征被检查？
- 谁做的决定：rule、embedding、LLM、human？
- 置信度是多少？

### 可回放

任何聚合结果都应可由输入 item、signature、candidate features、decision payload 重算。避免只留下 event summary 而丢失证据链。

### 渐进迁移

默认大库中存在 legacy cluster。新逻辑应优先写新 schema 或新字段，不破坏旧数据。旧 cluster 可在后续 migration/rebuild 中逐步补证据。

## 术语

| 术语 | 定义 |
|---|---|
| item | 一条摄入内容，如 RSS entry 或手动内容 |
| item duplicate | 同一 URL/GUID/同源同标题日期等导致的重复 item |
| event | 一个现实世界发生的事情 |
| eventness | item 是否适合形成 event 的判断 |
| event signature | 事件身份签名，通常由 actor/product/action/time 组成 |
| candidate pair | 可能有关联的两个 item 或 item-cluster |
| relation decision | 对候选 pair 的关系判断 |
| event cluster | 描述同一现实事件的一组 item |
| source material | 事件源头或高价值一手材料 |
| repeat | 重复报道或重复转发 |
| new_info | 同一事件的新事实 |
| same_topic | 同主题但不是同一事件 |

## 当前需要替换的模块边界

### 保留

- `normalize_content()`
- `build_dedupe_key()`
- `InboxStore.insert()`
- `mark_seen_with_latest()`
- `seen_count` / `latest_raw_json`
- `app.semantic.signatures.extract_event_signature()`
- `app.semantic.candidates.assess_candidate()`
- `review_queue` 基础表

### 改造

- `run_dedupe_stage()`
- `generate_information_objects()`
- `/api/runs/{run_id}/pipeline/{stage}` 的 stage 语义
- `events` 生成逻辑
- `briefings/reports` 对 event 的消费方式

### 避免继续扩张

- 不再把 `normalized_title(title)` 作为事件聚合主键。
- 不再为每个 item 无条件创建 event。
- 不再让 event summary 只是模板句。
- 不再把 medium candidate 自动合并。

## 目标数据模型

### Dedupe 层

现有表：

- `inbox_items`
- `dedupe_groups`
- `dedupe_group_items`

建议增强字段或 payload：

`dedupe_groups.evidence_json`：

```json
{
  "dedupe_key": "...",
  "method": "url|guid|title_date|title_content|manual",
  "canonical_item_id": "item_x",
  "seen_count": 5,
  "source_count": 3,
  "url_variants": [],
  "guid_variants": [],
  "first_seen_at": "...",
  "last_seen_at": "..."
}
```

`dedupe_group_items.role`：

- `canonical`
- `same_url`
- `same_guid`
- `same_title_date`
- `same_content_hash`
- `manual_duplicate`

关键点：即使写入阶段已经折叠重复，也要能从 `seen_count/latest_raw_json/item_run_links` 构造 dedupe explanation。

### Eventness 层

建议新增或复用 `semantic_extractions.normalized_output_json`，包含：

```json
{
  "eventness": {
    "decision": "event|thread|content|digest|low_signal|ad|unknown",
    "confidence": 0.0,
    "reasons": [],
    "negative_features": []
  }
}
```

事件资格建议枚举：

- `event`: 可建 event
- `thread`: 同主题线索，可入 topic/review
- `content`: 教程/观点/案例，不自动建 event
- `digest`: 日报/周报/roundup/market wrap，不自动建 event
- `low_signal`: 短标题、纯 emoji、纯链接、无事实
- `ad`: 广告/促销/垃圾内容

### Event Signature 层

建议结构：

```json
{
  "actor": "OpenAI",
  "actor_aliases": ["OpenAI/Codex"],
  "product_or_object": "GPT-5.5",
  "product_aliases": ["GPT 5.5", "GPT-5.5 Pro"],
  "action": "release",
  "time_bucket": "2026-05-30",
  "source_type": "media|official|social|paper|unknown",
  "signature_key": "openai|gpt55|release|2026-05-30",
  "confidence": 0.82,
  "invalid_reasons": []
}
```

Action 最小集合：

- `release`
- `feature_update`
- `availability`
- `pricing`
- `funding`
- `partnership`
- `policy`
- `security`
- `benchmark`
- `earnings`
- `market`
- `research_paper`
- `event`
- `company_launch`
- `integration`
- `other`

### Candidate 层

建议新增表：

```sql
CREATE TABLE event_candidate_pairs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id TEXT,
  item_a_id TEXT NOT NULL,
  item_b_id TEXT,
  candidate_cluster_id TEXT,
  candidate_score REAL NOT NULL,
  candidate_priority TEXT NOT NULL,
  lane TEXT NOT NULL,
  features_json TEXT NOT NULL DEFAULT '{}',
  disqualifiers_json TEXT NOT NULL DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'generated',
  created_at TEXT NOT NULL
);
```

候选优先级：

- `must_run`: 确定性重复或 exact signature
- `high`: 高置信同事件候选
- `medium`: 进入 review 或 LLM
- `low`: 只记录，不进入自动合并
- `suppress`: 不进入后续

### Relation 层

建议 relation_type：

- `item_duplicate`
- `near_duplicate`
- `same_event_repeat`
- `same_event_new_info`
- `same_event_new_angle`
- `same_topic_different_event`
- `same_product_different_event`
- `follow_up_event`
- `thread_only`
- `non_event`
- `different`
- `uncertain`

建议新增或扩展 `item_relations` / `cluster_items` payload：

```json
{
  "relation_type": "same_event_new_info",
  "same_event": true,
  "same_topic": true,
  "confidence": 0.91,
  "decision_source": "rule|llm|human",
  "positive_features": [],
  "negative_features": [],
  "new_facts": [],
  "evidence": [],
  "llm_call_id": null,
  "review_required": false
}
```

### Event Cluster 层

`event_clusters` 应表示“事件集合”，不是任意相似内容集合。

建议字段语义：

- `cluster_title`: 事件标题，不是第一条 item title
- `cluster_summary`: 事件摘要，必须具体
- `entities_json`: actor/product/object/topic
- `representative_item_id`: 最有代表性的 source material
- `item_count`: cluster_items 计数
- `created_by`: rule/llm/human/migrated
- `confidence`: 聚合置信度
- `status`: active/cooling/archived/needs_review/merged

### Event Object 层

`events` 应由 event cluster materialize 而来。

建议字段：

- `event_title`
- `event_summary`
- `event_type`
- `event_time`
- `status`
- `importance`
- `confidence`
- `primary_cluster_id`
- `evidence_json`

`evidence_json` 示例：

```json
{
  "source_item_count": 4,
  "source_count": 3,
  "representative_items": [],
  "new_facts": [],
  "relation_summary": {
    "repeat": 2,
    "new_info": 1,
    "source_material": 1
  },
  "decision_trace": []
}
```

## 目标处理流程

### Stage 1: Item Dedupe

输入：normalized item

处理：

1. 构造 dedupe key。
2. 查 `inbox_items.dedupe_key`。
3. 命中则更新 seen_count 和 latest_raw。
4. 未命中则插入 item。
5. 记录 dedupe decision。

输出：

- `ProcessResult`
- dedupe explanation

### Stage 2: Dedupe Explanation

输入：run_id 或 item_ids

处理：

1. 从 `inbox_items` 读取 seen_count。
2. 从 `item_run_links` 和 latest_raw 中提取 source/run 证据。
3. 写 `dedupe_groups` 和 `dedupe_group_items`。

目标：即使重复已被折叠，也能形成解释性 dedupe group。

### Stage 3: Eventness Classification

输入：item

规则特征：

- 标题长度
- 是否纯链接/emoji
- source category
- digest/newsletter/roundup/market wrap 关键词
- tutorial/opinion/case study 关键词
- adult/spam/ad 关键词
- value_score/personal_relevance
- source quality

输出：

- eventness decision
- confidence
- negative features

非 `event` 不自动进入 event cluster。

### Stage 4: Event Signature

输入：event-like item

处理：

1. 抽取 actor。
2. 抽取 product/object。
3. 抽取 action。
4. 归一化 alias。
5. 构造 date/time bucket。
6. 生成 signature key。

Signature exact 只作为高精度 seed，不作为唯一聚合依据。

### Stage 5: Candidate Generation

候选来源：

- exact signature group
- actor/product/action/time bucket 相近
- same actor + same product + title similarity
- same URL/GUID duplicate
- existing cluster representative item
- source diversity
- recency window

候选过滤：

- generic title
- digest/roundup
- same source boilerplate
- wide time window
- only generic entity overlap
- low signal

### Stage 6: Relation Decision

Rule fast path：

- same URL/GUID -> item_duplicate
- exact signature + non-generic -> same_event_repeat/new_info
- actor+product+action+time close + high title/entity evidence -> high candidate
- digest/generic -> non_event/different

LLM path：

- 只处理 medium/high-uncertain。
- 输入结构化 evidence，不直接丢全文。
- 输出必须符合 schema。

Human path：

- medium/uncertain 写入 review_queue。
- 人工结果应可回写 relation 和 cluster。

### Stage 7: Cluster Materialization

处理：

1. 如果 relation 是 auto-merge same_event，则 attach 到 existing cluster。
2. 如果是 new event，则 create cluster。
3. 如果 same_topic 或 uncertain，则 review。
4. 如果 non_event，则不建 event。
5. 更新 cluster_card。
6. 写 source_signal。

### Stage 8: Event Generation

从 cluster materialize event：

1. 生成 event_type。
2. 生成 event_title。
3. 生成具体 event_summary。
4. 汇总 evidence。
5. 计算 importance。
6. 计算 confidence。
7. 写 review_queue 或 ready status。

## API 和 Console 改造

### API

建议新增或增强：

- `POST /api/runs/{run_id}/pipeline/dedupe`
- `POST /api/runs/{run_id}/pipeline/eventness`
- `POST /api/runs/{run_id}/pipeline/signatures`
- `POST /api/runs/{run_id}/pipeline/candidates`
- `POST /api/runs/{run_id}/pipeline/relations`
- `POST /api/runs/{run_id}/pipeline/clusters`
- `POST /api/runs/{run_id}/pipeline/events`
- `GET /api/events/{event_id}/evidence`
- `GET /api/clusters/{cluster_id}/explain`
- `POST /api/review-queue/{id}/apply`

### Console

Run detail 页面应展示：

- item dedupe summary
- eventness stats
- signature stats
- candidate counts by priority
- auto-merged count
- review-required count
- rejected non-event count

Cluster detail 页面应展示：

- cluster title/summary/type/confidence
- member items
- relation per item
- positive evidence
- negative evidence
- source diversity
- new facts
- decision source

Review queue 页面应支持：

- confirm same event
- mark same topic
- mark non-event
- split cluster
- merge clusters
- set representative item

## Alias 和 Normalization

需要引入可配置 alias registry。

### Actor alias

示例：

```yaml
actors:
  openai:
    canonical: OpenAI
    aliases: [OpenAI/Codex, ChatGPT, Codex]
  deepseek:
    canonical: DeepSeek
    aliases: [深度求索, DeepSeek AI]
  european_commission:
    canonical: European Commission
    aliases: [EU Commission, 欧盟委员会, EU]
```

### Product alias

```yaml
products:
  gpt_5_5:
    canonical: GPT-5.5
    aliases: [GPT 5.5, GPT5.5, GPT-5.5 Pro]
    owner: OpenAI
  deepseek_v4_1:
    canonical: DeepSeek V4.1
    aliases: [DeepSeek-V4.1, 深度求索 V4.1]
    owner: DeepSeek
```

### Action alias

```yaml
actions:
  release:
    aliases: [launch, launched, released, rollout, 发布, 推出, 上线]
  funding:
    aliases: [raises, raised, financing, round, 融资, 投资]
```

## 迁移策略

### 只读盘点

先跑只读统计：

- cluster count
- cluster_items coverage
- event_type coverage
- signature scan
- seen_count distribution

### 新旧并存

新增 pipeline 输出应标记：

- `schema_version`
- `decision_source`
- `created_by`
- `input_fingerprint`

不要覆盖 legacy cluster。

### Rebuild 模式

提供 dry-run rebuild：

```bash
PYTHONPATH=. python -m app.semantic.cli rebuild-events --dry-run --limit 500
```

输出：

- would_create_clusters
- would_merge_items
- would_reject_non_events
- would_review
- quality metrics

### Commit 模式

真实写入必须：

- 指定 Fresh DB
- 生成 backup
- 记录 audit
- 支持 rollback by run_id

## 阶段计划

### Phase 1: Dedupe Explanation 和 Eventness

范围：

- 增强 dedupe stage，基于 seen_count 和 item_run_links 生成解释。
- 引入 eventness classifier。
- 阻止 digest/generic/low-signal 自动创建 event。

验收：

- dedupe explanation 覆盖 seen_count > 1 的 item。
- 非事件自动建 event 比率显著下降。
- eventness precision >= 0.90。

### Phase 2: Signature 接入

范围：

- 将 `extract_event_signature()` 接入 console pipeline。
- 引入 alias config。
- exact signature 自动 seed cluster。
- signature failure 写 review 或 diagnostic。

验收：

- exact signature auto-merge precision >= 0.98。
- multi_signature_groups 可 materialize 成 cluster_items。
- event_type known rate >= 0.60。

### Phase 3: Candidate 和 Relation

范围：

- 接入 `assess_candidate()`。
- high 自动合并，medium review。
- hard negative 规则。
- relation decision 写入 evidence。

验收：

- auto-merge precision >= 0.95。
- same-event pair F1 >= 0.75。
- digest/generic false positive <= 2%。

### Phase 4: Event Object 和 Review UI

范围：

- 事件摘要模板。
- evidence 展示。
- review apply。
- cluster split/merge。

验收：

- event summary specific rate >= 0.85。
- event_type known rate >= 0.80。
- review queue item 可一键应用决策。

### Phase 5: Briefing/Report 升级

范围：

- briefing/report 从 event cluster card 生成。
- 展示新增事实、来源数量、待审核风险。
- 输出质量评分进入测试。

验收：

- briefing quality score >= 0.85。
- report quality score >= 0.80。

## 风险与控制

| 风险 | 控制 |
|---|---|
| 自动误合并 | auto-merge 高精度门槛，medium 入 review |
| 召回不足 | review 和 LLM path 补召回 |
| 旧数据污染 | legacy 不覆盖，先 dry-run rebuild |
| LLM 成本 | 只对 uncertain candidate 调用 |
| Alias 维护成本 | 配置化，失败样例驱动更新 |
| 成人/垃圾内容污染事件 | source/content quality gate |
| 事件过碎 | signature + candidate recall |
| 事件过粗 | hard negative 和 action/product/time 限制 |

## 验收指标

| 指标 | 阶段目标 | 长期目标 |
|---|---:|---:|
| item duplicate pair F1 | >= 0.95 | >= 0.98 |
| dedupe explanation coverage | >= 0.80 | >= 0.95 |
| eventness precision | >= 0.90 | >= 0.95 |
| auto-merge precision | >= 0.95 | >= 0.98 |
| same-event pair recall | >= 0.70 | >= 0.85 |
| same-event pair F1 | >= 0.75 | >= 0.85 |
| digest/generic false positive | <= 0.02 | <= 0.01 |
| event_type known rate | >= 0.80 | >= 0.90 |
| event summary specific rate | >= 0.85 | >= 0.95 |
| review apply success | >= 0.95 | >= 0.99 |

## 推荐落地顺序

1. 固化测试方案和诊断脚本。
2. 补 dedupe explanation，不改变聚合行为。
3. 引入 eventness gate，减少错误 event。
4. 接入 signature exact，只做高精度 seed。
5. 接入 candidate high/medium 分层。
6. 增加 alias registry。
7. 引入 LLM 裁决 uncertain pair。
8. 迁移/重建 legacy cluster。
9. 升级 briefing/report。

## 完成定义

模块改造完成时，应满足：

- 每个 event cluster 都能追溯 member items。
- 每个 cluster item 都有 relation、confidence、evidence。
- 非事件内容不会自动成为 event。
- 去重重复来源可解释。
- 自动合并精度达到质量门。
- review 可以纠错并回写。
- briefing/report 基于可信事件对象生成。

