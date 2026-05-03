# content-inbox RSS 源级并发改进设计文档

> 适用仓库：`wrd233/information-center`  
> 适用组件：`content_inbox`  
> 设计日期：2026-05-03  
> 设计阶段：给 Codex 实现前的方案文档

---

## 1. 当前仓库状态简述

根据当前仓库重新检查，`content_inbox` 已经不只是一个简单的 RSS 入库模块，它已经具备以下能力：

- `POST /api/rss/analyze`：分析单个 RSS 源。
- `POST /api/content/analyze`：分析单条内容。
- `GET /api/inbox`：查询筛选后的内容。
- `process_content()` 内部已经包含：标准化、去重、AI 筛选、入库、事件聚类、通知决策等逻辑。
- `storage.py` 中已经存在 `inbox_items` 和 `event_clusters` 两类核心状态表。
- `clusterer.py` 中已经有 embedding、相似 cluster 检索、新事件判断、重复判断、增量更新判断等逻辑。
- `run_rss_sources_to_content_inbox.py` 已经具备读取 CSV、选择源、逐源提交、保存运行报告、断点恢复、跳过已知失败源等外围调度能力。

但当前并发能力仍然不足：

- `RSSAnalyzeRequest` 仍然是单个 `feed_url` 输入。
- `/api/rss/analyze` 仍然一次只处理一个 RSS 源。
- 单源内部 entries 是 `for entry in entries` 顺序处理。
- `run_rss_sources_to_content_inbox.py` 虽然能读取多个 RSS 源，但主流程仍然是 `for plan in pending_plans` 逐个调用 `/api/rss/analyze`。
- 当前没有原生的 `/api/rss/analyze-batch`，也没有 `max_concurrent_sources` 这类源级并发参数。

因此，这一次改进的目标不是把所有条目粗暴地多线程化，而是给 `content_inbox` 增加**受控的源级并发能力**。

---

## 2. 设计目标

一句话目标：

> 让 `content_inbox` 能稳定、可控地同时处理多个 RSS 源，但不牺牲单源顺序、全局去重和事件聚类的一致性。

具体目标：

1. 保留现有 `/api/rss/analyze` 单源接口，不破坏已有调用方式。
2. 新增 `/api/rss/analyze-batch` 批量接口，支持一次传入多个 RSS 源。
3. 支持 `max_concurrent_sources`，用于限制同时运行的 RSS 源数量。
4. 同一个 RSS 源内部的条目必须按确定顺序逐条处理，不做条目级并发。
5. 不同 RSS 源之间可以并发处理。
6. 单个源失败不能导致整个 batch 失败。
7. 单个条目失败不能导致同源后续条目全部中断。
8. 对去重、入库、事件聚类等全局共享状态保持保守，避免并发导致重复 cluster 或重复 item。
9. 让现有 `run_rss_sources_to_content_inbox.py` 后续可以变薄：它负责选择源和保存报告，核心批量处理能力由 `content_inbox` 服务端承担。

---

## 3. 非目标

本次不建议一次性做以下事情：

1. 不做全局条目级并发。
2. 不引入复杂任务队列，例如 Celery、Redis Queue、Kafka。
3. 不做长期后台任务系统。
4. 不做定时调度系统。
5. 不重写整个 `process_content()` 主流程。
6. 不把所有 RSS 源一次性无限并发打满。
7. 不把 `run_rss_sources_to_content_inbox.py` 直接删除。

这次改进应当是一个小步但方向正确的架构升级：先把**批量源输入 + 源级并发 + 同源顺序 + 结果汇总**做稳。

---

## 4. 第一性原理约束

### 4.1 RSS 源是一条有顺序的信息流

同一个 RSS 源里的近期条目通常存在时间和语义关系：

```text
Source A:
A1 → A2 → A3 → A4
```

这些条目可能是同一个事件的连续进展，也可能是同一个作者围绕一个主题的连续表达。

因此，同一个源内部不应该把条目打散并发处理。

设计原则：

```text
同一个源内部：串行、确定顺序、可维护 source-local context。
```

建议处理顺序：

```text
拉取最近 N 条后，按 published_at 从旧到新处理。
```

如果没有 `published_at`，再回退到 feed 原始顺序。

---

### 4.2 不同 RSS 源是可以并行读取的独立输入流

不同源之间不存在强制顺序。

```text
Source A: A1 → A2 → A3
Source B: B1 → B2
Source C: C1 → C2 → C3
```

可以让 A、B、C 三个 SourceWorker 同时运行。

设计原则：

```text
源与源之间：允许并发，但必须有上限。
```

默认建议：

```text
max_concurrent_sources = 3
```

可接受范围：

```text
1 <= max_concurrent_sources <= 5
```

第一版不要默认开放到 10、20。

---

### 4.3 去重、入库、事件聚类是全局共享状态

当前系统已经有：

- `inbox_items`
- `event_clusters`
- `dedupe_key`
- cluster similarity search
- cluster create/update
- notification decision

这些都是全局共享状态。

如果多个 SourceWorker 同时处理同一个热点事件，容易出现：

```text
Source A 发现“某模型发布”
Source B 发现“某模型发布”
Source C 发现“某模型发布”

三个 worker 同时查不到已有 cluster
于是分别创建 cluster
```

结果变成：

```text
cluster_1: 某模型发布
cluster_2: 某公司发布新模型
cluster_3: 新模型上线
```

这会降低事件聚类质量。

设计原则：

```text
可以并发做 I/O 和 AI 分析；
全局 dedupe、入库、cluster 匹配、cluster 创建、cluster 更新必须受控。
```

---

## 5. 推荐总体架构

新增一个服务端批量运行层：

```text
/api/rss/analyze-batch
        ↓
RSSBatchRunner
        ↓
最多 max_concurrent_sources 个 RSSSourceWorker 并发运行
        ↓
每个 RSSSourceWorker 内部按顺序处理 entries
        ↓
全局状态提交区保护 dedupe / insert / cluster
        ↓
返回 batch 汇总和 source_results
```

逻辑结构：

```text
RSSBatchRunner
    ├── SourceWorker A: A1 → A2 → A3
    ├── SourceWorker B: B1 → B2
    └── SourceWorker C: C1 → C2 → C3
```

核心边界：

```text
并发单位：RSS 源
顺序单位：同源条目
一致性单位：全局提交区
```

---

## 6. 建议新增或调整的代码结构

### 6.1 新增模型

建议在 `app/models.py` 中新增：

```python
class RSSSourceSpec(BaseModel):
    feed_url: str
    source_name: str | None = None
    source_category: str | None = None
    source_id: str | None = None
    limit: int | None = Field(default=None, ge=1, le=200)
    screen: bool | None = None

class RSSBatchAnalyzeRequest(BaseModel):
    sources: list[RSSSourceSpec]
    limit_per_source: int | None = Field(default=20, ge=1, le=200)
    screen: bool = True
    max_concurrent_sources: int = Field(default=3, ge=1, le=5)
    preserve_source_entry_order: bool = True
    include_items: bool = True

class RSSSourceAnalyzeResult(BaseModel):
    ok: bool
    source_id: str | None = None
    feed_url: str
    source_name: str | None = None
    source_category: str | None = None
    status: Literal["success", "partial_failed", "failed"]
    total_items: int = 0
    new_items: int = 0
    duplicate_items: int = 0
    screened_items: int = 0
    recommended_items: int = 0
    new_event_items: int = 0
    incremental_items: int = 0
    silent_items: int = 0
    failed_items: int = 0
    error: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)

class RSSBatchAnalyzeResponse(BaseModel):
    ok: bool
    total_sources: int
    successful_sources: int
    failed_sources: int
    partial_failed_sources: int
    total_items: int
    new_items: int
    duplicate_items: int
    screened_items: int
    recommended_items: int
    new_event_items: int
    incremental_items: int
    silent_items: int
    failed_items: int
    max_concurrent_sources: int
    source_results: list[RSSSourceAnalyzeResult]
```

第一版不一定必须全部使用 Pydantic response model，但建议先把结构稳定下来。

---

### 6.2 抽取单源处理函数

当前 `/api/rss/analyze` 的核心逻辑在 `server.py` 里。建议抽出为可复用函数：

```text
app/rss_runner.py
```

建议包含：

```python
def analyze_one_rss_source(
    inbox_store: InboxStore,
    payload: RSSAnalyzeRequest,
    *,
    include_items: bool = True,
) -> dict[str, Any]:
    ...
```

`/api/rss/analyze` 继续调用这个函数。

`/api/rss/analyze-batch` 的 SourceWorker 也调用这个函数。

这样可以避免单源逻辑在 `server.py` 和 batch runner 里复制两份。

---

### 6.3 新增批量运行器

建议新增：

```text
app/batch_runner.py
```

核心类：

```python
class RSSBatchRunner:
    def __init__(self, store: InboxStore, max_concurrent_sources: int):
        self.store = store
        self.max_concurrent_sources = max_concurrent_sources

    def run(self, request: RSSBatchAnalyzeRequest) -> dict[str, Any]:
        ...
```

第一版可以使用：

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
```

基本逻辑：

```python
with ThreadPoolExecutor(max_workers=request.max_concurrent_sources) as executor:
    future_map = {
        executor.submit(run_one_source, source): source
        for source in request.sources
    }

    for future in as_completed(future_map):
        result = future.result()
        source_results.append(result)
```

注意：返回结果最好按输入顺序排序，而不是按完成顺序排序。

可以在 `RSSSourceSpec` 或内部 plan 中加入 `sequence`。

---

## 7. 单源内部处理规则

### 7.1 每个 SourceWorker 只处理一个源

每个 worker 的流程：

```text
1. 解析 RSS 源
2. 取最近 N 条
3. 排序 entries
4. for entry in entries:
       逐条 process_content
5. 汇总结果
```

---

### 7.2 entries 排序规则

建议新增一个本地函数：

```python
def sort_entries_for_processing(entries: list[ContentAnalyzeRequest]) -> list[ContentAnalyzeRequest]:
    ...
```

排序建议：

1. 有 `published_at` 的，按 `published_at` 从旧到新。
2. 没有 `published_at` 的，保留原始 feed 顺序。
3. 混合情况要保持稳定排序，不要让无时间条目随机漂移。

原因：

```text
RSS 展示通常新到旧；
但事件理解更适合旧到新。
```

---

### 7.3 source-local context

第一版可以先不强制做复杂上下文，但可以预留结构。

建议每个 SourceWorker 内部维护：

```python
source_run_context = {
    "recent_accepted_items": [],
    "recent_cluster_ids": [],
    "recent_event_hints": [],
}
```

第一版可以只记录，不接入 prompt。

后续可用于判断：

- 当前条目是否是同源前序条目的补充。
- 当前条目是否只是重复描述。
- 当前条目是否把前面的事件推进了一步。

不要一开始把同源上下文全部塞给模型。

建议上限：

```text
最近 3～5 条
只保留 title、summary、event_hint、cluster_id、decision
```

---

## 8. 全局状态一致性设计

这是本次并发改进最重要的部分。

### 8.1 第一版保守策略

如果不想大幅改造 `process_content()`，第一版可以采用一个全局锁：

```python
CONTENT_STATE_LOCK = threading.RLock()
```

并在 batch runner 内部调用时保护全局状态相关路径。

最保守方式：

```python
with CONTENT_STATE_LOCK:
    result = process_content(inbox_store, entry, raw=entry.model_dump())
```

这个方式最安全，但并发收益有限，因为 AI 筛选、embedding、聚类都会被串行化。

适合作为第一步验证：

- batch API 是否正确。
- 源级并发是否能运行。
- 同源顺序是否稳定。
- 结果汇总是否可靠。

但它不是最终性能最优方案。

---

### 8.2 推荐的改进策略：两段式处理

后续建议把 `process_content()` 拆为：

```text
prepare_candidate 阶段：可并发
commit_candidate 阶段：受控提交
```

候选流程：

```text
normalize
build dedupe_key
初步 duplicate check
AI screening
embedding
生成 candidate
```

提交流程：

```text
二次 duplicate check
insert item
search active clusters
create/update cluster
update item clustering
mark seen
```

伪代码：

```python
candidate = prepare_content_candidate(entry)

with CONTENT_STATE_LOCK:
    result = commit_content_candidate(store, candidate)
```

这个方式可以让慢的网络/模型调用并发起来，同时让数据库和 cluster 状态保持一致。

---

### 8.3 为什么需要二次 dedupe check

并发场景下可能出现：

```text
Worker A 初查：没有 dedupe_key
Worker B 初查：没有 dedupe_key
Worker A 准备完成并写入
Worker B 准备完成后也想写入
```

所以提交时必须再次检查：

```text
commit 阶段必须重新 get_by_dedupe_key
```

如果发现已存在，就转为 duplicate / mark_seen，而不是继续 insert。

---

### 8.4 cluster 匹配需要在提交区内做最终判断

embedding 可以在提交区外生成。

但以下动作最好在提交区内完成：

```text
archive_stale_clusters
search_active_clusters
create_cluster
update_cluster
update_item_clustering
```

原因：cluster 搜索和 cluster 创建/更新之间不能被其他 worker 打断，否则容易重复建 cluster。

---

## 9. API 设计

### 9.1 新增接口

```text
POST /api/rss/analyze-batch
```

请求示例：

```json
{
  "sources": [
    {
      "source_id": "row_001",
      "feed_url": "http://127.0.0.1:1200/bilibili/user/video/3546676667091128",
      "source_name": "UP 主 A",
      "source_category": "Videos/Bilibili"
    },
    {
      "source_id": "row_002",
      "feed_url": "http://127.0.0.1:1200/bilibili/user/video/946974",
      "source_name": "UP 主 B",
      "source_category": "Videos/Bilibili"
    }
  ],
  "limit_per_source": 8,
  "screen": true,
  "max_concurrent_sources": 3,
  "preserve_source_entry_order": true,
  "include_items": true
}
```

返回示例：

```json
{
  "ok": true,
  "total_sources": 2,
  "successful_sources": 2,
  "failed_sources": 0,
  "partial_failed_sources": 0,
  "total_items": 16,
  "new_items": 7,
  "duplicate_items": 8,
  "screened_items": 16,
  "recommended_items": 4,
  "new_event_items": 3,
  "incremental_items": 1,
  "silent_items": 9,
  "failed_items": 0,
  "max_concurrent_sources": 3,
  "source_results": [
    {
      "ok": true,
      "source_id": "row_001",
      "feed_url": "http://127.0.0.1:1200/bilibili/user/video/3546676667091128",
      "source_name": "UP 主 A",
      "source_category": "Videos/Bilibili",
      "status": "success",
      "total_items": 8,
      "new_items": 3,
      "duplicate_items": 5,
      "failed_items": 0,
      "items": []
    }
  ]
}
```

---

### 9.2 单源失败返回

如果某个源拉取失败、解析失败或超时，不抛出整个 batch。

单源结果：

```json
{
  "ok": false,
  "source_id": "row_003",
  "feed_url": "http://bad-feed.example/rss.xml",
  "source_name": "Bad Source",
  "status": "failed",
  "total_items": 0,
  "failed_items": 0,
  "error": "failed to parse feed: ...",
  "items": []
}
```

batch 层：

```text
只要存在 failed source，batch ok 可以为 false；
但必须完整返回所有 source_results。
```

建议：

```text
batch.ok = failed_sources == 0 and partial_failed_sources == 0
```

---

### 9.3 单条失败返回

如果同一个源中某个 entry 失败：

- `failed_items += 1`
- `status = partial_failed`
- 继续处理同源后续 entry
- 在 `items` 中记录失败条目的 title/error

---

## 10. 执行脚本后续调整方向

当前 `run_rss_sources_to_content_inbox.py` 不要马上废弃。

短期保持：

```text
读取 rss_sources.csv
选择本次要跑的源
处理 url-mode
dry-run
resume
skip-known-failed
运行报告
```

后续改薄：

```text
原来：for plan in pending_plans: POST /api/rss/analyze
未来：构造 sources[]，一次 POST /api/rss/analyze-batch
```

脚本仍然负责：

- 从 CSV/Excel/OPML 中选择源。
- 管理运行目录。
- 输出 selected_sources.csv。
- 输出 source_results.csv。
- 输出 report.md。
- 处理 dry-run/resume/skip-known-failed 等操作层逻辑。

服务端负责：

- 批量源处理。
- 源级并发。
- 同源顺序。
- 去重、筛选、聚类、入库。
- 源结果汇总。

---

## 11. 测试设计

建议增加以下测试。

### 11.1 batch request 模型测试

验证：

- `max_concurrent_sources` 默认值为 3。
- `max_concurrent_sources < 1` 报错。
- `max_concurrent_sources > 5` 报错。
- `sources` 为空时报错。

---

### 11.2 单源顺序测试

构造一个 fake feed：

```text
A3 published_at=10:03
A1 published_at=10:01
A2 published_at=10:02
```

验证实际处理顺序为：

```text
A1 → A2 → A3
```

---

### 11.3 源级并发测试

构造多个 fake source，每个 source 内部 sleep。

验证：

- `max_concurrent_sources=1` 时总耗时接近串行。
- `max_concurrent_sources=3` 时总耗时明显下降。
- 同一个 source 内部处理顺序不乱。

---

### 11.4 单源失败隔离测试

构造：

```text
Source A success
Source B parse failed
Source C success
```

验证：

- batch 返回所有三个 source_results。
- Source B status = failed。
- Source A/C 不受影响。
- batch failed_sources = 1。

---

### 11.5 单条失败隔离测试

构造一个 source，其中第二条 entry 处理失败。

验证：

```text
A1 success
A2 failed
A3 success
```

并验证：

- Source status = partial_failed。
- failed_items = 1。
- 后续 entry 继续执行。

---

### 11.6 dedupe 并发安全测试

构造两个 source，包含相同 URL 或相同 guid。

验证：

- 最终只插入一个 item。
- 另一个被识别为 duplicate 或 mark_seen。
- 不出现 SQLite unique constraint 未捕获异常。

---

### 11.7 cluster 并发安全测试

构造多个 source 的相似内容。

验证：

- 不会因为并发创建大量重复 cluster。
- 相似内容应归入同一个 cluster，或至少不会因为竞态产生明显错误。

第一版如果难以做完整 embedding 测试，可以 mock `embed_text()` 和 `search_active_clusters()`。

---

## 12. 推荐实施步骤

### 第一步：抽函数，不改行为

- 把 `/api/rss/analyze` 内部逻辑抽到 `analyze_one_rss_source()`。
- 确保现有 `/api/rss/analyze` 行为不变。
- 跑现有测试或手动 curl 验证。

### 第二步：新增 batch API

- 增加请求/响应模型。
- 增加 `/api/rss/analyze-batch`。
- 使用 ThreadPoolExecutor 做源级并发。
- 单源内部仍然顺序处理。

### 第三步：加入全局状态保护

- 第一版可以先用 `RLock` 保护 `process_content()`。
- 保证不会出现数据库竞态或重复 cluster 明显异常。

### 第四步：补测试

优先补：

- 单源顺序。
- 源级并发上限。
- 失败隔离。
- 结果汇总。

### 第五步：逐步优化性能

将 `process_content()` 拆为：

```text
prepare_candidate
commit_candidate
```

让 AI 筛选和 embedding 在锁外执行，让 dedupe/insert/cluster commit 在锁内执行。

---

## 13. 验收标准

实现完成后，至少满足：

1. 原有 `/api/rss/analyze` 可继续使用。
2. 新增 `/api/rss/analyze-batch` 可一次处理多个 RSS 源。
3. `max_concurrent_sources=1` 时表现等价于源级串行。
4. `max_concurrent_sources=3` 时不同源可并发运行。
5. 同一个源内部条目顺序稳定。
6. 一个源失败不影响其他源。
7. 一个条目失败不影响后续条目。
8. 返回结果包含 source-level 汇总。
9. 不出现未捕获的 SQLite unique constraint 异常。
10. 不出现明显的并发重复 cluster 问题。
11. README 或 docs 中说明新接口和并发边界。

---

## 14. 最终设计结论

本次并发改进应采用：

```text
源级并发
同源串行
全局状态受控提交
服务端原生 batch API
外部脚本逐步变薄
```

一句话总结：

> 把并发放在“源”这一层，把顺序保留在“条目”这一层，把一致性收束在“去重、入库、聚类”这一层。
