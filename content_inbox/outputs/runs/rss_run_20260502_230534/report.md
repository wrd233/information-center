# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-02T15:05:34+00:00
- 结束时间：2026-05-02T15:05:34+00:00
- 日期：2026-05-02
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：501
- 已处理源数量：0
- 成功源数量：0
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：0
- new_items：0
- duplicate_items：0
- screened_items：0
- recommended_items_from_api_response：0
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：0
- failed_items：0
- inbox 查询模式：not_run
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|

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
