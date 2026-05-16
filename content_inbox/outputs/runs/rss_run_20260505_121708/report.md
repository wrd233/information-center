# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-05T04:17:08+00:00
- 结束时间：2026-05-05T05:17:47+00:00
- 日期：2026-05-05
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：482
- 已处理源数量：482
- 成功源数量：469
- 失败源数量：13
- 已知失败跳过数量：0
- total_items：1392
- new_items：1392
- duplicate_items：0
- screened_items：1392
- recommended_items_from_api_response：583
- new_items_recommended：unknown
- final_inbox_items_from_this_run：61
- full_push_items_from_this_run：58
- incremental_push_items_from_this_run：3
- silent_items：965
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 增量同步模式汇总

- 同步模式：until_existing
- 命中历史锚点的源数：197
- 新源基线同步数：270
- 老源未找到锚点数：2
- selected_items_for_processing 总计：1392

**⚠️ 老源未找到锚点 (old_source_no_anchor) 的源列表：**

- **51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台** (其他): This source has history in DB but no existing item was found within probe_limit=20. Processing first 10 items (old_source_no_anchor_limit=20). Possible causes: high-frequency updates, guid/url changes, RSSHub route changes, or dedupe rule changes.
- **🔔科技频道[奇诺分享-ccino.org]⚡️** (科技与编程): This source has history in DB but no existing item was found within probe_limit=20. Processing first 20 items (old_source_no_anchor_limit=20). Possible causes: high-frequency updates, guid/url changes, RSSHub route changes, or dedupe rule changes.

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- source concurrency=8, llm_max_concurrency_requested=6, llm_max_concurrency_applied=6, screening_mode_requested=merged, screening_mode_applied=merged, timeout=600, sleep=1.0, limit_per_source=20

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 2 | tanscp | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 3 | Airing 的博客 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 5 | Ben's Love | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 6 | 莫比乌斯 | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 7 | 白熊阿丸的小屋 | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 8 | 草稿拾遗 | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 9 | Paradise Lost | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 10 | 笨方法学写作 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 11 | StarYuhen | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 12 | Experimental History | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 13 | Blog - Remote Work Prep | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 14 | EVANGELION:ALL | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 15 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 10 | 0 |  |
| 16 | 今日热榜 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 17 | 安全代码 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 18 | 老T博客 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 19 | 小众软件 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 20 | HelloGithub - 月刊 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 21 | 宝玉的分享 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 22 | 阮一峰的网络日志 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 23 | 龙爪槐守望者 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 24 | 十年之约聚合订阅 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 25 | #UNTAG | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 26 | 混沌周刊 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 27 | 🔔科技频道[奇诺分享-ccino.org]⚡️ | 科技与编程 | success | 20 | 20 | 0 | 20 | 5 | 6 | 0 | 18 | 0 |  |
| 28 | 猴猴说话 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 29 | 潦草学者 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 30 | L先生说 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 31 | 常青说 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 32 | 啊桂实验室 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 33 | 大问题Dialectic | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 34 | ONE字幕组 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 35 | everystep | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 36 | 走路 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 37 | Vista看天下 | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 38 | Tinyfool的个人网站 | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 39 | 刘夙的科技世界 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 40 | 三联生活周刊 Lifeweek | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 41 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 42 | - 政府文件库 | 国内政策 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 43 | 不如读书 | Articles | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 44 | Lukas Petersson’s blog | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 45 | 偷懒爱好者周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 46 | GeekPlux Letters | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 47 | 信息差——独立开发者出海周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 48 | joojen Zhou 的网站 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 49 | 周刊 归档 - 酷口家数字花园 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 50 | 莫尔索随笔 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 51 | Ahead of AI | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 52 | 歸藏的AI工具箱 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | content_inbox_error |
| 53 | Kubernetes Blog | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 54 | AI洞察日报 RSS Feed | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 55 | 最新发布_共产党员网 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 56 | 新华社新闻_新华网 | 党政信息 | success | 8 | 8 | 0 | 8 | 1 | 0 | 0 | 8 | 0 |  |
| 57 | 半月谈快报 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 58 | - 求是网 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 59 | 学习一下订阅源 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 60 | Lex Fridman Podcast | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 61 | Podnews Daily - podcast industry news | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 62 | 新智元 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 63 | 机器之心 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 64 | 腾讯研究院 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 65 | 极客公园 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 66 | 极客公园 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 67 | 图书推荐 – 书伴 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 68 | 每周一书 – 书伴 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 69 | 笔记交流站 - 即刻圈子 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 70 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 71 | Mike Krieger(@mikeyk) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 72 | Richard Socher(@RichardSocher) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 73 | Hugging Face(@huggingface) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 74 | 小互(@imxiaohu) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 75 | AI at Meta(@AIatMeta) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 76 | Mistral AI(@MistralAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 77 | xAI(@xai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 78 | Dia(@diabrowser) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 79 | AI Breakfast(@AiBreakfast) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 80 | DeepSeek(@deepseek_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 81 | Jim Fan(@DrJimFan) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 82 | Akshay Kothari(@akothari) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 83 | 歸藏(guizang.ai)(@op7418) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 84 | Notion(@NotionHQ) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 85 | Replicate(@replicate) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 86 | lmarena.ai(@lmarena_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 87 | Poe(@poe_platform) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 88 | Ray Dalio(@RayDalio) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 89 | Arthur Mensch(@arthurmensch) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 90 | Paul Graham(@paulg) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 91 | Browser Use(@browser_use) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 92 | The Rundown AI(@TheRundownAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 93 | AI Will(@FinanceYF5) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 94 | Guillermo Rauch(@rauchg) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 95 | 向阳乔木(@vista8) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 96 | Nick St. Pierre(@nickfloats) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 97 | Sahil Lavingia(@shl) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 98 | Jan Leike(@janleike) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 99 | Gary Marcus(@GaryMarcus) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 100 | Monica_IM(@hey_im_monica) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 101 | Lenny Rachitsky(@lennysan) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 102 | Kling AI(@Kling_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 103 | Lilian Weng(@lilianweng) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 104 | Aadit Sheth(@aaditsh) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 105 | Augment Code(@augmentcode) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 106 | Skywork(@Skywork_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 107 | Firecrawl(@firecrawl_dev) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 108 | Adam D'Angelo(@adamdangelo) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 109 | Suhail(@Suhail) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 110 | Sualeh Asif(@sualehasif996) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 111 | Anthropic(@AnthropicAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 112 | AI Engineer(@aiDotEngineer) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 113 | Hailuo AI (MiniMax)(@Hailuo_AI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 114 | Fireworks AI(@FireworksAI_HQ) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 115 | Justine Moore(@venturetwins) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 116 | OpenAI Developers(@OpenAIDevs) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 117 | bolt.new(@boltdotnew) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 118 | Midjourney(@midjourney) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 119 | eric zakariasson(@ericzakariasson) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 120 | Sam Altman(@sama) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 121 | clem &#129303;(@ClementDelangue) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 122 | LangChain(@LangChainAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 123 | orange.ai(@oran_ge) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 124 | Dario Amodei(@DarioAmodei) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 125 | Geoffrey Hinton(@geoffreyhinton) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 126 | Harrison Chase(@hwchase17) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 127 | Kevin Weil &#127482;&#127480;(@kevinweil) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 128 | Jeff Dean(@JeffDean) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 129 | Perplexity(@perplexity_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 130 | ChatGPT(@ChatGPTapp) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 131 | Berkeley AI Research(@berkeley_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 132 | Paul Couvert(@itsPaulAi) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 133 | Barsee &#128054;(@heyBarsee) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 134 | OpenAI(@OpenAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 135 | Binyuan Hui(@huybery) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 136 | cohere(@cohere) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 137 | Aman Sanger(@amanrsanger) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 138 | Simon Willison(@simonw) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 139 | Microsoft Research(@MSFTResearch) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 140 | Yann LeCun(@ylecun) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 141 | Junyang Lin(@JustinLin610) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 142 | Alex Albert(@alexalbert__) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 143 | Aravind Srinivas(@AravSrinivas) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 144 | Genspark(@genspark_ai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 145 | Greg Brockman(@gdb) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 146 | elvis(@omarsar0) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 147 | Google AI(@GoogleAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 148 | LlamaIndex &#129433;(@llama_index) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 149 | Jerry Liu(@jerryjliu0) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 150 | Marc Andreessen &#127482;&#127480;(@pmarca) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 151 | Justin Welsh(@thejustinwelsh) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 152 | Pika(@pika_labs) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 153 | Sundar Pichai(@sundarpichai) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 154 | Lovable(@lovable_dev) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 155 | cat(@_catwu) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 156 | Anton Osika – eu/acc(@antonosika) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 157 | Replit ⠕(@Replit) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 158 | FlowiseAI(@FlowiseAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 159 | a16z(@a16z) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 160 | 李继刚(@lijigang_com) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 161 | Jina AI(@JinaAI_) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 162 | v0(@v0) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 163 | Andrej Karpathy(@karpathy) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 164 | Fei-Fei Li(@drfeifei) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 165 | DeepLearning.AI(@DeepLearningAI) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 166 | Rowan Cheung(@rowancheung) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 2 | 0 | 3 | 0 |  |
| 167 | Latent.Space(@latentspacepod) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 4 | 0 |  |
| 168 | Ideogram(@ideogram_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 1 | 3 | 1 | 4 | 0 |  |
| 169 | Demis Hassabis(@demishassabis) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 170 | Cognition(@cognition_labs) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 171 | andrew chen(@andrewchen) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 3 | 0 |  |
| 172 | NVIDIA AI(@NVIDIAAI) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 173 | Stanford AI Lab(@StanfordAILab) | SocialMedia | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 174 | Varun Mohan(@_mohansolo) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 4 | 0 |  |
| 175 | Logan Kilpatrick(@OfficialLoganK) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 176 | Qdrant(@qdrant_engine) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 1 | 3 | 0 |  |
| 177 | OpenRouter(@OpenRouterAI) | SocialMedia | success | 5 | 5 | 0 | 5 | 1 | 3 | 0 | 4 | 0 |  |
| 178 | Thomas Wolf(@Thom_Wolf) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 179 | mem0(@mem0ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 2 | 0 | 3 | 0 |  |
| 180 | Scott Wu(@ScottWu46) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 3 | 0 |  |
| 181 | Recraft(@recraftai) | SocialMedia | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 182 | Hunyuan(@TXhunyuan) | SocialMedia | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 183 | Google DeepMind(@GoogleDeepMind) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 2 | 0 |  |
| 184 | Mustafa Suleyman(@mustafasuleyman) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 5 | 0 | 3 | 0 |  |
| 185 | Y Combinator(@ycombinator) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 3 | 1 | 2 | 0 |  |
| 186 | Lex Fridman(@lexfridman) | SocialMedia | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 187 | Fellou(@FellouAI) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 4 | 0 |  |
| 188 | Runway(@runwayml) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 3 | 0 |  |
| 189 | Julien Chaumond(@julien_c) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 2 | 0 | 3 | 0 |  |
| 190 | 宝玉(@dotey) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 191 | Milvus(@milvusio) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 2 | 0 |  |
| 192 | Ian Goodfellow(@goodfellow_ian) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 2 | 0 | 4 | 0 |  |
| 193 | Taranjeet(@taranjeetio) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |
| 194 | Figma(@figma) | SocialMedia | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 5 | 0 |  |
| 195 | Patrick Loeber(@patloeber) | SocialMedia | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 196 | Windsurf(@windsurf_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |
| 197 | Google AI Developers(@googleaidevs) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 4 | 0 |  |
| 198 | Qwen(@Alibaba_Qwen) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 3 | 0 |  |
| 199 | Satya Nadella(@satyanadella) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 200 | Andrew Ng(@AndrewYNg) | SocialMedia | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 201 | AI SDK(@aisdk) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 202 | HeyGen(@HeyGen_Official) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 203 | Fish Audio(@FishAudio) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 204 | ElevenLabs(@elevenlabsio) | SocialMedia | success | 5 | 5 | 0 | 5 | 1 | 1 | 1 | 4 | 0 |  |
| 205 | ollama(@ollama) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 4 | 0 | 3 | 0 |  |
| 206 | Philipp Schmid(@_philschmid) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 3 | 1 | 2 | 0 |  |
| 207 | Cursor(@cursor_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |
| 208 | Google Gemini App(@GeminiApp) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 2 | 1 | 4 | 0 |  |
| 209 | Amjad Masad(@amasad) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 3 | 0 |  |
| 210 | AK(@_akhaliq) | SocialMedia | success | 5 | 5 | 0 | 5 | 5 | 3 | 0 | 2 | 0 |  |
| 211 | Groq Inc(@GroqInc) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 4 | 0 |  |
| 212 | ManusAI(@ManusAI_HQ) | SocialMedia | success | 5 | 5 | 0 | 5 | 5 | 3 | 0 | 2 | 0 |  |
| 213 | meng shao(@shao__meng) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 3 | 1 | 1 | 0 |  |
| 214 | Weaviate • vector database(@weaviate_io) | SocialMedia | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 215 | LovartAI(@lovart_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 216 | Character.AI(@character_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 1 | 4 | 0 |  |
| 217 | NotebookLM(@NotebookLM) | SocialMedia | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 2 | 0 |  |
| 218 | Dify(@dify_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 5 | 0 | 2 | 0 |  |
| 219 | Eric Jing(@ericjing_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 0 | 2 | 3 | 0 |  |
| 220 | Naval(@naval) | SocialMedia | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 4 | 0 |  |
| 221 | Lee Robinson(@leerob) | SocialMedia | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 222 | AliAbdaal | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 223 | 食事史馆 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 224 | 毕导 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 225 | CoCoVii | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 226 | 下班的三爷 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 227 | 本子在隔壁 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 228 | 岱川博士 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 229 | 退役编辑雨上 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 230 | 与书籍度过漫长岁月 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 231 | 智能路障 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 232 | Nenly同学 | 长知识 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 233 | 大问题Dialectic | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 234 | 英语播客狗 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 235 | 林川登罗 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 236 | 人间自习室 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 237 | 漫士沉思录 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 4 | 0 |  |
| 238 | 银屏系漫游指南 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 3 | 0 | 5 | 0 |  |
| 239 | 浮世叁千问 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 240 | LunaticMosfet | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 241 | 歌白说Geslook | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 0 | 0 | 5 | 0 |  |
| 242 | Larry想做技术大佬 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 243 | 赏味不足 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 244 | 西山在何许 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 245 | 坚果熊说博弈 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 246 | 罗明落ny | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 0 | 0 | 5 | 0 |  |
| 247 | 汤质看本质 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 5 | 0 |  |
| 248 | 要素分析 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 249 | 蒙克MK_ | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 250 | Morpheus红丸主义 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 251 | 慢慢学的四饼 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 252 | 辰星杂谈 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 253 | 非卿漫谈 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 254 | 拣尽南枝 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 255 | 硬核学长2077 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 256 | 海林A读书 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 257 | 机器人夏先生1号 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 258 | 知识共享者 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 259 | Maki的完美算术教室 | 长知识 | success | 5 | 5 | 0 | 5 | 3 | 1 | 0 | 4 | 0 |  |
| 260 | 心河摆渡 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 261 | 猴猴说话 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 0 | 0 | 5 | 0 |  |
| 262 | 3Blue1Brown | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 263 | 思维实验室 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 264 | 是落拓呀 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 265 | 学院派Academia | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 266 | 和张程一起学习吧 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 267 | 读书的Harry | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 268 | 小波心理 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 5 | 0 |  |
| 269 | 科幻视界 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 5 | 0 |  |
| 270 | 差评君 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 271 | 迷因水母 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 272 | 努力戒咕的coco锤 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 273 | 河口超人Aper | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 274 | 荒野初研园 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 275 | 二次元的Datawhale | 长知识 | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 2 | 0 |  |
| 276 | 白染one | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 0 | 0 | 5 | 0 |  |
| 277 | 卡纸大寨主 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 278 | 向杨Alan君 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 279 | 奥德修斯的绳索 | 长知识 | success | 5 | 5 | 0 | 5 | 3 | 0 | 0 | 5 | 0 |  |
| 280 | 岺玖贰叁 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 281 | 新石器公园 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 282 | 载脑体 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 283 | YouTube深度访谈 | 长知识 | success | 5 | 5 | 0 | 5 | 2 | 0 | 0 | 5 | 0 |  |
| 284 | 天才简史 | 长知识 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 285 | 这是个令人疑惑的星球 | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 286 | 周侃侃plus | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 287 | focus2flow | 长知识 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 288 | 飞鸟手札 | 短知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 289 | 英语播客党 | 短知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 290 | 波士顿圆脸 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 291 | 瓶子君152 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 292 | Super也好君 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 293 | 负面能量转换器 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 294 | 靠谱电竞 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 295 | 火兰朋克 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 296 | 馆长刘下饭_环球档案 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 297 | 老实憨厚的笑笑 | 最娱乐 | success | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |  |
| 298 | 冲击波工作室 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 299 | 邵艾伦Alan | 最娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 300 | 柯洁 | 最娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 301 | 逗比的雀巢 | 最娱乐 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 302 | 大祥哥来了 | 最娱乐 | success | 5 | 5 | 0 | 5 | 0 | 3 | 0 | 5 | 0 |  |
| 303 | Norah脱口秀 | 最娱乐 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 304 | 巅峰球迷汇 | 最娱乐 | success | 5 | 5 | 0 | 5 | 0 | 2 | 0 | 5 | 0 |  |
| 305 | MrBeast官方账号 | 最娱乐 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 2 | 0 |  |
| 306 | 泛式 | 最娱乐 | success | 5 | 5 | 0 | 5 | 1 | 4 | 0 | 4 | 0 |  |
| 307 | 贝拉kira | 最娱乐 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 5 | 0 |  |
| 308 | -LKs- | 最娱乐 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 309 | 真实球迷汇 | 最娱乐 | success | 5 | 5 | 0 | 5 | 1 | 3 | 0 | 4 | 0 |  |
| 310 | 李滇滇 | 最娱乐 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 5 | 0 |  |
| 311 | 影视飓风 | 最娱乐 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 312 | 猫眼看足球 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 313 | 陈大东瓜 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 314 | 司马尘 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 315 | 是啤酒鸭-梗图 | 绝活娱乐 | success | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |  |
| 316 | MOJi辞書 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 317 | Gray格雷老师 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 318 | 你是想气死1酱么 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 319 | Boo布姐自译 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 320 | 冲男阿凉 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 321 | 杰克森Jackson_ | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 322 | 半只笨猪 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 323 | 脱口秀_Talk_Show | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 5 | 0 |  |
| 324 | 罗翔说刑法 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 325 | 付航脱口秀精选 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 5 | 0 |  |
| 326 | 戴建业老师 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 327 | 听泉赏宝 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 328 | 灯果 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 329 | 隔壁红魔 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 330 | 管泽元 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 331 | 白马繁华 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 332 | 咖啡醉足球 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 5 | 0 |  |
| 333 | 单弦震脉 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 334 | 米国脱口秀 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 335 | 付航脱口秀 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 336 | 峡谷玄学家 | 绝活娱乐 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 337 | AI Foundations | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 338 | simonwillison.net | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 339 | jeffgeerling.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 340 | seangoedecke.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 341 | krebsonsecurity.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 342 | daringfireball.net | 英文博客 | success | 13 | 13 | 0 | 13 | 3 | 5 | 0 | 10 | 0 |  |
| 343 | ericmigi.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 344 | antirez.com | 英文博客 | success | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 |  |
| 345 | idiallo.com | 英文博客 | success | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 |  |
| 346 | maurycyz.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 347 | pluralistic.net | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 348 | shkspr.mobi | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 349 | lcamtuf.substack.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 350 | mitchellh.com | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 2 | 0 | 5 | 0 |  |
| 351 | dynomight.net | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 352 | utcc.utoronto.ca/~cks | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 353 | xeiaso.net | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 354 | devblogs.microsoft.com/oldnewthing | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 4 | 0 |  |
| 355 | righto.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 356 | lucumr.pocoo.org | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 357 | skyfall.dev | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 5 | 0 |  |
| 358 | garymarcus.substack.com | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 359 | rachelbythebay.com | 英文博客 | success | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |  |
| 360 | overreacted.io | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 1 | 0 | 5 | 0 |  |
| 361 | timsh.org | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 362 | johndcook.com | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 363 | gilesthomas.com | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 2 | 0 |  |
| 364 | matklad.github.io | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |
| 365 | derekthompson.org | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 366 | evanhahn.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 4 | 0 | 4 | 0 |  |
| 367 | terriblesoftware.org | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 4 | 0 | 3 | 0 |  |
| 368 | rakhim.exotext.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 369 | joanwestenberg.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 370 | xania.org | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 3 | 0 |  |
| 371 | micahflee.com | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 372 | nesbitt.io | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 373 | construction-physics.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 374 | tedium.co | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 375 | susam.net | 英文博客 | success | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 1 | 0 |  |
| 376 | entropicthoughts.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 0 | 0 | 5 | 0 |  |
| 377 | buttondown.com/hillelwayne | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 378 | dwarkesh.com | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 2 | 0 |  |
| 379 | borretti.me | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 380 | wheresyoured.at | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 4 | 1 | 0 | 0 |  |
| 381 | jayd.ml | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 382 | minimaxir.com | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 4 | 1 | 0 | 0 |  |
| 383 | geohot.github.io | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 384 | paulgraham.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 5 | 0 |  |
| 385 | filfre.net | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 1 | 0 | 4 | 0 |  |
| 386 | blog.jim-nielsen.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 3 | 0 |  |
| 387 | dfarq.homeip.net | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 388 | jyn.dev | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 3 | 0 | 5 | 0 |  |
| 389 | geoffreylitt.com | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 390 | downtowndougbrown.com | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 391 | brutecat.com | 英文博客 | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 2 | 0 |  |
| 392 | eli.thegreenplace.net | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 2 | 0 | 5 | 0 |  |
| 393 | abortretry.fail | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 394 | fabiensanglard.net | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 395 | oldvcr.blogspot.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 396 | bogdanthegeek.github.io | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 397 | hugotunius.se | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 398 | gwern.net | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 4 | 1 | 0 | 0 |  |
| 399 | berthub.eu | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 400 | chadnauseam.com | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 0 | 0 | 5 | 0 |  |
| 401 | simone.org | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 1 | 0 | 4 | 0 |  |
| 402 | it-notes.dragas.net | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 403 | beej.us | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 0 | 0 | 5 | 0 |  |
| 404 | hey.paris | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 405 | danielwirtz.com | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 1 | 0 | 5 | 0 |  |
| 406 | matduggan.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 4 | 0 | 3 | 0 |  |
| 407 | refactoringenglish.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 408 | worksonmymachine.substack.com | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 409 | philiplaine.com | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 410 | steveblank.com | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 2 | 0 |  |
| 411 | bernsteinbear.com | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 412 | danieldelaney.net | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 413 | troyhunt.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 3 | 0 |  |
| 414 | herman.bearblog.dev | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 3 | 0 |  |
| 415 | tomrenner.com | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |
| 416 | blog.pixelmelt.dev | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 417 | martinalderson.com | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 418 | danielchasehooper.com | 英文博客 | success | 5 | 5 | 0 | 5 | 1 | 2 | 0 | 4 | 0 |  |
| 419 | chiark.greenend.org.uk/~sgtatham | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 420 | grantslatton.com | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 421 | anildash.com | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 2 | 0 |  |
| 422 | aresluna.org | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 423 | michael.stapelberg.ch | 英文博客 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 424 | miguelgrinberg.com | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 1 | 3 | 0 |  |
| 425 | keygen.sh | 英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 426 | mjg59.dreamwidth.org | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 427 | computer.rip | 英文博客 | success | 5 | 5 | 0 | 5 | 2 | 2 | 0 | 3 | 0 |  |
| 428 | tedunangst.com | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 429 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 430 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 431 | 小宇宙 Podcast 648b0b641c48983391a63f98 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 432 | 小宇宙 Podcast 5e5c52c9418a84a04625e6cc | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 433 | 小宇宙 Podcast 63b7dd49289d2739647d9587 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 434 | 小宇宙 Podcast 6507bc165c88d2412626b401 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 435 | Lil'Log | 英文博客 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 436 | Very Small Woods | 英文博客 | success | 5 | 5 | 0 | 5 | 3 | 5 | 0 | 2 | 0 |  |
| 437 | 数字生命卡兹克 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 4 | 0 | 2 | 0 |  |
| 438 | AGI Hunt | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 2 | 0 |  |
| 439 | 卡尔的AI沃茨 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 0 | 0 |  |
| 440 | 赛博禅心 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 3 | 1 | 2 | 0 |  |
| 441 | AI产品黄叔 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 3 | 0 |  |
| 442 | 网罗灯下黑 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 4 | 0 |  |
| 443 | 苍何 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 3 | 0 |  |
| 444 | 饼干哥哥AGI | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 2 | 0 |  |
| 445 | 刘聪NLP | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 3 | 0 | 4 | 0 |  |
| 446 | AI产品阿颖 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 3 | 0 |  |
| 447 | 01Founder | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 3 | 1 | 4 | 0 |  |
| 448 | AI故事计划 | 微信公众号 | success | 5 | 5 | 0 | 5 | 2 | 3 | 0 | 4 | 0 |  |
| 449 | 十字路口Crossing | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |
| 450 | 沃垠AI | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 4 | 0 | 3 | 0 |  |
| 451 | 阿伦AI学习笔记 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 1 | 0 |  |
| 452 | 胡说成理 | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 453 | 云中江树 | 微信公众号 | success | 5 | 5 | 0 | 5 | 1 | 3 | 0 | 5 | 0 |  |
| 454 | 秋芝2046 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 3 | 0 |  |
| 455 | AI产品银海 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 1 | 0 |  |
| 456 | 哥飞 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 2 | 0 | 4 | 0 |  |
| 457 | 探索AGI | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 458 | 新智元 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 459 | 量子位 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 2 | 0 |  |
| 460 | APPSO | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 461 | 智东西 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 462 | 雷峰网 | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 4 | 0 |  |
| 463 | PaperWeekly | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 4 | 0 | 2 | 0 |  |
| 464 | 甲子光年 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 465 | 逛逛GitHub | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 2 | 0 |  |
| 466 | 开源AI项目落地 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 4 | 0 | 1 | 0 |  |
| 467 | 夕小瑶科技说 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 468 | Datawhale | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 2 | 0 |  |
| 469 | 极客公园 | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 2 | 2 | 1 | 0 |  |
| 470 | AIGC开放社区 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 3 | 0 | 3 | 0 |  |
| 471 | AI前线 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 0 | 0 |  |
| 472 | AI科技评论 | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 5 | 0 | 1 | 0 |  |
| 473 | 脑极体 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 2 | 0 | 5 | 0 |  |
| 474 | 硅星人Pro | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 1 | 2 | 0 |  |
| 475 | 特工宇宙 | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 3 | 0 | 3 | 0 |  |
| 476 | 光子星球 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 3 | 0 |  |
| 477 | CVer | 微信公众号 | success | 5 | 5 | 0 | 5 | 3 | 1 | 0 | 5 | 0 |  |
| 478 | Z Potentials | 微信公众号 | success | 5 | 5 | 0 | 5 | 5 | 4 | 0 | 1 | 0 |  |
| 479 | Z Finance | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 4 | 0 | 1 | 0 |  |
| 480 | 晚点LatePost | 微信公众号 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 |  |
| 481 | InfoQ | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 2 | 1 | 2 | 0 |  |
| 482 | 机器之心 | 微信公众号 | success | 5 | 5 | 0 | 5 | 4 | 5 | 0 | 1 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

- **大厂高管问我：要不要做 Token 消耗榜？**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/T26n4Dt401gb76F8cwBWow
  - 评分：3
  - 摘要：讨论企业跟风 Meta 做 Token 消耗排行榜的现象，分析其对员工生产力的象征性及内卷影响。
  - need_score：4
  - priority：P1
  - reason：语言幽默，话题轻松，适合放松阅读。
  - evidence：标题调侃风格, 摘要中调侃领导没有主见
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **10后，开始用AI给自己编黄冈密卷了**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/6FIFWLvlRZkX3RmBFm1wSw
  - 评分：3
  - 摘要：报道10后青少年使用AI工具（如ChatGPT）来生成类似黄冈密卷的练习题，展现新一代的学习方式。
  - need_score：4
  - priority：P1
  - reason：内容轻松有趣，适合放松阅读。
  - evidence：标题有趣, 摘要暗示现象观察
  - confidence：0.75
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **从灭蚊高手到智能宠物项圈，猎奇AI硬件的市场突围**
  - 来源：脑极体
  - 链接：https://mp.weixin.qq.com/s/LlYW8pnZHAC4y4-a5ou5dQ
  - 评分：3
  - 摘要：文章介绍猎奇AI硬件产品，如灭蚊高手和智能宠物项圈，探讨其市场突围路径。
  - need_score：4
  - priority：P1
  - reason：内容趣味性强，适合放松阅读。
  - evidence：猎奇AI硬件话题轻松有趣
  - confidence：0.7
  - needs_more_context：False
  - suggested_action：review
  - notification_decision：silent

- **五一假期，花半天装个 Claude Code 玩玩？**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/HH3CJnkMT4q1G7vi484PfQ
  - 评分：4
  - 摘要：介绍五一假期安装和使用Claude Code的教程文章
  - need_score：4
  - priority：P2
  - reason：标题带有'玩玩'，风格轻松，适合放松时阅读
  - evidence：标题中的'玩玩', 摘要'想做什么，就做什么'
  - confidence：0.7
  - needs_more_context：False
  - suggested_action：review
  - notification_decision：full_push

- **着相：把“安卓机”变成“影像手机”的这十年**
  - 来源：脑极体
  - 链接：https://mp.weixin.qq.com/s/L_Nss3aN09z8jJPfChxksQ
  - 评分：3
  - 摘要：回顾安卓手机过去十年在影像功能上的进化，从硬件到软件如何将普通手机变为专业的拍摄工具。
  - need_score：4
  - priority：P2
  - reason：内容轻松有趣，适合放松时阅读，符合娱乐需求。
  - evidence：标题和摘要暗示有趣的历史回顾
  - confidence：0.5
  - needs_more_context：True
  - suggested_action：skim
  - notification_decision：silent

- **等 DeepSeek 回复的 30 秒，是手机最好玩的半小时**
  - 来源：APPSO
  - 链接：https://mp.weixin.qq.com/s/bnKUKCiB99hxKN3HJrogKw
  - 评分：2
  - 摘要：调侃 DeepSeek 响应慢，等待期间的手机使用体验
  - need_score：4
  - priority：P2
  - reason：标题有趣，适合轻松阅读
  - evidence：标题调侃方式, 摘要轻松
  - confidence：0.7
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

### 我关注的前沿咋样了

- **别问树模型了！死磕结构化数据，清华团队把大模型表格理解推到极限**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/XA21XWHYt55BLoNeuv2wrg
  - 评分：5
  - 摘要：介绍了清华大学与稳准智能联合发布的LimiX系列结构化数据大模型，展示了其在分类、回归、缺失值填补等任务上的通用能力和工业落地效果，并开源了轻量级版本LimiX-2M。
  - need_score：5
  - priority：P0
  - reason：结构化数据大模型是AI前沿的重要突破，具有范式意义。
  - evidence：LimiX模型, 通用表格理解, 多项性能SOTA
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Meta超级智能实验室又发论文，模型混一混，性能直接SOTA**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/mK2E3qs0E2hs7SpKuJZcIA
  - 评分：4
  - 摘要：Meta提出SoCE方法，通过对不同类别模型进行非均匀加权平均融合，在多个基准上取得SOTA性能。
  - need_score：5
  - priority：P0
  - reason：重要AI前沿研究，新型模型融合方法取得SOTA
  - evidence：Meta, SoCE, BFCL SOTA
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **王兴兴亲测后点赞！这家AI公司提前半年把“龙虾”能力带上车，还管住了Token黑洞**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/PJSCqKBt_ikEDJ7wl-CHpg
  - 评分：4
  - 摘要：宇树科技创始人王兴兴体验宝马新世代i3，称赞其搭载的AI能力（代号'龙虾'），并解决了Token消耗问题。
  - need_score：5
  - priority：P0
  - reason：涉及AI产品在汽车上的重要动态，有明确前沿信号。
  - evidence：王兴兴, 宝马, Token黑洞
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：silent

- **超越 VTM-RA！快手双向智能视频编码器BRHVC亮相NeurIPS2025**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/Mlx1MLD_-4W76V6ck88V-Q
  - 评分：4
  - 摘要：快手提出BRHVC双向智能视频编码方法，在NeurIPS 2025亮相，压缩性能超越标准VTM-RA编码。
  - need_score：5
  - priority：P0
  - reason：介绍超越VTM-RA的智能视频编码新方法，属于AI技术前沿，提供重要技术信号。
  - evidence：标题明确超越VTM-RA, 摘要和正文详细说明技术方案与实验效果
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **“如果你不用更多Token，就永远逃不出底层”：AI竞赛开始变成资源战争**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/uP_cZBXgyC1eaMOO-meutQ
  - 评分：4
  - 摘要：AI模型Token供应紧张，顶级模型开始限量供应，AI竞赛变成资源战争
  - need_score：5
  - priority：P0
  - reason：涉及AI模型资源配给制这一重要前沿动态
  - evidence：标题提及AI竞赛变成资源战争, 摘要提及顶级模型限量供应
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：save
  - notification_decision：incremental_push

- **五一假期，花半天装个 Claude Code 玩玩？**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/HH3CJnkMT4q1G7vi484PfQ
  - 评分：4
  - 摘要：介绍五一假期安装和使用Claude Code的教程文章
  - need_score：5
  - priority：P0
  - reason：涉及Claude Code这一前沿AI Agent工具，可能影响工具选择
  - evidence：Claude Code, AI前沿
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **当国产模型追上闭源旗舰，企业 AI 编程的真正障碍才浮出水面**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/FjLOIWT1JKq4er3TEz8aow
  - 评分：4
  - 摘要：文章探讨国产AI模型能力追平闭源旗舰后，企业AI编程面临的真正障碍，如组织流程、工程实践等。
  - need_score：5
  - priority：P0
  - reason：涉及企业AI编程的前沿障碍和国产模型动态。
  - evidence：AI编程, 国产模型, 闭源旗舰
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **无需训练、只优化解码策略，DTS框架让大模型推理准确率提升6%，推理长度缩短23%**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/JEWHmqctZlhe-7zq5G_Raw
  - 评分：5
  - 摘要：DTS框架通过稀疏化解码树搜索和早停策略，无需训练即可提升大模型推理准确率并缩短推理长度。
  - need_score：5
  - priority：P0
  - reason：涉及大模型推理前沿突破，无需训练即可提升准确率和效率
  - evidence：DTS框架, DeepSeek-R1-Distill-Qwen, AIME基准提升
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **速递｜DeepSeek 多模态功能开始灰度内测，北大校友陈小康带队**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/8enK4u3koAfdP9yRB2Y0Aw
  - 评分：4
  - 摘要：DeepSeek 多模态功能开始灰度内测，由北大校友陈小康带队，公司正加速产品化。
  - need_score：5
  - priority：P0
  - reason：涉及 DeepSeek 多模态功能内测，重要前沿动态。
  - evidence：DeepSeek, 多模态
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **速递｜Microsoft放弃OpenAI独家销售权，OpenAI进驻其他云计算平台？**
  - 来源：Z Potentials
  - 链接：https://mp.weixin.qq.com/s/sXQ8K3TyZApXd2SlqF21QQ
  - 评分：4
  - 摘要：微软放弃OpenAI独家销售权，OpenAI将能进驻其他云计算平台，标志双方合作模式重大变化。
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品动态，微软与OpenAI关系变化是前沿趋势信号。
  - evidence：微软放弃独家销售权, OpenAI进驻其他云平台
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **对话EverMind：4个月做到SOTA，要给所有Agent装上长期记忆**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/ENJYzhAEH4C1th6TgzQtqQ
  - 评分：4
  - 摘要：EverMind 推出 SOTA 级别的 Agent 长期记忆产品，旨在提升所有智能体的记忆能力。
  - need_score：5
  - priority：P0
  - reason：Agent 长期记忆是重要前沿方向，EverMind 达到 SOTA 是标志性进展。
  - evidence：EverMind, Agent 长期记忆, SOTA
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **跑出首个万亿级大模型后，国产算力通过第一场大考**
  - 来源：光子星球
  - 链接：https://mp.weixin.qq.com/s/gAB0kvNW4pQ_CxjNzU-4Mg
  - 评分：5
  - 摘要：国产大模型突破万亿参数，国产算力通过首个大规模训练考验，Token经济学成新焦点。
  - need_score：5
  - priority：P0
  - reason：国产大模型突破万亿参数是AI前沿重大事件，算力进展直接影响模型发展。
  - evidence：万亿级大模型, 国产算力
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **速递｜Meta收购Manus被正式叫停，国家发改委要求撤销交易**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/CRr0VirGW6YlOzoXqLOewg
  - 评分：4
  - 摘要：Meta收购AI产品Manus被中国发改委正式叫停并要求撤销交易
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品收购被监管叫停，属于前沿动态
  - evidence：Meta, Manus, 国家发改委
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **独家｜前蔚来AI平台负责人白宇利创立「补天石科技」，聚焦具身数据 Infra 方向**
  - 来源：AI科技评论
  - 链接：https://mp.weixin.qq.com/s/iZNTljyU8rYp-AvY6iewXA
  - 评分：4
  - 摘要：前蔚来AI负责人白宇利创立补天石科技，聚焦具身数据Infra，获红杉领投。
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品动态，具身数据Infra是前沿方向。
  - evidence：白宇利, 补天石科技, 具身数据Infra, 红杉领投
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：review
  - notification_decision：full_push

- **DeepSeek首次有了视觉能力，技术论文却被它连夜删掉了**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/yjctJS4kVIssj1N3uEOPTQ
  - 评分：5
  - 摘要：DeepSeek首次推出视觉能力（多模态），但相关技术论文被连夜撤下，引发外界关注
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品动态，DeepSeek首次视觉能力是前沿信号
  - evidence：DeepSeek, 视觉能力, 多模态
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：review
  - notification_decision：full_push

- **开源SOTA！商汤原生多模态一个大脑完成看图、推理、作画**
  - 来源：AIGC开放社区
  - 链接：https://mp.weixin.qq.com/s/FxubSRfZPdCykhmNY9C-4A
  - 评分：4
  - 摘要：商汤发布开源多模态模型SenseNova U1，支持看图、推理、作画。
  - need_score：5
  - priority：P0
  - reason：开源多模态模型是重要前沿动态。
  - evidence：开源SOTA, 多模态, 商汤
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **DeepSeek 发布多模态模型及技术报告；小红书官宣组织调整：柯南出任总裁；宇树发布双臂人形机器人，2.69万元起售 \| 极客早知道**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/nDjyRtoi2vsU88bqSZDklQ
  - 评分：4
  - 摘要：汇总了DeepSeek发布多模态模型、小红书组织调整、宇树人形机器人等科技新闻
  - need_score：5
  - priority：P0
  - reason：涉及DeepSeek多模态模型、宇树人形机器人等前沿动态
  - evidence：DeepSeek多模态, 双臂人形机器人
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：incremental_push

- **首次大规模真实世界验证：机器人边部署边进化，8项任务全面碾压基线**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/k3LAWmyt5u_Nwpx2agYxEg
  - 评分：5
  - 摘要：机器人边部署边进化首次大规模真实世界验证，在8项任务上全面超越基线。
  - need_score：5
  - priority：P0
  - reason：提供了机器人领域重要的前沿动态，首次大规模真实世界验证。
  - evidence：机器人, 边部署边进化, 8项任务
  - confidence：0.92
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **22年的提示词技巧过时了！刚刚，吴恩达新课来了**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/be_Y52RbQXBIyaqra1aAig
  - 评分：5
  - 摘要：吴恩达发布新课，指出2022年的提示词技巧已过时，带来最新AI提示词工程方法。
  - need_score：5
  - priority：P0
  - reason：涉及吴恩达新课，更新提示词技巧，是AI领域重要前沿动态。
  - evidence：吴恩达新课, 提示词技巧更新
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **ICLR最佳论文：Transformer天生简洁**
  - 来源：AIGC开放社区
  - 链接：https://mp.weixin.qq.com/s/D67IK_p6Ez2txx3PW4SkMg
  - 评分：5
  - 摘要：ICLR2026最佳论文揭示Transformer架构内在简洁性
  - need_score：5
  - priority：P0
  - reason：ICLR最佳论文是重要前沿信号，Transformer简洁性可能影响后续模型发展
  - evidence：ICLR最佳论文, Transformer架构
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **15小时3.5万Star！Altman投资的AI终端开源炸圈：曾经没人用，如今靠Agent翻身**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/tG3qm1jmrLyf5lBLuIextA
  - 评分：4
  - 摘要：Warp终端客户端开源，基于Rust的Agentic开发环境，获得Altman投资，从无人问津到凭借Agent功能翻红。
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品开源和Agent前沿。
  - evidence：Warp开源, Agent, Altman投资
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **刚刚，DeepSeek最新成果，节前发布！**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/qXl3HK7txW0FUA3itWwMuA
  - 评分：4
  - 摘要：DeepSeek 在节前发布了最新研发成果，文章来自 Datawhale。
  - need_score：5
  - priority：P0
  - reason：涉及重要 AI 产品动态。
  - evidence：DeepSeek, 最新成果
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **DeepSeek多模态要来了，「识图模式」开启灰度**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/lqv95LNC99gP-0a2QejpFQ
  - 评分：4
  - 摘要：DeepSeek即将推出多模态识图功能，已开启灰度测试。
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品动态，多模态是当前AI前沿热点。
  - evidence：DeepSeek, 多模态
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **魔法原子进军硅谷背后：世界模型野望与生态卡位**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/SAhFum2UOuCmDq_5gyT7_Q
  - 评分：4
  - 摘要：中国具身智能公司魔法原子进军硅谷，布局世界模型和生态。
  - need_score：5
  - priority：P0
  - reason：涉及具身智能和世界模型，属于AI重要前沿方向。
  - evidence：具身智能, 世界模型
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：incremental_push

- **图像编辑模型不止生成：BIGAI&上交大提出EAR范式，系统测试其视觉规划能力**
  - 来源：AI科技评论
  - 链接：https://mp.weixin.qq.com/s/2_cDSnke-IwUW6ym-FmJlg
  - 评分：4
  - 摘要：BIGAI和上交大提出EAR范式与AMAZE基准，将视觉规划重构为单步图像编辑任务，测试图像编辑模型的视觉规划能力。
  - need_score：5
  - priority：P0
  - reason：涉及AI领域新研究范式，具有前沿价值。
  - evidence：EAR范式, AMAZE基准, 视觉规划能力
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Agent 超级应用：ChatGPT 用来聊，Codex 干活的时代来了！**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/Cp1f7KpEzZ-PqOI62dNF0Q
  - 评分：5
  - 摘要：介绍Agent超级应用概念：ChatGPT用于对话，Codex用于执行任务，标志AI分工新时代。
  - need_score：5
  - priority：P0
  - reason：讨论Agent超级应用这一重要前沿趋势。
  - evidence：标题提到Agent超级应用, 来源Datawhale常发布前沿技术内容
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **GenFlow4.0，让通用智能体走进办公现场**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/ihjHO3FHCZ4_ODaBRcAr5Q
  - 评分：4
  - 摘要：介绍GenFlow4.0版本，让通用AI智能体应用于办公场景。
  - need_score：5
  - priority：P0
  - reason：产品版本更新，Agent在办公场景应用，属于前沿动态
  - evidence：GenFlow4.0, 通用智能体
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **MiniCPM-o 4.5 技术报告发布：全双工全模态 API 开放，RTX5070 即可实时运行**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/TL5wKLcQRZUS6UA4YcKBGA
  - 评分：4
  - 摘要：MiniCPM-o 4.5 技术报告发布，支持全双工全模态 API，RTX5070 可实时运行，并提供一键安装包。
  - need_score：5
  - priority：P0
  - reason：涉及重要AI模型发布动态，低门槛全双工全模态，具有前沿价值。
  - evidence：MiniCPM-o 4.5, 全双工全模态, RTX5070
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **3.3k星星爆火！Claude Design开源升级版，中文本地化，支持DeepSeek V4**
  - 来源：开源AI项目落地
  - 链接：https://mp.weixin.qq.com/s/9VablWhs-7dThLqTlH8KHg
  - 评分：4
  - 摘要：Claude Design 开源升级版发布，新增中文本地化和 DeepSeek V4 支持，UI 可局部重写，在 GitHub 获 3.3k 星。
  - need_score：5
  - priority：P0
  - reason：涉及重要AI产品动态，开源升级和模型集成。
  - evidence：DeepSeek V4, Claude Design开源版
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **14.9g颠覆行业，AI眼镜终于实现无感日常佩戴｜甲子光年**
  - 来源：甲子光年
  - 链接：https://mp.weixin.qq.com/s/I6iKe1Y5OXu0iKYfY0Lzfw
  - 评分：5
  - 摘要：AI眼镜重量仅14.9g，实现无感日常佩戴，可能颠覆行业。
  - need_score：5
  - priority：P0
  - reason：AI眼镜轻量化是重要的AI硬件前沿动态。
  - evidence：标题提及14.9g颠覆行业
  - confidence：0.75
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

### 我关心的话题议题有什么新的进展

- **对话EverMind：4个月做到SOTA，要给所有Agent装上长期记忆**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/ENJYzhAEH4C1th6TgzQtqQ
  - 评分：4
  - 摘要：EverMind 推出 SOTA 级别的 Agent 长期记忆产品，旨在提升所有智能体的记忆能力。
  - need_score：5
  - priority：P0
  - reason：直接匹配 AI Agent 关注议题，且提供新事件。
  - evidence：EverMind 产品发布
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Harness开始自己进化了：复旦×北大让Agent实现自改，10轮跑赢Codex**
  - 来源：PaperWeekly
  - 链接：https://mp.weixin.qq.com/s/_mBKGxrA6Mj33_D8aDFJRQ
  - 评分：5
  - 摘要：复旦与北大联合提出AHE框架，让代码Agent自动读取轨迹、修改Harness组件，10轮迭代后性能超越人类设计的Codex-CLI。
  - need_score：5
  - priority：P0
  - reason：直接匹配AI Agent关注议题，且提供具体新进展。
  - evidence：Agent自动改进Harness, Terminal-Bench 2上pass@1从69.7%提升到77.0%
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Agent 超级应用：ChatGPT 用来聊，Codex 干活的时代来了！**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/Cp1f7KpEzZ-PqOI62dNF0Q
  - 评分：5
  - 摘要：介绍Agent超级应用概念：ChatGPT用于对话，Codex用于执行任务，标志AI分工新时代。
  - need_score：4
  - priority：P0
  - reason：匹配AI Agent议题，但摘要信息有限，可能只是趋势讨论而非实质性进展。
  - evidence：标题明确提到Agent, 摘要未提供具体新进展
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **深度｜对话红杉资本：SEO 已死，未来三年不懂 Agent 的营销人将被淘汰**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/xUm_u7n7nY5pNepZFreZPg
  - 评分：4
  - 摘要：红杉资本对话指出SEO即将被Agent取代，营销行业面临底层重构。
  - need_score：4
  - priority：P1
  - reason：内容匹配ai_agent议题，提供了关于Agent在营销领域的新观点。
  - evidence：Agent, SEO
  - confidence：0.65
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **“我可能不再建议学计算机”！图灵奖得主炮轰半个行业，并断言：AI Agent最后全是数据库问题**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/G8swKghfjcFKD_kCyugXXA
  - 评分：4
  - 摘要：图灵奖得主批评当前计算机教育过热，并断言AI Agent本质是数据库问题。
  - need_score：4
  - priority：P1
  - reason：匹配AI Agent议题，提供观点性更新。
  - evidence：AI Agent关键词
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **开源SOTA！商汤原生多模态一个大脑完成看图、推理、作画**
  - 来源：AIGC开放社区
  - 链接：https://mp.weixin.qq.com/s/FxubSRfZPdCykhmNY9C-4A
  - 评分：4
  - 摘要：商汤发布开源多模态模型SenseNova U1，支持看图、推理、作画。
  - need_score：4
  - priority：P1
  - reason：多模态视频生成相关，可匹配AI视频议题。
  - evidence：作画, 多模态
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **视频生成从"能生成"到"能卖钱"，差的是什么？**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/SeXEY7E8QQL_h_zegKWpIw
  - 评分：4
  - 摘要：AI视频生成的商业化应用场景和变现挑战
  - need_score：4
  - priority：P1
  - reason：匹配AI视频生成议题，讨论商业化进展。
  - evidence：标题和摘要涉及AI视频商业场景
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **15小时3.5万Star！Altman投资的AI终端开源炸圈：曾经没人用，如今靠Agent翻身**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/tG3qm1jmrLyf5lBLuIextA
  - 评分：4
  - 摘要：Warp终端客户端开源，基于Rust的Agentic开发环境，获得Altman投资，从无人问津到凭借Agent功能翻红。
  - need_score：4
  - priority：P1
  - reason：匹配AI Agent话题，提供重要新进展。
  - evidence：Agentic开发环境, 开源
  - confidence：0.82
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **既要安全⼜要弹性，理想汽车如何解开企业 OpenClaw 落地死结｜甲子光年**
  - 来源：甲子光年
  - 链接：https://mp.weixin.qq.com/s/MHN8nGChdt3HO_o-toOu_g
  - 评分：4
  - 摘要：理想汽车分享企业级OpenClaw（Agent）落地过程中平衡安全与弹性的实践经验。
  - need_score：4
  - priority：P1
  - reason：匹配AI Agent议题，提供新案例。
  - evidence：OpenClaw, Agent
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **GenFlow4.0，让通用智能体走进办公现场**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/ihjHO3FHCZ4_ODaBRcAr5Q
  - 评分：4
  - 摘要：介绍GenFlow4.0版本，让通用AI智能体应用于办公场景。
  - need_score：4
  - priority：P1
  - reason：匹配ai_agent议题，提供新版本信息
  - evidence：GenFlow4.0, 智能体
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **实测纳逗 Pro：能做专业影视级内容的智能平台长啥样**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/VolHR77wZNbhR2NsztgKjA
  - 评分：4
  - 摘要：评测纳逗 Pro 平台，声称能实现专业影视级 AI 内容创作，不仅限于改善抽卡效率。
  - need_score：4
  - priority：P1
  - reason：与关注议题AI视频生成直接相关，提供新平台信息。
  - evidence：标题提及专业影视级AI内容
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：skim
  - notification_decision：full_push

- **ACL 2026 \| 强模型越听话越危险？VIGIL重塑Agent工具流安全**
  - 来源：PaperWeekly
  - 链接：https://mp.weixin.qq.com/s/sS2nTWlJZGHvmW_QC4c3Nw
  - 评分：4
  - 摘要：ACL 2026 论文介绍 VIGIL 框架，旨在防御 Agent 工具使用中的投毒攻击，提出越听话的模型越危险的反直觉观点
  - need_score：4
  - priority：P1
  - reason：匹配 AI Agent 议题，提供了安全防御的新进展
  - evidence：VIGIL 重塑 Agent 工具流安全
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **万字长文梳理「罗福莉」三个半小时的访谈：2026年不是Agent元年，是生产力爆发年**
  - 来源：开源AI项目落地
  - 链接：https://mp.weixin.qq.com/s/ePslW5QYP6rvx_C3qF0IEQ
  - 评分：4
  - 摘要：对罗福莉长达三个半小时的访谈进行万字总结，核心观点是2026年不是Agent元年，而是生产力爆发年。
  - need_score：4
  - priority：P1
  - reason：直接关联AI Agent议题，提供新观点。
  - evidence：标题明确提出与Agent相关的观点
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **斑马智能进化论：从一家智能座舱供应商，到重新定义“汽车智能”的AI公司｜甲子光年**
  - 来源：甲子光年
  - 链接：https://mp.weixin.qq.com/s/Y2enWV4WhEcPpP5eI0zJtg
  - 评分：4
  - 摘要：文章报道斑马智能从智能座舱供应商转型为AI公司，提出汽车智能从“软件定义”走向“Agent定义”。
  - need_score：4
  - priority：P1
  - reason：匹配AI Agent议题，提供了新的行业应用方向。
  - evidence：标题和摘要聚焦Agent与汽车智能结合
  - confidence：0.75
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **🐴🔥 TokenDance 首发上线 HappyHorse**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/DWmRJ-WFLTrw4M-PKVDatQ
  - 评分：3
  - 摘要：TokenDance 平台首发上线阿里 ATH 旗下视频生成模型 HappyHorse 1.0，并已接入 DeepSeek V4 等模型，支持多协议兼容与智能路由。
  - need_score：4
  - priority：P2
  - reason：匹配 AI 视频生成议题，有明确新模型发布信息。
  - evidence：HappyHorse 为阿里 ATH 旗下视频生成模型
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

### 有什么是我值得看的

- **别问树模型了！死磕结构化数据，清华团队把大模型表格理解推到极限**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/XA21XWHYt55BLoNeuv2wrg
  - 评分：5
  - 摘要：介绍了清华大学与稳准智能联合发布的LimiX系列结构化数据大模型，展示了其在分类、回归、缺失值填补等任务上的通用能力和工业落地效果，并开源了轻量级版本LimiX-2M。
  - need_score：5
  - priority：P0
  - reason：高信息密度、高价值技术文章，值得花时间阅读。
  - evidence：详细技术分析, 实际案例, 开源模型
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **无需训练、只优化解码策略，DTS框架让大模型推理准确率提升6%，推理长度缩短23%**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/JEWHmqctZlhe-7zq5G_Raw
  - 评分：5
  - 摘要：DTS框架通过稀疏化解码树搜索和早停策略，无需训练即可提升大模型推理准确率并缩短推理长度。
  - need_score：5
  - priority：P0
  - reason：高信息密度、有实际收益的AI研究解读
  - evidence：准确率提升6%, 推理长度缩短23%, 即插即用
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **22年的提示词技巧过时了！刚刚，吴恩达新课来了**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/be_Y52RbQXBIyaqra1aAig
  - 评分：5
  - 摘要：吴恩达发布新课，指出2022年的提示词技巧已过时，带来最新AI提示词工程方法。
  - need_score：5
  - priority：P0
  - reason：高质量内容，对AI学习者有直接启发，值得花时间阅读。
  - evidence：Datawhale来源, 吴恩达
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Harness开始自己进化了：复旦×北大让Agent实现自改，10轮跑赢Codex**
  - 来源：PaperWeekly
  - 链接：https://mp.weixin.qq.com/s/_mBKGxrA6Mj33_D8aDFJRQ
  - 评分：5
  - 摘要：复旦与北大联合提出AHE框架，让代码Agent自动读取轨迹、修改Harness组件，10轮迭代后性能超越人类设计的Codex-CLI。
  - need_score：5
  - priority：P0
  - reason：高信息密度、高价值、高相关性，今天必看。
  - evidence：详细实验数据, 方法论可操作性强, 与Agent生态相关
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Meta收购华农校友机器人AI公司，团队并入超级智能实验室**
  - 来源：量子位
  - 链接：https://mp.weixin.qq.com/s/jLwHuaDEZ2wro4oquulyww
  - 评分：5
  - 摘要：Meta收购一家由华农校友创办的机器人AI公司，其团队将并入超级智能实验室，与Robotics Studio合作。
  - need_score：5
  - priority：P0
  - reason：高信息密度、高价值前沿动态，值得阅读。
  - evidence：Meta收购, 机器人AI, 超级智能实验室
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **“我可能不再建议学计算机”！图灵奖得主炮轰半个行业，并断言：AI Agent最后全是数据库问题**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/G8swKghfjcFKD_kCyugXXA
  - 评分：4
  - 摘要：图灵奖得主批评当前计算机教育过热，并断言AI Agent本质是数据库问题。
  - need_score：4
  - priority：P0
  - reason：有独特观点，值得阅读获取见解。
  - evidence：摘要中图灵奖得主观点
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **Agent 超级应用：ChatGPT 用来聊，Codex 干活的时代来了！**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/Cp1f7KpEzZ-PqOI62dNF0Q
  - 评分：5
  - 摘要：介绍Agent超级应用概念：ChatGPT用于对话，Codex用于执行任务，标志AI分工新时代。
  - need_score：4
  - priority：P0
  - reason：高相关性和信息密度，值得阅读。
  - evidence：前沿议题, 高质量来源
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **在大厂，token用少了不“健康”**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/Kj6oQSPijcE8mHbbeAKjkA
  - 评分：4
  - 摘要：讨论大厂中AI token使用量不足可能影响效率，反映AI提效竞争加剧的趋势。
  - need_score：4
  - priority：P1
  - reason：有信息密度，值得阅读全文。
  - evidence：标题和摘要暗示有实质讨论
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **Meta超级智能实验室又发论文，模型混一混，性能直接SOTA**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/mK2E3qs0E2hs7SpKuJZcIA
  - 评分：4
  - 摘要：Meta提出SoCE方法，通过对不同类别模型进行非均匀加权平均融合，在多个基准上取得SOTA性能。
  - need_score：4
  - priority：P1
  - reason：高信息密度，有实际方法论
  - evidence：论文实现, 代码开源
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **深度｜对话a16z：当Bot比真人还多，互联网必须重建「人籍」认证系统**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/t0c8ydcPzNPUFCWWmfLkyg
  - 评分：4
  - 摘要：与a16z深度对话，探讨互联网因Bot泛滥而需要重建人籍认证系统的挑战与方案。
  - need_score：4
  - priority：P1
  - reason：高质量内容，提供行业洞察。
  - evidence：深度对话, 知名投资机构
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **“如果你不用更多Token，就永远逃不出底层”：AI竞赛开始变成资源战争**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/uP_cZBXgyC1eaMOO-meutQ
  - 评分：4
  - 摘要：AI模型Token供应紧张，顶级模型开始限量供应，AI竞赛变成资源战争
  - need_score：4
  - priority：P1
  - reason：内容具有较高信息密度和洞察力
  - evidence：摘要提示重要趋势
  - confidence：0.75
  - needs_more_context：True
  - suggested_action：save
  - notification_decision：incremental_push

- **五一假期，花半天装个 Claude Code 玩玩？**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/HH3CJnkMT4q1G7vi484PfQ
  - 评分：4
  - 摘要：介绍五一假期安装和使用Claude Code的教程文章
  - need_score：4
  - priority：P1
  - reason：内容实用且前沿，值得阅读
  - evidence：标题和摘要指向实操教程, 来源可靠
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：review
  - notification_decision：full_push

- **速递｜Microsoft放弃OpenAI独家销售权，OpenAI进驻其他云计算平台？**
  - 来源：Z Potentials
  - 链接：https://mp.weixin.qq.com/s/sXQ8K3TyZApXd2SlqF21QQ
  - 评分：4
  - 摘要：微软放弃OpenAI独家销售权，OpenAI将能进驻其他云计算平台，标志双方合作模式重大变化。
  - need_score：4
  - priority：P1
  - reason：信息明确且重要，值得花时间阅读。
  - evidence：标题和摘要清晰说明事件
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **对话EverMind：4个月做到SOTA，要给所有Agent装上长期记忆**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/ENJYzhAEH4C1th6TgzQtqQ
  - 评分：4
  - 摘要：EverMind 推出 SOTA 级别的 Agent 长期记忆产品，旨在提升所有智能体的记忆能力。
  - need_score：4
  - priority：P1
  - reason：内容有明确信息增量，值得花时间阅读。
  - evidence：标题涉及 Agent 记忆产品 SOTA
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **“如果你不用更多Token，就永远逃不出底层”：AI竞赛开始变成资源战争**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/yQ5Bbjtd4I5Iw87tEJZa6A
  - 评分：4
  - 摘要：本文指出AI竞赛的瓶颈正从模型能力转向资源分配，强调了Token等资源的重要性。
  - need_score：4
  - priority：P1
  - reason：有信息密度，提供新颖视角。
  - evidence：摘要内容有启发
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **DeepSeek首次有了视觉能力，技术论文却被它连夜删掉了**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/yjctJS4kVIssj1N3uEOPTQ
  - 评分：5
  - 摘要：DeepSeek首次推出视觉能力（多模态），但相关技术论文被连夜撤下，引发外界关注
  - need_score：4
  - priority：P1
  - reason：有明确阅读收益，但需正文确认
  - evidence：标题, 摘要
  - confidence：0.75
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **DeepSeek 发布多模态模型及技术报告；小红书官宣组织调整：柯南出任总裁；宇树发布双臂人形机器人，2.69万元起售 \| 极客早知道**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/nDjyRtoi2vsU88bqSZDklQ
  - 评分：4
  - 摘要：汇总了DeepSeek发布多模态模型、小红书组织调整、宇树人形机器人等科技新闻
  - need_score：4
  - priority：P1
  - reason：多条科技动态汇总，值得一读
  - evidence：DeepSeek, 宇树机器人
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：incremental_push

- **视频生成从"能生成"到"能卖钱"，差的是什么？**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/SeXEY7E8QQL_h_zegKWpIw
  - 评分：4
  - 摘要：AI视频生成的商业化应用场景和变现挑战
  - need_score：4
  - priority：P1
  - reason：内容与前沿和关注议题相关，有潜在阅读价值。
  - evidence：标题摘要显示相关
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **首次大规模真实世界验证：机器人边部署边进化，8项任务全面碾压基线**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/k3LAWmyt5u_Nwpx2agYxEg
  - 评分：5
  - 摘要：机器人边部署边进化首次大规模真实世界验证，在8项任务上全面超越基线。
  - need_score：4
  - priority：P1
  - reason：高信息密度，值得花时间阅读。
  - evidence：前沿结果, 真实世界验证
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **15小时3.5万Star！Altman投资的AI终端开源炸圈：曾经没人用，如今靠Agent翻身**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/tG3qm1jmrLyf5lBLuIextA
  - 评分：4
  - 摘要：Warp终端客户端开源，基于Rust的Agentic开发环境，获得Altman投资，从无人问津到凭借Agent功能翻红。
  - need_score：4
  - priority：P1
  - reason：前沿动态，值得花时间阅读。
  - evidence：高星开源项目, 行业关注
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **魔法原子进军硅谷背后：世界模型野望与生态卡位**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/SAhFum2UOuCmDq_5gyT7_Q
  - 评分：4
  - 摘要：中国具身智能公司魔法原子进军硅谷，布局世界模型和生态。
  - need_score：4
  - priority：P1
  - reason：内容有信息密度且贴近AI商业趋势。
  - evidence：标题显示战略分析
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：incremental_push

- **王兴兴亲测后点赞！这家AI公司提前半年把“龙虾”能力带上车，还管住了Token黑洞**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/Aatbs15E9nw_OkaEhShxpA
  - 评分：4
  - 摘要：宇树科技创始人王兴兴体验宝马新世代i3，点赞某AI公司将先进AI能力（“龙虾”能力）提前半年部署到车上并解决了Token消耗问题。
  - need_score：4
  - priority：P1
  - reason：有明确阅读收益，信息密度较高。
  - evidence：明确的事件和人物, 潜在的AI技术细节
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **既要安全⼜要弹性，理想汽车如何解开企业 OpenClaw 落地死结｜甲子光年**
  - 来源：甲子光年
  - 链接：https://mp.weixin.qq.com/s/MHN8nGChdt3HO_o-toOu_g
  - 评分：4
  - 摘要：理想汽车分享企业级OpenClaw（Agent）落地过程中平衡安全与弹性的实践经验。
  - need_score：4
  - priority：P1
  - reason：高相关、高价值，但需全文确认。
  - evidence：前沿实践
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **GenFlow4.0，让通用智能体走进办公现场**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/ihjHO3FHCZ4_ODaBRcAr5Q
  - 评分：4
  - 摘要：介绍GenFlow4.0版本，让通用AI智能体应用于办公场景。
  - need_score：4
  - priority：P1
  - reason：信息密度高，与关注领域相关，值得阅读
  - evidence：标题明确指向前沿动态
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **3.3k星星爆火！Claude Design开源升级版，中文本地化，支持DeepSeek V4**
  - 来源：开源AI项目落地
  - 链接：https://mp.weixin.qq.com/s/9VablWhs-7dThLqTlH8KHg
  - 评分：4
  - 摘要：Claude Design 开源升级版发布，新增中文本地化和 DeepSeek V4 支持，UI 可局部重写，在 GitHub 获 3.3k 星。
  - need_score：4
  - priority：P1
  - reason：内容具体，信息密度适中，有实践价值。
  - evidence：标题明确功能升级
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **14.9g颠覆行业，AI眼镜终于实现无感日常佩戴｜甲子光年**
  - 来源：甲子光年
  - 链接：https://mp.weixin.qq.com/s/I6iKe1Y5OXu0iKYfY0Lzfw
  - 评分：5
  - 摘要：AI眼镜重量仅14.9g，实现无感日常佩戴，可能颠覆行业。
  - need_score：4
  - priority：P1
  - reason：标题吸引人，但缺乏正文，评估后可能降级。
  - evidence：标题和摘要
  - confidence：0.65
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **对话奔驰高管：AI 上车之后，豪华品牌如何重新定义智能化？**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/TzimXtZFSkpqn--F206NCQ
  - 评分：4
  - 摘要：奔驰高管探讨AI上车后豪华品牌如何重新定义智能化，并与豆包、高德、Momenta等合作将本土智能化能力反向输出到全球。
  - need_score：4
  - priority：P1
  - reason：内容有明确阅读收益，提供行业趋势和具体案例。
  - evidence：极客公园, 对话高管, 豪华品牌智能化
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **GitHub 上狂揽 4.6 万 Star！这款 AI 终端神器终于开源了。**
  - 来源：逛逛GitHub
  - 链接：https://mp.weixin.qq.com/s/MZgv94y9PX2JrODhKbI5_A
  - 评分：4
  - 摘要：介绍一款在 GitHub 上获得 4.6 万 Star 的 AI 终端工具，现已开源。
  - need_score：4
  - priority：P1
  - reason：高 Star 开源项目，可能有实用价值或学习价值。
  - evidence：4.6万 Star, 开源
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **DeepSeek“开眼”背后的技术，公开了！**
  - 来源：智东西
  - 链接：https://mp.weixin.qq.com/s/Uulx9T1PsAiEiwi9OMTZqQ
  - 评分：4
  - 摘要：DeepSeek公开了赋予大模型视觉定位和推理能力的新技术，让模型学会结合视觉与语言进行交互。
  - need_score：4
  - priority：P1
  - reason：内容有信息价值，但需要全文确认。
  - evidence：标题, 来源
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **爱芯元智的双轮驱动：车载放量，边缘爆发**
  - 来源：雷峰网
  - 链接：https://mp.weixin.qq.com/s/IXpSD_Z0_bnFUkknUqbfvA
  - 评分：4
  - 摘要：爱芯元智在车载和边缘计算领域的双轮驱动战略，独立芯片平台构建生态
  - need_score：4
  - priority：P1
  - reason：内容可能提供重要商业和技术洞察，适合深入阅读
  - evidence：雷峰网深度分析, 独立芯片平台生态
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

### 系统通知推荐

- **别问树模型了！死磕结构化数据，清华团队把大模型表格理解推到极限**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/XA21XWHYt55BLoNeuv2wrg
  - 评分：5
  - 摘要：介绍了清华大学与稳准智能联合发布的LimiX系列结构化数据大模型，展示了其在分类、回归、缺失值填补等任务上的通用能力和工业落地效果，并开源了轻量级版本LimiX-2M。
  - 理由：内容详实、技术前沿，开源模型具有实际使用价值，信息密度高，适合保存并后续深入阅读。
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **在大厂，token用少了不“健康”**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/Kj6oQSPijcE8mHbbeAKjkA
  - 评分：4
  - 摘要：讨论大厂中AI token使用量不足可能影响效率，反映AI提效竞争加剧的趋势。
  - 理由：标题有趣，涉及AI提效与token使用，但缺少正文，建议获取全文后评估。
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **Meta超级智能实验室又发论文，模型混一混，性能直接SOTA**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/mK2E3qs0E2hs7SpKuJZcIA
  - 评分：4
  - 摘要：Meta提出SoCE方法，通过对不同类别模型进行非均匀加权平均融合，在多个基准上取得SOTA性能。
  - 理由：提供前沿模型融合技术，信息密度高，有论文和代码，适合技术读者
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **超越 VTM-RA！快手双向智能视频编码器BRHVC亮相NeurIPS2025**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/Mlx1MLD_-4W76V6ck88V-Q
  - 评分：4
  - 摘要：快手提出BRHVC双向智能视频编码方法，在NeurIPS 2025亮相，压缩性能超越标准VTM-RA编码。
  - 理由：重要AI技术前沿，详细介绍了超越传统标准的智能视频编码方法，具有学术和产业价值。
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Z Tech｜世界模型真正的壁垒，可能是表征压缩，对话李智昊、王雨飞**
  - 来源：Z Potentials
  - 链接：https://mp.weixin.qq.com/s/AXD6K8sgUx43bbkLVHEj2w
  - 评分：4
  - 摘要：对话讨论世界模型的真正壁垒在于表征压缩，决定智能上限。
  - 理由：内容涉及AI前沿核心话题，但仅有标题摘要，需要全文评估具体信息量和价值。
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **深度｜对话a16z：当Bot比真人还多，互联网必须重建「人籍」认证系统**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/t0c8ydcPzNPUFCWWmfLkyg
  - 评分：4
  - 摘要：与a16z深度对话，探讨互联网因Bot泛滥而需要重建人籍认证系统的挑战与方案。
  - 理由：探讨AI时代身份认证前沿，匹配前沿需求与关注议题。
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **“如果你不用更多Token，就永远逃不出底层”：AI竞赛开始变成资源战争**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/uP_cZBXgyC1eaMOO-meutQ
  - 评分：4
  - 摘要：AI模型Token供应紧张，顶级模型开始限量供应，AI竞赛变成资源战争
  - 理由：标题和摘要揭示了AI领域重要趋势：Token成为稀缺资源，配给制可能影响行业格局，值得阅读
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：save
  - notification_decision：incremental_push

- **速递｜2026年OpenAI多月销售目标未达成，企业端被Anthropic反超，CFO内部预警1.4万亿算力承诺**
  - 来源：Z Potentials
  - 链接：https://mp.weixin.qq.com/s/HAbeszysq5wa7mpSMD9iHw
  - 评分：4
  - 摘要：OpenAI多月销售目标未达成，企业端被Anthropic反超，CFO内部预警1.4万亿算力承诺的财务风险。
  - 理由：提供了重要的AI商业竞争和财务风险信号，值得阅读以了解行业动态
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **深度｜对话红杉资本：SEO 已死，未来三年不懂 Agent 的营销人将被淘汰**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/xUm_u7n7nY5pNepZFreZPg
  - 评分：4
  - 摘要：红杉资本对话指出SEO即将被Agent取代，营销行业面临底层重构。
  - 理由：内容匹配AI前沿和Agent议题，但仅有标题和摘要，需要抓取全文以获取具体论据。
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **五一假期，花半天装个 Claude Code 玩玩？**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/HH3CJnkMT4q1G7vi484PfQ
  - 评分：4
  - 摘要：介绍五一假期安装和使用Claude Code的教程文章
  - 理由：内容涉及前沿AI工具Claude Code，匹配关注议题，且标题暗示实操性强，值得进一步阅读全文
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **当国产模型追上闭源旗舰，企业 AI 编程的真正障碍才浮出水面**
  - 来源：InfoQ
  - 链接：https://mp.weixin.qq.com/s/FjLOIWT1JKq4er3TEz8aow
  - 评分：4
  - 摘要：文章探讨国产AI模型能力追平闭源旗舰后，企业AI编程面临的真正障碍，如组织流程、工程实践等。
  - 理由：标题和摘要显示文章具有前沿洞察，涉及企业AI编程的深层障碍，值得详细阅读。
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **速递｜红杉、英伟达押注前DeepMind核心研究员，Ineffable种子轮估值51亿美元**
  - 来源：Z Potentials
  - 链接：https://mp.weixin.qq.com/s/DVNJgboCxgvyHJz9dgK8rg
  - 评分：4
  - 摘要：红杉、英伟达投资前DeepMind研究员创立的AI初创公司Ineffable，种子轮估值51亿美元，目标构建不依赖人类数据的自主知识发现系统。
  - 理由：内容涉及AI前沿投资动态和自主知识发现新范式，具有较高信息价值，但摘要信息有限，需抓取全文确认具体技术细节和团队背景。
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **无需训练、只优化解码策略，DTS框架让大模型推理准确率提升6%，推理长度缩短23%**
  - 来源：机器之心
  - 链接：https://mp.weixin.qq.com/s/JEWHmqctZlhe-7zq5G_Raw
  - 评分：5
  - 摘要：DTS框架通过稀疏化解码树搜索和早停策略，无需训练即可提升大模型推理准确率并缩短推理长度。
  - 理由：该内容报道了重要的AI推理优化前沿进展，具有实用价值和新颖性，值得阅读
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **速递｜DeepSeek 多模态功能开始灰度内测，北大校友陈小康带队**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/8enK4u3koAfdP9yRB2Y0Aw
  - 评分：4
  - 摘要：DeepSeek 多模态功能开始灰度内测，由北大校友陈小康带队，公司正加速产品化。
  - 理由：标题直接提及DeepSeek多模态内测，涉及重要AI产品动态，但正文缺失需全文确认详情
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **JoyInside 创新大赛现场，我看到 AI 硬件长出了灵魂**
  - 来源：特工宇宙
  - 链接：https://mp.weixin.qq.com/s/6NEUPNW5y5XcZXGv5-HFBw
  - 评分：4
  - 摘要：报道JoyInside创新大赛中AI硬件产品展现出情感化和智能化趋势
  - 理由：标题和摘要暗示AI硬件创新动态，但缺乏正文细节，需要全文确认价值
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **速递｜Microsoft放弃OpenAI独家销售权，OpenAI进驻其他云计算平台？**
  - 来源：Z Potentials
  - 链接：https://mp.weixin.qq.com/s/sXQ8K3TyZApXd2SlqF21QQ
  - 评分：4
  - 摘要：微软放弃OpenAI独家销售权，OpenAI将能进驻其他云计算平台，标志双方合作模式重大变化。
  - 理由：涉及AI行业重要合作模式变化，对了解前沿动态有价值。
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **对话EverMind：4个月做到SOTA，要给所有Agent装上长期记忆**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/ENJYzhAEH4C1th6TgzQtqQ
  - 评分：4
  - 摘要：EverMind 推出 SOTA 级别的 Agent 长期记忆产品，旨在提升所有智能体的记忆能力。
  - 理由：该内容涉及 AI Agent 前沿产品动态，信息密度高，有启发价值。
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **跑出首个万亿级大模型后，国产算力通过第一场大考**
  - 来源：光子星球
  - 链接：https://mp.weixin.qq.com/s/gAB0kvNW4pQ_CxjNzU-4Mg
  - 评分：5
  - 摘要：国产大模型突破万亿参数，国产算力通过首个大规模训练考验，Token经济学成新焦点。
  - 理由：标题和摘要指向AI前沿重大突破，但缺少细节，需获取全文评估具体技术路径和影响。
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **速递｜Meta收购Manus被正式叫停，国家发改委要求撤销交易**
  - 来源：Z Finance
  - 链接：https://mp.weixin.qq.com/s/CRr0VirGW6YlOzoXqLOewg
  - 评分：4
  - 摘要：Meta收购AI产品Manus被中国发改委正式叫停并要求撤销交易
  - 理由：正文缺失，需抓取全文获取细节；标题显示重要监管动态，与AI Agent关注议题高度相关
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **独家｜前蔚来AI平台负责人白宇利创立「补天石科技」，聚焦具身数据 Infra 方向**
  - 来源：AI科技评论
  - 链接：https://mp.weixin.qq.com/s/iZNTljyU8rYp-AvY6iewXA
  - 评分：4
  - 摘要：前蔚来AI负责人白宇利创立补天石科技，聚焦具身数据Infra，获红杉领投。
  - 理由：内容涉及AI前沿创业动态，但正文缺失，需抓取全文进一步评估。
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **“如果你不用更多Token，就永远逃不出底层”：AI竞赛开始变成资源战争**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/yQ5Bbjtd4I5Iw87tEJZa6A
  - 评分：4
  - 摘要：本文指出AI竞赛的瓶颈正从模型能力转向资源分配，强调了Token等资源的重要性。
  - 理由：摘要提供了关于AI前沿趋势的重要观点，但需要全文确认细节和论据。
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **对话Momenta曹旭东：加速落地物理AI，书写东方硅谷传奇**
  - 来源：光子星球
  - 链接：https://mp.weixin.qq.com/s/7aBl8CoI1Ln9sZODDEUI2A
  - 评分：4
  - 摘要：Momenta CEO曹旭东访谈，讨论物理AI落地与打造东方硅谷的愿景。
  - 理由：标题和摘要暗示重要前沿动态，但缺乏正文细节，需要抓取全文以评估具体价值和匹配度。
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **DeepSeek首次有了视觉能力，技术论文却被它连夜删掉了**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/yjctJS4kVIssj1N3uEOPTQ
  - 评分：5
  - 摘要：DeepSeek首次推出视觉能力（多模态），但相关技术论文被连夜撤下，引发外界关注
  - 理由：重要AI前沿动态，但正文缺失，需抓取全文以评估真实进展
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **“我可能不再建议学计算机”！图灵奖得主炮轰半个行业，并断言：AI Agent最后全是数据库问题**
  - 来源：AI前线
  - 链接：https://mp.weixin.qq.com/s/G8swKghfjcFKD_kCyugXXA
  - 评分：4
  - 摘要：图灵奖得主批评当前计算机教育过热，并断言AI Agent本质是数据库问题。
  - 理由：标题和摘要显示内容涉及AI前沿观点，对AI Agent方向有独特见解，但缺乏全文，需获取全文确认细节。
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **开源SOTA！商汤原生多模态一个大脑完成看图、推理、作画**
  - 来源：AIGC开放社区
  - 链接：https://mp.weixin.qq.com/s/FxubSRfZPdCykhmNY9C-4A
  - 评分：4
  - 摘要：商汤发布开源多模态模型SenseNova U1，支持看图、推理、作画。
  - 理由：内容涉及重要AI前沿动态，但摘要信息有限，需抓取全文确认细节。
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **AI 终于学会 「自我坦白」！Anthropic最新论文震撼来袭，「内省适配器」让黑盒模型自己说出隐藏行为**
  - 来源：AI科技评论
  - 链接：https://mp.weixin.qq.com/s/Cw1HaW-3rOlg4aZjAcKIeQ
  - 评分：5
  - 摘要：Anthropic发表论文，提出'内省适配器'技术，使AI模型能解释自身内部行为，提升AI安全与可解释性。
  - 理由：重要前沿研究，虽无全文但摘要价值高，需深入阅读原文。
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **DeepSeek 发布多模态模型及技术报告；小红书官宣组织调整：柯南出任总裁；宇树发布双臂人形机器人，2.69万元起售 \| 极客早知道**
  - 来源：极客公园
  - 链接：https://mp.weixin.qq.com/s/nDjyRtoi2vsU88bqSZDklQ
  - 评分：4
  - 摘要：汇总了DeepSeek发布多模态模型、小红书组织调整、宇树人形机器人等科技新闻
  - 理由：多条科技新闻摘要，信息密度适中，适合快速浏览了解动态
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：incremental_push

- **视频生成从"能生成"到"能卖钱"，差的是什么？**
  - 来源：硅星人Pro
  - 链接：https://mp.weixin.qq.com/s/SeXEY7E8QQL_h_zegKWpIw
  - 评分：4
  - 摘要：AI视频生成的商业化应用场景和变现挑战
  - 理由：标题和摘要显示本文讨论AI视频生成商业化，与前沿和ai_video议题高度相关，但正文缺失，需抓取全文确认细节。
  - confidence：0.85
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：full_push

- **首次大规模真实世界验证：机器人边部署边进化，8项任务全面碾压基线**
  - 来源：夕小瑶科技说
  - 链接：https://mp.weixin.qq.com/s/k3LAWmyt5u_Nwpx2agYxEg
  - 评分：5
  - 摘要：机器人边部署边进化首次大规模真实世界验证，在8项任务上全面超越基线。
  - 理由：涉及机器人领域重要前沿动态，首次大规模真实世界验证，具有较高技术价值和信息密度。
  - confidence：0.9
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **22年的提示词技巧过时了！刚刚，吴恩达新课来了**
  - 来源：Datawhale
  - 链接：https://mp.weixin.qq.com/s/be_Y52RbQXBIyaqra1aAig
  - 评分：5
  - 摘要：吴恩达发布新课，指出2022年的提示词技巧已过时，带来最新AI提示词工程方法。
  - 理由：该内容来自高质量AI教育社区Datawhale，吴恩达新课对前沿技术学习者有重要价值，提示词技巧更新是实用信息。
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

## 5. 失败源列表

- **StarYuhen**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.yuhenm.top/feed/
  - final feed_url：https://www.yuhenm.top/feed/
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 403: Forbidden"}
- **今日热榜**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://web2rss.cc/feed/rebang.today?preview=true
  - final feed_url：https://web2rss.cc/feed/rebang.today?preview=true
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno -2] Name or service not known>"}
- **刘夙的科技世界**
  - 分类：社评
  - local_xml_url：-
  - xml_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - final feed_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - error_type：feed_parse_error
  - error_message：{"detail": "failed to parse feed: <unknown>:2:0: not well-formed (invalid token)"}
- **偷懒爱好者周刊**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://toolight.cn/open/p/weekly/atom.xml
  - final feed_url：https://toolight.cn/open/p/weekly/atom.xml
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 404: Not Found"}
- **信息差——独立开发者出海周刊**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://gapis.money/rss.xml
  - final feed_url：https://gapis.money/rss.xml
  - error_type：feed_parse_error
  - error_message：{"detail": "failed to parse feed: <unknown>:28:5120: not well-formed (invalid token)"}
- **歸藏的AI工具箱**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml
  - final feed_url：https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml
  - error_type：content_inbox_error
  - error_message：{"detail": "HTTP Error 500: Internal Server Error"}
- **学习一下订阅源**
  - 分类：Articles
  - local_xml_url：http://127.0.0.1:1200/follow/profile/158883963341209600
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/follow/profile/158883963341209600
  - final feed_url：http://host.docker.internal:1200/follow/profile/158883963341209600
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **机器之心**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.jiqizhixin.com/rss
  - final feed_url：https://www.jiqizhixin.com/rss
  - error_type：feed_parse_error
  - error_message：{"detail": "failed to parse feed: <unknown>:12:244: mismatched tag"}
- **AI Foundations**
  - 分类：Videos
  - local_xml_url：-
  - xml_url：https://www.youtube.com/feeds/videos.xml?channel_id=UCWZwfV3ICOt3uEPpW6hYK4g
  - final feed_url：https://www.youtube.com/feeds/videos.xml?channel_id=UCWZwfV3ICOt3uEPpW6hYK4g
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 404: Not Found"}
- **dfarq.homeip.net**
  - 分类：英文博客
  - local_xml_url：-
  - xml_url：https://dfarq.homeip.net/feed/
  - final feed_url：https://dfarq.homeip.net/feed/
  - error_type：feed_parse_error
  - error_message：{"detail": "failed to parse feed: <unknown>:2:0: not well-formed (invalid token)"}
- **blog.pixelmelt.dev**
  - 分类：英文博客
  - local_xml_url：-
  - xml_url：https://blog.pixelmelt.dev/rss/
  - final feed_url：https://blog.pixelmelt.dev/rss/
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 530: <none>"}
- **mjg59.dreamwidth.org**
  - 分类：英文博客
  - local_xml_url：-
  - xml_url：https://mjg59.dreamwidth.org/data/rss
  - final feed_url：https://mjg59.dreamwidth.org/data/rss
  - error_type：timeout
  - error_message：{"detail": "The read operation timed out"}
- **tedunangst.com**
  - 分类：英文博客
  - local_xml_url：-
  - xml_url：https://www.tedunangst.com/flak/rss
  - final feed_url：https://www.tedunangst.com/flak/rss
  - error_type：timeout
  - error_message：{"detail": "<urlopen error _ssl.c:999: The handshake operation timed out>"}