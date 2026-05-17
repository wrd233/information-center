# Phase 1.3c Chinese Trigger Recommendations

## Current Coverage Assessment

- **发布/发布了/刚刚发布/正式发布**: FOUND (hits: 5) → mapped_action: release
- **推出/上线/开放/开源/释出**: FOUND (hits: 3) → mapped_action: release
- **支持/接入/打通/集成/连接/对接**: FOUND (hits: 3) → mapped_action: integration
- **技术预览/预览版/内测/公测/候补/waitlist**: FOUND (hits: 1) → mapped_action: availability
- **套餐/免费/降价/价格/1块钱/元/折扣/优惠**: FOUND (hits: 3) → mapped_action: pricing
- **超过/超越/领先/采用率/市场份额/市值/用户数/增长**: FOUND (hits: 2) → mapped_action: adoption_metric
- **官宣/新公司/联合创始人/创业/成立/融资**: FOUND (hits: 7) → mapped_action: company_launch
- **大会/活动/直播/研讨会/峰会/报名**: FOUND (hits: 1) → mapped_action: event
- **漏洞/安全/修复/补丁**: FOUND (hits: 2) → mapped_action: security
- **评测/跑分/榜单/基准/准确率**: FOUND (hits: 2) → mapped_action: benchmark

## Recommended New/Enhanced Triggers

Based on the false negative analysis, these triggers should be added or enhanced:

### High Priority (causing false negatives)

| Trigger | Mapped Action | Should Imply | Risk | Confidence | Force LLM? |
|---|---|---|---|---|---|

### Missing Trigger Assessment


## Root Cause Analysis

The Chinese detection rate of 0.3846 is caused by:

1. **Missing trigger coverage**: Several Chinese event trigger groups have zero hits, meaning the deterministic extractor cannot detect these event types.
2. **Weak entity extraction**: Many Chinese items have valid products/actors in their text but the entity extractor fails to identify them from the item cards.
3. **Validator over-rejection**: Some Chinese items with valid event signals are rejected due to `missing_concrete_actor_or_product` or `weak_action_without_entity`.
4. **LLM fallback not invoked**: Chinese event-like items that fail deterministic extraction don't get LLM-backed signature passes.
5. **Card summary quality**: Deterministic minimal cards for Chinese items often miss key entities.

