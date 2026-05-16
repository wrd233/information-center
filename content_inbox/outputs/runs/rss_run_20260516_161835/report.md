# RSS 批量输入 content-inbox 运行报告

- 开始时间：2026-05-16T08:18:35+00:00
- 结束时间：2026-05-16T08:27:12+00:00
- 日期：2026-05-16
- URL 模式：docker-host

## 1. 总览

- 选中 RSS 源数量：500
- 已处理源数量：500
- 成功源数量：454
- 失败源数量：46
- 已知失败跳过数量：0
- total_items：11175
- new_items：11173
- duplicate_items：0
- screened_items：11173
- recommended_items_from_api_response：0
- new_items_recommended：unknown
- final_inbox_items_from_this_run：0
- full_push_items_from_this_run：0
- incremental_push_items_from_this_run：0
- silent_items：0
- failed_items：0
- inbox 查询模式：from
- inbox 是否回退到 date=today：False

## 增量同步模式汇总

- 同步模式：until_existing
- 命中历史锚点的源数：2
- 新源基线同步数：452
- 老源未找到锚点数：0
- selected_items_for_processing 总计：11173

## 2. 统计口径说明

- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。
- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。
- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。
- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。
- source concurrency=24, llm_max_concurrency_requested=None, llm_max_concurrency_applied=None, screening_mode_requested=None, screening_mode_applied=None, timeout=60, sleep=1.0, limit_per_source=30

## 3. 各 RSS 源处理结果

| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | #UNTAG | Articles/科技与编程 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 2 | - 政府文件库 | Articles/国内政策 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 3 | - 求是网 | Articles/党政信息 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 4 | -LKs- | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 5 | 01Founder | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 6 | 3Blue1Brown | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 7 | 51吃瓜网 - 吃瓜爆料第一站，全网最快最全的吃瓜平台 | Articles/其他 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 8 | AGI Hunt | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 9 | AI Breakfast(@AiBreakfast) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 10 | AI Engineer(@aiDotEngineer) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 11 | AI Foundations | Videos | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 12 | AI SDK(@aisdk) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 13 | AI Will(@FinanceYF5) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 14 | AI at Meta(@AIatMeta) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 15 | AIGC开放社区 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 16 | AI产品银海 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 17 | AI产品阿颖 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 18 | AI产品黄叔 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 19 | AI前线 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 20 | AI故事计划 | Articles/微信公众号 | success | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 0 | 0 |  |
| 21 | AI洞察日报 RSS Feed | Articles | success | 7 | 7 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |  |
| 22 | AI科技评论 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 23 | AK(@_akhaliq) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 24 | APPSO | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 25 | Aadit Sheth(@aaditsh) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 26 | Adam D'Angelo(@adamdangelo) | SocialMedia | success | 16 | 16 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |  |
| 27 | Ahead of AI | Articles | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 28 | Airing 的博客 | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 29 | Akshay Kothari(@akothari) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 30 | Alex Albert(@alexalbert__) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 31 | AliAbdaal | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 32 | Aman Sanger(@amanrsanger) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 33 | Amjad Masad(@amasad) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 34 | Andrej Karpathy - YouTube | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 35 | Andrej Karpathy(@karpathy) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 36 | Andrew Ng(@AndrewYNg) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 37 | Anthropic(@AnthropicAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 38 | Anton Osika – eu/acc(@antonosika) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 39 | Aravind Srinivas(@AravSrinivas) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 40 | Arthur Mensch(@arthurmensch) | SocialMedia | success | 6 | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |  |
| 41 | Augment Code(@augmentcode) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 42 | Barsee &#128054;(@heyBarsee) | SocialMedia | success | 24 | 24 | 0 | 24 | 0 | 0 | 0 | 0 | 0 |  |
| 43 | Ben's Love | Articles/个人博客-人生 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 44 | Berkeley AI Research(@berkeley_ai) | SocialMedia | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| 45 | Binyuan Hui(@huybery) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 46 | Blog - Remote Work Prep | Articles | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 47 | Boo布姐自译 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 48 | Browser Use(@browser_use) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 49 | CVer | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 50 | Character.AI(@character_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 51 | ChatGPT(@ChatGPTapp) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 52 | CoCoVii | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 53 | Cognition(@cognition_labs) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 54 | Cursor(@cursor_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 55 | Dario Amodei(@DarioAmodei) | SocialMedia | success | 9 | 9 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |  |
| 56 | Datawhale | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 57 | DeepLearning.AI(@DeepLearningAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 58 | DeepSeek(@deepseek_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 59 | Demis Hassabis(@demishassabis) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 60 | Dia(@diabrowser) | SocialMedia | success | 19 | 19 | 0 | 19 | 0 | 0 | 0 | 0 | 0 |  |
| 61 | Dify(@dify_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 62 | EVANGELION:ALL | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 63 | ElevenLabs(@elevenlabsio) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 64 | Eric Jing(@ericjing_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 65 | Experimental History | Articles | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 66 | Fei-Fei Li(@drfeifei) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 67 | Fellou(@FellouAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 68 | Figma(@figma) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 69 | Firecrawl(@firecrawl_dev) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 70 | Fireworks AI(@FireworksAI_HQ) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 71 | Fish Audio(@FishAudio) | SocialMedia | success | 22 | 22 | 0 | 22 | 0 | 0 | 0 | 0 | 0 |  |
| 72 | FlowiseAI(@FlowiseAI) | SocialMedia | success | 18 | 18 | 0 | 18 | 0 | 0 | 0 | 0 | 0 |  |
| 73 | Gary Marcus(@GaryMarcus) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 74 | GeekPlux Letters | Articles | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 75 | Genspark(@genspark_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 76 | Geoffrey Hinton(@geoffreyhinton) | SocialMedia | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 77 | Google AI Developers(@googleaidevs) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 78 | Google AI(@GoogleAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 79 | Google DeepMind(@GoogleDeepMind) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 80 | Google Gemini App(@GeminiApp) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 81 | Gray格雷老师 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 82 | Greg Brockman(@gdb) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 83 | Groq Inc(@GroqInc) | SocialMedia | success | 23 | 23 | 0 | 23 | 0 | 0 | 0 | 0 | 0 |  |
| 84 | Guillermo Rauch(@rauchg) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 85 | Hailuo AI (MiniMax)(@Hailuo_AI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 86 | Harrison Chase(@hwchase17) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 87 | HelloGithub - 月刊 | Articles/科技与编程 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 88 | HeyGen(@HeyGen_Official) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 89 | Hi, DIYgod | Articles | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| 90 | Hugging Face(@huggingface) | SocialMedia | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 91 | Hunyuan(@TXhunyuan) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 92 | Ian Goodfellow(@goodfellow_ian) | SocialMedia | success | 13 | 13 | 0 | 13 | 0 | 0 | 0 | 0 | 0 |  |
| 93 | Ideogram(@ideogram_ai) | SocialMedia | success | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 0 | 0 |  |
| 94 | InfoQ | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 95 | Jan Leike(@janleike) | SocialMedia | success | 27 | 27 | 0 | 27 | 0 | 0 | 0 | 0 | 0 |  |
| 96 | Jeff Dean(@JeffDean) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 97 | Jerry Liu(@jerryjliu0) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 98 | Jim Fan(@DrJimFan) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 99 | Jina AI(@JinaAI_) | SocialMedia | success | 23 | 23 | 0 | 23 | 0 | 0 | 0 | 0 | 0 |  |
| 100 | Julien Chaumond(@julien_c) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 101 | Junyang Lin(@JustinLin610) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 102 | Justin Welsh(@thejustinwelsh) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 103 | Justine Moore(@venturetwins) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 104 | Kevin Weil &#127482;&#127480;(@kevinweil) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 105 | Kling AI(@Kling_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 106 | Kubernetes Blog | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 107 | LangChain(@LangChainAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 108 | Larry想做技术大佬 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 109 | Latent.Space(@latentspacepod) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 110 | Lee Robinson(@leerob) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 111 | Lenny Rachitsky(@lennysan) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 112 | Lex Fridman - YouTube | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 113 | Lex Fridman Podcast | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 114 | Lex Fridman(@lexfridman) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 115 | Lil'Log | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 116 | Lilian Weng(@lilianweng) | SocialMedia | success | 24 | 24 | 0 | 24 | 0 | 0 | 0 | 0 | 0 |  |
| 117 | LlamaIndex &#129433;(@llama_index) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 118 | Logan Kilpatrick(@OfficialLoganK) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 119 | Lovable(@lovable_dev) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 120 | LovartAI(@lovart_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 121 | Lukas Petersson’s blog | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 122 | LunaticMosfet | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 123 | L先生说 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 124 | MOJi辞書 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 125 | Maki的完美算术教室 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 126 | ManusAI(@ManusAI_HQ) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 127 | Marc Andreessen &#127482;&#127480;(@pmarca) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 128 | Microsoft Research(@MSFTResearch) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 129 | Midjourney(@midjourney) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 130 | Mike Krieger(@mikeyk) | SocialMedia | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 131 | Milvus(@milvusio) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 132 | Mistral AI(@MistralAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 133 | Monica_IM(@hey_im_monica) | SocialMedia | success | 16 | 16 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |  |
| 134 | Morpheus红丸主义 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 135 | MrBeast官方账号 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 136 | Mustafa Suleyman(@mustafasuleyman) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 137 | NASA中文 - 天文·每日一图 | Pictures/星空 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 138 | NVIDIA AI(@NVIDIAAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 139 | Naval(@naval) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 140 | Nenly同学 | Videos/长知识 | success | 9 | 9 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |  |
| 141 | Nick St. Pierre(@nickfloats) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 142 | Norah脱口秀 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 143 | NotebookLM(@NotebookLM) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 144 | Notion(@NotionHQ) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 145 | ONE字幕组 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 146 | OpenAI Developers(@OpenAIDevs) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 147 | OpenAI(@OpenAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 148 | OpenRouter(@OpenRouterAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 149 | PaperWeekly | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 150 | Paradise Lost | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 151 | Patrick Loeber(@patloeber) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 152 | Paul Couvert(@itsPaulAi) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 153 | Paul Graham(@paulg) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 154 | Perplexity(@perplexity_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 155 | Philipp Schmid(@_philschmid) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 156 | Pika(@pika_labs) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 157 | Podnews Daily - podcast industry news | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 158 | Poe(@poe_platform) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 159 | Qdrant(@qdrant_engine) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 160 | Qwen(@Alibaba_Qwen) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 161 | Ray Dalio(@RayDalio) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 162 | Recraft(@recraftai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 163 | Replicate(@replicate) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 164 | Replit ⠕(@Replit) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 165 | Richard Socher(@RichardSocher) | SocialMedia | success | 21 | 21 | 0 | 21 | 0 | 0 | 0 | 0 | 0 |  |
| 166 | Rolen's Blog | Articles/个人博客-人生 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 167 | Rowan Cheung(@rowancheung) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 168 | Runway(@runwayml) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 169 | Sahil Lavingia(@shl) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 170 | Sam Altman(@sama) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 171 | Satya Nadella(@satyanadella) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 172 | Scott Wu(@ScottWu46) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 173 | Simon Willison(@simonw) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 174 | Skywork(@Skywork_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 175 | Stanford AI Lab(@StanfordAILab) | SocialMedia | success | 9 | 9 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |  |
| 176 | StarYuhen | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 177 | Sualeh Asif(@sualehasif996) | SocialMedia | success | 13 | 13 | 0 | 13 | 0 | 0 | 0 | 0 | 0 |  |
| 178 | Suhail(@Suhail) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 179 | Sundar Pichai(@sundarpichai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 180 | Super也好君 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 181 | Taranjeet(@taranjeetio) | SocialMedia | success | 27 | 27 | 0 | 27 | 0 | 0 | 0 | 0 | 0 |  |
| 182 | The Rundown AI(@TheRundownAI) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 183 | Thomas Wolf(@Thom_Wolf) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 184 | Tinyfool的个人网站 | Articles/社评 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 185 | Twitter @Pietro Schirano | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 186 | Twitter @Theo - t3.gg | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 187 | Twitter @Tom Huang | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 188 | Twitter @Tw93 | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 189 | Twitter @ginobefun | SocialMedia | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 190 | Varun Mohan(@_mohansolo) | SocialMedia | success | 29 | 29 | 0 | 29 | 0 | 0 | 0 | 0 | 0 |  |
| 191 | Very Small Woods | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 192 | Vista看天下 | Articles/社评 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| 193 | Weaviate • vector database(@weaviate_io) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 194 | Windsurf(@windsurf_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 195 | Y Combinator(@ycombinator) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 196 | Yann LeCun(@ylecun) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 197 | YouTube深度访谈 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 198 | Z Finance | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 199 | Z Potentials | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 200 | a16z(@a16z) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 201 | abortretry.fail | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 202 | andrew chen(@andrewchen) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 203 | anildash.com | Articles/英文博客 | success | 12 | 12 | 0 | 12 | 0 | 0 | 0 | 0 | 0 |  |
| 204 | antirez.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 205 | aresluna.org | Articles/英文博客 | success | 14 | 14 | 0 | 14 | 0 | 0 | 0 | 0 | 0 |  |
| 206 | beej.us | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 207 | bernsteinbear.com | Articles/英文博客 | success | 11 | 11 | 0 | 11 | 0 | 0 | 0 | 0 | 0 |  |
| 208 | berthub.eu | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 209 | blog.jim-nielsen.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 210 | blog.pixelmelt.dev | Articles/英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 211 | bogdanthegeek.github.io | Articles/英文博客 | success | 8 | 8 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |  |
| 212 | bolt.new(@boltdotnew) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 213 | borretti.me | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 214 | brutecat.com | Articles/英文博客 | success | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |  |
| 215 | buttondown.com/hillelwayne | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 216 | cat(@_catwu) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 217 | chadnauseam.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 218 | chiark.greenend.org.uk/~sgtatham | Articles/英文博客 | success | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 0 | 0 |  |
| 219 | clem &#129303;(@ClementDelangue) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 220 | cohere(@cohere) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 221 | computer.rip | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 222 | construction-physics.com | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 223 | danielchasehooper.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 224 | danieldelaney.net | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 225 | danielwirtz.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 226 | daringfireball.net | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 227 | derekthompson.org | Articles/英文博客 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 228 | devblogs.microsoft.com/oldnewthing | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 229 | dfarq.homeip.net | Articles/英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 230 | downtowndougbrown.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 231 | dwarkesh.com | Articles/英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 232 | dynomight.net | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 233 | eli.thegreenplace.net | Articles/英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| 234 | elvis(@omarsar0) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 235 | entropicthoughts.com | Articles/英文博客 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 236 | eric zakariasson(@ericzakariasson) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 237 | ericmigi.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 238 | evanhahn.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 239 | everystep | Articles/微信公众号 | success | 29 | 29 | 0 | 29 | 0 | 0 | 0 | 0 | 0 |  |
| 240 | fabiensanglard.net | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 241 | filfre.net | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 242 | focus2flow | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 243 | garymarcus.substack.com | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 244 | geoffreylitt.com | Articles/英文博客 | success | 11 | 11 | 0 | 11 | 0 | 0 | 0 | 0 | 0 |  |
| 245 | geohot.github.io | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 246 | gilesthomas.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 247 | grantslatton.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 248 | gwern.net | Articles/英文博客 | success | 14 | 14 | 0 | 14 | 0 | 0 | 0 | 0 | 0 |  |
| 249 | herman.bearblog.dev | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 250 | hey.paris | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 251 | hugotunius.se | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 252 | idiallo.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 253 | it-notes.dragas.net | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 254 | jayd.ml | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 255 | jeffgeerling.com | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 256 | joanwestenberg.com | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 257 | johndcook.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 258 | joojen Zhou 的网站 | Articles | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 259 | jyn.dev | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 260 | keygen.sh | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 261 | krebsonsecurity.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 262 | lcamtuf.substack.com | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 263 | lmarena.ai(@lmarena_ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 264 | lucumr.pocoo.org | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 265 | martinalderson.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 266 | matduggan.com | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 267 | matklad.github.io | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 268 | maurycyz.com | Articles/英文博客 | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| 269 | mem0(@mem0ai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 270 | meng shao(@shao__meng) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 271 | micahflee.com | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 272 | michael.stapelberg.ch | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 273 | miguelgrinberg.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 274 | minimaxir.com | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 275 | mitchellh.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 276 | mjg59.dreamwidth.org | Articles/英文博客 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 277 | nesbitt.io | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 278 | oldvcr.blogspot.com | Articles/英文博客 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 279 | ollama(@ollama) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 280 | orange.ai(@oran_ge) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 281 | overreacted.io | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 282 | paulgraham.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 283 | philiplaine.com | Articles/英文博客 | success | 8 | 8 | 0 | 8 | 0 | 0 | 0 | 0 | 0 |  |
| 284 | pluralistic.net | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 285 | rachelbythebay.com | Articles/英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 286 | rakhim.exotext.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 287 | refactoringenglish.com | Articles/英文博客 | success | 18 | 18 | 0 | 18 | 0 | 0 | 0 | 0 | 0 |  |
| 288 | righto.com | Articles/英文博客 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 289 | seangoedecke.com | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 290 | shkspr.mobi | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 291 | simone.org | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 292 | simonwillison.net | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 293 | skyfall.dev | Articles/英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 294 | steveblank.com | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 295 | susam.net | Articles/英文博客 | success | 6 | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |  |
| 296 | tanscp | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 297 | tedium.co | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 298 | tedunangst.com | Articles/英文博客 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 299 | terriblesoftware.org | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 300 | timsh.org | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 301 | tomrenner.com | Articles/英文博客 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 302 | troyhunt.com | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 303 | utcc.utoronto.ca/~cks | Articles/英文博客 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 304 | v0(@v0) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 305 | wheresyoured.at | Articles/英文博客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 306 | worksonmymachine.substack.com | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 307 | xAI(@xai) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 308 | xania.org | Articles/英文博客 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 309 | xeiaso.net | Articles/英文博客 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 310 | 一亩三分地 - 日本热门帖子 | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 311 | 一觉醒来发生了什么 - 即刻圈子 | Articles/国内外资讯 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 312 | 三联生活周刊 Lifeweek | Articles/社评 | success | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 313 | 下班的三爷 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 314 | 不如读书 | Articles | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 315 | 与书籍度过漫长岁月 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 316 | 东西智库 – 专注中国制造业高质量发展 | Articles/国内外资讯 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 317 | 中国政府网 - 最新政策 | Articles/国内政策 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 318 | 二次元的Datawhale | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 319 | 云中江树 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 320 | 人间自习室 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 321 | 今日热榜 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | network_error |
| 322 | 付航脱口秀 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 323 | 付航脱口秀精选 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 324 | 你不知道的行业内幕 - 即刻圈子 | SocialMedia/资讯 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 325 | 你是想气死1酱么 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 326 | 信息差——独立开发者出海周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 327 | 偷懒爱好者周刊 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 328 | 光子星球 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 329 | 冲击波工作室 | Videos/最娱乐 | success | 17 | 17 | 0 | 17 | 0 | 0 | 0 | 0 | 0 |  |
| 330 | 冲男阿凉 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 331 | 刘夙的科技世界 | Articles/社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 332 | 刘聪NLP | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 333 | 努力戒咕的coco锤 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 334 | 十字路口Crossing | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 335 | 十年之约聚合订阅 | Articles/科技与编程 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 336 | 半只笨猪 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 337 | 半月谈快报 | Articles/党政信息 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 338 | 单弦震脉 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 339 | 卡尔的AI沃茨 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 340 | 卡纸大寨主 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 341 | 司机社综合周排行榜 | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 342 | 司机社综合月排行榜 | Videos | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 343 | 司马尘 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 344 | 向杨Alan君 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 345 | 向阳乔木(@vista8) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 346 | 听泉赏宝 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 347 | 周侃侃plus | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 348 | 周刊 归档 - 酷口家数字花园 | Articles | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 349 | 和张程一起学习吧 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 350 | 咖啡醉足球 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 351 | 哥飞 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 352 | 啊桂实验室 | Articles/微信公众号 | success | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 0 | 0 |  |
| 353 | 图书推荐 – 书伴 | SocialMedia | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 354 | 坚果熊说博弈 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 355 | 夕小瑶科技说 | Articles/微信公众号 | success | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 0 | 0 |  |
| 356 | 大祥哥来了 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 357 | 大问题Dialectic | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 358 | 大问题Dialectic | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 359 | 天才简史 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 360 | 奥德修斯的绳索 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 361 | 学习一下订阅源 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 362 | 学院派Academia | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 363 | 安全代码 | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 364 | 宝玉(@dotey) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 365 | 宝玉的分享 | Articles/科技与编程 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 366 | 小互(@imxiaohu) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 367 | 小众软件 | Articles/科技与编程 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 368 | 小宇宙 Podcast 5e5c52c9418a84a04625e6cc | Articles/播客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 369 | 小宇宙 Podcast 61cbaac48bb4cd867fcabe22 | Articles/播客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 370 | 小宇宙 Podcast 63b7dd49289d2739647d9587 | Articles/播客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 371 | 小宇宙 Podcast 643928f99361a4e7c38a9555 | Articles/播客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 372 | 小宇宙 Podcast 648b0b641c48983391a63f98 | Articles/播客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 373 | 小宇宙 Podcast 6507bc165c88d2412626b401 | Articles/播客 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 374 | 小波心理 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 375 | 少数派 | Articles/优质信息源 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 376 | 少数派 -- Matrix | Articles/优质信息源 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 377 | 岱川博士 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 378 | 岺玖贰叁 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 379 | 峡谷玄学家 | Videos/绝活娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 380 | 巅峰球迷汇 | Videos/最娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 381 | 差评君 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 382 | 常青说 | Articles/微信公众号 | success | 14 | 14 | 0 | 14 | 0 | 0 | 0 | 0 | 0 |  |
| 383 | 开源AI项目落地 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 384 | 影视飓风 | Videos/最娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 385 | 心河摆渡 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 386 | 思维实验室 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 387 | 慢慢学的四饼 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 388 | 戴建业老师 | Videos/绝活娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 389 | 拣尽南枝 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 390 | 探索AGI | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 391 | 数字生命卡兹克 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 392 | 新华社新闻_新华网 | Articles/党政信息 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 393 | 新智元 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 394 | 新智元 | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 395 | 新石器公园 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 396 | 时代观察 - 乌有之乡网刊 | Articles/社评 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | rsshub_503 |
| 397 | 是啤酒鸭-梗图 | Videos/绝活娱乐 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 398 | 是落拓呀 | Videos/长知识 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | timeout |
| 399 | 晚点LatePost | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 400 | 智东西 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 401 | 智能路障 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 402 | 最新发布_共产党员网 | Articles/党政信息 | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 403 | 本子在隔壁 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 404 | 机器之心 | Articles/微信公众号 | success | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 0 | 0 |  |
| 405 | 机器之心 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | feed_parse_error |
| 406 | 机器人夏先生1号 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 407 | 李滇滇 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 408 | 李继刚(@lijigang_com) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 409 | 杰克森Jackson_ | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 410 | 极客公园 | Articles/微信公众号 | success | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 0 | 0 |  |
| 411 | 极客公园 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | unknown |
| 412 | 极客公园 | Articles | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 413 | 林川登罗 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 414 | 柯洁 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 415 | 歌白说Geslook | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 416 | 歸藏(guizang.ai)(@op7418) | SocialMedia | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 417 | 歸藏的AI工具箱 | Articles | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | content_inbox_error |
| 418 | 每周一书 – 书伴 | SocialMedia | success | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |
| 419 | 每日一图-北京天文馆 | Pictures/星空 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 420 | 毕导 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 421 | 汤质看本质 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 422 | 沃垠AI | Articles/微信公众号 | success | 27 | 27 | 0 | 27 | 0 | 0 | 0 | 0 | 0 |  |
| 423 | 河口超人Aper | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 424 | 泛式 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 425 | 波士顿圆脸 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 426 | 浮世叁千问 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 427 | 海林A读书 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 428 | 混沌周刊 | Articles/科技与编程 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 429 | 漫士沉思录 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 430 | 潦草学者 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 431 | 火兰朋克 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 432 | 灯果 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 433 | 特工宇宙 | Articles/微信公众号 | success | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 0 | 0 |  |
| 434 | 猫眼看足球 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 435 | 猴猴说话 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 436 | 猴猴说话 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 437 | 瓶子君152 | Videos/最娱乐 | success | 8 | 7 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |  |
| 438 | 甲子光年 | Articles/微信公众号 | success | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 0 | 0 |  |
| 439 | 白染one | Videos/长知识 | success | 20 | 20 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |  |
| 440 | 白熊阿丸的小屋 | Articles/个人博客-人生 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 441 | 白马繁华 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 442 | 真实球迷汇 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 443 | 知识共享者 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 444 | 硅星人Pro | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 445 | 硬核学长2077 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 446 | 秋芝2046 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 447 | 科幻视界 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 448 | 笔记交流站 - 即刻圈子 | SocialMedia | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 449 | 笨方法学写作 | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 450 | 管泽元 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 451 | 米国脱口秀 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 452 | 纵横四海 | Articles | success | 15 | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |  |
| 453 | 网罗灯下黑 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 454 | 罗明落ny | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 455 | 罗翔说刑法 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 456 | 老T博客 | Articles | success | 5 | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| 457 | 老实憨厚的笑笑 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 458 | 胡说成理 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 459 | 脑极体 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 460 | 脱口秀_Talk_Show | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 461 | 腾讯研究院 | Articles | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 462 | 苍何 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 463 | 英语播客党 | Videos/短知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 464 | 英语播客狗 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 465 | 草稿拾遗 | Articles/个人博客-人生 | success | 14 | 14 | 0 | 14 | 0 | 0 | 0 | 0 | 0 |  |
| 466 | 荒野初研园 | Videos/长知识 | success | 19 | 19 | 0 | 19 | 0 | 0 | 0 | 0 | 0 |  |
| 467 | 莫尔索随笔 | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 468 | 莫比乌斯 | Articles/个人博客-人生 | success | 10 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |  |
| 469 | 蒙克MK_ | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 470 | 西山在何许 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 471 | 要素分析 | Videos/长知识 | success | 12 | 12 | 0 | 12 | 0 | 0 | 0 | 0 | 0 |  |
| 472 | 读书的Harry | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 473 | 豆瓣小组-无用美学 | Articles | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 474 | 贝拉kira | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 475 | 负面能量转换器 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 476 | 赏味不足 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 477 | 赛博禅心 | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 478 | 走路 | Articles/微信公众号 | success | 27 | 27 | 0 | 27 | 0 | 0 | 0 | 0 | 0 |  |
| 479 | 载脑体 | Videos/长知识 | success | 27 | 27 | 0 | 27 | 0 | 0 | 0 | 0 | 0 |  |
| 480 | 辰星杂谈 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 481 | 这是个令人疑惑的星球 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 482 | 迷因水母 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 483 | 退役编辑雨上 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 484 | 逗比的雀巢 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 485 | 逛逛GitHub | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 486 | 邵艾伦Alan | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 487 | 量子位 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 488 | 银屏系漫游指南 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 489 | 阮一峰的网络日志 | Articles/科技与编程 | success | 6 | 6 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |  |
| 490 | 阿伦AI学习笔记 | Articles/微信公众号 | success | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 0 | 0 |  |
| 491 | 陈大东瓜 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 492 | 隔壁红魔 | Videos/绝活娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 493 | 雷峰网 | Articles/微信公众号 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 494 | 非卿漫谈 | Videos/长知识 | success | 13 | 13 | 0 | 13 | 0 | 0 | 0 | 0 | 0 |  |
| 495 | 靠谱电竞 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 496 | 飞鸟手札 | Videos/短知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 497 | 食事史馆 | Videos/长知识 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 498 | 饼干哥哥AGI | Articles/微信公众号 | success | 25 | 25 | 0 | 25 | 0 | 0 | 0 | 0 | 0 |  |
| 499 | 馆长刘下饭_环球档案 | Videos/最娱乐 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |
| 500 | 龙爪槐守望者 | Articles/科技与编程 | success | 30 | 30 | 0 | 30 | 0 | 0 | 0 | 0 | 0 |  |

## 4. 阅读视图

### 今天看什么娱乐

无

### 我关注的前沿咋样了

无

### 我关心的话题议题有什么新的进展

无

### 有什么是我值得看的

无

### 系统通知推荐

无

## 5. 失败源列表

- **Andrej Karpathy - YouTube**
  - 分类：Videos
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/youtube/user/@AndrejKarpathy
  - final feed_url：http://127.0.0.1:1200/youtube/user/@AndrejKarpathy
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "videos-andrej-karpathy-youtube", "feed_url": "http://127.0.0.1:1200/youtube/user/@AndrejKarpathy"}, "run": {"run_id": "rss_20260516_081909_886342_videos-andrej-karpathy-youtube", "source_id": "videos-andrej-karpathy-youtube", "status": "failed", "started_at": "2026-05-16T08:19:09.886342+00:00", "finished_at": "2026-05-16T08:19:19.385742+00:00", "duration_ms": 9499, "duration_seconds": 9.499, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit
- **EVANGELION:ALL**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.eva-all.com/news/feed/
  - final feed_url：https://www.eva-all.com/news/feed/
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_http_error", "message": "HTTP Error 403: Forbidden", "retryable": true, "source_id": "articles-evangelion-all", "feed_url": "https://www.eva-all.com/news/feed/"}, "run": {"run_id": "rss_20260516_081942_084573_articles-evangelion-all", "source_id": "articles-evangelion-all", "status": "failed", "started_at": "2026-05-16T08:19:42.084573+00:00", "finished_at": "2026-05-16T08:19:43.300717+00:00", "duration_ms": 1216, "duration_seconds": 1.216, "error_code": "rss_fetch_http_error", "error_message": "HTTP Error 403: Forbidden", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null},
- **Lex Fridman - YouTube**
  - 分类：Videos
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/youtube/user/%40lexfridman
  - final feed_url：http://127.0.0.1:1200/youtube/user/%40lexfridman
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "videos-lex-fridman-youtube", "feed_url": "http://127.0.0.1:1200/youtube/user/%40lexfridman"}, "run": {"run_id": "rss_20260516_082032_463707_videos-lex-fridman-youtube", "source_id": "videos-lex-fridman-youtube", "status": "failed", "started_at": "2026-05-16T08:20:32.463707+00:00", "finished_at": "2026-05-16T08:20:34.827358+00:00", "duration_ms": 2364, "duration_seconds": 2.364, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incrementa
- **NASA中文 - 天文·每日一图**
  - 分类：Pictures/星空
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/nasa/apod-cn
  - final feed_url：http://127.0.0.1:1200/nasa/apod-cn
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "pictures-nasa", "feed_url": "http://127.0.0.1:1200/nasa/apod-cn"}, "run": {"run_id": "rss_20260516_082057_833617_pictures-nasa", "source_id": "pictures-nasa", "status": "failed", "started_at": "2026-05-16T08:20:57.833617+00:00", "finished_at": "2026-05-16T08:20:59.321317+00:00", "duration_ms": 1488, "duration_seconds": 1.488, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "erro
- **StarYuhen**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.yuhenm.top/feed/
  - final feed_url：https://www.yuhenm.top/feed/
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_http_error", "message": "HTTP Error 403: Forbidden", "retryable": true, "source_id": "articles-staryuhen", "feed_url": "https://www.yuhenm.top/feed/"}, "run": {"run_id": "rss_20260516_082137_290559_articles-staryuhen", "source_id": "articles-staryuhen", "status": "failed", "started_at": "2026-05-16T08:21:37.290559+00:00", "finished_at": "2026-05-16T08:21:38.954224+00:00", "duration_ms": 1664, "duration_seconds": 1.664, "error_code": "rss_fetch_http_error", "error_message": "HTTP Error 403: Forbidden", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_cod
- **Twitter @Pietro Schirano**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/twitter/user/skirano
  - final feed_url：http://127.0.0.1:1200/twitter/user/skirano
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "socialmedia-twitter-pietro-schirano", "feed_url": "http://127.0.0.1:1200/twitter/user/skirano"}, "run": {"run_id": "rss_20260516_082146_477960_socialmedia-twitter-pietro-schirano", "source_id": "socialmedia-twitter-pietro-schirano", "status": "failed", "started_at": "2026-05-16T08:21:46.477960+00:00", "finished_at": "2026-05-16T08:21:46.598258+00:00", "duration_ms": 120, "duration_seconds": 0.12, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_
- **Twitter @Theo - t3.gg**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/twitter/user/theo
  - final feed_url：http://127.0.0.1:1200/twitter/user/theo
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "socialmedia-twitter-theo-t3-gg", "feed_url": "http://127.0.0.1:1200/twitter/user/theo"}, "run": {"run_id": "rss_20260516_082147_480345_socialmedia-twitter-theo-t3-gg", "source_id": "socialmedia-twitter-theo-t3-gg", "status": "failed", "started_at": "2026-05-16T08:21:47.480345+00:00", "finished_at": "2026-05-16T08:21:47.509264+00:00", "duration_ms": 29, "duration_seconds": 0.029, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "increment
- **Twitter @Tom Huang**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/twitter/user/tuturetom
  - final feed_url：http://127.0.0.1:1200/twitter/user/tuturetom
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "socialmedia-twitter-tom-huang", "feed_url": "http://127.0.0.1:1200/twitter/user/tuturetom"}, "run": {"run_id": "rss_20260516_082148_491098_socialmedia-twitter-tom-huang", "source_id": "socialmedia-twitter-tom-huang", "status": "failed", "started_at": "2026-05-16T08:21:48.491098+00:00", "finished_at": "2026-05-16T08:21:48.504174+00:00", "duration_ms": 13, "duration_seconds": 0.013, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "increme
- **Twitter @Tw93**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/twitter/user/HiTw93
  - final feed_url：http://127.0.0.1:1200/twitter/user/HiTw93
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "socialmedia-twitter-tw93", "feed_url": "http://127.0.0.1:1200/twitter/user/HiTw93"}, "run": {"run_id": "rss_20260516_082149_499715_socialmedia-twitter-tw93", "source_id": "socialmedia-twitter-tw93", "status": "failed", "started_at": "2026-05-16T08:21:49.499715+00:00", "finished_at": "2026-05-16T08:21:49.512247+00:00", "duration_ms": 13, "duration_seconds": 0.013, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": nu
- **Twitter @ginobefun**
  - 分类：SocialMedia
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/twitter/user/hongming731
  - final feed_url：http://127.0.0.1:1200/twitter/user/hongming731
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "socialmedia-twitter-ginobefun", "feed_url": "http://127.0.0.1:1200/twitter/user/hongming731"}, "run": {"run_id": "rss_20260516_082150_509415_socialmedia-twitter-ginobefun", "source_id": "socialmedia-twitter-ginobefun", "status": "failed", "started_at": "2026-05-16T08:21:50.509415+00:00", "finished_at": "2026-05-16T08:21:50.519080+00:00", "duration_ms": 10, "duration_seconds": 0.01, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "increm
- **blog.pixelmelt.dev**
  - 分类：Articles/英文博客
  - local_xml_url：-
  - xml_url：https://blog.pixelmelt.dev/rss/
  - final feed_url：https://blog.pixelmelt.dev/rss/
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 530: <none>", "retryable": true, "source_id": "articles-blog-pixelmelt-dev", "feed_url": "https://blog.pixelmelt.dev/rss/"}, "run": {"run_id": "rss_20260516_082211_774721_articles-blog-pixelmelt-dev", "source_id": "articles-blog-pixelmelt-dev", "status": "failed", "started_at": "2026-05-16T08:22:11.774721+00:00", "finished_at": "2026-05-16T08:22:12.853750+00:00", "duration_ms": 1079, "duration_seconds": 1.079, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 530: <none>", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history":
- **dfarq.homeip.net**
  - 分类：Articles/英文博客
  - local_xml_url：-
  - xml_url：https://dfarq.homeip.net/feed/
  - final feed_url：https://dfarq.homeip.net/feed/
  - error_type：feed_parse_error
  - error_message：{"ok": false, "error": {"error_code": "rss_parse_error", "message": "failed to parse feed: <unknown>:2:0: not well-formed (invalid token)", "retryable": false, "source_id": "articles-dfarq-homeip-net", "feed_url": "https://dfarq.homeip.net/feed/"}, "run": {"run_id": "rss_20260516_082231_101014_articles-dfarq-homeip-net", "source_id": "articles-dfarq-homeip-net", "status": "failed", "started_at": "2026-05-16T08:22:31.101014+00:00", "finished_at": "2026-05-16T08:22:32.513073+00:00", "duration_ms": 1412, "duration_seconds": 1.412, "error_code": "rss_parse_error", "error_message": "failed to parse feed: <unknown>:2:0: not well-formed (invalid token)", "retryable": false, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_
- **dwarkesh.com**
  - 分类：Articles/英文博客
  - local_xml_url：-
  - xml_url：https://www.dwarkeshpatel.com/feed
  - final feed_url：https://www.dwarkeshpatel.com/feed
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_http_error", "message": "HTTP Error 308: Permanent Redirect", "retryable": true, "source_id": "articles-dwarkesh-com", "feed_url": "https://www.dwarkeshpatel.com/feed"}, "run": {"run_id": "rss_20260516_082233_114041_articles-dwarkesh-com", "source_id": "articles-dwarkesh-com", "status": "failed", "started_at": "2026-05-16T08:22:33.114041+00:00", "finished_at": "2026-05-16T08:22:34.738919+00:00", "duration_ms": 1625, "duration_seconds": 1.625, "error_code": "rss_fetch_http_error", "error_message": "HTTP Error 308: Permanent Redirect", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_hist
- **rachelbythebay.com**
  - 分类：Articles/英文博客
  - local_xml_url：-
  - xml_url：https://rachelbythebay.com/w/atom.xml
  - final feed_url：https://rachelbythebay.com/w/atom.xml
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_connection_error", "message": "[SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 alert protocol version (_ssl.c:1129)", "retryable": true, "source_id": "articles-rachelbythebay-com", "feed_url": "https://rachelbythebay.com/w/atom.xml"}, "run": {"run_id": "rss_20260516_082327_996684_articles-rachelbythebay-com", "source_id": "articles-rachelbythebay-com", "status": "failed", "started_at": "2026-05-16T08:23:27.996684+00:00", "finished_at": "2026-05-16T08:23:28.758717+00:00", "duration_ms": 762, "duration_seconds": 0.762, "error_code": "rss_fetch_connection_error", "error_message": "[SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 alert protocol version (_ssl.c:1129)", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null,
- **skyfall.dev**
  - 分类：Articles/英文博客
  - local_xml_url：-
  - xml_url：https://skyfall.dev/rss.xml
  - final feed_url：https://skyfall.dev/rss.xml
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_http_error", "message": "HTTP Error 308: Permanent Redirect", "retryable": true, "source_id": "articles-skyfall-dev", "feed_url": "https://skyfall.dev/rss.xml"}, "run": {"run_id": "rss_20260516_082336_063234_articles-skyfall-dev", "source_id": "articles-skyfall-dev", "status": "failed", "started_at": "2026-05-16T08:23:36.063234+00:00", "finished_at": "2026-05-16T08:23:37.229790+00:00", "duration_ms": 1167, "duration_seconds": 1.167, "error_code": "rss_fetch_http_error", "error_message": "HTTP Error 308: Permanent Redirect", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null
- **tedunangst.com**
  - 分类：Articles/英文博客
  - local_xml_url：-
  - xml_url：https://www.tedunangst.com/flak/rss
  - final feed_url：https://www.tedunangst.com/flak/rss
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "_ssl.c:1112: The handshake operation timed out", "retryable": true, "source_id": "articles-tedunangst-com", "feed_url": "https://www.tedunangst.com/flak/rss"}, "run": {"run_id": "rss_20260516_082341_108299_articles-tedunangst-com", "source_id": "articles-tedunangst-com", "status": "failed", "started_at": "2026-05-16T08:23:41.108299+00:00", "finished_at": "2026-05-16T08:24:01.621387+00:00", "duration_ms": 20513, "duration_seconds": 20.513, "error_code": "rss_fetch_timeout", "error_message": "_ssl.c:1112: The handshake operation timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decisi
- **东西智库 – 专注中国制造业高质量发展**
  - 分类：Articles/国内外资讯
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/dx2025
  - final feed_url：http://127.0.0.1:1200/dx2025
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "articles-625204ac", "feed_url": "http://127.0.0.1:1200/dx2025"}, "run": {"run_id": "rss_20260516_082359_418188_articles-625204ac", "source_id": "articles-625204ac", "status": "failed", "started_at": "2026-05-16T08:23:59.418188+00:00", "finished_at": "2026-05-16T08:24:05.863723+00:00", "duration_ms": 6446, "duration_seconds": 6.446, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null},
- **中国政府网 - 最新政策**
  - 分类：Articles/国内政策
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/gov/zhengce/zuixin
  - final feed_url：http://127.0.0.1:1200/gov/zhengce/zuixin
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "articles-1859ad11", "feed_url": "http://127.0.0.1:1200/gov/zhengce/zuixin"}, "run": {"run_id": "rss_20260516_082400_427374_articles-1859ad11", "source_id": "articles-1859ad11", "status": "failed", "started_at": "2026-05-16T08:24:00.427374+00:00", "finished_at": "2026-05-16T08:24:01.312064+00:00", "duration_ms": 885, "duration_seconds": 0.885, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_histo
- **今日热榜**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://web2rss.cc/feed/rebang.today?preview=true
  - final feed_url：https://web2rss.cc/feed/rebang.today?preview=true
  - error_type：network_error
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_connection_error", "message": "[Errno 8] nodename nor servname provided, or not known", "retryable": true, "source_id": "articles-6eee6aa9", "feed_url": "https://web2rss.cc/feed/rebang.today?preview=true"}, "run": {"run_id": "rss_20260516_082404_454346_articles-6eee6aa9", "source_id": "articles-6eee6aa9", "status": "failed", "started_at": "2026-05-16T08:24:04.454346+00:00", "finished_at": "2026-05-16T08:24:04.899166+00:00", "duration_ms": 445, "duration_seconds": 0.445, "error_code": "rss_fetch_connection_error", "error_message": "[Errno 8] nodename nor servname provided, or not known", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_
- **信息差——独立开发者出海周刊**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://gapis.money/rss.xml
  - final feed_url：https://gapis.money/rss.xml
  - error_type：feed_parse_error
  - error_message：{"ok": false, "error": {"error_code": "rss_parse_error", "message": "failed to parse feed: <unknown>:28:5120: not well-formed (invalid token)", "retryable": false, "source_id": "articles-b4b5f239", "feed_url": "https://gapis.money/rss.xml"}, "run": {"run_id": "rss_20260516_082409_489305_articles-b4b5f239", "source_id": "articles-b4b5f239", "status": "failed", "started_at": "2026-05-16T08:24:09.489305+00:00", "finished_at": "2026-05-16T08:24:12.771533+00:00", "duration_ms": 3282, "duration_seconds": 3.282, "error_code": "rss_parse_error", "error_message": "failed to parse feed: <unknown>:28:5120: not well-formed (invalid token)", "retryable": false, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit
- **偷懒爱好者周刊**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://toolight.cn/open/p/weekly/atom.xml
  - final feed_url：https://toolight.cn/open/p/weekly/atom.xml
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_not_found", "message": "HTTP Error 404: Not Found", "retryable": false, "source_id": "articles-0ab76289", "feed_url": "https://toolight.cn/open/p/weekly/atom.xml"}, "run": {"run_id": "rss_20260516_082410_674665_articles-0ab76289", "source_id": "articles-0ab76289", "status": "failed", "started_at": "2026-05-16T08:24:10.674665+00:00", "finished_at": "2026-05-16T08:24:12.839569+00:00", "duration_ms": 2165, "duration_seconds": 2.165, "error_code": "rss_fetch_not_found", "error_message": "HTTP Error 404: Not Found", "retryable": false, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error":
- **刘夙的科技世界**
  - 分类：Articles/社评
  - local_xml_url：-
  - xml_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - final feed_url：https://wewe-rss.jerrylf.uk/feeds/MP_WXS_3002603832.json
  - error_type：timeout
  - error_message："timed out"
- **司机社综合周排行榜**
  - 分类：Videos
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/xsijishe/rank/weekly
  - final feed_url：http://127.0.0.1:1200/xsijishe/rank/weekly
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "videos-ffbe1ba4", "feed_url": "http://127.0.0.1:1200/xsijishe/rank/weekly"}, "run": {"run_id": "rss_20260516_082425_261985_videos-ffbe1ba4", "source_id": "videos-ffbe1ba4", "status": "failed", "started_at": "2026-05-16T08:24:25.261985+00:00", "finished_at": "2026-05-16T08:24:27.954312+00:00", "duration_ms": 2692, "duration_seconds": 2.692, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history"
- **司机社综合月排行榜**
  - 分类：Videos
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/xsijishe/rank/monthly
  - final feed_url：http://127.0.0.1:1200/xsijishe/rank/monthly
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "videos-bd29fe04", "feed_url": "http://127.0.0.1:1200/xsijishe/rank/monthly"}, "run": {"run_id": "rss_20260516_082425_900857_videos-bd29fe04", "source_id": "videos-bd29fe04", "status": "failed", "started_at": "2026-05-16T08:24:25.900857+00:00", "finished_at": "2026-05-16T08:24:27.918754+00:00", "duration_ms": 2018, "duration_seconds": 2.018, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history
- **学习一下订阅源**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/follow/profile/158883963341209600
  - final feed_url：http://127.0.0.1:1200/follow/profile/158883963341209600
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "articles-4b4daed3", "feed_url": "http://127.0.0.1:1200/follow/profile/158883963341209600"}, "run": {"run_id": "rss_20260516_082445_058225_articles-4b4daed3", "source_id": "articles-4b4daed3", "status": "failed", "started_at": "2026-05-16T08:24:45.058225+00:00", "finished_at": "2026-05-16T08:24:48.000742+00:00", "duration_ms": 2943, "duration_seconds": 2.943, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "
- **小波心理**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/1033890839
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/1033890839
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-b6e88840", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/1033890839"}, "run": {"run_id": "rss_20260516_082458_349005_videos-b6e88840", "source_id": "videos-b6e88840", "status": "failed", "started_at": "2026-05-16T08:24:58.349005+00:00", "finished_at": "2026-05-16T08:25:18.644196+00:00", "duration_ms": 20295, "duration_seconds": 20.295, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeou
- **少数派**
  - 分类：Articles/优质信息源
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/sspai/index
  - final feed_url：http://127.0.0.1:1200/sspai/index
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "articles-4f25584f", "feed_url": "http://127.0.0.1:1200/sspai/index"}, "run": {"run_id": "rss_20260516_082459_372411_articles-4f25584f", "source_id": "articles-4f25584f", "status": "failed", "started_at": "2026-05-16T08:24:59.372411+00:00", "finished_at": "2026-05-16T08:25:19.382648+00:00", "duration_ms": 20010, "duration_seconds": 20.01, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout", "message":
- **少数派 -- Matrix**
  - 分类：Articles/优质信息源
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/sspai/matrix
  - final feed_url：http://127.0.0.1:1200/sspai/matrix
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "articles-matrix", "feed_url": "http://127.0.0.1:1200/sspai/matrix"}, "run": {"run_id": "rss_20260516_082500_367857_articles-matrix", "source_id": "articles-matrix", "status": "failed", "started_at": "2026-05-16T08:25:00.367857+00:00", "finished_at": "2026-05-16T08:25:20.383664+00:00", "duration_ms": 20016, "duration_seconds": 20.016, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout", "message": "ti
- **岱川博士**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/584630077
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/584630077
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-a2576d22", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/584630077"}, "run": {"run_id": "rss_20260516_082501_370505_videos-a2576d22", "source_id": "videos-a2576d22", "status": "failed", "started_at": "2026-05-16T08:25:01.370505+00:00", "finished_at": "2026-05-16T08:25:21.410668+00:00", "duration_ms": 20040, "duration_seconds": 20.04, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout"
- **岺玖贰叁**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/521296768
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/521296768
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-228c15a2", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/521296768"}, "run": {"run_id": "rss_20260516_082502_382177_videos-228c15a2", "source_id": "videos-228c15a2", "status": "failed", "started_at": "2026-05-16T08:25:02.382177+00:00", "finished_at": "2026-05-16T08:25:22.433965+00:00", "duration_ms": 20052, "duration_seconds": 20.052, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout
- **峡谷玄学家**
  - 分类：Videos/绝活娱乐
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/3493128455587886
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/3493128455587886
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-81d2bd04", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/3493128455587886"}, "run": {"run_id": "rss_20260516_082503_392908_videos-81d2bd04", "source_id": "videos-81d2bd04", "status": "failed", "started_at": "2026-05-16T08:25:03.392908+00:00", "finished_at": "2026-05-16T08:25:23.401598+00:00", "duration_ms": 20009, "duration_seconds": 20.009, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_
- **巅峰球迷汇**
  - 分类：Videos/最娱乐
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/365372809
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/365372809
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-7d4d5202", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/365372809"}, "run": {"run_id": "rss_20260516_082504_401390_videos-7d4d5202", "source_id": "videos-7d4d5202", "status": "failed", "started_at": "2026-05-16T08:25:04.401390+00:00", "finished_at": "2026-05-16T08:25:24.426975+00:00", "duration_ms": 20026, "duration_seconds": 20.026, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout
- **差评君**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/19319172
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/19319172
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-38d3abd1", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/19319172"}, "run": {"run_id": "rss_20260516_082505_409507_videos-38d3abd1", "source_id": "videos-38d3abd1", "status": "failed", "started_at": "2026-05-16T08:25:05.409507+00:00", "finished_at": "2026-05-16T08:25:25.501840+00:00", "duration_ms": 20092, "duration_seconds": 20.092, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout"
- **影视飓风**
  - 分类：Videos/最娱乐
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/946974
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/946974
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-473300ff", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/946974"}, "run": {"run_id": "rss_20260516_082508_446409_videos-473300ff", "source_id": "videos-473300ff", "status": "failed", "started_at": "2026-05-16T08:25:08.446409+00:00", "finished_at": "2026-05-16T08:25:29.083098+00:00", "duration_ms": 20637, "duration_seconds": 20.637, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout",
- **心河摆渡**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/230983435
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/230983435
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-1134c99b", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/230983435"}, "run": {"run_id": "rss_20260516_082509_597332_videos-1134c99b", "source_id": "videos-1134c99b", "status": "failed", "started_at": "2026-05-16T08:25:09.597332+00:00", "finished_at": "2026-05-16T08:25:30.114867+00:00", "duration_ms": 20518, "duration_seconds": 20.518, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout
- **思维实验室**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/14583962
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/14583962
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-7008e0e9", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/14583962"}, "run": {"run_id": "rss_20260516_082510_677720_videos-7008e0e9", "source_id": "videos-7008e0e9", "status": "failed", "started_at": "2026-05-16T08:25:10.677720+00:00", "finished_at": "2026-05-16T08:25:30.769560+00:00", "duration_ms": 20092, "duration_seconds": 20.092, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout"
- **慢慢学的四饼**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/95240876
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/95240876
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-a259b3dc", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/95240876"}, "run": {"run_id": "rss_20260516_082511_468332_videos-a259b3dc", "source_id": "videos-a259b3dc", "status": "failed", "started_at": "2026-05-16T08:25:11.468332+00:00", "finished_at": "2026-05-16T08:25:31.478121+00:00", "duration_ms": 20010, "duration_seconds": 20.01, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout",
- **戴建业老师**
  - 分类：Videos/绝活娱乐
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/532741557
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/532741557
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-23b9d7b4", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/532741557"}, "run": {"run_id": "rss_20260516_082512_477784_videos-23b9d7b4", "source_id": "videos-23b9d7b4", "status": "failed", "started_at": "2026-05-16T08:25:12.477784+00:00", "finished_at": "2026-05-16T08:25:32.508384+00:00", "duration_ms": 20031, "duration_seconds": 20.031, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout
- **拣尽南枝**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/39597640
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/39597640
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-23dacd94", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/39597640"}, "run": {"run_id": "rss_20260516_082513_487949_videos-23dacd94", "source_id": "videos-23dacd94", "status": "failed", "started_at": "2026-05-16T08:25:13.487949+00:00", "finished_at": "2026-05-16T08:25:33.537665+00:00", "duration_ms": 20050, "duration_seconds": 20.05, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout",
- **新石器公园**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/489640651
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/489640651
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-d27d49e7", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/489640651"}, "run": {"run_id": "rss_20260516_082519_866329_videos-d27d49e7", "source_id": "videos-d27d49e7", "status": "failed", "started_at": "2026-05-16T08:25:19.866329+00:00", "finished_at": "2026-05-16T08:25:40.265245+00:00", "duration_ms": 20399, "duration_seconds": 20.399, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout
- **时代观察 - 乌有之乡网刊**
  - 分类：Articles/社评
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/wyzxwk/article
  - final feed_url：http://127.0.0.1:1200/wyzxwk/article
  - error_type：rsshub_503
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 503: Service Unavailable", "retryable": true, "source_id": "articles-dfa99bd5", "feed_url": "http://127.0.0.1:1200/wyzxwk/article"}, "run": {"run_id": "rss_20260516_082520_910234_articles-dfa99bd5", "source_id": "articles-dfa99bd5", "status": "failed", "started_at": "2026-05-16T08:25:20.910234+00:00", "finished_at": "2026-05-16T08:25:29.082867+00:00", "duration_ms": 8173, "duration_seconds": 8.173, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 503: Service Unavailable", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history"
- **是啤酒鸭-梗图**
  - 分类：Videos/绝活娱乐
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/1073153713
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/1073153713
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-21b8a546", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/1073153713"}, "run": {"run_id": "rss_20260516_082521_956913_videos-21b8a546", "source_id": "videos-21b8a546", "status": "failed", "started_at": "2026-05-16T08:25:21.956913+00:00", "finished_at": "2026-05-16T08:25:42.200865+00:00", "duration_ms": 20244, "duration_seconds": 20.244, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeou
- **是落拓呀**
  - 分类：Videos/长知识
  - local_xml_url：-
  - xml_url：http://127.0.0.1:1200/bilibili/user/video/43276908
  - final feed_url：http://127.0.0.1:1200/bilibili/user/video/43276908
  - error_type：timeout
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_timeout", "message": "timed out", "retryable": true, "source_id": "videos-51174438", "feed_url": "http://127.0.0.1:1200/bilibili/user/video/43276908"}, "run": {"run_id": "rss_20260516_082523_326277_videos-51174438", "source_id": "videos-51174438", "status": "failed", "started_at": "2026-05-16T08:25:23.326277+00:00", "finished_at": "2026-05-16T08:25:43.496721+00:00", "duration_ms": 20170, "duration_seconds": 20.17, "error_code": "rss_fetch_timeout", "error_message": "timed out", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null}, "error": {"error_code": "rss_fetch_timeout",
- **机器之心**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.jiqizhixin.com/rss
  - final feed_url：https://www.jiqizhixin.com/rss
  - error_type：feed_parse_error
  - error_message：{"ok": false, "error": {"error_code": "rss_parse_error", "message": "failed to parse feed: <unknown>:12:244: mismatched tag", "retryable": false, "source_id": "articles-f5d6d15c", "feed_url": "https://www.jiqizhixin.com/rss"}, "run": {"run_id": "rss_20260516_082530_314416_articles-f5d6d15c", "source_id": "articles-f5d6d15c", "status": "failed", "started_at": "2026-05-16T08:25:30.314416+00:00", "finished_at": "2026-05-16T08:25:34.595535+00:00", "duration_ms": 4281, "duration_seconds": 4.281, "error_code": "rss_parse_error", "error_message": "failed to parse feed: <unknown>:12:244: mismatched tag", "retryable": false, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null,
- **极客公园**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://www.geekpark.net/rss
  - final feed_url：https://www.geekpark.net/rss
  - error_type：unknown
  - error_message：{"ok": false, "error": {"error_code": "unknown_error", "message": "Remote end closed connection without response", "retryable": true, "source_id": "articles-8a492afd", "feed_url": "https://www.geekpark.net/rss"}, "run": {"run_id": "rss_20260516_082535_871287_articles-8a492afd", "source_id": "articles-8a492afd", "status": "failed", "started_at": "2026-05-16T08:25:35.871287+00:00", "finished_at": "2026-05-16T08:25:37.824860+00:00", "duration_ms": 1954, "duration_seconds": 1.954, "error_code": "unknown_error", "error_message": "Remote end closed connection without response", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed_limit", "incremental_decision": null, "source_has_history": null
- **歸藏的AI工具箱**
  - 分类：Articles
  - local_xml_url：-
  - xml_url：https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml
  - final feed_url：https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml
  - error_type：content_inbox_error
  - error_message：{"ok": false, "error": {"error_code": "rss_fetch_server_error", "message": "HTTP Error 500: Internal Server Error", "retryable": true, "source_id": "articles-ai-211f08a4", "feed_url": "https://wechat2rss.bestblogs.dev/feed/1fc32fedbf5da37e8e819a9298ae80724c12cb03.xml"}, "run": {"run_id": "rss_20260516_082542_027863_articles-ai-211f08a4", "source_id": "articles-ai-211f08a4", "status": "failed", "started_at": "2026-05-16T08:25:42.027863+00:00", "finished_at": "2026-05-16T08:25:43.430266+00:00", "duration_ms": 1402, "duration_seconds": 1.402, "error_code": "rss_fetch_server_error", "error_message": "HTTP Error 500: Internal Server Error", "retryable": true, "stats": {"fetched_entries": 0, "processed_entries": 0, "new_items": 0, "duplicate_items": 0, "failed_items": 0, "feed_items_seen": 0, "selected_items_for_processing": 0, "processed_items": 0}, "incremental": {"mode": "fixed_limit", "decision": null, "anchor_found": null, "anchor_index": null, "warnings": [], "incremental_mode": "fixed