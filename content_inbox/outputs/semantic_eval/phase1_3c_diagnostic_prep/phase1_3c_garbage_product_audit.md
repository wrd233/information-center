# Phase 1.3c Garbage Product/Actor Audit

## Summary

- Total non-reject signatures analyzed: 206
- Suspicious field instances found: 110
- Blockers: 36
- Warnings: 74

## Suspicion Category Breakdown

| Category | Count |
|---|---|
| long_phrase_gt_6_words | 44 |
| random_alphanumeric_token | 30 |
| numeric_preposition_fragment | 16 |
| contains_sentence_punctuation_in_long_phrase | 16 |
| starts_with_weak_preposition | 9 |
| starts_with_verb_phrase | 9 |
| short_lowercase_non_entity | 3 |
| contains_date_fragment | 2 |
| is_month_day_phrase | 2 |
| generic_for_every_pattern | 1 |
| contains_url_fragment | 1 |

## Blocker Garbage Examples

### item_4c1cf2b00ead48d8bbd63164e51441d5 — `sow0e7ym`
- **Source**: Genspark(@genspark_ai)
- **Title**: tomorrow we're going live 😎 Genspark Shipped — our new monthly show breaking down everything we sh...
- **Field**: product_or_model
- **Level/Action**: event_signature/event
- **Actor**: Microsoft
- **Product**: sow0e7ym
- **Why**: random_alphanumeric_token

### item_249695641b6041f6a0ddff0f7a76e951 — `May 4th`
- **Source**: Jerry Liu(@jerryjliu0)
- **Title**: We're hosting a pregame for SF First Thursdays 🎉 In honor of May 4th today, we're making it Star ...
- **Field**: product_or_model
- **Level/Action**: event_signature/pricing
- **Actor**: LlamaIndex
- **Product**: May 4th
- **Why**: contains_date_fragment, is_month_day_phrase

### item_249695641b6041f6a0ddff0f7a76e951 — `i98ittfi`
- **Source**: Jerry Liu(@jerryjliu0)
- **Title**: We're hosting a pregame for SF First Thursdays 🎉 In honor of May 4th today, we're making it Star ...
- **Field**: object
- **Level/Action**: event_signature/pricing
- **Actor**: LlamaIndex
- **Product**: May 4th
- **Why**: random_alphanumeric_token

### item_4b1ececba3bb49348fbcc789e5ddffe6 — `google`
- **Source**: Patrick Loeber(@patloeber)
- **Title**: - Docs: https://t.co/qoUnGI1hcM - Cookbook: https://t.co/Hv16MQVGil - Cloudflare worker example repo...
- **Field**: actor
- **Level/Action**: event_signature/integration
- **Actor**: google
- **Product**: gemini-api
- **Why**: random_alphanumeric_token

### item_423819d009fe4f0da14949d06b8e720d — `cursor`
- **Source**: eric zakariasson(@ericzakariasson)
- **Title**: here's me using debug mode to fix a small bug in an swift app i just built issue was the initial ch...
- **Field**: actor
- **Level/Action**: event_signature/feature_update
- **Actor**: cursor
- **Product**: just built issue was the initial characters
- **Why**: random_alphanumeric_token

### item_2d5849395e6c498086aa1890e6753223 — `June 4th`
- **Source**: Runway(@runwayml)
- **Title**: Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...
- **Field**: product_or_model
- **Level/Action**: thread_signature/other
- **Actor**: Runway
- **Product**: June 4th
- **Why**: contains_date_fragment, is_month_day_phrase

### item_fe55c9a3aabd499a89176d9c44242782 — `iobqd8a9`
- **Source**: Runway(@runwayml)
- **Title**: RSVP: https://t.co/MgsZXl0gwp
- **Field**: product_or_model
- **Level/Action**: thread_signature/other
- **Actor**: 
- **Product**: iobqd8a9
- **Why**: random_alphanumeric_token

### item_92a9e82e74654bf695b05644aed07005 — `llamaindex`
- **Source**: Jerry Liu(@jerryjliu0)
- **Title**: I’m excited to announce that @llama_index is on the @CBInsights AI 100 list for 2026 🔥 We’re on a ...
- **Field**: actor
- **Level/Action**: event_signature/integration
- **Actor**: llamaindex
- **Product**: AI 100
- **Why**: random_alphanumeric_token

### item_d595ccdff9a8456b98935755e83b253d — `firecrawl`
- **Source**: Firecrawl(@firecrawl_dev)
- **Title**: Our PHP SDK is live 🔥 Scrape any page to markdown, run live web searches, and navigate dynamic sit...
- **Field**: actor
- **Level/Action**: event_signature/integration
- **Actor**: firecrawl
- **Product**: and navigate dynamic sit... Our PHP SDK
- **Why**: random_alphanumeric_token

### item_614f1ae12cf34cfb8ef9e40013180259 — `cursor`
- **Source**: Cursor(@cursor_ai)
- **Title**: Use a template from our marketplace to automate CI investigations: https://t.co/ou0OHzwvtq
- **Field**: actor
- **Level/Action**: thread_signature/other
- **Actor**: cursor
- **Product**: 
- **Why**: random_alphanumeric_token

### item_6186ef3f1a69438bba7e813c7ec9ed78 — `markchen90`
- **Source**: Latent.Space(@latentspacepod)
- **Title**: 🔬Doing Vibe Physics The full story of how GPT‑5.x derived new results in theoretical physics and q...
- **Field**: object
- **Level/Action**: event_signature/partnership
- **Actor**: GPT5
- **Product**: GPT5
- **Why**: random_alphanumeric_token

### item_eede5be929844a7a9372b449c3406d54 — `hwchase17`
- **Source**: Harrison Chase(@hwchase17)
- **Title**: "Traces everywhere. Feedback loop? Nowhere"
- **Field**: product_or_model
- **Level/Action**: thread_signature/other
- **Actor**: LangChain
- **Product**: hwchase17
- **Why**: random_alphanumeric_token

### item_5c72b7f0be8f43d2a275c1e7f48d2c61 — `elevenlabs`
- **Source**: ElevenLabs(@elevenlabsio)
- **Title**: One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...
- **Field**: actor
- **Level/Action**: event_signature/case_study
- **Actor**: elevenlabs
- **Product**: One agent
- **Why**: random_alphanumeric_token

### item_5af5b0c651eb4d6dbe3a4173312d28b8 — `nvidia`
- **Source**: Fireworks AI(@FireworksAI_HQ)
- **Title**: The future of the industry involves the model and product evolving together rather than existing as ...
- **Field**: actor
- **Level/Action**: thread_signature/feature_update
- **Actor**: nvidia
- **Product**: 
- **Why**: random_alphanumeric_token

### item_d743cfc40753479a81a1b6b28739d291 — `claudeai`
- **Source**: Aadit Sheth(@aaditsh)
- **Title**: This is how you announce a compute deal. Anthropic drops a thread: 1. Starts with what changes for...
- **Field**: product_or_model
- **Level/Action**: event_signature/adoption_metric
- **Actor**: Anthropic
- **Product**: claudeai
- **Why**: random_alphanumeric_token

### item_e22aa290a8f74b5a88f75179e33a69b0 — `notion`
- **Source**: Akshay Kothari(@akothari)
- **Title**: tweets like this are just the perfect fuel to keep going. it's similar to going to your neighborhood...
- **Field**: actor
- **Level/Action**: thread_signature/other
- **Actor**: notion
- **Product**: 
- **Why**: random_alphanumeric_token

### item_a8fe82c191a0491aa4f3a7d493ae6a22 — `lovable`
- **Source**: Lovable(@lovable_dev)
- **Title**: Read more: https://t.co/a0mLBTxSYM
- **Field**: actor
- **Level/Action**: thread_signature/other
- **Actor**: lovable
- **Product**: 
- **Why**: random_alphanumeric_token

### item_29c1459ec5d0457a9a7348fce60e4d89 — `recursive`
- **Source**: Anthropic(@AnthropicAI)
- **Title**: AI-driven R&D We expect AI systems to contribute more and more to AI R&D: that is, to be ab...
- **Field**: product_or_model
- **Level/Action**: thread_signature/other
- **Actor**: 
- **Product**: recursive
- **Why**: random_alphanumeric_token

### item_fd21792e60c0494799ec47de56ddcd52 — `ay4dy8o5`
- **Source**: Fellou(@FellouAI)
- **Title**: Most hackathons end at the demo. But product value starts after that: Do people open it? Use it? Com...
- **Field**: product_or_model
- **Level/Action**: thread_signature/pricing
- **Actor**: 
- **Product**: ay4dy8o5
- **Why**: random_alphanumeric_token

### item_6497b2f027a24a3eb9a4b9680c6af220 — `ay4dy8o5`
- **Source**: Fellou(@FellouAI)
- **Title**: Hi NYC builders — If you have an app idea sitting in your Notes, this might be your sign. @EazoAI ...
- **Field**: object
- **Level/Action**: thread_signature/adoption_metric
- **Actor**: 
- **Product**: a 48-hour
- **Why**: random_alphanumeric_token

### item_d5ed03ebeeb64a65ac586cd6c80c7033 — `trq212`
- **Source**: elvis(@omarsar0)
- **Title**: My point exactly:
- **Field**: product_or_model
- **Level/Action**: thread_signature/other
- **Actor**: 
- **Product**: trq212
- **Why**: random_alphanumeric_token

### item_a43f0ae85d174772b9b71d744f506c7a — `omarsar0`
- **Source**: elvis(@omarsar0)
- **Title**: My favourite new stack: Agents + MCP + Markdown + HTML “Files over apps” is a vibe!
- **Field**: product_or_model
- **Level/Action**: thread_signature/feature_update
- **Actor**: 
- **Product**: omarsar0
- **Why**: random_alphanumeric_token

### item_d3b416ae107c41fdae63f6f84b3ebd9f — `omarsar0`
- **Source**: elvis(@omarsar0)
- **Title**: More important takeaway: use both Markdown and HTML. Your agents will thank you for it.
- **Field**: object
- **Level/Action**: thread_signature/feature_update
- **Actor**: 
- **Product**: use both Markdown and HTML. Your agents
- **Why**: random_alphanumeric_token

### item_1b7d128007e744d7a6b0fcdcaaea4015 — `replit`
- **Source**: Replit ⠕(@Replit)
- **Title**: "You did not become less capable when you became a mother. You became more capable in ways that don'...
- **Field**: actor
- **Level/Action**: thread_signature/other
- **Actor**: replit
- **Product**: 
- **Why**: random_alphanumeric_token

### item_2d5bf052d569491cbccb81c0a4d470d1 — `o1`
- **Source**: Greg Brockman(@gdb)
- **Title**: /goal is underrated
- **Field**: product_or_model
- **Level/Action**: event_signature/pricing
- **Actor**: GPT-5.5
- **Product**: o1
- **Why**: short_lowercase_non_entity

### item_af0866973f4f4d34b1199f81580190cb — `openai`
- **Source**: OpenAI Developers(@OpenAIDevs)
- **Title**: Fork the repo and build your own voice-to-action workflow. https://t.co/G3ag8QeBl8
- **Field**: actor
- **Level/Action**: thread_signature/other
- **Actor**: openai
- **Product**: 
- **Why**: random_alphanumeric_token

### item_c7f4f61b77a24f5b8a42cb44fa7f5667 — `claude.com`
- **Source**: 小互(@imxiaohu)
- **Title**: Anthropic 提到的典型用法包括：同时派发多个想法、让不同 Agent 配合不同 skill 生成 PR、管理长期运行任务，比如 PR babysitter、dashboard updater，...
- **Field**: product_or_model
- **Level/Action**: event_signature/feature_update
- **Actor**: Anthropic
- **Product**: claude.com
- **Why**: contains_url_fragment

### item_d97bcf701a984509bbbe09a8045a30d8 — `ns123abc`
- **Source**: Gary Marcus(@GaryMarcus)
- **Title**: for now. when that changes, revenue may slow and the whole thing might fall apart.
- **Field**: product_or_model
- **Level/Action**: thread_signature/adoption_metric
- **Actor**: 
- **Product**: ns123abc
- **Why**: random_alphanumeric_token

### item_0ac7d3f53d6b497d81181a0f24f636d7 — `haider1`
- **Source**: Gary Marcus(@GaryMarcus)
- **Title**: counterpoint: i have no interest in a company that says we will roll everything out to anybody regar...
- **Field**: product_or_model
- **Level/Action**: event_signature/pricing
- **Actor**: anthropic
- **Product**: haider1
- **Why**: random_alphanumeric_token

### item_0ac7d3f53d6b497d81181a0f24f636d7 — `anthropic`
- **Source**: Gary Marcus(@GaryMarcus)
- **Title**: counterpoint: i have no interest in a company that says we will roll everything out to anybody regar...
- **Field**: actor
- **Level/Action**: event_signature/pricing
- **Actor**: anthropic
- **Product**: haider1
- **Why**: random_alphanumeric_token

### item_e729ffc533864f2d87731a6790437b91 — `k8s`
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: OpenShell v0.0.40 🔀 local-domain service routing in the gateway ☸️ k8s node scheduling + toleratio...
- **Field**: object
- **Level/Action**: event_signature/release
- **Actor**: NVIDIA
- **Product**: OpenShell v0.0.40
- **Why**: short_lowercase_non_entity

### item_5481d9d7e3204dfab120d8ffd41e5b7b — `zhenghy723`
- **Source**: Y Combinator(@ycombinator)
- **Title**: YouArt (@YouArtStudio) empowers storytellers to create AI films and series with leading video agents...
- **Field**: object
- **Level/Action**: thread_signature/company_launch
- **Actor**: 
- **Product**: films and series with leading video agents
- **Why**: random_alphanumeric_token

### item_d5e175dae5ac44d18d8bac85fbf27d13 — `hwchase17`
- **Source**: LangChain(@LangChainAI)
- **Title**: Coming up… 🎤 A conversation on the future of agents with @andrewng + @hwchase17 🎤A fireside chat...
- **Field**: object
- **Level/Action**: event_signature/event
- **Actor**: LangChain
- **Product**: conversation on the future of agents
- **Why**: random_alphanumeric_token

### item_533c83124ba84f25a2ec6e0a2d712255 — `hwchase17`
- **Source**: NVIDIA AI(@NVIDIAAI)
- **Title**: @hwchase17 We’re excited to be part of this initiative 🤝
- **Field**: product_or_model
- **Level/Action**: thread_signature/other
- **Actor**: LangChain
- **Product**: hwchase17
- **Why**: random_alphanumeric_token

### item_3a2d72eb9cb14b69a58fcfc130eeec29 — `vercel`
- **Source**: 向阳乔木(@vista8)
- **Title**: 原文：https://t.co/pVTjim12Ce 翻译：https://t.co/BhYuEybcTW
- **Field**: actor
- **Level/Action**: thread_signature/other
- **Actor**: vercel
- **Product**: 
- **Why**: random_alphanumeric_token

### item_26e607330dd64f728e4d0d7aa32cba37 — `a 0`
- **Source**: Marc Andreessen 🇺🇸(@pmarca)
- **Title**: Nuclear power plants were always ultra-safe as well; total global deaths from civilian nuclear power...
- **Field**: product_or_model
- **Level/Action**: thread_signature/pricing
- **Actor**: 
- **Product**: a 0
- **Why**: numeric_preposition_fragment, short_lowercase_non_entity


## Warning Examples

- **item_0cabbd2be8224c239efd856641a51f59**: `data then skip the interface entirely Agents` (product_or_model) — long_phrase_gt_6_words
- **item_0cabbd2be8224c239efd856641a51f59**: `hides friend activity from the public API` (object) — long_phrase_gt_6_words
- **item_aec7ba3620ae40b7a752e7f5f1543bb9**: `Git semantics for every file your agent` (product_or_model) — long_phrase_gt_6_words, generic_for_every_pattern
- **item_c52026599fe74d0798704579bb2e2507**: `around 1897` (product_or_model) — numeric_preposition_fragment
- **item_c52026599fe74d0798704579bb2e2507**: `about 2` (object) — numeric_preposition_fragment
- **item_c96041fbd0a94ecfa37626041240912d**: `We shipped Webhooks in the Gemini API` (product_or_model) — long_phrase_gt_6_words
- **item_2caa7c0db00c43d587471db36cb41da7**: `initiatives to help enterprises deploy AI agents` (object) — long_phrase_gt_6_words
- **item_423819d009fe4f0da14949d06b8e720d**: `just built issue was the initial characters` (product_or_model) — starts_with_weak_preposition, long_phrase_gt_6_words
- **item_5d8c86286d4b41cab3f469c659183a58**: `of 12M` (product_or_model) — numeric_preposition_fragment
- **item_92a9e82e74654bf695b05644aed07005**: `accessible to both humans and AI agents` (object) — long_phrase_gt_6_words
- **item_b6a1daec5e7c4789ba183ccc53b1f379**: `brings in licensed data for professional finance` (object) — long_phrase_gt_6_words
- **item_d595ccdff9a8456b98935755e83b253d**: `and navigate dynamic sit... Our PHP SDK` (product_or_model) — starts_with_weak_preposition, contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_d62784d9a97c48c780e9c19536c740e9**: `everything when you build products for Finance` (product_or_model) — long_phrase_gt_6_words
- **item_d62784d9a97c48c780e9c19536c740e9**: `Every output number on Perplexity Computer` (object) — starts_with_weak_preposition
- **item_14b505e34c184cc28ffeaaa3d53efe99**: `is now live on the xAI API` (object) — long_phrase_gt_6_words
- **item_e7f5295b80a94aa9a261b681feeb8f51**: `and Enterprise subscribers in Perplexity and Computer` (product_or_model) — starts_with_weak_preposition, long_phrase_gt_6_words
- **item_0f6325210acb4787b343cb407a0c2b3e**: `run Deep and Wide Research on sources` (object) — long_phrase_gt_6_words, starts_with_verb_phrase
- **item_5bc38f3d986d45d8997357e519c22e9f**: `launch multimodal support in the Gemini API` (product_or_model) — long_phrase_gt_6_words, starts_with_verb_phrase
- **item_1dee0f3f2dc544748c62612a17517b5a**: `CI failures. Set up always-on agents` (product_or_model) — contains_sentence_punctuation_in_long_phrase
- **item_f63fe66b9d914ea98803c096200cc894**: `a 24` (product_or_model) — numeric_preposition_fragment
- **item_f63fe66b9d914ea98803c096200cc894**: `away free Browser Use Boxes. Your agent` (object) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_1b391ec0115148f289aef512fc013217**: `to 3x` (object) — numeric_preposition_fragment
- **item_c31ab2c724f145d09732f4c99c8cbe1e**: `can now generate videos using Hermes Agent` (object) — long_phrase_gt_6_words
- **item_e8e0f0d00a0e409bbe75648f03a363be**: `to use it to power an agent` (product_or_model) — starts_with_weak_preposition, long_phrase_gt_6_words
- **item_e8e0f0d00a0e409bbe75648f03a363be**: `you need to... agent` (object) — contains_sentence_punctuation_in_long_phrase
- **item_d5a78d239fcf4ef08a5711b32c66a68e**: `you unleashed your creativity on Replit Agent` (object) — long_phrase_gt_6_words
- **item_3db3d25a81ed4a80a4d4b8f130fa6455**: `Run an entire company with agents` (product_or_model) — starts_with_verb_phrase
- **item_8cb6ff7938184ee8bad316cbf67b3cb0**: `self-improving b... Hermes agent` (object) — contains_sentence_punctuation_in_long_phrase
- **item_3c4738cff2884affb1a618a66617a4a6**: `as the Inner Skill in Agentic Harness` (product_or_model) — starts_with_weak_preposition, long_phrase_gt_6_words
- **item_3c49f6c462a5492abe1d7ffeccea834b**: `up 130` (product_or_model) — numeric_preposition_fragment
- **item_3c49f6c462a5492abe1d7ffeccea834b**: `up 63` (object) — numeric_preposition_fragment
- **item_1d4c37b426ec4b7c9cb80d9bd9b7d96f**: `reach out across channels. Now your agents` (product_or_model) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_b37e433468004a78b7db33d32d563eba**: `context across channels and modalities. An agent` (product_or_model) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_b37e433468004a78b7db33d32d563eba**: `Powered by xgo.ing Agents` (object) — contains_sentence_punctuation_in_long_phrase
- **item_5c72b7f0be8f43d2a275c1e7f48d2c61**: `they are with ElevenAgents. Le... One agent` (object) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_e7705fd7adad4367b22bb92d9c324fdc**: `is now available in the Perplexity Agent` (object) — long_phrase_gt_6_words
- **item_f11f7dd74d6a4ec299727b8ea87173bf**: `time licensed financial data into our API` (product_or_model) — long_phrase_gt_6_words
- **item_f11f7dd74d6a4ec299727b8ea87173bf**: `along with verified and current web sources` (object) — long_phrase_gt_6_words
- **item_0b72c78c93b74bda99765e60bd423d46**: `to 100x` (product_or_model) — numeric_preposition_fragment
- **item_9bfecdd077ce488fa7af592dad937060**: `and the Gemini API` (product_or_model) — starts_with_weak_preposition
- **item_9074658486ba44b6aee380c2c04f81c7**: `Build AI agent` (product_or_model) — starts_with_verb_phrase
- **item_9074658486ba44b6aee380c2c04f81c7**: `Build AI agents` (object) — starts_with_verb_phrase
- **item_2c3511efb40a443cacd59eaaf93b3899**: `as well as your favorite AI agent` (product_or_model) — starts_with_weak_preposition, long_phrase_gt_6_words
- **item_4ed2086d20e3477685bc6883b6afd0b9**: `interesting edge cases. Spun up an agent` (product_or_model) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_29c1459ec5d0457a9a7348fce60e4d89**: `weeks reading 100s of public data sources` (object) — long_phrase_gt_6_words
- **item_687f55f00e0e4148b1520abe1a6d50d1**: `to 55` (product_or_model) — numeric_preposition_fragment
- **item_687f55f00e0e4148b1520abe1a6d50d1**: `to 45` (object) — numeric_preposition_fragment
- **item_acd90927cbce4f8ab13d322963c9dd87**: `directly from your terminal or AI agent` (product_or_model) — long_phrase_gt_6_words
- **item_ea5e144423244e6684c14af24ffd3220**: `models are now available in the Realtime` (product_or_model) — long_phrase_gt_6_words
- **item_ea5e144423244e6684c14af24ffd3220**: `Build production-ready voice agents` (object) — starts_with_verb_phrase
- **item_bb85d23bf9064dbca400bec1babc86e2**: `reasoning to voice agents. Voice agents` (product_or_model) — contains_sentence_punctuation_in_long_phrase
- **item_bb85d23bf9064dbca400bec1babc86e2**: `conversations unfold. Now available in the API` (object) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_6497b2f027a24a3eb9a4b9680c6af220**: `a 48-hour` (product_or_model) — numeric_preposition_fragment
- **item_29f8de4335f04a3eb9af5549844f158a**: `deeper into Vision leaderboard rankings at arena` (product_or_model) — long_phrase_gt_6_words
- **item_33517af4a0664f5898650838bace7688**: `A 3D` (object) — numeric_preposition_fragment
- **item_b9b7be392b7346a08c716c359d9868e1**: `AI creation stack is changing fast. Search` (product_or_model) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words
- **item_b9b7be392b7346a08c716c359d9868e1**: `helped us find information. Agents` (object) — contains_sentence_punctuation_in_long_phrase
- **item_a43f0ae85d174772b9b71d744f506c7a**: `information that lets you and your agents` (object) — long_phrase_gt_6_words
- **item_d6302b1f42db42e68580c335eb1688e9**: `Give Your Chat Agent` (product_or_model) — starts_with_verb_phrase
- **item_d3b416ae107c41fdae63f6f84b3ebd9f**: `use both Markdown and HTML. Your agents` (product_or_model) — contains_sentence_punctuation_in_long_phrase, long_phrase_gt_6_words, starts_with_verb_phrase
- **item_bd397ddcf6b64f7999a46b949604e465**: `lot more system engineering efforts around agents` (product_or_model) — long_phrase_gt_6_words
- **item_bd397ddcf6b64f7999a46b949604e465**: `that models agentic workflows as an operator` (object) — starts_with_weak_preposition, long_phrase_gt_6_words
- **item_50dfa7bbc83f42a38dd0df68ff58e893**: `about 80` (object) — numeric_preposition_fragment
- **item_d8007ede942944088ca27efb500bfd4c**: `faster by running up to 10 agents` (object) — long_phrase_gt_6_words
- **item_a87b9a71afb94bc7ab648f6e9a29f397**: `Try Parallel Agents` (product_or_model) — starts_with_verb_phrase
- **item_a87b9a71afb94bc7ab648f6e9a29f397**: `Powered by xgo.ing Try Parallel Agents` (object) — contains_sentence_punctuation_in_long_phrase
- **item_9c3b6ce177d54263899ce2fb01b47c3b**: `help you build AI apps and agents` (object) — long_phrase_gt_6_words
- **item_7491463f1ffa47dda0c93bac46c5ea42**: `up 80` (product_or_model) — numeric_preposition_fragment
- **item_12864804ee7b41ad805d2f31dde79a03**: `of 1` (product_or_model) — numeric_preposition_fragment
- **item_5481d9d7e3204dfab120d8ffd41e5b7b**: `films and series with leading video agents` (product_or_model) — long_phrase_gt_6_words
- **item_4372ac63bca04408a5ac197fa39f4122**: `coordinated opposition campaigns around our Utah projects` (product_or_model) — long_phrase_gt_6_words
- **item_872fa612db90470185ad9de676ca54a6**: `develop new metaphors for ambitious technology projects` (product_or_model) — long_phrase_gt_6_words
- **item_e6f115055b3b43cd9bcc6d7189b70cfd**: `now available in Devin as an Agent` (object) — long_phrase_gt_6_words
- **item_fef20066df524b90a1044d1b1ce3ab36**: `been doing very inefficiently on my computer` (object) — long_phrase_gt_6_words

## Known Valid Products (must not be over-rejected)

- `AI Security Summit`
- `Adialante`
- `Agent Harness`
- `Claude`
- `Claude Code`
- `Claude Opus`
- `Claude w`
- `Codex`
- `Colossus 1`
- `DGX Spark`
- `DGX spark`
- `DeepSeek-V4`
- `ElevenAgents`
- `Finance Search`
- `GPT Image`
- `GPT Image 2`
- `GPT-5.5`
- `Gemini Intelligence`
- `Gemma 4`
- `Gemma-4`
- `GitHub Copilot Desktop`
- `Googlebook`
- `Grok 4.3`
- `Hailuo AI App v2.10.0`
- `Hermes Agent`
- `Hermes agent`
- `ICML26`
- `Krea 2`
- `LangSmith Fleet`
- `NVIDIA Nemotron 3 Nano Omni`
- `Notion Custom Agents`
- `Notion Developer Platform`
- `Notion Workers`
- `OpenShell`
- `OpenShell v0.0.37`
- `OpenShell v0.0.40`
- `OpenShell v0.0.41`
- `PLAN0`
- `Perplexity Computer`
- `QVeris CLI`
- `Recursive`
- `SF 2026`
- `Seedance 2.0`
- `Stelline Developer Kit`
- `Token calling plan`
- `codex`
- `nemotron 3 nano omni`
