# RSS 第一轮基线同步测试报告

日期：2026-05-05

---

## 1. 当前真实数据库路径

- **容器内路径**: `/data/content_inbox.sqlite3`（源自 `/health` 返回）
- **宿主机路径**: `content_inbox/data/content_inbox.sqlite3`（Docker volume 映射 `./data:/data`）
- **文件大小**: 约 20MB（宿主机）
- **当前状态**: `inbox_items: 539 rows`, `event_clusters: 143 rows`, `distinct sources: 96`
- **CONTENT_INBOX_DB 设置**: `.env` 中设置了 Mac 绝对路径，已在 `docker-compose.yml` 中硬编码为 `/data/content_inbox.sqlite3` 以确保 Docker 内路径正确

## 2. 备份情况

- **已备份**: 是
- **备份路径**: `/data/backups/content_inbox.sqlite3.before_first_baseline_20260504_161830`（容器内，即宿主机 `content_inbox/data/backups/`）
- **备份时间**: 2026-05-04 16:18:30

## 3. /health 检查结果

```json
{
    "ok": true,
    "database_path": "/data/content_inbox.sqlite3",
    "ai_configured": true,
    "embedding_configured": true,
    "sqlite_vec_available": true,
    "config": {
        "llm_model": "deepseek-v4-flash",
        "embedding_model": "text-embedding-3-small",
        "prompt_version": "reading_needs_v1",
        "llm_max_concurrency": 2,
        "screening_mode": "merged"
    }
}
```

运行时配置已设置：
- LLM 并发: 2
- 筛选模式: merged

## 4. RSSHub 可用性检查

- RSSHub 容器运行正常，返回 200
- 随机测试 3 个 local_xml_url 源，全部返回 200 + 有效 XML
- 测试源:
  1. 小宇宙 Podcast → Status 200, 188KB
  2. 奥德修斯的绳索 (B站) → Status 200, 30KB
  3. CoCoVii (B站) → Status 200, 31KB
- OPML 重新导出: 501 个源，已更新

## 5. Dry-run 结果

- **Run 目录**: `rss_run_20260505_101814`
- **选中源数**: 482（全部启用源）
- **URL 模式**: docker-host
- **local_xml_url 源**: 正确使用 `host.docker.internal:1200` / `host.docker.internal:8003`
- **xml_url 源**: 正确回退使用远程 URL
- **结论**: URL 解析正常，无空 URL 或错误 URL

## 6. 10 源真实测试结果

**Run 目录**: `rss_run_20260505_105446`

**注意**: 首次 rebuild 后 .env 中的 CONTENT_INBOX_DB 导致容器使用了错误的数据库路径，创建了空库。已修复 docker-compose.yml，重新 build 后数据库路径正确。

| 指标 | 数值 |
|------|------|
| 成功源数 | 10 |
| 失败源数 | 0 |
| new_items | 0 |
| duplicate_items | 0 |
| until_existing_anchor_found | 10/10 |
| new_source_initial_baseline | 0 |
| old_source_no_anchor | 0 |

**分析**: 这 10 个源在第一轮（旧代码 fixed_limit 模式）已经处理过，数据库中已有这些源的最新条目。until_existing 模式正确地识别了每个源的第一条就是已存在的锚点，跳过了所有条目。

## 7. 30 源真实测试结果

**Run 目录**: `rss_run_20260505_105547`

| 指标 | 数值 |
|------|------|
| 成功源数 | 29 |
| 失败源数 | 1 |
| new_items | 40 |
| recommended_items | 3 |
| until_existing_anchor_found | 25 |
| new_source_initial_baseline | 0 |
| old_source_no_anchor | 2 |
| failed | 1 |

**old_source_no_anchor 源**:
1. 51吃瓜网 - 该源有历史但 feed 返回了10条新内容（动态feed，去重键不匹配）
2. 新华社新闻_新华网 - 该源有历史但 feed 返回了20条新内容

**until_existing_anchor_found 找到非零锚点的源**:
- Vista看天下: anchor_index=4, 处理4条新条目
- simonwillison.net: anchor_index=6, 处理6条新条目

**失败源**:
- 飞鸟手札: network_error（RSSHub B站路由暂时不可达，非代码问题）

## 8. 50 源真实测试结果

**Run 目录**: `rss_run_20260505_110727`

| 指标 | 数值 |
|------|------|
| 成功源数 | 49 |
| 失败源数 | 1 |
| new_items | 1 |
| recommended_items | 1 |
| until_existing_anchor_found | 49 |
| new_source_initial_baseline | 0 |
| old_source_no_anchor | 0 |
| failed | 1 |

**测试了并发**: concurrency=2, llm-max-concurrency=2，无锁竞争问题。

**失败源**: 刘夙的科技世界 - feed_parse_error（源 feed 格式不合法，非代码问题）

## 9. 是否建议进入全源基线同步

**建议**: ✅ 是

理由：
- until_existing 模式在小批量测试中表现正确
- 三种决策路径均验证通过：
  - `until_existing_anchor_found`: 正常工作（包括 anchor_index=0 和非零锚点）
  - `new_source_initial_baseline`: API 直接调用验证通过（source_has_history=False → 处理5条）
  - `old_source_no_anchor`: 在30源测试中触发，正确限制为20条并返回 warning
- 并发安全性验证通过（concurrency=2）
- 失败率低（2/50 = 4%，均为外部源问题，非代码bug）
- 数据库备份已完成

## 10. 推荐全源命令

```bash
python3 -u /Users/wangrundong/work/infomation-center/content_inbox/scripts/run_rss_sources_to_content_inbox.py \
  --api-base http://127.0.0.1:8787 \
  --csv /Users/wangrundong/work/infomation-center/rsshub/rss_opml/rss_sources.csv \
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

**语义说明**:
- 不是每个源的历史全量归档
- 是所有启用源的第一轮基线同步
- 新源（数据库从未出现过）最多只取前 5 条
- 老源会向后扫描直到遇到已有条目，只处理新条目
- 老源前 20 条没遇到已有条目 → `old_source_no_anchor`，最多处理 20 条并记录 warning
- 日常每日同步可继续使用同一套 until_existing 模式

## 11. 风险提示

1. **source_name/source_category 判断源历史不够稳定**: 目前用 source_name + source_category 判断源历史。feed_url 不存储在表中，所以不同 feed_url 但相同 name+category 的源会共享历史记录。这可能导致误判 new_source/old_source。未来可考虑在 inbox_items 中增加 feed_url 列或 source_identity 字段。

2. **old_source_no_anchor 过多说明 dedupe 或 source identity 可能漂移**: 如果大量源触发 old_source_no_anchor，可能是 guid/URL 变化、RSSHub 路由变化、或去重规则变化导致。需要检查这些源的 warning 列表。

3. **RSSHub 503/timeout 时不要提高并发**: 部分 B站/小宇宙 路由可能不稳定。遇到 RSSHub 错误时应降低并发，而非提高。

4. **LLM/embedding 失败时不要直接重跑全量**: 先检查 failed_sources.csv，排查失败原因，修复后再单独重试失败源。

5. **数据库路径问题已修复**: docker-compose.yml 中 CONTENT_INBOX_DB 已硬编码为 `/data/content_inbox.sqlite3`，不再受 .env 影响。但未来如需修改 .env，需注意 Docker 和本地路径的区别。
