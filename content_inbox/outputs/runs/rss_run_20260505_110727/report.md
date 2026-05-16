# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-05T03:07:27+00:00
- 结束时间：2026-05-05T03:08:44+00:00
- 日期：2026-05-05
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：50
- 已处理源数量：50
- 成功源数量：49
- 失败源数量：1
- 已知失败跳过数量：0
- total_items：1
- new_items：1
- duplicate_items：0
- screened_items：1
- recommended_items_from_api_response：1
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：1
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 增量同步模式汇总

- 同步模式：until_existing
- 命中历史锚点的源数：49
- 新源基线同步数：0
- 老源未找到锚点数：0
- selected_items_for_processing 总计：1

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- source concurrency=2, llm_max_concurrency_requested=2, llm_max_concurrency_applied=2, screening_mode_requested=merged, screening_mode_applied=merged, timeout=600, sleep=1.0, limit_per_source=20

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 3 | AI Foundations | Videos | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 11 | 波士顿圆脸 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 12 | 飞鸟手札 | 短知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 13 | Vista看天下 | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 14 | 小众软件 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 15 | 猫眼看足球 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 16 | simonwillison.net | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 18 | AliAbdaal | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 19 | tanscp | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 20 | 每周一书 – 书伴 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 21 | Ben's Love | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 22 | 新华社新闻_新华网 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 23 | 潦草学者 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 24 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 25 | 瓶子君152 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 26 | 英语播客党 | 短知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 27 | Tinyfool的个人网站 | 社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 28 | HelloGithub - 月刊 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 29 | 陈大东瓜 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 30 | jeffgeerling.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 31 | 食事史馆 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 32 | Airing 的博客 | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 33 | 笔记交流站 - 即刻圈子 | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 34 | 莫比乌斯 | 个人博客-人生 | success | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |  |
| 35 | 半月谈快报 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 36 | L先生说 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 37 | 小宇宙 Podcast 648b0b641c48983391a63f98 | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 38 | Super也好君 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 39 | 刘夙的科技世界 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 40 | 宝玉的分享 | 科技与编程 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 41 | 司马尘 | 绝活娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 42 | seangoedecke.com | 英文博客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 43 | 毕导 | 长知识 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 44 | Paradise Lost | Articles | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 45 | Mike Krieger(@mikeyk) | SocialMedia | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 46 | 白熊阿丸的小屋 | 个人博客-人生 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 47 | - 求是网 | 党政信息 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 48 | 常青说 | 微信公众号 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 49 | 小宇宙 Podcast 5e5c52c9418a84a04625e6cc | 播客 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 50 | 负面能量转换器 | 最娱乐 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |

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

- **刘夙的科技世界**
  - 分类：社评
  - local_xml_url：-
  - xml_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - final feed_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - error_type：feed_parse_error
  - error_message：{"detail": "failed to parse feed: <unknown>:2:0: not well-formed (invalid token)"}