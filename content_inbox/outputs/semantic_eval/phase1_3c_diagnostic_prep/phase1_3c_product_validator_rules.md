# Phase 1.3c Product Validator Rules

## Product/Model Validation Rules

### PV-001: reject_short_random_alphanumeric
- **Severity**: blocker
- **Pattern**: `^[a-z0-9]{6,10}$`
- **Description**: Reject product if it is a short random alphanumeric token (e.g., sow0e7ym, iobqd8a9, ay4dy8o5)
- **Examples from 300-run**: `sow0e7ym`, `iobqd8a9`, `ay4dy8o5`, `CERX3N35`, `ns123abc`, `trq212`, `DeYA2K`, `Yeuoly1`
- **Field**: product_or_model

### PV-002: reject_month_day_phrase
- **Severity**: blocker
- **Pattern**: `^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(st|nd|rd|th)?$`
- **Description**: Reject product if it is a month+day phrase (e.g., May 4th, June 4th)
- **Examples from 300-run**: `May 4th`, `June 4th`
- **Field**: product_or_model

### PV-003: reject_pure_number_product
- **Severity**: blocker
- **Pattern**: `^[\d,]+\s*(million|billion|trillion|k|%|percent)?$|^(a\s+|an\s+)?\d+[\d\s,.-]*\w*$`
- **Description**: Reject product if it is a pure number or numeric phrase (e.g., around 1897, of 12M, a 24, up 130)
- **Examples from 300-run**: `around 1897`, `of 12M`, `a 24`, `up 130`, `to 100x`, `to 55`, `of 1`, `a 0`, `a 48-hour`, `crossed 4`, `top 12`, `top 10`, `under 35`, `up 80`
- **Field**: product_or_model

### PV-004: reject_date_fragment_product
- **Severity**: blocker
- **Pattern**: `(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+`
- **Description**: Reject product if it contains date-like fragments
- **Examples from 300-run**: `since 2018`
- **Field**: product_or_model

### PV-005: reject_weak_preposition_start_product
- **Severity**: warning
- **Pattern**: `^(for|with|from|every|just|and|or|in|on|to|of|as|by|the|a|an|that|this|its|our|your|their)\s`
- **Description**: Reject product if it starts with weak preposition/determiner unless in known product list
- **Exceptions**: `Notion Developer Platform`, `Notion Custom Agents`
- **Field**: product_or_model

### PV-006: reject_verb_phrase_product
- **Severity**: warning
- **Pattern**: `^(build|create|make|use|get|run|try|learn|see|find|give|take|send|launch|release|announce|introduce|ship|add|fix|update|upgrade|improve|integrate|support|meet)\s`
- **Description**: Reject product if it starts with a verb (looks like a sentence fragment, not a product name)
- **Examples from 300-run**: `Give Your Chat Agent`, `Meet Replit Parallel Agents`, `Try Parallel Agents`
- **Field**: product_or_model

### PV-007: reject_long_phrase_product
- **Severity**: warning
- **Pattern**: `^\w+(\s+\w+){6,}$`
- **Description**: Reject product if longer than 6 words and not a known valid product
- **Examples from 300-run**: `data then skip the interface entirely Agents`, `everything when you build products for Finance`
- **Field**: product_or_model

### PV-008: reject_sentence_fragment_product
- **Severity**: warning
- **Pattern**: `[.!?;,].*\s+\w+\s+\w+`
- **Description**: Reject product if contains sentence punctuation in a multi-word phrase
- **Examples from 300-run**: `CI failures. Set up always-on agents`, `just built issue was the initial characters`
- **Field**: product_or_model

### PV-009: reject_generic_for_every_product
- **Severity**: blocker
- **Pattern**: `for\s+every|for\s+your|for\s+all`
- **Description**: Reject product containing 'for every/your/all' pattern — these are descriptive phrases not products
- **Examples from 300-run**: `Git semantics for every file your agent`
- **Field**: product_or_model

### PV-010: reject_url_fragment_product
- **Severity**: blocker
- **Pattern**: `https?://|t\.co/|\.com|\.org|\.io|\.dev|\.ai\b`
- **Description**: Reject product if it contains URL fragments
- **Examples from 300-run**: `com 1Dl`
- **Field**: product_or_model

## Actor Validation Rules

### AV-001: former_employer_is_not_actor
- **Severity**: warning
- **Description**: Former employer mentioned in context (e.g., '前 Meta FAIR Director') is not the actor. The actor is the person or new company.
- **Examples**: Meta mentioned as former employer, actor should be 田渊栋 or Recursive

### AV-002: product_is_not_organization_actor
- **Severity**: warning
- **Description**: Product/model name (e.g., GPT-5.5, Gemini) should not be used as actor unless the source is the official product account.
- **Examples**: GPT-5.5 as actor → should be OpenAI, Gemini as actor → should be Google

### AV-003: source_account_as_actor_only_if_official
- **Severity**: info
- **Description**: Social media account name can be actor only if it's the official source making an announcement about itself.

### AV-004: prefer_empty_actor_over_wrong_actor
- **Severity**: blocker
- **Description**: Leave actor empty rather than populating it with a wrong organization/product name.
- **Examples**: arxiv as actor for pricing → wrong, should be empty

