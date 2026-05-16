# content-inbox

本地内容摄入与检索内核，负责 RSS/Atom 摄入、去重、source registry、run history、inbox 查询和 Agent CLI。`screen=false` 路径完全 deterministic，不需要 LLM 或 embedding key；`screen=true` 才会进入模型筛选路径。

## 安装

```bash
cd content_inbox
python3 -m pip install -r requirements.txt
```

## 启动

```bash
cd content_inbox
PYTHONPATH=. python3 -m app.server
```

默认服务地址：

```text
http://127.0.0.1:8787
```

## Docker 启动

项目提供了 `Dockerfile` 和 `docker-compose.yml`。Compose 会读取本目录的 `.env`，并把数据库保存到宿主机的 `./data/content_inbox.sqlite3`。

```bash
cd content_inbox
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

分析 RSS。测试和 CI 建议使用 `screen=false`，避免依赖 LLM：

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze \
  -H 'content-type: application/json' \
  -d '{"feed_url":"https://example.com/feed.xml","limit":5,"screen":false}'
```

批量分析 RSS：

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze-batch \
  -H 'content-type: application/json' \
  -d '{
    "sources":[
      {"source_id":"s1","feed_url":"https://example.com/feed1.xml","source_name":"source 1"},
      {"source_id":"s2","feed_url":"https://example.com/feed2.xml","source_name":"source 2"}
    ],
    "limit_per_source":5,
    "screen":true,
    "max_concurrent_sources":3
  }'
```

说明：

- 并发粒度是 RSS 源，不是条目。
- 同一个 RSS 源内部条目仍然顺序处理。
- `max_concurrent_sources` 默认是 `3`。
- 建议本地测试先从 `2` 或 `3` 开始。

查询 inbox：

```bash
curl -s 'http://127.0.0.1:8787/api/inbox?min_score=3&suggested_action=read,save&limit=20'
```

## RSS 源注册与状态

`rss_sources` 是 RSS 源事实来源。CSV/OPML 只是导入来源；后续调度中心应读取 registry，而不是直接读 CSV。注册后可查看源状态、按 `source_id` 摄入，并在摄入成功或失败后更新 health 与 run history。

注册源：

```bash
curl -s http://127.0.0.1:8787/api/rss/sources \
  -H 'content-type: application/json' \
  -d '{
    "source_id":"rsshub-36kr",
    "source_name":"36氪",
    "source_category":"科技/商业",
    "feed_url":"http://rsshub:1200/36kr/news/latest",
    "status":"active",
    "priority":2,
    "tags":["tech","business"],
    "config":{"incremental_mode":"until_existing","screen":false}
  }'
```

列出和查看源：

```bash
curl -s 'http://127.0.0.1:8787/api/rss/sources?status=active&limit=100'
curl -s http://127.0.0.1:8787/api/rss/sources/rsshub-36kr
```

更新或停用源：

```bash
curl -s -X PATCH http://127.0.0.1:8787/api/rss/sources/rsshub-36kr \
  -H 'content-type: application/json' \
  -d '{"status":"paused","priority":4}'

curl -s -X DELETE http://127.0.0.1:8787/api/rss/sources/rsshub-36kr
```

`status` 含义：

| status | 说明 |
|---|---|
| `active` | 正常源。 |
| `paused` | 临时暂停；手动 ingest 需要 `force=true`。 |
| `disabled` | 软停用，默认拒绝按源摄入。 |
| `broken` | 连续失败或待人工检查；`test=true` 或 `force=true` 可手动验证。 |

按注册源摄入：

```bash
curl -s http://127.0.0.1:8787/api/rss/sources/rsshub-36kr/ingest \
  -H 'content-type: application/json' \
  -d '{"screen":false,"incremental_mode":"until_existing","probe_limit":20,"process_order":"oldest_first"}'
```

查看 run history：

```bash
curl -s 'http://127.0.0.1:8787/api/rss/runs?limit=20'
curl -s http://127.0.0.1:8787/api/rss/runs/<run_id>
curl -s http://127.0.0.1:8787/api/rss/runs/<run_id>/sources
```

结构化错误示例：

```json
{
  "ok": false,
  "error": {
    "error_code": "rss_parse_error",
    "message": "failed to parse feed",
    "retryable": false,
    "source_id": "rsshub-36kr",
    "feed_url": "http://rsshub:1200/36kr/news/latest"
  }
}
```

## Agent CLI

正式 Agent 查询入口是 `python -m app.cli`。JSON 模式下 stdout 只输出 JSON，日志和人类可读错误写 stderr。

```bash
PYTHONPATH=. python -m app.cli inbox --json --limit 20
PYTHONPATH=. python -m app.cli inbox --json --today --tz Asia/Shanghai --limit 20
PYTHONPATH=. python -m app.cli sources list --json
PYTHONPATH=. python -m app.cli sources get rsshub-36kr --json
PYTHONPATH=. python -m app.cli sources register --source-id rsshub-36kr --name 36氪 --feed-url http://rsshub:1200/36kr/news/latest --json
PYTHONPATH=. python -m app.cli sources update rsshub-36kr --status paused --json
PYTHONPATH=. python -m app.cli sources ingest rsshub-36kr --json --screen false
PYTHONPATH=. python -m app.cli sources import-csv --csv ../rsshub/rss_opml/rss_sources.csv --dry-run --json
PYTHONPATH=. python -m app.cli sources backfill-items --dry-run --json
PYTHONPATH=. python -m app.cli runs list --json
```

`scripts/run_rss_sources_to_content_inbox.py` 仍是批量 runner、报告和调试工具，不是正式 Agent 查询 CLI；不要解析它的 stdout 作为稳定 JSON。新批量摄入可使用 registry mode：

```bash
PYTHONPATH=. python scripts/run_rss_sources_to_content_inbox.py \
  --source-mode registry \
  --count 20 \
  --no-screen \
  --incremental-mode until_existing
```

## RSS 增量同步模式

从 v0.2.0 开始，`/api/rss/analyze` 支持两种同步模式：

### fixed_limit（默认，当前行为）

每个 RSS 源按 `limit` 固定处理前 N 条。适合首次小批量测试、手动抽样、debug。

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze \
  -H 'content-type: application/json' \
  -d '{"feed_url":"https://example.com/feed.xml","limit":20,"screen":true}'
```

### until_existing（增量同步）

从最新条目向后扫描，遇到数据库中已存在的条目时停止，只处理该条目之前的新条目。适合每日定时同步。

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze \
  -H 'content-type: application/json' \
  -d '{
    "feed_url":"https://example.com/feed.xml",
    "incremental_mode":"until_existing",
    "probe_limit":20,
    "new_source_initial_limit":5,
    "old_source_no_anchor_limit":20,
    "screen":true
  }'
```

**决策逻辑：**

| 条件 | 决策 | 处理条目 |
|---|---|---|
| 在 probe_limit 内找到已存在条目 | `until_existing_anchor_found` | 锚点之前的新条目 |
| 数据库中无源历史记录（新源） | `new_source_initial_baseline` | 前 N 条（`new_source_initial_limit`，默认 5）|
| 数据库有历史但 probe_limit 内未找到锚点 | `old_source_no_anchor` | 前 N 条（`old_source_no_anchor_limit`，默认 20），返回 warning |

**新增请求字段：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `incremental_mode` | `"fixed_limit" \| "until_existing"` | `"fixed_limit"` | 同步模式 |
| `probe_limit` | `int` | `20` | 扫描锚点的最大条目数 |
| `new_source_initial_limit` | `int` | `5` | 新源基线处理条数 |
| `old_source_no_anchor_limit` | `int` | `20` | 老源无锚点时处理条数 |
| `stop_on_first_existing` | `bool` | `true` | 遇到第一条已存在条目即停止 |

**until_existing 模式新增响应字段：**

`incremental_mode`、`incremental_decision`、`source_has_history`、`probe_limit`、`new_source_initial_limit`、`old_source_no_anchor_limit`、`feed_items_seen`、`anchor_found`、`anchor_index`、`selected_items_for_processing`、`warnings`。

### 批量 API 和外部运行器

批量端点（`/api/rss/analyze-batch`）的 `RSSBatchAnalyzeRequest` 和 `RSSSourceSpec` 也支持增量字段。

外部运行器脚本新增 CLI 参数：

```bash
python3 -u content_inbox/scripts/run_rss_sources_to_content_inbox.py \
  --api-base http://127.0.0.1:8787 \
  --csv rsshub/rss_opml/rss_sources.csv \
  --all \
  --url-mode docker-host \
  --incremental-mode until_existing \
  --probe-limit 20 \
  --new-source-initial-limit 5 \
  --old-source-no-anchor-limit 20 \
  --concurrency 2 \
  --llm-max-concurrency 2 \
  --screening-mode merged \
  --timeout 600 \
  --profile
```

## 性能 Profiling

通过 `CONTENT_INBOX_PROFILE=1` 环境变量或 `--profile` 脚本标志启用逐源耗时记录。启用后 `source_results.csv` 会额外记录每个源各阶段的墙钟时间。

**开启方式：**

```bash
# 方式1: 服务端环境变量（所有请求自动记录）
CONTENT_INBOX_PROFILE=1 PYTHONPATH=. python3 -m app.server

# 方式2: 脚本 --profile 标志（通过 API payload 传递）
python3 scripts/run_rss_sources_to_content_inbox.py --all --profile ...
```

**记录的字段（`source_results.csv` 新增列）：**

| 字段 | 说明 |
|------|------|
| `fetch_feed_seconds` | RSS/Atom 源抓取耗时 |
| `llm_basic_screening_seconds` | 粗筛 LLM 调用耗时（basic_screening） |
| `llm_need_matching_seconds` | 需求匹配 LLM 调用耗时（need_matching） |
| `embedding_seconds` | 文本向量化 API 调用耗时 |
| `lock_wait_seconds` | 等待全局内容处理锁的时间（串行化程度指标） |
| `lock_held_seconds` | 持有全局锁的时间（锁内实际处理耗时） |
| `source_total_seconds` | 单个 RSS 源从抓取到完成的总墙钟时间 |

**API 单次调用也可开启（profile 字段）：**

```bash
curl -s http://127.0.0.1:8787/api/rss/analyze \
  -H 'content-type: application/json' \
  -d '{"feed_url":"https://example.com/feed.xml","limit":5,"screen":true,"profile":true}'
```

响应中会额外包含 `"profile": {...}` 字典。

## DeepSeek 配置

默认使用 DeepSeek 的 OpenAI-compatible Chat Completions API。`screen=true` 必须配置 API key；没有 key 时接口会返回错误，不做本地粗筛。

```bash
export CONTENT_INBOX_DEEPSEEK_API_KEY="..."
export CONTENT_INBOX_DEEPSEEK_BASE_URL="https://api.deepseek.com"
export CONTENT_INBOX_DEEPSEEK_MODEL="deepseek-v4-flash"
```

Embedding 使用独立的 OpenAI-compatible 中转站配置：

```bash
export CONTENT_INBOX_EMBEDDING_API_KEY="..."
export CONTENT_INBOX_EMBEDDING_BASE_URL="https://yunwu.apifox.cn/v1"
export CONTENT_INBOX_EMBEDDING_MODEL="text-embedding-3-small"
```

可调参数集中在 [config/content_inbox.yaml](/Users/wangrundong/work/infomation-center/content_inbox/config/content_inbox.yaml)。

## LLM-aware Semantic Pipeline

RSS ingest 仍然先写入事实层，semantic pipeline 作为后处理运行，不阻塞原始入库。

常用命令：

```bash
PYTHONPATH=. python -m content_inbox.semantic cards --limit 100
PYTHONPATH=. python -m content_inbox.semantic dedupe --limit 100
PYTHONPATH=. python -m content_inbox.semantic cluster --limit 100
PYTHONPATH=. python -m content_inbox.semantic source-profiles recompute
PYTHONPATH=. python -m content_inbox.semantic review list
```

查看 cluster/source/review：

```bash
PYTHONPATH=. python -m content_inbox.semantic clusters list --status active
PYTHONPATH=. python -m content_inbox.semantic clusters show CLUSTER_ID
PYTHONPATH=. python -m content_inbox.semantic source profile SOURCE_ID
PYTHONPATH=. python -m content_inbox.semantic source suggestions
PYTHONPATH=. python -m content_inbox.semantic source set-priority SOURCE_ID high
PYTHONPATH=. python -m content_inbox.semantic review approve REVIEW_ID
```

Live DeepSeek semantic calls are disabled by default. Enable them explicitly:

```bash
export CONTENT_INBOX_LLM_ENABLE_LIVE=1
export CONTENT_INBOX_LLM_SMALL_MODEL=deepseek-v4-flash
export CONTENT_INBOX_LLM_STRONG_MODEL=deepseek-v4-pro
```

Live smoke test uses a temporary SQLite DB unless both `--db-path` and `--write-real-db` are provided:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python -m content_inbox.semantic live-smoke all --limit 3 --max-calls 10
```

真实数据语义质量评估：

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --db-path content_inbox/data/content_inbox.sqlite3 \
  --limit 500 \
  --max-calls 100 \
  --max-candidates 5 \
  --concurrency 4 \
  --live \
  --dry-run \
  --output content_inbox/outputs/semantic_eval
```

`evaluate` 默认读取真实 DB 后写入临时评估 DB，并输出 `semantic_quality_report.md` 与 `semantic_quality_summary.json`。只有同时传入 `--db-path` 和 `--write-real-db` 才会写真实 DB。

`evaluate` 默认额度比 smoke test 更宽：`--max-calls 100`、`--token-budget 200000`、`--concurrency 4`。`--concurrency` 会并发 item-card batch 和 item-item relation 的 DeepSeek 调用；cluster 写入路径保持较保守，避免并发误聚类。

Semantic LLM calls write audit rows to `llm_call_logs`, including model, prompt/schema version, input fingerprint, latency, status, token usage, cache token fields when returned by the provider, raw output, parsed JSON, and error details. API keys are never logged.

This phase did not change console UI. Future console work can consume the backend-only `/api/semantic/*` endpoints for item semantic detail, relations, clusters, source profiles, review queue, and LLM call log summaries.

## 测试

```bash
cd "/Users/wangrundong/work/infomation-center/content_inbox"
PYTHONPATH=. pytest -q
```

Live DeepSeek tests are explicit and skip without live config:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. pytest -q -m live_deepseek
```

详细实现设计见 [docs/implementation_design.md](/Users/wangrundong/work/infomation-center/content_inbox/docs/implementation_design.md)。
