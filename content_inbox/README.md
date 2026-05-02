# content-inbox

本地内容处理模块，实现三个核心 API：RSS 分析、单条内容分析、筛选结果查询。

## 安装

```bash
cd "/Users/wangrundong/work/infomation-center/content_inbox"
python3 -m pip install -r requirements.txt
```

## 启动

```bash
cd "/Users/wangrundong/work/infomation-center/content_inbox"
PYTHONPATH=. python3 -m app.server
```

默认服务地址：

```text
http://127.0.0.1:8787
```

## Docker 启动

项目提供了 `Dockerfile` 和 `docker-compose.yml`。Compose 会读取本目录的 `.env`，并把数据库保存到宿主机的 `./data/content_inbox.sqlite3`。

```bash
cd "/Users/wangrundong/work/infomation-center/content_inbox"
docker compose up -d --build
```

查看状态：

```bash
docker compose ps
curl -s http://127.0.0.1:8787/health
```

停止服务：

```bash
docker compose down
```

`docker-compose.yml` 已配置 `restart: unless-stopped`。只要 Docker Desktop / Docker daemon 随系统启动，容器会在开机后自动恢复运行。在 macOS 上还需要在 Docker Desktop 设置里开启登录时启动 Docker Desktop。

## API 示例

分析单条内容：

```bash
curl -s http://127.0.0.1:8787/api/content/analyze \
  -H 'content-type: application/json' \
  -d '{
    "url":"https://example.com/article/123",
    "title":"文章标题",
    "source_name":"手动输入",
    "source_category":"Manual",
    "summary":"原始摘要",
    "content_text":"正文片段",
    "screen":true
  }'
```

分析 RSS：

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze \
  -H 'content-type: application/json' \
  -d '{"feed_url":"https://example.com/feed.xml","limit":5,"screen":true}'
```

查询 inbox：

```bash
curl -s 'http://127.0.0.1:8787/api/inbox?min_score=3&suggested_action=read,save&limit=20'
```

## DeepSeek 配置

默认使用 DeepSeek 的 OpenAI-compatible Chat Completions API。`screen=true` 必须配置 API key；没有 key 时接口会返回错误，不做本地粗筛。

```bash
export CONTENT_INBOX_DEEPSEEK_API_KEY="..."
export CONTENT_INBOX_DEEPSEEK_BASE_URL="https://api.deepseek.com"
export CONTENT_INBOX_DEEPSEEK_MODEL="deepseek-v4-flash"
```

## 测试

```bash
cd "/Users/wangrundong/work/infomation-center/content_inbox"
PYTHONPATH=. pytest -q
```

详细实现设计见 [docs/implementation_design.md](/Users/wangrundong/work/infomation-center/content_inbox/docs/implementation_design.md)。
