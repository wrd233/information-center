# content-inbox 锁粒度调整设计文档

> 建议存放路径：`content_inbox/docs/lock_granularity_design.md`

## 1. 背景

当前 `content-inbox` 的 RSS 批处理已经具备“源级并发”的外壳：外部脚本或服务端 batch runner 可以同时处理多个 RSS 源。但在单条内容进入 `process_content` 后，当前实现使用 `CONTENT_STATE_LOCK` 包住整个内容处理流程，导致 LLM、embedding、SQLite 写入和 cluster 更新全部串行执行。

这保证了正确性，但牺牲了吞吐。

当前问题可以概括为：

```text
源级可以并发
  ↓
RSS fetch / parse 可以并发
  ↓
但每条新内容进入 process_content 后
  ↓
LLM / embedding / DB / cluster 被同一把全局锁串行化
```

在已经完成 merged LLM、`merged_max_tokens`、prompt dump、`_raw_response` sanitize 等优化之后，单条内容的 LLM 成本已经下降。下一步可以考虑缩小锁粒度，让不同 RSS 源之间的新内容 LLM 处理真正并发。

本设计文档只讨论锁粒度调整，不讨论 prompt、评分策略、RSS 源管理、异步队列或完整任务系统。

---

## 2. 设计目标

本轮目标不是做一个完整并发架构，而是做一个**最小、安全、可回退的锁粒度调整**。

目标：

1. 不再在 LLM 调用期间持有 `CONTENT_STATE_LOCK`。
2. 不再因为一个源正在调用 LLM，而阻塞其他源的新内容 LLM。
3. 保持 SQLite 写入、dedupe 提交、cluster search/create/update 的一致性。
4. 保持同一个 RSS 源内部 entries 顺序处理。
5. 不引入任务队列、Celery、Redis、inflight registry、跨进程锁或复杂状态机。
6. 不改变 `/api/rss/analyze` 的对外语义。
7. 不改变数据库 schema。
8. 不删除 two_stage fallback，不改变 merged LLM 语义。
9. 通过小规模测试验证正确性，再考虑进一步优化。

---

## 3. 非目标

本轮明确不做：

1. 不做同一个 RSS 源内部 entry 并发。
2. 不做 inflight registry。
3. 不做任务队列。
4. 不做跨进程并发一致性。
5. 不支持多个 uvicorn worker 之间共享锁状态。
6. 不做 cluster 版本号、乐观锁、事件溯源。
7. 不改 embedding 模型、聚类阈值、评分策略。
8. 不改 prompt。
9. 不改 RSS 源 CSV 字段。
10. 不改数据库 schema。
11. 不清理历史 `data/` 或 `outputs/runs/`。
12. 不追求最大吞吐，只追求“不同源之间的 LLM 能并发”。

---

## 4. 当前锁的问题

当前逻辑可以抽象为：

```python
def process_content_thread_safe(store, payload, raw=None):
    with CONTENT_STATE_LOCK:
        return process_content(store, payload, raw=raw)
```

而 `process_content` 内部大致包含：

```text
normalize_content
build_dedupe_key
store.get_by_dedupe_key
screen_content        # LLM 网络调用
apply_score_policy
store.insert
cluster_content       # embedding 网络调用 + cluster search/create/update
store.update_item_clustering
```

问题在于：`screen_content` 和部分 `cluster_content` 是慢网络 I/O，但它们被包在全局锁里。这样即使外部 `--concurrency=2/3`，也只能做到多个源并发 fetch/parse，无法做到多个源并发 LLM。

---

## 5. 第一性原理分析：哪些操作需要锁？

### 5.1 不需要持有全局状态锁的操作

这些操作没有修改共享数据库状态，理论上可以在锁外执行：

```text
normalize_content
build_dedupe_key
pre-LLM gate（如果已有）
screen_content / LLM
apply_score_policy
生成 item embedding（仅计算向量，不做 cluster 判断）
```

注意：embedding API 调用本身是无共享状态的网络 I/O，可以锁外执行；但“拿 embedding 去查 cluster、决定 create/update cluster”涉及共享状态，不能锁外做。

### 5.2 必须在锁内执行的操作

这些操作读取或修改共享状态，第一版必须继续串行：

```text
store.get_by_dedupe_key 的最终确认
store.insert
cluster search active clusters
cluster create/update
cluster vector upsert
store.update_item_clustering
duplicate 命中时 update last_seen_at / seen 状态
```

尤其是 cluster 相关逻辑必须锁内执行。原因是 event cluster 没有简单唯一键约束，“是否属于同一个事件”依赖相似度和当前 cluster 状态。如果两个线程同时基于旧状态做判断，可能重复创建 cluster 或覆盖增量更新。

---

## 6. 建议的新流程

### 6.1 旧流程

```text
with CONTENT_STATE_LOCK:
    normalize
    build_dedupe_key
    dedupe check
    LLM screening
    score_policy
    insert item
    embedding
    cluster search/create/update
    update item clustering
```

### 6.2 新流程

```text
阶段 1：锁内快速 dedupe
    with CONTENT_STATE_LOCK:
        get_by_dedupe_key
        如果重复：
            update last_seen_at / seen 状态
            return duplicate

阶段 2：锁外慢处理
    screen_content / LLM
    apply_score_policy
    可选：embedding API 计算 item embedding
    注意：
        不写数据库
        不做 cluster search
        不 create/update cluster

阶段 3：锁内提交
    with CONTENT_STATE_LOCK:
        再次 get_by_dedupe_key
        如果重复：
            update last_seen_at / seen 状态
            return duplicate_after_prepare

        insert item

        如果不需要聚类：
            写 skipped_low_value / skipped 状态
            return result

        如果需要聚类：
            基于最新 cluster 状态 search active clusters
            判断 duplicate / incremental / new_event / uncertain
            create/update cluster
            upsert cluster vector
            update item clustering
            return result
```

关键点：

1. 阶段 3 必须做二次 dedupe。
2. cluster 判断必须在阶段 3 内基于最新状态做。
3. 阶段 2 不允许写库，不允许决定最终 cluster 归属。
4. 第一版可以接受重复 LLM 成本，但不允许重复写库。
5. 同一 RSS 源内部仍由 `rss_runner` 顺序处理 entries。

---

## 7. 关于重复内容重复调 LLM

第一版可以接受“极少数重复内容重复调 LLM”。

原因：

1. 当前场景不是高重复新闻聚合系统，大量 RSS 源之间完全重复的概率有限。
2. 就算重复，主要代价是 LLM 成本和时间，而不是数据正确性。
3. 第一版可以通过 commit 前二次 dedupe 保证不会重复写库。

但仍需注意风险：

```text
重复 LLM 会增加 API 成本
重复 LLM 会增加 API 限流概率
重复 LLM 可能得到略有差异的模型判断
如果没有二次 dedupe，可能导致 UNIQUE 冲突或重复 item
如果 cluster commit 不在锁内，可能导致重复 cluster
```

本轮不引入 inflight registry。后续如果发现重复 LLM 成本明显，再单独设计 inflight。

---

## 8. SQLite 写入策略

SQLite 写入阶段继续由一把 commit lock 保护。

本轮不追求多写并发，也不需要在 LLM 调用期间持有 SQLite 写锁。

建议：

```text
LLM 时不持锁
embedding 时尽量不持锁
DB insert/update 时持锁
cluster search/create/update 时持锁
```

如果当前 `CONTENT_STATE_LOCK` 名义上已经承担“全局内容状态提交锁”，可以继续复用它；也可以重命名为 `CONTENT_COMMIT_LOCK`，但第一版不建议为了命名做大改。

---

## 9. Cluster 风险与处理原则

### 9.1 重复 cluster 创建

风险：

```text
线程 A：锁外 LLM/embedding 完成
线程 B：锁外 LLM/embedding 完成

如果 A/B 都在锁外查 cluster：
    A 查不到相似 cluster，准备 create
    B 也查不到相似 cluster，准备 create
    最终同一事件出现两个 cluster
```

处理原则：

```text
embedding 可锁外计算
cluster search/create/update 必须锁内做
```

### 9.2 增量更新覆盖

风险：

```text
A 判断 item_1 是 cluster_X 的 incremental update
B 判断 item_2 也是 cluster_X 的 incremental update
A 更新 cluster_X
B 基于旧 cluster_X 再更新 cluster_X
```

处理原则：

```text
cluster update 必须锁内串行
第一版不做乐观锁
第一版不做 cluster version
第一版不做同一 cluster 的并发 update
```

---

## 10. 同源顺序

必须保持：

```text
不同源之间可以并发
同一源内部 entries 仍然顺序处理
```

不要把单个 RSS 源内的多个 entries 打平成全局线程池。

原因：

1. 同源条目通常具有时间顺序。
2. 同源条目可能在同一事件上连续更新。
3. 同源乱序会影响 dedupe、cluster、incremental update 的可解释性。
4. 当前项目第一阶段不需要追求同源最大吞吐。

---

## 11. LLM 并发安全阀

拆锁后，`--concurrency` 会真正增加同时 LLM 请求数。需要一个简单安全阀，避免一次发太多 API 请求。

第一版建议：

```yaml
llm:
  max_concurrency: 2
```

代码层可以使用：

```python
LLM_SEMAPHORE = threading.Semaphore(settings.llm.get("max_concurrency", 2))
```

原则：

1. 不引入复杂 rate limiter。
2. 不实现 token bucket。
3. 不做全局预算控制。
4. 只限制同时进行的 LLM 请求数。
5. 默认值保守设为 2。
6. 后续通过 profiling 再调大。

如果担心改动范围，第一版也可以先不加 semaphore，只建议用户将 `--concurrency` 控制在 2；但从安全性看，简单 semaphore 是值得的。

---

## 12. 可能的实施分阶段

### Step 1：只重构结构，不改变锁范围

目标：

```text
抽出 prepare / commit 函数
但 process_content_thread_safe 仍然锁住整个流程
确保行为完全不变
```

收益：

```text
降低后续拆锁风险
便于测试
```

### Step 2：只把 LLM 移到锁外

目标：

```text
快速 dedupe 锁内
LLM 锁外
insert + embedding + cluster 仍然锁内
```

收益：

```text
先释放最大瓶颈 LLM
不需要拆 cluster_content
风险较低
```

### Step 3：评估是否把 embedding 也移到锁外

前提：

```text
cluster_content 可以被拆成：
    embed item text
    cluster commit with existing embedding
```

如果当前 `cluster_content` 耦合太深，可以暂缓。

### Step 4：小样本并发测试

验证：

```text
--concurrency=1
--concurrency=2
--concurrency=3
```

比较：

```text
source_total_seconds
lock_wait_seconds
lock_held_seconds
llm_seconds
embedding_seconds
commit_seconds
failed_items
duplicate_after_prepare
cluster 结果
```

---

## 13. 第一版推荐方案

第一版推荐选择：

```text
只把 LLM 移到锁外
embedding + cluster 暂时留在锁内
```

原因：

1. LLM 是当前最大耗时。
2. 改动小，不需要拆 `cluster_content`。
3. cluster 风险最小。
4. 可以快速验证 `--concurrency` 是否真正提升。
5. 后续再决定是否拆 embedding。

新流程：

```text
锁内：
    初始 dedupe check

锁外：
    LLM screening
    apply_score_policy

锁内：
    二次 dedupe
    insert
    embedding
    cluster
    update item clustering
```

这不是最终最优，但可能是最稳的第一刀。

---

## 14. 预期影响

### 正面影响

1. 不同源的 LLM 可以并发。
2. 全局锁持有时间明显下降。
3. `--concurrency=2/3` 开始真正有效。
4. 单源顺序不变。
5. cluster 一致性基本不变。
6. 不改变 API 对外语义。

### 负面影响

1. 极少数重复内容可能重复调 LLM。
2. API 并发压力上升。
3. 如果没有 LLM semaphore，可能触发限流。
4. 二次 dedupe 后可能出现 `duplicate_after_prepare`，需要结果结构能表达。
5. 如果 LLM 成功但 commit 发现重复，会浪费一次 LLM。
6. 如果 LLM 失败，不会进入 commit，需要保持原有 failed screening 语义。
7. 如果 commit 阶段仍然很慢，整体提升有限。

---

## 15. 需要关注的结果状态

拆锁后可能需要表达一个新状态：

```text
duplicate_after_prepare
```

含义：

```text
prepare 阶段开始时未命中重复；
锁外 LLM 已完成；
commit 前二次 dedupe 发现其他线程已经写入；
因此本条不再 insert，作为 duplicate 返回。
```

第一版可以不新增复杂模型字段，但日志中必须可见，以便理解为什么“LLM 调了但最终 duplicate”。

---

## 16. 测试计划

### 16.1 单元测试

建议覆盖：

1. 旧重复内容：初始 dedupe 命中，不调用 LLM。
2. 新内容：初始 dedupe 未命中，调用 LLM，commit 成功。
3. commit 前二次 dedupe 命中：返回 duplicate_after_prepare，不重复 insert。
4. LLM 失败：不进入 commit，返回 screening failed。
5. suggested_action 修复、merged/two_stage 行为不受影响。
6. 同源 entries 顺序处理逻辑不变。

### 16.2 并发测试

建议 mock LLM，构造两个不同源同时处理：

1. 两个不同 dedupe_key：
   - 两个 LLM 可以并发进入；
   - commit 仍然串行；
   - 两条都成功入库。

2. 两个相同 dedupe_key：
   - 第一条 commit 成功；
   - 第二条 commit 前二次 dedupe 命中；
   - 不重复 insert。

3. LLM slow mock：
   - concurrency=2 时总耗时小于串行耗时；
   - 用于证明 LLM 已经移出全局锁。

### 16.3 手工验证

小样本：

```bash
python3 -u content_inbox/scripts/run_rss_sources_to_content_inbox.py   --api-base http://127.0.0.1:8787   --csv rsshub/rss_opml/rss_sources.csv   --count 2   --limit-per-source 2   --url-mode docker-host   --concurrency 2   --profile
```

观察：

```text
lock_wait_seconds 是否下降
lock_held_seconds 是否下降
source_total_seconds 是否下降
llm 时间是否并发重叠
failed_items 是否增加
duplicate_after_prepare 是否出现
cluster 是否异常重复
```

---

## 17. 回退策略

必须保留简单回退方式。

建议配置：

```yaml
processing:
  lock_scope: "full"      # full | commit
```

或者更轻：

```yaml
processing:
  llm_outside_lock: false
```

默认第一阶段可以先保持 `false`，验证时开启 `true`。

如果希望改动更少，也可以先不做配置开关，但必须保证 Git diff 小、容易 revert。

推荐：

```text
第一版加配置开关，默认 false；
手动测试时开启 true；
稳定后再默认开启。
```

---

## 18. 总结

当前全局锁的主要问题是把 LLM 网络 I/O 和共享状态提交绑定在一起。根据当前项目阶段，最小合理调整是：

```text
允许不同源的 LLM 并发；
继续串行提交数据库和 cluster；
保持同源 entries 顺序；
允许少量重复 LLM 成本；
commit 前二次 dedupe；
cluster 判断仍然锁内。
```

第一版不要追求完全并发化。最稳的第一刀是：

```text
只把 LLM 移出锁外；
embedding + cluster 暂时留在锁内；
加二次 dedupe；
可选加 LLM semaphore；
通过配置开关控制。
```

这能显著减少锁持有时间，同时不破坏当前系统最重要的一致性边界。
