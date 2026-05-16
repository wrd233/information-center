# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T13:57:50+00:00
- 结束时间：2026-05-04T13:58:42+00:00
- 日期：2026-05-04
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：10
- 已处理源数量：10
- 成功源数量：10
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：20
- new_items：20
- duplicate_items：0
- screened_items：20
- recommended_items_from_api_response：5
- new_items_recommended：unknown
- final_inbox_items_from_this_run：4
- full_push_items_from_this_run：4
- incremental_push_items_from_this_run：0
- silent_items：16
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- source concurrency=10, llm_max_concurrency_requested=10, llm_max_concurrency_applied=10, screening_mode_requested=merged, screening_mode_applied=merged, timeout=600, sleep=0.1, limit_per_source=2

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 1 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 2 | 2 | 0 | 2 | 0 | 1 | 0 | 2 | 0 |  |
| 3 | AI Foundations | Videos | success | 2 | 2 | 0 | 2 | 1 | 2 | 0 | 1 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 2 | 2 | 0 | 2 | 1 | 0 | 0 | 2 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 2 | 2 | 0 | 2 | 2 | 2 | 0 | 0 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

无

### 我关注的前沿咋样了

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布了 Live Artifacts...（惊人效果）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：4
  - 摘要：Claude 发布 Live Artifacts 功能，在 Cowork 侧边栏提供持久交互页面，提升工作流管理。
  - need_score：5
  - priority：P0
  - reason：涉及重要 AI 产品动态，Claude 新功能更新。
  - evidence：Claude, Live Artifacts
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Vol.27 对话汪华、袁进辉、胡修涵：2025年，活下来最重要，但机会一定要抓住**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/67743ca015a5fd520e20815b
  - 评分：5
  - 摘要：2024年AI行业复盘与2025年创业方向前瞻，由极客公园组织多位行业人士讨论，涵盖OpenAI、大模型趋势、应用爆发等关键话题。
  - need_score：5
  - priority：P0
  - reason：涉及2024年AI重要变化和2025年趋势，包括OpenAI、Scaling Law、应用爆发等前沿信号。
  - evidence：OpenAI, Scaling Law, Agent, AI应用
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Vol.28 和CES上最酷的AI硬件们，一起聊聊2025年什么方向值得做？**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/6791b46ca2c8d144a7ebc6cb
  - 评分：4
  - 摘要：本期播客讨论2025年CES上展示的AI硬件趋势，包括AI宠物、可穿戴设备、智能音箱等，并探讨百万销量单品方向。
  - need_score：5
  - priority：P1
  - reason：涉及重要AI产品动态，提供CES上多个AI硬件案例和趋势判断。
  - evidence：CES, AI硬件, Ropet, LOOI, RingConn
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **2025 重新定义的生活**
  - 来源：Hi, DIYgod
  - 链接：https://diygod.cc/2025
  - 评分：4
  - 摘要：个人年度总结，讲述AI革命下的存在危机、新手爸爸的感悟、加密货币投资教训以及开源思维与商业的冲突。
  - need_score：4
  - priority：P1
  - reason：讨论了AI对编程和插画行业的影响，以及AI工具的实际使用体验。
  - evidence：GPT-4, Stable Diffusion, GitHub Copilot, vibe coding
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

### 我关心的话题议题有什么新的进展

无

### 有什么是我值得看的

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布了 Live Artifacts...（惊人效果）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：4
  - 摘要：Claude 发布 Live Artifacts 功能，在 Cowork 侧边栏提供持久交互页面，提升工作流管理。
  - need_score：4
  - priority：P1
  - reason：有价值的前沿信息，快速浏览即可。
  - evidence：Claude 更新, AI 工具
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **2025 重新定义的生活**
  - 来源：Hi, DIYgod
  - 链接：https://diygod.cc/2025
  - 评分：4
  - 摘要：个人年度总结，讲述AI革命下的存在危机、新手爸爸的感悟、加密货币投资教训以及开源思维与商业的冲突。
  - need_score：4
  - priority：P1
  - reason：个人故事与行业观察结合，有启发性和真实性。
  - evidence：全文
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

### 系统通知推荐

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布了 Live Artifacts...（惊人效果）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：4
  - 摘要：Claude 发布 Live Artifacts 功能，在 Cowork 侧边栏提供持久交互页面，提升工作流管理。
  - 理由：介绍 Claude 新功能，有一定前沿价值，但来源营销感强，快速了解即可
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Vol.28 和CES上最酷的AI硬件们，一起聊聊2025年什么方向值得做？**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/6791b46ca2c8d144a7ebc6cb
  - 评分：4
  - 摘要：本期播客讨论2025年CES上展示的AI硬件趋势，包括AI宠物、可穿戴设备、智能音箱等，并探讨百万销量单品方向。
  - 理由：内容涉及AI硬件前沿动态，有实际产品案例和行业洞察，对关注AI趋势的用户有较高价值。
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **2025 重新定义的生活**
  - 来源：Hi, DIYgod
  - 链接：https://diygod.cc/2025
  - 评分：4
  - 摘要：个人年度总结，讲述AI革命下的存在危机、新手爸爸的感悟、加密货币投资教训以及开源思维与商业的冲突。
  - 理由：内容详实，对AI影响有深刻个人视角，涉及工作、投资、家庭多个维度，值得细读。
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Vol.27 对话汪华、袁进辉、胡修涵：2025年，活下来最重要，但机会一定要抓住**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/67743ca015a5fd520e20815b
  - 评分：5
  - 摘要：2024年AI行业复盘与2025年创业方向前瞻，由极客公园组织多位行业人士讨论，涵盖OpenAI、大模型趋势、应用爆发等关键话题。
  - 理由：深度AI行业复盘与前瞻，涉及多个重要公司和趋势，适合关注前沿的读者。
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

## 5. 失败源列表

无
