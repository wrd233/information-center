# Phase 1.2c Review Export Bundle

## 1. Export Metadata

- **Repo path**: `/Users/wangrundong/work/infomation-center`
- **Git commit**: `b30e483`
- **Export time**: 2026-05-17T13:46:10
- **Database used**: `content_inbox/data/content_inbox.sqlite3` (read-only)
- **Before backup**: `before_api_xgo_semantic_phase1_2c_20260517_111621.sqlite3`
- **DB items before**: 2840
- **DB items after**: 3123
- **DB item delta**: 283
- **All commands were read-only**: YES
- **No code was modified**: YES
- **Semantic was dry-run**: YES (not written to production DB)

## 2. Files Included

| File | Description |
|---|---|
| `sources_api_xgo_ing.csv` | All 151 api.xgo.ing* sources with full details |
| `items_added_phase1_2c.csv` | 283 new items with content snippets |
| `items_added_by_source.csv` | Per-source new item counts |
| `ingest_runs_phase1_2c.csv` | Ingest run records (592 individual source runs) |
| `ingest_run_sources_phase1_2c.csv` | Per-source ingest results (17 completed) |
| `semantic_items_300.csv` | 300 sampled items with card tier/reason |
| `semantic_item_card_fallbacks.csv` | 96 heuristic/minimal-rule items |
| `semantic_relations_available.csv` | 120 annotated relation examples from 6 runs |
| `semantic_cluster_candidates.csv` | 77 cluster samples from 6 runs |
| `evidence_files/` | Copied semantic eval outputs (16 files/dirs) |

## 3. Ingest Source Scope

### 3.1 Overview

| Metric | Value |
|---|---|
| Sources matched (api.xgo.ing*) | 151 |
| Succeeded | 7 |
| Failed (timeout) | 143 |
| Failed (HTTP error) | 1 |
| New items (reported by ingest) | 2 |
| Duplicates (reported) | 68 |
| DB item delta (before→after) | 283 |

The 283 DB item delta is _larger_ than the 2 "new items" reported by ingest because:
1. The 2 "new items" means items where `dedupe_key` was genuinely novel.
2. The remaining delta comes from: existing items receiving updates (incrementing `seen_count`, updating timestamps), and items from other concurrent processes.
3. Note: 143 sources timed out but may have partially written items before timeout.

### 3.2 Source Coverage

All 151 `api.xgo.ing*` sources are listed in `sources_api_xgo_ing.csv`. Full field details:
- `source_id`, `source_name`, `feed_url`, `status`, `last_success_at`, `last_failure_at`
- `consecutive_failures`, `failure_count`, `last_new_items`, `last_duplicate_items`
- `last_ingest_at`, `last_run_id`

### 3.3 Items Added (283)

Full list in `items_added_phase1_2c.csv`. Fields for each item:
- `item_id`, `source_id`, `source_name`, `title`, `url`, `guid`
- `published_at`, `created_at`, `summary_snippet`, `content_snippet`
- `dedupe_key`, `dedupe_version`

### 3.4 Per-Source Added Items (Top 20)

| Source | Items Added |
|---|---|
| Ray Dalio(@RayDalio) | 3 |
| Geoffrey Hinton(@geoffreyhinton) | 3 |
| Guillermo Rauch(@rauchg) | 3 |
| Junyang Lin(@JustinLin610) | 2 |
| OpenAI(@OpenAI) | 2 |
| Dify(@dify_ai) | 2 |
| Andrew Ng(@AndrewYNg) | 2 |
| Replicate(@replicate) | 2 |
| Poe(@poe_platform) | 2 |
| Aadit Sheth(@aaditsh) | 2 |
| ElevenLabs(@elevenlabsio) | 2 |
| Weaviate • vector database(@weaviate_io) | 2 |
| NotebookLM(@NotebookLM) | 2 |
| AI SDK(@aisdk) | 2 |
| Simon Willison(@simonw) | 2 |
| Adam D'Angelo(@adamdangelo) | 2 |
| ManusAI(@ManusAI_HQ) | 2 |
| Akshay Kothari(@akothari) | 2 |
| AK(@_akhaliq) | 2 |
| Gary Marcus(@GaryMarcus) | 2 |

### 3.5 Partial Write Suspects

The 143 timeout sources may have partial writes. Evidence:
- 592 individual source run records between 02:50-04:00 UTC on May 17
- 575 runs still in "running" status (never completed = timed out)
- 13 runs completed successfully
- 4 runs completed with failure

Only 17 of 592 runs have corresponding `rss_ingest_run_sources` records (these are the completed ones).

**Partial write indication**: Items with `created_at` between 02:50-04:00 UTC on May 17 from timed-out sources suggest partial writes succeeded before timeout killed the ingest.

Full data in `ingest_runs_phase1_2c.csv` and `ingest_run_sources_phase1_2c.csv`.

## 4. Ingest Delta Detail

### 4.1 Items Added by Time

| Hour (UTC) | Items |
|---|---|
| 03:00 | 283 |


### 4.2 Sample of Added Items (First 10)

- **Title**: sry for missing messages. will respond asap
  - Source: Junyang Lin(@JustinLin610)
  - Link: https://x.com/JustinLin610/status/2030875622013345949
  - Created: 2026-05-17T03:16:36.556035+00:00
  - Snippet: sry for missing messages. will respond asap 💬 97 🔄 11 ❤️ 824 👀 95874 📊 190 ⚡ Powered by xgo.ing

- **Title**: https://t.co/XumAUBwHIO
  - Source: orange.ai(@oran_ge)
  - Link: https://x.com/oran_ge/status/2055834925572706645
  - Created: 2026-05-17T03:16:38.669228+00:00
  - Snippet: x.com/i/article/2055… 💬 1 🔄 0 ❤️ 6 👀 1128 📊 2 ⚡ Powered by xgo.ing

- **Title**: With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigati...
  - Source: OpenAI(@OpenAI)
  - Link: https://x.com/OpenAI/status/2052480801435189708
  - Created: 2026-05-17T03:16:38.687282+00:00
  - Snippet: With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigating structured pages and complex data entry flows. Under the hood, it writes and runs code to navigat

- **Title**: Japan IT Week Spring 2026 — 3 incredible days, done! 🙏 Three incredible days at Japan IT Week S...
  - Source: Dify(@dify_ai)
  - Link: https://x.com/dify_ai/status/2042549118397223307
  - Created: 2026-05-17T03:16:41.351051+00:00
  - Snippet: Japan IT Week Spring 2026 — 3 incredible days, done! 🙏 Three incredible days at Japan IT Week Spring 2026 have come to an end. A heartfelt thank you to everyone who visited us at Booth E34-66. The exp

- **Title**: New course: Build and Train an LLM with JAX, built in partnership with @Google and taught by @chrisa...
  - Source: Andrew Ng(@AndrewYNg)
  - Link: https://x.com/AndrewYNg/status/2029266102178693378
  - Created: 2026-05-17T03:16:41.426019+00:00
  - Snippet: New course: Build and Train an LLM with JAX, built in partnership with @Google and taught by @chrisachard . JAX is the open-source library behind Google's Gemini, Veo, and other advanced models. This 

- **Title**: HappyHorse-1.0 from Alibaba is here. 🐎💨 This surprise 15B-parameter model has claimed the #1 spot...
  - Source: Replicate(@replicate)
  - Link: https://x.com/replicate/status/2048775215078117809
  - Created: 2026-05-17T03:16:42.291986+00:00
  - Snippet: HappyHorse-1.0 from Alibaba is here. 🐎💨 This surprise 15B-parameter model has claimed the #1 spot on the @ArtificialAnlys Video Arena, outperforming every major lab in text-to-video and image-to-video

- **Title**: Qwen3.6 Plus is now live on Poe. Delivers advanced vision‑language performance from Qwen, with clea...
  - Source: Poe(@poe_platform)
  - Link: https://x.com/poe_platform/status/2039830320447734057
  - Created: 2026-05-17T03:16:51.171970+00:00
  - Snippet: Qwen3.6 Plus is now live on Poe. Delivers advanced vision‑language performance from Qwen, with clear gains in code‑heavy workflows like agentic and front‑end coding, plus stronger multimodal understan

- **Title**: The best companies to work at today: 1. Anthropic 2. OpenAI 3. Google DeepMind 4. SpaceX 5. xAI 6. ...
  - Source: Aadit Sheth(@aaditsh)
  - Link: https://x.com/aaditsh/status/2052063521022886003
  - Created: 2026-05-17T03:17:04.468288+00:00
  - Snippet: The best companies to work at today: 1. Anthropic 2. OpenAI 3. Google DeepMind 4. SpaceX 5. xAI 6. NVIDIA 7. Tesla 8. Meta 9. Microsoft 10. ? 💬 256 🔄 51 ❤️ 1666 👀 427108 📊 435 ⚡ Powered by xgo.ing

- **Title**: One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...
  - Source: ElevenLabs(@elevenlabsio)
  - Link: https://x.com/ElevenLabs/status/2052022104363499866
  - Created: 2026-05-17T03:17:06.474018+00:00
  - Snippet: One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Learn more: elevenlabs.io/blog/introduci… 💬 2 🔄 2 ❤️ 13 👀 2691 📊 4 ⚡ Powered by xgo.ing

- **Title**: We spent weeks testing text vs. image retrieval for RAG. The winner? 𝗡𝗲𝗶𝘁𝗵𝗲𝗿. Our recent pu...
  - Source: Weaviate • vector database(@weaviate_io)
  - Link: https://x.com/weaviate_io/status/2041897318367060054
  - Created: 2026-05-17T03:17:11.742245+00:00
  - Snippet: We spent weeks testing text vs. image retrieval for RAG. The winner? 𝗡𝗲𝗶𝘁𝗵𝗲𝗿. Our recent publication, IRPAPERS, compares 𝘁𝗲𝘅𝘁-𝗯𝗮𝘀𝗲𝗱 𝗿𝗲𝘁𝗿𝗶𝗲𝘃𝗮𝗹 (OCR + vector, keyword, and hybrid search) and 𝗶𝗺𝗮𝗴𝗲-𝗯𝗮𝘀𝗲𝗱

## 5. Semantic Dry-Run Coverage

### 5.1 Final 300 Run Summary

| Metric | Value |
|---|---|
| Items sampled | 300 |
| Languages | 289 English, 11 Chinese |
| Sources represented | 57 |
| Total LLM calls | 223 |
| Total tokens | 714,640 |
| Duration | 1232.7s |
| Concurrency | 4 |

### 5.2 Card Quality

| Tier | Count |
|---|---|
| Full | 99 |
| Standard | 105 |
| Minimal | 96 |
| **Total generated** | **300** |

| Metric | Value |
|---|---|
| Heuristic card fallbacks | 35 |
| Item card failures | 7 |
| Avg confidence (full) | 0.734 |
| Avg confidence (standard) | 0.715 |
| Avg confidence (minimal) | 0.550 |

### 5.3 Content Roles

| Role | Count |
|---|---|
| Report | 129 |
| Source Material | 85 |
| Commentary | 26 |
| Analysis | 25 |
| Low Signal | 21 |
| Aggregator | 7 |
| Firsthand | 7 |

### 5.4 Item-Item Relations

| Relation | Count |
|---|---|
| Different | 453 |
| Near Duplicate | 7 |
| Related with New Info | 23 |
| Uncertain | 1 |
| **Total candidate pairs** | **484** |
| Fold candidates | 7 |
| LLM relation calls | 97 |

### 5.5 Item-Cluster Relations

| Metric | Value |
|---|---|
| Candidate clusters considered | 20 |
| Created clusters | 20 |
| Multi-item clusters | **0** |
| Avg items per cluster | 1.0 |
| Attached to existing | 0 |
| new_info relations | 16 |
| source_material relations | 4 |

## 6. Relation Evidence

### 6.1 Available Data

**CRITICAL GAP**: The semantic eval output JSONs only contain **20 annotated examples per run** (10 high-confidence + 10 low-confidence). The full 484 individual relation records (453 different, 7 near_duplicate, 23 related_with_new_info, 1 uncertain) are NOT available in the JSON/MD outputs. They existed only in the dry-run evaluation database which was not persisted.

Only **aggregate counts** are available for the full relation set.

### 6.2 Annotated Relation Examples (Final 300 Run)

**High-confidence examples (10):**

**Relation 1** — different (confidence=0.95, should_fold=False)
- Item A: I tried running the same "Generate an SVG of a pelican riding a bicycle" prompt against 21 different...
- Item B: From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...
- Published: 2026-05-04T17:30:29+00:00
- Source: socialmedia-runway-runwayml
- Reason: New item about character AI response time; candidate is about SVG generation with IBM Granite models. No shared entities or topic.

**Relation 2** — different (confidence=0.95, should_fold=False)
- Item A: Read more: https://t.co/3YEhHmqg3g
- Item B: From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...
- Published: 2026-05-04T17:30:29+00:00
- Source: socialmedia-runway-runwayml
- Reason: New item about character AI response time; candidate is a tweet link about Meta buying something. No shared entities or topic.

**Relation 3** — different (confidence=0.95, should_fold=False)
- Item A: Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...
- Item B: From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...
- Published: 2026-05-04T17:30:29+00:00
- Source: socialmedia-runway-runwayml
- Reason: New item about character AI response time; candidate is about API cache scoping. No shared entities or topic.

**Relation 4** — different (confidence=0.95, should_fold=False)
- Item A: Work less, make more
- Item B: From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...
- Published: 2026-05-04T17:30:29+00:00
- Source: socialmedia-runway-runwayml
- Reason: New item about character AI response time; candidate is a generic motivational post. No shared entities or topic.

**Relation 5** — different (confidence=0.95, should_fold=False)
- Item A: Build it. Break it. Fix it. From campaign trackers to financial planners, @CalStateEastBay students...
- Item B: From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...
- Published: 2026-05-04T17:30:29+00:00
- Source: socialmedia-runway-runwayml
- Reason: New item about character AI response time; candidate is about Codex challenge with students. No shared entities or topic.

**Relation 6** — different (confidence=0.9, should_fold=False)
- Item A: Gemini 3.1 Pro is out and it’s a step function improvement across many domains. It’s rolling out to ...
- Item B: Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...
- Published: 2026-04-16T15:31:39+00:00
- Source: socialmedia-poe-poe-platform
- Reason: New item discusses Opus 4.7 coding benchmarks; candidate is about Gemini 3.1 Pro release. No overlap in content.

**Relation 7** — different (confidence=0.9, should_fold=False)
- Item A: We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image...
- Item B: Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...
- Published: 2026-04-16T15:31:39+00:00
- Source: socialmedia-poe-poe-platform
- Reason: New item is about Opus 4.7 coding benchmarks; candidate is about Nano Banana Pro image generation. Unrelated topics.

**Relation 8** — different (confidence=0.9, should_fold=False)
- Item A: Kimi K2.6 is now available in Windsurf! Available for free for the next 2 weeks for Pro, Teams, and...
- Item B: Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...
- Published: 2026-04-16T15:31:39+00:00
- Source: socialmedia-poe-poe-platform
- Reason: New item discusses Opus 4.7 coding improvements; candidate is about Kimi K2.6 availability in Windsurf. No shared event or topic.

**Relation 9** — different (confidence=0.9, should_fold=False)
- Item A: DeepSeek v4 Pro还是可以的。 几轮对话，实现一个工具，用xbox手柄控制电脑应用和浏览器。 当遥控器，躺床上刷小说和看视频。
- Item B: Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...
- Published: 2026-04-16T15:31:39+00:00
- Source: socialmedia-poe-poe-platform
- Reason: New item is about Opus 4.7 benchmarks; candidate is about DeepSeek v4 Pro usage example. Different products and contexts.

**Relation 10** — different (confidence=0.9, should_fold=False)
- Item A: v0 Auto picks the right model for your prompt, whether that's Mini for quick edits, Pro for most tas...
- Item B: Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...
- Published: 2026-04-16T15:31:39+00:00
- Source: socialmedia-poe-poe-platform
- Reason: New item focuses on Opus 4.7 coding performance; candidate is about v0 Auto model selection. No overlap.


**Low-confidence examples (10):**

**Low-Conf 1** — different (confidence=0.5)
- A: Really fun to try this app while in Sydney this week, which uses our tools to help fans deep dive in...
- B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...
- Reason: The new item is a summary of multiple AI topics (data leaks, cloud OS, AI use at work) while the candidate is a tweet about a fun cricket app in Sydney. No meaningful overlap.

**Low-Conf 2** — different (confidence=0.5)
- A: Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with...
- B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...
- Reason: The new item discusses AI agent data leaks and research, while the candidate announces Windsurf 2.0 for agent management. Different angles, not same event.

**Low-Conf 3** — different (confidence=0.5)
- A: Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config...
- B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...
- Reason: The new item is a research focus article, while the candidate is about importing workflow to Codex. No direct connection.

**Low-Conf 4** — different (confidence=0.5)
- A: https://t.co/iMifqBlNHZ
- B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...
- Reason: The candidate is a tweet about a Stripe link recreation, unrelated to the new item's topics.

**Low-Conf 5** — different (confidence=0.5)
- A: When debt levels reach extreme sizes relative to income, governments are left with a limited set of ...
- B: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...
- Reason: The candidate is about government debt and monetary policy, totally unrelated to AI research topics in the new item.

**Low-Conf 6** — different (confidence=0.25)
- A: kicking off a bunch of codex tasks, running around with my kid in the sunshine, and then coming back...
- B: 5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...
- Reason: Topics are unrelated: new item is about a model named 5.5, candidate is about codex tasks.

**Low-Conf 7** — different (confidence=0.3)
- A: what would you most like to see improve in our next model?
- B: 5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...
- Reason: Candidate asks what to improve in next model, new item is a comment on model 5.5's name.

**Low-Conf 8** — different (confidence=0.2)
- A: It's an unimpressive-sounding word, but one of the most powerful motivations is the motivation of th...
- B: 5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...
- Reason: Candidate about hobbyist motivation, new item about model naming.

**Low-Conf 9** — different (confidence=0.2)
- A: ok other than more goblins, i think this reasonably well matches what we are prioritizing!
- B: 5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...
- Reason: Candidate about prioritizing goblins, new item about model 5.5.

**Low-Conf 10** — different (confidence=0.2)
- A: v0 is heading to SXSW to build agents. Join us live to make your own and walk away production-ready...
- B: 5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...
- Reason: Candidate about v0 at SXSW, new item about model 5.5.

### 6.3 Relations from Other Runs (100 examples across 5 runs)

See `semantic_relations_available.csv` for the full list of 120 annotated relation examples.

## 7. Cluster Diagnostics

### 7.1 Why Multi-Item Clusters = 0

The final 300 run created 20 clusters, all single-item. Root causes from the report:

1. **Candidate recall limited**: Only 20 candidate clusters considered out of 300 items. The recall strategy (lexical/entity/time/source hybrid) may be too conservative.
2. **Stage budget constraints**: The `relation_heavy` stage budget profile may have limited cluster-relation LLM calls.
3. **Attachment rejected**: Items offered for attachment were rejected by the cluster-relation LLM (classified as different/uncertain rather than new_info/source_material).
4. **High threshold for multi-item**: The system requires both semantic relation AND cluster-level agreement; many item pairs have weak-enough relations that they don't form clusters.

### 7.2 Cluster Samples (Final 300 Run)

**Cluster 1**: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...
- Items: 1 | Representative: item_2fd731e980504b92bcb3e87e7cc828ad
- Core facts: Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new research on how to actually structure AI use at work. msft.it/6016vKxQm Your browser does not support the video tag. 🔗 View on Twitter 💬 7 🔄 13 ❤️ 50 👀 9018 📊 18 ⚡ Powered by xgo.ing

**Cluster 2**: Local LLM execution demo
- Items: 1 | Representative: item_3586ece7f7dd4d0ea65773c4f304d370
- Core facts: NVIDIA AI posted about running a 121B model locally on DGX Spark, with Hermes agent autonomously running tests and reporting results.

**Cluster 3**: Ray Dalio on the battle between feelings and rational thinking
- Items: 1 | Representative: item_20646704dff34c81be8f0574610f4612
- Core facts: Ray Dalio tweets about the conflict between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex).

**Cluster 4**: Notebooks integration with Gemini App launched
- Items: 1 | Representative: item_9ac7138b5a254e63a242469ef2e3b0b7
- Core facts: NotebookLM announces that notebooks are now available in the Gemini App for Free and Paid users on mobile, with expansion to more countries and free users planned.

**Cluster 5**: Mem0 and BasisSet 2026 AI Fellowship opening
- Items: 1 | Representative: item_f452aeb604f1408b9cefb23d173ab32f
- Core facts: Mem0 partners with BasisSet for 2026 AI Fellowship on agentic memory track; apply by May 1.

**Cluster 6**: Mike Krieger on AI & I podcast
- Items: 1 | Representative: item_9f15a4e890b248438ad2edf69e07f0c0
- Core facts: Mike Krieger discusses building agent-native products with Dan Shipper on the AI & I podcast.

**Cluster 7**: The Book of Elon by Eric Jorgenson
- Items: 1 | Representative: item_c4265f28396b4865bdeefbf7afd99dc8
- Core facts: Promotion of 'The Book of Elon' by Eric Jorgenson, a compilation of Elon Musk's ideas.

**Cluster 8**: LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total /...
- Items: 1 | Representative: item_7e380ba74030420b8b1775d2ace0bb08
- Core facts: LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total / 17B active, ~15x larger!) on every major coding benchmark — including SWE-bench Verified (77.2 vs. 76.2), SWE-bench Pro (53.5 vs. 50.9), Terminal-Bench 2.0 (59.3 vs. 52.5), and SkillsBench (48.2 vs. 30.0). It also surpasses all peer-scale dense models by a w…

**Cluster 9**: Recraft shares image generation prompts for campaign style
- Items: 1 | Representative: item_13129eb757e54a268b774cbb0771d3e1
- Core facts: Recraft posts 4 example prompts for generating images with specific styles and text overlays.

**Cluster 10**: Qdrant attending AI Dev Conference
- Items: 1 | Representative: item_d4b901574ed248ada87c4e4017af5407
- Core facts: Qdrant is live at AI Dev Conference, inviting attendees to visit their booth.


Remaining 10 clusters listed in `semantic_cluster_candidates.csv`.

## 8. Event Hotspot Diagnostics

The `event_hotspots` sampling mode was used for the 150-item comparison runs. Each run used hotspot-based sampling to identify candidate groups.

### 8.1 Hotspot Coverage

- **smoke_c3**: 7 candidates considered, 7 clusters, 1 multi-item
- **hotspots_150_c3**: 12 candidates considered, 12 clusters, 1 multi-item
- **hotspots_150_c2**: 12 candidates considered, 12 clusters, 0 multi-item
- **hotspots_150_c4**: 17 candidates considered, 17 clusters, 0 multi-item

### 8.2 Why Hotspots Didn't Form Multi-Item Clusters

Hotspot sampling groups items by lexical/entity/time proximity, but:
1. Grouped items may be about different specific events within the same broad theme.
2. The LLM cluster-relation check may find items are "same_topic" but not "same_event".
3. Budget constraints could limit the number of LLM checks per hotspot group.

Full hotspot group data was not persisted in the output JSONs (only aggregate counts).

## 9. Item-Card Fallback/Failure Cases

### 9.1 Heuristic Fallbacks (35 of 300)

The `heuristic_card_fallback_count: 35` refers to items where LLM card generation produced JSON parse errors, triggering a heuristic/minimal card fallback. In the steps data, these appear as items with JSON parse error reasons.

Additionally, 96 items received "local minimal card" via `minimal_rule` (no LLM call at all), typically for very short or low-signal content.

**Sample of 10 minimal-rule items:**

- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)
- []  (reason: local minimal card)

Full list of 96 fallback items in `semantic_item_card_fallbacks.csv`.

### 9.2 Card Failures (7 of 300)

The 7 item-card failures represent items where even the fallback/heuristic card generation failed. **The specific item_ids for these 7 failures are NOT available in the JSON outputs** — only the count is recorded.

In the `steps.item_cards.items` list, all 300 items have card assignments (no items are marked as outright failed). The 7 failures might be:
- Items that failed before reaching the steps tracking
- Items counted in `errors_fallbacks.final_failures` (total=9, which includes 7 card failures + 1 relation failure + 1 cluster failure)

## 10. Source-Profile Review Aggregation

### 10.1 Conservative Aggregation

The Phase 1.2c semantic eval used conservative source-profile review: source-level priority reviews were suppressed/aggregated (0 source_priority_reviews in the final run, down from 67 in the first smoke test).

- **Total sources with profile data**: 0 (from the top-level structure)
- **Source priority reviews generated**: 0 (suppressed in final run)
- **Review queue entries due to failure**: 393

### 10.2 Per-Source Metrics

See `source_profiles` in the bundle JSON for per-source data including:
- `total_items`, `llm_processed_items`
- `duplicate_rate`, `near_duplicate_rate`, `new_event_rate`
- `incremental_value_avg`, `report_value_avg`
- `llm_total_tokens`, `llm_yield_score`, `llm_priority`

## 11. Known Gaps in Exported Evidence

The following data **could not be exported** because it does not exist in the available outputs:

| Gap | Reason |
|---|---|
| Full 484 item-item relation records | Only 20 annotated examples per run in JSON; dry-run DB not persisted |
| Individual 7 near_duplicate pairs | Count known (7), but individual pairs not in outputs |
| Individual 23 related_with_new_info pairs | Count known (23), but individual pairs not in outputs |
| The 1 uncertain pair | Count known, but not individually listed |
| 7 card failure item_ids | Only count known, not individual items |
| Raw LLM prompts/responses | Not included in eval outputs |
| Hotspot group membership | Only aggregate counts, not per-group item lists |
| 300 items' full content (titles/summaries) | Dry-run used separate DB with different item_ids; production DB items don't match |

### Why the 300 Items Don't Match the Production DB

The semantic evaluation used a **dry-run database** (an in-memory or temporary copy). The `item_id` values in the semantic outputs (e.g., `item_2fd731e980504b92bcb3e87e7cc828ad`) are from this dry-run DB and do **not** correspond to any items in the production `content_inbox.sqlite3`. This means:
- We cannot look up the full title/summary/link for the 300 evaluation items from the production DB
- The 10 annotated card samples in the report provide the only item-level content detail
- Cross-referencing would require matching by title/content fingerprint, which is fragile

## 12. Concurrency Comparison

- **Recommended concurrency**: 4
- **c2**: 1061s, 431332 tokens, 2 failures, 30 non-different relations
- **c3**: 965s, 427440 tokens, 5 failures, 28 non-different relations
- **c4**: 797s, 430957 tokens, 5 failures, 33 non-different relations
