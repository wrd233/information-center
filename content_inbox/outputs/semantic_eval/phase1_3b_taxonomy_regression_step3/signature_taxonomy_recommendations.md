# Signature Taxonomy Recommendations — Phase 1.3b Step 3

**Generated**: 2026-05-17
**Source**: 50-row benchmark from Phase 1.3 `api_xgo_ing_phase1_3_round_c_80_live_tuned`
**Purpose**: Stable taxonomy and extraction rules for the next Codex implementation pass

---

## 1. Four-Level Semantic Classification

Every processed item must be assigned exactly one `semantic_level`:

| Level | Count in Benchmark | Can Seed Event Cluster | Can Form Thread | Purpose |
|---|---|---|---|---|
| `event_signature` | 29 | Yes | Yes | Same-event matching, cluster seeds, event timelines |
| `thread_signature` | 8 | No | Yes | Navigation, source profiles, product timelines |
| `content_signature` | 1 | No | No | Search indexing, source profiling |
| `reject` | 12 | No | No | Exclude from semantic processing |

### 1.1 event_signature

**Definition**: A concrete, dated event-like unit. Must have at minimum: a concrete actor or product, a concrete event action (not "other"), and a time context.

**Key properties**:
- Can seed event clusters when matched with same-event items
- Can also form thread relations for navigation
- The most restricted category — false positives here cause over-clustering

**Representative examples**:

| Benchmark ID | What | Why event_signature |
|---|---|---|
| BENCH_1_3b_single_002 | OpenShell v0.0.40 release | Versioned software release with actor (NVIDIA), product+version, and feature list |
| BENCH_1_3b_single_007 | Googlebook release (Chinese) | Product launch with actor (Google), product name, Chinese release language "刚刚发布" |
| BENCH_1_3b_single_024 | Shanghai Telecom Token plan | Chinese pricing event, actor (China Telecom Shanghai), product, pricing action |
| BENCH_1_3b_single_009 | Anthropic adoption data | Adoption metric with actor, concrete data from Ramp AI Index, comparison |
| BENCH_1_3b_pair_039 | Notion CLI + Workers | Same-source coordinated launch, same timestamp, overlapping content |
| BENCH_1_3b_pair_040 | OpenShell v0.0.40 + v0.0.41 | Sequential versioned releases of same product |

### 1.2 thread_signature

**Definition**: A related sequence or topical thread that should NOT directly seed an event cluster.

**Key properties**:
- Can form thread relations for navigation and source profiling
- Must NOT seed event clusters
- Must NOT be folded into event clusters

**Representative examples**:

| Benchmark ID | What | Why thread_signature |
|---|---|---|
| BENCH_1_3b_single_004 | DGX Spark anecdote | Firsthand social anecdote, not a concrete product event |
| BENCH_1_3b_pair_035 | Codex remote vs sandbox | Same product (Codex), different features — thread, not same event |
| BENCH_1_3b_pair_036 | AK paper feed | Same source, same format, different papers — thread only |
| BENCH_1_3b_pair_044 | YC Modern vs YouArt | Same source, same format, different companies — recurring format |
| BENCH_1_3b_pair_045 | Vercel vs Ramp reports | Same company (Anthropic), different data sources — thread-like |
| BENCH_1_3b_cluster_candidate_049 | AK paper thread | Same-source paper feed — should form thread, NOT event cluster |

### 1.3 content_signature

**Definition**: Structured content useful for search, filtering, or source profiling, but not event/thread clustering.

**Representative examples**:

| Benchmark ID | What | Why content_signature |
|---|---|---|
| BENCH_1_3b_single_030 | Translation tool setup | Has concrete product names but no event action. Personal workflow share. |

### 1.4 reject

**Definition**: Low-signal or non-semantic content. No clustering, no threading, no search indexing beyond basic dedupe.

**Representative examples**:

| Benchmark ID | What | Why reject |
|---|---|---|
| BENCH_1_3b_single_017 | "Great advice" | One-phrase engagement bait |
| BENCH_1_3b_single_018 | "Banger" | One-word post |
| BENCH_1_3b_single_022 | "Open > closed" | Three-word social reply |
| BENCH_1_3b_single_006 | "Concerning." | One-word title, 69-char gibberish product |
| BENCH_1_3b_single_019 | Podcast opinion (Chinese) | Philosophical commentary, no event |

---

## 2. Action Taxonomy

### 2.1 Actions with cluster eligibility

These actions can seed event clusters when actor + product + action match:

| Action | English Triggers | Chinese Triggers | Example |
|---|---|---|---|
| `release` | release, launch, ship, now available, introducing | 发布, 推出, 上线, 开源, 释出 | Googlebook, Notion CLI, OpenShell |
| `feature_update` | now supports, can now, new feature, update | 支持, 接入, 新增, 更新 | Codex remote control, Notion Custom Agents |
| `availability` | now available on, waitlist, preview, beta, shipping | 技术预览, 候补, 内测, 公测 | GitHub Copilot Desktop, Stelline Dev Kit |
| `pricing` | free, discount, price, plan, tier, cost | 免费, 降价, 价格, 套餐, 1块钱 | Shanghai Telecom Token, LangSmith Fleet |
| `adoption_metric` | market share, surpassed, revenue, market cap, growth | 采用率, 市场份额, 超过, 市值 | NVIDIA $5.5T, Anthropic enterprise share |
| `integration` | integrate, connect, plugin, SDK, works with | 集成, 接入, 连接, 打通 | QVeris CLI + Claude Code |
| `company_launch` | congrats on the launch, founded, new company | 官宣, 新公司, 联合创始人, 正式成立 | Recursive, PLAN0, Adialante |
| `event` | summit, conference, webinar, meetup, register | 大会, 研讨会, 直播, 活动, 峰会 | AI Security Summit, LangChain Interrupt |
| `security` | vulnerability, CVE, security fix, patch, incident | 漏洞, 安全, 修复 | OpenShell security fixes (secondary action) |
| `technical_blog` | deep dive, how we built, architecture, engineering | 技术博客, 深度, 架构, 实现 | Codex Windows sandbox |

### 2.2 Actions without cluster eligibility (thread or content only)

| Action | Why Not Cluster-Eligible |
|---|---|
| `research_paper` | Different papers are different events. Thread only for same-source paper feeds. |
| `ranking` | Rankings change over time. Thread-like for tracking, not event clustering. |
| `case_study` | Each case study is a different customer story. Thread only. |
| `benchmark` | Benchmarks are evaluations, not product events. Can be content_signature. |
| `partnership` | Each partnership is a different relationship. Cluster only if same partners + same announcement. |
| `tutorial` | Educational, not event-driven. Content_signature only. |
| `opinion_analysis` | Subjective. No clustering. Reject or content_signature. |
| `funding` | Each round is a different event. Cluster only if same company + same round. |

---

## 3. Actor/Product Extraction Rules

### 3.1 Known Failure Modes and Fixes

| Failure Mode | Benchmark Example | Rule |
|---|---|---|
| URL fragment as product | `fkR2wVD129` (BENCH_single_010 paper) | Never allow products that match URL shortener patterns or raw URL path segments |
| Number fragment as product | `for 50`, `just 0.3` (BENCH_single_003, _009) | Never allow products that are purely numeric or numeric-preceded-by-preposition |
| Date as product | `May 14` (BENCH_single_001) | Never allow products that match date patterns (month names, day numbers) |
| Sentence fragment as product | `for updates from my phone. hermes agent` (BENCH_single_004) | Reject products longer than 8 words or containing sentence punctuation |
| Former employer as actor | `Meta` for Recursive launch (BENCH_single_003) | If text says "former X director/employee launches Y", actor=Y, NOT X |
| Integration target as actor | `Claude` for QVeris CLI (BENCH_single_014) | If text says "X integrates with Y" or "X for Y", actor=X maker, NOT Y |
| Product as organization | `Codex` as organization (BENCH_single_013) | Codex, Claude, ChatGPT are products; OpenAI, Anthropic are organizations |
| Version number without product | Various | Always attach version to a named product: "OpenShell v0.0.40", not "v0.0.40" |

### 3.2 Product Name Extraction Priority

1. Named entity in title matching known product pattern (CapitalizedWord + optional version)
2. Explicit product mention: "Introducing X", "X is now available", "Announcing X"
3. Card entities if they contain proper noun phrases (not generic terms)
4. Empty string if no product can be reliably extracted

### 3.3 Actor Extraction Priority

1. Organization making the announcement (from source_name for official accounts)
2. Explicit actor mention: "X announced", "X launched", "X released"
3. Product owner implied by context
4. Empty string if no actor can be reliably determined (prefer empty over wrong)

---

## 4. Accept/Reject Decision Flow

```
1. Does item have title?
   NO  → reject (empty content)
   YES → continue

2. Is title < 4 words AND no named entity?
   YES → reject (too short)
   NO  → continue

3. Does item have a concrete actor OR product?
   NO  → check for content_signature possibility
         Has concrete entities but no event? → content_signature
         Otherwise → reject
   YES → continue

4. Does item have a concrete event action (not "other")?
   NO  → check for thread_signature possibility
         Same source recurring format? → thread_signature
         Same product family mention? → thread_signature
         Otherwise → content_signature or reject
   YES → continue

5. Is the product a valid product (not URL/number/date/sentence fragment)?
   NO  → demote to thread_signature or reject
   YES → continue

6. Is the actor valid (not former employer, not integration target, not product-as-org)?
   NO  → fix actor if possible, otherwise demote confidence
   YES → event_signature
```

---

## 5. Relation Decision Flow

```
1. Are both items' primary content identical?
   YES → near_duplicate, should_fold=True
   NO  → continue

2. Are both items rejected (semantic_level=reject)?
   YES → low_signal (no relation except deterministic duplicate)
   NO  → continue

3. Do items share actor + product + action?
   YES → check if same event:
         Same timestamp/source? → related_with_new_info
         Different features/versions? → related_with_new_info (if same launch) or same_product_different_event
   NO  → continue

4. Do items share actor or product but have different actions?
   YES → same_thread (if same product ecosystem) or same_product_different_event
   NO  → continue

5. Do items share only generic tokens (agent, AI, API, code, cli, data)?
   YES → different (false positive from candidate generation)
   NO  → continue

6. Do items share source + format but different concrete subjects?
   YES → same_thread (recurring format)
   NO  → different
```

---

## 6. Cluster Seed Decision Flow

```
1. Is the candidate pair relation near_duplicate with confidence >= 0.85?
   YES → FOLD (merge items, don't create multi-item cluster)
   NO  → continue

2. Is the candidate pair relation related_with_new_info with confidence >= 0.8?
   YES → Can seed event cluster
   NO  → continue

3. Are items from same source + same timestamp window (< 1 hour) + same concrete launch?
   YES → Can seed event cluster (coordinated launch pattern)
   NO  → continue

4. Are items sequential versioned releases of same product?
   YES → Can seed event cluster (version chain pattern)
   NO  → continue

5. Do items share concrete actor + product + action match?
   YES → Can seed event cluster if cross-source
   NO  → Do not seed event cluster
```

---

## 7. Regression Test Coverage

The 50-row benchmark with semantic levels covers:

- **29 event_signature**: Testing that concrete events are accepted with correct actor/product/action
- **8 thread_signature**: Testing that same-source recurring content forms threads, not clusters
- **1 content_signature**: Testing that useful non-event content is indexed but not clustered
- **12 reject**: Testing that low-signal content is correctly rejected
- **17 relation pairs**: Testing that pair classifications match expectations
- **6 cluster fixtures**: Testing event cluster formation, thread formation, and rejection

### Key regression assertions:

1. `BENCH_1_3b_single_007` (Googlebook): Must be event_signature with action=release despite Chinese text
2. `BENCH_1_3b_single_024` (Shanghai Telecom): Must be event_signature with action=pricing, NOT reject
3. `BENCH_1_3b_single_003` (Recursive): Actor must NOT be "Meta"
4. `BENCH_1_3b_single_014` (QVeris CLI): Actor must NOT be "Claude"
5. `BENCH_1_3b_pair_034` (Anthropic adoption): Must be near_duplicate, should_fold=True
6. `BENCH_1_3b_pair_040` (OpenShell versions): Must form event cluster, NOT be different
7. `BENCH_1_3b_pair_044` (YC launches): Must NOT form event cluster despite same source
8. `BENCH_1_3b_cluster_candidate_049` (AK papers): Must form thread, NOT event cluster
9. `BENCH_1_3b_cluster_candidate_050` (Notion platform): Must form event cluster
10. `BENCH_1_3b_single_006` ("Concerning."): Must be reject, NOT accepted as funding event
