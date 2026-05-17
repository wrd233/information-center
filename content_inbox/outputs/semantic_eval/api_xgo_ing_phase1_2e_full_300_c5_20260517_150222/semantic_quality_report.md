# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 238,
  "actual_tokens": 742676,
  "batch_size": 5,
  "cache_hit_tokens": 269824,
  "cache_miss_tokens": 0,
  "concurrency": 5,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 1567.949,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_bj3um5ih.sqlite3",
  "finished_at": "2026-05-17T07:28:30.455101+00:00",
  "git_commit": "601ceafb56a9657d8b5b72b5ba552f8a8b028271",
  "include_archived": false,
  "items_sampled": 300,
  "live": true,
  "max_calls": 500,
  "max_candidates": 5,
  "max_items": 300,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260517_070222_464741",
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
  "started_at": "2026-05-17T07:02:22.464741+00:00",
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_name": "Guillermo Rauch(@rauchg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/58894bf2934a426ca833c682da2bc810",
      "item_count": 10,
      "latest_item_time": "2026-05-11T17:00:14+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_name": "Justin Welsh(@thejustinwelsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/db648e4d4eae4822aa0d34f0faef7ad2",
      "item_count": 10,
      "latest_item_time": "2026-04-30T06:49:02+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_name": "LovartAI(@lovart_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/221a88341acb475db221a12fed8208d0",
      "item_count": 10,
      "latest_item_time": "2026-04-30T17:30:36+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_name": "NotebookLM(@NotebookLM)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0c0856a69f9f49cf961018c32a0b0049",
      "item_count": 10,
      "latest_item_time": "2026-05-07T20:08:51+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-openai-openai",
      "source_name": "OpenAI(@OpenAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/17687b1051204b2dbaed4ea4c9178f28",
      "item_count": 10,
      "latest_item_time": "2026-05-02T04:37:44+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-poe-poe-platform",
      "source_name": "Poe(@poe_platform)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4838204097ed422eac24ad48e68dc3ff",
      "item_count": 10,
      "latest_item_time": "2026-05-07T21:07:12+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_name": "Ray Dalio(@RayDalio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/12eba9c3db4940c5ab2a72bd00f9ff2c",
      "item_count": 10,
      "latest_item_time": "2026-04-30T14:02:05+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-replicate-replicate",
      "source_name": "Replicate(@replicate)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3953aa71e87a422eb9d7bf6ff1c7c43e",
      "item_count": 10,
      "latest_item_time": "2026-05-05T16:39:00+00:00",
      "sampled_item_count": 8,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_name": "Julien Chaumond(@julien_c)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c61046471f174d86bc0eb76cb44a21c3",
      "item_count": 9,
      "latest_item_time": "2026-05-12T15:17:41+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-justine-moore-venturetwins",
      "source_name": "Justine Moore(@venturetwins)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/564237c3de274d58a04f064920817888",
      "item_count": 9,
      "latest_item_time": "2026-05-11T09:31:09+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 3,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-midjourney-midjourney",
      "source_name": "Midjourney(@midjourney)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/424e67b19eed4500b7a440976bbd2ade",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:01+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-milvus-milvusio",
      "source_name": "Milvus(@milvusio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/394acfaff8c44e09936f5bc0b8504f2c",
      "item_count": 9,
      "latest_item_time": "2026-04-28T17:12:10+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-notion-notionhq",
      "source_name": "Notion(@NotionHQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6326c63a2dfa445bbde88bea0c3112c2",
      "item_count": 9,
      "latest_item_time": "2026-05-04T23:36:39+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-ollama-ollama",
      "source_name": "ollama(@ollama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/971dc1fc90da449bac23e5fad8a33d55",
      "item_count": 9,
      "latest_item_time": "2026-05-11T22:23:07+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T20:47:13+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-paul-couvert-itspaulai",
      "source_name": "Paul Couvert(@itsPaulAi)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/900549ddadf04e839d3f7a17ebaba3fc",
      "item_count": 9,
      "latest_item_time": "2026-05-12T13:08:46+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-paul-graham-paulg",
      "source_name": "Paul Graham(@paulg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ce352bbf72e44033985bc756db2ee0e2",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:20:22+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_name": "Philipp Schmid(@_philschmid)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3306d8b253ec4e03aca3c2e9967e7119",
      "item_count": 9,
      "latest_item_time": "2026-05-02T01:52:21+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-pika-pika-labs",
      "source_name": "Pika(@pika_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a55f6e33dd224235aabaabaaf9d58a06",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:02+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_name": "Qdrant(@qdrant_engine)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/80032d016d654eb4afe741ff34b7643d",
      "item_count": 9,
      "latest_item_time": "2026-05-01T15:14:01+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_name": "Qwen(@Alibaba_Qwen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/acc648327c614d9b985b9fc3d737165b",
      "item_count": 9,
      "latest_item_time": "2026-05-11T09:54:46+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-recraft-recraftai",
      "source_name": "Recraft(@recraftai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/613f859e4bc440c5a28f40732840f5cf",
      "item_count": 9,
      "latest_item_time": "2026-05-11T17:34:29+00:00",
      "sampled_item_count": 7,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-sahil-lavingia-shl",
      "source_name": "Sahil Lavingia(@shl)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e30d4cd223f44bed9d404807105c8927",
      "item_count": 9,
      "latest_item_time": "2026-05-09T19:16:31+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-sam-altman-sama",
      "source_name": "Sam Altman(@sama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baa68dbd9a9e461a96fd9b2e3f35dcbf",
      "item_count": 9,
      "latest_item_time": "2026-05-02T12:11:51+00:00",
      "sampled_item_count": 7,
      "source_id": "socialmedia-satya-nadella-satyanadella",
      "source_name": "Satya Nadella(@satyanadella)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/30ad80be93c84e44acc37d5ddf31db57",
      "item_count": 9,
      "latest_item_time": "2026-05-07T17:13:19+00:00",
      "sampled_item_count": 9,
      "source_id": "socialmedia-simon-willison-simonw",
      "source_name": "Simon Willison(@simonw)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6d7d398dd80b48d79669c92745d32cf6",
      "item_count": 9,
      "latest_item_time": "2026-05-06T12:03:54+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-suhail-suhail",
      "source_name": "Suhail(@Suhail)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8324d65a63dc42c584a8c08cc8323c9f",
      "item_count": 9,
      "latest_item_time": "2026-04-29T20:49:27+00:00",
      "sampled_item_count": 8,
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
      "sampled_item_count": 6,
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
      "sampled_item_count": 9,
      "source_id": "socialmedia-weaviate-vector-database-weaviate-io",
      "source_name": "Weaviate • vector database(@weaviate_io)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4a8273800ed34a069eecdb6c5c1b9ccf",
      "item_count": 9,
      "latest_item_time": "2026-04-30T17:14:35+00:00",
      "sampled_item_count": 8,
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
      "sampled_item_count": 8,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_name": "Mistral AI(@MistralAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5d749cc613ec4069bb2a47334739e1b6",
      "item_count": 8,
      "latest_item_time": "2026-04-23T07:39:32+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_name": "Monica_IM(@hey_im_monica)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4d2d4165a7524217a08d3f57f27fa190",
      "item_count": 8,
      "latest_item_time": "2026-05-04T04:34:32+00:00",
      "sampled_item_count": 6,
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
      "sampled_item_count": 6,
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
      "sampled_item_count": 1,
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
    "en_or_unknown": 292,
    "zh": 8
  },
  "source_count": 75,
  "time_range": {
    "max_created_at": "2026-05-17T07:02:23.344838+00:00",
    "min_created_at": "2026-05-17T07:02:23.148409+00:00"
  },
  "top_sources": [
    [
      "socialmedia-weaviate-vector-database-weaviate-io",
      9
    ],
    [
      "socialmedia-simon-willison-simonw",
      9
    ],
    [
      "socialmedia-the-rundown-ai-therundownai",
      9
    ],
    [
      "socialmedia-y-combinator-ycombinator",
      9
    ],
    [
      "socialmedia-windsurf-windsurf-ai",
      8
    ],
    [
      "socialmedia-yann-lecun-ylecun",
      8
    ],
    [
      "socialmedia-taranjeet-taranjeetio",
      8
    ],
    [
      "socialmedia-thomas-wolf-thom-wolf",
      8
    ],
    [
      "socialmedia-xai-xai",
      8
    ],
    [
      "socialmedia-sundar-pichai-sundarpichai",
      8
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.681,
  "avg_confidence_by_tier": {
    "full": 0.77,
    "minimal": 0.55,
    "standard": 0.726
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 4991.0
  },
  "card_tier_distribution": {
    "full": 96,
    "minimal": 101,
    "standard": 103
  },
  "content_role_distribution": {
    "aggregator": 6,
    "analysis": 32,
    "commentary": 34,
    "firsthand": 9,
    "low_signal": 21,
    "report": 119,
    "source_material": 79
  },
  "entity_count_distribution": {
    "0": 3,
    "1": 16,
    "2": 43,
    "3": 66,
    "4": 52,
    "5": 51,
    "6": 32,
    "7": 13,
    "8": 12,
    "9": 4,
    "10": 2,
    "11": 2,
    "14": 1,
    "15": 1,
    "18": 1,
    "20": 1
  },
  "heuristic_card_fallback_count": 20,
  "item_cards_failed": 6,
  "item_cards_generated": 300,
  "item_cards_generated_or_reused": 300,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {
    "mixed_llm": 6
  },
  "samples": [
    {
      "item_id": "item_003d2eaa8ba04ab3a4fcd32aab9ee3c8",
      "role": "low_signal",
      "summary": "Qdrant is live at AI Dev Conference and invites attendees to their booth.",
      "title": "Qdrant at AI Dev Conference"
    },
    {
      "item_id": "item_0059e3c0096a4734bab44deff0f1904e",
      "role": "commentary",
      "summary": "Y Combinator promotes AI-Native Discovery Engines, claiming frontier models have reached PhD-level performance on scientific reasoning.",
      "title": "AI-Native Discovery Engines by xuster"
    },
    {
      "item_id": "item_0134b94779ae43a480af0a14c9777eb4",
      "role": "source_material",
      "summary": "Alibaba's HappyHorse-1.0, a 15B-parameter model, tops ArtificialAnlys Video Arena, offering 1080p text-to-video and image-to-video with audio and lip-sync.",
      "title": "HappyHorse-1.0 from Alibaba is here."
    },
    {
      "item_id": "item_0155f5daf6cc49bc9ca0cc9687cdcdbc",
      "role": "report",
      "summary": "Forward and backward benchmark results across common configurations. 💬 3 🔄 3 ❤️ 91 👀 11414 📊 13 ⚡ Powered by xgo.ing",
      "title": "Forward and backward benchmark results across common configurations."
    },
    {
      "item_id": "item_01e7975085184a6a9457bc5fc50991e0",
      "role": "commentary",
      "summary": "Richard Socher expressed wish for more pro-AI content from Hollywood, noting current anti-AI and anti-progress vibes, and quoted a post about a Chinese romance cdrama that promotes entrepreneurship in solar power and brain-computer interfaces.",
      "title": "Richard Socher comments on Hollywood's anti-AI stance and Chinese drama promoting tech entrepreneurship"
    },
    {
      "item_id": "item_02d478778ae54b649c8161c66ad91801",
      "role": "report",
      "summary": "Voice Cloning is now live via the xAI API! Create a custom voice in less than 2 minutes or select from our library of 80+ voices across 28 languages to personalize your voice agents, audiobooks, video game characters, and more. x.ai/news/grok-cust… Your browser does not support the video tag. 🔗 View on Twitter 💬 649 🔄 2092 ❤️ 17971 👀 99859503 📊 3378 ⚡ Power…",
      "title": "Voice Cloning is now live via the xAI API! Create a custom voice in less than 2 minutes or select f..."
    },
    {
      "item_id": "item_04cb93e1faa94fa493642c2ca4199cbb",
      "role": "source_material",
      "summary": "LovartAI announces winners of a contest and introduces a new Font Generator feature.",
      "title": "Congrats to our 10 lucky winners! one- month Pro membership are yours—don’t forget to check your DMs within the next 24 hours!"
    },
    {
      "item_id": "item_05435c40dfca4d3c8c921dade9a35629",
      "role": "commentary",
      "summary": "Gemini can generate documents like Docs, Sheets, PDF, CSV, Word, Excel, LaTeX, txt, etc. and integrate tables and diagrams.",
      "title": "Wow Gemini is basically your own cloud computer now 🔥"
    },
    {
      "item_id": "item_056c1b8a17124cefb9f55f5d27385dd0",
      "role": "report",
      "summary": "We've been building something that doesn't fit in a wave. Coming soon 💬 52 🔄 20 ❤️ 455 👀 62188 📊 116 ⚡ Powered by xgo.ing",
      "title": "We've been building something that doesn't fit in a wave. Coming soon"
    },
    {
      "item_id": "item_05c7ccd62d0a4b3093f8b51175475340",
      "role": "source_material",
      "summary": "Runway announces Runway Characters, allowing one image to become a fully expressive conversational video agent streaming at 24fps HD with 1.75 seconds end-to-end latency.",
      "title": "Runway Characters: Real-time video agents"
    }
  ],
  "warnings_distribution": {
    "Promotional content": 1,
    "aggregator_content": 2,
    "apology": 1,
    "claims_from_announcement": 1,
    "claims_not_independently_verified": 1,
    "contains opinion": 1,
    "content is a third-party quote of official announcement": 1,
    "emotional content": 1,
    "heuristic_card": 20,
    "job_posting": 1,
    "legal_promotion": 1,
    "likely_opinion": 1,
    "limited_information": 1,
    "links_only": 1,
    "low_signal": 3,
    "marketing": 4,
    "marketing_content": 1,
    "minimal_card": 101,
    "mixed_language": 1,
    "no_description": 1,
    "no_tech": 1,
    "only links, no details": 1,
    "only prompts, no substantive information": 1,
    "opinion": 2,
    "opinion piece": 1,
    "opinion_claims": 1,
    "opinion_heavy": 1,
    "opinion_only": 2,
    "opinion_piece": 1,
    "opinionated": 1,
    "performance claims not independently verified": 1,
    "personal opinion": 1,
    "personal reflection": 1,
    "personal_opinion": 1,
    "possible_marketing": 1,
    "promotional": 8,
    "promotional_content": 2,
    "prompts_only": 1,
    "results claimed but not independently verified": 1,
    "social_media_source": 1,
    "social_media_statement": 1,
    "speculative": 1,
    "speculative_claims": 1,
    "subjective": 1,
    "subjective_analysis": 1,
    "summary_only": 7,
    "thin_content": 1,
    "third-party analysis": 1,
    "third_party_announcement": 1,
    "too_general": 1,
    "too_short": 1,
    "unverifiable claim": 1,
    "unverified": 1,
    "unverified claims about internal policies": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.824,
  "candidate_pairs_considered": 331,
  "candidate_priority_distribution": {
    "high": 2447,
    "low": 10,
    "medium": 1265,
    "must_run": 1469,
    "suppress": 30
  },
  "candidates_suppressed_without_llm": 30,
  "cluster_eligible_count": 3,
  "different": 328,
  "duplicate": 0,
  "duplicate_direction_suppressed_count": 417,
  "event_relation_type_distribution": {
    "different": 31,
    "same_account_boilerplate": 46,
    "same_event": 3,
    "same_product_different_event": 1,
    "same_topic_only": 250
  },
  "examples": [
    {
      "candidate_item_title": "We are so excited to welcome Pierre to our team today! 🎉 Pierre Demagny is joining us from France ...",
      "confidence": 0.95,
      "new_item_title": "Hear from our team:",
      "primary_relation": "different",
      "published_at": "2026-04-28T14:06:46+00:00",
      "reason": "No shared entities or events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-mistral-ai-mistralai"
    },
    {
      "candidate_item_title": "Q1 earnings are in: 2026 is off to a terrific start. Our AI investments and full stack approach are...",
      "confidence": 0.95,
      "new_item_title": "Hear from our team:",
      "primary_relation": "different",
      "published_at": "2026-04-28T14:06:46+00:00",
      "reason": "No shared entities or events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-mistral-ai-mistralai"
    },
    {
      "candidate_item_title": "Create with GPT Image 2 in Skywork. Claim your gift from Skywork by RT, Like, Quote, & Subscr...",
      "confidence": 0.95,
      "new_item_title": "Hear from our team:",
      "primary_relation": "different",
      "published_at": "2026-04-28T14:06:46+00:00",
      "reason": "No shared entities or events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-mistral-ai-mistralai"
    },
    {
      "candidate_item_title": "Microsoft Research is at #CHI2026 this week. The question driving our work this year isn't about AI ...",
      "confidence": 0.95,
      "new_item_title": "Hear from our team:",
      "primary_relation": "different",
      "published_at": "2026-04-28T14:06:46+00:00",
      "reason": "No shared entities or events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-mistral-ai-mistralai"
    },
    {
      "candidate_item_title": "Trump's war on science.",
      "confidence": 0.95,
      "new_item_title": "Hear from our team:",
      "primary_relation": "different",
      "published_at": "2026-04-28T14:06:46+00:00",
      "reason": "No shared entities or events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-mistral-ai-mistralai"
    },
    {
      "candidate_item_title": "Now it's time to really execute. Episode 2 is coming. Two builders, two wildly different bets. One ...",
      "confidence": 0.95,
      "new_item_title": "Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...",
      "primary_relation": "different",
      "published_at": "2026-05-02T16:41:11+00:00",
      "reason": "Different topics: OpenRouter cache vs Replit Race To Revenue.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openrouter-openrouterai"
    },
    {
      "candidate_item_title": "Now it's time to really execute. Episode 2 is here. Two builders, two wildly different bets. One bu...",
      "confidence": 0.95,
      "new_item_title": "Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...",
      "primary_relation": "different",
      "published_at": "2026-05-02T16:41:11+00:00",
      "reason": "Different topics: OpenRouter cache vs Replit Race To Revenue.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openrouter-openrouterai"
    },
    {
      "candidate_item_title": "I tried running the same \"Generate an SVG of a pelican riding a bicycle\" prompt against 21 different...",
      "confidence": 0.95,
      "new_item_title": "Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...",
      "primary_relation": "different",
      "published_at": "2026-05-02T16:41:11+00:00",
      "reason": "Different topics: OpenRouter cache vs IBM Granite SVG experiment.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openrouter-openrouterai"
    },
    {
      "candidate_item_title": "Several major models shipped in the last 48 hours. 𝗙𝗼𝗿 𝗥𝗔𝗚 𝗮𝗻𝗱 𝗮𝗴𝗲𝗻𝘁 𝗯𝘂𝗶𝗹𝗱𝗲𝗿𝘀,...",
      "confidence": 0.95,
      "new_item_title": "Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...",
      "primary_relation": "different",
      "published_at": "2026-05-02T16:41:11+00:00",
      "reason": "Different topics: OpenRouter cache vs model shipping updates.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openrouter-openrouterai"
    },
    {
      "candidate_item_title": "By the way, if you want to work with me but don't think the above role is the *perfect* fit, I'm als...",
      "confidence": 0.95,
      "new_item_title": "Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...",
      "primary_relation": "different",
      "published_at": "2026-05-02T16:41:11+00:00",
      "reason": "Different topics: OpenRouter cache vs job hiring post.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openrouter-openrouterai"
    }
  ],
  "fold_candidates": 1,
  "high_priority_skips": 384,
  "llm_item_relation_calls": 78,
  "low_confidence_examples": [
    {
      "candidate_item_title": "Read the full tech blog here: https://t.co/hSl2GIbniT Free developer credits applied to the first 5...",
      "confidence": 0.55,
      "new_item_title": "Free Agent Day + Buildathon Office Hours https://t.co/RRGvOkNpZY",
      "primary_relation": "different",
      "published_at": "2026-05-02T22:03:08+00:00",
      "reason": "Different event: tech blog with developer credits vs. Free Agent Day broadcast.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-replit-replit"
    },
    {
      "candidate_item_title": "Source via Meta: https://t.co/l22aISUzys I break down stories like this every day in my free newsle...",
      "confidence": 0.55,
      "new_item_title": "Free Agent Day + Buildathon Office Hours https://t.co/RRGvOkNpZY",
      "primary_relation": "different",
      "published_at": "2026-05-02T22:03:08+00:00",
      "reason": "Different event: Meta source with newsletter boilerplate vs. Free Agent Day broadcast.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-replit-replit"
    },
    {
      "candidate_item_title": "Research paper link: https://t.co/XPbDNPcU6m I break down stories like this every day in my free ne...",
      "confidence": 0.55,
      "new_item_title": "Free Agent Day + Buildathon Office Hours https://t.co/RRGvOkNpZY",
      "primary_relation": "different",
      "published_at": "2026-05-02T22:03:08+00:00",
      "reason": "Different event: research paper link with newsletter boilerplate vs. Free Agent Day broadcast.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-replit-replit"
    },
    {
      "candidate_item_title": "Dev Community Live: GTC Vibe Hack Winners – Building Impactful Agents https://t.co/QzaGyw45i9",
      "confidence": 0.55,
      "new_item_title": "Free Agent Day + Buildathon Office Hours https://t.co/RRGvOkNpZY",
      "primary_relation": "different",
      "published_at": "2026-05-02T22:03:08+00:00",
      "reason": "Different event: GTC Vibe Hack Winners vs. Free Agent Day broadcast.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-replit-replit"
    },
    {
      "candidate_item_title": "Try it now for free: https://t.co/y7IZARLPZ5",
      "confidence": 0.55,
      "new_item_title": "Free Agent Day + Buildathon Office Hours https://t.co/RRGvOkNpZY",
      "primary_relation": "different",
      "published_at": "2026-05-02T22:03:08+00:00",
      "reason": "Different event: free trial offer vs. Free Agent Day broadcast.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-replit-replit"
    },
    {
      "candidate_item_title": "Perplexity Computer is now available in Microsoft Teams. Run research, analysis, and document creat...",
      "confidence": 0.1,
      "new_item_title": "Microsoft Research is at #CHI2026 this week. The question driving our work this year isn't about AI ...",
      "primary_relation": "different",
      "published_at": "2026-04-13T18:56:40+00:00",
      "reason": "Perplexity Computer in Teams is unrelated to Microsoft Research at CHI2026.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "Microsoft's AI can now detect cancer from a $10 tissue sample. For context, every time tumor cells ...",
      "confidence": 0.1,
      "new_item_title": "Microsoft Research is at #CHI2026 this week. The question driving our work this year isn't about AI ...",
      "primary_relation": "different",
      "published_at": "2026-04-13T18:56:40+00:00",
      "reason": "Microsoft AI cancer detection is a different event from Microsoft Research at CHI2026.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "2/ And with our Rubber Duck agent you get a multi-model reflection loop as a reviewer. GPT-5.5 can r...",
      "confidence": 0.0,
      "new_item_title": "Microsoft Research is at #CHI2026 this week. The question driving our work this year isn't about AI ...",
      "primary_relation": "different",
      "published_at": "2026-04-13T18:56:40+00:00",
      "reason": "Rubber Duck agent with GPT-5.5 is unrelated to Microsoft Research at CHI2026.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "This is a great report that provides a thoughtful, detailed and very well researched description of ...",
      "confidence": 0.0,
      "new_item_title": "Microsoft Research is at #CHI2026 this week. The question driving our work this year isn't about AI ...",
      "primary_relation": "different",
      "published_at": "2026-04-13T18:56:40+00:00",
      "reason": "International AI Safety Report 2026 is unrelated to Microsoft Research at CHI2026.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "Meet Skywork with Hermes Agent capabilities. An agent that evolves with you. Turn routine tasks i...",
      "confidence": 0.0,
      "new_item_title": "Microsoft Research is at #CHI2026 this week. The question driving our work this year isn't about AI ...",
      "primary_relation": "different",
      "published_at": "2026-04-13T18:56:40+00:00",
      "reason": "Skywork with Hermes Agent is unrelated to Microsoft Research at CHI2026.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    }
  ],
  "near_duplicate": 1,
  "raw_relation_count": 331,
  "related_with_new_info": 2,
  "related_with_new_info_count": 2,
  "relations_by_primary_relation": {
    "different": 328,
    "near_duplicate": 1,
    "related_with_new_info": 2
  },
  "uncertain_count": 0,
  "unique_relation_pair_count": 304
}
```

## 6. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 18
  },
  "attached_existing_clusters": 0,
  "avg_confidence": 0.6,
  "avg_items_per_cluster": 1.0,
  "candidate_clusters_considered": 18,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Hear from our team:",
      "core_facts": [
        "Hear from our team: Your browser does not support the video tag. 🔗 View on Twitter 💬 2 🔄 3 ❤️ 115 👀 31495 📊 17 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a9fd1ec464464fb184e2fee599df9d1e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "International AI Safety Report 2026 released",
      "core_facts": [
        "Geoffrey Hinton praises the International AI Safety Report 2026 by Yoshua Bengio, calling it essential reading on AI risks."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_6da46ee8d6a04be09585ec4c6a6e1de2"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Moonlake public launch",
      "core_facts": [
        "Moonlake launches publicly with $28M seed funding to build reasoning models that generate real-time simulations and games."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d1342a71ec784523917366e8e4e4f2f6"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Discussion on moltbook authenticity",
      "core_facts": [
        "Richard Socher suggests most salacious moltbook entries are human-made, citing a demonstration that anyone can post via HTTP POST."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_52916374f2a447a584df4b90d4066437"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Unstructured Data Meetup London talk on AI agents",
      "core_facts": [
        "Recap of Unstructured Data Meetup London with Jiang Chen (Zilliz) discussing building better agents, focusing on context, agent memory, and retrieval infrastructure."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_732fc3076c394c16b5c13f0c7c95ce4f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Recraft shares AI image generation prompts",
      "core_facts": [
        "Recraft posted a set of four image generation prompts for creating stylized portraits with specific text overlays and graphic stickers."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_aea4122dbca24d238960251514b51dc1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Vector Space Day 2026",
      "core_facts": [
        "Qdrant is hosting Vector Space Day 2026 in San Francisco on June 11. Call for proposals closes May 6. Early bird tickets available."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5e1cde906020498498157c51c52ed5e8"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Promotion of Fusion product",
      "core_facts": [
        "Try out Fusion if you want to get closer to the actual frontier: openrouter.ai/labs/fusion. Elad Gil: People at major AI labs 3-4 months ahead of startup SV engineers, etc."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3f4e751a607146f9a6ccd12f3ec6630b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Super proud of the work that went into this.",
      "core_facts": [
        "Mustafa Suleyman expresses pride in a MicrosoftAI project, noting implications for tool design."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_bf8659f7558b4c0a8a6a40808c1db903"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Kling AI Elite Creators Program recruitment",
      "core_facts": [
        "Kling AI's Elite Creators Program is still recruiting, offering Kling Pro plans and exclusive perks for growing creators."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c739a14bf7914136a49cbb2810c62cc4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Codex Chrome integration release",
      "core_facts": [
        "OpenAI announces Codex integration with Chrome on macOS and Windows, with parallel tab operation."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_290eb07820454f2681abe33e6f72e9d7"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "SAIL Postdoctoral Fellowships deadline",
      "core_facts": [
        "SAIL is accepting applications for Postdoctoral Fellowships until December 15."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c6607874ef124b44aac4b1d3814ca230"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mem0 reaches 100k developers milestone",
      "core_facts": [
        "Mem0 reaches 100,000 developers."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b8251fcd7b6f481980918dc294d42b6a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Personal festival recommendation",
      "core_facts": [
        "I LOVE and highly recommend the New Orleans Jazz and Heritage Festival because of the music, the food, and the vibe."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2ee357abcbc94ec69dfa67e662f9e8fc"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Debate on AI and labor market",
      "core_facts": [
        "Yann LeCun argues Dario is wrong about technological revolutions' effects on labor market, advises listening to economists like Aghion, Brynjolfsson, Acemoglu, McAfee, Autor."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b96bc3fd45fc4da8a044f27f108e3d74"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anthropic enterprise announcement",
      "core_facts": [
        "Anthropic made an enterprise announcement.",
        "The Wall Street Journal reported on the announcement."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_546dcd6e4fa6445a8f4c74865969dda9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anitgravity addresses malicious usage and service degradation",
      "core_facts": [
        "Anitgravity is shutting off access to users misusing their backend due to a massive increase in malicious usage that degraded service quality."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2cb02bff03ce48dba854961bd30bd5fa"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Trump fires all 24 members of the National Science Board",
      "core_facts": [
        "U.S. President Donald Trump fired all 24 members of the National Science Board.",
        "The National Science Board oversees the National Science Foundation."
      ],
      "item_count": 1,
      "known_angles": [
        "Science advocates view this as an attempt to erode or destroy the NSF."
      ],
      "representative_items": [
        "item_b95fde2797c04c35884720f281c5030a"
      ]
    }
  ],
  "created_clusters": 18,
  "follow_up_event": {
    "false": 18
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 0,
  "relations": {
    "new_info": 13,
    "source_material": 5
  },
  "same_event": {
    "true": 18
  },
  "same_topic": {
    "true": 18
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 18,
  "top_clusters": [
    {
      "cluster_id": "cluster_07181688a97e4867a13a0ab3393bf785",
      "cluster_title": "Hear from our team:",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_96567abe5af34848abdc5a9dc741df14",
      "cluster_title": "International AI Safety Report 2026 released",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_51f29a9c20bd4ec19c7e470af013968f",
      "cluster_title": "Moonlake public launch",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_c25a4ff8f7aa4d79a046503f881e32ff",
      "cluster_title": "Discussion on moltbook authenticity",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_934341c936b8447cbdbe83a459f25915",
      "cluster_title": "Unstructured Data Meetup London talk on AI agents",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_a1ad0e30964b44c4b3313cfd60ca3425",
      "cluster_title": "Recraft shares AI image generation prompts",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_d5bde243b04148f8b869c7ded719bc49",
      "cluster_title": "Vector Space Day 2026",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_97d50cff96d0402191ed335ccd54b0b3",
      "cluster_title": "Promotion of Fusion product",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b65a17f2d0d94a3caeb9f3c118eee845",
      "cluster_title": "Super proud of the work that went into this.",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_3bd0b0129a764e9eb8b25dc10465fb20",
      "cluster_title": "Kling AI Elite Creators Program recruitment",
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
    "cluster_title": "Hear from our team:",
    "core_facts": [
      "Hear from our team: Your browser does not support the video tag. 🔗 View on Twitter 💬 2 🔄 3 ❤️ 115 👀 31495 📊 17 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_a9fd1ec464464fb184e2fee599df9d1e"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "International AI Safety Report 2026 released",
    "core_facts": [
      "Geoffrey Hinton praises the International AI Safety Report 2026 by Yoshua Bengio, calling it essential reading on AI risks."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_6da46ee8d6a04be09585ec4c6a6e1de2"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Moonlake public launch",
    "core_facts": [
      "Moonlake launches publicly with $28M seed funding to build reasoning models that generate real-time simulations and games."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d1342a71ec784523917366e8e4e4f2f6"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Discussion on moltbook authenticity",
    "core_facts": [
      "Richard Socher suggests most salacious moltbook entries are human-made, citing a demonstration that anyone can post via HTTP POST."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_52916374f2a447a584df4b90d4066437"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Unstructured Data Meetup London talk on AI agents",
    "core_facts": [
      "Recap of Unstructured Data Meetup London with Jiang Chen (Zilliz) discussing building better agents, focusing on context, agent memory, and retrieval infrastructure."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_732fc3076c394c16b5c13f0c7c95ce4f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Recraft shares AI image generation prompts",
    "core_facts": [
      "Recraft posted a set of four image generation prompts for creating stylized portraits with specific text overlays and graphic stickers."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_aea4122dbca24d238960251514b51dc1"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Vector Space Day 2026",
    "core_facts": [
      "Qdrant is hosting Vector Space Day 2026 in San Francisco on June 11. Call for proposals closes May 6. Early bird tickets available."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_5e1cde906020498498157c51c52ed5e8"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Promotion of Fusion product",
    "core_facts": [
      "Try out Fusion if you want to get closer to the actual frontier: openrouter.ai/labs/fusion. Elad Gil: People at major AI labs 3-4 months ahead of startup SV engineers, etc."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_3f4e751a607146f9a6ccd12f3ec6630b"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Super proud of the work that went into this.",
    "core_facts": [
      "Mustafa Suleyman expresses pride in a MicrosoftAI project, noting implications for tool design."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_bf8659f7558b4c0a8a6a40808c1db903"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Kling AI Elite Creators Program recruitment",
    "core_facts": [
      "Kling AI's Elite Creators Program is still recruiting, offering Kling Pro plans and exclusive perks for growing creators."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c739a14bf7914136a49cbb2810c62cc4"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Codex Chrome integration release",
    "core_facts": [
      "OpenAI announces Codex integration with Chrome on macOS and Windows, with parallel tab operation."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_290eb07820454f2681abe33e6f72e9d7"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "SAIL Postdoctoral Fellowships deadline",
    "core_facts": [
      "SAIL is accepting applications for Postdoctoral Fellowships until December 15."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c6607874ef124b44aac4b1d3814ca230"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Mem0 reaches 100k developers milestone",
    "core_facts": [
      "Mem0 reaches 100,000 developers."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b8251fcd7b6f481980918dc294d42b6a"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Personal festival recommendation",
    "core_facts": [
      "I LOVE and highly recommend the New Orleans Jazz and Heritage Festival because of the music, the food, and the vibe."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2ee357abcbc94ec69dfa67e662f9e8fc"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Debate on AI and labor market",
    "core_facts": [
      "Yann LeCun argues Dario is wrong about technological revolutions' effects on labor market, advises listening to economists like Aghion, Brynjolfsson, Acemoglu, McAfee, Autor."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b96bc3fd45fc4da8a044f27f108e3d74"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Anthropic enterprise announcement",
    "core_facts": [
      "Anthropic made an enterprise announcement.",
      "The Wall Street Journal reported on the announcement."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_546dcd6e4fa6445a8f4c74865969dda9"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Anitgravity addresses malicious usage and service degradation",
    "core_facts": [
      "Anitgravity is shutting off access to users misusing their backend due to a massive increase in malicious usage that degraded service quality."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2cb02bff03ce48dba854961bd30bd5fa"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Trump fires all 24 members of the National Science Board",
    "core_facts": [
      "U.S. President Donald Trump fired all 24 members of the National Science Board.",
      "The National Science Board oversees the National Science Foundation."
    ],
    "item_count": 1,
    "known_angles": [
      "Science advocates view this as an attempt to erode or destroy the NSF."
    ],
    "representative_items": [
      "item_b95fde2797c04c35884720f281c5030a"
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
    "socialmedia-justin-welsh-thejustinwelsh": 7319,
    "socialmedia-justine-moore-venturetwins": 6101,
    "socialmedia-logan-kilpatrick-officiallogank": 11687,
    "socialmedia-microsoft-research-msftresearch": 9299,
    "socialmedia-nick-st-pierre-nickfloats": 24486,
    "socialmedia-nvidia-ai-nvidiaai": 17951,
    "socialmedia-openai-developers-openaidevs": 6093,
    "socialmedia-openai-openai": 14781,
    "socialmedia-openrouter-openrouterai": 11971,
    "socialmedia-paul-graham-paulg": 16098,
    "socialmedia-pika-pika-labs": 11857,
    "socialmedia-qdrant-qdrant-engine": 11266,
    "socialmedia-qwen-alibaba-qwen": 8257,
    "socialmedia-replit-replit": 12034,
    "socialmedia-richard-socher-richardsocher": 6841,
    "socialmedia-rowan-cheung-rowancheung": 22027,
    "socialmedia-runway-runwayml": 19196,
    "socialmedia-sahil-lavingia-shl": 10711,
    "socialmedia-sam-altman-sama": 20605,
    "socialmedia-satya-nadella-satyanadella": 16900,
    "socialmedia-scott-wu-scottwu46": 25148,
    "socialmedia-simon-willison-simonw": 22077,
    "socialmedia-skywork-skywork-ai": 9797,
    "socialmedia-sualeh-asif-sualehasif996": 8411,
    "socialmedia-sundar-pichai-sundarpichai": 15824,
    "socialmedia-taranjeet-taranjeetio": 12684,
    "socialmedia-the-rundown-ai-therundownai": 21459,
    "socialmedia-v0-v0": 7570,
    "socialmedia-varun-mohan-mohansolo": 8475,
    "socialmedia-windsurf-windsurf-ai": 12218
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 514,
  "reviews_suppressed_due_to_insufficient_data": 75,
  "sources_recomputed": 75,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-jeff-dean-jeffdean",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5724,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-junyang-lin-justinlin610",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 7319,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6101,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justine-moore-venturetwins",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-latent-space-latentspacepod",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-lenny-rachitsky-lennysan",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-lex-fridman-lexfridman",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5949,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-lilian-weng-lilianweng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-llamaindex-129433-llama-index",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2392,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 11687,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-logan-kilpatrick-officiallogank",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "total_items": 3,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3576,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-manusai-manusai-hq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-marc-andreessen-127482-127480-pmarca",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-mem0-mem0ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-jeff-dean-jeffdean",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5724,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-junyang-lin-justinlin610",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 7319,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6101,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justine-moore-venturetwins",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-latent-space-latentspacepod",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-milvus-milvusio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5879,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 14781,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 11971,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 11266,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 14781,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 11266,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4932,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-stanford-ai-lab-stanfordailab",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 6,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 8475,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-varun-mohan-mohansolo",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 6,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-milvus-milvusio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5879,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-milvus-milvusio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5879,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 14781,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 11971,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 11266,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    },
    {
      "created_at": "2026-05-17T07:28:30.408139+00:00",
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
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T07:28:30.408139+00:00"
    }
  ]
}
```

## 9. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 23796.3,
    "cache_hit_tokens": 54400,
    "cache_miss_tokens": 0,
    "calls": 53,
    "failed": 6,
    "input_tokens": 141479,
    "llm_call_count": 53,
    "operation_count": 74,
    "output_tokens": 123043,
    "p50_latency_ms": 25218,
    "p95_latency_ms": 34415,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 6,
    "skipped": 21,
    "success": 47,
    "task_type": "item_card",
    "total_tokens": 264522
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 15129.3,
    "cache_hit_tokens": 88192,
    "cache_miss_tokens": 0,
    "calls": 78,
    "failed": 11,
    "input_tokens": 146711,
    "llm_call_count": 78,
    "operation_count": 300,
    "output_tokens": 105722,
    "p50_latency_ms": 14646,
    "p95_latency_ms": 21785,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 11,
    "skipped": 222,
    "success": 67,
    "task_type": "item_relation",
    "total_tokens": 252433
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 6972.3,
    "cache_hit_tokens": 125696,
    "cache_miss_tokens": 0,
    "calls": 104,
    "failed": 1,
    "input_tokens": 161185,
    "llm_call_count": 104,
    "operation_count": 281,
    "output_tokens": 57609,
    "p50_latency_ms": 6408,
    "p95_latency_ms": 11077,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 1,
    "skipped": 177,
    "success": 103,
    "task_type": "item_cluster_relation",
    "total_tokens": 218794
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 11512.7,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3693,
    "llm_call_count": 3,
    "operation_count": 21,
    "output_tokens": 3234,
    "p50_latency_ms": 12810,
    "p95_latency_ms": 13581,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 18,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6927
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
  "actual_calls": 238,
  "actual_tokens": 742676,
  "avg_latency_ms": 13449.4,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 11512.7,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 12810,
      "p95_latency_ms": 13581,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6927
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
      "avg_latency_ms": 23796.3,
      "cache_hit_tokens": 54400,
      "calls": 53,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 6,
      "p50_latency_ms": 25218,
      "p95_latency_ms": 34415,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 6,
      "success": 47,
      "task_type": "item_card",
      "total_tokens": 264522
    },
    "item_cluster_relation": {
      "avg_latency_ms": 6972.3,
      "cache_hit_tokens": 125696,
      "calls": 104,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 1,
      "p50_latency_ms": 6408,
      "p95_latency_ms": 11077,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 1,
      "success": 103,
      "task_type": "item_cluster_relation",
      "total_tokens": 218794
    },
    "item_relation": {
      "avg_latency_ms": 15129.3,
      "cache_hit_tokens": 88192,
      "calls": 78,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 11,
      "p50_latency_ms": 14646,
      "p95_latency_ms": 21785,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 11,
      "success": 67,
      "task_type": "item_relation",
      "total_tokens": 252433
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
  "cache_hit_rate": 0.3633,
  "cache_hit_tokens": 269824,
  "calls_per_sec": 0.1518,
  "db_lock_errors": 0,
  "duration_seconds": 1567.949,
  "final_failures": 18,
  "max_concurrency": 5,
  "p50_latency_ms": 10980,
  "p95_latency_ms": 31582,
  "parse_failures": 2,
  "rate_limit_errors": 0,
  "repair_retry_count": 18,
  "tokens_per_sec": 473.66
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
      "consumed_tokens": 6927,
      "remaining_budget": 57073,
      "skipped": 18,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 240000,
      "calls": 53,
      "consumed_tokens": 264522,
      "remaining_budget": 0,
      "skipped": 21,
      "skipped_due_to_budget": 21
    },
    "item_cluster_relation": {
      "budget": 216000,
      "calls": 104,
      "consumed_tokens": 218794,
      "remaining_budget": 0,
      "skipped": 177,
      "skipped_due_to_budget": 177
    },
    "item_relation": {
      "budget": 240000,
      "calls": 78,
      "consumed_tokens": 252433,
      "remaining_budget": 0,
      "skipped": 222,
      "skipped_due_to_budget": 222
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
  "final_failures": 18,
  "llm_parse_failures": 0,
  "repair_retry_count": 18,
  "review_queue_entries_due_to_failure": 411,
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
  "cluster_signal_count": 18,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "18 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 15. Readiness Assessment

```json
{
  "cluster_signal_count": 18,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "18 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 16. Recommendations

- Add vector indexes for item_cards and cluster_cards before larger runs.
- Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.
- Collect more source_signals before trusting source_profile priority suggestions.
- Run a larger dry-run before any write-real-db semantic pass.
