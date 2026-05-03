# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-03T04:09:29+00:00
- 结束时间：2026-05-03T04:13:23+00:00
- 日期：2026-05-03
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：5
- 已处理源数量：5
- 成功源数量：5
- 失败源数量：0
- 已知失败跳过数量：0
- total_items：10
- new_items：10
- duplicate_items：0
- screened_items：10
- recommended_items_from_api_response：4
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：10
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
| 1 | Hi, DIYgod | Articles | success | 2 | 2 | 0 | 2 | 0 | 1 | 0 | 2 | 0 |  |
| 2 | 图书推荐 – 书伴 | SocialMedia | success | 2 | 2 | 0 | 2 | 0 | 1 | 0 | 2 | 0 |  |
| 3 | AI Foundations | Videos | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 4 | Rolen's Blog | 个人博客-人生 | success | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 2 | 0 |  |
| 5 | 最新发布_共产党员网 | 党政信息 | success | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

无

### 我关注的前沿咋样了

- **2025 重新定义的生活**
  - 来源：Hi, DIYgod
  - 链接：https://diygod.cc/2025
  - 评分：3
  - 摘要：DIYgod的2025年个人年度总结，涵盖AI冲击、育儿、投资经验与开源商业化反思。
  - need_score：4
  - priority：P1
  - reason：提供了AI对插画和编程岗位替代的深刻趋势观察，涉及GPT-4、Stable Diffusion、AI Coding等前沿技术动态。
  - evidence：GPT-4, Stable Diffusion, GitHub Copilot, AI Coding工具, vibe coding
  - confidence：0.85
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

### 我关心的话题议题有什么新的进展

无

### 有什么是我值得看的

- **2025 重新定义的生活**
  - 来源：Hi, DIYgod
  - 链接：https://diygod.cc/2025
  - 评分：3
  - 摘要：DIYgod的2025年个人年度总结，涵盖AI冲击、育儿、投资经验与开源商业化反思。
  - need_score：4
  - priority：P1
  - reason：内容有深度，提供AI趋势、投资教训和育儿反思等多维度个人经验，值得阅读。
  - evidence：
  - confidence：0.9
  - needs_more_context：False
  - suggested_action：skim
  - notification_decision：silent

### 系统通知推荐

无

## 5. 失败源列表

无
