# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T13:34:42+00:00
- 结束时间：2026-05-04T13:35:31+00:00
- 日期：2026-05-04
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：10
- 已处理源数量：10
- 成功源数量：10
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：20
- new_items：2
- duplicate_items：18
- screened_items：2
- recommended_items_from_api_response：6
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
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
- source concurrency=10, llm_max_concurrency_requested=10, llm_max_concurrency_applied=10, timeout=600, sleep=0.1, limit_per_source=2

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 2 | 0 | 2 | 0 | 0 | 2 | 0 | 1 | 0 |  |
| 3 | AI Foundations | Videos | success | 2 | 0 | 2 | 0 | 1 | 1 | 0 | 2 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 2 | 0 | 2 | 0 | 1 | 1 | 0 | 2 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 2 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 2 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 2 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 2 | 0 | 2 | 0 | 0 | 2 | 0 | 2 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 2 | 0 | 2 | 0 | 2 | 2 | 0 | 0 | 0 |  |

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

无
