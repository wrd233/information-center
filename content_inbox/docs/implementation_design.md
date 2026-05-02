# content-inbox 实现设计

## 目标

本项目实现核心设计文档中的三个 API：

- `POST /api/rss/analyze`
- `POST /api/content/analyze`
- `GET /api/inbox`

第一版只做本地内容入口、最小去重、标准化、模型粗筛和 SQLite 查询，不加入阅读器 UI、推送、归档、全文抓取、任务队列或跨源聚类。

## 模块划分

```text
app/server.py     FastAPI 路由和请求参数解析
app/rss.py        RSS/Atom 拉取与 item 提取
app/processor.py  统一处理流程：标准化、去重、粗筛、保存
app/screener.py   DeepSeek/OpenAI-compatible 粗筛客户端
app/storage.py    SQLite schema、写入、去重更新、查询过滤
app/models.py     Pydantic 请求、标准化内容、筛选结果模型
```

## 数据流

```text
RSS URL 或单条内容
  -> ContentAnalyzeRequest
  -> normalize_content
  -> build_dedupe_key
  -> SQLite 查重
  -> screen_content，screen=true 时调用 DeepSeek/OpenAI-compatible API
  -> SQLite 保存
  -> API 返回 / inbox 查询
```

RSS 和单条内容共享同一个 `process_content`，区别只在 RSS 会先把 feed entries 转为 `ContentAnalyzeRequest`。

## 去重策略

去重键按优先级生成：

1. 规范化 URL：去 fragment、统一 scheme/host 小写、去掉路径末尾 `/`。
2. `source_name + guid`。
3. `source_name + title`。

命中重复时只更新 `last_seen_at` 和 `seen_count`，直接返回已有筛选结果，不再次调用 AI，也不重复插入主内容。

## SQLite 表

主表是 `inbox_items`，保留标准化字段、筛选 JSON、原始 JSON、创建/更新时间和重复出现次数。第一版没有拆分多表，目的是保持查询和迁移成本低。

关键字段：

- `item_id`
- `dedupe_key`
- `url`
- `guid`
- `title`
- `source_name`
- `source_category`
- `content_type`
- `published_at`
- `summary`
- `content_text`
- `screening_json`
- `created_at`
- `last_seen_at`
- `seen_count`

## 粗筛策略

当 `screen=false` 时，保存内容并返回 `screening_method=none`、`suggested_action=review`。它只表示本次明确跳过模型筛选。

当 `screen=true` 时必须配置模型 API key。默认按 DeepSeek 官方 OpenAI-compatible 方式调用 `/chat/completions`：

```text
base_url=https://api.deepseek.com
model=deepseek-v4-flash
```

没有 API key、AI 被禁用或模型调用失败时，接口返回错误，不做本地粗筛，也不伪造筛选结果。

## 环境变量

```text
CONTENT_INBOX_HOST
CONTENT_INBOX_PORT
CONTENT_INBOX_DB
CONTENT_INBOX_REQUEST_TIMEOUT
CONTENT_INBOX_MAX_CONTENT_CHARS
CONTENT_INBOX_AI_ENABLED
CONTENT_INBOX_DEEPSEEK_API_KEY
CONTENT_INBOX_DEEPSEEK_BASE_URL
CONTENT_INBOX_DEEPSEEK_MODEL
CONTENT_INBOX_OPENAI_TIMEOUT
```

兼容别名仍保留为配置入口，便于接其他 OpenAI-compatible 服务：

```text
CONTENT_INBOX_OPENAI_API_KEY
CONTENT_INBOX_OPENAI_BASE_URL
CONTENT_INBOX_OPENAI_MODEL
```

## Docker 部署

第一版使用单容器部署：

- `Dockerfile` 基于 `python:3.11-slim` 安装 Python 依赖并运行 `python -m app.server`。
- `docker-compose.yml` 从 `.env` 注入 DeepSeek 配置。
- 容器内数据库路径固定为 `/data/content_inbox.sqlite3`。
- 宿主机 `./data` 挂载到容器 `/data`，便于保留 SQLite 数据。
- `restart: unless-stopped` 让容器在 Docker daemon 启动后自动恢复。

启动命令：

```bash
cd "/Users/wangrundong/work/infomation-center/content_inbox"
docker compose up -d --build
```

macOS 上 Docker Desktop 本身需要开启“登录时启动”，否则容器的 restart policy 要等 Docker Desktop 被启动后才会生效。

## RSS 测试源

可以从 `/Users/wangrundong/work/infomation-center/rsshub/rss_opml/rss_sources.csv` 选取启用且有 `local_xml_url` 或 `xml_url` 的行测试：

```bash
python - <<'PY'
import csv
from pathlib import Path

path = Path('/Users/wangrundong/work/infomation-center/rsshub/rss_opml/rss_sources.csv')
with path.open(encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        url = row.get('local_xml_url') or row.get('xml_url')
        if row.get('enabled') == 'Y' and row.get('status') == 'active' and url:
            print(row['title'], url)
            break
PY
```

再调用：

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze \
  -H 'content-type: application/json' \
  -d '{"feed_url":"<URL>","limit":5,"screen":true}'
```
