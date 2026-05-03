# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T04:25:35+00:00
- 结束时间：2026-05-03T04:31:32+00:00
- 日期：2026-05-03
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：8
- 已处理源数量：8
- 成功源数量：8
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：16
- new_items：16
- duplicate_items：0
- screened_items：16
- recommended_items_from_api_response：6
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：16
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
| 1 | B站娱乐测试-3546676667091128 | 最娱乐 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 2 | B站娱乐测试-946974 | 最娱乐 | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 3 | B站娱乐测试-456249922 | 最娱乐 | success | 2 | 2 | 0 | 2 | 1 | 0 | 0 | 2 | 0 |  |
| 4 | B站娱乐测试-269288799 | 最娱乐 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 5 | B站娱乐测试-334932680 | 最娱乐 | success | 2 | 2 | 0 | 2 | 1 | 0 | 0 | 2 | 0 |  |
| 6 | B站娱乐测试-1073153713 | 最娱乐 | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 7 | B站娱乐测试-6697975 | 最娱乐 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |
| 8 | B站娱乐测试-591610354 | 最娱乐 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

- **【乐意效劳｜翻跳】昭和打工人在工位跳舞珍贵影像**
  - 来源：B站娱乐测试-3546676667091128
  - 链接：https://www.bilibili.com/video/BV1WU9YBTEtM
  - 评分：2
  - 摘要：两位UP主合作翻跳昭和风格舞蹈，并制作了卡通形象，庆祝五一劳动节。
  - need_score：5
  - priority：P0
  - reason：轻松有趣的翻跳舞蹈视频，昭和风格和AI改编音乐增添趣味，适合放松心情。
  - evidence：标题含翻跳、昭和风, 摘要提及五一快乐, 内容为合作舞蹈视频
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **世纪双铲！球王C罗复刻世纪名场面，2肘1跳1红打服全场，名梗你什么冠军的底蕴来源**
  - 来源：B站娱乐测试-456249922
  - 链接：https://www.bilibili.com/video/BV1QX9aByEc2
  - 评分：1
  - 摘要：视频复盘解析C罗在比赛中做出两次肘击和一次跳跃动作导致红牌罚下，并关联足球文化中的名梗“你什么冠军”的由来。
  - need_score：4
  - priority：P2
  - reason：内容为足球娱乐复盘，结合C罗争议场面和名梗，轻松有趣，适合放松。
  - evidence：C罗, 红牌, 名场面, 娱乐
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **在7周年, 重生的凯尔希得到了明日方舟里最浪漫的名字**
  - 来源：B站娱乐测试-591610354
  - 链接：https://www.bilibili.com/video/BV1heRjBiEkN
  - 评分：2
  - 摘要：《明日方舟》七周年活动中，角色凯尔希重生并获得新名字“Kal'tsit·Esperanta”，被外国玩家称赞为美丽名字。
  - need_score：4
  - priority：P3
  - reason：内容轻松有趣，涉及游戏角色命名，适合放松。
  - evidence：标题, 摘要, 来源类别为最娱乐
  - confidence：0.8
  - needs_more_context：False
  - suggested_action：ignore
  - notification_decision：silent

- **“再散多几次烟给卓玛，传统烟应该换成快插”丨《快插》-缺支烟（怪咖-薛之谦）纯真烟嗓吉他弹唱丨填词丨改编丨抽象丨丁曲丨奶狗丨呼麦**
  - 来源：B站娱乐测试-269288799
  - 链接：https://www.bilibili.com/video/BV18nDiBGELa
  - 评分：2
  - 摘要：B站UP主用薛之谦《怪咖》改编成禁烟主题歌曲《快插》，仅供娱乐。
  - need_score：4
  - priority：P3
  - reason：轻松有趣的禁烟主题改编歌曲，适合放松观看。
  - evidence：标题含抽象、奶狗等标签, source_category为最娱乐
  - confidence：0.7
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
