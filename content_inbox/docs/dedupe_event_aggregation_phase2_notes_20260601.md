# Phase 2 去重与事件聚合实施记录

Status: historical implementation note. Use `event_aggregation_operational_v3.md` for current checkpoint policy and active targets.

生成日期: 2026-06-01

## 目标

本轮目标是 `Recall Hardening Without Precision Regression`：在不恢复标题分组、不让 medium 自动合并、不让非事件自动建 event 的前提下，提高 item dedupe 与 same-event 聚合召回。

## 本轮实现

- URL canonicalization 更保守也更完整：
  - HTTP/HTTPS 归一为 `https`。
  - `www.` 归一。
  - trailing slash、fragment 归一。
  - 移除 `utm_*`、`fbclid`、`gclid`、`igshid`、`mc_cid`、`mc_eid`、`ref`、`spm` 等 tracking 参数。
  - 保留 `id`、`page` 等业务 query 参数，避免动态页误合并。
- Dedupe explanation 增加 canonical URL variants，方便解释 tracking/scheme/www 归一。
- Signature alias registry 增强：
  - `config/event_aliases.json` 继续作为 actor/product/action alias 配置。
  - `EventSignature` 新增 `alias_hits`，记录 alias -> canonical 命中。
  - signature/evidence payload 会保留 alias 命中信息，支持回放和解释。
- Candidate recall lane 增强：
  - 新增 `exact_signature_alias` lane。
  - alias 归一后的 exact signature 可进入 `must_run`，但仍必须先通过 eventness gate 和 hard negative。
  - candidate features 会记录 `alias_normalized_signature_match`。
- Evaluation 升级：
  - `scripts/evaluate_ops_quality.py` 输出 auto-merge precision、medium review rate、alias hit count、candidate counts by lane/status/priority、disqualifier counts。

## 保持不变的安全边界

- 非事件不自动创建 event。
- `normalized_title(title)` 没有恢复为 event key。
- `medium` / `uncertain` 不自动 merge。
- hard negative 仍压制 digest、generic、low-signal、wide time window、topic-only overlap。
- legacy cluster/event 不被覆盖；新写入继续使用 `created_by=operational_v2_rule`、`schema_version=operational_v2`、run evidence、input fingerprint。
- LLM relation path 本轮未默认开启，避免无 API key 或非结构化输出影响稳定性。

## 未做或降级

- 没有接入真实 LLM relation decision。
- 没有做 review apply 完整闭环。
- 没有做 legacy cluster 全量迁移。
- 没有改 briefing/report 模板。
- 没有对默认大库执行真实写入。

## 主要取舍

本轮优先把 dedupe 召回补到门槛以上，并通过 alias exact signature 小幅提升 same-event recall。对于更激进的跨语言/标题改写召回，本轮没有把 medium candidate 自动升为 merge，而是继续进入 review，避免 precision 回退。
