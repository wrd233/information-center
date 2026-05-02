# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-02T15:05:39+00:00
- 结束时间：2026-05-02T15:26:38+00:00
- 日期：2026-05-02
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：501
- 已处理源数量：501
- 成功源数量：474
- 失败源数量：27
- 已知失败跳过数量：0
- total_items：473
- new_items：413
- duplicate_items：60
- screened_items：0
- recommended_items_from_api_response：436
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：445
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
| 1 | Hi, DIYgod | Articles | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 2 | tanscp | Articles | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 3 | Airing 的博客 | Articles | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 5 | Ben's Love | 个人博客-人生 | success | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |  |
| 6 | 莫比乌斯 | 个人博客-人生 | success | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |  |
| 7 | 白熊阿丸的小屋 | 个人博客-人生 | success | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |  |
| 8 | 草稿拾遗 | 个人博客-人生 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 9 | Paradise Lost | Articles | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 10 | 笨方法学写作 | Articles | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 11 | 豆瓣小组-无用美学 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 12 | StarYuhen | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 13 | 少数派 | 优质信息源 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 14 | 少数派 -- Matrix | 优质信息源 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 15 | Experimental History | Articles | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 16 | Blog - Remote Work Prep | Articles | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 17 | EVANGELION:ALL | Articles | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 18 | 纵横四海 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 19 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 20 | 今日热榜 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 21 | 安全代码 | Articles | success | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |  |
| 22 | 老T博客 | Articles | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 23 | 小众软件 | 科技与编程 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 24 | HelloGithub - 月刊 | 科技与编程 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 25 | 宝玉的分享 | 科技与编程 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 26 | 阮一峰的网络日志 | 科技与编程 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 27 | 龙爪槐守望者 | 科技与编程 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 28 | 十年之约聚合订阅 | 科技与编程 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 29 | #UNTAG | 科技与编程 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 30 | 混沌周刊 | 科技与编程 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 31 | 🔔科技频道[奇诺分享-ccino.org]⚡️ | 科技与编程 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 32 | 猴猴说话 | 微信公众号 | success | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |  |
| 33 | 潦草学者 | 微信公众号 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 34 | L先生说 | 微信公众号 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 35 | 常青说 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 36 | 啊桂实验室 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 37 | 大问题Dialectic | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 38 | ONE字幕组 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 39 | everystep | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 40 | 走路 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 41 | Vista看天下 | 社评 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 42 | Tinyfool的个人网站 | 社评 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 43 | 刘夙的科技世界 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 44 | 三联生活周刊 Lifeweek | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 45 | 时代观察 - 乌有之乡网刊 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 46 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 47 | 东西智库 – 专注中国制造业高质量发展 | 国内外资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 48 | 中国政府网 - 最新政策 | 国内政策 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 49 | - 政府文件库 | 国内政策 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 50 | 不如读书 | Articles | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 51 | Lukas Petersson’s blog | Articles | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 52 | 一亩三分地 - 日本热门帖子 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 53 | 偷懒爱好者周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 54 | GeekPlux Letters | Articles | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 55 | 信息差——独立开发者出海周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 56 | joojen Zhou 的网站 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 57 | 周刊 归档 - 酷口家数字花园 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 58 | 莫尔索随笔 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 59 | Ahead of AI | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 60 | 歸藏的AI工具箱 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 61 | Kubernetes Blog | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 62 | AI洞察日报 RSS Feed | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 63 | 最新发布_共产党员网 | 党政信息 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 64 | 新华社新闻_新华网 | 党政信息 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 65 | 半月谈快报 | 党政信息 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 66 | - 求是网 | 党政信息 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 67 | 学习一下订阅源 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 68 | Lex Fridman Podcast | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 69 | Podnews Daily - podcast industry news | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 70 | 新智元 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 71 | 机器之心 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 72 | 腾讯研究院 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 73 | 极客公园 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 74 | 极客公园 | Articles | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 75 | 图书推荐 – 书伴 | SocialMedia | success | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 76 | 每周一书 – 书伴 | SocialMedia | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 77 | 笔记交流站 - 即刻圈子 | SocialMedia | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 78 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 79 | Mike Krieger(@mikeyk) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 80 | Richard Socher(@RichardSocher) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 81 | Hugging Face(@huggingface) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 82 | 小互(@imxiaohu) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 83 | AI at Meta(@AIatMeta) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 84 | Mistral AI(@MistralAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 85 | xAI(@xai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 86 | Dia(@diabrowser) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 87 | AI Breakfast(@AiBreakfast) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 88 | DeepSeek(@deepseek_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 89 | Jim Fan(@DrJimFan) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 90 | Akshay Kothari(@akothari) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 91 | 歸藏(guizang.ai)(@op7418) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 92 | Notion(@NotionHQ) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 93 | Replicate(@replicate) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 94 | lmarena.ai(@lmarena_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 95 | Poe(@poe_platform) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 96 | Ray Dalio(@RayDalio) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 97 | Arthur Mensch(@arthurmensch) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 98 | Paul Graham(@paulg) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 99 | Browser Use(@browser_use) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 100 | The Rundown AI(@TheRundownAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 101 | AI Will(@FinanceYF5) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 102 | Guillermo Rauch(@rauchg) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 103 | 向阳乔木(@vista8) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 104 | Nick St. Pierre(@nickfloats) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 105 | Sahil Lavingia(@shl) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 106 | Jan Leike(@janleike) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 107 | Gary Marcus(@GaryMarcus) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 108 | Monica_IM(@hey_im_monica) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 109 | Lenny Rachitsky(@lennysan) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 110 | Kling AI(@Kling_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 111 | Lilian Weng(@lilianweng) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 112 | Aadit Sheth(@aaditsh) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 113 | Augment Code(@augmentcode) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 114 | Skywork(@Skywork_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 115 | Firecrawl(@firecrawl_dev) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 116 | Adam D'Angelo(@adamdangelo) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 117 | Suhail(@Suhail) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 118 | Sualeh Asif(@sualehasif996) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 119 | Anthropic(@AnthropicAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 120 | AI Engineer(@aiDotEngineer) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 121 | Hailuo AI (MiniMax)(@Hailuo_AI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 122 | Fireworks AI(@FireworksAI_HQ) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 123 | Justine Moore(@venturetwins) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 124 | OpenAI Developers(@OpenAIDevs) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 125 | bolt.new(@boltdotnew) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 126 | Midjourney(@midjourney) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 127 | eric zakariasson(@ericzakariasson) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 128 | Sam Altman(@sama) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 129 | clem &#129303;(@ClementDelangue) | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 130 | LangChain(@LangChainAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 131 | orange.ai(@oran_ge) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 132 | Dario Amodei(@DarioAmodei) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 133 | Geoffrey Hinton(@geoffreyhinton) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 134 | Harrison Chase(@hwchase17) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 135 | Kevin Weil &#127482;&#127480;(@kevinweil) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 136 | Jeff Dean(@JeffDean) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 137 | Perplexity(@perplexity_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 138 | ChatGPT(@ChatGPTapp) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 139 | Berkeley AI Research(@berkeley_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 140 | Paul Couvert(@itsPaulAi) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 141 | Barsee &#128054;(@heyBarsee) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 142 | OpenAI(@OpenAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 143 | Binyuan Hui(@huybery) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 144 | cohere(@cohere) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 145 | Aman Sanger(@amanrsanger) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 146 | Simon Willison(@simonw) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 147 | Microsoft Research(@MSFTResearch) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 148 | Yann LeCun(@ylecun) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 149 | Junyang Lin(@JustinLin610) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 150 | Alex Albert(@alexalbert__) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 151 | Aravind Srinivas(@AravSrinivas) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 152 | Genspark(@genspark_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 153 | Greg Brockman(@gdb) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 154 | elvis(@omarsar0) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 155 | Google AI(@GoogleAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 156 | LlamaIndex &#129433;(@llama_index) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 157 | Jerry Liu(@jerryjliu0) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 158 | Marc Andreessen &#127482;&#127480;(@pmarca) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 159 | Justin Welsh(@thejustinwelsh) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 160 | Pika(@pika_labs) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 161 | Sundar Pichai(@sundarpichai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 162 | Lovable(@lovable_dev) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 163 | cat(@_catwu) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 164 | Anton Osika – eu/acc(@antonosika) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 165 | Replit ⠕(@Replit) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 166 | FlowiseAI(@FlowiseAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 167 | a16z(@a16z) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 168 | 李继刚(@lijigang_com) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 169 | Jina AI(@JinaAI_) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 170 | v0(@v0) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 171 | Andrej Karpathy(@karpathy) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 172 | Fei-Fei Li(@drfeifei) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 173 | DeepLearning.AI(@DeepLearningAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 174 | Rowan Cheung(@rowancheung) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 175 | Latent.Space(@latentspacepod) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 176 | Ideogram(@ideogram_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 177 | Demis Hassabis(@demishassabis) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 178 | Cognition(@cognition_labs) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 179 | andrew chen(@andrewchen) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 180 | NVIDIA AI(@NVIDIAAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 181 | Stanford AI Lab(@StanfordAILab) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 182 | Varun Mohan(@_mohansolo) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 183 | Logan Kilpatrick(@OfficialLoganK) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 184 | Qdrant(@qdrant_engine) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 185 | OpenRouter(@OpenRouterAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 186 | Thomas Wolf(@Thom_Wolf) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 187 | mem0(@mem0ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 188 | Scott Wu(@ScottWu46) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 189 | Recraft(@recraftai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 190 | Hunyuan(@TXhunyuan) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 191 | Google DeepMind(@GoogleDeepMind) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 192 | Mustafa Suleyman(@mustafasuleyman) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 193 | Y Combinator(@ycombinator) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 194 | Lex Fridman(@lexfridman) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 195 | Fellou(@FellouAI) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 196 | Runway(@runwayml) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 197 | Julien Chaumond(@julien_c) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 198 | 宝玉(@dotey) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 199 | Milvus(@milvusio) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 200 | Ian Goodfellow(@goodfellow_ian) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 201 | Taranjeet(@taranjeetio) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 202 | Figma(@figma) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 203 | Patrick Loeber(@patloeber) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 204 | Windsurf(@windsurf_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 205 | Google AI Developers(@googleaidevs) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 206 | Qwen(@Alibaba_Qwen) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 207 | Satya Nadella(@satyanadella) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 208 | Andrew Ng(@AndrewYNg) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 209 | AI SDK(@aisdk) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 210 | HeyGen(@HeyGen_Official) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 211 | Fish Audio(@FishAudio) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 212 | ElevenLabs(@elevenlabsio) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 213 | ollama(@ollama) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 214 | Philipp Schmid(@_philschmid) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 215 | Cursor(@cursor_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 216 | Google Gemini App(@GeminiApp) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 217 | Amjad Masad(@amasad) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 218 | AK(@_akhaliq) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 219 | Groq Inc(@GroqInc) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 220 | ManusAI(@ManusAI_HQ) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 221 | meng shao(@shao__meng) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 222 | Weaviate • vector database(@weaviate_io) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 223 | LovartAI(@lovart_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 224 | Character.AI(@character_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 225 | NotebookLM(@NotebookLM) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 226 | Dify(@dify_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 227 | Eric Jing(@ericjing_ai) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 228 | Naval(@naval) | SocialMedia | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 229 | Twitter @Tom Huang | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 230 | Twitter @Tw93 | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 231 | Twitter @ginobefun | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 232 | Twitter @Theo - t3.gg | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 233 | Lee Robinson(@leerob) | SocialMedia | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 234 | Twitter @Pietro Schirano | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 235 | 每日一图-北京天文馆 | 星空 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 236 | NASA中文 - 天文·每日一图 | 星空 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 237 | AliAbdaal | 长知识 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 238 | 食事史馆 | 长知识 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 239 | 毕导 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 240 | CoCoVii | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 241 | 下班的三爷 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 242 | 本子在隔壁 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 243 | 岱川博士 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 244 | 退役编辑雨上 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 245 | 与书籍度过漫长岁月 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 246 | 智能路障 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 247 | Nenly同学 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 248 | 大问题Dialectic | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 249 | 英语播客狗 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 250 | 林川登罗 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 251 | 人间自习室 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 252 | 漫士沉思录 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 253 | 银屏系漫游指南 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 254 | 浮世叁千问 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 255 | LunaticMosfet | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 256 | 歌白说Geslook | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 257 | Larry想做技术大佬 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 258 | 赏味不足 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 259 | 西山在何许 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 260 | 坚果熊说博弈 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 261 | 罗明落ny | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 262 | 汤质看本质 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 263 | 要素分析 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 264 | 蒙克MK_ | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 265 | Morpheus红丸主义 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 266 | 慢慢学的四饼 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 267 | 辰星杂谈 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 268 | 非卿漫谈 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 269 | 拣尽南枝 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 270 | 硬核学长2077 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 271 | 海林A读书 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 272 | 机器人夏先生1号 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 273 | 知识共享者 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 274 | Maki的完美算术教室 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 275 | 心河摆渡 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 276 | 猴猴说话 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 277 | 3Blue1Brown | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 278 | 思维实验室 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 279 | 是落拓呀 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 280 | 学院派Academia | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 281 | 和张程一起学习吧 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 282 | 读书的Harry | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 283 | 小波心理 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 284 | 科幻视界 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 285 | 差评君 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 286 | 迷因水母 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 287 | 努力戒咕的coco锤 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 288 | 河口超人Aper | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 289 | 荒野初研园 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 290 | 二次元的Datawhale | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 291 | 白染one | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 292 | 卡纸大寨主 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 293 | 向杨Alan君 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 294 | 奥德修斯的绳索 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 295 | 岺玖贰叁 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 296 | 新石器公园 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 297 | 载脑体 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 298 | YouTube深度访谈 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 299 | 天才简史 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 300 | 这是个令人疑惑的星球 | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 301 | 周侃侃plus | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 302 | focus2flow | 长知识 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 303 | 飞鸟手札 | 短知识 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 304 | 英语播客党 | 短知识 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 305 | 波士顿圆脸 | 最娱乐 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 306 | 瓶子君152 | 最娱乐 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 307 | Super也好君 | 最娱乐 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 308 | 负面能量转换器 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 309 | 靠谱电竞 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 310 | 火兰朋克 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 311 | 馆长刘下饭_环球档案 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 312 | 老实憨厚的笑笑 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 313 | 冲击波工作室 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 314 | 邵艾伦Alan | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 315 | 柯洁 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 316 | 逗比的雀巢 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 317 | 大祥哥来了 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 318 | Norah脱口秀 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 319 | 巅峰球迷汇 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 320 | MrBeast官方账号 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 321 | 泛式 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 322 | 贝拉kira | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 323 | -LKs- | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 324 | 真实球迷汇 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 325 | 李滇滇 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 326 | 影视飓风 | 最娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 327 | 猫眼看足球 | 绝活娱乐 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 328 | 陈大东瓜 | 绝活娱乐 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 329 | 司马尘 | 绝活娱乐 | success | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |
| 330 | 是啤酒鸭-梗图 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 331 | MOJi辞書 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 332 | Gray格雷老师 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 333 | 你是想气死1酱么 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 334 | Boo布姐自译 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 335 | 冲男阿凉 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 336 | 杰克森Jackson_ | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 337 | 半只笨猪 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 338 | 脱口秀_Talk_Show | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 339 | 罗翔说刑法 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 340 | 付航脱口秀精选 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 341 | 戴建业老师 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 342 | 听泉赏宝 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 343 | 灯果 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 344 | 隔壁红魔 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 345 | 管泽元 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 346 | 白马繁华 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 347 | 咖啡醉足球 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 348 | 单弦震脉 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 349 | 米国脱口秀 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 350 | 付航脱口秀 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 351 | 峡谷玄学家 | 绝活娱乐 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 352 | AI Foundations | Videos | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 353 | 司机社综合周排行榜 | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 354 | 司机社综合月排行榜 | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 355 | Andrej Karpathy - YouTube | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 356 | Lex Fridman - YouTube | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 357 | simonwillison.net | 英文博客 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 358 | jeffgeerling.com | 英文博客 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 359 | seangoedecke.com | 英文博客 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 360 | krebsonsecurity.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 361 | daringfireball.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 362 | ericmigi.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 363 | antirez.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 364 | idiallo.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 365 | maurycyz.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 366 | pluralistic.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 367 | shkspr.mobi | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 368 | lcamtuf.substack.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 369 | mitchellh.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 370 | dynomight.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 371 | utcc.utoronto.ca/~cks | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 372 | xeiaso.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 373 | devblogs.microsoft.com/oldnewthing | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 374 | righto.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 375 | lucumr.pocoo.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 376 | skyfall.dev | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 377 | garymarcus.substack.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 378 | rachelbythebay.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 379 | overreacted.io | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 380 | timsh.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 381 | johndcook.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 382 | gilesthomas.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 383 | matklad.github.io | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 384 | derekthompson.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 385 | evanhahn.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 386 | terriblesoftware.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 387 | rakhim.exotext.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 388 | joanwestenberg.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 389 | xania.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 390 | micahflee.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 391 | nesbitt.io | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 392 | construction-physics.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 393 | tedium.co | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 394 | susam.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 395 | entropicthoughts.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 396 | buttondown.com/hillelwayne | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 397 | dwarkesh.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 398 | borretti.me | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 399 | wheresyoured.at | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 400 | jayd.ml | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 401 | minimaxir.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 402 | geohot.github.io | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 403 | paulgraham.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 404 | filfre.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 405 | blog.jim-nielsen.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 406 | dfarq.homeip.net | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 407 | jyn.dev | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 408 | geoffreylitt.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 409 | downtowndougbrown.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 410 | brutecat.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 411 | eli.thegreenplace.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 412 | abortretry.fail | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 413 | fabiensanglard.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 414 | oldvcr.blogspot.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 415 | bogdanthegeek.github.io | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 416 | hugotunius.se | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 417 | gwern.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 418 | berthub.eu | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 419 | chadnauseam.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 420 | simone.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 421 | it-notes.dragas.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 422 | beej.us | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 423 | hey.paris | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 424 | danielwirtz.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 425 | matduggan.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 426 | refactoringenglish.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 427 | worksonmymachine.substack.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 428 | philiplaine.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 429 | steveblank.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 430 | bernsteinbear.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 431 | danieldelaney.net | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 432 | troyhunt.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 433 | herman.bearblog.dev | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 434 | tomrenner.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 435 | blog.pixelmelt.dev | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 436 | martinalderson.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 437 | danielchasehooper.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 438 | chiark.greenend.org.uk/~sgtatham | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 439 | grantslatton.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 440 | anildash.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 441 | aresluna.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 442 | michael.stapelberg.ch | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 443 | miguelgrinberg.com | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 444 | keygen.sh | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 445 | mjg59.dreamwidth.org | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 446 | computer.rip | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 447 | tedunangst.com | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 448 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 449 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | 播客 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 450 | 小宇宙 Podcast 648b0b641c48983391a63f98 | 播客 | success | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |  |
| 451 | 小宇宙 Podcast 5e5c52c9418a84a04625e6cc | 播客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 452 | 小宇宙 Podcast 63b7dd49289d2739647d9587 | 播客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 453 | 小宇宙 Podcast 6507bc165c88d2412626b401 | 播客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 454 | Lil'Log | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 455 | Very Small Woods | 英文博客 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 456 | 数字生命卡兹克 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 457 | AGI Hunt | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 458 | 卡尔的AI沃茨 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 459 | 赛博禅心 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 460 | AI产品黄叔 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 461 | 网罗灯下黑 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 462 | 苍何 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 463 | 饼干哥哥AGI | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 464 | 刘聪NLP | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 465 | AI产品阿颖 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 466 | 01Founder | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 467 | AI故事计划 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 468 | 十字路口Crossing | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 469 | 沃垠AI | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 470 | 阿伦AI学习笔记 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 471 | 胡说成理 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 472 | 云中江树 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 473 | 秋芝2046 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 474 | AI产品银海 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 475 | 哥飞 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 476 | 探索AGI | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 477 | 新智元 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 478 | 量子位 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 479 | APPSO | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 480 | 智东西 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 481 | 雷峰网 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 482 | PaperWeekly | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 483 | 甲子光年 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 484 | 逛逛GitHub | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 485 | 开源AI项目落地 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 486 | 夕小瑶科技说 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 487 | Datawhale | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 488 | 极客公园 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 489 | AIGC开放社区 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 490 | AI前线 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 491 | AI科技评论 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 492 | 脑极体 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 493 | 硅星人Pro | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 494 | 特工宇宙 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 495 | 光子星球 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 496 | CVer | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 497 | Z Potentials | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 498 | Z Finance | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 499 | 晚点LatePost | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 500 | InfoQ | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 501 | 机器之心 | 微信公众号 | success | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |  |

## 4. 今日推荐内容

### 新事件

无

### 增量更新

无

### 建议转录

无

### 需要人工复核

无

### 其他推荐内容

无

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
- **时代观察 - 乌有之乡网刊**
  - 分类：社评
  - local_xml_url：http://127.0.0.1:1200/wyzxwk/article
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/wyzxwk/article
  - final feed_url：http://host.docker.internal:1200/wyzxwk/article
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **东西智库 – 专注中国制造业高质量发展**
  - 分类：国内外资讯
  - local_xml_url：http://127.0.0.1:1200/dx2025
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/dx2025
  - final feed_url：http://host.docker.internal:1200/dx2025
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **中国政府网 - 最新政策**
  - 分类：国内政策
  - local_xml_url：http://127.0.0.1:1200/gov/zhengce/zuixin
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/gov/zhengce/zuixin
  - final feed_url：http://host.docker.internal:1200/gov/zhengce/zuixin
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
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
- **周刊 归档 - 酷口家数字花园**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://weqoocu.com/feed
  - final feed_url：https://weqoocu.com/feed
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 403: Forbidden"}
- **歸藏的AI工具箱**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml
  - final feed_url：https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml
  - error_type：timeout
  - error_message：{"detail": "<urlopen error _ssl.c:999: The handshake operation timed out>"}
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
- **腾讯研究院**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://wechat2rss.bestblogs.dev/feed/6152301e0978bffb0a8284cab339262b9764dcfb.xml
  - final feed_url：https://wechat2rss.bestblogs.dev/feed/6152301e0978bffb0a8284cab339262b9764dcfb.xml
  - error_type：timeout
  - error_message：{"detail": "<urlopen error _ssl.c:999: The handshake operation timed out>"}
- **clem &#129303;(@ClementDelangue)**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：https://api.xgo.ing/rss/user/5dbd038a8f5140938d0877511571797b
  - final feed_url：https://api.xgo.ing/rss/user/5dbd038a8f5140938d0877511571797b
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)>"}
- **Twitter @Tom Huang**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/twitter/user/tuturetom
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/twitter/user/tuturetom
  - final feed_url：http://host.docker.internal:1200/twitter/user/tuturetom
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Twitter @Tw93**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/twitter/user/HiTw93
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/twitter/user/HiTw93
  - final feed_url：http://host.docker.internal:1200/twitter/user/HiTw93
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Twitter @ginobefun**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/twitter/user/hongming731
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/twitter/user/hongming731
  - final feed_url：http://host.docker.internal:1200/twitter/user/hongming731
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Twitter @Theo - t3.gg**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/twitter/user/theo
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/twitter/user/theo
  - final feed_url：http://host.docker.internal:1200/twitter/user/theo
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Twitter @Pietro Schirano**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/twitter/user/skirano
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/twitter/user/skirano
  - final feed_url：http://host.docker.internal:1200/twitter/user/skirano
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **NASA中文 - 天文·每日一图**
  - 分类：星空
  - local_xml_url：http://127.0.0.1:1200/nasa/apod-cn
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/nasa/apod-cn
  - final feed_url：http://host.docker.internal:1200/nasa/apod-cn
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **司机社综合周排行榜**
  - 分类：Videos
  - local_xml_url：http://127.0.0.1:1200/xsijishe/rank/weekly
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/xsijishe/rank/weekly
  - final feed_url：http://host.docker.internal:1200/xsijishe/rank/weekly
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **司机社综合月排行榜**
  - 分类：Videos
  - local_xml_url：http://127.0.0.1:1200/xsijishe/rank/monthly
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/xsijishe/rank/monthly
  - final feed_url：http://host.docker.internal:1200/xsijishe/rank/monthly
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Andrej Karpathy - YouTube**
  - 分类：Videos
  - local_xml_url：http://127.0.0.1:1200/youtube/user/@AndrejKarpathy
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/youtube/user/@AndrejKarpathy
  - final feed_url：http://host.docker.internal:1200/youtube/user/@AndrejKarpathy
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Lex Fridman - YouTube**
  - 分类：Videos
  - local_xml_url：http://127.0.0.1:1200/youtube/user/%40lexfridman
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/youtube/user/%40lexfridman
  - final feed_url：http://host.docker.internal:1200/youtube/user/%40lexfridman
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
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
- **tedunangst.com**
  - 分类：英文博客
  - local_xml_url：-
  - xml_url：https://www.tedunangst.com/flak/rss
  - final feed_url：https://www.tedunangst.com/flak/rss
  - error_type：timeout
  - error_message：{"detail": "<urlopen error _ssl.c:999: The handshake operation timed out>"}