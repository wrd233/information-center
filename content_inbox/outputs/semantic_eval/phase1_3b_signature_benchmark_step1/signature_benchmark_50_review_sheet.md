# Event Signature Benchmark — Review Sheet

Quick-reference review sheet for the 50-row benchmark. Simplified columns for spreadsheet-style review.

## Valid Signature Candidates (6 rows)

| ID | Kind | Source | Title | Rec. Label | Rec. Signature | Cluster? | Reason |
|---|---|---|---|---|---|---|---|
| BENCH_1_3b_single_001 | single | AI Engineer | Security is Job #0... AI Security Summit | event_announcement | Snyk\|AI Security Summit\|event | No | Wrong product (date instead of name), missing actor |
| BENCH_1_3b_single_002 | single | NVIDIA AI | OpenShell v0.0.40... | integration_or_tooling | NVIDIA\|OpenShell v0.0.40\|release | No | Wrong action (security), wrong product (k8s) |
| BENCH_1_3b_single_003 | single | meng shao | 田渊栋... Recursive | company_or_funding | Recursive\|Recursive Superintelligence\|company_launch | No | Wrong actor (Meta), gibberish product |
| BENCH_1_3b_single_004 | single | NVIDIA AI | Curious what people are running... | technical_blog | NVIDIA\|DGX Spark + Hermes Agent\|case_study | No | Gibberish product, social anecdote not product |
| BENCH_1_3b_single_005 | single | Y Combinator | PLAN0... construction cost estimates | company_or_funding | PLAN0\|PLAN0\|company_launch | No | Missing actor, best accepted signature |
| BENCH_1_3b_single_006 | single | pmarca | Concerning. | low_signal_social | REJECTED | No | False positive — 69-char product, one-word title |

## Single-Failure: missing_concrete_event_action (10 rows)

| ID | Kind | Source | Title | Rec. Label | Rec. Signature | Cluster? | Reason |
|---|---|---|---|---|---|---|---|
| BENCH_1_3b_single_007 | single | 小互 | Google 刚刚发布了 Googlebook | event_announcement | Google\|Googlebook\|release | No | Chinese launch language missed by regex |
| BENCH_1_3b_single_008 | single | The Rundown AI | Nvidia $5.5T market cap | adoption_metric | NVIDIA\|NVDA\|adoption_metric | No | "Became first company to hit" not in taxonomy |
| BENCH_1_3b_single_009 | single | The Rundown AI | Anthropic surpassed OpenAI | adoption_metric | Anthropic\|Claude\|adoption_metric | No | "Surpassed" not detected as action |
| BENCH_1_3b_single_010 | single | Notion | Notion CLI... | integration_or_tooling | Notion\|Notion CLI\|release | No | Product is sentence fragment |
| BENCH_1_3b_single_011 | single | Notion | Give your Custom Agents any tool | feature_update | Notion\|Notion Custom Agents\|feature_update | No | Actor missing, product is verb phrase |
| BENCH_1_3b_single_012 | single | meng shao | Codex Windows sandbox | technical_blog | OpenAI\|Codex for Windows\|technical_blog | No | Product="exit 1", Object="Part 1" artifacts |
| BENCH_1_3b_single_013 | single | 歸藏 | Codex ChatGPT 远程控制 | feature_update | OpenAI/Codex\|Codex Remote Control\|feature_update | No | Actor=Codex as org (it's a product) |
| BENCH_1_3b_single_014 | single | AI Will | QVeris CLI + Claude Code | integration_or_tooling | QVeris\|QVeris CLI\|integration | No | Actor confusion: Claude is target, not maker |
| BENCH_1_3b_single_015 | single | NVIDIA AI | OpenShell v0.0.41 | integration_or_tooling | NVIDIA\|OpenShell v0.0.41\|release | No | v0.0.40 accepted, v0.0.41 rejected (inconsistent) |
| BENCH_1_3b_single_016 | single | LangChain | Andrew Ng + Harrison Chase | event_announcement | LangChain\|LangChain Interrupt\|event | No | Product is descriptive phrase, not event name |

## Triple-Failure Low-Signal (9 rows)

| ID | Kind | Source | Title | Rec. Label | Rec. Signature | Cluster? | Reason |
|---|---|---|---|---|---|---|---|
| BENCH_1_3b_single_017 | single | Lenny Rachitsky | Great advice | generic_opinion | REJECTED | No | One-phrase social engagement. Correctly rejected. |
| BENCH_1_3b_single_018 | single | Lenny Rachitsky | Banger | generic_opinion | REJECTED | No | One-word post. Correctly rejected. |
| BENCH_1_3b_single_019 | single | orange.ai | 这期播客实在太... 大模型太简单了 | generic_opinion | REJECTED | No | Chinese podcast opinion. Correctly rejected. |
| BENCH_1_3b_single_020 | single | orange.ai | 创业... follow your heart | generic_opinion | REJECTED | No | Startup advice. Correctly rejected. |
| BENCH_1_3b_single_021 | single | orange.ai | 人只有在真实的环境里... skin in the game | generic_opinion | REJECTED | No | Philosophy. Correctly rejected. |
| BENCH_1_3b_single_022 | single | NVIDIA AI | @xeophon Open > closed | low_signal_social | REJECTED | No | 3-word reply. Correctly rejected. |
| BENCH_1_3b_single_023 | single | orange.ai | 塔勒布箴言集 | generic_opinion | REJECTED | No | Book excerpts. Correctly rejected. |
| BENCH_1_3b_single_024 | single | orange.ai | 上海电信 Token 话费套餐 ⚠️ | pricing_or_availability | China Telecom Shanghai\|Token plan\|pricing | No | **FALSE NEGATIVE** — real pricing event |
| BENCH_1_3b_single_025 | single | NVIDIA AI | If Luigi knows you... ⚠️ | event_announcement | NVIDIA\|Stelline Dev Kit\|availability | No | **FALSE NEGATIVE** — real hardware shipping |

## Borderline / Edge Cases (8 rows)

| ID | Kind | Source | Title | Rec. Label | Rec. Signature | Cluster? | Reason |
|---|---|---|---|---|---|---|---|
| BENCH_1_3b_single_026 | single | 歸藏 | GitHub Copilot 桌面端 | event_announcement | GitHub\|Copilot Desktop\|availability | No | 0 reasons but no signature — pipeline gap |
| BENCH_1_3b_single_027 | single | LangChain | LangSmith Fleet free model ⚠️ | pricing_or_availability | LangChain\|LangSmith Fleet\|pricing | No | **FALSE NEGATIVE** — real pricing event |
| BENCH_1_3b_single_028 | single | LangChain | Free LLMs and sandboxes | pricing_or_availability | LangChain\|LangSmith Fleet\|pricing | No | Related to D2, same event different post |
| BENCH_1_3b_single_029 | single | Y Combinator | Adialante mobile MRI | company_or_funding | Adialante\|Adialante MRI\|company_launch | No | Inconsistent: action=launch but rejected |
| BENCH_1_3b_single_030 | single | orange.ai | 翻译方案... DeepSeek V4 Flash | generic_opinion | REJECTED | No | Personal tool share, correctly rejected |
| BENCH_1_3b_single_031 | single | orange.ai | Notion 终于出了 CLI | integration_or_tooling | Notion\|Notion CLI+Platform\|release | No | Third-party restatement of Notion launch |
| BENCH_1_3b_single_032 | single | Notion | Agent Tools via Workers | integration_or_tooling | Notion\|Agent Tools (Workers)\|feature_update | No | Part of launch series, sentence fragment product |
| BENCH_1_3b_single_033 | single | NVIDIA AI | Ask the Experts: Nemotron 3 | event_announcement | NVIDIA\|Nemotron 3 Nano Omni\|event | No | Webinar format not in action taxonomy |

## Pair Rows (15 rows)

| ID | Kind | Source A | Title A | Source B | Title B | Rec. Relation | Fold? | Reason |
|---|---|---|---|---|---|---|---|---|
| BENCH_1_3b_pair_001 | pair | The Rundown AI | Anthropic surpassed OpenAI (EN) | AI Will | Anthropic 超越 OpenAI (ZH) | near_duplicate | Yes | ✅ Correct. Cross-language duplicate. |
| BENCH_1_3b_pair_002 | pair | 歸藏 | Codex remote control | meng shao | Codex Windows sandbox | same_product_different_event | No | ✅ Correct. Same product, different features. |
| BENCH_1_3b_pair_003 | pair | AK | paper: nRjIqRD2fg | AK | paper: fkR2wVD129 | same_thread | No | ❌ Should be thread. Same source+format+action. |
| BENCH_1_3b_pair_004 | pair | AI Will | QVeris CLI + Claude Code | The Rundown AI | AI news roundup | different | No | ✅ Correct. Claude Code false positive. |
| BENCH_1_3b_pair_005 | pair | Y Combinator | PLAN0 launch | Y Combinator | Modern launch | same_product_different_event | No | ⚠️ Both YC launches, different companies. |
| BENCH_1_3b_pair_006 | pair | Notion | Notion CLI | Notion | Notion Workers | same_product_different_event | No | ❌ Missed pair. Same source+timestamp. |
| BENCH_1_3b_pair_007 | pair | NVIDIA AI | OpenShell v0.0.40 | NVIDIA AI | OpenShell v0.0.41 | related_with_new_info | No | ❌ Missed pair. Sequential releases. |
| BENCH_1_3b_pair_008 | pair | NVIDIA AI | Agentic inference post | NVIDIA AI | Read more link | near_duplicate | Yes | ❌ Missed pair. Link follow-up. |
| BENCH_1_3b_pair_009 | pair | The Rundown AI | Anthropic adoption | Gary Marcus | Anthropic Mythos debate | same_thread | No | ⚠️ Same company, different topics. |
| BENCH_1_3b_pair_010 | pair | meng shao | Recursive launch | NVIDIA AI | Agentic inference | different | No | ✅ Correct. Generic tokens inflate score. |
| BENCH_1_3b_pair_011 | pair | Y Combinator | Modern launch | Y Combinator | YouArt launch | same_product_different_event | No | ✅ Same source, different companies. |
| BENCH_1_3b_pair_012 | pair | 向阳乔木 | Vercel AI report | The Rundown AI | Anthropic adoption | same_thread | No | ⚠️ Different reports, same company. |
| BENCH_1_3b_pair_013 | pair | orange.ai | skin in the game | orange.ai | CUDA commentary | same_thread | No | ⚠️ Same-author philosophy, both items rejected |
| BENCH_1_3b_pair_014 | pair | AI Engineer | AI Security Summit | LangChain | LangChain Interrupt | different | No | Different events, same format. |
| BENCH_1_3b_pair_015 | pair | Notion | Custom Agents tools | Notion | Agent Tools Workers | related_with_new_info | No | ❌ Missed pair. Same launch series. |

## Cluster Candidates (2 rows)

| ID | Kind | Items | Rec. Label | Rec. Signature | Cluster? | Thread? | Confidence |
|---|---|---|---|---|---|---|---|
| BENCH_1_3b_cluster_001 | cluster | AK paper posts ×2 | research_paper | AK\|HF papers\|research_paper | Yes | Yes | 0.55 |
| BENCH_1_3b_cluster_002 | cluster | Notion CLI + Custom Agents + Workers | integration_or_tooling | Notion\|Developer Platform\|release | Yes | No | 0.80 |

## Legend

- ✅ = System verdict correct
- ❌ = System verdict wrong / missed pair
- ⚠️ = Borderline / debatable
- **FALSE NEGATIVE** = Real event incorrectly rejected
