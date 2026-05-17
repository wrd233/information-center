# Phase 1.3c Token Cost Attribution

## Overall

| Metric | Value |
|---|---|
| Total items | 300 |
| Total tokens | 877,140 |
| Total LLM calls | 220 |
| Tokens per item | 2923.8 |
| Cache hit rate | 26.92% |
| Failure tokens | 0 (0.0%) |

## By Stage

| Stage | Calls | Tokens | % of Total | Tokens/Item | Success | Failed |
|---|---|---|---|---|---|---|
| item_card | 54 | 282,644 | 32.2% | 942.1 | 51 | 3 |
| item_relation | 157 | 539,265 | 61.5% | 1797.5 | 129 | 28 |
| item_cluster_relation | 6 | 48,727 | 5.6% | 162.4 | 6 | 0 |
| cluster_card_patch | 3 | 6,504 | 0.7% | 21.7 | 3 | 0 |

## By Semantic Level

| Level | Estimated Tokens | Items Touching | Avg Tokens/Item |
|---|---|---|---|
| event_signature | 521,088 | 860 | 605.9 |
| thread_signature | 278,421 | 464 | 600.0 |
| reject | 75,732 | 71 | 1066.7 |
| content_signature | 1,899 | 4 | 474.7 |

## Top 10 Most Expensive Items

| Item ID | Title | Source | Level | Est. Tokens |
|---|---|---|---|---|
| item_9d0967dbc96b4c769897a436562d8634 | Code Arena's frontend leaderboard for models using visual inputs in agentic codi | lmarena.ai(@lmarena_ai) | event_signature | 16,425 |
| item_bb7e8c917d314f0eb996a1df026c74b6 | The best companies to work at today: 1. Anthropic 2. OpenAI 3. Google DeepMind 4 | Aadit Sheth(@aaditsh) | thread_signature | 12,900 |
| item_00a7372d41284c28931a28e579a03d61 | 田渊栋 (前 Meta FAIR Director) 以联合创始人身份正式官宣新公司：Recursive @Recursive_SI Recursive 的使命 | meng shao(@shao__meng) | event_signature | 11,858 |
| item_c8aa2dd69e2b4f12a6954bdf92ae0d17 | 哪个模型最牛逼？arena榜都被刷烂了。 要看就看 Vercel的最新报告。 20万个项目，7个月十万亿个 token的消耗分析，有些结论有意思： 1. 按费用 | 向阳乔木(@vista8) | thread_signature | 10,414 |
| item_5af5b0c651eb4d6dbe3a4173312d28b8 | The future of the industry involves the model and product evolving together rath | Fireworks AI(@FireworksAI_HQ) | thread_signature | 9,448 |
| item_6158804009654a348b271d1235155975 | With the new Chrome extension, Codex can quickly move through repetitive browser | OpenAI(@OpenAI) | event_signature | 9,326 |
| item_088c6d5128b44f2ab4ef70f800809d11 | playing around with local AI models after I recently built out my home lab (DGX  | andrew chen(@andrewchen) | event_signature | 8,702 |
| item_e6f115055b3b43cd9bcc6d7189b70cfd | We've partnered with @OpenAI to offer GPT-5.5 in Devin at 50% off through May 14 | Cognition(@cognition_labs) | event_signature | 8,685 |
| item_d743cfc40753479a81a1b6b28739d291 | This is how you announce a compute deal. Anthropic drops a thread: 1. Starts wit | Aadit Sheth(@aaditsh) | event_signature | 8,533 |
| item_e8c1433e1223438ca1da6a754d88f42c | Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用  | AI Will(@FinanceYF5) | thread_signature | 8,347 |

## Top 10 Most Expensive Calls

| Call ID | Stage | Tokens | Success | Variant | Items |
|---|---|---|---|---|---|
| 315 | item_cluster_relation | 9,021 | True | full | 9 |
| 3 | item_card | 8,901 | True | full | 5 |
| 313 | item_cluster_relation | 8,564 | True | full | 9 |
| 312 | item_cluster_relation | 8,492 | True | full | 10 |
| 43 | item_card | 8,174 | True | full | 5 |
| 2 | item_card | 8,138 | True | full | 5 |
| 311 | item_cluster_relation | 7,870 | True | full | 9 |
| 322 | item_cluster_relation | 7,726 | True | full | 11 |
| 41 | item_card | 7,547 | True | full | 5 |
| 7 | item_card | 7,459 | True | full | 5 |
