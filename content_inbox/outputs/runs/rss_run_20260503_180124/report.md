# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T10:01:24+00:00
- 结束时间：2026-05-03T10:01:39+00:00
- 日期：2026-05-03
- URL 模式：remote

## 1. 总览

- 选中 RSS 源数量：27
- 已处理源数量：27
- 成功源数量：27
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：135
- new_items：27
- duplicate_items：108
- screened_items：0
- recommended_items_from_api_response：75
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：111
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
| 1 | bilibili-user-1033890839 | bilibili | success | 5 | 0 | 5 | 0 | 2 | 0 | 0 | 4 | 0 |  |
| 2 | bilibili-user-25073738 | bilibili | success | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 5 | 0 |  |
| 3 | bilibili-user-19319172 | bilibili | success | 5 | 0 | 5 | 0 | 4 | 0 | 0 | 2 | 0 |  |
| 4 | bilibili-user-1858861103 | bilibili | success | 5 | 0 | 5 | 0 | 1 | 0 | 0 | 5 | 0 |  |
| 5 | bilibili-user-470585121 | bilibili | success | 5 | 0 | 5 | 0 | 3 | 0 | 0 | 4 | 0 |  |
| 6 | bilibili-user-1288663494 | bilibili | success | 5 | 0 | 5 | 0 | 1 | 0 | 0 | 5 | 0 |  |
| 7 | bilibili-user-252411834 | bilibili | success | 5 | 0 | 5 | 0 | 4 | 0 | 0 | 5 | 0 |  |
| 8 | bilibili-user-431850986 | bilibili | success | 5 | 0 | 5 | 0 | 4 | 0 | 0 | 3 | 0 |  |
| 9 | bilibili-user-476051104 | bilibili | success | 5 | 0 | 5 | 0 | 2 | 0 | 0 | 2 | 0 |  |
| 10 | bilibili-user-17780825 | bilibili | success | 5 | 0 | 5 | 0 | 2 | 0 | 0 | 5 | 0 |  |
| 11 | bilibili-user-495979610 | bilibili | success | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 4 | 0 |  |
| 12 | bilibili-user-14004258 | bilibili | success | 5 | 0 | 5 | 0 | 4 | 0 | 0 | 3 | 0 |  |
| 13 | bilibili-user-521296768 | bilibili | success | 5 | 0 | 5 | 0 | 3 | 0 | 0 | 5 | 0 |  |
| 14 | bilibili-user-489640651 | bilibili | success | 5 | 0 | 5 | 0 | 2 | 0 | 0 | 4 | 0 |  |
| 15 | bilibili-user-1850874570 | bilibili | success | 5 | 0 | 5 | 0 | 1 | 0 | 0 | 1 | 0 |  |
| 16 | bilibili-user-3493286931073848 | bilibili | success | 5 | 0 | 5 | 0 | 1 | 0 | 0 | 5 | 0 |  |
| 17 | bilibili-user-213845897 | bilibili | success | 5 | 0 | 5 | 0 | 2 | 0 | 0 | 5 | 0 |  |
| 18 | bilibili-user-409842788 | bilibili | success | 5 | 0 | 5 | 0 | 1 | 0 | 0 | 5 | 0 |  |
| 19 | bilibili-user-600428973 | bilibili | success | 5 | 0 | 5 | 0 | 3 | 0 | 0 | 5 | 0 |  |
| 20 | bilibili-user-17549684 | bilibili | success | 5 | 0 | 5 | 0 | 1 | 0 | 0 | 2 | 0 |  |
| 21 | bilibili-user-1366786686 | bilibili | success | 5 | 0 | 5 | 0 | 4 | 0 | 0 | 2 | 0 |  |
| 22 | bilibili-user-3537109151386355 | bilibili | success | 5 | 5 | 0 | 0 | 5 | 0 | 0 | 5 | 0 |  |
| 23 | bilibili-user-346563107 | bilibili | success | 5 | 5 | 0 | 0 | 5 | 0 | 0 | 5 | 0 |  |
| 24 | bilibili-user-730732 | bilibili | success | 5 | 2 | 3 | 0 | 5 | 0 | 0 | 5 | 0 |  |
| 25 | bilibili-user-1372433 | bilibili | success | 5 | 5 | 0 | 0 | 5 | 0 | 0 | 5 | 0 |  |
| 26 | bilibili-user-281127303 | bilibili | success | 5 | 5 | 0 | 0 | 5 | 0 | 0 | 5 | 0 |  |
| 27 | bilibili-user-279991456 | bilibili | success | 5 | 5 | 0 | 0 | 5 | 0 | 0 | 5 | 0 |  |

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
