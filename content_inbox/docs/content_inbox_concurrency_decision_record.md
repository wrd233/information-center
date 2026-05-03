# content-inbox RSS 并发改进：决策背景、决策过程和决策结果

> 文档类型：架构决策记录 / ADR 风格说明  
> 适用仓库：`wrd233/information-center`  
> 适用组件：`content_inbox`  
> 日期：2026-05-03

---

## 1. 决策背景

### 1.1 当前系统定位

`content_inbox` 不是单纯的 RSS 抓取器，而是一个面向个人信息入口的内容处理模块。

它当前承担的职责包括：

```text
RSS 解析
内容标准化
去重
AI 打分/筛选
摘要和标签生成
embedding
事件聚类
重复/增量判断
通知决策
入库
查询
```

因此，`content_inbox` 的并发设计不能只考虑“跑得更快”，还必须考虑：

```text
内容顺序
去重一致性
事件聚类稳定性
失败隔离
可重跑
运行报告可解释
```

---

### 1.2 当前实现状态

重新检查当前仓库后，可以看到：

- `content_inbox/app/models.py` 中 `RSSAnalyzeRequest` 仍然是单个 `feed_url`。
- `content_inbox/app/server.py` 中 `/api/rss/analyze` 仍然一次处理一个 RSS 源。
- `/api/rss/analyze` 内部会 `parse_feed()`，然后对 entries 做顺序 `for entry in entries`。
- `content_inbox/app/processor.py` 中 `process_content()` 同时负责去重、筛选、入库、聚类。
- `content_inbox/app/storage.py` 中已有 `inbox_items` 和 `event_clusters` 两类核心状态表。
- `content_inbox/app/clusterer.py` 中已有 embedding 检索、新事件判断、重复判断、增量更新判断。
- `content_inbox/scripts/run_rss_sources_to_content_inbox.py` 已经能从 CSV 读取多个源、选择源、调用接口、保存报告、断点恢复，但主流程仍然是逐源顺序调用 `/api/rss/analyze`。

这说明系统已经有较完整的内容理解和事件聚类基础，但缺少服务端原生的多源并发处理能力。

---

### 1.3 需要解决的问题

当前主要问题不是“无法读取多个源”，而是：

```text
多个源只能在外部脚本中逐个提交；
content_inbox 服务本身不知道 batch；
并发控制没有沉到服务内部；
后续每个外部脚本都可能重复实现并发、失败隔离、结果汇总；
如果简单在外部开多进程打接口，又容易引发数据库和 cluster 竞态。
```

因此，需要为 `content_inbox` 原生增加：

```text
批量 RSS 源输入
源级并发控制
同源顺序保证
失败隔离
结果汇总
全局状态保护
```

---

## 2. 核心约束

### 2.1 同源条目具有顺序语义

同一个 RSS 源里的近期内容不是随机集合，而是一条时间流。

例如：

```text
08:00 某模型发布
09:30 开发者发现新能力
11:00 官方补充说明
14:00 社区争议扩大
```

如果这些条目被并发处理，后面的内容可能在前面的内容入库之前被判断，导致：

```text
重复判断不准
增量判断不准
cluster 归属不稳
上下文关系丢失
```

所以，同一个源内部必须保持顺序处理。

---

### 2.2 不同源之间没有强制顺序

不同 RSS 源是独立输入流。

```text
Source A: AI 新闻
Source B: 技术博客
Source C: B 站视频
Source D: 社会议题
```

这些源之间没有天然的处理先后要求，因此可以并发。

并发边界应该是：

```text
源与源之间并发；
源内部条目串行。
```

---

### 2.3 全局去重和事件聚类是共享状态

`content_inbox` 当前已经有 `inbox_items` 和 `event_clusters`。

并发处理时，最危险的不是 RSS 拉取，而是：

```text
多个 worker 同时检查 dedupe_key
多个 worker 同时搜索 active cluster
多个 worker 同时创建 cluster
多个 worker 同时更新 cluster item_count / summary / vector
```

如果不加控制，可能导致：

```text
重复 item
SQLite unique constraint 异常
重复 cluster
错误的 item_count
错误的 notification decision
```

因此，全局状态部分必须受控。

---

## 3. 备选方案比较

### 3.1 方案 A：不改 content_inbox，只在外部脚本里并发

做法：

```text
run_rss_sources_to_content_inbox.py 内部使用线程池；
多个线程同时调用 /api/rss/analyze。
```

优点：

```text
改动小；
不动服务端；
短期容易验证。
```

缺点：

```text
并发语义散落在外部脚本中；
以后每个新脚本都要重复实现并发；
服务端无法统一控制全局状态；
多个外部进程同时打服务时风险更高；
错误汇总和结果结构不稳定。
```

判断：

```text
不推荐作为长期方案。
```

可以作为临时压测手段，但不应成为核心架构。

---

### 3.2 方案 B：条目级全局并发

做法：

```text
把所有源的所有 entries 打平成一个大列表；
丢进全局线程池；
所有条目一起处理。
```

优点：

```text
吞吐可能最高；
实现看起来直接。
```

缺点：

```text
破坏同源顺序；
破坏事件演化判断；
更容易产生重复 cluster；
更难解释运行结果；
更难重试；
对 SQLite 和模型 API 压力不可控。
```

判断：

```text
明确不采用。
```

这类并发适合无状态数据清洗，不适合当前这种有去重、聚类、增量判断的信息入口系统。

---

### 3.3 方案 C：引入任务队列

做法：

```text
引入 Celery / Redis Queue / Kafka / APScheduler 等；
把 RSS 源或条目变成异步任务。
```

优点：

```text
扩展性强；
后续可以做后台任务、定时调度、重试队列。
```

缺点：

```text
复杂度明显上升；
本地开发和部署成本上升；
当前阶段需求没有复杂到必须引入队列；
会把注意力从内容处理逻辑转移到基础设施。
```

判断：

```text
暂不采用。
```

未来如果 RSS 源数量、抓取频率、任务时长明显增加，可以再考虑任务队列。

---

### 3.4 方案 D：content_inbox 原生 batch API + 源级并发

做法：

```text
新增 /api/rss/analyze-batch；
一次接收多个 RSS 源；
用 max_concurrent_sources 控制源级并发；
每个源内部 entries 顺序处理；
全局 dedupe / insert / cluster 受控提交；
返回 source_results 和 batch 汇总。
```

优点：

```text
符合 RSS 源的顺序语义；
吞吐比纯串行更好；
服务端统一掌握并发边界；
结果结构稳定；
失败隔离清楚；
外部脚本可以变薄；
后续容易扩展到 CLI / Web UI / 自动调度。
```

缺点：

```text
需要改服务端模型和 API；
需要处理并发安全；
第一版可能需要较保守的锁，性能不是极限。
```

判断：

```text
采用。
```

这是当前阶段收益、复杂度、稳定性之间最平衡的方案。

---

## 4. 决策过程

### 4.1 第一轮判断：并发粒度不能是“条目”

最开始的问题看似是“content_inbox 是否支持多线程”，但真正需要回答的是：

```text
什么东西可以乱序？
什么东西必须有序？
什么状态必须保持一致？
```

结论：

```text
RSS 源之间可以并发；
同源条目不能并发；
全局状态不能无保护并发。
```

所以并发粒度从“条目”收紧为“源”。

---

### 4.2 第二轮判断：批量能力应该进服务端，而不是只留在脚本

`run_rss_sources_to_content_inbox.py` 已经有很强的外围能力：

```text
CSV 读取
源选择
url-mode
运行目录
日志
报告
resume
skip-known-failed
```

但这些是“运行编排”能力，不是“内容处理”能力。

并发处理 RSS 源、保证同源顺序、聚合结果、隔离失败，更接近 `content_inbox` 的核心处理能力。

因此决策是：

```text
content_inbox 服务端提供 batch API；
外部脚本调用 batch API，而不是每个脚本自己实现并发。
```

---

### 4.3 第三轮判断：先保守一致，再逐步提速

当前 `process_content()` 内部职责比较集中：

```text
去重
筛选
入库
聚类
更新 item clustering
```

如果第一版就大规模拆分，改动风险较高。

所以采用分阶段策略：

```text
第一版：
- 先抽取单源处理函数；
- 新增 batch API；
- 源级 ThreadPoolExecutor；
- 同源顺序；
- 必要时用全局锁保护 process_content 或全局状态路径。

第二版：
- 把 process_content 拆成 prepare_candidate 和 commit_candidate；
- AI 筛选、embedding 放到锁外；
- dedupe、insert、cluster commit 放到锁内；
- 提升并发收益。
```

这个过程更符合当前项目节奏。

---

## 5. 最终决策结果

### 5.1 采用的方案

采用：

```text
content_inbox 原生 batch API + 源级并发 + 同源串行 + 全局状态受控提交
```

具体是：

```text
新增 POST /api/rss/analyze-batch
新增 RSSBatchAnalyzeRequest
新增 RSSSourceSpec
新增 RSSBatchRunner
抽取 analyze_one_rss_source
保留 POST /api/rss/analyze
保留 run_rss_sources_to_content_inbox.py
```

---

### 5.2 并发规则

最终规则：

```text
不同 RSS 源之间可以并发。
同一个 RSS 源内部不能并发。
同一个 RSS 源内部按 published_at 从旧到新处理。
如果没有 published_at，则保持原始顺序。
```

默认并发数：

```text
max_concurrent_sources = 3
```

建议上限：

```text
max_concurrent_sources <= 5
```

---

### 5.3 状态一致性规则

全局状态包括：

```text
dedupe_key
inbox_items
event_clusters
cluster vector
cluster item_count
item clustering_json
```

这些状态必须受控。

第一版可以使用保守锁。

后续优化方向是两段式：

```text
prepare_candidate：可并发
commit_candidate：受控提交
```

提交阶段必须至少包含：

```text
二次 dedupe check
insert item
search active clusters
create/update cluster
update item clustering
```

---

### 5.4 API 返回规则

batch API 必须返回：

```text
batch 总览统计
source_results
每个源的 success / partial_failed / failed 状态
每个源的 error 信息
每个源的 item 统计
```

返回顺序：

```text
source_results 按输入 sources 顺序返回，而不是按完成时间返回。
```

---

### 5.5 脚本职责调整

`run_rss_sources_to_content_inbox.py` 后续不再承担核心并发。

它保留：

```text
读取源清单
选择本次运行的源
处理 url-mode
dry-run
resume
skip-known-failed
保存 selected_sources.csv
保存 source_results.csv
保存 report.md
```

它逐步从：

```text
for source:
    POST /api/rss/analyze
```

改为：

```text
POST /api/rss/analyze-batch
```

---

## 6. 预期收益

### 6.1 吞吐提升

多个源可以同时处理。

尤其是 RSSHub、外部网络、模型 API 存在等待时间时，源级并发可以明显减少总运行时间。

---

### 6.2 语义稳定

同源内容不被打乱。

有利于：

```text
事件演化判断
增量判断
同源上下文维护
后续个性化主题判断
```

---

### 6.3 架构清晰

职责变成：

```text
content_inbox：内容处理、源级并发、去重、聚类、入库
run script：选择源、调用 API、保存运行报告
```

---

### 6.4 失败更可解释

batch 返回 `source_results`，每个源都有独立状态。

可以清楚区分：

```text
源失败
条目失败
模型失败
RSS 解析失败
网络失败
```

---

## 7. 风险和缓解

### 7.1 风险：SQLite 写入竞争

缓解：

```text
第一版使用全局锁保护全局状态路径；
必要时保持 max_concurrent_sources 默认 3；
不要默认开大并发。
```

---

### 7.2 风险：重复 cluster

缓解：

```text
cluster search/create/update 放在受控提交区；
提交阶段做最终 cluster 判断；
后续补 cluster 并发安全测试。
```

---

### 7.3 风险：性能提升不明显

如果第一版直接锁住整个 `process_content()`，AI 筛选和 embedding 也会被串行化。

缓解：

```text
第一版先保证正确性；
第二版拆 prepare_candidate / commit_candidate；
把 AI 和 embedding 放到锁外；
只锁 dedupe、insert、cluster commit。
```

---

### 7.4 风险：batch 响应过大

如果每个源、每个条目都返回完整 item，响应会很大。

缓解：

```text
增加 include_items 参数；
默认可以 true，后续大规模运行时设为 false；
source_results 中始终保留统计数据。
```

---

## 8. 后续演进

### 8.1 短期

```text
实现 /api/rss/analyze-batch
补基础测试
更新 README
让脚本可选调用 batch API
```

### 8.2 中期

```text
拆分 process_content
引入 prepare_candidate / commit_candidate
减少锁范围
增加 source-local context
更好地处理同源增量关系
```

### 8.3 长期

```text
引入轻量任务队列或后台调度
支持定时运行
支持源优先级和限流策略
支持更复杂的事件合并和 cluster 修复
支持 Web UI 查看 batch run
```

---

## 9. 最终结论

本次决策选择的是一条中间路线：

```text
不继续把并发留在外部脚本；
也不引入重型任务队列；
不做条目级全局并发；
而是在 content_inbox 内部实现源级并发 batch API。
```

最终原则：

> 把并发放在“源”这一层，把顺序保留在“条目”这一层，把一致性收束在“去重、入库、聚类”这一层。
