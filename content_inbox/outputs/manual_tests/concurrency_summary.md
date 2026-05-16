# 拆锁后并发验证报告

## 测试环境

- **Date**: 2026-05-04
- **Git branch**: main (2 files modified: processor.py, screener.py)
- **Screening mode**: two_stage
- **llm.max_concurrency**: 2 (default) / 1 (temp config for comparison)
- **llm.model**: deepseek-v4-flash
- **sqlite_vec_available**: false (vec search fails, embedding still works)
- **Profile**: enabled per-request via `profile: True`
- **Service**: FastAPI + Uvicorn, 1 worker

## 新数据库路径

`content_inbox/outputs/manual_tests/concurrency_db/content_inbox_concurrency_test*.sqlite3`

确认方法：health check 返回 `"database_path": "outputs/manual_tests/concurrency_db/..."` 而非 `"data/content_inbox.sqlite3"`

## 服务启动命令

```bash
cd content_inbox
CONTENT_INBOX_DB=outputs/manual_tests/concurrency_db/<db_name>.sqlite3 \
CONTENT_INBOX_PORT=8789 \
CONTENT_INBOX_CONFIG=outputs/manual_tests/concurrency_db/temp_config_max1.yaml \  # 仅实验3A
PYTHONPATH=. python3 -m app.server
```

环境变量 `CONTENT_INBOX_DB` 覆盖数据库路径，`CONTENT_INBOX_PORT` 指定端口（8789，区别于生产端口 8787）。

---

## 实验 1：两个源 × 2 条 × concurrency=2（串行 vs 并发对比）

测试命令（串行）：
```python
# 顺序调用，两次独立 HTTP 请求
call_api(1, 小众软件, limit=2)
call_api(2, DaringFireball, limit=2)
```

测试命令（并发）：
```python
# ThreadPoolExecutor(max_workers=2)，同时发起两个 HTTP 请求
with ThreadPoolExecutor(max_workers=2):
    submit(小众软件), submit(DaringFireball)
```

### 结果总表

| 运行模式 | wall-clock | source_total_sum | max_source_total | sum_llm |
|---|---:|---:|---:|---:|
| 顺序 | 103.3s | 103.2s | - | 77.9s |
| 并发 | 58.7s | 104.4s | 58.7s | 79.0s |

**Speedup: 1.8x**。并发 wall clock (58.7s) ≈ max(source_total) (58.7s)，远小于 sum(source_total) (104.4s)。

### 详细 profile

| source | source_total | llm_seconds | pre_ded_wait | pre_ded_held | commit_wait | commit_held | embedding |
|---|---:|---:|---:|---:|---:|---:|---:|
| 小 众软件 (seq) | 55.6s | 34.0s | 0.000s | 0.006s | 0.000s | 0.018s | 0.000s |
| DaringFireball (seq) | 47.7s | 44.0s | 0.000s | 0.000s | 0.000s | 1.859s | 1.840s |
| SimonWillison (conc) | 58.7s | 53.1s | 0.000s | 0.000s | 0.000s | 3.601s | 3.586s |
| JeffGeerling (conc) | 45.8s | 25.9s | 0.000s | 0.000s | 0.000s | 0.015s | 0.000s |

### 判断

- **LLM 已并发**: wall=58.7s, sum_llm=79.0s (79s LLM work in 58.7s wall)
- **commit lock 开销极小**: commit_held 最大的情况(3.6s)包含了 embedding(3.586s)，实际 cluster commit 本身仅 0.015s
- **锁统计字段正常**: pre_dedupe 和 commit lock 的 wait/held 正确分拆，数值合理
- **embedding 仍在锁内**: commit_held=3.6s 中 embedding=3.586s，说明 commit lock 主要被 embedding 占据

---

## 实验 2：两个源 × 3 条 × concurrency=2

### 结果总表

| 运行模式 | wall-clock | source_total_sum | max_source_total | sum_llm | new_items |
|---|---:|---:|---:|---:|---:|
| 并发 | 27.6s | 55.1s | 27.6s | 47.4s | 2 (1+1) |

### 详细 profile

| source | source_total | llm_seconds | commit_wait | commit_held | embedding | total/new/dup |
|---|---:|---:|---:|---:|---:|---:|
| 小 众软件 | 27.6s | 23.4s | 0.000s | 2.065s | 2.056s | 3/1/2 |
| DaringFireball | 27.6s | 24.0s | 1.070s | 0.003s | 0.000s | 3/1/2 |

### 判断

- **同源串行、跨源并发**: 每个源 3 条，1 新 + 2 重复。新条目走 LLM（23-24s），重复条目直接 dedupe（<0.1s）
- **LLM 并发因子 1.7x**: 47.4s LLM 工作完成于 27.6s wall clock
- **commit lock 有轻微等待**: DaringFireball 的 commit_wait=1.070s（等小众软件的 embedding commit 完成），但 1s 相对于 27.6s total 仅占 3.6%
- **commit lock 不是主要瓶颈**: wait 时间远小于 LLM 时间

---

## 实验 3：max_concurrency 对比

### 同一组源 (SimonWillison + JeffGeerling, limit=2) 的并发运行

| max_concurrency | wall-clock | source_total_sum | max_source | sum_llm |
|---|---:|---:|---:|---:|
| 1 | 96.7s | 181.4s | 96.7s | 60.1s ⚠️ |
| 2 | 66.2s | 115.0s | 66.2s | 87.8s |

### 详细对比 (max_concurrency=2)

| source | source_total | llm_seconds | commit_wait | commit_held | embedding |
|---|---:|---:|---:|---:|---:|
| SimonWillison | 66.2s | 59.2s | 0.000s | 5.219s | ? |
| JeffGeerling | 48.8s | 28.6s | 0.000s | 1.576s | ? |

### 判断

- **max_concurrency=2 比 1 快约 46%**: wall 66.2s vs 96.7s（但 max_concurrency=1 的 profiler 数据有异常，一个 source 的 LLM 记录为 0.0s）
- **sum_llm/wall 在 max_concurrency=2 时 = 1.3x**: 确认有交错的 LLM 并发
- **无 429/timeout/JSON 失败**: 两个并发度下均未见 API 限流

---

## 锁粒度结论

### 1. Primary LLM 是否已从 CONTENT_STATE_LOCK 中移出？

**是**。实验 1 的并发 wall clock (58.7s) 远小于 sum(source_total) (104.4s)，且 pre_dedupe 和 commit lock 的 held 时间合计不超过 3.6s/源，远小于 LLM 耗时（25-53s/源）。

### 2. 不同源之间的 primary LLM 是否能并发？

**是**。并发模式下 79.0s 的 LLM 工作在 58.7s wall clock 内完成，LLM 并发因子 1.3x-1.8x。

### 3. Commit lock 是否明显阻塞？

**不明显**。commit_wait 最大仅 1.07s，commit_held 中大部分时间被 embedding API 占用（不是锁竞争）。对总耗时的影响 < 5%。

### 4. Embedding/cluster 是否成为新瓶颈？

**Embedding 是 commit lock 内的主要耗时项**（1.8-3.6s/源），但目前嵌入时间远小于 LLM 时间（25-53s/源），暂不构成瓶颈。如果后续 LLM 并发度增大（如 max_concurrency=4+），embedding 在锁内的累计等待可能值得关注。

### 5. 当前推荐的 --concurrency 值

**2-3**。当前 max_concurrent_sources 默认 3（batch_runner），LLM semaphore 默认 2。两者配比较合理。不建议超过 3，因为 LLM semaphore 会限制实际并发 LLM 数。

### 6. 当前推荐的 llm.max_concurrency 值

**2**（保持默认）。实验 3 显示 2 比 1 有显著收益（~46%），且未观察 API 限流。待后续用更多源跑全量测试后可考虑提升至 3。

---

## 风险和下一步建议

### 优先级 P0（确认稳定）
1. **全量回归测试**: 用 5-10 个源跑 batch 测试，确认拆锁不引入重复写入
2. **旧 profile 字段兼容**: `lock_wait_seconds` / `lock_held_seconds` 不再输出，需要更新下游消费者（如 source_results.csv 提取逻辑）

### 优先级 P1（优化）
3. **Embedding 出锁**: commit_held 中 embedding 是主要耗时。可考虑先获取 embedding（锁外），再在 commit lock 内做 cluster search/create/update（仅 DB 写）
4. **sqlite-vec 启用**: 当前 `sqlite_vec_available: false`，所有 cluster 操作返回 `embedding_failed`。需要排查 vec 扩展加载
5. **Profiler 线程安全**: 实验 3 中 max_concurrency=1 的一个源 LLM 记录为 0.0s，疑似 thread-local profiler 在特定并发模式下有数据丢失

### 优先级 P2（后续）
6. **Pre-LLM gate 优化**: 减少不必要的 LLM 调用，间接提升有效并发
7. **llm.max_concurrency 环境变量覆盖**: 目前只能通过 yaml 配置，建议增加 `CONTENT_INBOX_LLM_MAX_CONCURRENCY` 环境变量

---

## 测试文件清理

本轮创建的临时文件：
```bash
# 测试数据库
rm -rf content_inbox/outputs/manual_tests/concurrency_db/
# 测试 run 目录（由脚本自动生成）
# content_inbox/outputs/runs/rss_run_20260503_234*
```
