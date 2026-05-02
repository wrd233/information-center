# 打分过滤与事件聚类参数说明

配置文件：`config/content_inbox.yaml`

## LLM 配置

`llm.provider`

- 默认值：`deepseek`
- 含义：结构化打分和增量摘要使用的模型服务标识。
- 调整位置：`llm.provider`
- 什么时候改：接入其他 OpenAI-compatible 服务时改。
- 影响：只影响可读标识，真实调用由 `base_url`、`model` 和 `api_key_env` 决定。

`llm.base_url`

- 默认值：`https://api.deepseek.com`
- 含义：Chat Completions API 地址。
- 调高/调低：不适用。
- 什么时候改：使用自建网关、代理、中转站或其他模型服务时。
- 影响：错误地址会导致打分失败，内容会进入 `review/manual_review`。

`llm.model`

- 默认值：`deepseek-v4-flash`
- 含义：打分过滤和增量摘要模型。
- 什么时候调强：分类不稳定、JSON 错误多、需要更细的 hidden_signals。
- 什么时候调轻：成本敏感、RSS 量大、只需要粗筛。
- 可替换：DeepSeek 其他 chat 模型，或任何支持 OpenAI-compatible Chat Completions 和 JSON object 输出的模型。

`llm.temperature`

- 默认值：`0.2`
- 含义：输出随机性。
- 调高：希望分类和 hidden_signals 更发散。
- 调低：希望结果更稳定、可复盘。
- 影响：过高可能导致 JSON 不稳定或建议动作摇摆。

`llm.max_tokens`

- 默认值：`1200`
- 含义：模型输出 token 上限。
- 调高：hidden_signals、reason 或 incremental_summary 经常被截断。
- 调低：控制成本和延迟。
- 影响：过低会增加 schema 校验失败。

`llm.prompt_version`

- 默认值：`screening_v1`
- 含义：写入 screening 结果，方便复盘不同提示词版本。
- 什么时候改：调整系统提示词、字段解释或评分口径后。

## Screening 配置

`screening.enabled`

- 默认值：`true`
- 含义：是否启用模型打分。
- 关闭后：内容保存为 `review/manual_review`，`screening_status=skipped`。

`screening.max_input_chars`

- 默认值：`4000`
- 含义：传给 LLM 的正文片段最大长度。
- 调高：摘要不足、长文需要更多上下文。
- 调低：降低成本、避免 RSS 噪声正文污染判断。
- 影响：过低可能漏掉关键细节，过高会增加延迟和成本。

`screening.categories`

- 默认值：AI前沿、AI工具、信息管理、技术学习、工程实践、社会观察、人生经验、商业产品、娱乐内容、新闻资讯、低质营销、其他。
- 含义：建议模型优先使用的粗分类。
- 什么时候改：信息源结构发生变化，或需要更贴近自己的阅读分组。
- 影响：分类越细，模型越容易摇摆；分类越粗，后续统计颗粒度越低。

## Score Policy

`score_policy.ignore_below_value_score`

- 默认值：`2`
- 含义：内容价值小于等于该值时强制 `ignore`。
- 调高：想更激进过滤低价值内容。
- 调低：担心错过小众但有用的信息。
- 影响：调高会减少 inbox 噪声，但可能漏掉长尾内容。

`score_policy.read_min_value_score`

- 默认值：`4`
- 含义：达到该价值分且相关度达标时可升级为 `read`。
- 调高：只保留最值得读的内容。
- 调低：希望 inbox 更宽松。

`score_policy.read_min_personal_relevance`

- 默认值：`3`
- 含义：进入 `read` 的最低个人相关度。
- 调高：让 inbox 更贴近当前项目。
- 调低：保留更多泛知识内容。

`score_policy.save_min_value_score`

- 默认值：`4`
- 含义：进入 `save/archive` 的最低价值分。
- 调高：减少归档候选。
- 调低：扩大素材库。

`score_policy.save_min_personal_relevance`

- 默认值：`4`
- 含义：进入 `save/archive` 的最低相关度。
- 调高：只收藏强相关内容。
- 调低：收藏更多未来可能有用的内容。

`score_policy.transcribe_min_value_score`

- 默认值：`4`
- 含义：音视频建议转录的最低价值分。
- 调高：节省转录成本。
- 调低：更积极保留音视频材料。

`score_policy.transcribe_min_personal_relevance`

- 默认值：`3`
- 含义：音视频建议转录的最低相关度。
- 调高：只转录强相关内容。
- 调低：允许更多探索性音视频进入后续流程。

`score_policy.manual_review_confidence_below`

- 默认值：`0.6`
- 含义：模型置信度低于该值时强制 `review/manual_review`。
- 调高：更保守，更多内容交给人工复核。
- 调低：更信任模型自动判断。
- 影响：调高会增加复核量，调低会增加误判风险。

## Embedding 配置

`embedding.enabled`

- 默认值：`true`
- 含义：是否启用事件聚类所需的 embedding。
- 关闭后：聚类不执行，内容不会进入事件簇。

`embedding.provider`

- 默认值：`yunwu`
- 含义：embedding 服务标识。
- 可替换：OpenAI、Azure OpenAI、自建 bge/m3e 服务、其他 OpenAI-compatible 中转站。

`embedding.base_url`

- 默认值：`https://yunwu.apifox.cn/v1`
- 含义：OpenAI-compatible Embeddings API 地址。
- 什么时候改：切换中转站或自建 embedding 服务。

`embedding.model`

- 默认值：`text-embedding-3-small`
- 含义：生成事件向量的模型。
- 调强：事件聚类误判多、跨语言语义匹配差。
- 调轻：成本敏感、内容量大。
- 可替换：`text-embedding-3-large`、bge-m3、jina embeddings 等，但要同步调整 `dimensions`。

`embedding.dimensions`

- 默认值：`1536`
- 含义：sqlite-vec 虚拟表向量维度。
- 什么时候改：更换 embedding 模型时。
- 影响：维度不匹配会导致向量写入失败；已有 vec 表通常需要重建。

`embedding.max_input_chars`

- 默认值：`3000`
- 含义：embedding_text 最大长度。
- 调高：事件描述需要更多上下文。
- 调低：减少噪声，让向量更聚焦事件。

## Clustering 配置

`clustering.enabled`

- 默认值：`true`
- 含义：是否启用事件聚类。

`clustering.top_k`

- 默认值：`5`
- 含义：检索最相似 active event_clusters 的数量。
- 调高：事件簇多、担心错过候选。
- 调低：减少检索成本。

`clustering.new_event_threshold`

- 默认值：`0.85`
- 含义：最高相似度低于该值时视为新事件。
- 调高：更容易创建新事件簇。
- 调低：更容易合并到旧事件。
- 影响：调高会增加簇数量，调低可能误合并。

`clustering.duplicate_threshold`

- 默认值：`0.97`
- 含义：达到该相似度并且实体高度重合时视为重复。
- 调高：更谨慎静默。
- 调低：更积极静默重复内容。
- 影响：调低可能误杀高相似但有新增信息的内容。

`clustering.high_overlap_entity_ratio`

- 默认值：`0.6`
- 含义：判定重复时要求的实体重合比例。
- 调高：减少误判重复。
- 调低：更容易把同主题内容视为重复。

`clustering.cluster_min_value_score`

- 默认值：`3`
- 含义：进入聚类的最低 value_score。
- 调高：节省 embedding 成本，减少噪声簇。
- 调低：让更多低价值内容也参与降噪。

`clustering.cluster_min_personal_relevance`

- 默认值：`3`
- 含义：进入聚类的最低 personal_relevance。
- 调高：只为强相关内容建事件簇。
- 调低：为更多泛内容建立历史上下文。

`clustering.cluster_vector_strategy`

- 默认值：`summary_embedding`
- 当前实现：新事件使用首条 item 向量；增量更新时默认用新 item 向量刷新簇向量，`average_items` 会做均值，`representative_item` 不更新。
- 可选值：`representative_item`、`summary_embedding`、`average_items`。
- 什么时候选 representative_item：希望事件簇稳定，不被后续边缘内容拖偏。
- 什么时候选 average_items：希望簇向量代表多篇内容的平均主题。
- 什么时候选 summary_embedding：希望簇向量跟随事件摘要演进。

`clustering.archive_after_days`

- 默认值：`7`
- 含义：active cluster 连续多少天无更新后归档。
- 调高：长期事件持续参与匹配。
- 调低：热点生命周期短，避免旧事件干扰新事件。

## Notification 配置

`notification.full_push_for_new_event`

- 默认值：`true`
- 含义：高价值新事件默认完整推送决策。
- 当前项目只产出 `notification_decision`，不实现推送。

`notification.incremental_push_when_has_new_info`

- 默认值：`true`
- 含义：有新增信息时标记 `incremental_push`。

`notification.silent_duplicates`

- 默认值：`true`
- 含义：高度重复内容标记 `silent`。

`notification.include_silent_in_default_inbox`

- 默认值：`false`
- 含义：`GET /api/inbox` 默认是否包含 silent 内容。
- 调高为 true：调试聚类时更容易看到所有结果。
- 保持 false：日常 inbox 更清爽。

`notification.manual_review_when_uncertain`

- 默认值：`true`
- 含义：高相似但实体不重合时是否进入人工复核。
- 调低为 false：会更积极当作增量更新。
- 影响：false 会减少复核量，但增加误合并风险。

## 技术选型替换

Embedding provider 可以替换为任何 OpenAI-compatible `/embeddings` 服务。更换时同步调整：

- `embedding.base_url`
- `embedding.api_key_env`
- `embedding.model`
- `embedding.dimensions`

向量存储当前使用 SQLite + sqlite-vec。优势是部署简单、数据随本地 SQLite 走。未来可替换为：

- Qdrant：适合更大量 item 和更强过滤条件。
- LanceDB：适合本地文件型向量库。
- Postgres + pgvector：适合已有 Postgres 基础设施。

阈值策略可从固定阈值改为：

- 按来源类型分阈值：新闻源更高，个人博客更低。
- 按 category 分阈值：AI前沿更高频聚类，人生经验更少聚类。
- 按时间衰减：旧 cluster 相似度要求更高。

这些替换会影响成本、可解释性和误判模式。当前版本优先保持本地、简单、可复盘。
