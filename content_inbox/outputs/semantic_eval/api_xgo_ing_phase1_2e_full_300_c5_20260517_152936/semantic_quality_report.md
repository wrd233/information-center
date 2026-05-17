# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 234,
  "actual_tokens": 728728,
  "batch_size": 5,
  "cache_hit_tokens": 301824,
  "cache_miss_tokens": 0,
  "concurrency": 5,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 1517.69,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_9g6va8m_.sqlite3",
  "finished_at": "2026-05-17T07:54:54.040811+00:00",
  "git_commit": "601ceafb56a9657d8b5b72b5ba552f8a8b028271",
  "include_archived": false,
  "items_sampled": 300,
  "live": true,
  "max_calls": 500,
  "max_candidates": 5,
  "max_items": 300,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260517_072936_314637",
  "sample_mode": "event_hotspots",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "stage_budget_profile": "phase1_2e_profile",
  "stage_budgets": {
    "cluster_card_patch": 64000,
    "item_card": 240000,
    "item_cluster_relation": 216000,
    "item_relation": 240000,
    "source_profile": 40000
  },
  "started_at": "2026-05-17T07:29:36.314637+00:00",
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
      "sampled_item_count": 5,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 9,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_name": "ChatGPT(@ChatGPTapp)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0be252fedbe84ad7bea21be44b18da89",
      "item_count": 10,
      "latest_item_time": "2026-04-30T19:00:00+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-dify-dify-ai",
      "source_name": "Dify(@dify_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/1897eed387064dfab443764d6da50bc6",
      "item_count": 10,
      "latest_item_time": "2026-05-07T14:00:37+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_name": "ElevenLabs(@elevenlabsio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/931d6e88e067496cac6bf23f69d60f33",
      "item_count": 10,
      "latest_item_time": "2026-05-10T16:39:05+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-elvis-omarsar0",
      "source_name": "elvis(@omarsar0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/cb6169815e2e447e8e6148a4af3f9686",
      "item_count": 10,
      "latest_item_time": "2026-05-01T17:33:11+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_name": "Geoffrey Hinton(@geoffreyhinton)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/771b32075fe54a83bdb6966de9647b4f",
      "item_count": 10,
      "latest_item_time": "2026-02-18T22:04:39+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_name": "Groq Inc(@GroqInc)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e8750659b8154dbfa0489f451e044af1",
      "item_count": 10,
      "latest_item_time": "2026-05-10T19:32:11+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_name": "Guillermo Rauch(@rauchg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/58894bf2934a426ca833c682da2bc810",
      "item_count": 10,
      "latest_item_time": "2026-05-11T17:00:14+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_name": "Justin Welsh(@thejustinwelsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/db648e4d4eae4822aa0d34f0faef7ad2",
      "item_count": 10,
      "latest_item_time": "2026-04-30T06:49:02+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_name": "LovartAI(@lovart_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/221a88341acb475db221a12fed8208d0",
      "item_count": 10,
      "latest_item_time": "2026-04-30T17:30:36+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_name": "NotebookLM(@NotebookLM)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0c0856a69f9f49cf961018c32a0b0049",
      "item_count": 10,
      "latest_item_time": "2026-05-07T20:08:51+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_name": "Ray Dalio(@RayDalio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/12eba9c3db4940c5ab2a72bd00f9ff2c",
      "item_count": 10,
      "latest_item_time": "2026-04-30T14:02:05+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-replicate-replicate",
      "source_name": "Replicate(@replicate)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3953aa71e87a422eb9d7bf6ff1c7c43e",
      "item_count": 10,
      "latest_item_time": "2026-05-05T16:39:00+00:00",
      "sampled_item_count": 6,
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
      "sampled_item_count": 3,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-akshay-kothari-akothari",
      "source_name": "Akshay Kothari(@akothari)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/524525de0d69407b80f0a7d891fdc8df",
      "item_count": 9,
      "latest_item_time": "2026-04-20T17:19:14+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_name": "Alex Albert(@alexalbert__)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/edf707b5c0b248579085f66d7a3c5524",
      "item_count": 9,
      "latest_item_time": "2026-04-30T17:43:06+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 3,
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_name": "Cognition(@cognition_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/462aa134ed914f98b3491680ad9b36ed",
      "item_count": 9,
      "latest_item_time": "2026-04-30T13:11:45+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-cohere-cohere",
      "source_name": "cohere(@cohere)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/49666ce6fe3e4cb786c6574684542ec5",
      "item_count": 9,
      "latest_item_time": "2026-04-07T18:14:19+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-dario-amodei-darioamodei",
      "source_name": "Dario Amodei(@DarioAmodei)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/42e6b4901b97498eab2ab64c07d56177",
      "item_count": 9,
      "latest_item_time": "2026-05-01T00:09:55+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-eric-zakariasson-ericzakariasson",
      "source_name": "eric zakariasson(@ericzakariasson)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a4bfe44bfc0d4c949da21ebd3f5f42a5",
      "item_count": 9,
      "latest_item_time": "2026-04-07T16:48:36+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-google-ai-googleai",
      "source_name": "Google AI(@GoogleAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6fb337feeec44ca38b79491b971d868d",
      "item_count": 9,
      "latest_item_time": "2026-05-04T18:39:22+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-guizang-ai-op7418",
      "source_name": "歸藏(guizang.ai)(@op7418)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e65b5e59fcb544918c1ba17f5758f0f8",
      "item_count": 9,
      "latest_item_time": "2026-05-06T04:10:52+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-hailuo-ai-minimax-hailuo-ai",
      "source_name": "Hailuo AI (MiniMax)(@Hailuo_AI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f299207df53745bca04a03db8d11c5aa",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:31:58+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-harrison-chase-hwchase17",
      "source_name": "Harrison Chase(@hwchase17)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a9aff6b016c143ed8728dd86eb70d7db",
      "item_count": 9,
      "latest_item_time": "2026-05-11T16:14:16+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-heygen-heygen-official",
      "source_name": "HeyGen(@HeyGen_Official)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6e8e7b42cb434818810f87bcf77d86fb",
      "item_count": 9,
      "latest_item_time": "2026-04-29T13:55:43+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-hunyuan-txhunyuan",
      "source_name": "Hunyuan(@TXhunyuan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a719880fe66e4156a111187f50dae91b",
      "item_count": 9,
      "latest_item_time": "2026-04-22T16:46:12+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_name": "Kling AI(@Kling_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/862fee50a745423c87e2633b274caf1d",
      "item_count": 9,
      "latest_item_time": "2026-05-14T19:33:28+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-lee-robinson-leerob",
      "source_name": "Lee Robinson(@leerob)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/77d5ce4736854b0ebae603e4b54d3095",
      "item_count": 9,
      "latest_item_time": "2026-05-12T15:41:09+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-lenny-rachitsky-lennysan",
      "source_name": "Lenny Rachitsky(@lennysan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/adf65931519340f795e2336910b4cd15",
      "item_count": 9,
      "latest_item_time": "2026-04-09T17:56:46+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-lex-fridman-lexfridman",
      "source_name": "Lex Fridman(@lexfridman)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ca2fa444b6ea4b8b974fe148056e497a",
      "item_count": 9,
      "latest_item_time": "2026-05-06T04:41:58+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-lijigang-com",
      "source_name": "李继刚(@lijigang_com)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a8f7e2238039461cbc8bf55f5f194498",
      "item_count": 9,
      "latest_item_time": "2026-03-10T17:08:44+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-lilian-weng-lilianweng",
      "source_name": "Lilian Weng(@lilianweng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f01b088d5a39473e854b07143df77ec5",
      "item_count": 9,
      "latest_item_time": "2026-05-08T16:01:31+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_name": "lmarena.ai(@lmarena_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4f63d960de644aeebd0aa97e4994dafe",
      "item_count": 9,
      "latest_item_time": "2026-05-04T22:53:00+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-logan-kilpatrick-officiallogank",
      "source_name": "Logan Kilpatrick(@OfficialLoganK)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/639cd13d44284e10ac89fbd1c5399767",
      "item_count": 9,
      "latest_item_time": "2026-05-07T16:03:04+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-lovable-lovable-dev",
      "source_name": "Lovable(@lovable_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/320181c4651a41a08015946b55f704ab",
      "item_count": 9,
      "latest_item_time": "2026-05-06T15:01:44+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_name": "meng shao(@shao__meng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/61f4b78554fb4b8fa5653ec5d924d15a",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:57:40+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_name": "Microsoft Research(@MSFTResearch)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/72dd496bfd9d44c5a5761a974630376d",
      "item_count": 9,
      "latest_item_time": "2026-04-30T22:04:00+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_name": "Mustafa Suleyman(@mustafasuleyman)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b43bc203409e4c5a9c3ae86fe1ac00c9",
      "item_count": 9,
      "latest_item_time": "2026-05-05T03:38:58+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-naval-naval",
      "source_name": "Naval(@naval)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6ebdf0d91eef4c149acd0ef110635866",
      "item_count": 9,
      "latest_item_time": "2026-04-24T19:15:41+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-nick-st-pierre-nickfloats",
      "source_name": "Nick St. Pierre(@nickfloats)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f97a26863aec4425b021720d4f8e4ede",
      "item_count": 9,
      "latest_item_time": "2026-05-13T16:27:37+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-notion-notionhq",
      "source_name": "Notion(@NotionHQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6326c63a2dfa445bbde88bea0c3112c2",
      "item_count": 9,
      "latest_item_time": "2026-05-04T23:36:39+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-ollama-ollama",
      "source_name": "ollama(@ollama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/971dc1fc90da449bac23e5fad8a33d55",
      "item_count": 9,
      "latest_item_time": "2026-05-11T22:23:07+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-openai-developers-openaidevs",
      "source_name": "OpenAI Developers(@OpenAIDevs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e503a90c035c4b1d8f8dd34907d15bf4",
      "item_count": 9,
      "latest_item_time": "2026-05-10T18:53:21+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_name": "OpenRouter(@OpenRouterAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c65c68f3713747bba863f92d6b5e996f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T18:12:41+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T20:47:13+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-paul-couvert-itspaulai",
      "source_name": "Paul Couvert(@itsPaulAi)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/900549ddadf04e839d3f7a17ebaba3fc",
      "item_count": 9,
      "latest_item_time": "2026-05-12T13:08:46+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-paul-graham-paulg",
      "source_name": "Paul Graham(@paulg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ce352bbf72e44033985bc756db2ee0e2",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:20:22+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_name": "Philipp Schmid(@_philschmid)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3306d8b253ec4e03aca3c2e9967e7119",
      "item_count": 9,
      "latest_item_time": "2026-05-02T01:52:21+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-pika-pika-labs",
      "source_name": "Pika(@pika_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a55f6e33dd224235aabaabaaf9d58a06",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:02+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_name": "Qdrant(@qdrant_engine)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/80032d016d654eb4afe741ff34b7643d",
      "item_count": 9,
      "latest_item_time": "2026-05-01T15:14:01+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_name": "Qwen(@Alibaba_Qwen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/acc648327c614d9b985b9fc3d737165b",
      "item_count": 9,
      "latest_item_time": "2026-05-11T09:54:46+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 5,
      "source_id": "socialmedia-rowan-cheung-rowancheung",
      "source_name": "Rowan Cheung(@rowancheung)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e6bb4f612dd24db5bc1a6811e6dd5820",
      "item_count": 9,
      "latest_item_time": "2026-05-05T14:22:35+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-runway-runwayml",
      "source_name": "Runway(@runwayml)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baad3713defe4182844d2756b4c2c9ed",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:41:48+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-sahil-lavingia-shl",
      "source_name": "Sahil Lavingia(@shl)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e30d4cd223f44bed9d404807105c8927",
      "item_count": 9,
      "latest_item_time": "2026-05-09T19:16:31+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-sam-altman-sama",
      "source_name": "Sam Altman(@sama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baa68dbd9a9e461a96fd9b2e3f35dcbf",
      "item_count": 9,
      "latest_item_time": "2026-05-02T12:11:51+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-satya-nadella-satyanadella",
      "source_name": "Satya Nadella(@satyanadella)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/30ad80be93c84e44acc37d5ddf31db57",
      "item_count": 9,
      "latest_item_time": "2026-05-07T17:13:19+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-simon-willison-simonw",
      "source_name": "Simon Willison(@simonw)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6d7d398dd80b48d79669c92745d32cf6",
      "item_count": 9,
      "latest_item_time": "2026-05-06T12:03:54+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-skywork-skywork-ai",
      "source_name": "Skywork(@Skywork_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fafa6df3c67644b1a367a177240e0173",
      "item_count": 9,
      "latest_item_time": "2026-04-21T22:41:39+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-sualeh-asif-sualehasif996",
      "source_name": "Sualeh Asif(@sualehasif996)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c961547e08df4396b3ab69367a07a1cd",
      "item_count": 9,
      "latest_item_time": "2026-05-11T16:44:53+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-suhail-suhail",
      "source_name": "Suhail(@Suhail)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8324d65a63dc42c584a8c08cc8323c9f",
      "item_count": 9,
      "latest_item_time": "2026-04-29T20:49:27+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-sundar-pichai-sundarpichai",
      "source_name": "Sundar Pichai(@sundarpichai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/83b1ea38940b4a1d81ea57d1ffb12ad7",
      "item_count": 9,
      "latest_item_time": "2026-05-13T15:45:57+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-the-rundown-ai-therundownai",
      "source_name": "The Rundown AI(@TheRundownAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4918efb13c47459b8dcaa79cfdf72d09",
      "item_count": 9,
      "latest_item_time": "2026-04-29T19:01:30+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-thomas-wolf-thom-wolf",
      "source_name": "Thomas Wolf(@Thom_Wolf)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dbf37973e6fc4eae91d4be9669a78fc7",
      "item_count": 9,
      "latest_item_time": "2026-04-30T00:36:35+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-v0-v0",
      "source_name": "v0(@v0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7794c4268a504019a94af1778857a703",
      "item_count": 9,
      "latest_item_time": "2026-02-24T01:40:04+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-varun-mohan-mohansolo",
      "source_name": "Varun Mohan(@_mohansolo)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe",
      "item_count": 9,
      "latest_item_time": "2026-05-15T08:40:27+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-vista8",
      "source_name": "向阳乔木(@vista8)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2f1035ec6b28475987af06b600e1d04c",
      "item_count": 9,
      "latest_item_time": "2026-04-30T16:02:39+00:00",
      "sampled_item_count": 7,
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
      "sampled_item_count": 7,
      "source_id": "socialmedia-y-combinator-ycombinator",
      "source_name": "Y Combinator(@ycombinator)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f5f4f928dede472ea55053672ad27ab6",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:44:38+00:00",
      "sampled_item_count": 3,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_name": "andrew chen(@andrewchen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f54b2b40185943ce8f48a880110b7bc2",
      "item_count": 8,
      "latest_item_time": "2026-04-22T02:10:13+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-google-deepmind-googledeepmind",
      "source_name": "Google DeepMind(@GoogleDeepMind)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fc16750ce50741f1b1f05ea1fb29436f",
      "item_count": 8,
      "latest_item_time": "2026-04-24T07:06:35+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_name": "Hugging Face(@huggingface)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/57831559d22440debbfb2f2528e4ba84",
      "item_count": 8,
      "latest_item_time": "2026-04-09T18:58:45+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_name": "Ian Goodfellow(@goodfellow_ian)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/78d7b99318b04b309b04000f7e24da29",
      "item_count": 8,
      "latest_item_time": "2026-04-16T15:36:13+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 5,
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_name": "Monica_IM(@hey_im_monica)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4d2d4165a7524217a08d3f57f27fa190",
      "item_count": 8,
      "latest_item_time": "2026-05-04T04:34:32+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-richard-socher-richardsocher",
      "source_name": "Richard Socher(@RichardSocher)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fca8ccd87344d388bc863304ed6fd86",
      "item_count": 8,
      "latest_item_time": "2026-05-04T17:57:54+00:00",
      "sampled_item_count": 8,
      "source_id": "socialmedia-scott-wu-scottwu46",
      "source_name": "Scott Wu(@ScottWu46)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2de92402f4a24c90bb27e7580b93a878",
      "item_count": 8,
      "latest_item_time": "2026-04-24T21:21:51+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_name": "Taranjeet(@taranjeetio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fdd601ea751949e7bec9e4cdad7c8e6c",
      "item_count": 7,
      "latest_item_time": "2026-05-06T14:09:37+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-perplexity-perplexity-ai",
      "source_name": "Perplexity(@perplexity_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d5fc365556e641cba2278f501e8c6f92",
      "item_count": 7,
      "latest_item_time": "2026-04-23T07:26:58+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-stanford-ai-lab-stanfordailab",
      "source_name": "Stanford AI Lab(@StanfordAILab)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d8121d969fb34c7daad2dd2aac4ba270",
      "item_count": 5,
      "latest_item_time": "2026-03-16T23:24:00+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 2,
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
    "en_or_unknown": 288,
    "zh": 12
  },
  "source_count": 107,
  "time_range": {
    "max_created_at": "2026-05-17T07:29:37.225538+00:00",
    "min_created_at": "2026-05-17T07:29:36.995572+00:00"
  },
  "top_sources": [
    [
      "socialmedia-windsurf-windsurf-ai",
      9
    ],
    [
      "socialmedia-nvidia-ai-nvidiaai",
      9
    ],
    [
      "socialmedia-scott-wu-scottwu46",
      8
    ],
    [
      "socialmedia-perplexity-perplexity-ai",
      7
    ],
    [
      "socialmedia-the-rundown-ai-therundownai",
      7
    ],
    [
      "socialmedia-thomas-wolf-thom-wolf",
      7
    ],
    [
      "socialmedia-weaviate-vector-database-weaviate-io",
      7
    ],
    [
      "socialmedia-y-combinator-ycombinator",
      7
    ],
    [
      "socialmedia-varun-mohan-mohansolo",
      6
    ],
    [
      "socialmedia-xai-xai",
      6
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.68,
  "avg_confidence_by_tier": {
    "full": 0.771,
    "minimal": 0.55,
    "standard": 0.743
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 4157.3
  },
  "card_tier_distribution": {
    "full": 103,
    "minimal": 113,
    "standard": 84
  },
  "content_role_distribution": {
    "aggregator": 3,
    "analysis": 36,
    "commentary": 30,
    "firsthand": 9,
    "low_signal": 14,
    "report": 129,
    "source_material": 79
  },
  "entity_count_distribution": {
    "1": 10,
    "2": 41,
    "3": 59,
    "4": 53,
    "5": 47,
    "6": 39,
    "7": 21,
    "8": 14,
    "9": 5,
    "10": 3,
    "11": 3,
    "14": 2,
    "16": 1,
    "17": 1,
    "21": 1
  },
  "heuristic_card_fallback_count": 18,
  "item_cards_failed": 9,
  "item_cards_generated": 300,
  "item_cards_generated_or_reused": 300,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {
    "mixed_llm": 9
  },
  "samples": [
    {
      "item_id": "item_00562a0677fe4036bc8bfbc68086ee30",
      "role": "low_signal",
      "summary": "Monica AI announced the launch of Claude 4.7 Opus and GPT Image 2 on its platform.",
      "title": "Monica AI launches Claude 4.7 Opus and GPT Image 2"
    },
    {
      "item_id": "item_01ca25b63613425087f550e0edb71748",
      "role": "source_material",
      "summary": "Windsurf announces that Devin runs in its own cloud VM, is included with all plans, and is rolling out over 48 hours.",
      "title": "Devin runs in its own VM in the cloud"
    },
    {
      "item_id": "item_025ea693f07c434b8ab6d52f32539015",
      "role": "report",
      "summary": "Read more: robotnews.therundown.ai/p/meta-buys-a-… 💬 0 🔄 0 ❤️ 0 👀 1674 ⚡ Powered by xgo.ing",
      "title": "Read more: https://t.co/3YEhHmqg3g"
    },
    {
      "item_id": "item_028b3bc3ac0c4bebbe4da5751289b0c2",
      "role": "source_material",
      "summary": "Replit gives free access to Replit Agent on May 2nd for its 10th anniversary.",
      "title": "3 things you can build for $0 on May 2nd: your website, your research, your internal systems. We’re celebrating 10 years of Replit by giving every user FREE access to Replit Agent for the day."
    },
    {
      "item_id": "item_03abf623d87e4ccd9833c4e0272bad3c",
      "role": "source_material",
      "summary": "LlamaIndex co-hosting an AI Builders Rooftop Happy Hour with LinkupAPI during NYC FinTech Week.",
      "title": "LlamaIndex co-hosts AI Builders Rooftop Happy Hour at NYC FinTech Week"
    },
    {
      "item_id": "item_048abb5b73cf4ad4a5e87fd564892217",
      "role": "analysis",
      "summary": "Hugging Face's ml-intern agent automates post-training, achieving GPQA improvement from 10% to 32% on Qwen3-1.7B, beating Claude Code.",
      "title": "Hugging Face introduces ml-intern agent for automated post-training"
    },
    {
      "item_id": "item_04ec8f4c77404c9da3528f553b8bfcb2",
      "role": "report",
      "summary": "great deep dive from @walden_yan ! Walden @walden_yan x.com/i/article/2046… 🔗 View Quoted Tweet 💬 7 🔄 30 ❤️ 505 👀 137427 📊 177 ⚡ Powered by xgo.ing",
      "title": "great deep dive from @walden_yan!"
    },
    {
      "item_id": "item_06727f757818482cb6cd8c69566e9833",
      "role": "report",
      "summary": "another cracked swedish founder (and my amazing YC partner) 💬 11 🔄 4 ❤️ 310 👀 19742 📊 47 ⚡ Powered by xgo.ing",
      "title": "another cracked swedish founder (and my amazing YC partner)"
    },
    {
      "item_id": "item_08759dc4566241318c8352a60fb56e7c",
      "role": "report",
      "summary": "Connect to any Open Responses compatible API. 💬 2 🔄 11 ❤️ 68 👀 5227 📊 16 ⚡ Powered by xgo.ing",
      "title": "Connect to any Open Responses compatible API."
    },
    {
      "item_id": "item_0a5bffb75af54cda940c1b25c4029b1c",
      "role": "source_material",
      "summary": "v0 by Vercel announces integration with PostHog, enabling building with product data, creating feature flags, debugging targeting, and checking experiment results.",
      "title": "You can now connect v0 to your @posthog data to iterate and build with product insights and context."
    }
  ],
  "warnings_distribution": {
    "anecdotal": 1,
    "claims not independently verified": 2,
    "contains opinion": 1,
    "contains quoted opinion": 1,
    "contains subjective assessment": 1,
    "heuristic_card": 18,
    "likely_fictional": 1,
    "low_information": 1,
    "marketing": 2,
    "marketing_language": 1,
    "marketing_promotion": 1,
    "minimal_card": 113,
    "model not named": 1,
    "non_official_source": 1,
    "not confirmed": 1,
    "opinion": 1,
    "opinion_dominant": 2,
    "opinion_mixed": 1,
    "opinion_piece": 2,
    "opinionated": 1,
    "personal_opinion": 1,
    "promotional": 6,
    "promotional content": 1,
    "promotional tone": 1,
    "promotional_claim": 1,
    "promotional_content": 4,
    "promotional_language": 1,
    "quote tweet, not original source": 1,
    "quote_only": 1,
    "recruitment_post": 1,
    "reported": 1,
    "retweeted_content": 1,
    "short_social_media_post": 3,
    "social_media": 1,
    "social_media_commentary": 1,
    "social_media_post": 1,
    "social_media_quote": 1,
    "speculative": 1,
    "spelling: Anitgravity vs Antigravity": 1,
    "subjective_comparison": 1,
    "summary of a report, not original source": 1,
    "summary_only": 6,
    "thin_content": 3,
    "tweet, not official announcement": 1,
    "tweet, not official source": 1,
    "tweet: speculative opinion": 1,
    "unofficial_source": 1,
    "unsubstantiated_claims": 1,
    "unverified_claim": 1,
    "unverified_claims": 1,
    "vague_claims": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.769,
  "candidate_pairs_considered": 321,
  "candidate_priority_distribution": {
    "high": 2189,
    "low": 29,
    "medium": 1997,
    "must_run": 984,
    "suppress": 31
  },
  "candidates_suppressed_without_llm": 31,
  "cluster_eligible_count": 7,
  "different": 314,
  "duplicate": 0,
  "duplicate_direction_suppressed_count": 446,
  "event_relation_type_distribution": {
    "different": 36,
    "entity_overlap_only": 10,
    "same_account_boilerplate": 15,
    "same_event": 7,
    "same_product_different_event": 4,
    "same_topic_only": 249
  },
  "examples": [
    {
      "candidate_item_title": "So much negative thinking and panic about AI when ultimately, just like with pretty much every major...",
      "confidence": 1.0,
      "new_item_title": "Hi! For those of you who have been using Cinematic Video Overviews over the past few weeks— what do ...",
      "primary_relation": "different",
      "published_at": "2026-04-06T19:18:07+00:00",
      "reason": "No overlap in topic or event; one is about Richard Socher's commentary on AI, the other about Cinematic Video Overviews.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notebooklm-notebooklm"
    },
    {
      "candidate_item_title": "What this means in practice: → Evolves with you. The more you use it, the better it knows your work...",
      "confidence": 1.0,
      "new_item_title": "Hi! For those of you who have been using Cinematic Video Overviews over the past few weeks— what do ...",
      "primary_relation": "different",
      "published_at": "2026-04-06T19:18:07+00:00",
      "reason": "Candidate is about Skywork product promotion, completely different from Cinematic Video Overviews.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notebooklm-notebooklm"
    },
    {
      "candidate_item_title": "This pipeline is why the same base model produces more accurate, better-cited, and more efficient an...",
      "confidence": 1.0,
      "new_item_title": "Hi! For those of you who have been using Cinematic Video Overviews over the past few weeks— what do ...",
      "primary_relation": "different",
      "published_at": "2026-04-06T19:18:07+00:00",
      "reason": "Candidate is about Perplexity pipeline, no relation to Cinematic Video Overviews.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notebooklm-notebooklm"
    },
    {
      "candidate_item_title": "Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i...",
      "confidence": 1.0,
      "new_item_title": "Hi! For those of you who have been using Cinematic Video Overviews over the past few weeks— what do ...",
      "primary_relation": "different",
      "published_at": "2026-04-06T19:18:07+00:00",
      "reason": "Candidate promotes Skywork with Hermes Agent, while new item is about Cinematic Video Overviews.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notebooklm-notebooklm"
    },
    {
      "candidate_item_title": "Grok's Speech to Text API is now available. Instant, multi-speaker transcription across 25 language...",
      "confidence": 1.0,
      "new_item_title": "Hi! For those of you who have been using Cinematic Video Overviews over the past few weeks— what do ...",
      "primary_relation": "different",
      "published_at": "2026-04-06T19:18:07+00:00",
      "reason": "Candidate announces Grok STT API, no connection to Cinematic Video Overviews.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notebooklm-notebooklm"
    },
    {
      "candidate_item_title": "OpenShell v0.0.41 🧩 agent-driven policy management 🎚️ sandbox resource flags in the CLI 🔒 custom...",
      "confidence": 0.9,
      "new_item_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T22:12:42+00:00",
      "reason": "New item is about Custom Agents improvements, candidate is about OpenShell release; different products.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notion-notionhq"
    },
    {
      "candidate_item_title": "🎙️ Voice AI only feels natural when conversation keeps pace with speech. Here’s how we rebuilt our...",
      "confidence": 0.9,
      "new_item_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T22:12:42+00:00",
      "reason": "New item is about Custom Agents, candidate is about OpenAI WebRTC stack; no shared event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notion-notionhq"
    },
    {
      "candidate_item_title": "Real-time video agents are here. Today, we’re sharing how we built Runway Characters, allowing you ...",
      "confidence": 0.9,
      "new_item_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T22:12:42+00:00",
      "reason": "New item is about Custom Agents, candidate is about Runway Characters; different products and companies.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notion-notionhq"
    },
    {
      "candidate_item_title": "Here’s how you can integrate GPT-Realtime-2 to bring voice control to a CRM workflow.",
      "confidence": 0.9,
      "new_item_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T22:12:42+00:00",
      "reason": "New item is about Custom Agents, candidate is about GPT-Realtime-2 integration; different topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notion-notionhq"
    },
    {
      "candidate_item_title": "Custom Models now live. Access it through the API: https://t.co/tuGOvCZNuc See for more details: ...",
      "confidence": 0.9,
      "new_item_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T22:12:42+00:00",
      "reason": "New item is about Custom Agents, candidate is about Custom Models from Ideogram; entity overlap only.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-notion-notionhq"
    }
  ],
  "fold_candidates": 4,
  "high_priority_skips": 0,
  "llm_item_relation_calls": 80,
  "low_confidence_examples": [
    {
      "candidate_item_title": "Here’s how you can integrate GPT-Realtime-2 to bring voice control to a CRM workflow.",
      "confidence": 0.5,
      "new_item_title": "What if your team gave standup updates, and GPT-Realtime-2 moved the tickets?",
      "primary_relation": "different",
      "published_at": "2026-05-11T22:23:04+00:00",
      "reason": "Both items discuss GPT-Realtime-2 integration but for different use cases (CRM voice control vs standup ticket management).",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-developers-openaidevs"
    },
    {
      "candidate_item_title": "3 things you can build for $0 on May 2nd: your website, your research, your internal systems. We’re...",
      "confidence": 0.2,
      "new_item_title": "You can give Replit Agent 4 a try right here: https://t.co/BHgQ5SUFxb (And you’re getting $10 credi...",
      "primary_relation": "different",
      "published_at": "2026-05-01T15:22:59+00:00",
      "reason": "Both involve Replit Agent but the events are distinct: a free promotion on May 2nd vs. a general trial with $10 credits.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-paul-couvert-itspaulai"
    },
    {
      "candidate_item_title": "Try Parallel Agents today at https://t.co/6y57dDajXd",
      "confidence": 0.1,
      "new_item_title": "You can give Replit Agent 4 a try right here: https://t.co/BHgQ5SUFxb (And you’re getting $10 credi...",
      "primary_relation": "different",
      "published_at": "2026-05-01T15:22:59+00:00",
      "reason": "The candidate is about Parallel Agents, not Replit Agent. Only common entity is Replit.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-paul-couvert-itspaulai"
    },
    {
      "candidate_item_title": "Internally at NVIDIA, we use cuOpt based agentic workflows with agent skills to optimize our supply ...",
      "confidence": 0.0,
      "new_item_title": "You can give Replit Agent 4 a try right here: https://t.co/BHgQ5SUFxb (And you’re getting $10 credi...",
      "primary_relation": "different",
      "published_at": "2026-05-01T15:22:59+00:00",
      "reason": "Completely unrelated topic: NVIDIA cuOpt vs Replit Agent 4.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-paul-couvert-itspaulai"
    },
    {
      "candidate_item_title": "You can build a full pitch deck in Replit without touching a single slide. Just describe what you w...",
      "confidence": 0.1,
      "new_item_title": "You can give Replit Agent 4 a try right here: https://t.co/BHgQ5SUFxb (And you’re getting $10 credi...",
      "primary_relation": "different",
      "published_at": "2026-05-01T15:22:59+00:00",
      "reason": "Both are about Replit but different features: pitch deck builder vs Replit Agent.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-paul-couvert-itspaulai"
    },
    {
      "candidate_item_title": "Try out Grok STT here: https://t.co/PjykMmkYVv",
      "confidence": 0.0,
      "new_item_title": "You can give Replit Agent 4 a try right here: https://t.co/BHgQ5SUFxb (And you’re getting $10 credi...",
      "primary_relation": "different",
      "published_at": "2026-05-01T15:22:59+00:00",
      "reason": "Completely unrelated: Grok STT vs Replit Agent.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-paul-couvert-itspaulai"
    },
    {
      "candidate_item_title": "Get Perplexity Computer in the Microsoft Marketplace: https://t.co/T7l8LE4Hxa",
      "confidence": 0.55,
      "new_item_title": "Available to all Max and Enterprise subscribers in Perplexity and Computer. Available only in Comput...",
      "primary_relation": "different",
      "published_at": "2026-05-05T17:07:22+00:00",
      "reason": "One is about Perplexity Computer in Microsoft Marketplace, the other about premium health sources in Perplexity and Computer.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-perplexity-perplexity-ai"
    },
    {
      "candidate_item_title": "Perplexity Computer is now available in Microsoft Teams. Run research, analysis, and document creat...",
      "confidence": 0.55,
      "new_item_title": "Available to all Max and Enterprise subscribers in Perplexity and Computer. Available only in Comput...",
      "primary_relation": "different",
      "published_at": "2026-05-05T17:07:22+00:00",
      "reason": "One is about Perplexity Computer in Microsoft Teams, the other about premium health sources availability.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-perplexity-perplexity-ai"
    },
    {
      "candidate_item_title": "Visit @Vapi_AI at Interrupt! Swing by their booth during our agent conference and see how their API...",
      "confidence": 0.55,
      "new_item_title": "Available to all Max and Enterprise subscribers in Perplexity and Computer. Available only in Comput...",
      "primary_relation": "different",
      "published_at": "2026-05-05T17:07:22+00:00",
      "reason": "One is about Vapi_AI at Interrupt conference, the other about Perplexity premium health sources.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-perplexity-perplexity-ai"
    },
    {
      "candidate_item_title": "Download the latest version of Windsurf to try the Agent Command Center, Spaces, and Devin: https://...",
      "confidence": 0.55,
      "new_item_title": "Available to all Max and Enterprise subscribers in Perplexity and Computer. Available only in Comput...",
      "primary_relation": "different",
      "published_at": "2026-05-05T17:07:22+00:00",
      "reason": "One is about Windsurf Agent Command Center, the other about Perplexity premium health sources.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-perplexity-perplexity-ai"
    }
  ],
  "near_duplicate": 4,
  "raw_relation_count": 321,
  "related_with_new_info": 3,
  "related_with_new_info_count": 3,
  "relations_by_primary_relation": {
    "different": 314,
    "near_duplicate": 4,
    "related_with_new_info": 3
  },
  "uncertain_count": 0,
  "unique_relation_pair_count": 284
}
```

## 6. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 23
  },
  "attached_existing_clusters": 4,
  "avg_confidence": 0.622,
  "avg_items_per_cluster": 1.211,
  "candidate_clusters_considered": 19,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "core_facts": [
        "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of new improvements for you! Here’s whats new with Custom Agents: 💬 3 🔄 3 ❤️ 121 👀 12334 📊 23 ⚡ Powered by xgo.ing"
      ],
      "item_count": 5,
      "known_angles": [],
      "representative_items": [
        "item_3a61e695f72e44d1b77b6b2c552c88b0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Cognition-Mercedes-Benz partnership announcement",
      "core_facts": [
        "Cognition is partnering with Mercedes-Benz to deploy AI software engineering across their global engineering teams, one of the most extensive deployments in the automotive industry."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ad640f6d4f034003ac4d4345982da9c3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Runway Academy promotion",
      "core_facts": [
        "Runway encourages users to create films, ads, and ideas using Runway Academy."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_7398954c82b7435b821ae9ad72319004"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "HeyGen demonstrates Seedance 2.0 for realistic home tours",
      "core_facts": [
        "HeyGen demonstrates Seedance 2.0 with a prompt for a realistic home tour by a realtor, using a house character sheet as reference."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c9210b7e7cce49948bbcfbee95c6135e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Code Arena leaderboard update",
      "core_facts": [
        "Code Arena's frontend leaderboard for models using visual inputs in agentic coding shows significant turnover: Claude Opus 4.7 Thinking takes #1, GPT-5.5 enters at #6 and #8, Qwen-3.6 Plus enters at #9, older OpenAI and Gemini entries drop out."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_fa95941af10a4489a76c4da7d3a655f0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Publication of Young Money book",
      "core_facts": [
        "Alex Albert recommends the book 'Young Money' by Jack Raines, based on his blog about opportunity costs."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c69237af01ea49cb8fd35a1487571e58"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Meeting between Demis Hassabis and President Lee on AI safety",
      "core_facts": [
        "Demis Hassabis met with President Jaemyung Lee in Seoul to discuss AI safety and using AI to advance science."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_9093a7cfd0d4435aa287f861eb1927fe"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Devin integrated into Windsurf platform",
      "core_facts": [
        "Windsurf announces that Devin runs in its own cloud VM, is included with all plans, and is rolling out over 48 hours."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_01ca25b63613425087f550e0edb71748"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "TIME names Architects of AI as 2025 Person of the Year",
      "core_facts": [
        "Fei-Fei Li expresses surprise and gratitude for being recognized as part of TIME's 2025 Person of the Year 'Architects of AI' and shares her vision for human-centered AI and spatial intelligence."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_4836bf83c942458a9e591c5f52824e2a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Discussion on data center aesthetics",
      "core_facts": [
        "Richard Socher, quoting Mike Bird, suggests that data centers should be made beautiful to increase local acceptance, as they generate tax revenue but face opposition partly due to ugliness."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ee73caa9a3424b5b929a7bd5d3fc5d67"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Critique of creator economy sponsorship",
      "core_facts": [
        "Nick St. Pierre comments on the weirdness of creator economy sponsorship, citing HP OmniBook 7 AI 14 as an example."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c1ee82f31b8b4dcebf01b15e5a6f0169"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mistral AI Series C funding round",
      "core_facts": [
        "Mistral AI announced €1.7B Series C funding round led by ASML to accelerate AI research."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a700705c718145459ad2858b17b8ea35"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Psychohistory as a diffusion model for future prediction",
      "core_facts": [
        "Andrew Chen speculates that psychohistory from Foundation could be realized as a diffusion model trained on multiple date cutoffs, and discusses talkie, a 13B model trained only on pre-1931 text."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_bd2c2dfb937945b0afb5888d7f2f6c88"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ray Dalio promotes Digital Ray digital twin for decision-making improvement",
      "core_facts": [
        "Ray Dalio promotes 'Digital Ray' digital twin, emphasizing that improving outcomes requires evolving both design and people."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a5ec4d445db74ae7b96cf59974ee4861"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Dify webinar reminder",
      "core_facts": [
        "Dify sends a final call to sign up for the Human Input node webinar, offering a resource pack with replay and DSL files."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_fe64dae73f0148bc857415e4e8ff4914"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Open letter supporting SB 1047 by AI employees",
      "core_facts": [
        "Geoffrey Hinton endorses an open letter supporting SB 1047, signed by 110+ employees and alumni of top AI companies."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b8fb94cf5af14a77b54d668c5afe590c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Cursor SDK launch",
      "core_facts": [
        "Cursor SDK launched, with 11 projects built in the first day."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_52779e745ca1401c98ed79202f38c7b8"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Grok 4.3 release on Poe",
      "core_facts": [
        "Grok 4.3 is now available on Poe, with strong performance for daily use and tool use."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_daebc62d68ec483f86070cfedd4cf925"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LlamaIndex event at NYC FinTech Week",
      "core_facts": [
        "LlamaIndex co-hosting an AI Builders Rooftop Happy Hour with LinkupAPI during NYC FinTech Week."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_03abf623d87e4ccd9833c4e0272bad3c"
      ]
    }
  ],
  "created_clusters": 19,
  "follow_up_event": {
    "false": 23
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 1,
  "relations": {
    "new_info": 16,
    "source_material": 7
  },
  "same_event": {
    "true": 23
  },
  "same_topic": {
    "true": 23
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 23,
  "top_clusters": [
    {
      "cluster_id": "cluster_238ac9b02f884dc2b51e6a4b9932504f",
      "cluster_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
      "item_count": 5
    },
    {
      "cluster_id": "cluster_c1b363d5afed4929aa4e47e92aadbcbb",
      "cluster_title": "Cognition-Mercedes-Benz partnership announcement",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_65fa4d38ee4643c7a253ea9d149edc4b",
      "cluster_title": "Runway Academy promotion",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_a45e6bd2671f44f78d4adc7b01bb8e93",
      "cluster_title": "HeyGen demonstrates Seedance 2.0 for realistic home tours",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_a9fe32bf3fff49f3a6114494ce9a17ca",
      "cluster_title": "Code Arena leaderboard update",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_df857c587edd4dab9cc8cdae7fad82af",
      "cluster_title": "Publication of Young Money book",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_38964e1b0c74496c9340ddbad4d5fbbe",
      "cluster_title": "Meeting between Demis Hassabis and President Lee on AI safety",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b337fbe63a9b41d79ec588906496e4aa",
      "cluster_title": "Devin integrated into Windsurf platform",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_2d97c668c0a14086bd999fde2565e9f5",
      "cluster_title": "TIME names Architects of AI as 2025 Person of the Year",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_25e617fe24bd491680b73a90c4ee00ae",
      "cluster_title": "Discussion on data center aesthetics",
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
    "cluster_title": "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of ...",
    "core_facts": [
      "As Custom Agents scaled, so has the need for more control and visibility. So we shipped a number of new improvements for you! Here’s whats new with Custom Agents: 💬 3 🔄 3 ❤️ 121 👀 12334 📊 23 ⚡ Powered by xgo.ing"
    ],
    "item_count": 5,
    "known_angles": [],
    "representative_items": [
      "item_3a61e695f72e44d1b77b6b2c552c88b0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Cognition-Mercedes-Benz partnership announcement",
    "core_facts": [
      "Cognition is partnering with Mercedes-Benz to deploy AI software engineering across their global engineering teams, one of the most extensive deployments in the automotive industry."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ad640f6d4f034003ac4d4345982da9c3"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Runway Academy promotion",
    "core_facts": [
      "Runway encourages users to create films, ads, and ideas using Runway Academy."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_7398954c82b7435b821ae9ad72319004"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "HeyGen demonstrates Seedance 2.0 for realistic home tours",
    "core_facts": [
      "HeyGen demonstrates Seedance 2.0 with a prompt for a realistic home tour by a realtor, using a house character sheet as reference."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c9210b7e7cce49948bbcfbee95c6135e"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Code Arena leaderboard update",
    "core_facts": [
      "Code Arena's frontend leaderboard for models using visual inputs in agentic coding shows significant turnover: Claude Opus 4.7 Thinking takes #1, GPT-5.5 enters at #6 and #8, Qwen-3.6 Plus enters at #9, older OpenAI and Gemini entries drop out."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_fa95941af10a4489a76c4da7d3a655f0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Publication of Young Money book",
    "core_facts": [
      "Alex Albert recommends the book 'Young Money' by Jack Raines, based on his blog about opportunity costs."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c69237af01ea49cb8fd35a1487571e58"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Meeting between Demis Hassabis and President Lee on AI safety",
    "core_facts": [
      "Demis Hassabis met with President Jaemyung Lee in Seoul to discuss AI safety and using AI to advance science."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_9093a7cfd0d4435aa287f861eb1927fe"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Devin integrated into Windsurf platform",
    "core_facts": [
      "Windsurf announces that Devin runs in its own cloud VM, is included with all plans, and is rolling out over 48 hours."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_01ca25b63613425087f550e0edb71748"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "TIME names Architects of AI as 2025 Person of the Year",
    "core_facts": [
      "Fei-Fei Li expresses surprise and gratitude for being recognized as part of TIME's 2025 Person of the Year 'Architects of AI' and shares her vision for human-centered AI and spatial intelligence."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_4836bf83c942458a9e591c5f52824e2a"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Discussion on data center aesthetics",
    "core_facts": [
      "Richard Socher, quoting Mike Bird, suggests that data centers should be made beautiful to increase local acceptance, as they generate tax revenue but face opposition partly due to ugliness."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ee73caa9a3424b5b929a7bd5d3fc5d67"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Critique of creator economy sponsorship",
    "core_facts": [
      "Nick St. Pierre comments on the weirdness of creator economy sponsorship, citing HP OmniBook 7 AI 14 as an example."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c1ee82f31b8b4dcebf01b15e5a6f0169"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Mistral AI Series C funding round",
    "core_facts": [
      "Mistral AI announced €1.7B Series C funding round led by ASML to accelerate AI research."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_a700705c718145459ad2858b17b8ea35"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Psychohistory as a diffusion model for future prediction",
    "core_facts": [
      "Andrew Chen speculates that psychohistory from Foundation could be realized as a diffusion model trained on multiple date cutoffs, and discusses talkie, a 13B model trained only on pre-1931 text."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_bd2c2dfb937945b0afb5888d7f2f6c88"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Ray Dalio promotes Digital Ray digital twin for decision-making improvement",
    "core_facts": [
      "Ray Dalio promotes 'Digital Ray' digital twin, emphasizing that improving outcomes requires evolving both design and people."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_a5ec4d445db74ae7b96cf59974ee4861"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Dify webinar reminder",
    "core_facts": [
      "Dify sends a final call to sign up for the Human Input node webinar, offering a resource pack with replay and DSL files."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_fe64dae73f0148bc857415e4e8ff4914"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Open letter supporting SB 1047 by AI employees",
    "core_facts": [
      "Geoffrey Hinton endorses an open letter supporting SB 1047, signed by 110+ employees and alumni of top AI companies."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b8fb94cf5af14a77b54d668c5afe590c"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Cursor SDK launch",
    "core_facts": [
      "Cursor SDK launched, with 11 projects built in the first day."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_52779e745ca1401c98ed79202f38c7b8"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Grok 4.3 release on Poe",
    "core_facts": [
      "Grok 4.3 is now available on Poe, with strong performance for daily use and tool use."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_daebc62d68ec483f86070cfedd4cf925"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "LlamaIndex event at NYC FinTech Week",
    "core_facts": [
      "LlamaIndex co-hosting an AI Builders Rooftop Happy Hour with LinkupAPI during NYC FinTech Week."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_03abf623d87e4ccd9833c4e0272bad3c"
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
    "socialmedia-adam-d-angelo-adamdangelo": 16725,
    "socialmedia-ai-sdk-aisdk": 13554,
    "socialmedia-elevenlabs-elevenlabsio": 13529,
    "socialmedia-eric-zakariasson-ericzakariasson": 7910,
    "socialmedia-fireworks-ai-fireworksai-hq": 6706,
    "socialmedia-google-ai-googleai": 8881,
    "socialmedia-guizang-ai-op7418": 11632,
    "socialmedia-hailuo-ai-minimax-hailuo-ai": 6803,
    "socialmedia-hugging-face-huggingface": 6700,
    "socialmedia-kling-ai-kling-ai": 12367,
    "socialmedia-langchain-langchainai": 9478,
    "socialmedia-lijigang-com": 10731,
    "socialmedia-microsoft-research-msftresearch": 6993,
    "socialmedia-notion-notionhq": 6747,
    "socialmedia-nvidia-ai-nvidiaai": 15198,
    "socialmedia-ollama-ollama": 16821,
    "socialmedia-openai-developers-openaidevs": 8788,
    "socialmedia-orange-ai-oran-ge": 8979,
    "socialmedia-paul-couvert-itspaulai": 9099,
    "socialmedia-paul-graham-paulg": 11097,
    "socialmedia-perplexity-perplexity-ai": 14359,
    "socialmedia-poe-poe-platform": 6780,
    "socialmedia-qwen-alibaba-qwen": 7114,
    "socialmedia-replicate-replicate": 11593,
    "socialmedia-runway-runwayml": 18542,
    "socialmedia-sam-altman-sama": 7138,
    "socialmedia-satya-nadella-satyanadella": 15288,
    "socialmedia-scott-wu-scottwu46": 22389,
    "socialmedia-the-rundown-ai-therundownai": 11063,
    "socialmedia-windsurf-windsurf-ai": 16144
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 507,
  "reviews_suppressed_due_to_insufficient_data": 107,
  "sources_recomputed": 107,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 16725,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 5.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 13554,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-akshay-kothari-akothari",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5981,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5884,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5654,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-anton-osika-eu-acc-antonosika",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-augment-code-augmentcode",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-binyuan-hui-huybery",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5701,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2430,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-clem-129303-clementdelangue",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2430,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6150,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.2,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-cohere-cohere",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-dario-amodei-darioamodei",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 6397,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-deeplearning-ai-deeplearningai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-dify-dify-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 13529,
      "llm_yield_score": 2.5,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 2.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 16725,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 5.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 13554,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-akshay-kothari-akothari",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5981,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5884,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5654,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-anton-osika-eu-acc-antonosika",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-augment-code-augmentcode",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 5.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 13554,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5884,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-dify-dify-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 13529,
      "llm_yield_score": 2.5,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 2.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 7910,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-zakariasson-ericzakariasson",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-heygen-heygen-official",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2559,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-llamaindex-129433-llama-index",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6780,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-poe-poe-platform",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 22389,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-scott-wu-scottwu46",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 8,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 16144,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-windsurf-windsurf-ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 9,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 5.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 13554,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5884,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 5.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 13554,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5884,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-dify-dify-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 7910,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-zakariasson-ericzakariasson",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    },
    {
      "created_at": "2026-05-17T07:54:53.988324+00:00",
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
      "source_id": "socialmedia-heygen-heygen-official",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:54:53.988324+00:00"
    }
  ]
}
```

## 9. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 19808.2,
    "cache_hit_tokens": 71424,
    "cache_miss_tokens": 0,
    "calls": 63,
    "failed": 9,
    "input_tokens": 143133,
    "llm_call_count": 63,
    "operation_count": 80,
    "output_tokens": 118777,
    "p50_latency_ms": 20620,
    "p95_latency_ms": 31988,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 9,
    "skipped": 17,
    "success": 54,
    "task_type": "item_card",
    "total_tokens": 261910
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 16231.8,
    "cache_hit_tokens": 83328,
    "cache_miss_tokens": 0,
    "calls": 80,
    "failed": 16,
    "input_tokens": 139695,
    "llm_call_count": 80,
    "operation_count": 298,
    "output_tokens": 104858,
    "p50_latency_ms": 16628,
    "p95_latency_ms": 23253,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 16,
    "skipped": 218,
    "success": 64,
    "task_type": "item_relation",
    "total_tokens": 244553
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 6975.1,
    "cache_hit_tokens": 145536,
    "cache_miss_tokens": 0,
    "calls": 88,
    "failed": 1,
    "input_tokens": 165276,
    "llm_call_count": 88,
    "operation_count": 277,
    "output_tokens": 50795,
    "p50_latency_ms": 6354,
    "p95_latency_ms": 11705,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 1,
    "skipped": 189,
    "success": 87,
    "task_type": "item_cluster_relation",
    "total_tokens": 216071
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9926.0,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3535,
    "llm_call_count": 3,
    "operation_count": 22,
    "output_tokens": 2659,
    "p50_latency_ms": 9708,
    "p95_latency_ms": 14096,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 19,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6194
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
  "actual_calls": 234,
  "actual_tokens": 728728,
  "avg_latency_ms": 13632.7,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 9926.0,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 9708,
      "p95_latency_ms": 14096,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6194
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
      "avg_latency_ms": 19808.2,
      "cache_hit_tokens": 71424,
      "calls": 63,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 9,
      "p50_latency_ms": 20620,
      "p95_latency_ms": 31988,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 9,
      "success": 54,
      "task_type": "item_card",
      "total_tokens": 261910
    },
    "item_cluster_relation": {
      "avg_latency_ms": 6975.1,
      "cache_hit_tokens": 145536,
      "calls": 88,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 1,
      "p50_latency_ms": 6354,
      "p95_latency_ms": 11705,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 1,
      "success": 87,
      "task_type": "item_cluster_relation",
      "total_tokens": 216071
    },
    "item_relation": {
      "avg_latency_ms": 16231.8,
      "cache_hit_tokens": 83328,
      "calls": 80,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 16,
      "p50_latency_ms": 16628,
      "p95_latency_ms": 23253,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 16,
      "success": 64,
      "task_type": "item_relation",
      "total_tokens": 244553
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
  "cache_hit_rate": 0.4142,
  "cache_hit_tokens": 301824,
  "calls_per_sec": 0.1542,
  "db_lock_errors": 0,
  "duration_seconds": 1517.69,
  "final_failures": 26,
  "max_concurrency": 5,
  "p50_latency_ms": 11523,
  "p95_latency_ms": 28533,
  "parse_failures": 3,
  "rate_limit_errors": 0,
  "repair_retry_count": 26,
  "tokens_per_sec": 480.16
}
```

## 11. Stage Budget Summary

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "phase1_2e_profile",
  "stages": {
    "cluster_card_patch": {
      "budget": 64000,
      "calls": 3,
      "consumed_tokens": 6194,
      "remaining_budget": 57806,
      "skipped": 19,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 240000,
      "calls": 63,
      "consumed_tokens": 261910,
      "remaining_budget": 0,
      "skipped": 17,
      "skipped_due_to_budget": 17
    },
    "item_cluster_relation": {
      "budget": 216000,
      "calls": 88,
      "consumed_tokens": 216071,
      "remaining_budget": 0,
      "skipped": 189,
      "skipped_due_to_budget": 189
    },
    "item_relation": {
      "budget": 240000,
      "calls": 80,
      "consumed_tokens": 244553,
      "remaining_budget": 0,
      "skipped": 218,
      "skipped_due_to_budget": 218
    },
    "source_profile": {
      "budget": 40000,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 40000,
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
  "final_failures": 26,
  "llm_parse_failures": 0,
  "repair_retry_count": 26,
  "review_queue_entries_due_to_failure": 424,
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
  "cluster_signal_count": 23,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "26 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 15. Readiness Assessment

```json
{
  "cluster_signal_count": 23,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "26 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 16. Recommendations

- Add vector indexes for item_cards and cluster_cards before larger runs.
- Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.
- Collect more source_signals before trusting source_profile priority suggestions.
- Run a larger dry-run before any write-real-db semantic pass.
