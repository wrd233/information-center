# Operational v3 Real-Use Smoke Report

Generated at: 2026-06-01T03:28:35.540823+00:00

## Scope

- source_db_path: `/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3`
- evaluation_db_path: `/tmp/claude-501/content_inbox_real_use_smoke_k6n2hbx4.sqlite3`
- dry_run: `True`
- write_real_db: `False`
- sample_mode: `event_hotspots`
- limit: `40`
- source_filter: `None`
- source_url_prefix: `None`
- source item/source scope: `{'item_count': 3278, 'source_count': 469, 'latest_item_time': '2026-05-28T15:29:11+00:00'}`

## Pipeline

- sampled_items: 40
- dedupe: `{'dedupe_groups_created_or_updated': 40, 'seen_count_gt_1_items': 0, 'dedupe_explanation_count': 0, 'dedupe_explanation_coverage': 1.0, 'schema_version': 'operational_v3'}`
- item_cards: `{'selected': 40, 'written': 40, 'llm_calls': 0, 'skipped': 0, 'errors': 0, 'dry_run': False, 'card_tiers': {'minimal': 24, 'full': 1, 'standard': 15}, 'local_minimal_cards': 24, 'deterministic_minimal_cards': 24, 'heuristic_fallback_count': 16, 'parse_error_fallback_count': 0, 'budget_skip_fallback_count': 0, 'failed_batch_count': 4, 'split_retry_success_count': 0, 'single_retry_success_count': 0}`
- information_objects: `{'item_count': 40, 'schema_version': 'operational_v3', 'created_by': 'operational_v3_rule', 'eventness': {'content': 1, 'unknown': 20, 'thread': 8, 'event': 10, 'low_signal': 1}, 'signature': {'event_signature': 11, 'thread_signature': 9, 'content_signature': 0, 'reject': 20, 'invalid': 29}, 'candidates_by_priority': {'low': 29, 'suppress': 12, 'must_run': 1, 'high': 3}, 'candidates_by_lane': {'same_thread': 8, 'exploratory_recall': 21, 'suppressed': 12, 'exact_signature_alias': 1, 'same_source_repeat': 3}, 'disqualifiers_by_reason': {'wide_time_window': 25}, 'alias_hit_count': 58, 'auto_merged': 4, 'review_required': 10, 'rejected_non_event': 30, 'clusters_created_or_updated': 7, 'events_created_or_updated': 7, 'llm_calls': 0}`

## Candidate And Review Trace

- candidate_pair_count: 45
- by_priority: `{'low': 29, 'suppress': 12, 'must_run': 1, 'high': 3}`
- by_lane: `{'same_thread': 8, 'exploratory_recall': 21, 'suppressed': 12, 'exact_signature_alias': 1, 'same_source_repeat': 3}`
- by_status: `{'rejected': 36, 'auto_merge': 4, 'review': 5}`
- pending_review_count: 68

## Cluster Audit

- cluster_count: 7
- multi_item_cluster_count: 2
- ready_event_count: 7
- cluster_item_relations: `{'same_event_repeat': 3, 'source_material': 7}`

## Top Clusters

- OpenAI/Codex integration Codex | items=3 | status=active | members=With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigati...; Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...; If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...
- Anthropic event Claude | items=2 | status=active | members=experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @an...; I'm at the Claude w/ Code event in San Francisco, and I'll be live blogging the keynote here https:/...
- Anthropic adoption metric Claude | items=1 | status=needs_review | members=5/一种复利的技术债，没人提醒你 Anthropic提出：Agentic Technical Debt 传统技术债线性增长 AI技术债是复利——每个session健忘，每次重新推导架构，结果都不一...
- Anthropic company launch Claude Code | items=1 | status=needs_review | members=3/2026最大创业陷阱 Anthropic引了个数据：42%的创业失败因为做了没人要的东西。AI之前的数字。他们说这个比例只会继续往上走 为什么？ 过去做prototype要几个月——这本身就...
- Notion release Notion Developer Platform | items=1 | status=needs_review | members=The Notion command-line interface (CLI) is a new way to work with Notion programmatically, made just...
- OpenAI event SF 2026 | items=1 | status=needs_review | members=GenAI Summit SF 2026：湾区数万人大会！ 🔗 Will粉丝专属购票链接（可享受15%优惠）： 专属Code：WILL 专属链接： Luma：https://t.co/OoGPFp...
- OpenAI/Codex feature update codex | items=1 | status=needs_review | members=源：https://t.co/O7NnTsIIPF

## Daily Briefing Preview

```markdown
# 每日简报 2026-06-01

## 可信事件
- OpenAI/Codex integration Codex（可信事件，置信度 0.98）
- Anthropic event Claude（可信事件，置信度 0.98）
- Anthropic company launch Claude Code（可信事件，置信度 0.98）
- OpenAI event SF 2026（可信事件，置信度 0.98）
- OpenAI/Codex feature update codex（可信事件，置信度 0.98）
- Anthropic adoption metric Claude（可信事件，置信度 0.98）
- Notion release Notion Developer Platform（可信事件，置信度 0.98）

## 待审核
- eventness_review item:item_0513431281ed4b1c8dc89127100648d9
- eventness_review item:item_121fb943b0f24e3bba309474b8d35c76
- eventness_review item:item_193356763044416597c6a5ef0557bf49
- eventness_review item:item_194e2990d69843398e4ad24814bebef1
- eventness_review item:item_19f0f96015c949f6b82290e72412ea1a
- eventness_review item:item_1da7d26c653d494a9c1c099de5c15f40
- eventness_review item:item_260c0406b6dd4fda9b9a8ac4a4da918c
- eventness_review item:item_291caeefffc847638ac30a08cd3230a8
- eventness_review item:item_29fd642dc61747229ddaadc26d83b95d
- eventness_review item:item_413261cbb0004698b99a3410613efa7d
```

## Run Report Preview

```markdown
# 运行报告

生成时间: 2026-06-01T03:27:07.419801+00:00

关联对象: run real_use_smoke_36e57ad0ddad

## 可信事件
- OpenAI/Codex integration Codex：integration，置信度 0.98，cluster cluster_b063616c10239614
- Anthropic event Claude：event，置信度 0.98，cluster cluster_601081733adc458c
- Anthropic company launch Claude Code：company_launch，置信度 0.98，cluster cluster_385b1d130279f8ae
- OpenAI event SF 2026：event，置信度 0.98，cluster cluster_81069ecd4b34a8b9
- OpenAI/Codex feature update codex：feature_update，置信度 0.98，cluster cluster_65829a0c8c61fb5f
- Anthropic adoption metric Claude：adoption_metric，置信度 0.98，cluster cluster_b2784f076cc5c636
- Notion release Notion Developer Platform：release，置信度 0.98，cluster cluster_e6a84769e4c123d8

## 质量概览
- 可信事件数: 7
- 全部事件数: 7
- 待审核项: 40
- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。

```

## Readiness Notes

- This smoke uses real inbox rows but writes only to a temporary evaluation database.
- Live LLM calls: enabled. Attempted 20, succeeded 20.
- No gold labels are available for this real sample, so FN/FP proof remains qualitative: candidate/review/cluster traces are emitted for manual audit.
- Briefing/report previews consume materialized `events` and `event_clusters`; they do not directly list raw inbox rows.
