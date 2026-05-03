# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T09:36:20+00:00
- 结束时间：2026-05-03T09:51:21+00:00
- 日期：2026-05-03
- URL 模式：remote

## 1. 总览

- 选中 RSS 源数量：27
- 已处理源数量：15
- 成功源数量：0
- 失败源数量：15
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
| 1 | bilibili-user-1033890839 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 2 | bilibili-user-25073738 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 3 | bilibili-user-19319172 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 4 | bilibili-user-1858861103 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 5 | bilibili-user-470585121 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 6 | bilibili-user-1288663494 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 7 | bilibili-user-252411834 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 8 | bilibili-user-431850986 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 9 | bilibili-user-476051104 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 10 | bilibili-user-17780825 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 11 | bilibili-user-495979610 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 12 | bilibili-user-14004258 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 13 | bilibili-user-521296768 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 14 | bilibili-user-489640651 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 15 | bilibili-user-1850874570 | bilibili | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |

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

- **bilibili-user-1033890839**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/1033890839
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/1033890839
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-25073738**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/25073738
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/25073738
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-19319172**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/19319172
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/19319172
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-1858861103**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/1858861103
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/1858861103
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-470585121**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/470585121
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/470585121
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-1288663494**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/1288663494
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/1288663494
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-252411834**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/252411834
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/252411834
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-431850986**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/431850986
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/431850986
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-476051104**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/476051104
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/476051104
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-17780825**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/17780825
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/17780825
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-495979610**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/495979610
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/495979610
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-14004258**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/14004258
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/14004258
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-521296768**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/521296768
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/521296768
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-489640651**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/489640651
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/489640651
  - error_type：timeout
  - error_message："timed out"
- **bilibili-user-1850874570**
  - 分类：bilibili
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/1850874570
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/1850874570
  - error_type：timeout
  - error_message："timed out"