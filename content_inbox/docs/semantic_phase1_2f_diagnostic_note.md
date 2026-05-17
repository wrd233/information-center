# Phase 1.2f Diagnostic Note

Scope inspected: `content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_2e_full_300_c5_20260517_152936/`.

## Why Phase 1.2e Hotspots Were Too Broad

The largest hotspot was `agent`, with 90 items, 54 sources, and a 358 day time window. Other selected keys included `api`, `research`, `claude`, `pricing`, `released`, `always`, `add`, `ago`, `by:api`, and `byapi`. These are topic, template, or fallback tokens rather than event signatures. Several groups had time windows measured in months, so the group key was acting as a broad topical bucket instead of a same-event selector.

## Generic Tokens Over-Triggered Candidates

The over-triggering terms were mostly generic AI and social/RSS boilerplate:

- AI/topic terms: `agent`, `agents`, `api`, `model`, `models`, `research`, `paper`, `benchmark`, `release`, `update`, `launch`, `preview`, `gpt`, `llm`, `github`.
- Template terms: `learn`, `more`, `powered`, `view`, `twitter`, `tweet`, `support`, `video`, `browser`.
- Filler terms that reached weighted scoring in Phase 1.2e examples: `like`, `just`, `been`, `free`, `list`, `always`, `add`, `ago`.

These terms promoted pairs such as unrelated `Learn more: <url>` posts and close-time generic social posts into `must_run` or `high`.

## Why The Multi-Item Cluster Was Suspect

The only meaningful multi-item path was rooted in broad hotspot evidence such as `agent` rather than a concrete actor/product/action/time signature. Phase 1.2e cluster eligibility included relations where the same-event proof was weak: same conference, same product family, or same generic agent/API wording. That makes the cluster likely a topic-level merge rather than a validated same-event cluster.

## Over-Broad `related_with_new_info` Examples

- Quora mission posts: likely near-duplicate or low-increment repeat, not strong `related_with_new_info` unless a concrete additional fact is required.
- AI Dev 26 Oracle booth vs workshop: same conference/thread, not necessarily same event.
- GPT-Realtime-2 standup tickets vs Reachy mini: same product/model context but different application angles; should be lower-confidence same-thread/product context unless tied to the exact announcement.

## High-Priority Budget Skip Concentration

The 1.2e evidence shows high/must-run inflation caused by generic overlap and template similarity, not only an insufficient budget. Examples include unrelated close-time posts, `Learn more` boilerplate, and same-product/different-event Perplexity posts. The budget was therefore spent adjudicating many weak candidates, while plausible event-level candidates were skipped later.

## Phase 1.2f Quality Changes

- Generate event-signature hotspots from actor/entity, product/model/project, action type, and date bucket.
- Treat generic AI and template tokens as weak supporting evidence only.
- Recalibrate priority so `must_run/high` require deterministic duplicate evidence or concrete event evidence.
- Preserve middle-state evidence with secondary roles such as `same_product_different_event`, `same_thread`, `same_conference`, `same_template`, `generic_topic_overlap`, and `weak_context`.
- Make `related_with_new_info` same-event-only and non-clusterable when evidence is same-product/thread/topic.
- Harden cluster attachment/seeding and export seed accept/reject diagnostics.
- Add budget skip tiers by stage, priority, and quality tier.
- Add item-card split retry metrics for batch JSON failures.
