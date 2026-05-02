# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-02T15:26:43+00:00
- 结束时间：2026-05-02T15:27:41+00:00
- 日期：2026-05-02
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：20
- 已处理源数量：20
- 成功源数量：20
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：60
- new_items：0
- duplicate_items：60
- screened_items：0
- recommended_items_from_api_response：18
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：39
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
| 1 | Hi, DIYgod | Articles | success | 3 | 0 | 3 | 0 | 2 | 2 | 0 | 1 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 3 | 0 | 3 | 0 | 3 | 0 | 0 | 3 | 0 |  |
| 3 | AI Foundations | Videos | success | 3 | 0 | 3 | 0 | 3 | 3 | 0 | 0 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 3 | 0 | 3 | 0 | 0 | 1 | 0 | 2 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 3 | 0 | 3 | 0 | 0 | 2 | 0 | 1 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 3 | 0 | 3 | 0 | 0 | 1 | 0 | 2 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 3 | 0 | 3 | 0 | 3 | 3 | 0 | 0 | 0 |  |
| 11 | 波士顿圆脸 | 最娱乐 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |
| 12 | 飞鸟手札 | 短知识 | success | 3 | 0 | 3 | 0 | 1 | 3 | 0 | 0 | 0 |  |
| 13 | Vista看天下 | 社评 | success | 3 | 0 | 3 | 0 | 1 | 1 | 0 | 2 | 0 |  |
| 14 | 小众软件 | 科技与编程 | success | 3 | 0 | 3 | 0 | 1 | 1 | 0 | 2 | 0 |  |
| 15 | 猫眼看足球 | 绝活娱乐 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |
| 16 | simonwillison.net | 英文博客 | success | 3 | 0 | 3 | 0 | 3 | 3 | 0 | 0 | 0 |  |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 3 | 0 | 3 | 0 | 1 | 0 | 0 | 3 | 0 |  |
| 18 | AliAbdaal | 长知识 | success | 3 | 0 | 3 | 0 | 0 | 1 | 0 | 2 | 0 |  |
| 19 | 少数派 | 优质信息源 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |
| 20 | 每日一图-北京天文馆 | 星空 | success | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |  |

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

无
