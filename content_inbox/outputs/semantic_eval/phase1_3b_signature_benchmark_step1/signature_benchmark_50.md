# Event Signature Benchmark — 50 Rows

**Generated**: 2026-05-17
**Source Run**: `api_xgo_ing_phase1_3_round_c_80_live_tuned`
**Items in run**: 80 | **Accepted signatures**: 11 | **Rejected**: 69
**Benchmark rows**: 50 (33 single, 15 pairs, 2 cluster candidates)

---

## Distribution Summary

| Kind | Count |
|---|---|
| single_item | 33 |
| pair | 15 |
| cluster_candidate | 2 |

| Recommended Label | Count |
|---|---|
| integration_or_tooling | 7 |
| event_announcement | 6 |
| generic_opinion | 6 |
| same_product_different_event | 4 |
| adoption_metric | 3 |
| company_or_funding | 3 |
| different_pair | 3 |
| pricing_or_availability | 3 |
| same_thread | 3 |
| feature_update | 2 |
| low_signal_social | 2 |
| related_with_new_info_candidate | 2 |
| research_paper | 2 |
| technical_blog | 2 |
| tutorial_or_guide | 1 |
| near_duplicate_candidate | 1 |

| Recommended Relation | Count |
|---|---|
| same_thread | 5 |
| same_product_different_event | 4 |
| different | 3 |
| related_with_new_info | 3 |
| near_duplicate | 2 |

---

## Section A: Valid Signatures — Accepted but Flawed (6 rows)

These items were **accepted** by the current extractor (`is_concrete=True`) but have significant extraction errors. They demonstrate that the 0.7 concreteness threshold is too permissive.

### Row A1 — BENCH_1_3b_single_001
- **Source**: AI Engineer(@aiDotEngineer)
- **Title**: Security is Job #0 for AI Engineers. Our friends at @snyksec are bringing the AI Security Summit to London this week on May 14!
- **Current**: `unknown|may14|security|2026-05-12` (accepted, 0.7)
- **Recommended**: `Snyk|AI Security Summit|event|London|2026-05-14` (0.85)
- **Issue**: Product="May 14" (date, not product). Actor="" (should be Snyk).
- **Label**: `event_announcement`

### Row A2 — BENCH_1_3b_single_002
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: OpenShell v0.0.40 — local-domain service routing, k8s scheduling, TLS fixes, SecretResolver debug
- **Current**: `nvidia|k8s|security|2026-05-13` (accepted, 1.0)
- **Recommended**: `NVIDIA|OpenShell v0.0.40|release|k8s scheduling + TLS security fixes|2026-05-13` (0.9)
- **Issue**: Action="security" but this is a versioned software release. Product="k8s" is a feature domain, not the product name.
- **Label**: `integration_or_tooling`

### Row A3 — BENCH_1_3b_single_003
- **Source**: meng shao(@shao__meng)
- **Title**: 田渊栋 (前 Meta FAIR Director) 以联合创始人身份正式官宣新公司：Recursive
- **Current**: `meta|our25|launch|2026-05-14` (accepted, 1.0)
- **Recommended**: `Recursive|Recursive Superintelligence|company_launch||2026-05-14` (0.9)
- **Issue**: Actor="Meta" (former employer, not the launched company). Product="Our 25" (gibberish token fragment).
- **Label**: `company_or_funding`

### Row A4 — BENCH_1_3b_single_004
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: Curious what people are running locally these days — DGX Spark local 121B model testing
- **Current**: `unknown|forupdatesfrommyphonehermesagent|featureupdate|2026-05-13` (accepted, 0.7)
- **Recommended**: `NVIDIA|DGX Spark + Hermes Agent|case_study|121B model local testing|2026-05-13` (0.65)
- **Issue**: Product is a garbled 42-character phrase. This is a social anecdote, not a product announcement.
- **Label**: `technical_blog`

### Row A5 — BENCH_1_3b_single_005
- **Source**: Y Combinator(@ycombinator)
- **Title**: PLAN0 (@PLAN0AI) turns architectural plans into construction cost estimates and analytics in minutes
- **Current**: `unknown|plan0|launch|2026-05-14` (accepted, 0.7)
- **Recommended**: `PLAN0|PLAN0|company_launch|construction cost estimation|2026-05-14` (0.85)
- **Issue**: Actor="" despite product name being obvious. Most correct accepted signature in the dataset.
- **Label**: `company_or_funding`

### Row A6 — BENCH_1_3b_single_006
- **Source**: Marc Andreessen 🇺🇸(@pmarca)
- **Title**: Concerning.
- **Current**: `unknown|coordinatedoppositioncampaignsaroundourutahprojects|funding|2026-05-16` (accepted, 0.7)
- **Recommended**: REJECTED (None)
- **Issue**: Product is a 69-character phrase. Title is one word. This is a false positive acceptance — low-context social reaction that should have been rejected.
- **Label**: `low_signal_social`

---

## Section B: Single Failure — missing_concrete_event_action (10 rows)

Items with clear actors/products but action regex failed. Concreteness scores 0.48-0.8. These should produce valid signatures.

### Row B1 — BENCH_1_3b_single_007
- **Source**: 小互(@imxiaohu)
- **Title**: Google 刚刚发布了一个新东西：Googlebook — Gemini 为核心的 AI Laptop 平台
- **Current**: REJECTED (actor=Google, action=other, concreteness 0.48)
- **Recommended**: `Google|Googlebook|release|Gemini-powered AI Laptop platform|2026-05-12` (0.9)
- **Issue**: Clear product launch in Chinese text. Action="other" despite explicit "刚刚发布" (just released).
- **Label**: `event_announcement`

### Row B2 — BENCH_1_3b_single_008
- **Source**: The Rundown AI(@TheRundownAI)
- **Title**: NEW: Nvidia became the first company to hit a $5.5T market cap today
- **Current**: REJECTED (actor=Nvidia, action=other, concreteness 0.48)
- **Recommended**: `NVIDIA|NVDA|adoption_metric|$5.5T market cap milestone|2026-05-13` (0.85)
- **Issue**: Clear milestone event. "Became the first company to hit" is not in action taxonomy.
- **Label**: `adoption_metric`

### Row B3 — BENCH_1_3b_single_009
- **Source**: The Rundown AI(@TheRundownAI)
- **Title**: Big shift in enterprise AI spending: Anthropic surpassed OpenAI for the first time in April (Ramp AI Index)
- **Current**: REJECTED (actor=Anthropic, action=other, concreteness 0.8)
- **Recommended**: `Anthropic|Claude|adoption_metric|34.4% enterprise share surpasses OpenAI|2026-05-13` (0.85)
- **Issue**: Clear adoption data. Action="other" despite "surpassed" language.
- **Label**: `adoption_metric`

### Row B4 — BENCH_1_3b_single_010
- **Source**: Notion(@NotionHQ)
- **Title**: The Notion command-line interface (CLI) is a new way to work with Notion programmatically
- **Current**: REJECTED (actor=Notion, action=other, concreteness 0.8)
- **Recommended**: `Notion|Notion CLI|release|command-line interface for developers|2026-05-13` (0.9)
- **Issue**: Product="made just for developers and coding agents" is a sentence fragment, not product name.
- **Label**: `integration_or_tooling`

### Row B5 — BENCH_1_3b_single_011
- **Source**: Notion(@NotionHQ)
- **Title**: Give your Custom Agents any tool — with agent tools (powered by Workers)
- **Current**: REJECTED (actor="", action=other, concreteness 0.5)
- **Recommended**: `Notion|Notion Custom Agents|feature_update|agent tools via Workers|2026-05-13` (0.85)
- **Issue**: Actor missing. Product="Give your Custom Agents" is a verb phrase.
- **Label**: `feature_update`

### Row B6 — BENCH_1_3b_single_012
- **Source**: meng shao(@shao__meng)
- **Title**: OpenAI 给 Codex 在 Windows 造了一个沙箱 — David Wiesen 技术博客
- **Current**: REJECTED (actor=OpenAI, action=other, concreteness 0.8)
- **Recommended**: `OpenAI|Codex for Windows|technical_blog|sandbox implementation deep-dive|2026-05-14` (0.85)
- **Issue**: Detailed technical blog post. Product="exit 1" and object="Part 1" are tokenization artifacts.
- **Label**: `technical_blog`

### Row B7 — BENCH_1_3b_single_013
- **Source**: 歸藏(guizang.ai)(@op7418)
- **Title**: Codex 终于支持手机上的 ChatGPT 远程控制了！
- **Current**: REJECTED (actor=Codex, action=other, concreteness 0.48)
- **Recommended**: `OpenAI/Codex|Codex Remote Control|feature_update|ChatGPT mobile remote control|2026-05-15` (0.8)
- **Issue**: Actor="Codex" as organization (Codex is a product). Clear feature update.
- **Label**: `feature_update`

### Row B8 — BENCH_1_3b_single_014
- **Source**: AI Will(@FinanceYF5)
- **Title**: QVeris CLI 把 candles、RSI、布林带、公司基本面接进 Claude Code
- **Current**: REJECTED (actor=Claude, action=other, concreteness 0.8)
- **Recommended**: `QVeris|QVeris CLI|integration|Claude Code financial analysis|2026-05-15` (0.8)
- **Issue**: Actor="Claude" is wrong — Claude Code is the integration target, not the maker. Actor should be QVeris.
- **Label**: `integration_or_tooling`

### Row B9 — BENCH_1_3b_single_015
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: OpenShell v0.0.41 — agent-driven policy management, sandbox resource flags, OIDC support
- **Current**: REJECTED (actor=NVIDIA, action=other, concreteness 0.8)
- **Recommended**: `NVIDIA|OpenShell v0.0.41|release|agent-driven policy + sandbox flags|2026-05-14` (0.9)
- **Issue**: Inconsistent: v0.0.40 was accepted, v0.0.41 rejected. Same product, same format. Product="U4n62" is a URL fragment.
- **Label**: `integration_or_tooling`

### Row B10 — BENCH_1_3b_single_016
- **Source**: LangChain(@LangChainAI)
- **Title**: Coming up… A conversation on the future of agents with @andrewng + @hwchase17
- **Current**: REJECTED (actor="", action=other, concreteness 0.5)
- **Recommended**: `LangChain|LangChain Interrupt|event|agent conference with Andrew Ng|2026-05-14` (0.8)
- **Issue**: Event announcement. Product is a descriptive phrase, not event name "Interrupt".
- **Label**: `event_announcement`

---

## Section C: Triple-Failure Low-Signal (9 rows)

Items with all three invalid reasons (concreteness ≤ 0.2). Most are correctly rejected. Two are false negatives.

### Row C1 — BENCH_1_3b_single_017
- **Source**: Lenny Rachitsky(@lennysan)
- **Title**: Great advice
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: One-phrase social engagement bait. Correctly rejected.
- **Label**: `generic_opinion`

### Row C2 — BENCH_1_3b_single_018
- **Source**: Lenny Rachitsky(@lennysan)
- **Title**: Banger
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: One-word social post. Correctly rejected. Shows that very short posts are fundamentally un-extractable.
- **Label**: `generic_opinion`

### Row C3 — BENCH_1_3b_single_019
- **Source**: orange.ai(@oran_ge)
- **Title**: 这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了...
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: Chinese podcast commentary on LLM development. Philosophical opinion, no event. Correctly rejected.
- **Label**: `generic_opinion`

### Row C4 — BENCH_1_3b_single_020
- **Source**: orange.ai(@oran_ge)
- **Title**: 有位朋友创业做的好好的... 别听他们的 follow your heart, follow your money!
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: Chinese startup advice/motivational content. No concrete event. Correctly rejected.
- **Label**: `generic_opinion`

### Row C5 — BENCH_1_3b_single_021
- **Source**: orange.ai(@oran_ge)
- **Title**: 人只有在真实的环境里才能做出正确的决定 (decision-making / skin in the game philosophy)
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: Philosophy/psychology commentary. References "skin in the game" concept. No event. Correctly rejected.
- **Label**: `generic_opinion`

### Row C6 — BENCH_1_3b_single_022
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: @xeophon @arcee_ai Open > closed
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: Three-word social reply. Zero event content. Correctly rejected. Should be filtered at ingest.
- **Label**: `low_signal_social`

### Row C7 — BENCH_1_3b_single_023
- **Source**: orange.ai(@oran_ge)
- **Title**: 塔勒布的箴言集太好看了，一口气读完 (Taleb aphorisms)
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: REJECTED (None)
- **Issue**: Book excerpt/literary appreciation. No event. Correctly rejected.
- **Label**: `generic_opinion`

### Row C8 — BENCH_1_3b_single_024 ⚠️ FALSE NEGATIVE
- **Source**: orange.ai(@oran_ge)
- **Title**: 上海电信直接把 Token 做成话费套餐了。1块钱25万token
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: `China Telecom Shanghai|Token calling plan|pricing|1 RMB per 250K tokens|2026-05-16` (0.7)
- **Issue**: **MISCLASSIFIED**. This IS a real pricing event: China Telecom Shanghai launched token bundles as phone plan add-ons. Chinese text completely obscured the event from the extractor.
- **Label**: `pricing_or_availability`

### Row C9 — BENCH_1_3b_single_025 ⚠️ FALSE NEGATIVE
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: If Luigi knows you, there's a good chance a box is headed to your desk soon
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: `NVIDIA|Stelline Developer Kit|availability|shipping to developers|2026-05-15` (0.65)
- **Issue**: **MISCLASSIFIED**. Cryptic social title hides real hardware shipping event. Card entities show "Stelline Developer Kit, DGX Spark".
- **Label**: `event_announcement`

---

## Section D: Borderline / Edge Cases (8 rows)

Items that fall between categories or have interesting extraction behaviors.

### Row D1 — BENCH_1_3b_single_026
- **Source**: 歸藏(guizang.ai)(@op7418)
- **Title**: GitHub 发布了 GitHub Copilot 桌面端的技术预览版
- **Current**: NONE (action=availability, concreteness 0.68, 0 invalid reasons, but signature_key=None)
- **Recommended**: `GitHub|GitHub Copilot Desktop|availability|technical preview, waitlist|2026-05-15` (0.8)
- **Issue**: 0 invalid reasons yet signature_key=None — fell through a pipeline gap. Neither accepted nor rejected.
- **Label**: `event_announcement`

### Row D2 — BENCH_1_3b_single_027 ⚠️ FALSE NEGATIVE
- **Source**: LangChain(@LangChainAI)
- **Title**: LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans
- **Current**: REJECTED (3 reasons, concreteness 0.18)
- **Recommended**: `LangChain|LangSmith Fleet|pricing|free tier via Fireworks AI|2026-05-14` (0.7)
- **Issue**: **MISCLASSIFIED**. Clear pricing change with concrete product name. Should not be triple-failure.
- **Label**: `pricing_or_availability`

### Row D3 — BENCH_1_3b_single_028
- **Source**: LangChain(@LangChainAI)
- **Title**: Doesn't get much better than free LLMs and sandboxes in everyone's favorite agent builder!
- **Current**: REJECTED (1 reason: missing_concrete_event_action, concreteness 0.8)
- **Recommended**: `LangChain|LangSmith Fleet|pricing|free LLMs and sandboxes|2026-05-14` (0.7)
- **Issue**: Follow-up to D2. High concreteness but only single-failure. Related to D2 — same event, different post.
- **Label**: `pricing_or_availability`

### Row D4 — BENCH_1_3b_single_029
- **Source**: Y Combinator(@ycombinator)
- **Title**: Cancer kills because it's caught late. Adialante is changing that by making mobile MRI accessible
- **Current**: REJECTED (1 reason: missing_concrete_actor_or_product, concreteness 0.38, action=launch)
- **Recommended**: `Adialante|Adialante mobile MRI|company_launch|accessible cancer screening|2026-05-13` (0.75)
- **Issue**: Action=launch detected correctly! But actor missing. Other YC launches with same format were accepted. Pipeline inconsistency.
- **Label**: `company_or_funding`

### Row D5 — BENCH_1_3b_single_030
- **Source**: orange.ai(@oran_ge)
- **Title**: 最近终于把沉浸式翻译的方案换完了 陪读蛙+DeepSeek V4 Flash 用用看
- **Current**: REJECTED (1 reason: missing_concrete_event_action, concreteness 0.48, actor=DeepSeek)
- **Recommended**: REJECTED (None)
- **Issue**: Personal tool setup share. Has concrete product names (DeepSeek V4 Flash) but no event action. Correctly rejected — this is a personal workflow share, not an event.
- **Label**: `generic_opinion`

### Row D6 — BENCH_1_3b_single_031
- **Source**: orange.ai(@oran_ge)
- **Title**: Notion 终于出了 CLI… 跟上了这个时代
- **Current**: REJECTED (1 reason: missing_concrete_event_action, concreteness 0.8, actor=Notion)
- **Recommended**: `Notion|Notion CLI + Developer Platform|release|CLI, Workers, Agent tools, Webhooks|2026-05-16` (0.8)
- **Issue**: Third-party restatement of Notion launch. Same event as official Notion posts but from a different source. High concreteness from rich card entities.
- **Label**: `integration_or_tooling`

### Row D7 — BENCH_1_3b_single_032
- **Source**: Notion(@NotionHQ)
- **Title**: Tools give your Custom Agents capabilities that Notion and MCP don't cover on their own
- **Current**: REJECTED (1 reason: missing_concrete_event_action, concreteness 0.8, actor=Notion)
- **Recommended**: `Notion|Notion Agent Tools (Workers)|feature_update|custom agent capabilities via Workers|2026-05-13` (0.85)
- **Issue**: Part of Notion developer platform launch series. Product is a sentence fragment. Related to CLI and Workers posts.
- **Label**: `integration_or_tooling`

### Row D8 — BENCH_1_3b_single_033
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs
- **Current**: REJECTED (1 reason: missing_concrete_event_action, concreteness 0.5, product=Nemotron 3)
- **Recommended**: `NVIDIA|Nemotron 3 Nano Omni|event|Ask the Experts webinar|2026-05-12` (0.75)
- **Issue**: Webinar/livestream announcement. Product correctly identified as Nemotron 3. Event format "Ask the Experts" not in action taxonomy.
- **Label**: `event_announcement`

---

## Section E: Pair Rows (15 rows)

### E1 — near_duplicate: Anthropic Adoption Data
- **BENCH_1_3b_pair_001**
- **A**: The Rundown AI — "Big shift in enterprise AI spending: Anthropic surpassed OpenAI..." (English)
- **B**: AI Will — "Anthropic 首次在企业采用率上超越 OpenAI..." (Chinese)
- **Current relation**: near_duplicate (candidate_score 4.56, should_fold=True)
- **Recommended relation**: near_duplicate (0.95)
- **Verdict**: ✅ System correct. Cross-language duplicate detection works. Should fold.

### E2 — same_product_different_event: Codex
- **BENCH_1_3b_pair_002**
- **A**: 歸藏 — Codex remote control via ChatGPT mobile
- **B**: meng shao — Codex Windows sandbox technical blog
- **Current relation**: same_product_different_event (score 3.381)
- **Recommended relation**: same_product_different_event (0.9)
- **Verdict**: ✅ System correct. Both about Codex, different features. Should form thread.

### E3 — suspicious_different → same_thread: AK Papers
- **BENCH_1_3b_pair_003**
- **A**: AK — "paper: https://t.co/nRjIqRD2fg"
- **B**: AK — "paper: https://t.co/fkR2wVD129"
- **Current**: suspicious_different (score 4.15)
- **Recommended**: same_thread (0.7)
- **Verdict**: ❌ System too strict. Same source, same format, same action, same day = thread.

### E4 — suspicious_different: QVeris vs Rundown (correct rejection)
- **BENCH_1_3b_pair_004**
- **A**: AI Will — QVeris CLI + Claude Code integration
- **B**: The Rundown AI — AI news roundup mentioning Claude Code
- **Current**: suspicious_different (score 4.103)
- **Recommended**: different (0.9)
- **Verdict**: ✅ System correct. "Claude Code" entity causes false positive candidate generation.

### E5 — suspicious_different → same_product_different_event: YC Launches
- **BENCH_1_3b_pair_005**
- **A**: Y Combinator — PLAN0 launch
- **B**: Y Combinator — Modern launch
- **Current**: suspicious_different (score 4.05)
- **Recommended**: same_product_different_event (0.85)
- **Verdict**: ⚠️ Borderline. Same source, same action (launch), same format, but different companies.

### E6 — same_product_different_event: Notion CLI vs Workers
- **BENCH_1_3b_pair_006**
- **A**: Notion — Notion CLI announcement
- **B**: Notion — Notion Workers announcement
- **Current**: Not evaluated as a pair in relations_interesting
- **Recommended**: same_product_different_event (0.9)
- **Verdict**: ❌ Missed pair. Same source, same timestamp, same launch series. Should form thread.

### E7 — related_with_new_info: OpenShell v0.0.40 vs v0.0.41
- **BENCH_1_3b_pair_007**
- **A**: NVIDIA — OpenShell v0.0.40 (accepted as security)
- **B**: NVIDIA — OpenShell v0.0.41 (rejected)
- **Current**: Not evaluated as a pair
- **Recommended**: related_with_new_info (0.85)
- **Verdict**: ❌ Missed pair. Sequential releases of same product. v0.0.40 accepted, v0.0.41 rejected — pipeline inconsistency.

### E8 — near_duplicate: Agentic Inference + Link Follow-up
- **BENCH_1_3b_pair_008**
- **A**: NVIDIA — Agentic inference at scale (long post)
- **B**: NVIDIA — "Read more" link (same timestamp +1s)
- **Current**: Not evaluated as a pair
- **Recommended**: near_duplicate (0.9)
- **Verdict**: ❌ Missed pair. Second post is a link to the full article. Should fold.

### E9 — same_thread: Anthropic Adoption vs Mythos Debate
- **BENCH_1_3b_pair_009**
- **A**: The Rundown AI — Anthropic enterprise adoption data
- **B**: Gary Marcus — Anthropic Mythos rollout debate
- **Current**: suspicious_different (score 1.572)
- **Recommended**: same_thread (0.8)
- **Verdict**: ⚠️ Borderline. Same company, different topics. Thread-like.

### E10 — different: Recursive vs NVIDIA Agentic Inference
- **BENCH_1_3b_pair_010**
- **A**: meng shao — Recursive startup launch
- **B**: NVIDIA — Agentic inference platform
- **Current**: suspicious_different (score 3.6)
- **Recommended**: different (0.95)
- **Verdict**: ✅ System correct. Generic tokens "agentic", "algorithm" inflate score.

### E11 — same_product_different_event: YC Modern vs YouArt
- **BENCH_1_3b_pair_011**
- **A**: Y Combinator — Modern launch
- **B**: Y Combinator — YouArt launch
- **Current**: suspicious_different (score 3.411)
- **Recommended**: same_product_different_event (0.9)
- **Verdict**: ✅ System reasonable. Both YC launches, different companies.

### E12 — same_thread: Vercel AI Report vs Anthropic Adoption
- **BENCH_1_3b_pair_012**
- **A**: 向阳乔木 — Vercel AI Gateway report (Anthropic 61% spend)
- **B**: The Rundown AI — Ramp AI Index (Anthropic surpasses OpenAI)
- **Current**: suspicious_different (score 1.415)
- **Recommended**: same_thread (0.65)
- **Verdict**: ⚠️ Ambiguous. Different reports, different metrics, same company.

### E13 — same_thread: skin in the game vs CUDA (same-source philosophy, both rejected)
- **BENCH_1_3b_pair_013**
- **A**: orange.ai — Decision-making philosophy (skin in the game)
- **B**: orange.ai — CUDA decision commentary
- **Current**: suspicious_different (score 3.6)
- **Recommended**: same_thread (0.7)
- **Verdict**: ⚠️ CJK text fragment overlap inflates score. Same author's philosophical thread. Neither item should produce event signatures (both rejected).

### E14 — different: AI Security Summit vs LangChain Interrupt
- **BENCH_1_3b_pair_014**
- **A**: AI Engineer — AI Security Summit London May 14
- **B**: LangChain — LangChain Interrupt with Andrew Ng
- **Current**: Not evaluated as a pair
- **Recommended**: different (0.9)
- **Verdict**: Both are event announcements but completely different events. Should be different.

### E15 — related_with_new_info: Notion Custom Agents vs Agent Tools
- **BENCH_1_3b_pair_015**
- **A**: Notion — Custom Agents any tool announcement
- **B**: Notion — Agent Tools/Workers technical details
- **Current**: Not evaluated as a pair
- **Recommended**: related_with_new_info (0.85)
- **Verdict**: ❌ Missed pair. Same launch series, same timestamp. Should cluster.

---

## Section F: Cluster Candidates (2 rows)

### F1 — AK Research Paper Thread
- **BENCH_1_3b_cluster_001**
- **Items**: Two "paper:" link posts from AK@_akhaliq on May 13
- **Current**: Both in separate single-item clusters
- **Recommended**: `AK (@_akhaliq)|HuggingFace papers feed|research_paper||2026-05-13` (0.55)
- **Should form**: Event cluster + thread relation
- **Risk**: SPECULATIVE — no multi-item cluster existed in run. Products are URL fragments.

### F2 — Notion Developer Platform Launch
- **BENCH_1_3b_cluster_002**
- **Items**: Notion CLI + Custom Agents + Workers + Agent Tools from @NotionHQ on May 13
- **Current**: Four separate single-item clusters
- **Recommended**: `Notion|Notion Developer Platform|release|CLI + Workers + Custom Agents + Agent Tools|2026-05-13` (0.8)
- **Should form**: Event cluster
- **Risk**: SPECULATIVE — but strongest cluster candidate in the dataset. Coordinated launch with multiple posts.

---

## Column Reference

| Column | Description |
|---|---|
| `benchmark_id` | Unique ID: BENCH_1_3b_{kind}_{seq} |
| `kind` | single_item, pair, or cluster_candidate |
| `source_file_refs` | Evidence files supporting this row |
| `item_id` / `candidate_item_id` | Dry-run item identifiers |
| `source_name` / `candidate_source_name` | Twitter/X account name |
| `title` / `candidate_title` | Content title |
| `current_signature` | Extracted signature or REJECTED reason |
| `current_invalid_reasons` | List of failure reasons |
| `current_relation` | LLM relation verdict (pairs only) |
| `recommended_label` | Human-assigned content category |
| `recommended_event_signature` | Corrected {actor, product, action, object, date} |
| `recommended_relation` | Corrected pair relation |
| `should_form_event_cluster` | Should items cluster together? |
| `should_form_thread_relation` | Should items form a thread? |
| `should_fold` | Should one item be folded into the other? |
| `confidence` | Human confidence in recommended label (0-1) |
| `reason` | Why current extraction failed |
| `risk_notes` | Caveats and edge cases |
| `human_label` | (Empty — for future human review) |
| `human_notes` | (Empty — for future human review) |
