# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T03:54:02+00:00
- 结束时间：2026-05-03T03:58:07+00:00
- 日期：2026-05-03
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：5
- 已处理源数量：5
- 成功源数量：5
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：10
- new_items：10
- duplicate_items：0
- screened_items：10
- recommended_items_from_api_response：7
- new_items_recommended：unknown
- final_inbox_items_from_this_run：2
- full_push_items_from_this_run：2
- incremental_push_items_from_this_run：0
- silent_items：9
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 3 | AI Foundations | Videos | success | 2 | 2 | 0 | 2 | 2 | 1 | 0 | 1 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 2 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

无

### 我关注的前沿咋样了

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布 Live Artifacts……（效果惊人）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：4
  - needs_more_context：False
  - confidence：0.9
  - 摘要：Claude 发布 Live Artifacts 功能，可在 Cowork 侧边栏创建持久交互页面，提升工作流效率。
  - 理由：该内容介绍了 Cluade 的重要新功能，对 AI 用户有实际参考价值，且时效性强。
  - 标签：Claude, Live Artifacts, AI 工具更新, 工作流
  - need_match[frontier] score=5 priority=P0 reason=Claude 发布 Live Artifacts 功能，这是重要的 AI 产品更新，代表 AI 工具向持久化工作界面演进的前沿信号。 evidence=Claude, Live Artifacts, AI 工具竞争 confidence=0.95 needs_more_context=False
  - need_match[entertainment] score=2 priority=P3 reason=内容聚焦于技术功能演示，并非轻松娱乐内容。 evidence=标题和摘要强调技术更新，无娱乐元素 confidence=0.9 needs_more_context=False
  - need_match[watch_topic_update] score=4 priority=P1 reason=匹配关注议题中的 AI Agent（相关工作流方向），提供了功能更新信息。 evidence=Live Artifacts 与工作流管理相关，可能用于 Agent 场景 confidence=0.75 needs_more_context=True
  - need_match[worth_reading] score=4 priority=P1 reason=内容介绍了重要新功能，对 AI 用户有实际价值，信息密度适中。 evidence=高时效性, 可行动性高, 内容清晰 confidence=0.9 needs_more_context=False
  - topic_match[ai_agent] score=3 update_type=related reason=Live Artifacts 功能可增强工作流管理，与 Agent 的交互界面和工作流有一定关联，但非直接 Agent 更新。 confidence=0.7
  - topic_match[information_system] score=2 update_type=related reason=涉及工作区文件夹和效率管理，但与 RSS、知识库自动化等典型信息系统主题关联较弱。 confidence=0.6
  - topic_match[ai_video] score=1 update_type=related reason=内容不涉及视频生成领域。 confidence=0.95

- **OpenAI Agent SDK ships**
  - 中文解释：OpenAI Agent SDK 发布
  - 来源：Tech Blog
  - 评分：4
  - needs_more_context：False
  - confidence：0.9
  - 摘要：OpenAI 发布了面向开发者的 Agent SDK。
  - 理由：标题明确且有摘要支撑，值得进一步了解 SDK 细节
  - 标签：OpenAI, Agent SDK, AI开发工具
  - need_match[frontier] score=5 priority=P0 reason=OpenAI 正式发布 Agent SDK，是 AI 工具前沿的重要动态，可能影响 Agent 开发趋势。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - need_match[entertainment] score=1 priority=P3 reason=技术发布内容，不适合轻松娱乐。 evidence= confidence=0.9 needs_more_context=False
  - need_match[watch_topic_update] score=4 priority=P1 reason=该内容直接匹配关注议题 AI Agent，提供了 OpenAI 官方 SDK 的新进展。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - need_match[worth_reading] score=4 priority=P1 reason=高相关、高行动性，对 AI 开发者有明确阅读价值。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - topic_match[ai_agent] score=5 update_type=new_event reason=OpenAI 发布 Agent SDK，是 AI Agent 领域的重要新事件。 confidence=0.95

### 我关心的话题议题有什么新的进展

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布 Live Artifacts……（效果惊人）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：4
  - needs_more_context：False
  - confidence：0.9
  - 摘要：Claude 发布 Live Artifacts 功能，可在 Cowork 侧边栏创建持久交互页面，提升工作流效率。
  - 理由：该内容介绍了 Cluade 的重要新功能，对 AI 用户有实际参考价值，且时效性强。
  - 标签：Claude, Live Artifacts, AI 工具更新, 工作流
  - need_match[frontier] score=5 priority=P0 reason=Claude 发布 Live Artifacts 功能，这是重要的 AI 产品更新，代表 AI 工具向持久化工作界面演进的前沿信号。 evidence=Claude, Live Artifacts, AI 工具竞争 confidence=0.95 needs_more_context=False
  - need_match[entertainment] score=2 priority=P3 reason=内容聚焦于技术功能演示，并非轻松娱乐内容。 evidence=标题和摘要强调技术更新，无娱乐元素 confidence=0.9 needs_more_context=False
  - need_match[watch_topic_update] score=4 priority=P1 reason=匹配关注议题中的 AI Agent（相关工作流方向），提供了功能更新信息。 evidence=Live Artifacts 与工作流管理相关，可能用于 Agent 场景 confidence=0.75 needs_more_context=True
  - need_match[worth_reading] score=4 priority=P1 reason=内容介绍了重要新功能，对 AI 用户有实际价值，信息密度适中。 evidence=高时效性, 可行动性高, 内容清晰 confidence=0.9 needs_more_context=False
  - topic_match[ai_agent] score=3 update_type=related reason=Live Artifacts 功能可增强工作流管理，与 Agent 的交互界面和工作流有一定关联，但非直接 Agent 更新。 confidence=0.7
  - topic_match[information_system] score=2 update_type=related reason=涉及工作区文件夹和效率管理，但与 RSS、知识库自动化等典型信息系统主题关联较弱。 confidence=0.6
  - topic_match[ai_video] score=1 update_type=related reason=内容不涉及视频生成领域。 confidence=0.95

- **OpenAI Agent SDK ships**
  - 中文解释：OpenAI Agent SDK 发布
  - 来源：Tech Blog
  - 评分：4
  - needs_more_context：False
  - confidence：0.9
  - 摘要：OpenAI 发布了面向开发者的 Agent SDK。
  - 理由：标题明确且有摘要支撑，值得进一步了解 SDK 细节
  - 标签：OpenAI, Agent SDK, AI开发工具
  - need_match[frontier] score=5 priority=P0 reason=OpenAI 正式发布 Agent SDK，是 AI 工具前沿的重要动态，可能影响 Agent 开发趋势。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - need_match[entertainment] score=1 priority=P3 reason=技术发布内容，不适合轻松娱乐。 evidence= confidence=0.9 needs_more_context=False
  - need_match[watch_topic_update] score=4 priority=P1 reason=该内容直接匹配关注议题 AI Agent，提供了 OpenAI 官方 SDK 的新进展。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - need_match[worth_reading] score=4 priority=P1 reason=高相关、高行动性，对 AI 开发者有明确阅读价值。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - topic_match[ai_agent] score=5 update_type=new_event reason=OpenAI 发布 Agent SDK，是 AI Agent 领域的重要新事件。 confidence=0.95

### 有什么是我值得看的

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布 Live Artifacts……（效果惊人）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：4
  - needs_more_context：False
  - confidence：0.9
  - 摘要：Claude 发布 Live Artifacts 功能，可在 Cowork 侧边栏创建持久交互页面，提升工作流效率。
  - 理由：该内容介绍了 Cluade 的重要新功能，对 AI 用户有实际参考价值，且时效性强。
  - 标签：Claude, Live Artifacts, AI 工具更新, 工作流
  - need_match[frontier] score=5 priority=P0 reason=Claude 发布 Live Artifacts 功能，这是重要的 AI 产品更新，代表 AI 工具向持久化工作界面演进的前沿信号。 evidence=Claude, Live Artifacts, AI 工具竞争 confidence=0.95 needs_more_context=False
  - need_match[entertainment] score=2 priority=P3 reason=内容聚焦于技术功能演示，并非轻松娱乐内容。 evidence=标题和摘要强调技术更新，无娱乐元素 confidence=0.9 needs_more_context=False
  - need_match[watch_topic_update] score=4 priority=P1 reason=匹配关注议题中的 AI Agent（相关工作流方向），提供了功能更新信息。 evidence=Live Artifacts 与工作流管理相关，可能用于 Agent 场景 confidence=0.75 needs_more_context=True
  - need_match[worth_reading] score=4 priority=P1 reason=内容介绍了重要新功能，对 AI 用户有实际价值，信息密度适中。 evidence=高时效性, 可行动性高, 内容清晰 confidence=0.9 needs_more_context=False
  - topic_match[ai_agent] score=3 update_type=related reason=Live Artifacts 功能可增强工作流管理，与 Agent 的交互界面和工作流有一定关联，但非直接 Agent 更新。 confidence=0.7
  - topic_match[information_system] score=2 update_type=related reason=涉及工作区文件夹和效率管理，但与 RSS、知识库自动化等典型信息系统主题关联较弱。 confidence=0.6
  - topic_match[ai_video] score=1 update_type=related reason=内容不涉及视频生成领域。 confidence=0.95

- **OpenAI Agent SDK ships**
  - 中文解释：OpenAI Agent SDK 发布
  - 来源：Tech Blog
  - 评分：4
  - needs_more_context：False
  - confidence：0.9
  - 摘要：OpenAI 发布了面向开发者的 Agent SDK。
  - 理由：标题明确且有摘要支撑，值得进一步了解 SDK 细节
  - 标签：OpenAI, Agent SDK, AI开发工具
  - need_match[frontier] score=5 priority=P0 reason=OpenAI 正式发布 Agent SDK，是 AI 工具前沿的重要动态，可能影响 Agent 开发趋势。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - need_match[entertainment] score=1 priority=P3 reason=技术发布内容，不适合轻松娱乐。 evidence= confidence=0.9 needs_more_context=False
  - need_match[watch_topic_update] score=4 priority=P1 reason=该内容直接匹配关注议题 AI Agent，提供了 OpenAI 官方 SDK 的新进展。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - need_match[worth_reading] score=4 priority=P1 reason=高相关、高行动性，对 AI 开发者有明确阅读价值。 evidence=OpenAI, Agent SDK confidence=0.9 needs_more_context=False
  - topic_match[ai_agent] score=5 update_type=new_event reason=OpenAI 发布 Agent SDK，是 AI Agent 领域的重要新事件。 confidence=0.95

## 5. 失败源列表

无
