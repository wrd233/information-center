# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T06:35:27+00:00
- 结束时间：2026-05-04T07:00:30+00:00
- 日期：2026-05-04
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：100
- 已处理源数量：27
- 成功源数量：4
- 失败源数量：23
- 已知失败跳过数量：0
- total_items：16
- new_items：8
- duplicate_items：8
- screened_items：8
- recommended_items_from_api_response：10
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：13
- failed_items：0
- inbox 查询模式：pending
- inbox 是否回退到 date=today：False

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- 连续失败达到阈值 20，提前停止运行。

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Hi, DIYgod | Articles | success | 4 | 0 | 4 | 0 | 4 | 2 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 4 | 4 | 0 | 4 | 1 | 1 | 0 | 3 | 0 |  |
| 3 | AI Foundations | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 4 | Rolen's Blog | 个人博客-人生 | success | 4 | 0 | 4 | 0 | 3 | 1 | 0 | 4 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 4 | 4 | 0 | 4 | 2 | 0 | 0 | 4 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 8 | - 政府文件库 | 国内政策 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 9 | 猴猴说话 | 微信公众号 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 11 | 波士顿圆脸 | 最娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 12 | 飞鸟手札 | 短知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 13 | Vista看天下 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 14 | 小众软件 | 科技与编程 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 15 | 猫眼看足球 | 绝活娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 16 | simonwillison.net | 英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 18 | AliAbdaal | 长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 19 | tanscp | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 20 | 每周一书 – 书伴 | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 21 | Ben's Love | 个人博客-人生 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 22 | 新华社新闻_新华网 | 党政信息 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 23 | 潦草学者 | 微信公众号 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 24 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | 播客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 25 | 瓶子君152 | 最娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 26 | 英语播客党 | 短知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 27 | Tinyfool的个人网站 | 社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |

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

- **AI Foundations**
  - 分类：Videos
  - local_xml_url：-
  - xml_url：https://www.youtube.com/feeds/videos.xml?channel_id=UCWZwfV3ICOt3uEPpW6hYK4g
  - final feed_url：https://www.youtube.com/feeds/videos.xml?channel_id=UCWZwfV3ICOt3uEPpW6hYK4g
  - error_type：unknown
  - error_message：{"detail": "HTTP Error 404: Not Found"}
- **最新发布_共产党员网**
  - 分类：党政信息
  - local_xml_url：http://127.0.0.1:1200/12371/zxfb
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/12371/zxfb
  - final feed_url：http://host.docker.internal:1200/12371/zxfb
  - error_type：timeout
  - error_message："timed out"
- **一觉醒来发生了什么 - 即刻圈子**
  - 分类：国内外资讯
  - local_xml_url：http://127.0.0.1:1200/jike/topic/553870e8e4b0cafb0a1bef68
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/jike/topic/553870e8e4b0cafb0a1bef68
  - final feed_url：http://host.docker.internal:1200/jike/topic/553870e8e4b0cafb0a1bef68
  - error_type：timeout
  - error_message："timed out"
- **- 政府文件库**
  - 分类：国内政策
  - local_xml_url：http://127.0.0.1:1200/gov/zhengce/zhengceku/bmwj
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/gov/zhengce/zhengceku/bmwj
  - final feed_url：http://host.docker.internal:1200/gov/zhengce/zhengceku/bmwj
  - error_type：timeout
  - error_message："timed out"
- **猴猴说话**
  - 分类：微信公众号
  - local_xml_url：http://127.0.0.1:8003/feed/MP_WXS_3279284299.atom
  - xml_url：http://192.168.1.6:8003/feed/MP_WXS_3279284299.atom
  - final feed_url：http://host.docker.internal:8003/feed/MP_WXS_3279284299.atom
  - error_type：timeout
  - error_message："timed out"
- **小宇宙 Podcast 643928f99361a4e7c38a9555**
  - 分类：播客
  - local_xml_url：http://127.0.0.1:1200/xiaoyuzhou/podcast/643928f99361a4e7c38a9555
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/xiaoyuzhou/podcast/643928f99361a4e7c38a9555
  - final feed_url：http://host.docker.internal:1200/xiaoyuzhou/podcast/643928f99361a4e7c38a9555
  - error_type：timeout
  - error_message："timed out"
- **波士顿圆脸**
  - 分类：最娱乐
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/346563107
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/346563107
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/346563107
  - error_type：timeout
  - error_message："timed out"
- **飞鸟手札**
  - 分类：短知识
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/1366786686
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/1366786686
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/1366786686
  - error_type：timeout
  - error_message："timed out"
- **Vista看天下**
  - 分类：社评
  - local_xml_url：-
  - xml_url：https://plink.anyfeeder.com/weixin/vistaweek
  - final feed_url：https://plink.anyfeeder.com/weixin/vistaweek
  - error_type：timeout
  - error_message："timed out"
- **小众软件**
  - 分类：科技与编程
  - local_xml_url：-
  - xml_url：https://www.appinn.com/feed/
  - final feed_url：https://www.appinn.com/feed/
  - error_type：timeout
  - error_message："timed out"
- **猫眼看足球**
  - 分类：绝活娱乐
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/456249922
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/456249922
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/456249922
  - error_type：timeout
  - error_message："timed out"
- **simonwillison.net**
  - 分类：英文博客
  - local_xml_url：-
  - xml_url：https://simonwillison.net/atom/everything/
  - final feed_url：https://simonwillison.net/atom/everything/
  - error_type：timeout
  - error_message："timed out"
- **你不知道的行业内幕 - 即刻圈子**
  - 分类：资讯
  - local_xml_url：http://127.0.0.1:1200/jike/topic/5699f451d3e8351200bffdc8
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/jike/topic/5699f451d3e8351200bffdc8
  - final feed_url：http://host.docker.internal:1200/jike/topic/5699f451d3e8351200bffdc8
  - error_type：timeout
  - error_message："timed out"
- **AliAbdaal**
  - 分类：长知识
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/3546581580122806
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/3546581580122806
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/3546581580122806
  - error_type：timeout
  - error_message："timed out"
- **tanscp**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://tanscp.com/feed/
  - final feed_url：https://tanscp.com/feed/
  - error_type：timeout
  - error_message："timed out"
- **每周一书 – 书伴**
  - 分类：SocialMedia
  - local_xml_url：http://127.0.0.1:1200/bookfere/weekly
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bookfere/weekly
  - final feed_url：http://host.docker.internal:1200/bookfere/weekly
  - error_type：timeout
  - error_message："timed out"
- **Ben's Love**
  - 分类：个人博客-人生
  - local_xml_url：-
  - xml_url：https://bens.love/feed
  - final feed_url：https://bens.love/feed
  - error_type：timeout
  - error_message："timed out"
- **新华社新闻_新华网**
  - 分类：党政信息
  - local_xml_url：-
  - xml_url：https://plink.anyfeeder.com/newscn/whxw
  - final feed_url：https://plink.anyfeeder.com/newscn/whxw
  - error_type：timeout
  - error_message："timed out"
- **潦草学者**
  - 分类：微信公众号
  - local_xml_url：http://127.0.0.1:8003/feed/MP_WXS_3239649460.atom
  - xml_url：http://192.168.1.6:8003/feed/MP_WXS_3239649460.atom
  - final feed_url：http://host.docker.internal:8003/feed/MP_WXS_3239649460.atom
  - error_type：timeout
  - error_message："timed out"
- **小宇宙 Podcast 61cbaac48bb4cd867fcabe22**
  - 分类：播客
  - local_xml_url：http://127.0.0.1:1200/xiaoyuzhou/podcast/61cbaac48bb4cd867fcabe22
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/xiaoyuzhou/podcast/61cbaac48bb4cd867fcabe22
  - final feed_url：http://host.docker.internal:1200/xiaoyuzhou/podcast/61cbaac48bb4cd867fcabe22
  - error_type：timeout
  - error_message："timed out"
- **瓶子君152**
  - 分类：最娱乐
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/730732
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/730732
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/730732
  - error_type：timeout
  - error_message："timed out"
- **英语播客党**
  - 分类：短知识
  - local_xml_url：http://127.0.0.1:1200/bilibili/user/video/3537109151386355
  - xml_url：https://macmini-rsshub.tail99ecfa.ts.net/bilibili/user/video/3537109151386355
  - final feed_url：http://host.docker.internal:1200/bilibili/user/video/3537109151386355
  - error_type：timeout
  - error_message："timed out"
- **Tinyfool的个人网站**
  - 分类：社评
  - local_xml_url：-
  - xml_url：https://codechina.org/feed/
  - final feed_url：https://codechina.org/feed/
  - error_type：timeout
  - error_message："timed out"