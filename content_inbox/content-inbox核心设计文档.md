# content-inbox 最小核心模块设计

## 1. 模块定位

`content-inbox` 是一个本地内容处理模块。

它只负责三件事：

1. 接收 RSS 源或单条内容输入。
2. 完成去重、标准化、AI 粗筛。
3. 通过 API 输出筛选结果。

它不负责阅读器界面、IM 推送、Obsidian 归档、视频转录、复杂任务调度和知识库管理。

---

## 2. 核心处理流程

所有输入统一走同一条内部流程：

```text
输入内容
  ↓
解析/提取基础信息
  ↓
去重判断
  ↓
标准化
  ↓
AI 粗筛
  ↓
存入本地数据库
  ↓
供筛选结果 API 查询
```

RSS 输入和单条内容输入的差别只在第一步：

```text
RSS 源地址
  ↓
解析 RSS item
  ↓
逐条进入统一处理流程
```

```text
单条内容
  ↓
直接进入统一处理流程
```

---

## 3. API 总览

第一版只提供三个核心接口：

```http
POST /api/rss/analyze
POST /api/content/analyze
GET  /api/inbox
```

可选保留健康检查接口：

```http
GET /health
```

---

## 4. 接口一：分析一个 RSS 源

### 4.1 用途

给定一个 RSS 源地址，系统拉取并解析该 RSS 源中的内容，然后把每条 RSS item 送入统一处理流程。

这个接口适合：

- 手动测试一个 RSS 源。
- 由脚本或定时任务定期处理某个 RSS 源。
- 后续由 RSS 源管理模块逐个调用。

### 4.2 接口

```http
POST /api/rss/analyze
```

### 4.3 请求参数

```json
{
  "feed_url": "https://example.com/feed.xml",
  "source_name": "示例 RSS 源",
  "source_category": "Articles/AI",
  "limit": 20,
  "screen": true
}
```

### 4.4 参数说明

| 参数 | 必填 | 说明 |
|---|---:|---|
| `feed_url` | 是 | RSS / Atom 源地址 |
| `source_name` | 否 | 来源名称；为空时可从 RSS 元信息中提取 |
| `source_category` | 否 | 来源分类；用于辅助 AI 判断 |
| `limit` | 否 | 本次最多处理多少条 item |
| `screen` | 否 | 是否调用 AI 粗筛；默认为 true |

### 4.5 内部流程

```text
接收 feed_url
  ↓
请求 RSS / Atom 内容
  ↓
解析 feed 元信息和 item 列表
  ↓
对每条 item 执行：
    1. 提取标题、链接、发布时间、作者、摘要、正文片段
    2. 去重判断
    3. 标准化
    4. AI 粗筛
    5. 存入本地数据库
  ↓
返回本次处理结果
```

### 4.6 返回示例

```json
{
  "ok": true,
  "feed_url": "https://example.com/feed.xml",
  "source_name": "示例 RSS 源",
  "total_items": 20,
  "new_items": 12,
  "duplicate_items": 8,
  "screened_items": 12,
  "recommended_items": 3,
  "failed_items": 0
}
```

---

## 5. 接口二：分析一条内容

### 5.1 用途

给定一条外部内容，系统对其进行去重、标准化和 AI 粗筛。

这个接口用于复用内容处理中心的核心能力。

适合接入：

- 手动 URL 分析。
- 浏览器剪藏。
- Memo / Obsidian 输入。
- 小红书、知乎、公众号等页面归档工具。
- IM 机器人转发来的内容。
- 其他脚本产生的内容。

### 5.2 接口

```http
POST /api/content/analyze
```

### 5.3 请求参数

```json
{
  "url": "https://example.com/article/123",
  "title": "文章标题",
  "source_name": "手动输入",
  "source_category": "Manual",
  "content_type": "article",
  "summary": "原始摘要或简短说明",
  "content_text": "正文、摘要、转录文本或其他可供分析的文本内容",
  "screen": true
}
```

### 5.4 参数说明

| 参数 | 必填 | 说明 |
|---|---:|---|
| `url` | 否 | 原始链接；有链接时用于去重和展示 |
| `title` | 否 | 内容标题 |
| `source_name` | 否 | 来源名称 |
| `source_category` | 否 | 来源分类 |
| `content_type` | 否 | 内容类型，如 article / video / audio / social / note / unknown |
| `summary` | 否 | 外部已有摘要 |
| `content_text` | 否 | 正文、摘要、转录文本或片段 |
| `screen` | 否 | 是否调用 AI 粗筛；默认为 true |

`url`、`title`、`summary`、`content_text` 不要求全部存在，但至少应提供能让系统判断内容的基本信息。

### 5.5 内部流程

```text
接收单条内容
  ↓
整理输入字段
  ↓
去重判断
  ↓
标准化
  ↓
AI 粗筛
  ↓
存入本地数据库
  ↓
返回标准化结果和粗筛结果
```

### 5.6 返回示例

```json
{
  "ok": true,
  "item_id": "item_xxx",
  "is_duplicate": false,
  "normalized": {
    "title": "文章标题",
    "url": "https://example.com/article/123",
    "source_name": "手动输入",
    "source_category": "Manual",
    "content_type": "article"
  },
  "screening": {
    "summary": "一句话说明这条内容在讲什么",
    "category": "AI工具",
    "value_score": 4,
    "personal_relevance": 5,
    "suggested_action": "save",
    "reason": "这条内容与个人信息系统搭建相关，适合后续整理。",
    "tags": ["RSS", "AI工具", "信息管理"],
    "followup_type": "archive"
  }
}
```

---

## 6. 接口三：获取筛选结果

### 6.1 用途

获取已经处理过的内容结果。

这个接口是下游组件的主要读取入口。

适合接入：

- 每日内容推送。
- Web 查看页面。
- Obsidian 导出脚本。
- 视频转录候选任务。
- 人工复核列表。
- 后续内容工作流。

### 6.2 接口

```http
GET /api/inbox
```

### 6.3 查询参数

```http
GET /api/inbox?date=today&min_score=4&suggested_action=read,save&limit=50
```

### 6.4 参数说明

| 参数 | 说明 |
|---|---|
| `date` | 日期过滤；支持 today 或 YYYY-MM-DD |
| `from` | 起始时间 |
| `to` | 结束时间 |
| `source_name` | 按来源名称过滤 |
| `source_category` | 按来源分类过滤 |
| `content_type` | 按内容类型过滤 |
| `category` | 按 AI 粗分类过滤 |
| `min_score` | 最低内容价值分 |
| `min_relevance` | 最低个人相关度 |
| `suggested_action` | 按建议动作过滤，支持多个值 |
| `followup_type` | 按后续处理类型过滤 |
| `tag` | 按标签过滤 |
| `keyword` | 按标题、摘要、理由中的关键词搜索 |
| `include_ignored` | 是否包含建议忽略的内容 |
| `limit` | 返回数量 |
| `offset` | 分页偏移 |

### 6.5 返回示例

```json
{
  "ok": true,
  "filters": {
    "date": "today",
    "min_score": 4,
    "suggested_action": ["read", "save"]
  },
  "stats": {
    "total": 18,
    "read": 9,
    "save": 5,
    "transcribe": 4
  },
  "items": [
    {
      "item_id": "item_xxx",
      "title": "文章标题",
      "url": "https://example.com/article/123",
      "source_name": "示例 RSS 源",
      "source_category": "Articles/AI",
      "content_type": "article",
      "published_at": "2026-05-02T10:00:00",
      "screening": {
        "summary": "一句话摘要",
        "category": "AI工具",
        "value_score": 5,
        "personal_relevance": 4,
        "suggested_action": "read",
        "reason": "推荐理由",
        "tags": ["AI", "RSS"],
        "followup_type": "none"
      }
    }
  ]
}
```

---

## 7. 去重思路

第一版只做最小去重，不做事件聚类和语义去重。

目标是避免同一条内容被重复处理。

### 7.1 去重输入

优先使用：

```text
url
RSS guid
title + source_name
```

### 7.2 去重结果

去重只需要返回：

```text
is_duplicate = true / false
```

如果是重复内容：

- 不重复调用 AI。
- 不重复写入主要内容。
- 可以更新最后见到时间。
- API 返回中说明是重复内容。

### 7.3 暂不处理

第一版不做：

- 不同来源报道同一事件的合并。
- 相似标题合并。
- embedding 聚类。
- 增量信息判断。

---

## 8. 标准化思路

标准化只做最小统一，不追求完整知识卡片。

目标是让 RSS 内容和外部内容进入同一种处理格式。

### 8.1 标准化后的核心信息

```json
{
  "title": "内容标题",
  "url": "原始链接",
  "source_name": "来源名称",
  "source_category": "来源分类",
  "content_type": "article",
  "published_at": "发布时间",
  "summary": "摘要",
  "content_text": "可供 AI 分析的文本"
}
```

### 8.2 标准化原则

- 保留原始链接。
- 保留来源信息。
- 尽量提取标题、摘要、正文片段。
- HTML 内容可以先简单去标签。
- 不强制抓取全文。
- 不下载图片。
- 不做 OCR。
- 不做视频转录。

---

## 9. AI 粗筛思路

AI 粗筛用于判断内容是否值得进一步处理。

它不负责深度研究和长篇总结。

### 9.1 输入给 AI 的信息

```json
{
  "source_name": "来源名称",
  "source_category": "来源分类",
  "title": "标题",
  "url": "链接",
  "content_type": "内容类型",
  "summary": "摘要",
  "content_text": "正文片段"
}
```

### 9.2 AI 输出格式

```json
{
  "summary": "一句话说明这条内容在讲什么",
  "category": "粗分类",
  "value_score": 4,
  "personal_relevance": 5,
  "suggested_action": "read",
  "reason": "推荐或忽略原因",
  "tags": ["标签1", "标签2"],
  "followup_type": "none"
}
```

### 9.3 建议动作

`suggested_action` 只允许：

```text
ignore
skim
read
save
transcribe
review
```

### 9.4 后续处理类型

`followup_type` 只允许：

```text
none
fetch_fulltext
archive
transcribe
manual_review
```

---

## 10. 三个接口的关系

```text
POST /api/rss/analyze
  输入 RSS 源地址
  解析出多条内容
  每条内容进入统一处理流程
  结果进入 inbox

POST /api/content/analyze
  输入单条内容
  单条内容进入统一处理流程
  结果进入 inbox

GET /api/inbox
  查询已经进入 inbox 的筛选结果
  供人阅读或供其他组件调用
```

统一处理流程：

```text
内容输入
  ↓
去重
  ↓
标准化
  ↓
AI 粗筛
  ↓
保存
  ↓
查询输出
```

---

## 11. 第一版明确不做

第一版不做以下内容：

- 不做完整 RSS 源管理后台。
- 不做复杂数据库模型设计。
- 不做网页 UI。
- 不做 IM 推送。
- 不做 Obsidian 写入。
- 不做 Memo 自动增强。
- 不做视频转录调用。
- 不做全文抓取系统。
- 不做图片下载和 OCR。
- 不做 embedding 聚类。
- 不做跨源事件合并。
- 不做复杂任务队列。
- 不做用户反馈学习。

---

## 12. Codex 实现目标

请优先实现这三个接口和它们背后的统一处理流程：

```http
POST /api/rss/analyze
POST /api/content/analyze
GET  /api/inbox
```

实现时保持简单：

- 使用本地数据库保存处理结果。
- 支持 OpenAI 兼容大模型 API。
- 所有配置写入环境变量。
- 保证重复内容不会重复调用 AI。
- 保证接口返回结构稳定。
- 保证后续组件可以通过 `GET /api/inbox` 获取结果。
- 暂时不要加入本文档明确不做的功能。
