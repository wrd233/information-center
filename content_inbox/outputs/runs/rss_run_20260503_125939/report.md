# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T04:59:39+00:00
- 结束时间：2026-05-03T05:03:00+00:00
- 日期：2026-05-03
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：501
- 已处理源数量：10
- 成功源数量：0
- 失败源数量：10
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
| 1 | Hi, DIYgod | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 2 | tanscp | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 3 | Airing 的博客 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 4 | Rolen's Blog | 个人博客-人生 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 5 | Ben's Love | 个人博客-人生 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 6 | 莫比乌斯 | 个人博客-人生 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 7 | 白熊阿丸的小屋 | 个人博客-人生 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 8 | 草稿拾遗 | 个人博客-人生 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 11 | 豆瓣小组-无用美学 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 12 | StarYuhen | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |

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

- **Hi, DIYgod**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://diygod.cc/feed
  - final feed_url：https://diygod.cc/feed
  - error_type：timeout
  - error_message："timed out"
- **tanscp**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://tanscp.com/feed/
  - final feed_url：https://tanscp.com/feed/
  - error_type：timeout
  - error_message："timed out"
- **Airing 的博客**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://ursb.me/blog/feed.xml
  - final feed_url：https://ursb.me/blog/feed.xml
  - error_type：timeout
  - error_message："timed out"
- **Rolen's Blog**
  - 分类：个人博客-人生
  - local_xml_url：-
  - xml_url：https://rolen.wiki/feed/
  - final feed_url：https://rolen.wiki/feed/
  - error_type：timeout
  - error_message："timed out"
- **Ben's Love**
  - 分类：个人博客-人生
  - local_xml_url：-
  - xml_url：https://bens.love/feed
  - final feed_url：https://bens.love/feed
  - error_type：timeout
  - error_message："timed out"
- **莫比乌斯**
  - 分类：个人博客-人生
  - local_xml_url：-
  - xml_url：https://mobius.blog/feed/
  - final feed_url：https://mobius.blog/feed/
  - error_type：timeout
  - error_message："timed out"
- **白熊阿丸的小屋**
  - 分类：个人博客-人生
  - local_xml_url：-
  - xml_url：https://blog.bxaw.name/feed/
  - final feed_url：https://blog.bxaw.name/feed/
  - error_type：timeout
  - error_message："timed out"
- **草稿拾遗**
  - 分类：个人博客-人生
  - local_xml_url：-
  - xml_url：https://kill-the-newsletter.com/feeds/t87xbbj6p4iwfhsi.xml
  - final feed_url：https://kill-the-newsletter.com/feeds/t87xbbj6p4iwfhsi.xml
  - error_type：timeout
  - error_message："timed out"
- **豆瓣小组-无用美学**
  - 分类：Articles
  - local_xml_url：http://127.0.0.1:1200/douban/group/699356/essence
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/douban/group/699356/essence
  - final feed_url：http://host.docker.internal:1200/douban/group/699356/essence
  - error_type：timeout
  - error_message：{"detail": "timed out"}
- **StarYuhen**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.yuhenm.top/feed/
  - final feed_url：https://www.yuhenm.top/feed/
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 403: Forbidden"}