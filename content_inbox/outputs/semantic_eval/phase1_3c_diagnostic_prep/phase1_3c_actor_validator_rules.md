# Phase 1.3c Actor Validator Rules

## Current Actor Extraction Issues

Based on the 300-run evidence, actor extraction has these issues:

- **item_4b1ececba3bb49348fbcc789e5ddffe6**: actor=`google` — random_alphanumeric_token
- **item_423819d009fe4f0da14949d06b8e720d**: actor=`cursor` — random_alphanumeric_token
- **item_92a9e82e74654bf695b05644aed07005**: actor=`llamaindex` — random_alphanumeric_token
- **item_d595ccdff9a8456b98935755e83b253d**: actor=`firecrawl` — random_alphanumeric_token
- **item_614f1ae12cf34cfb8ef9e40013180259**: actor=`cursor` — random_alphanumeric_token
- **item_5c72b7f0be8f43d2a275c1e7f48d2c61**: actor=`elevenlabs` — random_alphanumeric_token
- **item_5af5b0c651eb4d6dbe3a4173312d28b8**: actor=`nvidia` — random_alphanumeric_token
- **item_e22aa290a8f74b5a88f75179e33a69b0**: actor=`notion` — random_alphanumeric_token
- **item_a8fe82c191a0491aa4f3a7d493ae6a22**: actor=`lovable` — random_alphanumeric_token
- **item_1b7d128007e744d7a6b0fcdcaaea4015**: actor=`replit` — random_alphanumeric_token
- **item_af0866973f4f4d34b1199f81580190cb**: actor=`openai` — random_alphanumeric_token
- **item_0ac7d3f53d6b497d81181a0f24f636d7**: actor=`anthropic` — random_alphanumeric_token
- **item_3a2d72eb9cb14b69a58fcfc130eeec29**: actor=`vercel` — random_alphanumeric_token

## Actor Validation Rules

### AV-001: former_employer_is_not_actor
- **Severity**: warning
- **Former employer mentioned in context (e.g., '前 Meta FAIR Director') is not the actor. The actor is the person or new company.**
  - Meta mentioned as former employer, actor should be 田渊栋 or Recursive

### AV-002: product_is_not_organization_actor
- **Severity**: warning
- **Product/model name (e.g., GPT-5.5, Gemini) should not be used as actor unless the source is the official product account.**
  - GPT-5.5 as actor → should be OpenAI
  - Gemini as actor → should be Google

### AV-003: source_account_as_actor_only_if_official
- **Severity**: info
- **Social media account name can be actor only if it's the official source making an announcement about itself.**

### AV-004: prefer_empty_actor_over_wrong_actor
- **Severity**: blocker
- **Leave actor empty rather than populating it with a wrong organization/product name.**
  - arxiv as actor for pricing → wrong, should be empty


## Recommendations

1. Never use a social media username/handle as actor unless verified as official source
2. Never use a product/model name as the actor — always use the organization
3. Cross-check actor against source_name — if the source is a personal account tweeting about a company, the company is the actor
4. Prefer empty actor over incorrect actor — missing actor is better than wrong attribution
5. For Chinese items, allow person names as actors when they are making official announcements
