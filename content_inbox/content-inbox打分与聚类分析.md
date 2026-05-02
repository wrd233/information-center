# content-inbox 打分过滤与事件聚类去重模块设计

## 1. 模块目标

本设计覆盖 `content-inbox` 中两个核心模块：

1. 打分过滤模块：对进入系统的内容进行结构化分析、评分、分类、摘要、提取水下信息，并决定后续动作。
2. 事件聚类去重模块：基于向量嵌入和相似度计算，把同一主题或同一事件的多来源内容归并到事件簇中，并输出通知降噪决策。

两个模块共同服务于同一个目标：

```text
让内容处理中心不仅知道“这条内容是什么”，还要知道：
1. 它值不值得看；
2. 它是不是已经看过的同一件事；
3. 它是否提供了新增信息；
4. 它应该被完整推送、增量推送，还是静默处理。
```

---

## 2. 总体处理链路

所有内容统一进入同一条处理链路。

```text
内容输入
  ↓
基础解析
  ↓
标准化
  ↓
精确去重
  ↓
打分过滤
  ↓
生成 embedding_text
  ↓
向量嵌入
  ↓
事件聚类匹配
  ↓
增量判断
  ↓
通知降噪决策
  ↓
保存结果
  ↓
通过 GET /api/inbox 输出
```

RSS 输入和单条内容输入共享同一套后续流程。

```text
POST /api/rss/analyze
  ↓
feedparser 解析 RSS 源
  ↓
逐条 item 转为标准内容输入
  ↓
进入统一处理链路
```

```text
POST /api/content/analyze
  ↓
接收单条内容
  ↓
进入统一处理链路
```

---

## 3. 技术选型

### 3.1 RSS 解析

使用：

```text
feedparser
```

用途：

- 拉取并解析 RSS / Atom。
- 提取 feed 元信息。
- 提取 item 的标题、链接、摘要、发布时间、作者、guid 等基础字段。

RSS 解析不负责打分、聚类、摘要和正文深度抽取。

---

### 3.2 大模型结构化打分

使用：

```text
DeepSeek
```

调用方式：

- 使用 OpenAI-compatible Chat Completions 接口。
- 输出必须是结构化 JSON。
- 输出结果需要经过 schema 校验。
- 原始模型响应需要保存，便于调试和复盘。

用途：

- 分类。
- 评分。
- 简单摘要。
- 提取水下信息。
- 判断后续动作。
- 为事件聚类提供实体、事件描述和 embedding_text 的辅助信息。

---

### 3.3 向量嵌入

使用：

```text
text-embedding-3-small
```

调用方式：

```text
通过 https://yunwu.apifox.cn/ 这类 OpenAI-compatible 中转站调用
```

用途：

- 为内容生成向量。
- 为事件簇生成代表向量。
- 支撑相似内容检索。
- 支撑事件聚类去重。

---

### 3.4 向量存储与相似搜索

使用：

```text
SQLite + sqlite-vec
```

用途：

- 继续保持本地单服务形态。
- 保存内容向量。
- 保存事件簇向量。
- 执行相似度检索。
- 避免过早引入独立向量数据库服务。

---

## 4. 打分过滤模块设计

### 4.1 模块输入

打分过滤模块接收标准化后的内容对象。

```json
{
  "item_id": "item_xxx",
  "title": "内容标题",
  "url": "https://example.com/article/123",
  "source_name": "来源名称",
  "source_category": "Articles/AI",
  "content_type": "article",
  "published_at": "2026-05-02T10:00:00",
  "author": "作者",
  "summary": "RSS 摘要或外部摘要",
  "content_text": "正文片段、摘要、转录片段或其他可分析文本"
}
```

### 4.2 输入文本构造

传给 DeepSeek 的内容不直接使用原始对象，而是构造一个稳定的分析输入。

```text
来源名称：{source_name}
来源分类：{source_category}
内容类型：{content_type}
标题：{title}
链接：{url}
发布时间：{published_at}
作者：{author}
摘要：{summary}
正文片段：{content_text}
```

正文片段需要有长度限制。超出限制时截断，不在打分过滤阶段做全文处理。

---

### 4.3 模块输出

打分过滤模块输出结构化结果。

```json
{
  "summary": "一句话说明这条内容在讲什么",
  "category": "AI前沿",
  "value_score": 4,
  "personal_relevance": 5,
  "novelty_score": 4,
  "source_quality": 3,
  "actionability": 4,
  "hidden_signals": [
    "这条内容背后反映了某个值得关注的趋势",
    "这条内容可以启发后续信息系统设计"
  ],
  "entities": ["OpenAI", "RSS", "Embedding"],
  "event_hint": "某个主体发布或讨论了某个与内容处理相关的新方法",
  "suggested_action": "read",
  "followup_type": "archive",
  "reason": "这条内容与个人信息系统搭建高度相关，值得阅读和归档。",
  "tags": ["RSS", "信息管理", "AI工作流"],
  "confidence": 0.86
}
```

---

### 4.4 字段说明

| 字段 | 说明 |
|---|---|
| `summary` | 一句话摘要，用于 inbox 展示 |
| `category` | 内容粗分类 |
| `value_score` | 内容本身价值，1-5 |
| `personal_relevance` | 与用户长期兴趣和当前项目的相关度，1-5 |
| `novelty_score` | 是否包含新信息、新观点、新工具、新案例，1-5 |
| `source_quality` | 来源质量、可信度、信息密度，1-5 |
| `actionability` | 是否能转化为项目行动、方法、笔记或后续研究，1-5 |
| `hidden_signals` | 水下信息，即标题和摘要表层之外的隐含价值 |
| `entities` | 核心实体，用于事件聚类和实体重合判断 |
| `event_hint` | AI 提炼的事件描述，用于构造 embedding_text |
| `suggested_action` | 建议动作 |
| `followup_type` | 后续处理类型 |
| `reason` | 推荐、忽略或复核的理由 |
| `tags` | 少量标签 |
| `confidence` | 模型对判断的置信度，0-1 |

---

### 4.5 分类设计

`category` 使用粗分类，不做过细标签体系。

建议默认分类：

```text
AI前沿
AI工具
信息管理
技术学习
工程实践
社会观察
人生经验
商业产品
娱乐内容
新闻资讯
低质营销
其他
```

分类用于：

- inbox 过滤。
- 每日内容分组。
- 后续统计不同信息源质量。
- 辅助事件聚类判断。

---

### 4.6 评分维度

#### 4.6.1 value_score

内容本身价值。

```text
5 = 非常有价值，信息密度高，值得重点阅读或收藏
4 = 有价值，值得阅读
3 = 可看可不看，有一定信息量
2 = 价值较低，通常不需要主动阅读
1 = 噪声、低质、营销、标题党或空泛内容
```

#### 4.6.2 personal_relevance

与用户兴趣和当前项目的相关度。

```text
5 = 与当前项目或长期关注方向高度相关
4 = 明显相关，可能启发后续行动
3 = 一般相关
2 = 关系较弱
1 = 基本无关
```

#### 4.6.3 novelty_score

新颖度。

```text
5 = 明显包含新工具、新趋势、新方法或新事实
4 = 有较明确的新信息
3 = 有少量新信息
2 = 多数是已知内容
1 = 基本没有新增信息
```

#### 4.6.4 source_quality

来源质量。

```text
5 = 一手信息、权威来源、高信息密度
4 = 可靠来源，内容质量较高
3 = 普通来源，有参考价值
2 = 来源一般，可能有噪声
1 = 低质、营销、搬运或不可靠来源
```

#### 4.6.5 actionability

可行动性。

```text
5 = 可以直接转化为项目任务、工具选择、写作素材或研究方向
4 = 有明确启发，值得记录
3 = 有一些启发
2 = 行动价值较低
1 = 基本无法转化为行动
```

---

### 4.7 suggested_action 设计

`suggested_action` 只允许以下枚举：

```text
ignore
skim
read
save
transcribe
review
```

| 值 | 含义 |
|---|---|
| `ignore` | 忽略，不进入主动阅读 |
| `skim` | 快速扫一眼 |
| `read` | 值得阅读 |
| `save` | 值得收藏或归档 |
| `transcribe` | 值得转录，主要用于音视频 |
| `review` | 模型不确定，需要人工复核 |

---

### 4.8 followup_type 设计

`followup_type` 只允许以下枚举：

```text
none
fetch_fulltext
archive
transcribe
manual_review
```

| 值 | 含义 |
|---|---|
| `none` | 不需要后续处理 |
| `fetch_fulltext` | 值得后续抓取全文 |
| `archive` | 值得进入归档或知识库 |
| `transcribe` | 值得进入转录流程 |
| `manual_review` | 需要人工判断 |

---

### 4.9 阈值策略

打分过滤结果需要转换成系统行为。

建议采用可配置规则，而不是把判断写死在代码中。

```yaml
score_policy:
  ignore_below_value_score: 2
  read_min_value_score: 4
  read_min_personal_relevance: 3
  save_min_value_score: 4
  save_min_personal_relevance: 4
  transcribe_min_value_score: 4
  transcribe_min_personal_relevance: 3
  manual_review_confidence_below: 0.6
```

动作派生逻辑：

```text
confidence < manual_review_confidence_below
  → suggested_action = review

value_score <= ignore_below_value_score
  → suggested_action = ignore

content_type in video/audio
且 value_score >= transcribe_min_value_score
且 personal_relevance >= transcribe_min_personal_relevance
  → suggested_action = transcribe
  → followup_type = transcribe

value_score >= save_min_value_score
且 personal_relevance >= save_min_personal_relevance
  → suggested_action = save
  → followup_type = archive

value_score >= read_min_value_score
且 personal_relevance >= read_min_personal_relevance
  → suggested_action = read

否则
  → suggested_action = skim 或 ignore
```

DeepSeek 可以先给出建议动作；系统规则可以在模型输出后进行二次校正。

---

### 4.10 水下信息 hidden_signals

`hidden_signals` 用于提取标题、摘要和表层内容之外的潜在价值。

它不是摘要，也不是标签。

它应该回答：

```text
这条内容背后有什么值得注意的趋势、方法、风险、机会、工作流或项目启发？
```

示例：

```json
{
  "hidden_signals": [
    "多个独立工具都在向 API 化工作流演进，说明个人信息系统的接口层值得优先建设。",
    "这篇内容虽然表面是工具介绍，但核心价值在于它暴露了一个内容过滤和通知降噪的设计模式。"
  ]
}
```

如果没有明显水下信息，可以返回空数组。

---

### 4.11 供事件聚类使用的字段

打分过滤模块需要为事件聚类模块提供辅助字段：

```json
{
  "entities": ["OpenAI", "RSSHub", "sqlite-vec"],
  "event_hint": "某个项目或主体围绕 RSS 内容过滤和事件聚类进行设计或发布"
}
```

用途：

- 构造 embedding_text。
- 判断实体重合度。
- 判断相似内容是否属于同一事件。
- 辅助生成事件簇标题和摘要。

---

## 5. 事件聚类去重模块设计

### 5.1 模块目标

事件聚类去重模块用于判断新内容和历史内容之间的关系。

它回答三个问题：

```text
1. 这是不是一个全新事件？
2. 这是不是已有事件的新增报道？
3. 这是不是高度重复内容，应该静默？
```

它不替代精确去重。

精确去重用于处理同 URL、同 guid、同来源同标题等重复内容。

事件聚类用于处理不同来源、不同标题、不同链接但语义上属于同一事件或同一主题的内容。

---

### 5.2 模块输入

事件聚类模块接收：

```json
{
  "item_id": "item_xxx",
  "title": "内容标题",
  "summary": "一句话摘要",
  "source_name": "来源名称",
  "source_category": "来源分类",
  "content_type": "article",
  "published_at": "2026-05-02T10:00:00",
  "entities": ["OpenAI", "RSS", "Embedding"],
  "event_hint": "OpenAI 发布或讨论了某个与内容处理相关的新能力",
  "value_score": 4,
  "personal_relevance": 5
}
```

---

### 5.3 embedding_text 构造

不直接使用全文生成 embedding。

系统先构造一个用于事件匹配的 `embedding_text`。

推荐格式：

```text
标题：{title}
摘要：{summary}
核心实体：{entities}
事件描述：{event_hint}
来源分类：{source_category}
内容类型：{content_type}
```

这样做的目的：

- 降低全文噪声。
- 让相似度更关注事件本身。
- 让不同来源对同一事件的报道更容易聚在一起。
- 避免长文中大量背景信息稀释主题。

---

### 5.4 向量生成

使用 `text-embedding-3-small` 生成向量。

调用配置：

```yaml
embedding:
  provider: "yunwu"
  base_url: "https://yunwu.apifox.cn/v1"
  model: "text-embedding-3-small"
```

处理要求：

- embedding_text 为空时不执行聚类。
- embedding 调用失败时，内容仍可保存，但聚类状态标记为 `embedding_failed`。
- 向量结果写入 SQLite + sqlite-vec。
- 需要保存 embedding 模型名称和 embedding_text，便于后续重算。

---

### 5.5 相似内容检索

新内容生成向量后，在历史内容或事件簇中检索最相似对象。

推荐优先检索事件簇，而不是直接检索所有 item。

原因：

- item 数量会持续增长。
- cluster 是更稳定的事件单位。
- 通知降噪最终也是围绕事件簇进行。

检索流程：

```text
新 item vector
  ↓
查询 active event_clusters
  ↓
获得 Top K 相似 cluster
  ↓
取最高相似度 cluster 作为候选
  ↓
结合实体重合度判断关系
```

可配置参数：

```yaml
clustering:
  top_k: 5
  new_event_threshold: 0.85
  duplicate_threshold: 0.97
  high_overlap_entity_ratio: 0.6
```

---

### 5.6 相似度区间

使用三个区间做初始判断。

#### 5.6.1 全新事件

```text
similarity < 0.85
```

判断：

```text
视为全新事件
```

动作：

```text
新建 event_cluster
notification_decision = full_push
cluster_relation = new_event
```

#### 5.6.2 增量更新

```text
0.85 <= similarity < 0.97
```

判断：

```text
可能是已有事件的新增报道、补充说明或不同角度
```

动作：

```text
加入已有 event_cluster
调用 DeepSeek 比较新内容与 cluster_summary
提取 incremental_summary
notification_decision = incremental_push
cluster_relation = incremental_update
```

#### 5.6.3 高度重复

```text
similarity >= 0.97
且实体高度重合
```

判断：

```text
高度重复内容
```

动作：

```text
加入已有 event_cluster
notification_decision = silent
cluster_relation = duplicate
```

如果 similarity 很高但实体不重合，则进入 `manual_review` 或 `incremental_update`，避免误判。

---

### 5.7 实体重合判断

实体重合用于修正单纯向量相似度的误判。

输入：

```json
{
  "new_item_entities": ["OpenAI", "Embedding", "RSS"],
  "cluster_entities": ["OpenAI", "text-embedding-3-small", "RSS"]
}
```

计算：

```text
entity_overlap_ratio = intersection(new_item_entities, cluster_entities) / min(len(new_item_entities), len(cluster_entities))
```

用途：

```text
similarity >= duplicate_threshold
且 entity_overlap_ratio >= high_overlap_entity_ratio
  → duplicate

similarity >= duplicate_threshold
但 entity_overlap_ratio < high_overlap_entity_ratio
  → incremental_update 或 manual_review
```

---

### 5.8 event_cluster 设计

事件簇是事件聚类去重模块的核心对象。

建议事件簇包含以下信息：

```json
{
  "cluster_id": "cluster_xxx",
  "cluster_title": "事件簇标题",
  "cluster_summary": "这个事件目前已经知道什么",
  "entities": ["OpenAI", "RSS", "Embedding"],
  "representative_item_id": "item_xxx",
  "first_seen_at": "2026-05-01T10:00:00",
  "last_seen_at": "2026-05-02T12:00:00",
  "item_count": 5,
  "status": "active"
}
```

#### 5.8.1 cluster_title

由第一条内容或 DeepSeek 生成。

要求：

- 简短。
- 能代表事件。
- 不要直接复制噪声标题。

#### 5.8.2 cluster_summary

事件簇摘要。

内容包括：

- 已知事实。
- 事件主线。
- 已确认的重要信息。
- 不包含每篇文章的重复描述。

#### 5.8.3 cluster_entities

事件簇实体集合。

来源：

- 第一条内容的 entities。
- 后续增量内容补充的 entities。
- 可以去重合并。

#### 5.8.4 cluster_vector

事件簇代表向量。

可选策略：

1. 使用代表内容的向量。
2. 使用 cluster_summary 重新生成向量。
3. 使用簇内 item 向量平均值。

建议配置化：

```yaml
clustering:
  cluster_vector_strategy: "summary_embedding"
```

可选值：

```text
representative_item
summary_embedding
average_items
```

---

### 5.9 item 与 cluster 的关系

每条内容都应记录与事件簇的关系。

```json
{
  "item_id": "item_xxx",
  "cluster_id": "cluster_xxx",
  "cluster_relation": "incremental_update",
  "max_similarity": 0.91,
  "entity_overlap_ratio": 0.67,
  "notification_decision": "incremental_push",
  "incremental_summary": "相比此前内容，新增了定价和发布时间信息。"
}
```

`cluster_relation` 枚举：

```text
new_event
incremental_update
duplicate
uncertain
embedding_failed
```

`notification_decision` 枚举：

```text
full_push
incremental_push
silent
manual_review
```

---

### 5.10 增量摘要

当新内容被判断为 `incremental_update` 时，需要提取它相对已有事件簇的新增信息。

输入给 DeepSeek：

```json
{
  "cluster_title": "事件簇标题",
  "cluster_summary": "已有事件摘要",
  "new_item_title": "新内容标题",
  "new_item_summary": "新内容摘要",
  "new_item_hidden_signals": ["水下信息1", "水下信息2"],
  "new_item_entities": ["实体1", "实体2"]
}
```

输出：

```json
{
  "has_incremental_value": true,
  "incremental_summary": "相比已有内容，新增了具体发布时间、价格信息和一个新的应用场景。",
  "new_entities": ["新实体"],
  "should_update_cluster_summary": true,
  "updated_cluster_summary": "更新后的事件簇摘要"
}
```

如果没有新增信息：

```json
{
  "has_incremental_value": false,
  "incremental_summary": "",
  "should_update_cluster_summary": false
}
```

通知决策：

```text
has_incremental_value = true
  → notification_decision = incremental_push

has_incremental_value = false
  → notification_decision = silent
```

---

### 5.11 事件簇归档

事件簇如果连续一段时间没有更新，应自动归档。

默认策略：

```text
active cluster 连续 7 天没有新 item
  → status = archived
```

配置：

```yaml
clustering:
  archive_after_days: 7
```

归档后的事件簇：

- 默认不参与 active cluster 通知。
- 可在历史检索中查询。
- 可选参与低优先级相似度参考。

---

## 6. 两个模块之间的关系

### 6.1 先后顺序

推荐顺序：

```text
标准化
  ↓
精确去重
  ↓
打分过滤
  ↓
事件聚类
  ↓
通知决策
```

原因：

1. 精确去重先挡掉完全重复内容，避免浪费模型和 embedding 调用。
2. 打分过滤先判断内容价值，避免低价值内容进入高成本聚类流程。
3. 事件聚类再判断高价值内容是否是新事件、增量更新或重复内容。
4. 通知决策综合打分结果和聚类结果。

---

### 6.2 低分内容是否聚类

默认策略：

```text
低分内容不进入事件聚类
```

原因：

- 节省 embedding 成本。
- 避免为噪声建立事件簇。
- 让事件簇主要服务于值得关注的内容。

可配置：

```yaml
clustering:
  cluster_min_value_score: 3
  cluster_min_personal_relevance: 3
```

只有满足条件的内容才进入聚类。

---

### 6.3 打分结果如何影响通知

通知决策同时参考：

```text
value_score
personal_relevance
suggested_action
cluster_relation
similarity
entity_overlap_ratio
has_incremental_value
```

基础逻辑：

```text
value_score 低
  → silent

高价值 + 新事件
  → full_push

高价值 + 增量更新 + 有新增信息
  → incremental_push

高价值 + 高度重复
  → silent

模型或聚类不确定
  → manual_review
```

---

### 6.4 最终输出结构

`GET /api/inbox` 中每条内容应包含打分过滤结果和聚类降噪结果。

```json
{
  "item_id": "item_xxx",
  "title": "文章标题",
  "url": "https://example.com/article/123",
  "source_name": "来源名称",
  "source_category": "Articles/AI",
  "content_type": "article",
  "published_at": "2026-05-02T10:00:00",
  "screening": {
    "summary": "一句话摘要",
    "category": "AI工具",
    "value_score": 5,
    "personal_relevance": 4,
    "novelty_score": 4,
    "source_quality": 3,
    "actionability": 4,
    "hidden_signals": ["隐含价值"],
    "entities": ["OpenAI", "RSS"],
    "event_hint": "事件描述",
    "suggested_action": "read",
    "followup_type": "none",
    "reason": "推荐理由",
    "tags": ["AI", "RSS"],
    "confidence": 0.86
  },
  "clustering": {
    "cluster_id": "cluster_xxx",
    "cluster_title": "事件簇标题",
    "cluster_relation": "incremental_update",
    "max_similarity": 0.91,
    "entity_overlap_ratio": 0.67,
    "notification_decision": "incremental_push",
    "incremental_summary": "相比此前内容，新增了具体时间和应用场景。"
  }
}
```

---

## 7. API 影响

### 7.1 POST /api/content/analyze

该接口应完整执行：

```text
标准化
  ↓
精确去重
  ↓
打分过滤
  ↓
事件聚类
  ↓
保存
  ↓
返回结果
```

返回中应包含：

```json
{
  "ok": true,
  "item_id": "item_xxx",
  "is_duplicate": false,
  "screening": {},
  "clustering": {}
}
```

---

### 7.2 POST /api/rss/analyze

该接口应：

```text
解析 RSS 源
  ↓
逐条调用统一内容处理流程
  ↓
汇总返回处理结果
```

返回中应增加聚类相关统计：

```json
{
  "ok": true,
  "total_items": 20,
  "new_items": 12,
  "duplicate_items": 8,
  "screened_items": 12,
  "new_event_items": 4,
  "incremental_items": 3,
  "silent_items": 5,
  "recommended_items": 3,
  "failed_items": 0
}
```

---

### 7.3 GET /api/inbox

查询参数应支持打分过滤和聚类降噪字段。

已有或建议支持：

```text
date
from
to
source_name
source_category
content_type
category
min_score
min_relevance
suggested_action
followup_type
tag
keyword
include_ignored
limit
offset
```

新增建议支持：

```text
cluster_id
cluster_relation
notification_decision
min_similarity
include_silent
only_new_events
only_incremental
```

示例：

```http
GET /api/inbox?date=today&notification_decision=full_push,incremental_push
```

```http
GET /api/inbox?cluster_relation=new_event&min_score=4
```

```http
GET /api/inbox?suggested_action=transcribe&include_silent=false
```

---

## 8. 配置文件设计

建议使用配置文件集中管理可调整参数。

示例文件：

```text
config/content_inbox.yaml
```

---

### 8.1 模型配置

```yaml
llm:
  provider: "deepseek"
  base_url: "https://api.deepseek.com/v1"
  api_key_env: "DEEPSEEK_API_KEY"
  model: "deepseek-chat"
  temperature: 0.2
  max_tokens: 1200
  timeout_seconds: 60
  prompt_version: "screening_v1"
```

---

### 8.2 打分过滤配置

```yaml
screening:
  enabled: true
  max_input_chars: 4000
  categories:
    - "AI前沿"
    - "AI工具"
    - "信息管理"
    - "技术学习"
    - "工程实践"
    - "社会观察"
    - "人生经验"
    - "商业产品"
    - "娱乐内容"
    - "新闻资讯"
    - "低质营销"
    - "其他"

  score_policy:
    ignore_below_value_score: 2
    read_min_value_score: 4
    read_min_personal_relevance: 3
    save_min_value_score: 4
    save_min_personal_relevance: 4
    transcribe_min_value_score: 4
    transcribe_min_personal_relevance: 3
    manual_review_confidence_below: 0.6
```

---

### 8.3 Embedding 配置

```yaml
embedding:
  enabled: true
  provider: "yunwu"
  base_url: "https://yunwu.apifox.cn/v1"
  api_key_env: "YUNWU_API_KEY"
  model: "text-embedding-3-small"
  timeout_seconds: 60
  max_input_chars: 3000
```

---

### 8.4 聚类配置

```yaml
clustering:
  enabled: true
  top_k: 5
  new_event_threshold: 0.85
  duplicate_threshold: 0.97
  high_overlap_entity_ratio: 0.6
  cluster_min_value_score: 3
  cluster_min_personal_relevance: 3
  cluster_vector_strategy: "summary_embedding"
  archive_after_days: 7
```

---

### 8.5 通知降噪配置

```yaml
notification:
  full_push_for_new_event: true
  incremental_push_when_has_new_info: true
  silent_duplicates: true
  include_silent_in_default_inbox: false
  manual_review_when_uncertain: true
```

---

## 9. 错误处理

### 9.1 DeepSeek 打分失败

处理策略：

```text
保存原始内容
screening.status = failed
suggested_action = review
followup_type = manual_review
```

不得伪造高分或低分结果。

---

### 9.2 Embedding 调用失败

处理策略：

```text
内容仍然保存
clustering.cluster_relation = embedding_failed
notification_decision = manual_review
```

---

### 9.3 sqlite-vec 检索失败

处理策略：

```text
内容仍然保存
聚类结果标记为 failed
不影响打分过滤结果
```

---

### 9.4 增量摘要失败

处理策略：

```text
保留 cluster_relation = incremental_update
notification_decision = manual_review
incremental_summary 为空
```

---

## 10. 保存要求

每条内容至少需要保存：

```text
原始输入
标准化结果
打分过滤结果
embedding_text
embedding 模型名
聚类结果
通知决策
创建时间
更新时间
```

每个事件簇至少需要保存：

```text
cluster_id
cluster_title
cluster_summary
entities
representative_item_id
first_seen_at
last_seen_at
item_count
status
cluster_vector
```

---

## 11. 查询输出要求

`GET /api/inbox` 默认应面向“可阅读结果”，而不是数据库裸字段。

默认返回：

```text
推荐阅读
建议收藏
建议转录
需要复核
```

默认不返回：

```text
ignore
silent duplicate
```

除非用户显式传入：

```text
include_ignored=true
include_silent=true
```

---

## 12. 边界

本设计不包含：

- IM 推送实现。
- Obsidian 写入实现。
- Memo 自动增强实现。
- 视频转录服务调用实现。
- 网页 UI。
- 跨设备同步。
- 用户反馈学习。
- 离线主题建模。
