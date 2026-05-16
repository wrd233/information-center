# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T07:19:46+00:00
- 结束时间：2026-05-04T09:55:40+00:00
- 日期：2026-05-04
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：100
- 已处理源数量：100
- 成功源数量：97
- 失败源数量：3
- 已知失败跳过数量：0
- total_items：384
- new_items：384
- duplicate_items：0
- screened_items：384
- recommended_items_from_api_response：199
- new_items_recommended：unknown
- final_inbox_items_from_this_run：9
- full_push_items_from_this_run：9
- incremental_push_items_from_this_run：0
- silent_items：330
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 4 | 4 | 0 | 4 | 0 | 3 | 0 | 3 | 0 |  |
| 3 | AI Foundations | Videos | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 3 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 4 | 4 | 0 | 4 | 1 | 3 | 0 | 4 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 3 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 4 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 4 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 4 | 4 | 0 | 4 | 1 | 2 | 0 | 4 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 4 | 4 | 0 | 4 | 4 | 3 | 0 | 1 | 0 |  |
| 11 | 波士顿圆脸 | 最娱乐 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 12 | 飞鸟手札 | 短知识 | success | 4 | 4 | 0 | 4 | 3 | 3 | 0 | 4 | 0 |  |
| 13 | Vista看天下 | 社评 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 14 | 小众软件 | 科技与编程 | success | 4 | 4 | 0 | 4 | 4 | 1 | 0 | 3 | 0 |  |
| 15 | 猫眼看足球 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 16 | simonwillison.net | 英文博客 | success | 4 | 4 | 0 | 4 | 4 | 2 | 0 | 2 | 0 |  |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 4 | 4 | 0 | 4 | 0 | 2 | 0 | 4 | 0 |  |
| 18 | AliAbdaal | 长知识 | success | 4 | 4 | 0 | 4 | 3 | 1 | 0 | 3 | 0 |  |
| 19 | tanscp | Articles | success | 4 | 4 | 0 | 4 | 3 | 3 | 0 | 2 | 0 |  |
| 20 | 每周一书 – 书伴 | SocialMedia | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 21 | Ben's Love | 个人博客-人生 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 22 | 新华社新闻_新华网 | 党政信息 | success | 4 | 4 | 0 | 4 | 0 | 2 | 0 | 4 | 0 |  |
| 23 | 潦草学者 | 微信公众号 | success | 4 | 4 | 0 | 4 | 1 | 4 | 0 | 3 | 0 |  |
| 24 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | 播客 | success | 4 | 4 | 0 | 4 | 4 | 1 | 0 | 3 | 0 |  |
| 25 | 瓶子君152 | 最娱乐 | success | 4 | 4 | 0 | 4 | 3 | 0 | 0 | 4 | 0 |  |
| 26 | 英语播客党 | 短知识 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 27 | Tinyfool的个人网站 | 社评 | success | 4 | 4 | 0 | 4 | 4 | 2 | 0 | 2 | 0 |  |
| 28 | HelloGithub - 月刊 | 科技与编程 | success | 4 | 4 | 0 | 4 | 4 | 0 | 0 | 4 | 0 |  |
| 29 | 陈大东瓜 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 30 | jeffgeerling.com | 英文博客 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 4 | 0 |  |
| 31 | 食事史馆 | 长知识 | success | 4 | 4 | 0 | 4 | 3 | 0 | 0 | 4 | 0 |  |
| 32 | Airing 的博客 | Articles | success | 4 | 4 | 0 | 4 | 3 | 1 | 0 | 4 | 0 |  |
| 33 | 笔记交流站 - 即刻圈子 | SocialMedia | success | 4 | 4 | 0 | 4 | 0 | 2 | 0 | 4 | 0 |  |
| 34 | 莫比乌斯 | 个人博客-人生 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 3 | 0 |  |
| 35 | 半月谈快报 | 党政信息 | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 3 | 0 |  |
| 36 | L先生说 | 微信公众号 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 4 | 0 |  |
| 37 | 小宇宙 Podcast 648b0b641c48983391a63f98 | 播客 | success | 4 | 4 | 0 | 4 | 4 | 2 | 0 | 2 | 0 |  |
| 38 | Super也好君 | 最娱乐 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 39 | 刘夙的科技世界 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 40 | 宝玉的分享 | 科技与编程 | success | 4 | 4 | 0 | 4 | 4 | 2 | 0 | 2 | 0 |  |
| 41 | 司马尘 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 4 | 0 |  |
| 42 | seangoedecke.com | 英文博客 | success | 4 | 4 | 0 | 4 | 3 | 4 | 0 | 1 | 0 |  |
| 43 | 毕导 | 长知识 | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 4 | 0 |  |
| 44 | Paradise Lost | Articles | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 45 | Mike Krieger(@mikeyk) | SocialMedia | success | 4 | 4 | 0 | 4 | 4 | 1 | 0 | 3 | 0 |  |
| 46 | 白熊阿丸的小屋 | 个人博客-人生 | success | 4 | 4 | 0 | 4 | 3 | 3 | 0 | 2 | 0 |  |
| 47 | - 求是网 | 党政信息 | success | 4 | 4 | 0 | 4 | 2 | 1 | 1 | 2 | 0 |  |
| 48 | 常青说 | 微信公众号 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 4 | 0 |  |
| 49 | 小宇宙 Podcast 5e5c52c9418a84a04625e6cc | 播客 | success | 4 | 4 | 0 | 4 | 4 | 1 | 0 | 3 | 0 |  |
| 50 | 负面能量转换器 | 最娱乐 | success | 4 | 4 | 0 | 4 | 4 | 0 | 0 | 4 | 0 |  |
| 51 | 三联生活周刊 Lifeweek | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 52 | 阮一峰的网络日志 | 科技与编程 | success | 4 | 4 | 0 | 4 | 4 | 1 | 0 | 3 | 0 |  |
| 53 | 是啤酒鸭-梗图 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 54 | krebsonsecurity.com | 英文博客 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 3 | 0 |  |
| 55 | CoCoVii | 长知识 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 56 | 笨方法学写作 | Articles | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 4 | 0 |  |
| 57 | Richard Socher(@RichardSocher) | SocialMedia | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 3 | 0 |  |
| 58 | 草稿拾遗 | 个人博客-人生 | success | 4 | 4 | 0 | 4 | 3 | 1 | 0 | 4 | 0 |  |
| 59 | 啊桂实验室 | 微信公众号 | success | 4 | 4 | 0 | 4 | 3 | 0 | 0 | 4 | 0 |  |
| 60 | 小宇宙 Podcast 63b7dd49289d2739647d9587 | 播客 | success | 4 | 4 | 0 | 4 | 4 | 2 | 0 | 2 | 0 |  |
| 61 | 靠谱电竞 | 最娱乐 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 62 | 龙爪槐守望者 | 科技与编程 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 4 | 0 |  |
| 63 | MOJi辞書 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 3 | 0 | 0 | 4 | 0 |  |
| 64 | daringfireball.net | 英文博客 | success | 4 | 4 | 0 | 4 | 2 | 3 | 0 | 2 | 0 |  |
| 65 | 下班的三爷 | 长知识 | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 3 | 0 |  |
| 66 | StarYuhen | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 67 | Hugging Face(@huggingface) | SocialMedia | success | 4 | 4 | 0 | 4 | 3 | 1 | 0 | 3 | 0 |  |
| 68 | 大问题Dialectic | 微信公众号 | success | 4 | 4 | 0 | 4 | 3 | 1 | 0 | 4 | 0 |  |
| 69 | 小宇宙 Podcast 6507bc165c88d2412626b401 | 播客 | success | 4 | 4 | 0 | 4 | 3 | 2 | 0 | 2 | 0 |  |
| 70 | 火兰朋克 | 最娱乐 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 71 | 十年之约聚合订阅 | 科技与编程 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 72 | Gray格雷老师 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 73 | ericmigi.com | 英文博客 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 3 | 0 |  |
| 74 | 本子在隔壁 | 长知识 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 4 | 0 |  |
| 75 | Experimental History | Articles | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 3 | 0 |  |
| 76 | 小互(@imxiaohu) | SocialMedia | success | 4 | 4 | 0 | 4 | 4 | 0 | 0 | 4 | 0 |  |
| 77 | ONE字幕组 | 微信公众号 | success | 4 | 4 | 0 | 4 | 2 | 2 | 0 | 4 | 0 |  |
| 78 | 馆长刘下饭_环球档案 | 最娱乐 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 79 | #UNTAG | 科技与编程 | success | 4 | 4 | 0 | 4 | 1 | 3 | 0 | 4 | 0 |  |
| 80 | 你是想气死1酱么 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 81 | antirez.com | 英文博客 | success | 4 | 4 | 0 | 4 | 4 | 3 | 0 | 1 | 0 |  |
| 82 | 岱川博士 | 长知识 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 83 | Blog - Remote Work Prep | Articles | success | 4 | 4 | 0 | 4 | 2 | 3 | 0 | 3 | 0 |  |
| 84 | AI at Meta(@AIatMeta) | SocialMedia | success | 4 | 4 | 0 | 4 | 0 | 2 | 0 | 4 | 0 |  |
| 85 | everystep | 微信公众号 | success | 4 | 4 | 0 | 4 | 1 | 2 | 0 | 4 | 0 |  |
| 86 | 老实憨厚的笑笑 | 最娱乐 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 87 | 混沌周刊 | 科技与编程 | success | 4 | 4 | 0 | 4 | 4 | 2 | 0 | 2 | 0 |  |
| 88 | Boo布姐自译 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 3 | 0 | 0 | 4 | 0 |  |
| 89 | idiallo.com | 英文博客 | success | 4 | 4 | 0 | 4 | 3 | 1 | 0 | 3 | 0 |  |
| 90 | 退役编辑雨上 | 长知识 | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 4 | 0 |  |
| 91 | EVANGELION:ALL | Articles | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 92 | Mistral AI(@MistralAI) | SocialMedia | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 93 | 走路 | 微信公众号 | success | 4 | 4 | 0 | 4 | 0 | 2 | 0 | 4 | 0 |  |
| 94 | 冲击波工作室 | 最娱乐 | success | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 4 | 0 |  |
| 95 | 🔔科技频道[奇诺分享-ccino.org]⚡️ | 科技与编程 | success | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 4 | 0 |  |
| 96 | 冲男阿凉 | 绝活娱乐 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 97 | maurycyz.com | 英文博客 | success | 4 | 4 | 0 | 4 | 2 | 1 | 0 | 4 | 0 |  |
| 98 | 与书籍度过漫长岁月 | 长知识 | success | 4 | 4 | 0 | 4 | 1 | 2 | 0 | 4 | 0 |  |
| 99 | 今日热榜 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 100 | xAI(@xai) | SocialMedia | success | 4 | 4 | 0 | 4 | 4 | 1 | 0 | 3 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

- **感觉不如LDL……水平 —— [冲击波工作室] S14 入围赛**
  - 来源：冲击波工作室
  - 链接：https://www.bilibili.com/video/BV1nyxDeKEgz
  - 评分：2
  - 摘要：B站视频调侃S14入围赛水平不如LDL，属于游戏娱乐评论
  - need_score：5
  - priority：P0
  - reason：内容轻松有趣，标题引人发笑，适合放松观看。
  - evidence：标题: 感觉不如LDL……水平, 来源: 冲击波工作室，娱乐向, 内容: 调侃S14入围赛，轻松吐槽
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **Lines of EVANGELION 香港站门票信息**
  - 来源：EVANGELION:ALL
  - 链接：https://www.eva-all.com/news/46686/lines-of-evangelion-hong-kong-station-ticket-information
  - 评分：3
  - 摘要：EVA香港站展览早鸟预售门票信息发布。
  - need_score：5
  - priority：P0
  - reason：EVA展览门票信息，轻松有趣，适合放松浏览。
  - evidence：EVANGELION, 香港站门票
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **Have You Seen the New Excel?**
  - 中文解释：你看过新版Excel吗？
  - 来源：idiallo.com
  - 链接：https://idiallo.com/blog/have-you-seen-the-new-xl-ai-parody?src=feed
  - 评分：2
  - 摘要：一篇以讽刺口吻赞美Excel的幽默文章，调侃科技界对AI和复杂软件的过度追捧，认为Excel才是终极业务工具。
  - need_score：5
  - priority：P0
  - reason：文章幽默讽刺，风格轻松有趣，非常适合放松阅读。
  - evidence：讽刺口吻, 调侃科技界, 轻松阅读
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **如何一眼找到盲人?**
  - 来源：Boo布姐自译
  - 链接：https://www.bilibili.com/video/BV16qvAz7EkE
  - 评分：3
  - 摘要：一个可能带有戏谑或反讽意味的娱乐视频标题，探讨如何识别盲人。
  - need_score：5
  - priority：P0
  - reason：标题具有娱乐性，来源为绝活娱乐，适合轻松观看。
  - evidence：标题：如何一眼找到盲人？, 来源类别：绝活娱乐
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **给个冠军吧哥，给点 给点 - [冲击波工作室]s14 决赛**
  - 来源：冲击波工作室
  - 链接：https://www.bilibili.com/video/BV153DjYMEGm
  - 评分：2
  - 摘要：冲击波工作室制作的关于S14决赛的娱乐视频，标题调侃求冠军。
  - need_score：5
  - priority：P1
  - reason：内容是冲击波工作室关于S14决赛的娱乐视频，标题调侃求冠军，适合轻松观看，符合娱乐需求。
  - evidence：S14决赛, 冲击波工作室, 娱乐视频
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **【AL vs IG】德云色解说：硬实力碾了（2026第二赛段）**
  - 来源：老实憨厚的笑笑
  - 链接：https://www.bilibili.com/video/BV1mWR7BwEjr
  - 评分：2
  - 摘要：德云色解说英雄联盟AL vs IG比赛的2026第二赛段视频。
  - need_score：5
  - priority：P1
  - reason：视频是德云色解说的LOL比赛，轻松有趣，非常适合放松娱乐。
  - evidence：标题明确为AL vs IG比赛解说, 来源为娱乐UP主德云色, 摘要提及硬实力碾压
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **你能明显感觉到 OpenAI 是由一群产品经理在主导 而 Anthropic 是由一群工程师主导 所以 Anthropic 搞的一些创意，总能被OpenAI 抄过去改造的体验更好😂**
  - 来源：小互(@imxiaohu)
  - 链接：https://x.com/xiaohu/status/2050751703381876829
  - 评分：3
  - 摘要：小互发帖调侃OpenAI由产品经理主导、Anthropic由工程师主导，指出Anthropic的创意常被OpenAI抄去并优化体验。
  - need_score：5
  - priority：P1
  - reason：内容轻松有趣，调侃OpenAI和Anthropic的产品文化差异，适合放松观看。
  - evidence：帖子标题含😂表情, 社交平台调侃风格
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：review
  - notification_decision：silent

- **『福音战士』与皮革产品制造商「NADAYA」合作、推出以碇真嗣和渚薰为印象的真皮迷你钱包**
  - 来源：EVANGELION:ALL
  - 链接：https://www.eva-all.com/news/46693/reservations-begin-today-for-the-collaboration-between-evangelion-and-leather-accessory-manufacturer-nadaya-introducing-genuine-leather-mini-wallets-inspired-by-shinji-ikari-and-kaworu-nagisa
  - 评分：2
  - 摘要：《福音战士》与皮革制造商NADAYA合作，推出以碇真嗣和渚薰为形象的真皮迷你钱包。
  - need_score：4
  - priority：P1
  - reason：内容轻松有趣，适合放松观看。
  - evidence：福音战士合作主题钱包, 娱乐内容
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **【1酱赛评】LPL竞男颜值鉴赏指南，谁是各队门面，谁又魅惑众生？**
  - 来源：你是想气死1酱么
  - 链接：https://www.bilibili.com/video/BV1gLD1BqEJh
  - 评分：2
  - 摘要：盘点LPL各队电竞选手的颜值门面，分析谁更吸引观众。
  - need_score：4
  - priority：P1
  - reason：内容为LPL选手颜值鉴赏，轻松娱乐，适合放松观看。
  - evidence：LPL, 颜值, 娱乐
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **The 3rd Annual Blog Post Competition, Extravaganza, and Jamboree**
  - 中文解释：第三届年度博客比赛、盛会与狂欢
  - 来源：Experimental History
  - 链接：https://www.experimental-history.com/p/the-3rd-annual-blog-post-competition
  - 评分：3
  - 摘要：Adam Mastroianni在Experimental History上举办第三届年度博客比赛，征集未发表的博客文章，提供现金奖励和推荐机会。
  - need_score：4
  - priority：P1
  - reason：这是一场轻松有趣的博客比赛公告，适合放松阅读，但需要一定参与意愿。
  - evidence：博客比赛, 轻松氛围, 奖励机制
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **看世界丨中午只吃三片面包，荷兰饮食让我震惊**
  - 来源：走路
  - 链接：https://mp.weixin.qq.com/s/PC4RhOokBRlN8EDtrkPn2w
  - 评分：2
  - 摘要：作者分享对荷兰饮食文化中中午只吃三片面包的惊讶观察。
  - need_score：4
  - priority：P2
  - reason：轻松有趣的跨文化饮食观察，适合放松。
  - evidence：荷兰饮食, 个人观察
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **来抄设定！七百年前的脑洞依然顶流，一个视频带你速通基督神话宇宙观的终极形态——但丁《神曲》宇宙观**
  - 来源：馆长刘下饭_环球档案
  - 链接：https://www.bilibili.com/video/BV1CeoaBBEUo
  - 评分：2
  - 摘要：一个视频介绍但丁《神曲》的宇宙观，作为创作设定参考。
  - need_score：4
  - priority：P2
  - reason：娱乐内容，介绍但丁神曲宇宙观，标题有趣，适合轻松观看。
  - evidence：但丁, 神曲, 宇宙观
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：review
  - notification_decision：silent

- **中国人为什么要贿赂撒旦？一个视频看懂外国人是如何看待中国神话（世界神话地图杂谈篇）**
  - 来源：馆长刘下饭_环球档案
  - 链接：https://www.bilibili.com/video/BV1de6rBrEBE
  - 评分：2
  - 摘要：一个B站视频中，创作者讨论外国人对中国神话的误解，例如认为中国人贿赂撒旦，并说明自己因英语水平有限可能解读不准。
  - need_score：4
  - priority：P2
  - reason：内容轻松有趣，讨论外国人对中国神话的误解，适合放松观看，但创作者信息准确性存疑。
  - evidence：标题：中国人为什么要贿赂撒旦？, 摘要：讨论外国人对中国神话的误解，创作者坦诚英语水平有限
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

### 我关注的前沿咋样了

- **Voice Cloning is now live via the xAI API! Create a custom voice in less than 2 minutes or select f...**
  - 中文解释：xAI API 现已支持语音克隆！不到2分钟创建自定义语音或从80+语音库中选择
  - 来源：xAI(@xai)
  - 链接：https://x.com/xai/status/2050355373052223585
  - 评分：4
  - 摘要：xAI宣布通过API推出语音克隆功能，可在2分钟内创建自定义语音或从80多种语音库中选择，支持28种语言，用于语音代理、有声书、游戏角色等场景。
  - need_score：5
  - priority：P0
  - reason：xAI 发布语音克隆 API，是重要的 AI 产品动态，属于前沿技术趋势。
  - evidence：xAI, 语音克隆, API, 多语言
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **Today we’re announcing an agreement with Amazon Web Services to bring tens of millions of AWS Gravit...**
  - 中文解释：Meta与AWS达成协议，引入数千万Graviton核心扩展AI基础设施
  - 来源：AI at Meta(@AIatMeta)
  - 链接：https://x.com/AIatMeta/status/2047647617681957207
  - 评分：3
  - 摘要：Meta宣布与AWS合作，将引入数百万AWS Graviton核心以扩展AI基础设施，支持Meta AI及代理服务。
  - need_score：5
  - priority：P0
  - reason：Meta与AWS扩大AI基础设施合作，引入Graviton核心，是AI算力前沿的重要动态。
  - evidence：AWS Graviton, Meta AI, agentic experiences
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **把 tmux 变成 AI 协作总线：我为什么觉得 smux 这个小工具很有意思**
  - 来源：everystep
  - 链接：https://mp.weixin.qq.com/s/4ROPNgcscY07qJlnQtBENg
  - 评分：3
  - 摘要：介绍 smux 工具，通过一条命令整合 tmux 和多个 AI 终端工具，解决多模型协作时的终端混乱问题。
  - need_score：5
  - priority：P0
  - reason：介绍 smux 工具，整合多个 AI 终端，属于 AI 工具前沿动态。
  - evidence：smux, Claude Code, Codex, Gemini CLI, AI终端协作
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：silent

- **5/ https://t.co/mtEUo3Appi**
  - 中文解释：系列第五部分：Meta Muse Spark演示
  - 来源：AI at Meta(@AIatMeta)
  - 链接：https://x.com/AIatMeta/status/2042360019300372634
  - 评分：3
  - 摘要：Meta展示了Muse Spark工具，能从截图推断产品逻辑，超越了传统图像到代码的能力。
  - need_score：5
  - priority：P0
  - reason：Meta展示Muse Spark工具，能从截图推断产品逻辑，是AI前沿的重要进展。
  - evidence：Meta, Muse Spark, 产品逻辑推断
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：skim
  - notification_decision：silent

- **AI cybersecurity is not proof of work**
  - 中文解释：AI网络安全并非工作量证明
  - 来源：antirez.com
  - 链接：http://antirez.com/news/163
  - 评分：4
  - 摘要：文章论证AI网络安全不应类比工作量证明，强调模型智能（而非算力）才是发现代码漏洞的关键，并以OpenBSD SACK漏洞为例说明弱模型无限推理也无法发现真正漏洞。
  - need_score：5
  - priority：P0
  - reason：作者antirez（Redis创始人）提出AI安全应从算力竞赛转向模型智能竞赛，观点新颖且具有前瞻性，对理解AI在安全领域的局限性和未来方向有启发。
  - evidence：AI网络安全并非工作量证明, 模型智能决定漏洞发现能力, OpenBSD SACK漏洞案例分析
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Redis patterns for coding**
  - 中文解释：Redis编程模式
  - 来源：antirez.com
  - 链接：http://antirez.com/news/161
  - 评分：4
  - 摘要：Redis作者antirez发布了一个面向LLM和编码代理的Redis模式与命令文档站点。
  - need_score：5
  - priority：P0
  - reason：Redis作者发布面向LLM和编码代理的文档站点，体现AI与数据库结合的新趋势。
  - evidence：Redis官方将LLM/编码代理视为重要文档消费者, 针对编码代理的文档组织方式可能成为新趋势
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **UI is dead, long live the UI \| UNTAG**
  - 中文解释：用户界面已死，用户界面万岁
  - 来源：#UNTAG
  - 链接：https://utgd.net/article/21344
  - 评分：3
  - 摘要：探讨人工智能时代用户界面（UI）的变革，提出UI已死但新UI诞生的观点。
  - need_score：5
  - priority：P0
  - reason：讨论AI重新定义UI范式，属重要前沿趋势。
  - evidence：AI重新定义人机交互, 传统UI可能被对话式取代, UI设计师角色转变
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：silent

- **🔜**
  - 中文解释：🔜 Muse Spark API即将推出
  - 来源：AI at Meta(@AIatMeta)
  - 链接：https://x.com/AIatMeta/status/2042617283638628489
  - 评分：3
  - 摘要：AI at Meta宣布Alexandr Wang的Muse Spark API即将推出，开发者可将其集成到agentic harnesses中。
  - need_score：4
  - priority：P1
  - reason：涉及Muse Spark API的发布预告，属于AI工具和Agent生态的前沿动态。
  - evidence：Muse Spark API, agentic harnesses, AI at Meta
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：skim
  - notification_decision：silent

### 我关心的话题议题有什么新的进展

- **把 tmux 变成 AI 协作总线：我为什么觉得 smux 这个小工具很有意思**
  - 来源：everystep
  - 链接：https://mp.weixin.qq.com/s/4ROPNgcscY07qJlnQtBENg
  - 评分：3
  - 摘要：介绍 smux 工具，通过一条命令整合 tmux 和多个 AI 终端工具，解决多模型协作时的终端混乱问题。
  - need_score：4
  - priority：P1
  - reason：匹配关注议题 AI Agent，提供了终端协作工具新进展。
  - evidence：smux, Claude Code, AI Agent协作
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：silent

- **🔜**
  - 中文解释：🔜 Muse Spark API即将推出
  - 来源：AI at Meta(@AIatMeta)
  - 链接：https://x.com/AIatMeta/status/2042617283638628489
  - 评分：3
  - 摘要：AI at Meta宣布Alexandr Wang的Muse Spark API即将推出，开发者可将其集成到agentic harnesses中。
  - need_score：4
  - priority：P1
  - reason：匹配AI Agent议题，提供了Muse Spark API即将推出的新进展。
  - evidence：agentic harnesses, Alexandr Wang
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：skim
  - notification_decision：silent

### 有什么是我值得看的

- **AI cybersecurity is not proof of work**
  - 中文解释：AI网络安全并非工作量证明
  - 来源：antirez.com
  - 链接：http://antirez.com/news/163
  - 评分：4
  - 摘要：文章论证AI网络安全不应类比工作量证明，强调模型智能（而非算力）才是发现代码漏洞的关键，并以OpenBSD SACK漏洞为例说明弱模型无限推理也无法发现真正漏洞。
  - need_score：5
  - priority：P0
  - reason：内容质量高（来源antirez.com，作者权威）、观点深刻、论证扎实，对技术从业者具有较高阅读价值。
  - evidence：标题及摘要表明核心论点, 详细论证弱模型与强模型差异, 实际漏洞案例佐证
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Redis patterns for coding**
  - 中文解释：Redis编程模式
  - 来源：antirez.com
  - 链接：http://antirez.com/news/161
  - 评分：4
  - 摘要：Redis作者antirez发布了一个面向LLM和编码代理的Redis模式与命令文档站点。
  - need_score：5
  - priority：P1
  - reason：Redis官方高质量文档，对开发者和AI应用有直接实用价值，信息密度高。
  - evidence：actionability=5, value_score=4, personal_relevance=4
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Voice Cloning is now live via the xAI API! Create a custom voice in less than 2 minutes or select f...**
  - 中文解释：xAI API 现已支持语音克隆！不到2分钟创建自定义语音或从80+语音库中选择
  - 来源：xAI(@xai)
  - 链接：https://x.com/xai/status/2050355373052223585
  - 评分：4
  - 摘要：xAI宣布通过API推出语音克隆功能，可在2分钟内创建自定义语音或从80多种语音库中选择，支持28种语言，用于语音代理、有声书、游戏角色等场景。
  - need_score：4
  - priority：P1
  - reason：官方发布的产品更新，具有技术前瞻性和实际应用价值，值得阅读了解详情。
  - evidence：xAI, 语音克隆, API
  - confidence：0.75
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **混沌周刊 #42 \| 谁的救生衣**
  - 来源：混沌周刊
  - 链接：https://weekly.love/issue-42
  - 评分：4
  - 摘要：本期混沌周刊从开发者视角总结了近期科技行业裁员、苹果功能调整、.NET 7发布等事件，并反思科技从业者的处境。
  - need_score：4
  - priority：P1
  - reason：内容质量高，视角独特，对开发者有参考价值，综合评分高。
  - evidence：value_score:4, personal_relevance:4, source_quality:4, reason: 内容综合了近期科技行业重要动态
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Today we’re announcing an agreement with Amazon Web Services to bring tens of millions of AWS Gravit...**
  - 中文解释：Meta与AWS达成协议，引入数千万Graviton核心扩展AI基础设施
  - 来源：AI at Meta(@AIatMeta)
  - 链接：https://x.com/AIatMeta/status/2047647617681957207
  - 评分：3
  - 摘要：Meta宣布与AWS合作，将引入数百万AWS Graviton核心以扩展AI基础设施，支持Meta AI及代理服务。
  - need_score：4
  - priority：P1
  - reason：对于关注AI前沿的读者，这是值得一读的行业合作新闻。
  - evidence：Meta, AWS, AI基础设施
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

- **把 tmux 变成 AI 协作总线：我为什么觉得 smux 这个小工具很有意思**
  - 来源：everystep
  - 链接：https://mp.weixin.qq.com/s/4ROPNgcscY07qJlnQtBENg
  - 评分：3
  - 摘要：介绍 smux 工具，通过一条命令整合 tmux 和多个 AI 终端工具，解决多模型协作时的终端混乱问题。
  - need_score：4
  - priority：P1
  - reason：涉及实际工具，可操作性强，对 AI 工作流有参考价值。
  - evidence：smux工具, AI工作流
  - confidence：0.7
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：silent

- **UI is dead, long live the UI \| UNTAG**
  - 中文解释：用户界面已死，用户界面万岁
  - 来源：#UNTAG
  - 链接：https://utgd.net/article/21344
  - 评分：3
  - 摘要：探讨人工智能时代用户界面（UI）的变革，提出UI已死但新UI诞生的观点。
  - need_score：4
  - priority：P1
  - reason：具有高新颖性和思辨价值，但需要全文确认细节。
  - evidence：标题引人思考, 摘要暗示重要观点
  - confidence：0.6
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：silent

- **Nothing ever dies. It merely becomes embarrassing.**
  - 中文解释：没有什么会真正消亡，它只是变得尴尬
  - 来源：Experimental History
  - 链接：https://www.experimental-history.com/p/nothing-ever-dies-it-merely-becomes
  - 评分：4
  - 摘要：本文探讨科学现象为何难以被证伪，即使面临复现危机，旧理论仍以新名称继续存在，提出‘现象从不消亡，只是变得尴尬’的类比。
  - need_score：4
  - priority：P1
  - reason：观点新颖，对科学传播和复现危机有启发，信息密度较高。
  - evidence：提出‘现象从不消亡，只是变得尴尬’的类比, 讨论power posing等理论的持续存在
  - confidence：0.88
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **Don't use localhost:3000, use your own custom domain**
  - 中文解释：不要使用localhost:3000，使用你自己的自定义域名
  - 来源：idiallo.com
  - 链接：https://idiallo.com/blog/say-no-to-localhost3000-use-custom-domains?src=feed
  - 评分：4
  - 摘要：本文介绍如何在本地开发中使用自定义域名替代localhost和端口号，通过修改hosts文件并配置Nginx反向代理来实现。
  - need_score：4
  - priority：P2
  - reason：文章提供实用的本地开发环境改进方法，操作步骤清晰，可立即应用，有明确阅读收益。
  - evidence：actionability=5, 内容包含具体配置步骤, 作者经验分享
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

### 系统通知推荐

- **Voice Cloning is now live via the xAI API! Create a custom voice in less than 2 minutes or select f...**
  - 中文解释：xAI API 现已支持语音克隆！不到2分钟创建自定义语音或从80+语音库中选择
  - 来源：xAI(@xai)
  - 链接：https://x.com/xai/status/2050355373052223585
  - 评分：4
  - 摘要：xAI宣布通过API推出语音克隆功能，可在2分钟内创建自定义语音或从80多种语音库中选择，支持28种语言，用于语音代理、有声书、游戏角色等场景。
  - 理由：官方发布的产品更新，具有技术前瞻性和实际应用价值，但摘要信息有限，需获取完整公告以确认细节和限制。
  - confidence：0.8
  - needs_more_context：True
  - suggested_action：read
  - notification_decision：full_push

- **Don't use localhost:3000, use your own custom domain**
  - 中文解释：不要使用localhost:3000，使用你自己的自定义域名
  - 来源：idiallo.com
  - 链接：https://idiallo.com/blog/say-no-to-localhost3000-use-custom-domains?src=feed
  - 评分：4
  - 摘要：本文介绍如何在本地开发中使用自定义域名替代localhost和端口号，通过修改hosts文件并配置Nginx反向代理来实现。
  - 理由：提供实用的本地开发环境改进方法，操作步骤清晰，可立即应用。
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **混沌周刊 #42 \| 谁的救生衣**
  - 来源：混沌周刊
  - 链接：https://weekly.love/issue-42
  - 评分：4
  - 摘要：本期混沌周刊从开发者视角总结了近期科技行业裁员、苹果功能调整、.NET 7发布等事件，并反思科技从业者的处境。
  - 理由：内容综合了近期科技行业重要动态，视角独特，对开发者有参考价值
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **混沌周刊 #39 \| Coding**
  - 来源：混沌周刊
  - 链接：https://weekly.love/issue-39
  - 评分：4
  - 摘要：混沌周刊第39期推荐《编码》一书，并汇总苹果、华为、AMD等科技新闻及技术动态。
  - 理由：内容涵盖书评与科技新闻，适合快速浏览获取信息
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **How do you deal with endless work notifications?**
  - 中文解释：如何应对无止尽的工作通知？
  - 来源：Blog - Remote Work Prep
  - 链接：https://www.remoteworkprep.com/blog/how-do-you-deal-with-endless-work-notifications
  - 评分：4
  - 摘要：提出用'Boxed Sync'方法（划定同步时段）来管理无限的工作通知，避免通知干扰深度工作。
  - 理由：提供了具体可操作的方法来管理通知和深度工作，适合远程工作人士
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **AI cybersecurity is not proof of work**
  - 中文解释：AI网络安全并非工作量证明
  - 来源：antirez.com
  - 链接：http://antirez.com/news/163
  - 评分：4
  - 摘要：文章论证AI网络安全不应类比工作量证明，强调模型智能（而非算力）才是发现代码漏洞的关键，并以OpenBSD SACK漏洞为例说明弱模型无限推理也无法发现真正漏洞。
  - 理由：作者是Redis创始人，观点有深度；内容对理解AI在安全领域的局限性和未来方向有启发。
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

- **GNU and the AI reimplementations**
  - 中文解释：GNU与AI重写
  - 来源：antirez.com
  - 链接：http://antirez.com/news/162
  - 评分：4
  - 摘要：本文通过回顾GNU项目重写UNIX工具的历史，类比当前AI重写软件项目的争议，讨论版权法的界限，并质疑反对者是否言行一致。
  - 理由：作者是知名技术人物，观点独特且基于历史分析，对理解AI重写争议有深度参考价值。
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Redis patterns for coding**
  - 中文解释：Redis编程模式
  - 来源：antirez.com
  - 链接：http://antirez.com/news/161
  - 评分：4
  - 摘要：Redis作者antirez发布了一个面向LLM和编码代理的Redis模式与命令文档站点。
  - 理由：Redis官方高质量文档，对开发者和AI应用有直接实用价值
  - confidence：0.95
  - needs_more_context：False
  - suggested_action：save
  - notification_decision：full_push

- **Nothing ever dies. It merely becomes embarrassing.**
  - 中文解释：没有什么会真正消亡，它只是变得尴尬
  - 来源：Experimental History
  - 链接：https://www.experimental-history.com/p/nothing-ever-dies-it-merely-becomes
  - 评分：4
  - 摘要：本文探讨科学现象为何难以被证伪，即使面临复现危机，旧理论仍以新名称继续存在，提出‘现象从不消亡，只是变得尴尬’的类比。
  - 理由：文章观点新颖，对科学传播和学术评价有启发，值得一读。
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：read
  - notification_decision：full_push

## 5. 失败源列表

- **刘夙的科技世界**
  - 分类：社评
  - local_xml_url：-
  - xml_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - final feed_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - error_type：feed_parse_error
  - error_message：{"detail": "failed to parse feed: <unknown>:2:0: not well-formed (invalid token)"}
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