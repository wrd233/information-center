# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 221,
  "actual_tokens": 737878,
  "batch_size": 5,
  "cache_hit_tokens": 266240,
  "cache_miss_tokens": 0,
  "concurrency": 5,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 1168.356,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_n6ixwleo.sqlite3",
  "finished_at": "2026-05-17T06:22:12.675376+00:00",
  "git_commit": "b30e4834ebf710177acced15fca3e1befb97f550",
  "include_archived": false,
  "items_sampled": 300,
  "live": true,
  "max_calls": 500,
  "max_candidates": 5,
  "max_items": 300,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260517_060244_285276",
  "sample_mode": "event_hotspots",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "stage_budget_profile": "relation_heavy",
  "stage_budgets": {
    "cluster_card_patch": 56000,
    "item_card": 256000,
    "item_cluster_relation": 192000,
    "item_relation": 272000,
    "source_profile": 24000
  },
  "started_at": "2026-05-17T06:02:44.285276+00:00",
  "strong_model": null,
  "token_budget": 800000,
  "vector_index": false,
  "warnings": [],
  "write_real_db": false
}
```

## 2. Source Scope

```json
{
  "matched_source_count": 151,
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "sources": [
    {
      "feed_url": "https://api.xgo.ing/rss/user/0277b0bbefd54df7bc6b7880122da8f7",
      "item_count": 26,
      "latest_item_time": "2026-05-17T02:16:56+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_name": "NVIDIA AI(@NVIDIAAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/74e542992cf7441390c708f5601071d4",
      "item_count": 11,
      "latest_item_time": "2026-05-12T23:47:03+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-imxiaohu",
      "source_name": "小互(@imxiaohu)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/082097117b4543e9a741cd2580f936d3",
      "item_count": 11,
      "latest_item_time": "2026-04-24T07:24:53+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-junyang-lin-justinlin610",
      "source_name": "Junyang Lin(@JustinLin610)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/179bcc4b8e5d4274b6e9e935f9fd4434",
      "item_count": 10,
      "latest_item_time": "2026-05-06T19:30:36+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-aadit-sheth-aaditsh",
      "source_name": "Aadit Sheth(@aaditsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/22af005b21ec45b1a4503acca777b7f0",
      "item_count": 10,
      "latest_item_time": "2026-03-10T20:50:07+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_name": "AI SDK(@aisdk)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/08b5488b20bc437c8bfc317a52e5c26d",
      "item_count": 10,
      "latest_item_time": "2026-04-30T16:21:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_name": "Andrew Ng(@AndrewYNg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f7992687b8d74b14bf2341eb3a0a5ec4",
      "item_count": 10,
      "latest_item_time": "2026-05-05T17:02:24+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_name": "ChatGPT(@ChatGPTapp)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0be252fedbe84ad7bea21be44b18da89",
      "item_count": 10,
      "latest_item_time": "2026-04-30T19:00:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-dify-dify-ai",
      "source_name": "Dify(@dify_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/1897eed387064dfab443764d6da50bc6",
      "item_count": 10,
      "latest_item_time": "2026-05-07T14:00:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_name": "ElevenLabs(@elevenlabsio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/931d6e88e067496cac6bf23f69d60f33",
      "item_count": 10,
      "latest_item_time": "2026-05-10T16:39:05+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-elvis-omarsar0",
      "source_name": "elvis(@omarsar0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/cb6169815e2e447e8e6148a4af3f9686",
      "item_count": 10,
      "latest_item_time": "2026-05-01T17:33:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_name": "Geoffrey Hinton(@geoffreyhinton)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/771b32075fe54a83bdb6966de9647b4f",
      "item_count": 10,
      "latest_item_time": "2026-02-18T22:04:39+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_name": "Groq Inc(@GroqInc)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e8750659b8154dbfa0489f451e044af1",
      "item_count": 10,
      "latest_item_time": "2026-05-10T19:32:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_name": "Guillermo Rauch(@rauchg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/58894bf2934a426ca833c682da2bc810",
      "item_count": 10,
      "latest_item_time": "2026-05-11T17:00:14+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_name": "Justin Welsh(@thejustinwelsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/db648e4d4eae4822aa0d34f0faef7ad2",
      "item_count": 10,
      "latest_item_time": "2026-04-30T06:49:02+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_name": "LovartAI(@lovart_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/221a88341acb475db221a12fed8208d0",
      "item_count": 10,
      "latest_item_time": "2026-04-30T17:30:36+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_name": "NotebookLM(@NotebookLM)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0c0856a69f9f49cf961018c32a0b0049",
      "item_count": 10,
      "latest_item_time": "2026-05-07T20:08:51+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-openai-openai",
      "source_name": "OpenAI(@OpenAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/17687b1051204b2dbaed4ea4c9178f28",
      "item_count": 10,
      "latest_item_time": "2026-05-02T04:37:44+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-poe-poe-platform",
      "source_name": "Poe(@poe_platform)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4838204097ed422eac24ad48e68dc3ff",
      "item_count": 10,
      "latest_item_time": "2026-05-07T21:07:12+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_name": "Ray Dalio(@RayDalio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/12eba9c3db4940c5ab2a72bd00f9ff2c",
      "item_count": 10,
      "latest_item_time": "2026-04-30T14:02:05+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-replicate-replicate",
      "source_name": "Replicate(@replicate)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3953aa71e87a422eb9d7bf6ff1c7c43e",
      "item_count": 10,
      "latest_item_time": "2026-05-05T16:39:00+00:00",
      "sampled_item_count": 10,
      "source_id": "socialmedia-xai-xai",
      "source_name": "xAI(@xai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f3fedf817599470dbf8d8d11f0872475",
      "item_count": 9,
      "latest_item_time": "2026-05-08T18:00:28+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-a16z-a16z",
      "source_name": "a16z(@a16z)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3042b6f912b24f64982cc23f7bd59681",
      "item_count": 9,
      "latest_item_time": "2026-04-28T15:15:29+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_name": "Adam D'Angelo(@adamdangelo)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0e3ebaf288014c45b0d24b71fe37312b",
      "item_count": 9,
      "latest_item_time": "2026-04-27T11:31:05+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_name": "AI Breakfast(@AiBreakfast)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7d19a619a1cc4a9896129211269d2c85",
      "item_count": 9,
      "latest_item_time": "2026-05-12T18:36:29+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_name": "AI Engineer(@aiDotEngineer)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/aa74321087f9405a872fd9a76b743bf8",
      "item_count": 9,
      "latest_item_time": "2026-05-15T08:22:59+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_name": "AI Will(@FinanceYF5)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/341f7b9f8d9b477e8bb200caa7f32c6e",
      "item_count": 9,
      "latest_item_time": "2026-05-13T12:46:05+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ak-akhaliq",
      "source_name": "AK(@_akhaliq)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3434c0d56ee0446f991fb6af42bfac4b",
      "item_count": 9,
      "latest_item_time": "2026-05-08T00:50:20+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-akshay-kothari-akothari",
      "source_name": "Akshay Kothari(@akothari)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/524525de0d69407b80f0a7d891fdc8df",
      "item_count": 9,
      "latest_item_time": "2026-04-20T17:19:14+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_name": "Alex Albert(@alexalbert__)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/edf707b5c0b248579085f66d7a3c5524",
      "item_count": 9,
      "latest_item_time": "2026-04-30T17:43:06+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_name": "Andrej Karpathy(@karpathy)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fc28a211471b496682feff329ec616e5",
      "item_count": 9,
      "latest_item_time": "2026-05-07T17:08:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-anthropic-anthropicai",
      "source_name": "Anthropic(@AnthropicAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5f13b32b124a41cfb659f903a84032b1",
      "item_count": 9,
      "latest_item_time": "2026-05-04T10:49:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-anton-osika-eu-acc-antonosika",
      "source_name": "Anton Osika – eu/acc(@antonosika)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/59e6b63ae9684d11be0ae13d9e7420f2",
      "item_count": 9,
      "latest_item_time": "2026-05-06T14:33:15+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-aravind-srinivas-aravsrinivas",
      "source_name": "Aravind Srinivas(@AravSrinivas)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e153fdd077df458b8298d975c060dcc3",
      "item_count": 9,
      "latest_item_time": "2026-05-04T23:25:51+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-augment-code-augmentcode",
      "source_name": "Augment Code(@augmentcode)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/760ab7cd9708452c9ce1f9144b92a430",
      "item_count": 9,
      "latest_item_time": "2026-04-30T23:30:36+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-bolt-new-boltdotnew",
      "source_name": "bolt.new(@boltdotnew)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b8d7530f0b294405825013bbc1cc198f",
      "item_count": 9,
      "latest_item_time": "2026-05-06T00:48:01+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-browser-use-browser-use",
      "source_name": "Browser Use(@browser_use)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/66a6b39ddcfa42e39621e0ab293c1bdd",
      "item_count": 9,
      "latest_item_time": "2026-04-30T21:29:34+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cat-catwu",
      "source_name": "cat(@_catwu)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3877c31cdb554cffb750b3b683c98c4d",
      "item_count": 9,
      "latest_item_time": "2026-04-30T21:37:28+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-character-ai-character-ai",
      "source_name": "Character.AI(@character_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4cc14cbd15c74e189d537c415369e1a7",
      "item_count": 9,
      "latest_item_time": "2026-05-05T17:00:56+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_name": "Cognition(@cognition_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/462aa134ed914f98b3491680ad9b36ed",
      "item_count": 9,
      "latest_item_time": "2026-04-30T13:11:45+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cohere-cohere",
      "source_name": "cohere(@cohere)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/49666ce6fe3e4cb786c6574684542ec5",
      "item_count": 9,
      "latest_item_time": "2026-04-07T18:14:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-dario-amodei-darioamodei",
      "source_name": "Dario Amodei(@DarioAmodei)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/42e6b4901b97498eab2ab64c07d56177",
      "item_count": 9,
      "latest_item_time": "2026-05-01T00:09:55+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-deeplearning-ai-deeplearningai",
      "source_name": "DeepLearning.AI(@DeepLearningAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/68b610deb24b47ae9a236811563cda86",
      "item_count": 9,
      "latest_item_time": "2026-04-29T02:20:52+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-deepseek-deepseek-ai",
      "source_name": "DeepSeek(@deepseek_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4a884d5e2f3740c5a26c9c093de6388a",
      "item_count": 9,
      "latest_item_time": "2026-05-02T11:34:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_name": "Demis Hassabis(@demishassabis)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6384ee3c656c48fea5e8b3cdacece4d0",
      "item_count": 9,
      "latest_item_time": "2026-03-26T17:03:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-dia-diabrowser",
      "source_name": "Dia(@diabrowser)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/65f321be670b4ffba7f40d0afd38c94d",
      "item_count": 9,
      "latest_item_time": "2026-05-07T18:18:58+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-eric-zakariasson-ericzakariasson",
      "source_name": "eric zakariasson(@ericzakariasson)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a4bfe44bfc0d4c949da21ebd3f5f42a5",
      "item_count": 9,
      "latest_item_time": "2026-04-07T16:48:36+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_name": "Fei-Fei Li(@drfeifei)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/326763c2f6154826babcfd71c5ab0f70",
      "item_count": 9,
      "latest_item_time": "2026-05-08T19:47:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-fellou-fellouai",
      "source_name": "Fellou(@FellouAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c04abb206bbf4f91b22795024d6c0614",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:11:06+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-firecrawl-firecrawl-dev",
      "source_name": "Firecrawl(@firecrawl_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/9f35c76341554bd78c2b9e63dc4fa5d8",
      "item_count": 9,
      "latest_item_time": "2026-05-06T23:42:49+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-fireworks-ai-fireworksai-hq",
      "source_name": "Fireworks AI(@FireworksAI_HQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4900b3dcd592424687582ff9e0f148ea",
      "item_count": 9,
      "latest_item_time": "2026-04-29T10:59:12+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_name": "Fish Audio(@FishAudio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/be74da51698d4cefb12b39830d6cd201",
      "item_count": 9,
      "latest_item_time": "2026-03-16T20:10:48+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-flowiseai-flowiseai",
      "source_name": "FlowiseAI(@FlowiseAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/35a38c5646d946fb894d8c30c1d9629e",
      "item_count": 9,
      "latest_item_time": "2026-05-14T06:35:28+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-gary-marcus-garymarcus",
      "source_name": "Gary Marcus(@GaryMarcus)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/71ffd342cb5d478185ef7d55bdfca011",
      "item_count": 9,
      "latest_item_time": "2026-05-05T02:48:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-genspark-genspark-ai",
      "source_name": "Genspark(@genspark_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/69d925d4a8d44221b03eecbe07bd0f74",
      "item_count": 9,
      "latest_item_time": "2026-05-04T23:11:31+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-ai-developers-googleaidevs",
      "source_name": "Google AI Developers(@googleaidevs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4de0bd2d5cef4333a0260dc8157054a7",
      "item_count": 9,
      "latest_item_time": "2026-05-01T16:10:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-ai-googleai",
      "source_name": "Google AI(@GoogleAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6fb337feeec44ca38b79491b971d868d",
      "item_count": 9,
      "latest_item_time": "2026-05-04T18:39:22+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-gemini-app-geminiapp",
      "source_name": "Google Gemini App(@GeminiApp)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/af19d054e26a49129f23abfa82d9e268",
      "item_count": 9,
      "latest_item_time": "2026-05-11T21:00:48+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-greg-brockman-gdb",
      "source_name": "Greg Brockman(@gdb)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/831fac36aa0a49a9af79f35dc1c9b5d9",
      "item_count": 9,
      "latest_item_time": "2026-05-15T02:21:02+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-guizang-ai-op7418",
      "source_name": "歸藏(guizang.ai)(@op7418)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e65b5e59fcb544918c1ba17f5758f0f8",
      "item_count": 9,
      "latest_item_time": "2026-05-06T04:10:52+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-hailuo-ai-minimax-hailuo-ai",
      "source_name": "Hailuo AI (MiniMax)(@Hailuo_AI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f299207df53745bca04a03db8d11c5aa",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:31:58+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-harrison-chase-hwchase17",
      "source_name": "Harrison Chase(@hwchase17)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a9aff6b016c143ed8728dd86eb70d7db",
      "item_count": 9,
      "latest_item_time": "2026-05-11T16:14:16+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-heygen-heygen-official",
      "source_name": "HeyGen(@HeyGen_Official)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6e8e7b42cb434818810f87bcf77d86fb",
      "item_count": 9,
      "latest_item_time": "2026-04-29T13:55:43+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-hunyuan-txhunyuan",
      "source_name": "Hunyuan(@TXhunyuan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a719880fe66e4156a111187f50dae91b",
      "item_count": 9,
      "latest_item_time": "2026-04-22T16:46:12+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ideogram-ideogram-ai",
      "source_name": "Ideogram(@ideogram_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dceb5cd131b34c72a8376cba8ea5d864",
      "item_count": 9,
      "latest_item_time": "2026-04-14T19:43:38+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jan-leike-janleike",
      "source_name": "Jan Leike(@janleike)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b1013166769c49f8aa3fbdc222867054",
      "item_count": 9,
      "latest_item_time": "2026-04-28T20:16:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jeff-dean-jeffdean",
      "source_name": "Jeff Dean(@JeffDean)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b3d904c0d7c446558ef3a1e7f2eb362b",
      "item_count": 9,
      "latest_item_time": "2026-05-06T17:44:01+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jerry-liu-jerryjliu0",
      "source_name": "Jerry Liu(@jerryjliu0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c6cfe7c0d6b74849997073233fdea840",
      "item_count": 9,
      "latest_item_time": "2026-04-01T15:15:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jim-fan-drjimfan",
      "source_name": "Jim Fan(@DrJimFan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f510f6e7eecf456ca7e2895a46752888",
      "item_count": 9,
      "latest_item_time": "2026-03-13T12:29:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jina-ai-jinaai",
      "source_name": "Jina AI(@JinaAI_)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/44d9fa384087448a94d3c8595f8d535e",
      "item_count": 9,
      "latest_item_time": "2026-05-01T17:08:33+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_name": "Julien Chaumond(@julien_c)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c61046471f174d86bc0eb76cb44a21c3",
      "item_count": 9,
      "latest_item_time": "2026-05-12T15:17:41+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-justine-moore-venturetwins",
      "source_name": "Justine Moore(@venturetwins)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/564237c3de274d58a04f064920817888",
      "item_count": 9,
      "latest_item_time": "2026-05-11T09:31:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_name": "Kling AI(@Kling_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/862fee50a745423c87e2633b274caf1d",
      "item_count": 9,
      "latest_item_time": "2026-05-14T19:33:28+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-langchain-langchainai",
      "source_name": "LangChain(@LangChainAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a7be8b61a1264ea7984abfaea3eff686",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:25:16+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-latent-space-latentspacepod",
      "source_name": "Latent.Space(@latentspacepod)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dc2426bc8348495189b45451d1707a1c",
      "item_count": 9,
      "latest_item_time": "2026-05-02T23:47:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lee-robinson-leerob",
      "source_name": "Lee Robinson(@leerob)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/77d5ce4736854b0ebae603e4b54d3095",
      "item_count": 9,
      "latest_item_time": "2026-05-12T15:41:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lenny-rachitsky-lennysan",
      "source_name": "Lenny Rachitsky(@lennysan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/adf65931519340f795e2336910b4cd15",
      "item_count": 9,
      "latest_item_time": "2026-04-09T17:56:46+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lex-fridman-lexfridman",
      "source_name": "Lex Fridman(@lexfridman)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ca2fa444b6ea4b8b974fe148056e497a",
      "item_count": 9,
      "latest_item_time": "2026-05-06T04:41:58+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lijigang-com",
      "source_name": "李继刚(@lijigang_com)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a8f7e2238039461cbc8bf55f5f194498",
      "item_count": 9,
      "latest_item_time": "2026-03-10T17:08:44+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lilian-weng-lilianweng",
      "source_name": "Lilian Weng(@lilianweng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f01b088d5a39473e854b07143df77ec5",
      "item_count": 9,
      "latest_item_time": "2026-05-08T16:01:31+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_name": "lmarena.ai(@lmarena_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4f63d960de644aeebd0aa97e4994dafe",
      "item_count": 9,
      "latest_item_time": "2026-05-04T22:53:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-logan-kilpatrick-officiallogank",
      "source_name": "Logan Kilpatrick(@OfficialLoganK)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/639cd13d44284e10ac89fbd1c5399767",
      "item_count": 9,
      "latest_item_time": "2026-05-07T16:03:04+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lovable-lovable-dev",
      "source_name": "Lovable(@lovable_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/320181c4651a41a08015946b55f704ab",
      "item_count": 9,
      "latest_item_time": "2026-05-06T15:01:44+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-manusai-manusai-hq",
      "source_name": "ManusAI(@ManusAI_HQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/94bb691baeff461686326af619beb116",
      "item_count": 9,
      "latest_item_time": "2026-05-01T23:08:57+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-mem0-mem0ai",
      "source_name": "mem0(@mem0ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/48aae530e0bf413aa7d44380f418e2e3",
      "item_count": 9,
      "latest_item_time": "2026-05-14T09:27:33+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_name": "meng shao(@shao__meng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/61f4b78554fb4b8fa5653ec5d924d15a",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:57:40+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_name": "Microsoft Research(@MSFTResearch)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/72dd496bfd9d44c5a5761a974630376d",
      "item_count": 9,
      "latest_item_time": "2026-04-30T22:04:00+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-midjourney-midjourney",
      "source_name": "Midjourney(@midjourney)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/424e67b19eed4500b7a440976bbd2ade",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:01+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-milvus-milvusio",
      "source_name": "Milvus(@milvusio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/394acfaff8c44e09936f5bc0b8504f2c",
      "item_count": 9,
      "latest_item_time": "2026-04-28T17:12:10+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_name": "Mustafa Suleyman(@mustafasuleyman)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b43bc203409e4c5a9c3ae86fe1ac00c9",
      "item_count": 9,
      "latest_item_time": "2026-05-05T03:38:58+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-naval-naval",
      "source_name": "Naval(@naval)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6ebdf0d91eef4c149acd0ef110635866",
      "item_count": 9,
      "latest_item_time": "2026-04-24T19:15:41+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-nick-st-pierre-nickfloats",
      "source_name": "Nick St. Pierre(@nickfloats)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f97a26863aec4425b021720d4f8e4ede",
      "item_count": 9,
      "latest_item_time": "2026-05-13T16:27:37+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-notion-notionhq",
      "source_name": "Notion(@NotionHQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6326c63a2dfa445bbde88bea0c3112c2",
      "item_count": 9,
      "latest_item_time": "2026-05-04T23:36:39+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-ollama-ollama",
      "source_name": "ollama(@ollama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/971dc1fc90da449bac23e5fad8a33d55",
      "item_count": 9,
      "latest_item_time": "2026-05-11T22:23:07+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-openai-developers-openaidevs",
      "source_name": "OpenAI Developers(@OpenAIDevs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e503a90c035c4b1d8f8dd34907d15bf4",
      "item_count": 9,
      "latest_item_time": "2026-05-10T18:53:21+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_name": "OpenRouter(@OpenRouterAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c65c68f3713747bba863f92d6b5e996f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T18:12:41+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T20:47:13+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-paul-couvert-itspaulai",
      "source_name": "Paul Couvert(@itsPaulAi)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/900549ddadf04e839d3f7a17ebaba3fc",
      "item_count": 9,
      "latest_item_time": "2026-05-12T13:08:46+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-paul-graham-paulg",
      "source_name": "Paul Graham(@paulg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ce352bbf72e44033985bc756db2ee0e2",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:20:22+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_name": "Philipp Schmid(@_philschmid)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3306d8b253ec4e03aca3c2e9967e7119",
      "item_count": 9,
      "latest_item_time": "2026-05-02T01:52:21+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-pika-pika-labs",
      "source_name": "Pika(@pika_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a55f6e33dd224235aabaabaaf9d58a06",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:02+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_name": "Qdrant(@qdrant_engine)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/80032d016d654eb4afe741ff34b7643d",
      "item_count": 9,
      "latest_item_time": "2026-05-01T15:14:01+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_name": "Qwen(@Alibaba_Qwen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/acc648327c614d9b985b9fc3d737165b",
      "item_count": 9,
      "latest_item_time": "2026-05-11T09:54:46+00:00",
      "sampled_item_count": 8,
      "source_id": "socialmedia-recraft-recraftai",
      "source_name": "Recraft(@recraftai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/613f859e4bc440c5a28f40732840f5cf",
      "item_count": 9,
      "latest_item_time": "2026-05-11T17:34:29+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-replit-replit",
      "source_name": "Replit ⠕(@Replit)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a636de3cbda0495daabd15b9fd298614",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:18:21+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-rowan-cheung-rowancheung",
      "source_name": "Rowan Cheung(@rowancheung)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e6bb4f612dd24db5bc1a6811e6dd5820",
      "item_count": 9,
      "latest_item_time": "2026-05-05T14:22:35+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-runway-runwayml",
      "source_name": "Runway(@runwayml)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baad3713defe4182844d2756b4c2c9ed",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:41:48+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-sahil-lavingia-shl",
      "source_name": "Sahil Lavingia(@shl)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e30d4cd223f44bed9d404807105c8927",
      "item_count": 9,
      "latest_item_time": "2026-05-09T19:16:31+00:00",
      "sampled_item_count": 8,
      "source_id": "socialmedia-sam-altman-sama",
      "source_name": "Sam Altman(@sama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baa68dbd9a9e461a96fd9b2e3f35dcbf",
      "item_count": 9,
      "latest_item_time": "2026-05-02T12:11:51+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-satya-nadella-satyanadella",
      "source_name": "Satya Nadella(@satyanadella)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/30ad80be93c84e44acc37d5ddf31db57",
      "item_count": 9,
      "latest_item_time": "2026-05-07T17:13:19+00:00",
      "sampled_item_count": 8,
      "source_id": "socialmedia-simon-willison-simonw",
      "source_name": "Simon Willison(@simonw)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6d7d398dd80b48d79669c92745d32cf6",
      "item_count": 9,
      "latest_item_time": "2026-05-06T12:03:54+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-skywork-skywork-ai",
      "source_name": "Skywork(@Skywork_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fafa6df3c67644b1a367a177240e0173",
      "item_count": 9,
      "latest_item_time": "2026-04-21T22:41:39+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-sualeh-asif-sualehasif996",
      "source_name": "Sualeh Asif(@sualehasif996)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c961547e08df4396b3ab69367a07a1cd",
      "item_count": 9,
      "latest_item_time": "2026-05-11T16:44:53+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-suhail-suhail",
      "source_name": "Suhail(@Suhail)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8324d65a63dc42c584a8c08cc8323c9f",
      "item_count": 9,
      "latest_item_time": "2026-04-29T20:49:27+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-sundar-pichai-sundarpichai",
      "source_name": "Sundar Pichai(@sundarpichai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/83b1ea38940b4a1d81ea57d1ffb12ad7",
      "item_count": 9,
      "latest_item_time": "2026-05-13T15:45:57+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-the-rundown-ai-therundownai",
      "source_name": "The Rundown AI(@TheRundownAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4918efb13c47459b8dcaa79cfdf72d09",
      "item_count": 9,
      "latest_item_time": "2026-04-29T19:01:30+00:00",
      "sampled_item_count": 8,
      "source_id": "socialmedia-thomas-wolf-thom-wolf",
      "source_name": "Thomas Wolf(@Thom_Wolf)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dbf37973e6fc4eae91d4be9669a78fc7",
      "item_count": 9,
      "latest_item_time": "2026-04-30T00:36:35+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-v0-v0",
      "source_name": "v0(@v0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7794c4268a504019a94af1778857a703",
      "item_count": 9,
      "latest_item_time": "2026-02-24T01:40:04+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-varun-mohan-mohansolo",
      "source_name": "Varun Mohan(@_mohansolo)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe",
      "item_count": 9,
      "latest_item_time": "2026-05-15T08:40:27+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-vista8",
      "source_name": "向阳乔木(@vista8)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2f1035ec6b28475987af06b600e1d04c",
      "item_count": 9,
      "latest_item_time": "2026-04-30T16:02:39+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-weaviate-vector-database-weaviate-io",
      "source_name": "Weaviate • vector database(@weaviate_io)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4a8273800ed34a069eecdb6c5c1b9ccf",
      "item_count": 9,
      "latest_item_time": "2026-04-30T17:14:35+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-windsurf-windsurf-ai",
      "source_name": "Windsurf(@windsurf_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b1ab109f6afd42ab8ea32e17a19a3a3e",
      "item_count": 9,
      "latest_item_time": "2026-05-14T15:50:00+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-y-combinator-ycombinator",
      "source_name": "Y Combinator(@ycombinator)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f5f4f928dede472ea55053672ad27ab6",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:44:38+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-yann-lecun-ylecun",
      "source_name": "Yann LeCun(@ylecun)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ef7c70f9568d45f4915169fef4ce90b4",
      "item_count": 8,
      "latest_item_time": "2026-04-24T12:03:30+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_name": "AI at Meta(@AIatMeta)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a02496979a0e4d86baf2b72c24db52a4",
      "item_count": 8,
      "latest_item_time": "2026-03-24T23:59:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_name": "Aman Sanger(@amanrsanger)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fb1814c610c4af2911caa98c5c5ef82",
      "item_count": 8,
      "latest_item_time": "2026-05-05T21:08:54+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_name": "Amjad Masad(@amasad)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a3eb6beb2d894da3a9b7ab6d2e46790e",
      "item_count": 8,
      "latest_item_time": "2026-05-07T18:02:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_name": "andrew chen(@andrewchen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f54b2b40185943ce8f48a880110b7bc2",
      "item_count": 8,
      "latest_item_time": "2026-04-22T02:10:13+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-binyuan-hui-huybery",
      "source_name": "Binyuan Hui(@huybery)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5287b4e0e13a4ab7ab7b1d56f9d88960",
      "item_count": 8,
      "latest_item_time": "2026-05-06T16:15:44+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_name": "Cursor(@cursor_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ddfdcdd4e390495c942f0b5da62af0fb",
      "item_count": 8,
      "latest_item_time": "2026-05-05T02:41:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_name": "Eric Jing(@ericjing_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f8a106a09a7d404fb8de7eb0c5ddd2a2",
      "item_count": 8,
      "latest_item_time": "2026-05-04T16:33:18+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-figma-figma",
      "source_name": "Figma(@figma)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a99538443a484fcc846bdcc8f50745ec",
      "item_count": 8,
      "latest_item_time": "2026-05-01T16:01:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-deepmind-googledeepmind",
      "source_name": "Google DeepMind(@GoogleDeepMind)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fc16750ce50741f1b1f05ea1fb29436f",
      "item_count": 8,
      "latest_item_time": "2026-04-24T07:06:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_name": "Hugging Face(@huggingface)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/57831559d22440debbfb2f2528e4ba84",
      "item_count": 8,
      "latest_item_time": "2026-04-09T18:58:45+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_name": "Ian Goodfellow(@goodfellow_ian)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/78d7b99318b04b309b04000f7e24da29",
      "item_count": 8,
      "latest_item_time": "2026-04-16T15:36:13+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_name": "Mike Krieger(@mikeyk)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8d2d03aea8af49818096da4ea00409d1",
      "item_count": 8,
      "latest_item_time": "2026-04-30T23:06:24+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_name": "Mistral AI(@MistralAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5d749cc613ec4069bb2a47334739e1b6",
      "item_count": 8,
      "latest_item_time": "2026-04-23T07:39:32+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_name": "Monica_IM(@hey_im_monica)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4d2d4165a7524217a08d3f57f27fa190",
      "item_count": 8,
      "latest_item_time": "2026-05-04T04:34:32+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-richard-socher-richardsocher",
      "source_name": "Richard Socher(@RichardSocher)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fca8ccd87344d388bc863304ed6fd86",
      "item_count": 8,
      "latest_item_time": "2026-05-04T17:57:54+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-scott-wu-scottwu46",
      "source_name": "Scott Wu(@ScottWu46)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2de92402f4a24c90bb27e7580b93a878",
      "item_count": 8,
      "latest_item_time": "2026-04-24T21:21:51+00:00",
      "sampled_item_count": 8,
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_name": "Taranjeet(@taranjeetio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fdd601ea751949e7bec9e4cdad7c8e6c",
      "item_count": 7,
      "latest_item_time": "2026-05-06T14:09:37+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-perplexity-perplexity-ai",
      "source_name": "Perplexity(@perplexity_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d5fc365556e641cba2278f501e8c6f92",
      "item_count": 7,
      "latest_item_time": "2026-04-23T07:26:58+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-stanford-ai-lab-stanfordailab",
      "source_name": "Stanford AI Lab(@StanfordAILab)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d8121d969fb34c7daad2dd2aac4ba270",
      "item_count": 5,
      "latest_item_time": "2026-03-16T23:24:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_name": "Arthur Mensch(@arthurmensch)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6bbf31cac345443585c3280320ba9009",
      "item_count": 5,
      "latest_item_time": "2026-04-29T15:45:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-berkeley-ai-research-berkeley-ai",
      "source_name": "Berkeley AI Research(@berkeley_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/97f1484ae48c430fbbf3438099743674",
      "item_count": 5,
      "latest_item_time": "2026-05-04T02:33:59+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-dotey",
      "source_name": "宝玉(@dotey)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5dbd038a8f5140938d0877511571797b",
      "item_count": 4,
      "latest_item_time": "2026-05-08T14:47:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-clem-129303-clementdelangue",
      "source_name": "clem 🤗(@ClementDelangue)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3ca3c7698fd04611a0e7d14fae93c84c",
      "item_count": 4,
      "latest_item_time": "2026-04-07T17:48:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-kevin-weil-127482-127480-kevinweil",
      "source_name": "Kevin Weil 🇺🇸(@kevinweil)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/67e259bd5be544ce84bbc867eace54c2",
      "item_count": 4,
      "latest_item_time": "2026-04-21T13:47:55+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-llamaindex-129433-llama-index",
      "source_name": "LlamaIndex 🦙(@llama_index)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/63316630d94543f5a6480f230f483008",
      "item_count": 4,
      "latest_item_time": "2026-05-16T20:13:06+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-marc-andreessen-127482-127480-pmarca",
      "source_name": "Marc Andreessen 🇺🇸(@pmarca)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/244eb9fa77ce4fa3b7fa5ceba80027a4",
      "item_count": 2,
      "latest_item_time": "2025-05-23T14:50:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-barsee-128054-heybarsee",
      "source_name": "Barsee 🐶(@heyBarsee)"
    }
  ]
}
```

## 3. Input Sample Summary

```json
{
  "items_sampled": 300,
  "items_too_short": 0,
  "items_with_raw_content": 300,
  "items_with_summary_only": 0,
  "languages": {
    "en_or_unknown": 289,
    "zh": 11
  },
  "source_count": 57,
  "time_range": {
    "max_created_at": "2026-05-17T06:02:44.978771+00:00",
    "min_created_at": "2026-05-17T06:02:44.783883+00:00"
  },
  "top_sources": [
    [
      "socialmedia-xai-xai",
      10
    ],
    [
      "socialmedia-ray-dalio-raydalio",
      9
    ],
    [
      "socialmedia-satya-nadella-satyanadella",
      9
    ],
    [
      "socialmedia-the-rundown-ai-therundownai",
      9
    ],
    [
      "socialmedia-v0-v0",
      9
    ],
    [
      "socialmedia-windsurf-windsurf-ai",
      9
    ],
    [
      "socialmedia-yann-lecun-ylecun",
      9
    ],
    [
      "socialmedia-weaviate-vector-database-weaviate-io",
      9
    ],
    [
      "socialmedia-y-combinator-ycombinator",
      9
    ],
    [
      "socialmedia-simon-willison-simonw",
      8
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.697,
  "avg_confidence_by_tier": {
    "full": 0.777,
    "minimal": 0.55,
    "standard": 0.755
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 6150.6
  },
  "card_tier_distribution": {
    "full": 99,
    "minimal": 96,
    "standard": 105
  },
  "content_role_distribution": {
    "aggregator": 2,
    "analysis": 29,
    "commentary": 39,
    "firsthand": 6,
    "low_signal": 14,
    "report": 123,
    "source_material": 87
  },
  "entity_count_distribution": {
    "0": 3,
    "1": 15,
    "2": 35,
    "3": 57,
    "4": 57,
    "5": 56,
    "6": 32,
    "7": 15,
    "8": 16,
    "9": 5,
    "10": 2,
    "11": 3,
    "15": 2,
    "17": 1,
    "23": 1
  },
  "heuristic_card_fallback_count": 25,
  "item_cards_failed": 5,
  "item_cards_generated": 300,
  "item_cards_generated_or_reused": 300,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {
    "unknown": 5
  },
  "samples": [
    {
      "item_id": "item_0020227c5ffa4367900ddf24be017f2c",
      "role": "low_signal",
      "summary": "Now it's time to really execute. Episode 2 is here. Two builders, two wildly different bets. One building AI voice tools from a farm. The other turning bartending gigs into a career engine. Who hits revenue first? Race To Revenue out Wednesday. Don't miss it.",
      "title": "Now it's time to really execute. Episode 2 is here."
    },
    {
      "item_id": "item_0021aa7f75a54dd1bd164345557e5263",
      "role": "low_signal",
      "summary": "Recraft shares four photorealistic image prompts for generating nature scenes.",
      "title": "Prompt 1: Photorealistic still life scene in a lush garden..."
    },
    {
      "item_id": "item_014630969a4643f78c953f1e7b742209",
      "role": "analysis",
      "summary": "Test-Time Training enables AI to make discoveries on open scientific problems, outperforming prompt engineering with closed models.",
      "title": "New research: Test-Time Training enables AI to discover SOTA in science with a few hundred dollars"
    },
    {
      "item_id": "item_01941afc962546799b5fcd84c9f4a44a",
      "role": "report",
      "summary": "Hallelujah I found something but I won’t reveal due to selfish gpu hoarding. 💬 8 🔄 1 ❤️ 135 👀 35956 📊 19 ⚡ Powered by xgo.ing",
      "title": "Hallelujah I found something but I won’t reveal due to selfish gpu hoarding."
    },
    {
      "item_id": "item_023cc431a62b4c13ab300e0c4d05bea7",
      "role": "report",
      "summary": "We just crossed 100k developers using Mem0 What began as an experiment to solve AI amnesia problem is now used by thousands of developers building AI agents. Grateful to everyone building and pushing us to make it better every day. Still early. A lot more to build. 💬 8 🔄 3 ❤️ 47 👀 2695 📊 15 ⚡ Powered by xgo.ing",
      "title": "We just crossed 100k developers using Mem0 What began as an experiment to solve AI amnesia problem ..."
    },
    {
      "item_id": "item_02b209317d0e4aa6822b2bd6afb87c19",
      "role": "analysis",
      "summary": "Satya Nadella describes the Rubber Duck agent that uses GPT-5.5 as a reviewer in a multi-model reflection loop.",
      "title": "Rubber Duck agent with GPT-5.5 as reviewer"
    },
    {
      "item_id": "item_02b9c8e2d9344cf290e67b12b1a7b3db",
      "role": "source_material",
      "summary": "PLAN0 (@PLAN0AI) turns architectural plans into construction cost estimates and analytics in minutes. They are building the Bloomberg of construction, with $20B of projects already running through the platform.",
      "title": "PLAN0 (@PLAN0AI) turns architectural plans into construction cost estimates and analytics"
    },
    {
      "item_id": "item_02e17f7619c845f8b3dbc4fecfaf2f3d",
      "role": "commentary",
      "summary": "Ray Dalio promotes his digital twin tool Digital Ray, emphasizing that improving outcomes requires evolving both design and people.",
      "title": "Your success depends on two things: your design and your people."
    },
    {
      "item_id": "item_0309c0c3bf0c4d34822379c6c70b9db0",
      "role": "commentary",
      "summary": "Paul Graham states that the motivation of the hobbyist is a powerful force that keeps successful founders working on their companies beyond financial need.",
      "title": "It's an unimpressive-sounding word, but one of the most powerful motivations is the motivation of the hobbyist"
    },
    {
      "item_id": "item_04face20eb404395b4827f8ac965855a",
      "role": "report",
      "summary": "we are gonna do something nice for everyone who applied for the GPT-5.5 party and that we didn't have space for. hope you enjoy! 💬 1126 🔄 158 ❤️ 6811 👀 468608 📊 1372 ⚡ Powered by xgo.ing",
      "title": "we are gonna do something nice for everyone who applied for the GPT-5.5 party and that we didn't hav..."
    }
  ],
  "warnings_distribution": {
    "biased_opinion": 1,
    "contains promotional language": 1,
    "firsthand account": 1,
    "heuristic_card": 25,
    "informal_announcement": 1,
    "job_posting": 1,
    "likely_unreliable": 1,
    "low information": 1,
    "low_engagement": 2,
    "marketing": 1,
    "marketing content": 1,
    "marketing_content": 1,
    "minimal_card": 96,
    "no factual content": 1,
    "no_verifiable_facts": 2,
    "opinion": 4,
    "opinion piece": 2,
    "opinion_based": 1,
    "opinion_heavy": 1,
    "opinion_included": 1,
    "opinion_only": 3,
    "opinion_present": 2,
    "opinion_statement": 2,
    "promotional": 3,
    "promotional language": 1,
    "promotional_content": 10,
    "results claimed, verify": 1,
    "social media source": 2,
    "social_media": 1,
    "social_media_source": 2,
    "social_media_summary": 2,
    "speculation": 2,
    "summary_only": 6,
    "thin_content": 2,
    "third_party_summary": 1,
    "too_short": 1,
    "translation_needed": 1,
    "tweet context incomplete": 1,
    "unnamed model": 1,
    "unsubstantiated_claim": 1,
    "unsupported claims": 1,
    "unverifiable claims": 1,
    "unverified_claims": 2,
    "vendor_case_study": 1,
    "转述笔记，可能失真": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.883,
  "candidate_pairs_considered": 479,
  "different": 449,
  "duplicate": 0,
  "examples": [
    {
      "candidate_item_title": "NEW: Nvidia became the first company to hit a $5.5T market cap today. CEO Jensen Huang, when asked...",
      "confidence": 0.95,
      "new_item_title": "这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch...",
      "primary_relation": "different",
      "published_at": "2026-05-13T01:07:50+00:00",
      "reason": "Unrelated topics. New item discusses a podcast about large models and organizational heroism; candidate is about Nvidia market cap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-orange-ai-oran-ge"
    },
    {
      "candidate_item_title": "Read more: https://t.co/yZgH0hEATU",
      "confidence": 0.95,
      "new_item_title": "这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch...",
      "primary_relation": "different",
      "published_at": "2026-05-13T01:07:50+00:00",
      "reason": "Unrelated topics. New item discusses a podcast about large models; candidate is a link to a site.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-orange-ai-oran-ge"
    },
    {
      "candidate_item_title": "SF Happy Hour on April 28 In town for AI Dev? Come hang with the Qdrant team 👇 → Meet builders → ...",
      "confidence": 0.95,
      "new_item_title": "这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch...",
      "primary_relation": "different",
      "published_at": "2026-05-13T01:07:50+00:00",
      "reason": "Unrelated topics. New item discusses a podcast about large models; candidate is about a happy hour event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-orange-ai-oran-ge"
    },
    {
      "candidate_item_title": "I spent a ton of time exploring everything from interning at a Robotics Startup to Lunar Space Rover...",
      "confidence": 0.95,
      "new_item_title": "这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch...",
      "primary_relation": "different",
      "published_at": "2026-05-13T01:07:50+00:00",
      "reason": "Unrelated topics. New item discusses a podcast about large models; candidate is a personal exploration story.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-orange-ai-oran-ge"
    },
    {
      "candidate_item_title": "You can now ask Gemini to create Docs, Sheets, Slides, PDFs, and more directly in your chat. No more...",
      "confidence": 0.95,
      "new_item_title": "这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch...",
      "primary_relation": "different",
      "published_at": "2026-05-13T01:07:50+00:00",
      "reason": "Unrelated topics. New item discusses a podcast about large models; candidate is about Gemini creating docs.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-orange-ai-oran-ge"
    },
    {
      "candidate_item_title": "Gemini 3.1 Pro is out and it’s a step function improvement across many domains. It’s rolling out to ...",
      "confidence": 0.95,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item about Opus 4.7 benchmarks; candidate is about Gemini 3.1 Pro release. No overlap in models or events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image...",
      "confidence": 0.95,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item about Opus 4.7 benchmarks; candidate is about Nano Banana Pro image generation. No overlap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "Kimi K2.6 is now available in Windsurf! Available for free for the next 2 weeks for Pro, Teams, and...",
      "confidence": 0.95,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item about Opus 4.7 benchmarks; candidate is about Kimi K2.6 availability. No overlap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "DeepSeek v4 Pro还是可以的。 几轮对话，实现一个工具，用xbox手柄控制电脑应用和浏览器。 当遥控器，躺床上刷小说和看视频。",
      "confidence": 0.95,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item about Opus 4.7 benchmarks; candidate is about DeepSeek v4 Pro and Xbox controller. No overlap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "v0 Auto picks the right model for your prompt, whether that's Mini for quick edits, Pro for most tas...",
      "confidence": 0.95,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item about Opus 4.7 benchmarks; candidate is about v0 model selection feature. No overlap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    }
  ],
  "fold_candidates": 4,
  "llm_item_relation_calls": 98,
  "low_confidence_examples": [
    {
      "candidate_item_title": "wow!",
      "confidence": 0.1,
      "new_item_title": "https://t.co/iMifqBlNHZ",
      "primary_relation": "different",
      "published_at": "2026-04-30T13:34:47+00:00",
      "reason": "New item is about a workflow demo for Stripe Link; candidate is about an open-source dataset. No shared entities or event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-philipp-schmid-philschmid"
    },
    {
      "candidate_item_title": "Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config...",
      "confidence": 0.1,
      "new_item_title": "https://t.co/iMifqBlNHZ",
      "primary_relation": "different",
      "published_at": "2026-04-30T13:34:47+00:00",
      "reason": "New item is about a workflow demo; candidate is about Codex import features. No shared entities or event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-philipp-schmid-philschmid"
    },
    {
      "candidate_item_title": "Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with...",
      "confidence": 0.1,
      "new_item_title": "https://t.co/iMifqBlNHZ",
      "primary_relation": "different",
      "published_at": "2026-04-30T13:34:47+00:00",
      "reason": "New item is about a workflow demo; candidate is about Windsurf 2.0 agent management. No shared entities or event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-philipp-schmid-philschmid"
    },
    {
      "candidate_item_title": "Really fun to try this app while in Sydney this week, which uses our tools to help fans deep dive in...",
      "confidence": 0.1,
      "new_item_title": "https://t.co/iMifqBlNHZ",
      "primary_relation": "different",
      "published_at": "2026-04-30T13:34:47+00:00",
      "reason": "New item is about a workflow demo; candidate is about a cricket app. No shared entities or event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-philipp-schmid-philschmid"
    },
    {
      "candidate_item_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "confidence": 0.1,
      "new_item_title": "https://t.co/iMifqBlNHZ",
      "primary_relation": "different",
      "published_at": "2026-04-30T13:34:47+00:00",
      "reason": "New item is about a workflow demo; candidate is about research focus on AI agents. No shared entities or event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-philipp-schmid-philschmid"
    },
    {
      "candidate_item_title": "Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle...",
      "confidence": 0.5,
      "new_item_title": "I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti...",
      "primary_relation": "different",
      "published_at": "2026-04-09T15:17:33+00:00",
      "reason": "New item is a generic newsletter promotion; candidate is about a specific Meta source.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-rowan-cheung-rowancheung"
    },
    {
      "candidate_item_title": "Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne...",
      "confidence": 0.5,
      "new_item_title": "I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti...",
      "primary_relation": "different",
      "published_at": "2026-04-09T15:17:33+00:00",
      "reason": "New item is a generic newsletter promotion; candidate is about a research paper link.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-rowan-cheung-rowancheung"
    },
    {
      "candidate_item_title": "We just crossed 100k developers using Mem0 What began as an experiment to solve AI amnesia problem ...",
      "confidence": 0.5,
      "new_item_title": "I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti...",
      "primary_relation": "different",
      "published_at": "2026-04-09T15:17:33+00:00",
      "reason": "New item is a generic newsletter promotion; candidate is about Mem0 milestone.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-rowan-cheung-rowancheung"
    },
    {
      "candidate_item_title": "I spent a ton of time exploring everything from interning at a Robotics Startup to Lunar Space Rover...",
      "confidence": 0.5,
      "new_item_title": "I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti...",
      "primary_relation": "different",
      "published_at": "2026-04-09T15:17:33+00:00",
      "reason": "New item is a generic newsletter promotion; candidate is a personal reflection.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-rowan-cheung-rowancheung"
    },
    {
      "candidate_item_title": "Try it now for free: https://t.co/y7IZARLPZ5",
      "confidence": 0.5,
      "new_item_title": "I break down stories like this every day in my free newsletter. Keep up with the latest in AI/Roboti...",
      "primary_relation": "different",
      "published_at": "2026-04-09T15:17:33+00:00",
      "reason": "New item is a generic newsletter promotion; candidate is about xAI console trial.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-rowan-cheung-rowancheung"
    }
  ],
  "near_duplicate": 4,
  "related_with_new_info": 24,
  "related_with_new_info_count": 24,
  "relations_by_primary_relation": {
    "different": 449,
    "near_duplicate": 4,
    "related_with_new_info": 24,
    "uncertain": 2
  },
  "uncertain_count": 2
}
```

## 6. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 19
  },
  "attached_existing_clusters": 1,
  "avg_confidence": 0.618,
  "avg_items_per_cluster": 1.056,
  "candidate_clusters_considered": 18,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "core_facts": [
        "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new research on how to actually structure AI use at work. msft.it/6016vKxQm Your browser does not support the video tag. 🔗 View on Twitter 💬 7 🔄 13 ❤️ 50 👀 9018 📊 18 ⚡ Powered by xgo.ing"
      ],
      "item_count": 2,
      "known_angles": [],
      "representative_items": [
        "item_153b053b4e2f4f7d845156e8b418851c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "NVIDIA AI highlights local AI agent capability",
      "core_facts": [
        "NVIDIA AI shares a user experience of running a 121B model locally on DGX Spark via a Hermes agent that autonomously passed all tests."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_15c586321ecc435d84c9603a5c96de7e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
      "core_facts": [
        "Ray Dalio discusses the internal battle between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8f18e494f5a14811ae5b5b2c41a9c28f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Monica AI launches Claude 4.7 Opus and GPT Image 2",
      "core_facts": [
        "Monica AI announced the launch of Claude 4.7 Opus and GPT Image 2 on their platform."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_4d31618a325b457babfe6de93534a9e4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "播客讨论：李想与老罗谈AI与商业",
      "core_facts": [
        "播客笔记记录李想与老罗关于AI、一人公司、增效降本、裁员、出海、具身智能、人的价值等话题的讨论。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3965e6d5ecd14787aa50b9cda05a3672"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mem0 and BasisSet announce 2026 AI Fellowship Agentic Memory Track",
      "core_facts": [
        "Mem0 partners with BasisSet for 2026 AI Fellowship Agentic Memory Track, applications due May 1."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_cbf825c399f3462e8e01444668c676f3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "OpenAI builds sandbox for Codex on Windows",
      "core_facts": [
        "Detailed summary of OpenAI Codex sandbox for Windows, covering design iterations and final elevated sandbox solution."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_0ef913313e7040aba5790f2990e052fa"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Book release: The Book of Elon",
      "core_facts": [
        "Eric Jorgenson's 'The Book of Elon' launched, compiled from Elon Musk's public appearances."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2ae8b16d066e4ce6803f040b7ad3524a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gemini API docs, cookbook, and Cloudflare worker example",
      "core_facts": [
        "Links to Gemini API docs, cookbook, and Cloudflare worker example repo."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ef11c4ff68b140edb01534cb11a4aa18"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qwen3.6-27B benchmark results",
      "core_facts": [
        "Qwen announces Qwen3.6-27B outperforming Qwen3.5-397B-A17B on SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.0, and SkillsBench."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f1c16295e60c464ab1d12dc414e98358"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Case study of Datagraphs integrating Qdrant for Graph RAG",
      "core_facts": [
        "Qdrant presents a case study of Datagraphs, which built a knowledge graph platform integrating Qdrant for semantic search, highlighting complementary roles of vector and graph retrieval."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_97d257ff339f4c49a1ba251516d1dccd"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qwen3.6 Plus achieves Code Arena #7 and Text Arena #36 improvements",
      "core_facts": [
        "Qwen3.6 Plus lands at #7 in Code Arena with score 1476, up 16 points, and at #36 in Text Arena, up 13 points. AlibabaGroup moves to #3 lab in Code Arena."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_beb942d4df9f410c938301d606a48137"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Satya Nadella reports Microsoft Copilot milestones",
      "core_facts": [
        "Satya Nadella reports over 20 million M365 Copilot seats, nearly 140,000 orgs using GitHub Copilot, and 2x increase in Security Copilot customers YoY."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b1a9fa40cd1540ab8fac1aefdb1f272c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gemma 4 gets Multi-Token Prediction drafters",
      "core_facts": [
        "Multi-Token Prediction drafters are here for Gemma 4, making inference up to 3x faster with zero quality loss. Available for E2B and E4B versions under Apache 2.0 license."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_071af4614d46408c8e5e9d8f3ea01606"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Replit teases Episode 2 of Race To Revenue",
      "core_facts": [
        "Now it's time to really execute. Episode 2 is coming. Two builders, two wildly different bets. One building AI voice tools from a farm. The other turning bartending gigs into a career engine. Who hits revenue first? Race To Revenue out Wednesday. Don't miss it."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c63c9cb40415424a95ef922becbc51f4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "3D soft toy character 'FEEL MORE / THINK LESS' prompt",
      "core_facts": [
        "Prompt describes a 3D soft toy-like character with glossy texture, holding a floating heart, with typography 'FEEL MORE / THINK LESS' and caption 'emotion update v2'."
      ],
      "item_count": 1,
      "known_angles": [
        "The design combines a cute character with a philosophical message."
      ],
      "representative_items": [
        "item_187faea341af48678e92d006028e10b1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Stanford SAIL and ETH demonstrate SDPO for RL with rich feedback",
      "core_facts": [
        "Stanford SAIL and ETH collaboration shows RL with rich feedback significantly outperforms scalar rewards on hard tasks, introducing SDPO."
      ],
      "item_count": 1,
      "known_angles": [
        "Rich feedback provides more granular signal for hard tasks than scalar rewards."
      ],
      "representative_items": [
        "item_eb48830993f3442688d0f4d4f262c974"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Debate on AI's impact on labor market",
      "core_facts": [
        "Yann LeCun states that Dario (likely Dario Amodei) is wrong about AI's labor market effects and advises listening to economists."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_342aa6368b3f4c39bc3051fe86d68d4b"
      ]
    }
  ],
  "created_clusters": 18,
  "follow_up_event": {
    "false": 19
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 1,
  "relations": {
    "new_info": 13,
    "repeat": 1,
    "source_material": 5
  },
  "same_event": {
    "true": 19
  },
  "same_topic": {
    "true": 19
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 18,
  "top_clusters": [
    {
      "cluster_id": "cluster_4e7dc4612e0b4942805c884e47560f1a",
      "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "item_count": 2
    },
    {
      "cluster_id": "cluster_9a8723057cb646c18f98d692b6eeb192",
      "cluster_title": "NVIDIA AI highlights local AI agent capability",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_3bfe3368634e4e9baed3a7131ebff5a3",
      "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_429b7806cd2d44d7ad8b8f1272433a98",
      "cluster_title": "Monica AI launches Claude 4.7 Opus and GPT Image 2",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b138cc46cefc4b88a597ee9aff6d898c",
      "cluster_title": "播客讨论：李想与老罗谈AI与商业",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_7ba7956fd9b846ac987dd57fb67f9e4b",
      "cluster_title": "Mem0 and BasisSet announce 2026 AI Fellowship Agentic Memory Track",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_37bda0c305c04f99bd815c9170115f61",
      "cluster_title": "OpenAI builds sandbox for Codex on Windows",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_ad01c1e298ee467aa7ae9f354a10c8ca",
      "cluster_title": "Book release: The Book of Elon",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_4de395df04e947588eef52b3f7df04ee",
      "cluster_title": "Gemini API docs, cookbook, and Cloudflare worker example",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_41aa703f8a7f4e3f819cc178e2d665a6",
      "cluster_title": "Qwen3.6-27B benchmark results",
      "item_count": 1
    }
  ],
  "uncertain_clusters": 0
}
```

## 7. Cluster Quality Samples

```json
[
  {
    "cluster_status": "active",
    "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
    "core_facts": [
      "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new research on how to actually structure AI use at work. msft.it/6016vKxQm Your browser does not support the video tag. 🔗 View on Twitter 💬 7 🔄 13 ❤️ 50 👀 9018 📊 18 ⚡ Powered by xgo.ing"
    ],
    "item_count": 2,
    "known_angles": [],
    "representative_items": [
      "item_153b053b4e2f4f7d845156e8b418851c"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "NVIDIA AI highlights local AI agent capability",
    "core_facts": [
      "NVIDIA AI shares a user experience of running a 121B model locally on DGX Spark via a Hermes agent that autonomously passed all tests."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_15c586321ecc435d84c9603a5c96de7e"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
    "core_facts": [
      "Ray Dalio discusses the internal battle between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex)."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_8f18e494f5a14811ae5b5b2c41a9c28f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Monica AI launches Claude 4.7 Opus and GPT Image 2",
    "core_facts": [
      "Monica AI announced the launch of Claude 4.7 Opus and GPT Image 2 on their platform."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_4d31618a325b457babfe6de93534a9e4"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "播客讨论：李想与老罗谈AI与商业",
    "core_facts": [
      "播客笔记记录李想与老罗关于AI、一人公司、增效降本、裁员、出海、具身智能、人的价值等话题的讨论。"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_3965e6d5ecd14787aa50b9cda05a3672"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Mem0 and BasisSet announce 2026 AI Fellowship Agentic Memory Track",
    "core_facts": [
      "Mem0 partners with BasisSet for 2026 AI Fellowship Agentic Memory Track, applications due May 1."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_cbf825c399f3462e8e01444668c676f3"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "OpenAI builds sandbox for Codex on Windows",
    "core_facts": [
      "Detailed summary of OpenAI Codex sandbox for Windows, covering design iterations and final elevated sandbox solution."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_0ef913313e7040aba5790f2990e052fa"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Book release: The Book of Elon",
    "core_facts": [
      "Eric Jorgenson's 'The Book of Elon' launched, compiled from Elon Musk's public appearances."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2ae8b16d066e4ce6803f040b7ad3524a"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Gemini API docs, cookbook, and Cloudflare worker example",
    "core_facts": [
      "Links to Gemini API docs, cookbook, and Cloudflare worker example repo."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ef11c4ff68b140edb01534cb11a4aa18"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Qwen3.6-27B benchmark results",
    "core_facts": [
      "Qwen announces Qwen3.6-27B outperforming Qwen3.5-397B-A17B on SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.0, and SkillsBench."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f1c16295e60c464ab1d12dc414e98358"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Case study of Datagraphs integrating Qdrant for Graph RAG",
    "core_facts": [
      "Qdrant presents a case study of Datagraphs, which built a knowledge graph platform integrating Qdrant for semantic search, highlighting complementary roles of vector and graph retrieval."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_97d257ff339f4c49a1ba251516d1dccd"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Qwen3.6 Plus achieves Code Arena #7 and Text Arena #36 improvements",
    "core_facts": [
      "Qwen3.6 Plus lands at #7 in Code Arena with score 1476, up 16 points, and at #36 in Text Arena, up 13 points. AlibabaGroup moves to #3 lab in Code Arena."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_beb942d4df9f410c938301d606a48137"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Satya Nadella reports Microsoft Copilot milestones",
    "core_facts": [
      "Satya Nadella reports over 20 million M365 Copilot seats, nearly 140,000 orgs using GitHub Copilot, and 2x increase in Security Copilot customers YoY."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b1a9fa40cd1540ab8fac1aefdb1f272c"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Gemma 4 gets Multi-Token Prediction drafters",
    "core_facts": [
      "Multi-Token Prediction drafters are here for Gemma 4, making inference up to 3x faster with zero quality loss. Available for E2B and E4B versions under Apache 2.0 license."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_071af4614d46408c8e5e9d8f3ea01606"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Replit teases Episode 2 of Race To Revenue",
    "core_facts": [
      "Now it's time to really execute. Episode 2 is coming. Two builders, two wildly different bets. One building AI voice tools from a farm. The other turning bartending gigs into a career engine. Who hits revenue first? Race To Revenue out Wednesday. Don't miss it."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c63c9cb40415424a95ef922becbc51f4"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "3D soft toy character 'FEEL MORE / THINK LESS' prompt",
    "core_facts": [
      "Prompt describes a 3D soft toy-like character with glossy texture, holding a floating heart, with typography 'FEEL MORE / THINK LESS' and caption 'emotion update v2'."
    ],
    "item_count": 1,
    "known_angles": [
      "The design combines a cute character with a philosophical message."
    ],
    "representative_items": [
      "item_187faea341af48678e92d006028e10b1"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Stanford SAIL and ETH demonstrate SDPO for RL with rich feedback",
    "core_facts": [
      "Stanford SAIL and ETH collaboration shows RL with rich feedback significantly outperforms scalar rewards on hard tasks, introducing SDPO."
    ],
    "item_count": 1,
    "known_angles": [
      "Rich feedback provides more granular signal for hard tasks than scalar rewards."
    ],
    "representative_items": [
      "item_eb48830993f3442688d0f4d4f262c974"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Debate on AI's impact on labor market",
    "core_facts": [
      "Yann LeCun states that Dario (likely Dario Amodei) is wrong about AI's labor market effects and advises listening to economists."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_342aa6368b3f4c39bc3051fe86d68d4b"
    ]
  }
]
```

## 8. Source Profile Results

```json
{
  "disabled_for_llm_candidates": [],
  "high_candidates": [],
  "llm_total_tokens_by_source": {
    "socialmedia-microsoft-research-msftresearch": 9630,
    "socialmedia-mike-krieger-mikeyk": 6156,
    "socialmedia-naval-naval": 9972,
    "socialmedia-nvidia-ai-nvidiaai": 8889,
    "socialmedia-openai-developers-openaidevs": 5678,
    "socialmedia-openai-openai": 5555,
    "socialmedia-orange-ai-oran-ge": 5833,
    "socialmedia-paul-couvert-itspaulai": 6313,
    "socialmedia-perplexity-perplexity-ai": 5606,
    "socialmedia-pika-pika-labs": 11440,
    "socialmedia-qdrant-qdrant-engine": 10262,
    "socialmedia-recraft-recraftai": 9646,
    "socialmedia-rowan-cheung-rowancheung": 17108,
    "socialmedia-runway-runwayml": 24958,
    "socialmedia-sahil-lavingia-shl": 14596,
    "socialmedia-sam-altman-sama": 40570,
    "socialmedia-satya-nadella-satyanadella": 27615,
    "socialmedia-scott-wu-scottwu46": 20967,
    "socialmedia-simon-willison-simonw": 33599,
    "socialmedia-skywork-skywork-ai": 26785,
    "socialmedia-stanford-ai-lab-stanfordailab": 7675,
    "socialmedia-sualeh-asif-sualehasif996": 11144,
    "socialmedia-suhail-suhail": 20855,
    "socialmedia-taranjeet-taranjeetio": 9539,
    "socialmedia-the-rundown-ai-therundownai": 22611,
    "socialmedia-thomas-wolf-thom-wolf": 5636,
    "socialmedia-v0-v0": 11053,
    "socialmedia-varun-mohan-mohansolo": 15155,
    "socialmedia-vista8": 17451,
    "socialmedia-windsurf-windsurf-ai": 19530
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 480,
  "reviews_suppressed_due_to_insufficient_data": 57,
  "sources_recomputed": 57,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5261,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-marc-andreessen-127482-127480-pmarca",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9630,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-midjourney-midjourney",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6156,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-milvus-milvusio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9972,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-naval-naval",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 2991,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-notion-notionhq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 8889,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ollama-ollama",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5678,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-developers-openaidevs",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5555,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4928,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5833,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5261,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-marc-andreessen-127482-127480-pmarca",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9630,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-midjourney-midjourney",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6156,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-milvus-milvusio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9630,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9972,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-naval-naval",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 8889,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5833,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5223,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5072,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10262,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.2857142857142857,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 27615,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-satya-nadella-satyanadella",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 9,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9630,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9972,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-naval-naval",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 8889,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5833,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5223,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9630,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9972,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-naval-naval",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 8889,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5833,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5223,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5072,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    },
    {
      "created_at": "2026-05-17T06:22:12.634531+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10262,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T06:22:12.634531+00:00"
    }
  ]
}
```

## 9. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 27806.4,
    "cache_hit_tokens": 62848,
    "cache_miss_tokens": 0,
    "calls": 41,
    "failed": 5,
    "input_tokens": 131229,
    "llm_call_count": 41,
    "operation_count": 41,
    "output_tokens": 120945,
    "p50_latency_ms": 28205,
    "p95_latency_ms": 33210,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 5,
    "skipped": 0,
    "success": 36,
    "task_type": "item_card",
    "total_tokens": 252174
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 10857.7,
    "cache_hit_tokens": 72192,
    "cache_miss_tokens": 0,
    "calls": 98,
    "failed": 3,
    "input_tokens": 180696,
    "llm_call_count": 98,
    "operation_count": 296,
    "output_tokens": 106217,
    "p50_latency_ms": 9192,
    "p95_latency_ms": 18103,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 3,
    "skipped": 198,
    "success": 95,
    "task_type": "item_relation",
    "total_tokens": 286913
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 6234.8,
    "cache_hit_tokens": 129664,
    "cache_miss_tokens": 0,
    "calls": 79,
    "failed": 0,
    "input_tokens": 148847,
    "llm_call_count": 79,
    "operation_count": 278,
    "output_tokens": 43332,
    "p50_latency_ms": 5590,
    "p95_latency_ms": 10657,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 199,
    "success": 79,
    "task_type": "item_cluster_relation",
    "total_tokens": 192179
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9100.3,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3987,
    "llm_call_count": 3,
    "operation_count": 21,
    "output_tokens": 2625,
    "p50_latency_ms": 7186,
    "p95_latency_ms": 13094,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 18,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6612
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 0,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 0,
    "task_type": "cluster_card_rebuild",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 0,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 0,
    "task_type": "source_review",
    "total_tokens": 0
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 0.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 0,
    "failed": 0,
    "input_tokens": 0,
    "llm_call_count": 0,
    "operation_count": 0,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 0,
    "task_type": "json_repair",
    "total_tokens": 0
  }
]
```

## 10. Concurrency Summary

```json
{
  "actual_calls": 221,
  "actual_tokens": 737878,
  "avg_latency_ms": 12325.7,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 9100.3,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 7186,
      "p95_latency_ms": 13094,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6612
    },
    "cluster_card_rebuild": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 0,
      "p95_latency_ms": 0,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 0,
      "task_type": "cluster_card_rebuild",
      "total_tokens": 0
    },
    "item_card": {
      "avg_latency_ms": 27806.4,
      "cache_hit_tokens": 62848,
      "calls": 41,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 5,
      "p50_latency_ms": 28205,
      "p95_latency_ms": 33210,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 5,
      "success": 36,
      "task_type": "item_card",
      "total_tokens": 252174
    },
    "item_cluster_relation": {
      "avg_latency_ms": 6234.8,
      "cache_hit_tokens": 129664,
      "calls": 79,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 5590,
      "p95_latency_ms": 10657,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 79,
      "task_type": "item_cluster_relation",
      "total_tokens": 192179
    },
    "item_relation": {
      "avg_latency_ms": 10857.7,
      "cache_hit_tokens": 72192,
      "calls": 98,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 3,
      "p50_latency_ms": 9192,
      "p95_latency_ms": 18103,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 3,
      "success": 95,
      "task_type": "item_relation",
      "total_tokens": 286913
    },
    "json_repair": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 0,
      "p95_latency_ms": 0,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 0,
      "task_type": "json_repair",
      "total_tokens": 0
    },
    "source_review": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 0,
      "p95_latency_ms": 0,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 0,
      "task_type": "source_review",
      "total_tokens": 0
    }
  },
  "cache_hit_rate": 0.3608,
  "cache_hit_tokens": 266240,
  "calls_per_sec": 0.1892,
  "db_lock_errors": 0,
  "duration_seconds": 1168.356,
  "final_failures": 8,
  "max_concurrency": 5,
  "p50_latency_ms": 8350,
  "p95_latency_ms": 30641,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 8,
  "tokens_per_sec": 631.55
}
```

## 11. Stage Budget Summary

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "relation_heavy",
  "stages": {
    "cluster_card_patch": {
      "budget": 56000,
      "calls": 3,
      "consumed_tokens": 6612,
      "remaining_budget": 49388,
      "skipped": 18,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 256000,
      "calls": 41,
      "consumed_tokens": 252174,
      "remaining_budget": 3826,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_cluster_relation": {
      "budget": 192000,
      "calls": 79,
      "consumed_tokens": 192179,
      "remaining_budget": 0,
      "skipped": 199,
      "skipped_due_to_budget": 199
    },
    "item_relation": {
      "budget": 272000,
      "calls": 98,
      "consumed_tokens": 286913,
      "remaining_budget": 0,
      "skipped": 198,
      "skipped_due_to_budget": 198
    },
    "source_profile": {
      "budget": 24000,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 24000,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 800000
}
```

## 12. Errors / Fallbacks / Retries

```json
{
  "db_lock_errors": 0,
  "final_failures": 8,
  "llm_parse_failures": 0,
  "repair_retry_count": 8,
  "review_queue_entries_due_to_failure": 400,
  "skipped_due_to_max_calls": false,
  "skipped_due_to_missing_card": 0,
  "skipped_due_to_no_candidate": 0,
  "skipped_due_to_token_budget": false
}
```

## 13. Prompt Iteration Notes

```json
[
  {
    "changes": [
      "source scope filtering",
      "sample modes",
      "operation_count versus llm_call_count report split",
      "concurrency summary"
    ],
    "concurrency": 5,
    "iteration": "phase1_2_current",
    "max_calls": 500,
    "max_items": 300,
    "notes": "No enum expansion; prompt JSON contracts remain stable.",
    "sample_mode": "event_hotspots"
  }
]
```

## 14. Manual Review Suggestions

```json
{
  "high_uncertain": [],
  "possible_miscluster": [],
  "possible_missplit": [],
  "top_review_items_or_clusters": []
}
```

## 14. Readiness Assessment

```json
{
  "cluster_signal_count": 19,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "8 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 15. Readiness Assessment

```json
{
  "cluster_signal_count": 19,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "8 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 16. Recommendations

- Review uncertain relations and tune prompts with real examples.
- Add vector indexes for item_cards and cluster_cards before larger runs.
- Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.
- Collect more source_signals before trusting source_profile priority suggestions.
- Run a larger dry-run before any write-real-db semantic pass.
