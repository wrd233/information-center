# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T13:12:18+00:00
- 结束时间：2026-05-04T13:13:58+00:00
- 日期：2026-05-04
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：20
- 已处理源数量：20
- 成功源数量：8
- 失败源数量：12
- 已知失败跳过数量：0
- total_items：32
- new_items：8
- duplicate_items：24
- screened_items：8
- recommended_items_from_api_response：17
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：24
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
| 1 | Hi, DIYgod | Articles | success | 4 | 0 | 4 | 0 | 2 | 2 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 3 | AI Foundations | Videos | success | 4 | 0 | 4 | 0 | 2 | 2 | 0 | 3 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 4 | 0 | 4 | 0 | 1 | 3 | 0 | 4 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 4 | 4 | 0 | 4 | 1 | 0 | 0 | 4 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 8 | - 政府文件库 | 国内政策 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 9 | 猴猴说话 | 微信公众号 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 11 | 波士顿圆脸 | 最娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 12 | 飞鸟手札 | 短知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 13 | Vista看天下 | 社评 | success | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 4 | 0 |  |
| 14 | 小众软件 | 科技与编程 | success | 4 | 0 | 4 | 0 | 4 | 1 | 0 | 3 | 0 |  |
| 15 | 猫眼看足球 | 绝活娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 16 | simonwillison.net | 英文博客 | success | 4 | 0 | 4 | 0 | 4 | 2 | 0 | 2 | 0 |  |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 18 | AliAbdaal | 长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 19 | tanscp | Articles | success | 4 | 0 | 4 | 0 | 3 | 3 | 0 | 2 | 0 |  |
| 20 | 每周一书 – 书伴 | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |

## 4. 阅读视图

### 今天看什么娱乐

- **爱出轨的水果千万不能吃**
  - 来源：Vista看天下
  - 链接：http://weixin.sogou.com/weixin?query=Vista%E7%9C%8B%E5%A4%A9%E4%B8%8B+%E7%88%B1%E5%87%BA%E8%BD%A8%E7%9A%84%E6%B0%B4%E6%9E%9C%E5%8D%83%E4%B8%87%E4%B8%8D%E8%83%BD%E5%90%83&type=2
  - 评分：2
  - 摘要：文章评论了AI生成的水果角色短剧在社交媒体上走红的现象，探讨其狗血剧情和AI的创造性。
  - need_score：5
  - priority：P1
  - reason：内容轻松有趣，描述AI生成的狗血水果短剧，非常适合放松。
  - evidence：AI短剧, 狗血剧情, 娱乐趋势
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

### 我关注的前沿咋样了

无

### 我关心的话题议题有什么新的进展

无

### 有什么是我值得看的

无

### 系统通知推荐

无

## 5. 失败源列表

- **图书推荐 – 书伴**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/bookfere/books
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bookfere/books
  - final feed_url：http://host.docker.internal:1200/bookfere/books
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **最新发布_共产党员网**
  - 分类：党政信息
  - local_xml_url：http://127.0.0.1:1200/12371/zxfb
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/12371/zxfb
  - final feed_url：http://host.docker.internal:1200/12371/zxfb
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **一觉醒来发生了什么 - 即刻圈子**
  - 分类：国内外资讯
  - local_xml_url：http://127.0.0.1:1200/jike/topic/553870e8e4b0cafb0a1bef68
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/jike/topic/553870e8e4b0cafb0a1bef68
  - final feed_url：http://host.docker.internal:1200/jike/topic/553870e8e4b0cafb0a1bef68
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **- 政府文件库**
  - 分类：国内政策
  - local_xml_url：http://127.0.0.1:1200/gov/zhengce/zhengceku/bmwj
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/gov/zhengce/zhengceku/bmwj
  - final feed_url：http://host.docker.internal:1200/gov/zhengce/zhengceku/bmwj
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **猴猴说话**
  - 分类：微信公众号
  - local_xml_url：http://127.0.0.1:8003/feed/MP_WXS_3279284299.atom
  - xml_url：http://192.168.1.6:8003/feed/MP_WXS_3279284299.atom
  - final feed_url：http://host.docker.internal:8003/feed/MP_WXS_3279284299.atom
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **小宇宙 Podcast 643928f99361a4e7c38a9555**
  - 分类：播客
  - local_xml_url：http://127.0.0.1:1200/xiaoyuzhou/podcast/643928f99361a4e7c38a9555
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/xiaoyuzhou/podcast/643928f99361a4e7c38a9555
  - final feed_url：http://host.docker.internal:1200/xiaoyuzhou/podcast/643928f99361a4e7c38a9555
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **波士顿圆脸**
  - 分类：最娱乐
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/346563107
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/346563107
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/346563107
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **飞鸟手札**
  - 分类：短知识
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/1366786686
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/1366786686
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/1366786686
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **猫眼看足球**
  - 分类：绝活娱乐
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/456249922
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/456249922
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/456249922
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **你不知道的行业内幕 - 即刻圈子**
  - 分类：资讯
  - local_xml_url：http://127.0.0.1:1200/jike/topic/5699f451d3e8351200bffdc8
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/jike/topic/5699f451d3e8351200bffdc8
  - final feed_url：http://host.docker.internal:1200/jike/topic/5699f451d3e8351200bffdc8
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **AliAbdaal**
  - 分类：长知识
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/3546581580122806
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/3546581580122806
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/3546581580122806
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}
- **每周一书 – 书伴**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/bookfere/weekly
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bookfere/weekly
  - final feed_url：http://host.docker.internal:1200/bookfere/weekly
  - error_type：network_error
  - error_message：{"detail": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"}