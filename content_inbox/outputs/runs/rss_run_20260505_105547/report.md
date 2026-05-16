# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-05T02:55:47+00:00
- 结束时间：2026-05-05T03:06:05+00:00
- 日期：2026-05-05
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：30
- 已处理源数量：30
- 成功源数量：29
- 失败源数量：1
- 已知失败跳过数量：0
- total_items：40
- new_items：40
- duplicate_items：0
- screened_items：40
- recommended_items_from_api_response：3
- new_items_recommended：unknown
- final_inbox_items_from_this_run：3
- full_push_items_from_this_run：3
- incremental_push_items_from_this_run：0
- silent_items：37
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 增量同步模式汇总

- 同步模式：until_existing
- 命中历史锚点的源数：27
- 新源基线同步数：0
- 老源未找到锚点数：2
- selected_items_for_processing 总计：40

**⚠️ 老源未找到锚点 (old_source_no_anchor) 的源列表：**

- **51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台** (其他): This source has history in DB but no existing item was found within probe_limit=20. Processing first 10 items (old_source_no_anchor_limit=20). Possible causes: high-frequency updates, guid/url changes, RSSHub route changes, or dedupe rule changes.
- **新华社新闻_新华网** (党政信息): This source has history in DB but no existing item was found within probe_limit=20. Processing first 20 items (old_source_no_anchor_limit=20). Possible causes: high-frequency updates, guid/url changes, RSSHub route changes, or dedupe rule changes.

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- source concurrency=1, llm_max_concurrency_requested=2, llm_max_concurrency_applied=2, screening_mode_requested=merged, screening_mode_applied=merged, timeout=600, sleep=1.0, limit_per_source=20

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 3 | AI Foundations | Videos | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 10 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 11 | 波士顿圆脸 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 12 | 飞鸟手札 | 短知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 13 | Vista看天下 | 社评 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 3 | 0 |  |
| 14 | 小众软件 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 15 | 猫眼看足球 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 16 | simonwillison.net | 英文博客 | success | 6 | 6 | 0 | 6 | 1 | 3 | 0 | 5 | 0 |  |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 18 | AliAbdaal | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 19 | tanscp | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 20 | 每周一书 – 书伴 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 21 | Ben's Love | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 22 | 新华社新闻_新华网 | 党政信息 | success | 20 | 20 | 0 | 20 | 1 | 1 | 0 | 19 | 0 |  |
| 23 | 潦草学者 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 24 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 25 | 瓶子君152 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 26 | 英语播客党 | 短知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 27 | Tinyfool的个人网站 | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 28 | HelloGithub - 月刊 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 29 | 陈大东瓜 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 30 | jeffgeerling.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

- **决胜局一杆制胜，吴宜泽首夺斯诺克世锦赛冠军**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/3af61e7cf67a4d57aa581c4f227c6d09/c.html
  - 评分：5
  - 摘要：中国选手吴宜泽在斯诺克世锦赛决赛中18:17击败墨菲，夺得职业生涯首个世锦赛冠军。
  - need_score：5
  - priority：P1
  - reason：重大体育赛事夺冠新闻，轻松有趣，适合放松。
  - evidence：标题, 摘要, 正文详细描述比赛过程
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **从“数字次元”到“星空花火” 看沪上年轻人的假日新风尚**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/6e3cbb6cb28b4556b51a833868886258/c.html
  - 评分：3
  - 摘要：上海五一假期推出数字IP活动与夜间烟花秀，展现年轻人假日新风尚
  - need_score：4
  - priority：P0
  - reason：内容轻松有趣，描述假日活动，适合放松。
  - evidence：上海五一假期活动, 年轻人打卡
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **被全网追着嘲了5年，这“千禧年白月光”为啥越挨骂越要唱**
  - 来源：Vista看天下
  - 链接：http://weixin.sogou.com/weixin?query=Vista%E7%9C%8B%E5%A4%A9%E4%B8%8B+%E8%A2%AB%E5%85%A8%E7%BD%91%E8%BF%BD%E7%9D%80%E5%98%B2%E4%BA%865%E5%B9%B4%EF%BC%8C%E8%BF%99%E2%80%9C%E5%8D%83%E7%A6%A7%E5%B9%B4%E7%99%BD%E6%9C%88%E5%85%89%E2%80%9D%E4%B8%BA%E5%95%A5%E8%B6%8A%E6%8C%A8%E9%AA%82%E8%B6%8A%E8%A6%81%E5%94%B1&type=2
  - 评分：4
  - 摘要：深度报道范玮琪近年舆论争议与个人经历，聚焦她参加《乘风2026》的挑战与内心转变。
  - need_score：4
  - priority：P1
  - reason：适合放松阅读的人物故事，有话题性
  - evidence：范玮琪, 乘风2026, 舆论争议
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **韵动节拍丨逐风迎夏 向动而行**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/304e3566784a4bb0987adc4751590dfd/c.html
  - 评分：2
  - 摘要：新华社发布了一组初夏风景摄影作品，展现自然风光和活力，属于轻松的视觉内容。
  - need_score：4
  - priority：P2
  - reason：内容轻松、视觉愉悦，适合放松。
  - evidence：标题和摘要描述初夏美景, 来源权威但非严肃题材
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **U17亚洲杯前瞻：时隔21年，中国男足能否重返世界大赛？**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/b694ad44843b45c29c5135a578f0de02/c.html
  - 评分：3
  - 摘要：新华社报道中国U17男足参加亚洲杯，目标时隔21年重返世少赛，介绍球队阵容、备战情况和小组赛形势。
  - need_score：4
  - priority：P2
  - reason：内容讲述中国足球小将追梦故事，有一定故事性和期待感，适合体育爱好者轻松阅读。
  - evidence：title, summary, content_text
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

### 我关注的前沿咋样了

- **Redis Array Playground**
  - 中文解释：Redis 数组交互式试玩工具
  - 来源：simonwillison.net
  - 链接：https://simonwillison.net/2026/May/4/redis-array
  - 评分：4
  - 摘要：Redis 新增数组数据类型，并可用 Claude Code 构建的 WASM 交互式 playground 测试新命令。
  - need_score：5
  - priority：P0
  - reason：Redis 新增数组数据类型是重要技术更新，且展示了 AI 辅助开发的实践。
  - evidence：Redis 新数据类型 ARRAY, 使用 Claude Code 构建 playground
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Granite 4.1 3B SVG Pelican Gallery**
  - 中文解释：Granite 4.1 3B SVG 鹈鹕画廊
  - 来源：simonwillison.net
  - 链接：https://simonwillison.net/2026/May/4/granite-41-3b-svg-pelican-gallery
  - 评分：3
  - 摘要：作者介绍了 IBM 新发布的 Granite 4.1 系列 LLM，并尝试用不同量化大小的 3B 模型生成 SVG 图片（鹈鹕骑自行车），结果都较差，实验无明显规律。
  - need_score：5
  - priority：P1
  - reason：涉及新模型 Granite 4.1 发布及量化变体实验，有前沿信号。
  - evidence：Granite 4.1, Apache 2.0, GGUF 量化
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **April 2026 newsletter**
  - 中文解释：2026 年 4 月通讯
  - 来源：simonwillison.net
  - 链接：https://simonwillison.net/2026/May/4/april-newsletter
  - 评分：3
  - 摘要：Simon Willison 发布 2026 年 4 月赞助者专属月刊，内容涵盖 Opus 4.7、GPT-5.5 价格调整、Claude Mythos 与 LLM 安全研究、ChatGPT Images 2.0 等 AI 前沿话题。
  - need_score：4
  - priority：P1
  - reason：直接提及 Opus 4.7、GPT-5.5 价格调整及 ChatGPT Images 2.0 等最新模型动态，属于前沿信号。
  - evidence：Opus 4.7, GPT-5.5, ChatGPT Images 2.0
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：skim
  - notification_decision：silent

### 我关心的话题议题有什么新的进展

无

### 有什么是我值得看的

- **决胜局一杆制胜，吴宜泽首夺斯诺克世锦赛冠军**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/3af61e7cf67a4d57aa581c4f227c6d09/c.html
  - 评分：5
  - 摘要：中国选手吴宜泽在斯诺克世锦赛决赛中18:17击败墨菲，夺得职业生涯首个世锦赛冠军。
  - need_score：4
  - priority：P2
  - reason：重要体育新闻，内容扎实，值得花时间阅读。
  - evidence：标题, 摘要
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **浏阳烟花厂爆炸已致21死61伤**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/2bbdc92a9d83421c9ffa8dd060d61b36/c.html
  - 评分：4
  - 摘要：湖南浏阳烟花厂爆炸致21死61伤，救援有序进行。
  - need_score：4
  - priority：P2
  - reason：重大新闻事件，具有信息价值。
  - evidence：官方通报伤亡数据，权威来源
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

### 系统通知推荐

- **决胜局一杆制胜，吴宜泽首夺斯诺克世锦赛冠军**
  - 来源：新华社新闻_新华网
  - 链接：http://www.news.cn/20260505/3af61e7cf67a4d57aa581c4f227c6d09/c.html
  - 评分：5
  - 摘要：中国选手吴宜泽在斯诺克世锦赛决赛中18:17击败墨菲，夺得职业生涯首个世锦赛冠军。
  - 理由：重大体育赛事夺冠报道，内容翔实，适合娱乐放松和新闻阅读。
  - confidence：1.0
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Redis Array Playground**
  - 中文解释：Redis 数组交互式试玩工具
  - 来源：simonwillison.net
  - 链接：https://simonwillison.net/2026/May/4/redis-array
  - 评分：4
  - 摘要：Redis 新增数组数据类型，并可用 Claude Code 构建的 WASM 交互式 playground 测试新命令。
  - 理由：技术前沿动态，Redis 核心数据结构扩展且附有实用演示工具，文章来源可信。
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **被全网追着嘲了5年，这“千禧年白月光”为啥越挨骂越要唱**
  - 来源：Vista看天下
  - 链接：http://weixin.sogou.com/weixin?query=Vista%E7%9C%8B%E5%A4%A9%E4%B8%8B+%E8%A2%AB%E5%85%A8%E7%BD%91%E8%BF%BD%E7%9D%80%E5%98%B2%E4%BA%865%E5%B9%B4%EF%BC%8C%E8%BF%99%E2%80%9C%E5%8D%83%E7%A6%A7%E5%B9%B4%E7%99%BD%E6%9C%88%E5%85%89%E2%80%9D%E4%B8%BA%E5%95%A5%E8%B6%8A%E6%8C%A8%E9%AA%82%E8%B6%8A%E8%A6%81%E5%94%B1&type=2
  - 评分：4
  - 摘要：深度报道范玮琪近年舆论争议与个人经历，聚焦她参加《乘风2026》的挑战与内心转变。
  - 理由：适合娱乐阅读的人物故事，有一定深度但非紧急议题
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

## 5. 失败源列表

- **飞鸟手札**
  - 分类：短知识
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/1366786686
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/1366786686
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/1366786686
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 101] Network is unreachable>"}