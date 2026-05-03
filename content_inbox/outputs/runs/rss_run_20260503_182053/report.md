# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T10:20:53+00:00
- 结束时间：2026-05-03T10:20:59+00:00
- 日期：2026-05-03
- URL 模式：remote

## 1. 总览

- 选中 RSS 源数量：5
- 已处理源数量：5
- 成功源数量：3
- 失败源数量：2
- 已知失败跳过数量：0
- total_items：6
- new_items：0
- duplicate_items：6
- screened_items：0
- recommended_items_from_api_response：2
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：6
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
| 1 | 东西智库 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 2 | 少数派 | Articles | success | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 2 | 0 |  |
| 3 | Twitter-@Tom-Huang | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 4 | 即刻-笔记交流站 | SocialMedia | success | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 2 | 0 |  |
| 5 | 书伴-每周一书 | SocialMedia | success | 2 | 0 | 2 | 0 | 0 | 2 | 0 | 2 | 0 |  |

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

- **东西智库**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/dx2025
  - final feed_url：http://127.0.0.1:1200/dx2025
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}
- **Twitter-@Tom-Huang**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/twitter/user/tuturetom
  - final feed_url：http://127.0.0.1:1200/twitter/user/tuturetom
  - error_type：rsshub_503
  - error_message：{"detail": "HTTP Error 503: Service Unavailable"}