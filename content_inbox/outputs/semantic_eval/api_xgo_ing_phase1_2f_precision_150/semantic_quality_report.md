# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 64,
  "actual_tokens": 228659,
  "batch_size": 5,
  "cache_hit_tokens": 75008,
  "cache_miss_tokens": 0,
  "concurrency": 5,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 414.886,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_8evuobzw.sqlite3",
  "finished_at": "2026-05-17T08:59:52.570024+00:00",
  "git_commit": "de6fff192ebb520fd1b8a814d744db46db24f6f4",
  "include_archived": false,
  "items_sampled": 150,
  "live": true,
  "max_calls": 260,
  "max_candidates": 5,
  "max_items": 150,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260517_085257_673166",
  "sample_mode": "event_hotspots",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "stage_budget_profile": "balanced",
  "stage_budgets": {
    "cluster_card_patch": 14000,
    "item_card": 80000,
    "item_cluster_relation": 50000,
    "item_relation": 50000,
    "source_profile": 6000
  },
  "started_at": "2026-05-17T08:52:57.673166+00:00",
  "strong_model": null,
  "token_budget": 200000,
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
      "sampled_item_count": 21,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 13,
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_name": "NVIDIA AI(@NVIDIAAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/74e542992cf7441390c708f5601071d4",
      "item_count": 11,
      "latest_item_time": "2026-05-12T23:47:03+00:00",
      "sampled_item_count": 6,
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
      "sampled_item_count": 3,
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_name": "Justin Welsh(@thejustinwelsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/db648e4d4eae4822aa0d34f0faef7ad2",
      "item_count": 10,
      "latest_item_time": "2026-04-30T06:49:02+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-openai-openai",
      "source_name": "OpenAI(@OpenAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/17687b1051204b2dbaed4ea4c9178f28",
      "item_count": 10,
      "latest_item_time": "2026-05-02T04:37:44+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-poe-poe-platform",
      "source_name": "Poe(@poe_platform)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4838204097ed422eac24ad48e68dc3ff",
      "item_count": 10,
      "latest_item_time": "2026-05-07T21:07:12+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_name": "Ray Dalio(@RayDalio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/12eba9c3db4940c5ab2a72bd00f9ff2c",
      "item_count": 10,
      "latest_item_time": "2026-04-30T14:02:05+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-replicate-replicate",
      "source_name": "Replicate(@replicate)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3953aa71e87a422eb9d7bf6ff1c7c43e",
      "item_count": 10,
      "latest_item_time": "2026-05-05T16:39:00+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_name": "AI Breakfast(@AiBreakfast)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7d19a619a1cc4a9896129211269d2c85",
      "item_count": 9,
      "latest_item_time": "2026-05-12T18:36:29+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_name": "AI Engineer(@aiDotEngineer)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/aa74321087f9405a872fd9a76b743bf8",
      "item_count": 9,
      "latest_item_time": "2026-05-15T08:22:59+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_name": "AI Will(@FinanceYF5)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/341f7b9f8d9b477e8bb200caa7f32c6e",
      "item_count": 9,
      "latest_item_time": "2026-05-13T12:46:05+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 3,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 3,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 3,
      "source_id": "socialmedia-greg-brockman-gdb",
      "source_name": "Greg Brockman(@gdb)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/831fac36aa0a49a9af79f35dc1c9b5d9",
      "item_count": 9,
      "latest_item_time": "2026-05-15T02:21:02+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_name": "Julien Chaumond(@julien_c)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c61046471f174d86bc0eb76cb44a21c3",
      "item_count": 9,
      "latest_item_time": "2026-05-12T15:17:41+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-lee-robinson-leerob",
      "source_name": "Lee Robinson(@leerob)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/77d5ce4736854b0ebae603e4b54d3095",
      "item_count": 9,
      "latest_item_time": "2026-05-12T15:41:09+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-manusai-manusai-hq",
      "source_name": "ManusAI(@ManusAI_HQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/94bb691baeff461686326af619beb116",
      "item_count": 9,
      "latest_item_time": "2026-05-01T23:08:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-mem0-mem0ai",
      "source_name": "mem0(@mem0ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/48aae530e0bf413aa7d44380f418e2e3",
      "item_count": 9,
      "latest_item_time": "2026-05-14T09:27:33+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_name": "meng shao(@shao__meng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/61f4b78554fb4b8fa5653ec5d924d15a",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:57:40+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_name": "Microsoft Research(@MSFTResearch)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/72dd496bfd9d44c5a5761a974630376d",
      "item_count": 9,
      "latest_item_time": "2026-04-30T22:04:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-midjourney-midjourney",
      "source_name": "Midjourney(@midjourney)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/424e67b19eed4500b7a440976bbd2ade",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:01+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-notion-notionhq",
      "source_name": "Notion(@NotionHQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6326c63a2dfa445bbde88bea0c3112c2",
      "item_count": 9,
      "latest_item_time": "2026-05-04T23:36:39+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_name": "OpenRouter(@OpenRouterAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c65c68f3713747bba863f92d6b5e996f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T18:12:41+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T20:47:13+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_name": "Philipp Schmid(@_philschmid)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3306d8b253ec4e03aca3c2e9967e7119",
      "item_count": 9,
      "latest_item_time": "2026-05-02T01:52:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-pika-pika-labs",
      "source_name": "Pika(@pika_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a55f6e33dd224235aabaabaaf9d58a06",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:00:02+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_name": "Qdrant(@qdrant_engine)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/80032d016d654eb4afe741ff34b7643d",
      "item_count": 9,
      "latest_item_time": "2026-05-01T15:14:01+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-replit-replit",
      "source_name": "Replit ⠕(@Replit)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a636de3cbda0495daabd15b9fd298614",
      "item_count": 9,
      "latest_item_time": "2026-05-04T15:18:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-rowan-cheung-rowancheung",
      "source_name": "Rowan Cheung(@rowancheung)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e6bb4f612dd24db5bc1a6811e6dd5820",
      "item_count": 9,
      "latest_item_time": "2026-05-05T14:22:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-runway-runwayml",
      "source_name": "Runway(@runwayml)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baad3713defe4182844d2756b4c2c9ed",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:41:48+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-sahil-lavingia-shl",
      "source_name": "Sahil Lavingia(@shl)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e30d4cd223f44bed9d404807105c8927",
      "item_count": 9,
      "latest_item_time": "2026-05-09T19:16:31+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-sam-altman-sama",
      "source_name": "Sam Altman(@sama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baa68dbd9a9e461a96fd9b2e3f35dcbf",
      "item_count": 9,
      "latest_item_time": "2026-05-02T12:11:51+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-satya-nadella-satyanadella",
      "source_name": "Satya Nadella(@satyanadella)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/30ad80be93c84e44acc37d5ddf31db57",
      "item_count": 9,
      "latest_item_time": "2026-05-07T17:13:19+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-sundar-pichai-sundarpichai",
      "source_name": "Sundar Pichai(@sundarpichai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/83b1ea38940b4a1d81ea57d1ffb12ad7",
      "item_count": 9,
      "latest_item_time": "2026-05-13T15:45:57+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-the-rundown-ai-therundownai",
      "source_name": "The Rundown AI(@TheRundownAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4918efb13c47459b8dcaa79cfdf72d09",
      "item_count": 9,
      "latest_item_time": "2026-04-29T19:01:30+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-thomas-wolf-thom-wolf",
      "source_name": "Thomas Wolf(@Thom_Wolf)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dbf37973e6fc4eae91d4be9669a78fc7",
      "item_count": 9,
      "latest_item_time": "2026-04-30T00:36:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-v0-v0",
      "source_name": "v0(@v0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7794c4268a504019a94af1778857a703",
      "item_count": 9,
      "latest_item_time": "2026-02-24T01:40:04+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-weaviate-vector-database-weaviate-io",
      "source_name": "Weaviate • vector database(@weaviate_io)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4a8273800ed34a069eecdb6c5c1b9ccf",
      "item_count": 9,
      "latest_item_time": "2026-04-30T17:14:35+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-windsurf-windsurf-ai",
      "source_name": "Windsurf(@windsurf_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b1ab109f6afd42ab8ea32e17a19a3a3e",
      "item_count": 9,
      "latest_item_time": "2026-05-14T15:50:00+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-y-combinator-ycombinator",
      "source_name": "Y Combinator(@ycombinator)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f5f4f928dede472ea55053672ad27ab6",
      "item_count": 9,
      "latest_item_time": "2026-05-04T16:44:38+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_name": "Cursor(@cursor_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ddfdcdd4e390495c942f0b5da62af0fb",
      "item_count": 8,
      "latest_item_time": "2026-05-05T02:41:21+00:00",
      "sampled_item_count": 1,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_name": "Mike Krieger(@mikeyk)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8d2d03aea8af49818096da4ea00409d1",
      "item_count": 8,
      "latest_item_time": "2026-04-30T23:06:24+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_name": "Mistral AI(@MistralAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5d749cc613ec4069bb2a47334739e1b6",
      "item_count": 8,
      "latest_item_time": "2026-04-23T07:39:32+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_name": "Monica_IM(@hey_im_monica)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4d2d4165a7524217a08d3f57f27fa190",
      "item_count": 8,
      "latest_item_time": "2026-05-04T04:34:32+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-richard-socher-richardsocher",
      "source_name": "Richard Socher(@RichardSocher)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fca8ccd87344d388bc863304ed6fd86",
      "item_count": 8,
      "latest_item_time": "2026-05-04T17:57:54+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-scott-wu-scottwu46",
      "source_name": "Scott Wu(@ScottWu46)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2de92402f4a24c90bb27e7580b93a878",
      "item_count": 8,
      "latest_item_time": "2026-04-24T21:21:51+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_name": "Taranjeet(@taranjeetio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fdd601ea751949e7bec9e4cdad7c8e6c",
      "item_count": 7,
      "latest_item_time": "2026-05-06T14:09:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-perplexity-perplexity-ai",
      "source_name": "Perplexity(@perplexity_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d5fc365556e641cba2278f501e8c6f92",
      "item_count": 7,
      "latest_item_time": "2026-04-23T07:26:58+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 4,
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
  "items_sampled": 150,
  "items_too_short": 0,
  "items_with_raw_content": 150,
  "items_with_summary_only": 0,
  "languages": {
    "en_or_unknown": 109,
    "zh": 41
  },
  "source_count": 51,
  "time_range": {
    "max_created_at": "2026-05-17T08:52:58.448501+00:00",
    "min_created_at": "2026-05-17T08:52:58.347814+00:00"
  },
  "top_sources": [
    [
      "socialmedia-orange-ai-oran-ge",
      21
    ],
    [
      "socialmedia-nvidia-ai-nvidiaai",
      13
    ],
    [
      "socialmedia-imxiaohu",
      6
    ],
    [
      "socialmedia-lenny-rachitsky-lennysan",
      4
    ],
    [
      "socialmedia-justine-moore-venturetwins",
      4
    ],
    [
      "socialmedia-the-rundown-ai-therundownai",
      4
    ],
    [
      "socialmedia-ak-akhaliq",
      4
    ],
    [
      "socialmedia-notion-notionhq",
      4
    ],
    [
      "socialmedia-gary-marcus-garymarcus",
      4
    ],
    [
      "socialmedia-y-combinator-ycombinator",
      4
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.674,
  "avg_confidence_by_tier": {
    "full": 0.796,
    "minimal": 0.55,
    "standard": 0.763
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 5333.2
  },
  "card_tier_distribution": {
    "full": 34,
    "minimal": 68,
    "standard": 48
  },
  "content_role_distribution": {
    "aggregator": 3,
    "analysis": 14,
    "commentary": 15,
    "firsthand": 8,
    "low_signal": 1,
    "report": 74,
    "source_material": 35
  },
  "entity_count_distribution": {
    "0": 1,
    "1": 5,
    "2": 20,
    "3": 31,
    "4": 23,
    "5": 23,
    "6": 13,
    "7": 13,
    "8": 17,
    "9": 2,
    "10": 1,
    "12": 1
  },
  "heuristic_card_fallback_count": 8,
  "item_cards_failed": 2,
  "item_cards_generated": 150,
  "item_cards_generated_or_reused": 150,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {
    "mixed_llm": 2
  },
  "samples": [
    {
      "item_id": "item_016f33e6e47947d296636585fc494f95",
      "role": "firsthand",
      "summary": "😂 绝了，上海电信直接把 Token 做成话费套餐了。 1块钱25万token，账单里直接就能扣。 手机厂商还在想怎么做 AI 入口，运营商先自己下场了。 甚至还说... \"Token服务是中国电信今后的经营主线。\" 具体方案： 1元 = 25万额度点 支持 30+ 主流大模型调用（文本、多模态） 话费账单直接付 上海电信用户免费领2500万额度点体验 💬 77 🔄 8 ❤️ 128 👀 63015 📊 91 ⚡ Powered by xgo.ing",
      "title": "😂 绝了，上海电信直接把 Token 做成话费套餐了。 1块钱25万token，账单里直接就能扣。 手机厂商还在想怎么做 AI 入口，运营商先自己下场了。 甚至还说... \"Token服务是中国电..."
    },
    {
      "item_id": "item_0170d51a0f87416783a2e489ea82e68f",
      "role": "report",
      "summary": "Try Unlimited with GPT Image 2.0➡️ lovart.ai 💬 1 🔄 0 ❤️ 18 👀 3629 📊 4 ⚡ Powered by xgo.ing",
      "title": "Try Unlimited with GPT Image 2.0➡️ https://t.co/uTOnzfs5gu"
    },
    {
      "item_id": "item_05eb86df60474345a05f4a18c5f18ccf",
      "role": "source_material",
      "summary": "GPT Image 2 is now available in Lovable, with before/after comparisons.",
      "title": "GPT Image 2 integrated into Lovable"
    },
    {
      "item_id": "item_0dbd3fc088ae4fda8c1c4014cfd8d317",
      "role": "source_material",
      "summary": "DeepSeek-V4 Preview is live & open-sourced, with 1M context. V4-Pro has 1.6T/49B params, V4-Flash 284B/13B params.",
      "title": "DeepSeek-V4 Preview officially live & open-sourced"
    },
    {
      "item_id": "item_0ebbf74c316544c2b9319b1a391b2403",
      "role": "report",
      "summary": "I write a short Saturday essay each week to help people build better lives. One story or lesson on rethinking how you work, earn, and live. 5 minutes. No marketing emails. Unsub anytime. Join 180,000+ here: justinwelsh.me/subscribe 💬 3 🔄 0 ❤️ 3 👀 5976 📊 3 ⚡ Powered by xgo.ing",
      "title": "I write a short Saturday essay each week to help people build better lives. One story or lesson on ..."
    },
    {
      "item_id": "item_106c2cedfe5a47ae86c6491166525b9d",
      "role": "report",
      "summary": "We've partnered with @OpenAI to offer GPT-5.5 in Windsurf at 50% off through May 14 starting today. Windsurf @windsurf GPT-5.5 is now available in Windsurf 2.0! 🔗 View Quoted Tweet 💬 23 🔄 37 ❤️ 593 👀 55600 📊 89 ⚡ Powered by xgo.ing",
      "title": "We've partnered with @OpenAI to offer GPT-5.5 in Windsurf at 50% off through May 14 starting today."
    },
    {
      "item_id": "item_127c0d1ede6e462a91f0a1083181e0cd",
      "role": "analysis",
      "summary": "LlamaIndex tested Opus 4.7 on ParseBench and found improvements in charts and formatting but regression in layout; compares with LlamaParse Agentic.",
      "title": "Anthropic says Opus 4.7 hits 80.6% on Document Reasoning — up from 57.1%. But \"reasoning about documents\" ≠ \"parsing documents for agents.\""
    },
    {
      "item_id": "item_13c7f74eaa2440fe82aef5884c91db16",
      "role": "report",
      "summary": "QVeris CLI integrates financial data and technical indicators into Claude Code.",
      "title": "金融分析的门槛正在被 AI 降低。 QVeris CLI 把 candles、RSI、布林带、公司基本面接进 Claude Code"
    },
    {
      "item_id": "item_165ecd4d023a4e099b7fc08257c33e46",
      "role": "commentary",
      "summary": "Author reflects on exploring various career paths including interning at a robotics startup, working on lunar space rovers, and building an autonomous AI researcher.",
      "title": "I spent a ton of time exploring everything from interning at a Robotics Startup to Lunar Space Rovers to building an Autonomous AI researcher"
    },
    {
      "item_id": "item_1b6f61289c0a40a2990358b2a2ec4db6",
      "role": "report",
      "summary": "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。 💬 2 🔄 2 ❤️ 10 👀 6278 📊 5 ⚡ Powered by xgo.ing",
      "title": "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。"
    }
  ],
  "warnings_distribution": {
    "aggregator": 1,
    "heuristic_card": 8,
    "marketing_generic": 1,
    "minimal_card": 68,
    "no_breaking_news": 1,
    "no_external_sources": 1,
    "opinion": 1,
    "opinion_based": 1,
    "opinion_heavy": 2,
    "opinion_laden": 1,
    "opinion_only": 1,
    "opinions_present": 1,
    "personal_opinion": 1,
    "promotional_content": 1,
    "promotional_tone": 1,
    "summary_of_report": 1,
    "summary_of_talk": 1,
    "summary_only": 3,
    "truncated_url": 1,
    "tweet_only": 1,
    "unverifiable_claim": 2,
    "unverified_claims": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.555,
  "candidate_pairs_considered": 77,
  "candidate_priority_distribution": {
    "low": 1995,
    "medium": 478,
    "must_run": 33,
    "suppress": 43
  },
  "candidates_suppressed_without_llm": 43,
  "cluster_eligible_count": 0,
  "different": 76,
  "duplicate": 0,
  "duplicate_direction_suppressed_count": 224,
  "event_relation_type_distribution": {
    "different": 70,
    "same_account_boilerplate": 6,
    "same_topic_only": 1
  },
  "examples": [
    {
      "candidate_item_title": "What if your team gave standup updates, and GPT-Realtime-2 moved the tickets?",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated topics: hiring call vs standup/ticket management.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "Marry well, stay in shape, build something you own, and protect your time.",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs life advice.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "在任意 Claude Code 会话里按左箭头，或者在终端运行： claude agents 就能打开 Agent View。每一行会显示一个会话、当前状态、最后回复内容、上次交互时间。",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs Claude Code feature announcement.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "I always tell visitors that Hobbs House Sherston is the best white bread they'll ever try. Now I've ...",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs bread award post.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs ColaOS promotional announcement.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "for now. when that changes, revenue may slow and the whole thing might fall apart.",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "My biggest takeaways from @EricRies: 1. There’s a force that pulls organizations toward mediocrity ...",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "Curious what people are running locally these days 👀",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "\"Only older people are buying the magic beans of AI.\" It's fascinating how people just make shit u...",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "\"Only older people are buying the magic beans of AI.\" The real data tells a different story - the ...",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    }
  ],
  "fold_candidates": 0,
  "high_priority_skips": 0,
  "llm_item_relation_calls": 19,
  "low_confidence_examples": [
    {
      "candidate_item_title": "What if your team gave standup updates, and GPT-Realtime-2 moved the tickets?",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated topics: hiring call vs standup/ticket management.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "Marry well, stay in shape, build something you own, and protect your time.",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs life advice.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "在任意 Claude Code 会话里按左箭头，或者在终端运行： claude agents 就能打开 Agent View。每一行会显示一个会话、当前状态、最后回复内容、上次交互时间。",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs Claude Code feature announcement.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "I always tell visitors that Hobbs House Sherston is the best white bread they'll ever try. Now I've ...",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs bread award post.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs ColaOS promotional announcement.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "Fork the repo and build your own voice-to-action workflow. https://t.co/G3ag8QeBl8",
      "confidence": 0.1,
      "new_item_title": "Grateful to our partners and the entire ecosystem for embracing OpenAI's mission, supporting this en...",
      "primary_relation": "different",
      "published_at": "2026-05-11T17:10:16+00:00",
      "reason": "Different topics: one is a voice-to-action workflow, the other is a generic thank you post.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-greg-brockman-gdb"
    },
    {
      "candidate_item_title": "Daybreak: our umbrella effort for defensive acceleration, equipping cyber defenders with the best po...",
      "confidence": 0.1,
      "new_item_title": "Grateful to our partners and the entire ecosystem for embracing OpenAI's mission, supporting this en...",
      "primary_relation": "different",
      "published_at": "2026-05-11T17:10:16+00:00",
      "reason": "Different initiatives: Daybreak cyber defense vs generic thank you.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-greg-brockman-gdb"
    },
    {
      "candidate_item_title": "Introducing the OpenAI Deployment Company, which will help businesses maximally succeed with their d...",
      "confidence": 0.3,
      "new_item_title": "Grateful to our partners and the entire ecosystem for embracing OpenAI's mission, supporting this en...",
      "primary_relation": "uncertain",
      "published_at": "2026-05-11T17:10:16+00:00",
      "reason": "Possible same event (Deployment Company) but new item is generic gratitude lacking specifics.",
      "secondary_roles": [
        "same_event_hint",
        "weak_context"
      ],
      "should_fold": false,
      "source": "socialmedia-greg-brockman-gdb"
    },
    {
      "candidate_item_title": "We've partnered with @OpenAI to offer GPT-5.5 in Windsurf at 50% off through May 14 starting today.",
      "confidence": 0.1,
      "new_item_title": "Grateful to our partners and the entire ecosystem for embracing OpenAI's mission, supporting this en...",
      "primary_relation": "different",
      "published_at": "2026-05-11T17:10:16+00:00",
      "reason": "Different: GPT-5.5 Windsurf deal vs generic thank you.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-greg-brockman-gdb"
    },
    {
      "candidate_item_title": "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 ...",
      "confidence": 0.1,
      "new_item_title": "Grateful to our partners and the entire ecosystem for embracing OpenAI's mission, supporting this en...",
      "primary_relation": "different",
      "published_at": "2026-05-11T17:10:16+00:00",
      "reason": "Different: adoption statistics vs generic thank you.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-greg-brockman-gdb"
    }
  ],
  "near_duplicate": 0,
  "raw_relation_count": 77,
  "related_with_new_info": 0,
  "related_with_new_info_count": 0,
  "relations_by_primary_relation": {
    "different": 76,
    "uncertain": 1
  },
  "uncertain_count": 1,
  "unique_relation_pair_count": 75
}
```

## 6. Event Signature Hotspots

```json
{
  "evidence_files": [
    "event_hotspots.jsonl",
    "event_hotspot_items.csv"
  ],
  "generic_token_policy": "generic AI/template tokens are supporting evidence only and cannot independently create high-priority hotspots",
  "sample_mode": "event_hotspots"
}
```

## 7. Candidate Priority Distribution

```json
{
  "candidate_priority_distribution": {
    "low": 1995,
    "medium": 478,
    "must_run": 33,
    "suppress": 43
  },
  "candidates_suppressed_without_llm": 43,
  "warning": "must_run/high should remain scarce; inspect candidate_generation.jsonl if inflated"
}
```

## 8. Relation Precision Review

```json
{
  "event_relation_type_distribution": {
    "different": 70,
    "same_account_boilerplate": 6,
    "same_topic_only": 1
  },
  "examples": [
    {
      "candidate_item_title": "What if your team gave standup updates, and GPT-Realtime-2 moved the tickets?",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated topics: hiring call vs standup/ticket management.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "Marry well, stay in shape, build something you own, and protect your time.",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs life advice.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "在任意 Claude Code 会话里按左箭头，或者在终端运行： claude agents 就能打开 Agent View。每一行会显示一个会话、当前状态、最后回复内容、上次交互时间。",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs Claude Code feature announcement.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "I always tell visitors that Hobbs House Sherston is the best white bread they'll ever try. Now I've ...",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs bread award post.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
      "confidence": 0.0,
      "new_item_title": "Mountain: identified. Time to climb. Looking for the early team: low level model optimization and p...",
      "primary_relation": "different",
      "published_at": "2026-05-11T15:05:32+00:00",
      "reason": "Unrelated: hiring call vs ColaOS promotional announcement.",
      "secondary_roles": [
        "generic_topic_overlap"
      ],
      "should_fold": false,
      "source": "socialmedia-suhail-suhail"
    },
    {
      "candidate_item_title": "for now. when that changes, revenue may slow and the whole thing might fall apart.",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "My biggest takeaways from @EricRies: 1. There’s a force that pulls organizations toward mediocrity ...",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "Curious what people are running locally these days 👀",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "\"Only older people are buying the magic beans of AI.\" It's fascinating how people just make shit u...",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    },
    {
      "candidate_item_title": "\"Only older people are buying the magic beans of AI.\" The real data tells a different story - the ...",
      "confidence": 0.95,
      "new_item_title": "The most successful people I know are annoyingly unaware of what everyone else is doing.",
      "primary_relation": "different",
      "published_at": "2026-05-11T13:07:05+00:00",
      "reason": "The new item and candidate discuss completely unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-justin-welsh-thejustinwelsh"
    }
  ],
  "near_duplicate": 0,
  "related_with_new_info": 0
}
```

## 9. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 11
  },
  "attached_existing_clusters": 0,
  "avg_confidence": 0.6,
  "avg_items_per_cluster": 1.0,
  "candidate_clusters_considered": 11,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Marry well, stay in shape, build something you own, and protect your time.",
      "core_facts": [
        "Marry well, stay in shape, build something you own, and protect your time. 💬 143 🔄 394 ❤️ 2920 👀 49589 📊 524 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ec66fa5b1702427cabec08b44164588e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Enterprise AI spending shift: Anthropic surpasses OpenAI",
      "core_facts": [
        "Anthropic surpassed OpenAI in share of U.S. businesses with paid AI subscriptions in April, per Ramp's AI Index."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_32baaf7e21464a8fb04ed59a6785c51c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Notion launches CLI for developers",
      "core_facts": [
        "Notion announces a new CLI for programmatic access, including sign-in, actions, Workers, and extensions."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_9d548b456ee443ffa26bc5f84123478b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Critique of METR time horizon graph",
      "core_facts": [
        "Gary Marcus suggests improvements to METR's time horizon graph, recommending lines for various accuracy criteria and clarifying that tasks are software engineering."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c551ba2c93b34702b3cfa32eb5c86463"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Code with Claude conference announced for spring 2026",
      "core_facts": [
        "Code with Claude developer conference returns this spring in San Francisco, London, and Tokyo. It includes workshops, demos, and 1:1 office hours. Registration for virtual and in-person available."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_931e65c5657c43baab35899f26c1fcc1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Cursor releases technical report on Composer 2 training",
      "core_facts": [
        "Cursor is releasing a technical report describing how Composer 2 was trained."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5dac52a4f59a4177b9a20fc966f2f190"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gemma-4 models ranked in Vision Arena",
      "core_facts": [
        "Gemma-4 lands in Vision Arena as #2 & #4 open models, and shifts the Pareto frontier! @GoogleDeepMind dominates the price-performance Pareto in Vision across both proprietary and open models. Gemma-4-31b ranks #2 open (#20 overall), Gemma-4-26b-a4b ranks #4 open (#26 overall)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_de39b611a75241a0bd3b1f5b18b8b3ef"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "李想与老罗播客讨论AI与一人公司",
      "core_facts": [
        "李想和老罗在播客中讨论AI与一人公司，李想认为AI是生产力和劳动力的技术，不太相信一人公司，建议企业不要裁员，用AI增效而非降本，并分享了关于具身智能、星际穿越等观点。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2c3a3d9d6da24ffbb957bd652c7fcef4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "田渊栋官宣新公司Recursive，获超6.5亿美元融资",
      "core_facts": [
        "田渊栋（前Meta FAIR Director）以联合创始人身份官宣新公司Recursive。",
        "公司全称Recursive Superintelligence，使命是构建递归自改进超智能。",
        "核心思路是AI自动写代码，闭合自改进环路。",
        "获超6.5亿美元融资（GV、Greycroft、NVIDIA、AMD领投），估值约46.5亿美元。",
        "创始人团队包括Richard Socher（CEO）等。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_99a1d87e87fa4322a2de5b04205c8b05"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Demonstration of AI game creation workflow",
      "core_facts": [
        "Eric Jing created open-world RPGs using GPT Image 2 and Seedance 2.0 via Genspark Claw, all from phone, no coding."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a65add9f1e244cb0b9904f2f30366de9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Release of DeepSeek-V4 Preview",
      "core_facts": [
        "DeepSeek announced the release of DeepSeek-V4 Preview, along with DeepSeek-V4-Pro and DeepSeek-V4-Flash."
      ],
      "item_count": 1,
      "known_angles": [
        "AI Breakfast analyzes DeepSeek's open-source strategy as a competitive move akin to 'Sun-Tzu shit'."
      ],
      "representative_items": [
        "item_6681aec5192b48fe95ffd5c4bb333852"
      ]
    }
  ],
  "created_clusters": 11,
  "follow_up_event": {
    "false": 11
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 0,
  "relations": {
    "new_info": 9,
    "source_material": 2
  },
  "same_event": {
    "true": 11
  },
  "same_topic": {
    "true": 11
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 11,
  "top_clusters": [
    {
      "cluster_id": "cluster_ae39fe294c074c779daf78b10e08f1df",
      "cluster_title": "Marry well, stay in shape, build something you own, and protect your time.",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_d2fbd1c97ec94604976fb2aeb4135508",
      "cluster_title": "Enterprise AI spending shift: Anthropic surpasses OpenAI",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_c85b0875a07e44638097e727660bbb85",
      "cluster_title": "Notion launches CLI for developers",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_6f7b0b2abc45438c9470aef253bfef95",
      "cluster_title": "Critique of METR time horizon graph",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_0da091611f0242808464dbf92f620de4",
      "cluster_title": "Code with Claude conference announced for spring 2026",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_95a1d9788e9a4078ac9aef4f053d95f8",
      "cluster_title": "Cursor releases technical report on Composer 2 training",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_43e4bae1174040daafca1cb4a17902f7",
      "cluster_title": "Gemma-4 models ranked in Vision Arena",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_e3faae8d2caf4ccfa09d13bc10f07775",
      "cluster_title": "李想与老罗播客讨论AI与一人公司",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b9e8f541e6754aafa1727122f7cf103e",
      "cluster_title": "田渊栋官宣新公司Recursive，获超6.5亿美元融资",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_c5f36478e2bd40fa9c1aa65c6afb4520",
      "cluster_title": "Demonstration of AI game creation workflow",
      "item_count": 1
    }
  ],
  "uncertain_clusters": 0
}
```

## 10. Cluster Seed Review

```json
{
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Marry well, stay in shape, build something you own, and protect your time.",
      "core_facts": [
        "Marry well, stay in shape, build something you own, and protect your time. 💬 143 🔄 394 ❤️ 2920 👀 49589 📊 524 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ec66fa5b1702427cabec08b44164588e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Enterprise AI spending shift: Anthropic surpasses OpenAI",
      "core_facts": [
        "Anthropic surpassed OpenAI in share of U.S. businesses with paid AI subscriptions in April, per Ramp's AI Index."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_32baaf7e21464a8fb04ed59a6785c51c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Notion launches CLI for developers",
      "core_facts": [
        "Notion announces a new CLI for programmatic access, including sign-in, actions, Workers, and extensions."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_9d548b456ee443ffa26bc5f84123478b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Critique of METR time horizon graph",
      "core_facts": [
        "Gary Marcus suggests improvements to METR's time horizon graph, recommending lines for various accuracy criteria and clarifying that tasks are software engineering."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c551ba2c93b34702b3cfa32eb5c86463"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Code with Claude conference announced for spring 2026",
      "core_facts": [
        "Code with Claude developer conference returns this spring in San Francisco, London, and Tokyo. It includes workshops, demos, and 1:1 office hours. Registration for virtual and in-person available."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_931e65c5657c43baab35899f26c1fcc1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Cursor releases technical report on Composer 2 training",
      "core_facts": [
        "Cursor is releasing a technical report describing how Composer 2 was trained."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5dac52a4f59a4177b9a20fc966f2f190"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gemma-4 models ranked in Vision Arena",
      "core_facts": [
        "Gemma-4 lands in Vision Arena as #2 & #4 open models, and shifts the Pareto frontier! @GoogleDeepMind dominates the price-performance Pareto in Vision across both proprietary and open models. Gemma-4-31b ranks #2 open (#20 overall), Gemma-4-26b-a4b ranks #4 open (#26 overall)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_de39b611a75241a0bd3b1f5b18b8b3ef"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "李想与老罗播客讨论AI与一人公司",
      "core_facts": [
        "李想和老罗在播客中讨论AI与一人公司，李想认为AI是生产力和劳动力的技术，不太相信一人公司，建议企业不要裁员，用AI增效而非降本，并分享了关于具身智能、星际穿越等观点。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2c3a3d9d6da24ffbb957bd652c7fcef4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "田渊栋官宣新公司Recursive，获超6.5亿美元融资",
      "core_facts": [
        "田渊栋（前Meta FAIR Director）以联合创始人身份官宣新公司Recursive。",
        "公司全称Recursive Superintelligence，使命是构建递归自改进超智能。",
        "核心思路是AI自动写代码，闭合自改进环路。",
        "获超6.5亿美元融资（GV、Greycroft、NVIDIA、AMD领投），估值约46.5亿美元。",
        "创始人团队包括Richard Socher（CEO）等。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_99a1d87e87fa4322a2de5b04205c8b05"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Demonstration of AI game creation workflow",
      "core_facts": [
        "Eric Jing created open-world RPGs using GPT Image 2 and Seedance 2.0 via Genspark Claw, all from phone, no coding."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a65add9f1e244cb0b9904f2f30366de9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Release of DeepSeek-V4 Preview",
      "core_facts": [
        "DeepSeek announced the release of DeepSeek-V4 Preview, along with DeepSeek-V4-Pro and DeepSeek-V4-Flash."
      ],
      "item_count": 1,
      "known_angles": [
        "AI Breakfast analyzes DeepSeek's open-source strategy as a competitive move akin to 'Sun-Tzu shit'."
      ],
      "representative_items": [
        "item_6681aec5192b48fe95ffd5c4bb333852"
      ]
    }
  ],
  "evidence_files": [
    "cluster_seed_candidates.jsonl",
    "cluster_seed_rejections.jsonl",
    "clusters_final.jsonl"
  ],
  "multi_item_cluster_count": 0
}
```

## 11. Budget Skip Quality

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "balanced",
  "stages": {
    "cluster_card_patch": {
      "budget": 14000,
      "calls": 3,
      "consumed_tokens": 7178,
      "remaining_budget": 6822,
      "skipped": 11,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 80000,
      "calls": 20,
      "consumed_tokens": 106665,
      "remaining_budget": 0,
      "skipped": 9,
      "skipped_due_to_budget": 9
    },
    "item_cluster_relation": {
      "budget": 50000,
      "calls": 22,
      "consumed_tokens": 50010,
      "remaining_budget": 0,
      "skipped": 117,
      "skipped_due_to_budget": 117
    },
    "item_relation": {
      "budget": 50000,
      "calls": 19,
      "consumed_tokens": 64806,
      "remaining_budget": 0,
      "skipped": 130,
      "skipped_due_to_budget": 130
    },
    "source_profile": {
      "budget": 6000,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 6000,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 200000
}
```

## 12. Cost / Yield

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 25605.1,
    "cache_hit_tokens": 20096,
    "cache_miss_tokens": 0,
    "calls": 20,
    "failed": 2,
    "input_tokens": 53226,
    "llm_call_count": 20,
    "operation_count": 29,
    "output_tokens": 53439,
    "p50_latency_ms": 27486,
    "p95_latency_ms": 35362,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 2,
    "skipped": 9,
    "success": 18,
    "task_type": "item_card",
    "total_tokens": 106665
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 13263.2,
    "cache_hit_tokens": 21120,
    "cache_miss_tokens": 0,
    "calls": 19,
    "failed": 2,
    "input_tokens": 40862,
    "llm_call_count": 19,
    "operation_count": 149,
    "output_tokens": 23944,
    "p50_latency_ms": 13143,
    "p95_latency_ms": 19925,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 2,
    "skipped": 130,
    "success": 17,
    "task_type": "item_relation",
    "total_tokens": 64806
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 5948.9,
    "cache_hit_tokens": 32256,
    "cache_miss_tokens": 0,
    "calls": 22,
    "failed": 0,
    "input_tokens": 38989,
    "llm_call_count": 22,
    "operation_count": 139,
    "output_tokens": 11021,
    "p50_latency_ms": 5549,
    "p95_latency_ms": 7548,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 117,
    "success": 22,
    "task_type": "item_cluster_relation",
    "total_tokens": 50010
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 10148.0,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 4353,
    "llm_call_count": 3,
    "operation_count": 14,
    "output_tokens": 2825,
    "p50_latency_ms": 10241,
    "p95_latency_ms": 12707,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 11,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 7178
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

## 13. Cluster Quality Samples

```json
[
  {
    "cluster_status": "active",
    "cluster_title": "Marry well, stay in shape, build something you own, and protect your time.",
    "core_facts": [
      "Marry well, stay in shape, build something you own, and protect your time. 💬 143 🔄 394 ❤️ 2920 👀 49589 📊 524 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ec66fa5b1702427cabec08b44164588e"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Enterprise AI spending shift: Anthropic surpasses OpenAI",
    "core_facts": [
      "Anthropic surpassed OpenAI in share of U.S. businesses with paid AI subscriptions in April, per Ramp's AI Index."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_32baaf7e21464a8fb04ed59a6785c51c"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Notion launches CLI for developers",
    "core_facts": [
      "Notion announces a new CLI for programmatic access, including sign-in, actions, Workers, and extensions."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_9d548b456ee443ffa26bc5f84123478b"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Critique of METR time horizon graph",
    "core_facts": [
      "Gary Marcus suggests improvements to METR's time horizon graph, recommending lines for various accuracy criteria and clarifying that tasks are software engineering."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c551ba2c93b34702b3cfa32eb5c86463"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Code with Claude conference announced for spring 2026",
    "core_facts": [
      "Code with Claude developer conference returns this spring in San Francisco, London, and Tokyo. It includes workshops, demos, and 1:1 office hours. Registration for virtual and in-person available."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_931e65c5657c43baab35899f26c1fcc1"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Cursor releases technical report on Composer 2 training",
    "core_facts": [
      "Cursor is releasing a technical report describing how Composer 2 was trained."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_5dac52a4f59a4177b9a20fc966f2f190"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Gemma-4 models ranked in Vision Arena",
    "core_facts": [
      "Gemma-4 lands in Vision Arena as #2 & #4 open models, and shifts the Pareto frontier! @GoogleDeepMind dominates the price-performance Pareto in Vision across both proprietary and open models. Gemma-4-31b ranks #2 open (#20 overall), Gemma-4-26b-a4b ranks #4 open (#26 overall)."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_de39b611a75241a0bd3b1f5b18b8b3ef"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "李想与老罗播客讨论AI与一人公司",
    "core_facts": [
      "李想和老罗在播客中讨论AI与一人公司，李想认为AI是生产力和劳动力的技术，不太相信一人公司，建议企业不要裁员，用AI增效而非降本，并分享了关于具身智能、星际穿越等观点。"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2c3a3d9d6da24ffbb957bd652c7fcef4"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "田渊栋官宣新公司Recursive，获超6.5亿美元融资",
    "core_facts": [
      "田渊栋（前Meta FAIR Director）以联合创始人身份官宣新公司Recursive。",
      "公司全称Recursive Superintelligence，使命是构建递归自改进超智能。",
      "核心思路是AI自动写代码，闭合自改进环路。",
      "获超6.5亿美元融资（GV、Greycroft、NVIDIA、AMD领投），估值约46.5亿美元。",
      "创始人团队包括Richard Socher（CEO）等。"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_99a1d87e87fa4322a2de5b04205c8b05"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Demonstration of AI game creation workflow",
    "core_facts": [
      "Eric Jing created open-world RPGs using GPT Image 2 and Seedance 2.0 via Genspark Claw, all from phone, no coding."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_a65add9f1e244cb0b9904f2f30366de9"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Release of DeepSeek-V4 Preview",
    "core_facts": [
      "DeepSeek announced the release of DeepSeek-V4 Preview, along with DeepSeek-V4-Pro and DeepSeek-V4-Flash."
    ],
    "item_count": 1,
    "known_angles": [
      "AI Breakfast analyzes DeepSeek's open-source strategy as a competitive move akin to 'Sun-Tzu shit'."
    ],
    "representative_items": [
      "item_6681aec5192b48fe95ffd5c4bb333852"
    ]
  }
]
```

## 14. Source Profile Results

```json
{
  "disabled_for_llm_candidates": [],
  "high_candidates": [],
  "llm_total_tokens_by_source": {
    "socialmedia-ai-breakfast-aibreakfast": 2144,
    "socialmedia-ai-engineer-aidotengineer": 6148,
    "socialmedia-ai-will-financeyf5": 0,
    "socialmedia-ak-akhaliq": 6400,
    "socialmedia-alex-albert-alexalbert": 0,
    "socialmedia-aman-sanger-amanrsanger": 0,
    "socialmedia-augment-code-augmentcode": 0,
    "socialmedia-cat-catwu": 0,
    "socialmedia-cognition-cognition-labs": 0,
    "socialmedia-cursor-cursor-ai": 0,
    "socialmedia-eric-jing-ericjing-ai": 2610,
    "socialmedia-gary-marcus-garymarcus": 0,
    "socialmedia-google-ai-googleai": 0,
    "socialmedia-greg-brockman-gdb": 6347,
    "socialmedia-guizang-ai-op7418": 0,
    "socialmedia-heygen-heygen-official": 0,
    "socialmedia-hugging-face-huggingface": 0,
    "socialmedia-imxiaohu": 6177,
    "socialmedia-justin-welsh-thejustinwelsh": 9032,
    "socialmedia-justine-moore-venturetwins": 6237,
    "socialmedia-lenny-rachitsky-lennysan": 19397,
    "socialmedia-meng-shao-shao-meng": 2424,
    "socialmedia-nvidia-ai-nvidiaai": 8863,
    "socialmedia-openai-developers-openaidevs": 8539,
    "socialmedia-orange-ai-oran-ge": 18964,
    "socialmedia-paul-graham-paulg": 11470,
    "socialmedia-replit-replit": 6118,
    "socialmedia-suhail-suhail": 6137,
    "socialmedia-the-rundown-ai-therundownai": 4218,
    "socialmedia-y-combinator-ycombinator": 2602
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 272,
  "reviews_suppressed_due_to_insufficient_data": 51,
  "sources_recomputed": 51,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2144,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6148,
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
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6400,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ak-akhaliq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cat-catwu",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2610,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-gary-marcus-garymarcus",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-google-ai-googleai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6347,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-greg-brockman-gdb",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-guizang-ai-op7418",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-heygen-heygen-official",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6177,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-imxiaohu",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-junyang-lin-justinlin610",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2144,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6148,
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
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6400,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ak-akhaliq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cat-catwu",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2144,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cat-catwu",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2610,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-gary-marcus-garymarcus",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9032,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2424,
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
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-notion-notionhq",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 18964,
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
      "total_items": 21,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-notion-notionhq",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2144,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cat-catwu",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2610,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-gary-marcus-garymarcus",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9032,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2424,
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
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 18964,
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
      "total_items": 21,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2144,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-cat-catwu",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2610,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-gary-marcus-garymarcus",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9032,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2424,
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
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
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
      "source_id": "socialmedia-notion-notionhq",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    },
    {
      "created_at": "2026-05-17T08:59:52.550899+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 18964,
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
      "total_items": 21,
      "updated_at": "2026-05-17T08:59:52.550899+00:00"
    }
  ]
}
```

## 15. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 25605.1,
    "cache_hit_tokens": 20096,
    "cache_miss_tokens": 0,
    "calls": 20,
    "failed": 2,
    "input_tokens": 53226,
    "llm_call_count": 20,
    "operation_count": 29,
    "output_tokens": 53439,
    "p50_latency_ms": 27486,
    "p95_latency_ms": 35362,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 2,
    "skipped": 9,
    "success": 18,
    "task_type": "item_card",
    "total_tokens": 106665
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 13263.2,
    "cache_hit_tokens": 21120,
    "cache_miss_tokens": 0,
    "calls": 19,
    "failed": 2,
    "input_tokens": 40862,
    "llm_call_count": 19,
    "operation_count": 149,
    "output_tokens": 23944,
    "p50_latency_ms": 13143,
    "p95_latency_ms": 19925,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 2,
    "skipped": 130,
    "success": 17,
    "task_type": "item_relation",
    "total_tokens": 64806
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 5948.9,
    "cache_hit_tokens": 32256,
    "cache_miss_tokens": 0,
    "calls": 22,
    "failed": 0,
    "input_tokens": 38989,
    "llm_call_count": 22,
    "operation_count": 139,
    "output_tokens": 11021,
    "p50_latency_ms": 5549,
    "p95_latency_ms": 7548,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 117,
    "success": 22,
    "task_type": "item_cluster_relation",
    "total_tokens": 50010
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 10148.0,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 4353,
    "llm_call_count": 3,
    "operation_count": 14,
    "output_tokens": 2825,
    "p50_latency_ms": 10241,
    "p95_latency_ms": 12707,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 11,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 7178
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

## 16. Concurrency Summary

```json
{
  "actual_calls": 64,
  "actual_tokens": 228659,
  "avg_latency_ms": 14459.7,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 10148.0,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 10241,
      "p95_latency_ms": 12707,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 7178
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
      "avg_latency_ms": 25605.1,
      "cache_hit_tokens": 20096,
      "calls": 20,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 2,
      "p50_latency_ms": 27486,
      "p95_latency_ms": 35362,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 2,
      "success": 18,
      "task_type": "item_card",
      "total_tokens": 106665
    },
    "item_cluster_relation": {
      "avg_latency_ms": 5948.9,
      "cache_hit_tokens": 32256,
      "calls": 22,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 5549,
      "p95_latency_ms": 7548,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 22,
      "task_type": "item_cluster_relation",
      "total_tokens": 50010
    },
    "item_relation": {
      "avg_latency_ms": 13263.2,
      "cache_hit_tokens": 21120,
      "calls": 19,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 2,
      "p50_latency_ms": 13143,
      "p95_latency_ms": 19925,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 2,
      "success": 17,
      "task_type": "item_relation",
      "total_tokens": 64806
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
  "cache_hit_rate": 0.328,
  "cache_hit_tokens": 75008,
  "calls_per_sec": 0.1543,
  "db_lock_errors": 0,
  "duration_seconds": 414.886,
  "final_failures": 4,
  "max_concurrency": 5,
  "p50_latency_ms": 12707,
  "p95_latency_ms": 32018,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 4,
  "tokens_per_sec": 551.14
}
```

## 17. Stage Budget Summary

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "balanced",
  "stages": {
    "cluster_card_patch": {
      "budget": 14000,
      "calls": 3,
      "consumed_tokens": 7178,
      "remaining_budget": 6822,
      "skipped": 11,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 80000,
      "calls": 20,
      "consumed_tokens": 106665,
      "remaining_budget": 0,
      "skipped": 9,
      "skipped_due_to_budget": 9
    },
    "item_cluster_relation": {
      "budget": 50000,
      "calls": 22,
      "consumed_tokens": 50010,
      "remaining_budget": 0,
      "skipped": 117,
      "skipped_due_to_budget": 117
    },
    "item_relation": {
      "budget": 50000,
      "calls": 19,
      "consumed_tokens": 64806,
      "remaining_budget": 0,
      "skipped": 130,
      "skipped_due_to_budget": 130
    },
    "source_profile": {
      "budget": 6000,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 6000,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 200000
}
```

## 18. Errors / Fallbacks / Retries

```json
{
  "db_lock_errors": 0,
  "failed_batch_count": 3,
  "fallback_rate": 0.0,
  "final_failures": 4,
  "heuristic_fallback_count": 0,
  "item_card_count": 150,
  "llm_card_count": 18,
  "llm_parse_failures": 0,
  "repair_retry_count": 4,
  "review_queue_entries_due_to_failure": 249,
  "single_retry_success_count": 4,
  "skipped_due_to_max_calls": false,
  "skipped_due_to_missing_card": 0,
  "skipped_due_to_no_candidate": 0,
  "skipped_due_to_token_budget": false,
  "split_retry_success_count": 0
}
```

## 19. Prompt Iteration Notes

```json
[
  {
    "changes": [
      "event-signature hotspot keys",
      "generic AI/template token suppression",
      "scarcer must_run/high candidate priorities",
      "same_product_different_event and same_thread secondary roles",
      "cluster seed precision diagnostics",
      "budget skip quality tiers",
      "item-card split retry metrics"
    ],
    "concurrency": 5,
    "iteration": "phase1_2f",
    "max_calls": 260,
    "max_items": 150,
    "notes": "Primary relation enums remain stable; prompt versions bumped to v3 with stricter same-event rules.",
    "sample_mode": "event_hotspots"
  }
]
```

## 20. Manual Review Suggestions

```json
{
  "high_uncertain": [],
  "possible_miscluster": [],
  "possible_missplit": [],
  "top_review_items_or_clusters": []
}
```

## 21. Readiness Assessment

```json
{
  "cluster_signal_count": 11,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "4 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 22. Recommendations

- Review uncertain relations and tune prompts with real examples.
- Add vector indexes for item_cards and cluster_cards before larger runs.
- Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.
- Collect more source_signals before trusting source_profile priority suggestions.
- Run a larger dry-run before any write-real-db semantic pass.
- Increase token_budget or lower max_items for more complete evaluation.

## 10. Concurrency Summary

```json
{
  "actual_calls": 64,
  "actual_tokens": 228659,
  "avg_latency_ms": 14459.7,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 10148.0,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 10241,
      "p95_latency_ms": 12707,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 7178
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
      "avg_latency_ms": 25605.1,
      "cache_hit_tokens": 20096,
      "calls": 20,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 2,
      "p50_latency_ms": 27486,
      "p95_latency_ms": 35362,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 2,
      "success": 18,
      "task_type": "item_card",
      "total_tokens": 106665
    },
    "item_cluster_relation": {
      "avg_latency_ms": 5948.9,
      "cache_hit_tokens": 32256,
      "calls": 22,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 5549,
      "p95_latency_ms": 7548,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 22,
      "task_type": "item_cluster_relation",
      "total_tokens": 50010
    },
    "item_relation": {
      "avg_latency_ms": 13263.2,
      "cache_hit_tokens": 21120,
      "calls": 19,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 2,
      "p50_latency_ms": 13143,
      "p95_latency_ms": 19925,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 2,
      "success": 17,
      "task_type": "item_relation",
      "total_tokens": 64806
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
  "cache_hit_rate": 0.328,
  "cache_hit_tokens": 75008,
  "calls_per_sec": 0.1543,
  "db_lock_errors": 0,
  "duration_seconds": 414.886,
  "final_failures": 4,
  "max_concurrency": 5,
  "p50_latency_ms": 12707,
  "p95_latency_ms": 32018,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 4,
  "tokens_per_sec": 551.14
}
```

## 14. Readiness Assessment

```json
{
  "cluster_signal_count": 11,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "4 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```
