# content_inbox 核心功能测评报告

## 1. 执行摘要

- 总体结论：部分可用，适合作为本地 RSS 摄入与 HTTP API 查询底座接管；接管前应明确时区与 CLI JSON 输出边界。
- 最大风险：`/api/inbox?date=today` 使用服务端 UTC 日期边界，和 Asia/Shanghai 用户理解的“今天”存在 8 小时偏差风险。
- 必须修复：如果要给下游 Agent 作为 CLI 工具使用，需要新增纯 JSON stdout 的查询 wrapper，或约定 Agent 直接调用 HTTP API。
- 可后续优化：缺 `<link>` 的 RSS item 会被 feedparser 暴露为 `url=guid`，当前 dedupe 会走 URL 优先路径；缺 URL/guid 的 fallback 使用 `source_name + title`，有误判重复风险。

## 2. 测评范围

- 已测：RSS/Atom fixture 解析、RSS API 摄入、去重、SQLite 持久化、并发摄入、`incremental_mode=until_existing`、`/api/inbox` Agent 查询、批量运行脚本的参数与产物。
- 未测：LLM 分类、标签、动作建议、need/topic 语义质量、embedding 聚类、通知策略质量、真实公网 RSS 稳定性。
- 测试策略：全部使用 `screen=false`、本地 fixture、`tmp_path` SQLite；未读取 `.env`、`content_inbox/data/**`、`content_inbox/outputs/runs/**`。

## 3. 环境信息

- OS：Darwin arm64，kernel 24.1.0。
- Python：3.9.6。
- 数据库：pytest `tmp_path` 下临时 SQLite。
- Docker：未使用。
- LLM key：未配置、未调用。

## 4. 当前能力地图

| 能力 | 当前入口 | 关键代码 | 当前判断 | 风险 |
|---|---|---|---|---|
| RSS/Atom 获取 | `/api/rss/analyze`, `parse_feed` | `app/rss.py` | 可解析标准 RSS/Atom、HTML、Emoji、缺字段、空 feed | 网络异常直接转 400；bad feed 依赖 feedparser bozo 行为 |
| 单条内容摄入 | `/api/content/analyze` | `app/processor.py` | `screen=false` 可不依赖 LLM 完整入库 | `screen=true` 无 key 时会失败状态入库 |
| 去重 | API + SQLite | `build_dedupe_key`, `InboxStore` | URL/guid/title fallback 有回归测试；并发重复安全 | fallback 规则可能误合并同标题周期内容 |
| 增量同步 | `incremental_mode=until_existing` | `app/rss_runner.py` | 新源、锚点、无锚点 fallback 均可用 | `preserve_source_entry_order=true` 实际会按日期旧到新排序，命名易误导 |
| Inbox 查询 | `/api/inbox` | `app/server.py`, `app/storage.py` | JSON 结构稳定，支持 date/from/to/keyword/source/type/limit/offset | 日期基于 `created_at` UTC，不是 `published_at` 或用户本地日期 |
| 批量运行 | `scripts/run_rss_sources_to_content_inbox.py` | 外部脚本 | 适合批量摄入、报告和机器可读 artifact | stdout 混有日志，不能作为纯 JSON 查询 CLI |

## 5. 测试结果总览

| 测试域 | 用例数 | 通过 | 失败 | 主要问题 |
|---|---:|---:|---:|---|
| 新增 focused suite | 42 | 42 | 0 | 暴露并记录 missing-link/guid、UTC today、stdout 非 JSON 等边界 |
| 既有基线 suite | 43 | 43 | 0 | 无新增回归 |
| 全量 pytest | 152 | 142 | 0 | 10 个 integration 测试按既有规则跳过 |

## 6. 详细发现

### 6.1 RSS 获取与解析

- 标准 RSS 2.0、Atom、HTML summary/content、Emoji/Unicode、缺 guid、缺 link/guid、bad date、empty feed、limit 均已被 fixture 覆盖。
- HTML 清洗不是 `parse_feed` 阶段完成，而是在 `normalize_content` 中完成；当前行为可接受，但报告给下游调用者时应说明 parse 层返回原始 HTML 字符串。
- `rss_malformed.xml` 这种完全非 XML 响应会通过 `/api/rss/analyze` 返回 HTTP 400 和 `failed to parse feed` detail。
- 缺 `<link>` 但有 `<guid>` 时，feedparser 当前会让 `entry.get("link")` 等于 guid；因此内部 `url` 与 `guid` 都是同一个 guid 字符串。

### 6.2 去重

- 当前去重优先级已验证：normalized URL 优先，其次 `source_name + guid`，最后 `source_name + lower(title)`。
- URL 规范化会移除 fragment、trailing slash、常见 tracking 参数，并排序 query；不会合并 `http` 和 `https`。
- 重复摄入只 `mark_seen`：`seen_count` 增加，`last_seen_at`/`updated_at` 更新，`created_at` 和原始 title/summary/content 不被覆盖。
- 同 feed 内重复 URL、并发 20 次单条摄入、并发 10 次 RSS 摄入均不会产生重复 DB 行。

### 6.3 增量同步

- `fixed_limit` 只处理指定前 N 条。
- 新源 `until_existing` 返回 `new_source_initial_baseline`，只处理 `new_source_initial_limit`。
- 老源找到锚点时返回 `until_existing_anchor_found`，只处理锚点之前的新条目。
- 老源找不到锚点时返回 `old_source_no_anchor`，只处理 `old_source_no_anchor_limit` 并返回 warning。
- 当前 `preserve_source_entry_order=true` 不是保持 feed 原始顺序，而是将 dated entries 按 `published_at` 从旧到新排序、undated 放最后。

### 6.4 CLI/agent 查询

- `/api/inbox` 响应稳定为 `ok`、`filters`、`stats`、`items`，适合 Agent 直接解析。
- `date=today` 当前调用 `date.today()` 后构造 UTC `00:00:00` 到 `23:59:59.999999`，数据库 `created_at` 也是 UTC；Asia/Shanghai 用户在 00:00-07:59 查询“今天”时可能漏掉本地今天凌晨内容。
- 推荐短期 Agent 调用方式：显式传 UTC `from/to`；中期新增 `tz` 参数或 CLI wrapper 做本地时区转换。

示例：

```bash
curl -s 'http://127.0.0.1:8787/api/inbox?from=2026-05-15T16:00:00+00:00&to=2026-05-16T15:59:59+00:00&include_silent=true&include_ignored=true&limit=20'
```

### 6.5 批量运行器

- `/api/rss/analyze-batch` 单源失败不会阻塞其他源，source result 保持输入顺序。
- 批量 API 的 `incremental_mode`、`probe_limit`、`new_source_initial_limit`、`old_source_no_anchor_limit` 已验证能下传。
- 外部脚本 dry-run 会生成 `selected_sources.csv`、`report.md`、`run_state.json` 等机器可读 artifact。
- 外部脚本 stdout 以 `[INFO]`、`[SUMMARY]` 等日志为主，不能作为纯 JSON stdout 的 Agent 查询 CLI。

## 7. 关键缺陷列表

| ID | 严重性 | 问题 | 复现步骤 | 建议修复 |
|---|---|---|---|---|
| P0-1 | P0 | 缺少纯 JSON 查询 CLI，批量脚本 stdout 混杂日志 | 运行 `run_rss_sources_to_content_inbox.py --dry-run` 并尝试 `json.loads(stdout)` | 新增 `python -m app.cli inbox --json`，日志写 stderr，stdout 只写 JSON |
| P1-1 | P1 | `date=today` 是 UTC today，不是用户本地 today | 调用 `resolve_date_filters("today", None, None)` | API 增加 `tz` 参数，或 CLI 将本地日期转换为 UTC `from/to` |
| P1-2 | P1 | `preserve_source_entry_order=true` 命名与行为不一致 | 用 order-change fixture 调批量 API | 重命名参数或增加明确 `process_oldest_first` 参数 |
| P2-1 | P2 | 缺 link 有 guid 时 guid 会进入 URL 优先 dedupe 路径 | 解析 `rss_missing_link.xml` | parse 层区分真实 link 与 feedparser fallback，或报告中明确约束 |
| P2-2 | P2 | `source_name + title` fallback 可能误合并周期性同标题内容 | 无 URL/guid、同 source、同 title 连续提交 | fallback 可考虑加入 normalized date 或内容 hash |

## 8. 建议补充测试

- 本轮新增 15 个 fixture 和 7 个 focused 测试文件。
- 后续可补真实 HTTP timeout/502 的本地 server 测试，以及 RSSHub 包装链接规范化测试。
- 若实现 CLI wrapper，应新增 `test_app_cli.py` 覆盖 stdout/stderr、exit code、`--today` 本地时区转换。

## 9. 建议后续路线图

- P0：实现 Agent 查询 CLI wrapper，保证 stdout 纯 JSON、stderr 放日志、失败非 0。
- P1：修正或扩展日期查询时区语义；明确 `date` 查询基于 `created_at` 而非 `published_at`。
- P1：澄清 `preserve_source_entry_order` 语义，避免调用者误以为返回 feed 原始顺序。
- P2：增强 dedupe fallback，引入内容 hash 或日期窗口，降低同标题误合并。
- P2：增加本地 HTTP server fixture，覆盖 timeout、502、非 XML content-type。

## 10. 附录

关键命令：

```bash
cd content_inbox
PYTHONPATH=. pytest -q tests/test_api.py tests/test_processor.py tests/test_run_rss_sources_script.py
PYTHONPATH=. pytest -q tests/test_rss_parse_fixtures.py tests/test_rss_api_ingestion.py tests/test_dedupe_rules.py tests/test_dedupe_concurrency.py tests/test_incremental_until_existing.py tests/test_inbox_query_agent_use_cases.py tests/test_rss_runner_cli_or_script.py
PYTHONPATH=. pytest -q
```

执行结果：

```text
43 passed in 1.15s
42 passed in 0.59s
142 passed, 10 skipped in 1.61s
```

新增 fixture：

```text
atom_basic.xml
rss_bad_date.xml
rss_basic.xml
rss_duplicate_items.xml
rss_empty.xml
rss_html_summary.xml
rss_incremental_v1.xml
rss_incremental_v2.xml
rss_malformed.xml
rss_many_items.xml
rss_missing_guid.xml
rss_missing_link.xml
rss_missing_link_guid.xml
rss_order_change_v1.xml
rss_order_change_v2.xml
```
