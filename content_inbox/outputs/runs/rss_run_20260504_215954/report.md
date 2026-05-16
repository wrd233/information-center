# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T13:59:54+00:00
- 结束时间：2026-05-04T14:01:00+00:00
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
- recommended_items_from_api_response：9
- new_items_recommended：unknown
- final_inbox_items_from_this_run：3
- full_push_items_from_this_run：3
- incremental_push_items_from_this_run：0
- silent_items：17
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- source concurrency=10, llm_max_concurrency_requested=10, llm_max_concurrency_applied=10, screening_mode_requested=two_stage, screening_mode_applied=two_stage, timeout=600, sleep=0.1, limit_per_source=2

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 2 | 2 | 0 | 2 | 1 | 0 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 2 | 2 | 0 | 2 | 1 | 0 | 0 | 2 | 0 |  |
| 3 | AI Foundations | Videos | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 2 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 1 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 2 | 2 | 0 | 2 | 1 | 2 | 0 | 1 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 2 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 1 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

- **欧洲旅游VLOG \| 巴塞罗那 罗马 梵蒂冈 威尼斯 米兰 苏黎世 因特拉肯 巴黎**
  - 来源：Hi, DIYgod
  - 链接：https://diygod.cc/europe-travel
  - 评分：1
  - 摘要：作者分享2022年12月欧洲多国旅游VLOG。
  - need_score：4
  - priority：P2
  - reason：旅游VLOG内容轻松有趣，适合放松观看。
  - evidence：标题为欧洲旅游VLOG，包含多个城市
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

### 我关注的前沿咋样了

- **Claude Just Released LIVE Artifacts... (Amazing Results)**
  - 中文解释：Claude 刚刚发布了 Live Artifacts 功能（效果惊人）
  - 来源：AI Foundations
  - 链接：https://www.youtube.com/watch?v=K4_uPtfLfJg
  - 评分：3
  - 摘要：Claude 发布 Live Artifacts 功能，提供持久交互页面以改善工作流管理。
  - need_score：5
  - priority：P0
  - reason：Claude发布Live Artifacts功能是AI工具领域的重要更新，直接影响工作流管理，属于前沿动态。
  - evidence：Claude, Live Artifacts, Cowork sidebar
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **Vol.27 对话汪华、袁进辉、胡修涵：2025年，活下来最重要，但机会一定要抓住**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/67743ca015a5fd520e20815b
  - 评分：4
  - 摘要：一期播客邀请三位AI创业者与投资人复盘2024年AI行业变化，探讨2025年创业策略与技术趋势。
  - need_score：5
  - priority：P0
  - reason：全面覆盖2024年AI前沿动态，包括OpenAI、Scaling Law、Sora、Agent、字节跳动、AI搜索、AI Coding等，对2025年趋势有重要启发。
  - evidence：Scaling Law撞墙, Sora遇冷, 字节爆发, AI应用未爆发, 二次元AI热潮
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：full_push

### 我关心的话题议题有什么新的进展

- **Vol.27 对话汪华、袁进辉、胡修涵：2025年，活下来最重要，但机会一定要抓住**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/67743ca015a5fd520e20815b
  - 评分：4
  - 摘要：一期播客邀请三位AI创业者与投资人复盘2024年AI行业变化，探讨2025年创业策略与技术趋势。
  - need_score：4
  - priority：P1
  - reason：部分匹配关注议题（AI Agent、AI视频生成），提供了行业复盘和趋势更新。
  - evidence：讨论Agent形态, 提及Sora遇冷
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：full_push

### 有什么是我值得看的

- **Vol.27 对话汪华、袁进辉、胡修涵：2025年，活下来最重要，但机会一定要抓住**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/67743ca015a5fd520e20815b
  - 评分：4
  - 摘要：一期播客邀请三位AI创业者与投资人复盘2024年AI行业变化，探讨2025年创业策略与技术趋势。
  - need_score：5
  - priority：P0
  - reason：高价值播客，信息密度高，由多位行业专家提供深度见解，适合AI从业者花时间收听。
  - evidence：高质量嘉宾, 系统复盘2024, 给出2025创业建议
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：full_push

### 系统通知推荐

- **花钱买体验**
  - 来源：Rolen's Blog
  - 链接：https://rolen.wiki/what-are-you-really-buying
  - 评分：4
  - 摘要：文章探讨了将金钱视为能量介质、花钱买体验而非追求回报的思维方式转变。
  - 理由：文章提供了有价值的思维角度，适合阅读并反思个人消费观。
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Vol.27 对话汪华、袁进辉、胡修涵：2025年，活下来最重要，但机会一定要抓住**
  - 来源：小宇宙 Podcast 643928f99361a4e7c38a9555
  - 链接：https://www.xiaoyuzhoufm.com/episode/67743ca015a5fd520e20815b
  - 评分：4
  - 摘要：一期播客邀请三位AI创业者与投资人复盘2024年AI行业变化，探讨2025年创业策略与技术趋势。
  - 理由：内容来自高质量播客，提供行业深度讨论和创业建议，适合AI从业者保存参考
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：full_push

- **一觉醒来发生了什么 05月02日**
  - 来源：一觉醒来发生了什么 - 即刻圈子
  - 链接：https://m.okjike.com/originalPosts/69f531a351a4db608ccb045a
  - 评分：4
  - 摘要：2026年5月2日国内外资讯与即刻社区帖子汇总
  - 理由：常规新闻汇总，信息全面但深度不足，可快速浏览
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

## 5. 失败源列表

无
