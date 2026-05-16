# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-04T13:17:41+00:00
- 结束时间：2026-05-04T13:18:21+00:00
- 日期：2026-05-04
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：20
- 已处理源数量：20
- 成功源数量：20
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：80
- new_items：2
- duplicate_items：78
- screened_items：2
- recommended_items_from_api_response：36
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：66
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
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 4 | 0 | 4 | 0 | 0 | 3 | 0 | 3 | 0 |  |
| 3 | AI Foundations | Videos | success | 4 | 0 | 4 | 0 | 2 | 2 | 0 | 3 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 4 | 0 | 4 | 0 | 1 | 3 | 0 | 4 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 4 | 0 | 4 | 0 | 1 | 1 | 0 | 3 | 0 |  |
| 6 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | 其他 | success | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 0 |  |
| 7 | 一觉醒来发生了什么 - 即刻圈子 | 国内外资讯 | success | 4 | 0 | 4 | 0 | 1 | 1 | 0 | 4 | 0 |  |
| 8 | - 政府文件库 | 国内政策 | success | 4 | 0 | 4 | 0 | 2 | 0 | 0 | 4 | 0 |  |
| 9 | 猴猴说话 | 微信公众号 | success | 4 | 0 | 4 | 0 | 1 | 2 | 0 | 4 | 0 |  |
| 10 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | 播客 | success | 4 | 0 | 4 | 0 | 4 | 3 | 0 | 1 | 0 |  |
| 11 | 波士顿圆脸 | 最娱乐 | success | 4 | 0 | 4 | 0 | 2 | 0 | 0 | 4 | 0 |  |
| 12 | 飞鸟手札 | 短知识 | success | 4 | 0 | 4 | 0 | 3 | 3 | 0 | 4 | 0 |  |
| 13 | Vista看天下 | 社评 | success | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 0 |  |
| 14 | 小众软件 | 科技与编程 | success | 4 | 0 | 4 | 0 | 4 | 1 | 0 | 3 | 0 |  |
| 15 | 猫眼看足球 | 绝活娱乐 | success | 4 | 1 | 3 | 1 | 2 | 0 | 0 | 4 | 0 |  |
| 16 | simonwillison.net | 英文博客 | success | 4 | 0 | 4 | 0 | 4 | 2 | 0 | 2 | 0 |  |
| 17 | 你不知道的行业内幕 - 即刻圈子 | 资讯 | success | 4 | 1 | 3 | 1 | 0 | 2 | 0 | 4 | 0 |  |
| 18 | AliAbdaal | 长知识 | success | 4 | 0 | 4 | 0 | 3 | 1 | 0 | 3 | 0 |  |
| 19 | tanscp | Articles | success | 4 | 0 | 4 | 0 | 3 | 3 | 0 | 2 | 0 |  |
| 20 | 每周一书 – 书伴 | SocialMedia | success | 4 | 0 | 4 | 0 | 1 | 0 | 0 | 4 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

- **4连逮捕！利雅得胜利一战认清越位王C罗，挂件带队+战犯表演拦不住，马内才是真大腿（胡拜尔库迪西亚3-1利雅得胜利）**
  - 来源：猫眼看足球
  - 链接：https://www.bilibili.com/video/BV1wARvB6EBh
  - 评分：2
  - 摘要：足球复盘视频锐评C罗在比赛中的表现并称赞马内是真正大腿。
  - need_score：5
  - priority：P1
  - reason：内容为足球娱乐性复盘，轻松有趣，符合娱乐需求。
  - evidence：标题调侃C罗越位, 来源为绝活娱乐, 内容锐评球员表现
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

无
