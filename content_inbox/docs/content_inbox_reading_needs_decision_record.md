# content-inbox 阅读需求匹配改造决策记录

## 1. 决策背景

`content-inbox` 当前已经完成了从 RSS 源到内容筛选的主链路：

```text
RSS 输入
  ↓
标准化
  ↓
去重
  ↓
AI 结构化打分
  ↓
embedding 事件聚类
  ↓
通知降噪
  ↓
inbox / report 输出
```

当前系统已经能从大量 RSS item 中筛选出候选内容，但仍存在几个问题：

1. 打分提示词主要内嵌在代码中，不便于查看和迭代。
2. 当前通用打分逻辑更偏“信息价值/个人相关度/可行动性”，不适合所有内容，尤其不适合娱乐内容。
3. 用户真正想解决的是几个阅读消费问题，而不是只得到一个混合推荐列表。
4. 用户的阅读需求会变化，因此不应把需求硬编码进 item JSON 或数据库字段。
5. RSS item 信息量有限，不足以支撑过多细粒度打分维度。
6. 如果为每个需求设计一套 prompt 目录、字段、打分维度，会引入过度复杂度。

用户当前明确关心四个问题：

```text
1. 今天看什么娱乐？
2. 我关注的一些前沿咋样了？
3. 我关心的话题/议题有什么新的进展？
4. 有什么是我值得看的？
```

---

## 2. 被否定的方案

### 2.1 多 Prompt 目录方案

曾考虑使用：

```text
prompts/
  screening_v2/
  incremental_v1/
  digest_lanes_v1/
  entertainment_v1/
  frontier_v1/
  watch_topics_v1/
  worth_reading_v1/
```

该方案被否定。

原因：

```text
1. 目录结构过重；
2. 新增/删除需求需要修改多个位置；
3. 用户后续自定义成本高；
4. prompt 版本、schema、purpose 文件过多；
5. 不适合当前轻量系统。
```

### 2.2 每个需求一套固定打分字段

曾考虑为娱乐、前沿、议题、值得看设计不同维度，例如：

```text
fun_score
relaxation_score
aesthetic_score
frontier_importance
technical_depth
trend_signal
time_worthiness
```

该方案被否定。

原因：

```text
1. 维度过多且语义容易重叠；
2. RSS item 信息不足时无法可靠打分；
3. 模型会产生伪精细分数；
4. item JSON 会不断膨胀；
5. 新增需求时需要新增字段和代码逻辑；
6. 不利于长期扩展。
```

### 2.3 为每个需求建立独立对象

例如：

```text
EntertainmentItem
FrontierItem
WatchTopicItem
WorthReadingItem
```

该方案被否定。

原因：

```text
1. 同一内容可能同时适合多个需求；
2. 内容底层对象应保持统一；
3. 拆对象会引入存储、查询、报告复杂度；
4. 不符合当前 content-inbox 的单一 item 处理模型。
```

---

## 3. 第一性原理分析

系统真正要解决的问题不是“给每条内容打很多分”，而是：

```text
每天有大量内容进入；
用户没有时间全部看；
系统需要根据用户当前阅读需求，把合适的内容挑出来，并说明为什么。
```

因此核心问题只有三个：

```text
1. 这条内容是什么？
2. 它和用户当前哪个阅读需求有关？
3. 在这个阅读需求下，它值不值得被用户看到？
```

对应设计应分为三层：

```text
基础内容理解层
  ↓
阅读需求匹配层
  ↓
视图输出层
```

---

## 4. 最终决策

### 4.1 保留稳定基础理解

每个 item 继续保留一份通用基础理解，包括：

```text
summary
title_cn
content_category
entities
topics
base_value_score
quality_signal
evidence_level
needs_more_context
suggested_next_step
confidence
```

这层只回答：

```text
内容是什么？
大概质量如何？
依据是否充分？
```

不把所有阅读需求硬塞进去。

### 4.2 用 reading_needs.yaml 配置阅读需求

新增：

```text
content_inbox/config/reading_needs.yaml
```

阅读需求成为配置数据，而不是代码结构。

每个需求包含：

```text
id
name
enabled
description
source_categories
question
rubric
min_score
```

新增需求时只改 YAML。

删除需求时设置 `enabled: false`。

### 4.3 用 watch_topics.yaml 配置关注议题

新增：

```text
content_inbox/config/watch_topics.yaml
```

用于定义用户关心的长期议题，例如：

```text
AI Agent
个人信息系统
AI 视频生成
```

每个 topic 包含：

```text
id
name
description
keywords
```

### 4.4 用 prompts.yaml 集中管理提示词

新增：

```text
content_inbox/prompts.yaml
```

只保留少量 prompt：

```text
basic_screening
need_matching
incremental
```

不为每个需求建立独立 prompt 文件夹。

### 4.5 用 need_matches[] 表示阅读需求匹配

不新增固定字段，例如 `entertainment_score`。

统一使用：

```json
{
  "need_matches": [
    {
      "need_id": "frontier",
      "need_name": "我关注的前沿咋样了",
      "score": 5,
      "decision": "include",
      "priority": "P0",
      "reason": "涉及重要 AI 产品动态。",
      "evidence": ["DeepSeek", "多模态"],
      "confidence": 0.9,
      "needs_more_context": false
    }
  ]
}
```

### 4.6 用 topic_matches[] 表示关注议题匹配

统一使用：

```json
{
  "topic_matches": [
    {
      "topic_id": "ai_video",
      "topic_name": "AI 视频生成",
      "score": 4,
      "update_type": "new_event",
      "reason": "讨论 AI 视频商业化和产品落地。",
      "confidence": 0.82
    }
  ]
}
```

### 4.7 输出视图按阅读需求组织

最终报告不再只看 `notification_decision`，而是按阅读需求输出：

```text
今天看什么娱乐
我关注的前沿咋样了
我关心的话题议题有什么新的进展
有什么是我值得看的
```

---

## 5. 决策结果

本次决策确定：

```text
content-inbox 不做复杂分类体系；
不为每个需求硬编码字段；
不为每个需求建立独立对象；
不设计大量细分打分维度；
不把需求写死进 item JSON。
```

取而代之：

```text
用 reading_needs.yaml 定义阅读需求；
用 watch_topics.yaml 定义关注议题；
用 prompts.yaml 管理少量通用 prompt；
用 need_matches[] 存储需求匹配结果；
用 topic_matches[] 存储议题匹配结果；
用 evidence_level/confidence 表示判断可靠度；
用报告层按需求生成可阅读视图。
```

---

## 6. 预期收益

### 6.1 可扩展

新增阅读需求只需要修改 YAML：

```yaml
- id: writing_material
  name: "适合作为写作素材"
  question: "这条内容是否适合作为我后续写文章或报告的素材？"
```

不需要改数据库字段，不需要改 item schema。

### 6.2 可解释

每个匹配结果都包含：

```text
score
decision
priority
reason
evidence
confidence
```

用户可以知道为什么某条内容进入某个视图。

### 6.3 适应不同内容类型

娱乐内容可以使用娱乐需求的判断问题，不再被通用“可行动性/信息价值”压低。

AI 前沿内容可以使用前沿需求的判断问题。

议题追踪可以使用 watch_topics。

### 6.4 避免伪精细化

系统不再要求模型输出大量语义不清的细分分数，减少 RSS 信息不足导致的猜测。

### 6.5 保持系统轻量

不引入复杂目录、不重构数据库、不新增独立对象体系，适合当前本地化 content-inbox 项目。

---

## 7. 后续验证标准

改造完成后，应验证：

```text
1. Prompt 可以从 prompts.yaml 查看和修改；
2. reading_needs.yaml 可以新增/删除需求；
3. watch_topics.yaml 可以新增/删除议题；
4. item 中出现 need_matches[] 和 topic_matches[]；
5. 英文内容有 title_cn 或中文解释；
6. 娱乐内容能进入 entertainment 视图；
7. AI 前沿内容能进入 frontier 视图；
8. AI Agent 相关内容能进入对应 topic；
9. GET /api/inbox?need_id=entertainment 可查询；
10. GET /api/inbox?topic_id=ai_agent 可查询；
11. 老 item 没有新字段时系统仍兼容。
```

---

## 8. 当前决策一句话总结

本次决策将 `content-inbox` 的下一步方向从：

```text
给内容增加更多硬编码打分字段
```

调整为：

```text
用可配置的阅读需求，从内容池中挑选适合不同消费场景的内容，并解释为什么。
```
