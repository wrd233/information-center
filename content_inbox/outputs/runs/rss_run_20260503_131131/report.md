# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T05:11:31+00:00
- 结束时间：2026-05-03T06:51:35+00:00
- 日期：2026-05-03
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：501
- 已处理源数量：99
- 成功源数量：88
- 失败源数量：11
- 已知失败跳过数量：0
- total_items：261
- new_items：255
- duplicate_items：6
- screened_items：255
- recommended_items_from_api_response：143
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：217
- failed_items：0
- inbox 查询模式：pending
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 3 | 1 | 2 | 1 | 3 | 1 | 0 | 2 | 0 |  |
| 2 | tanscp | Articles | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 2 | 0 |  |
| 3 | Airing 的博客 | Articles | success | 3 | 3 | 0 | 3 | 3 | 0 | 0 | 3 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 3 | 3 | 0 | 3 | 0 | 2 | 0 | 3 | 0 |  |
| 5 | Ben's Love | 个人博客-人生 | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 6 | 莫比乌斯 | 个人博客-人生 | success | 3 | 3 | 0 | 3 | 0 | 1 | 0 | 3 | 0 |  |
| 7 | 白熊阿丸的小屋 | 个人博客-人生 | success | 3 | 3 | 0 | 3 | 1 | 2 | 0 | 2 | 0 |  |
| 8 | 草稿拾遗 | 个人博客-人生 | success | 3 | 3 | 0 | 3 | 3 | 0 | 0 | 3 | 0 |  |
| 9 | Paradise Lost | Articles | success | 3 | 3 | 0 | 3 | 0 | 1 | 0 | 3 | 0 |  |
| 10 | 笨方法学写作 | Articles | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 11 | 豆瓣小组-无用美学 | Articles | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 12 | StarYuhen | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 13 | 少数派 | 优质信息源 | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 14 | 少数派 -- Matrix | 优质信息源 | success | 3 | 2 | 1 | 2 | 1 | 2 | 0 | 3 | 0 |  |
| 15 | Experimental History | Articles | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 3 | 0 |  |
| 16 | Blog - Remote Work Prep | Articles | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 17 | EVANGELION:ALL | Articles | success | 3 | 3 | 0 | 3 | 0 | 1 | 0 | 3 | 0 |  |
| 18 | 纵横四海 | Articles | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 19 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 20 | 今日热榜 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 21 | 安全代码 | Articles | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 22 | 老T博客 | Articles | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 2 | 0 |  |
| 23 | 小众软件 | 科技与编程 | success | 3 | 3 | 0 | 3 | 3 | 0 | 0 | 3 | 0 |  |
| 24 | HelloGithub - 月刊 | 科技与编程 | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 25 | 宝玉的分享 | 科技与编程 | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 2 | 0 |  |
| 26 | 阮一峰的网络日志 | 科技与编程 | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 27 | 龙爪槐守望者 | 科技与编程 | success | 3 | 3 | 0 | 3 | 2 | 2 | 1 | 2 | 0 |  |
| 28 | 十年之约聚合订阅 | 科技与编程 | success | 3 | 2 | 1 | 2 | 2 | 0 | 0 | 3 | 0 |  |
| 29 | #UNTAG | 科技与编程 | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 3 | 0 |  |
| 30 | 混沌周刊 | 科技与编程 | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 31 | 🔔科技频道[奇诺分享-ccino.org]⚡️ | 科技与编程 | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 32 | 猴猴说话 | 微信公众号 | success | 3 | 3 | 0 | 3 | 2 | 2 | 0 | 3 | 0 |  |
| 33 | 潦草学者 | 微信公众号 | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 34 | L先生说 | 微信公众号 | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 3 | 0 |  |
| 35 | 常青说 | 微信公众号 | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 3 | 0 |  |
| 36 | 啊桂实验室 | 微信公众号 | success | 3 | 3 | 0 | 3 | 2 | 2 | 0 | 3 | 0 |  |
| 37 | 大问题Dialectic | 微信公众号 | success | 3 | 3 | 0 | 3 | 1 | 2 | 0 | 3 | 0 |  |
| 38 | ONE字幕组 | 微信公众号 | success | 3 | 3 | 0 | 3 | 1 | 2 | 0 | 3 | 0 |  |
| 39 | everystep | 微信公众号 | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 40 | 走路 | 微信公众号 | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 3 | 0 |  |
| 41 | Vista看天下 | 社评 | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 42 | Tinyfool的个人网站 | 社评 | success | 3 | 3 | 0 | 3 | 2 | 2 | 0 | 1 | 0 |  |
| 43 | 刘夙的科技世界 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 44 | 三联生活周刊 Lifeweek | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 45 | 时代观察 - 乌有之乡网刊 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 46 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 3 | 3 | 0 | 3 | 0 | 3 | 0 | 3 | 0 |  |
| 47 | 东西智库 – 专注中国制造业高质量发展 | 国内外资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 48 | 中国政府网 - 最新政策 | 国内政策 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 49 | - 政府文件库 | 国内政策 | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 50 | 不如读书 | Articles | success | 3 | 3 | 0 | 3 | 0 | 1 | 0 | 3 | 0 |  |
| 51 | Lukas Petersson’s blog | Articles | success | 3 | 3 | 0 | 3 | 3 | 3 | 0 | 0 | 0 |  |
| 52 | 一亩三分地 - 日本热门帖子 | Articles | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 53 | 偷懒爱好者周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 54 | GeekPlux Letters | Articles | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 55 | 信息差——独立开发者出海周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 56 | joojen Zhou 的网站 | Articles | success | 3 | 3 | 0 | 3 | 0 | 2 | 0 | 3 | 0 |  |
| 57 | 周刊 归档 - 酷口家数字花园 | Articles | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 58 | 莫尔索随笔 | Articles | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 59 | Ahead of AI | Articles | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 60 | 歸藏的AI工具箱 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | content_inbox_error |
| 61 | Kubernetes Blog | Articles | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 62 | AI洞察日报 RSS Feed | Articles | success | 3 | 3 | 0 | 3 | 3 | 0 | 0 | 3 | 0 |  |
| 63 | 最新发布_共产党员网 | 党政信息 | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 64 | 新华社新闻_新华网 | 党政信息 | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 65 | 半月谈快报 | 党政信息 | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 2 | 0 |  |
| 66 | - 求是网 | 党政信息 | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 67 | 学习一下订阅源 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 68 | Lex Fridman Podcast | Articles | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 2 | 0 |  |
| 69 | Podnews Daily - podcast industry news | Articles | success | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 0 |  |
| 70 | 新智元 | Articles | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 71 | 机器之心 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 72 | 腾讯研究院 | Articles | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 73 | 极客公园 | Articles | success | 3 | 3 | 0 | 3 | 3 | 1 | 1 | 1 | 0 |  |
| 74 | 极客公园 | Articles | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 75 | 图书推荐 – 书伴 | SocialMedia | success | 3 | 1 | 2 | 1 | 2 | 0 | 0 | 3 | 0 |  |
| 76 | 每周一书 – 书伴 | SocialMedia | success | 3 | 3 | 0 | 3 | 0 | 3 | 0 | 3 | 0 |  |
| 77 | 笔记交流站 - 即刻圈子 | SocialMedia | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 78 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 3 | 3 | 0 | 3 | 0 | 1 | 0 | 3 | 0 |  |
| 79 | Mike Krieger(@mikeyk) | SocialMedia | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 80 | Richard Socher(@RichardSocher) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 3 | 0 |  |
| 81 | Hugging Face(@huggingface) | SocialMedia | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 82 | 小互(@imxiaohu) | SocialMedia | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 83 | AI at Meta(@AIatMeta) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 2 | 0 |  |
| 84 | Mistral AI(@MistralAI) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 2 | 0 |  |
| 85 | xAI(@xai) | SocialMedia | success | 3 | 3 | 0 | 3 | 3 | 0 | 0 | 3 | 0 |  |
| 86 | Dia(@diabrowser) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 87 | AI Breakfast(@AiBreakfast) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 2 | 0 | 2 | 0 |  |
| 88 | DeepSeek(@deepseek_ai) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 1 | 1 | 2 | 0 |  |
| 89 | Jim Fan(@DrJimFan) | SocialMedia | success | 3 | 3 | 0 | 3 | 3 | 1 | 0 | 2 | 0 |  |
| 90 | Akshay Kothari(@akothari) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 91 | 歸藏(guizang.ai)(@op7418) | SocialMedia | success | 3 | 3 | 0 | 3 | 2 | 0 | 0 | 3 | 0 |  |
| 92 | Notion(@NotionHQ) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 2 | 0 | 3 | 0 |  |
| 93 | Replicate(@replicate) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 94 | lmarena.ai(@lmarena_ai) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 0 | 0 | 3 | 0 |  |
| 95 | Poe(@poe_platform) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 1 | 0 | 3 | 0 |  |
| 96 | Ray Dalio(@RayDalio) | SocialMedia | success | 3 | 3 | 0 | 3 | 2 | 1 | 0 | 3 | 0 |  |
| 97 | Arthur Mensch(@arthurmensch) | SocialMedia | success | 3 | 3 | 0 | 3 | 3 | 2 | 0 | 1 | 0 |  |
| 98 | Paul Graham(@paulg) | SocialMedia | success | 3 | 3 | 0 | 3 | 1 | 2 | 0 | 2 | 0 |  |
| 99 | Browser Use(@browser_use) | SocialMedia | success | 3 | 3 | 0 | 3 | 3 | 0 | 0 | 3 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

无

### 我关注的前沿咋样了

无

### 我关心的话题议题有什么新的进展

无

### 有什么是我值得看的

无

### 系统通知推荐

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
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1016)>"}