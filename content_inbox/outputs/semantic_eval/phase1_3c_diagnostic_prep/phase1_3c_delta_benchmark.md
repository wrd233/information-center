# Phase 1.3c Delta Benchmark

## Summary

- Total rows: 30
- Complements existing 50-row Step 1 benchmark (38 existing IDs excluded)

## Distribution by Kind

| Kind | Count |
|---|---|
| single_item_chinese_fn | 11 |
| single_item_garbage_product | 19 |

## All Benchmark Rows

### delta_001: single_item_chinese_fn
- **Item**: item_815fb633b2c14ae7ace5554fbaccd60f
- **Source**: 李继刚(@lijigang_com)
- **Title**: 在「世界刺激」和「你的反应」之间，有一片空间，那里是「你对它的解释」，像是一面观察透镜。 那片空间，目前看来，是语言搭建起来的。 当切换对一个刺激的语言描述时，「你的反应」就会跟着变。 有时候，...
- **Current**: level=reject, action=other, actor=, product=
- **Recommended**: level=reject, action=other, actor=, product=
- **Reason**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'weak_action_without_entity', 'semantic_level_reject']

### delta_002: single_item_chinese_fn
- **Item**: item_12eda743705a4e9497ce8b40bbd7c4b0
- **Source**: orange.ai(@oran_ge)
- **Title**: 五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...
- **Current**: level=thread_signature, action=pricing, actor=, product=CERX3N35
- **Recommended**: level=event_signature, action=pricing, actor=ColaOS, product=CERX3N35
- **Reason**: Chinese false negative: likely_false_negative_thread. ['semantic_level_thread_signature']

### delta_003: single_item_chinese_fn
- **Item**: item_4f4c39a8207b4b0187b880edfea031c4
- **Source**: orange.ai(@oran_ge)
- **Title**: 有位朋友创业做的好好的，又赚钱又开心又不用上班... 结果天天被投资人 PUA 说要融资搞架构找联创 all in 什么的 我说你活在美好的未来，他们还在苦逼的过去 别听他们的 follow your...
- **Current**: level=reject, action=funding, actor=, product=
- **Recommended**: level=thread_signature, action=funding, actor=PUA, product=有位朋友创业做的
- **Reason**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'semantic_level_reject']

### delta_004: single_item_chinese_fn
- **Item**: item_e891530dd3a1420da85a9d9a7ec1378d
- **Source**: orange.ai(@oran_ge)
- **Title**: 李想 × 老罗播客笔记 AI 与一人公司 李想：AI 是生产力和劳动力的技术。我现在不太相信一人公司。很多一人公司都在更新内容来验证这个概念成立，但验证了一段时间之后发现，他们每天更新的事情就是 ...
- **Current**: level=reject, action=adoption_metric, actor=, product=
- **Recommended**: level=thread_signature, action=adoption_metric, actor=OpenClaw, product=OpenClaw
- **Reason**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'semantic_level_reject']

### delta_005: single_item_chinese_fn
- **Item**: item_ef32d9713ac8427a91271666294ec161
- **Source**: orange.ai(@oran_ge)
- **Title**: 企业里的人+Agent 协作产品 Syncless 发布了
- **Current**: level=thread_signature, action=release, actor=, product=Yeuoly1
- **Recommended**: level=event_signature, action=release, actor=Agent, product=Yeuoly1
- **Reason**: Chinese false negative: likely_false_negative_thread. ['semantic_level_thread_signature']

### delta_006: single_item_chinese_fn
- **Item**: item_afe50ae6a16d4bf9ba653e75cf32829d
- **Source**: orange.ai(@oran_ge)
- **Title**: 我们不断地去思考协作的本质是什么 团队之间真正需要对齐的是什么 只有把沟通协作的模型想透彻 才能做出 Human-Agent 产品
- **Current**: level=reject, action=other, actor=, product=
- **Recommended**: level=thread_signature, action=other, actor=Human-Agent, product=我们不断地去思考
- **Reason**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'weak_action_without_entity', 'semantic_level_reject']

### delta_007: single_item_chinese_fn
- **Item**: item_974fcb9fd04b4f188ef1c5fa2d39b98b
- **Source**: 歸藏(guizang.ai)(@op7418)
- **Title**: 嘉琛的 bridge 有些设计和能力真的很顶
- **Current**: level=reject, action=technical_blog, actor=, product=
- **Recommended**: level=event_signature, action=technical_blog, actor=Jc He, product=bridge
- **Reason**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'semantic_level_reject']

### delta_008: single_item_chinese_fn
- **Item**: item_9d2e5c5ad045467688302f8d8df3acde
- **Source**: orange.ai(@oran_ge)
- **Title**: 开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。
- **Current**: level=reject, action=release, actor=, product=
- **Recommended**: level=event_signature, action=release, actor=CLI, product=开源一个月的时间
- **Reason**: Chinese false negative: likely_false_negative_event. ['missing_concrete_actor_or_product', 'weak_action_without_entity', 'semantic_level_reject']

### delta_009: single_item_chinese_fn
- **Item**: item_ff8c9467986d426e90becc6e1ecf654e
- **Source**: orange.ai(@oran_ge)
- **Title**: 人只有在真实的环境里才能做出正确的决定。 人类学研究表明，人类的决策过程主要是由激素推动的，知识，经验，理智在这个过程中所起的作用并不大。 我们往往是做出决定之后，再用智慧去寻找证据以便证明自己的决定...
- **Current**: level=reject, action=research_paper, actor=, product=
- **Recommended**: level=thread_signature, action=research_paper, actor=, product=skin in the game
- **Reason**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'semantic_level_reject']

### delta_010: single_item_chinese_fn
- **Item**: item_fd493ad98cdb483a9ae3d1da67788425
- **Source**: orange.ai(@oran_ge)
- **Title**: 实践是获得真理和获悉真相的唯一途径。
- **Current**: level=reject, action=case_study, actor=, product=
- **Recommended**: level=thread_signature, action=case_study, actor=Powered, product=实践是获得真理和
- **Reason**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'semantic_level_reject']

### delta_011: single_item_chinese_fn
- **Item**: item_107661efeb1343b5b3a1576c6a4a39db
- **Source**: orange.ai(@oran_ge)
- **Title**: 老黄当年决定做 CUDA 的时候 大概也没想到后来会有一万个人为这个决定辩经 人类太沉迷寻找证据寻找因果了
- **Current**: level=reject, action=research_paper, actor=, product=
- **Recommended**: level=thread_signature, action=research_paper, actor=CUDA, product=CUDA
- **Reason**: Chinese false negative: likely_false_negative_thread. ['missing_concrete_actor_or_product', 'semantic_level_reject']

### delta_012: single_item_garbage_product
- **Item**: item_4c1cf2b00ead48d8bbd63164e51441d5
- **Source**: Genspark(@genspark_ai)
- **Title**: tomorrow we're going live 😎 Genspark Shipped — our new monthly show breaking down everything we sh...
- **Current**: level=event_signature, action=event, actor=Microsoft, product=sow0e7ym
- **Recommended**: level=event_signature, action=event, actor=Microsoft, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'sow0e7ym' — random_alphanumeric_token

### delta_013: single_item_garbage_product
- **Item**: item_249695641b6041f6a0ddff0f7a76e951
- **Source**: Jerry Liu(@jerryjliu0)
- **Title**: We're hosting a pregame for SF First Thursdays 🎉 In honor of May 4th today, we're making it Star ...
- **Current**: level=event_signature, action=pricing, actor=LlamaIndex, product=May 4th
- **Recommended**: level=event_signature, action=pricing, actor=LlamaIndex, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'May 4th' — contains_date_fragment, is_month_day_phrase

### delta_014: single_item_garbage_product
- **Item**: item_4b1ececba3bb49348fbcc789e5ddffe6
- **Source**: Patrick Loeber(@patloeber)
- **Title**: - Docs: https://t.co/qoUnGI1hcM - Cookbook: https://t.co/Hv16MQVGil - Cloudflare worker example repo...
- **Current**: level=event_signature, action=integration, actor=google, product=gemini-api
- **Recommended**: level=event_signature, action=integration, actor=[FIX], product=gemini-api
- **Reason**: Garbage actor: 'google' — random_alphanumeric_token

### delta_015: single_item_garbage_product
- **Item**: item_423819d009fe4f0da14949d06b8e720d
- **Source**: eric zakariasson(@ericzakariasson)
- **Title**: here's me using debug mode to fix a small bug in an swift app i just built issue was the initial ch...
- **Current**: level=event_signature, action=feature_update, actor=cursor, product=just built issue was the initial characters
- **Recommended**: level=event_signature, action=feature_update, actor=[FIX], product=just built issue was the initial characters
- **Reason**: Garbage actor: 'cursor' — random_alphanumeric_token

### delta_016: single_item_garbage_product
- **Item**: item_2d5849395e6c498086aa1890e6753223
- **Source**: Runway(@runwayml)
- **Title**: Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...
- **Current**: level=thread_signature, action=other, actor=Runway, product=June 4th
- **Recommended**: level=thread_signature, action=other, actor=Runway, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'June 4th' — contains_date_fragment, is_month_day_phrase

### delta_017: single_item_garbage_product
- **Item**: item_fe55c9a3aabd499a89176d9c44242782
- **Source**: Runway(@runwayml)
- **Title**: RSVP: https://t.co/MgsZXl0gwp
- **Current**: level=thread_signature, action=other, actor=, product=iobqd8a9
- **Recommended**: level=thread_signature, action=other, actor=, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'iobqd8a9' — random_alphanumeric_token

### delta_018: single_item_garbage_product
- **Item**: item_92a9e82e74654bf695b05644aed07005
- **Source**: Jerry Liu(@jerryjliu0)
- **Title**: I’m excited to announce that @llama_index is on the @CBInsights AI 100 list for 2026 🔥 We’re on a ...
- **Current**: level=event_signature, action=integration, actor=llamaindex, product=AI 100
- **Recommended**: level=event_signature, action=integration, actor=[FIX], product=AI 100
- **Reason**: Garbage actor: 'llamaindex' — random_alphanumeric_token

### delta_019: single_item_garbage_product
- **Item**: item_d595ccdff9a8456b98935755e83b253d
- **Source**: Firecrawl(@firecrawl_dev)
- **Title**: Our PHP SDK is live 🔥 Scrape any page to markdown, run live web searches, and navigate dynamic sit...
- **Current**: level=event_signature, action=integration, actor=firecrawl, product=and navigate dynamic sit... Our PHP SDK
- **Recommended**: level=event_signature, action=integration, actor=[FIX], product=and navigate dynamic sit... Our PHP SDK
- **Reason**: Garbage actor: 'firecrawl' — random_alphanumeric_token

### delta_020: single_item_garbage_product
- **Item**: item_614f1ae12cf34cfb8ef9e40013180259
- **Source**: Cursor(@cursor_ai)
- **Title**: Use a template from our marketplace to automate CI investigations: https://t.co/ou0OHzwvtq
- **Current**: level=thread_signature, action=other, actor=cursor, product=
- **Recommended**: level=thread_signature, action=other, actor=[FIX], product=
- **Reason**: Garbage actor: 'cursor' — random_alphanumeric_token

### delta_021: single_item_garbage_product
- **Item**: item_6186ef3f1a69438bba7e813c7ec9ed78
- **Source**: Latent.Space(@latentspacepod)
- **Title**: 🔬Doing Vibe Physics The full story of how GPT‑5.x derived new results in theoretical physics and q...
- **Current**: level=event_signature, action=partnership, actor=GPT5, product=GPT5
- **Recommended**: level=event_signature, action=partnership, actor=GPT5, product=GPT5
- **Reason**: Garbage object: 'markchen90' — random_alphanumeric_token

### delta_022: single_item_garbage_product
- **Item**: item_eede5be929844a7a9372b449c3406d54
- **Source**: Harrison Chase(@hwchase17)
- **Title**: "Traces everywhere. Feedback loop? Nowhere"
- **Current**: level=thread_signature, action=other, actor=LangChain, product=hwchase17
- **Recommended**: level=thread_signature, action=other, actor=LangChain, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'hwchase17' — random_alphanumeric_token

### delta_023: single_item_garbage_product
- **Item**: item_5c72b7f0be8f43d2a275c1e7f48d2c61
- **Source**: ElevenLabs(@elevenlabsio)
- **Title**: One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...
- **Current**: level=event_signature, action=case_study, actor=elevenlabs, product=One agent
- **Recommended**: level=event_signature, action=case_study, actor=[FIX], product=One agent
- **Reason**: Garbage actor: 'elevenlabs' — random_alphanumeric_token

### delta_024: single_item_garbage_product
- **Item**: item_5af5b0c651eb4d6dbe3a4173312d28b8
- **Source**: Fireworks AI(@FireworksAI_HQ)
- **Title**: The future of the industry involves the model and product evolving together rather than existing as ...
- **Current**: level=thread_signature, action=feature_update, actor=nvidia, product=
- **Recommended**: level=thread_signature, action=feature_update, actor=[FIX], product=
- **Reason**: Garbage actor: 'nvidia' — random_alphanumeric_token

### delta_025: single_item_garbage_product
- **Item**: item_d743cfc40753479a81a1b6b28739d291
- **Source**: Aadit Sheth(@aaditsh)
- **Title**: This is how you announce a compute deal. Anthropic drops a thread: 1. Starts with what changes for...
- **Current**: level=event_signature, action=adoption_metric, actor=Anthropic, product=claudeai
- **Recommended**: level=event_signature, action=adoption_metric, actor=Anthropic, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'claudeai' — random_alphanumeric_token

### delta_026: single_item_garbage_product
- **Item**: item_e22aa290a8f74b5a88f75179e33a69b0
- **Source**: Akshay Kothari(@akothari)
- **Title**: tweets like this are just the perfect fuel to keep going. it's similar to going to your neighborhood...
- **Current**: level=thread_signature, action=other, actor=notion, product=
- **Recommended**: level=thread_signature, action=other, actor=[FIX], product=
- **Reason**: Garbage actor: 'notion' — random_alphanumeric_token

### delta_027: single_item_garbage_product
- **Item**: item_a8fe82c191a0491aa4f3a7d493ae6a22
- **Source**: Lovable(@lovable_dev)
- **Title**: Read more: https://t.co/a0mLBTxSYM
- **Current**: level=thread_signature, action=other, actor=lovable, product=
- **Recommended**: level=thread_signature, action=other, actor=[FIX], product=
- **Reason**: Garbage actor: 'lovable' — random_alphanumeric_token

### delta_028: single_item_garbage_product
- **Item**: item_29c1459ec5d0457a9a7348fce60e4d89
- **Source**: Anthropic(@AnthropicAI)
- **Title**: AI-driven R&D We expect AI systems to contribute more and more to AI R&D: that is, to be ab...
- **Current**: level=thread_signature, action=other, actor=, product=recursive
- **Recommended**: level=thread_signature, action=other, actor=, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'recursive' — random_alphanumeric_token

### delta_029: single_item_garbage_product
- **Item**: item_fd21792e60c0494799ec47de56ddcd52
- **Source**: Fellou(@FellouAI)
- **Title**: Most hackathons end at the demo. But product value starts after that: Do people open it? Use it? Com...
- **Current**: level=thread_signature, action=pricing, actor=, product=ay4dy8o5
- **Recommended**: level=thread_signature, action=pricing, actor=, product=[FIX: extract from title/entities]
- **Reason**: Garbage product_or_model: 'ay4dy8o5' — random_alphanumeric_token

### delta_030: single_item_garbage_product
- **Item**: item_6497b2f027a24a3eb9a4b9680c6af220
- **Source**: Fellou(@FellouAI)
- **Title**: Hi NYC builders — If you have an app idea sitting in your Notes, this might be your sign. @EazoAI ...
- **Current**: level=thread_signature, action=adoption_metric, actor=, product=a 48-hour
- **Recommended**: level=thread_signature, action=adoption_metric, actor=, product=a 48-hour
- **Reason**: Garbage object: 'ay4dy8o5' — random_alphanumeric_token

