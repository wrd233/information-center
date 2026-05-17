# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 223,
  "actual_tokens": 714640,
  "batch_size": 5,
  "cache_hit_tokens": 258560,
  "cache_miss_tokens": 0,
  "concurrency": 4,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 1232.673,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_xtw_uj8k.sqlite3",
  "finished_at": "2026-05-17T04:59:51.164577+00:00",
  "git_commit": "e7d51ad7bd188d0d986f52ec19a05ce2cbab9f41",
  "include_archived": false,
  "items_sampled": 300,
  "live": true,
  "max_calls": 500,
  "max_candidates": 5,
  "max_items": 300,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260517_043918_451646",
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
  "started_at": "2026-05-17T04:39:18.451646+00:00",
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
    "max_created_at": "2026-05-17T04:39:19.037464+00:00",
    "min_created_at": "2026-05-17T04:39:18.841322+00:00"
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
  "avg_confidence": 0.668,
  "avg_confidence_by_tier": {
    "full": 0.734,
    "minimal": 0.55,
    "standard": 0.715
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 5628.0
  },
  "card_tier_distribution": {
    "full": 99,
    "minimal": 96,
    "standard": 105
  },
  "content_role_distribution": {
    "aggregator": 7,
    "analysis": 25,
    "commentary": 26,
    "firsthand": 7,
    "low_signal": 21,
    "report": 129,
    "source_material": 85
  },
  "entity_count_distribution": {
    "0": 4,
    "1": 25,
    "2": 40,
    "3": 48,
    "4": 57,
    "5": 55,
    "6": 28,
    "7": 21,
    "8": 13,
    "9": 3,
    "10": 3,
    "11": 1,
    "12": 1,
    "16": 1
  },
  "heuristic_card_fallback_count": 35,
  "item_cards_failed": 7,
  "item_cards_generated": 300,
  "item_cards_generated_or_reused": 300,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {
    "unknown": 7
  },
  "samples": [
    {
      "item_id": "item_002d2254c8824601b74bc973e71cd884",
      "role": "firsthand",
      "summary": "Yann LeCun recounts the history of the tensor engine and naming conventions from SN3 (Lush) in 1992 to PyTorch.",
      "title": "History of tensor engine naming in deep learning libraries"
    },
    {
      "item_id": "item_032b1a3020024b1fa53fff9ceb5bbced",
      "role": "source_material",
      "summary": "Qwen announces strategic partnership with Fireworks AI to deliver optimized production-ready deployment of Qwen's closed weights models on the Fireworks Platform.",
      "title": "Qwen Partners with Fireworks AI to Accelerate Access to Qwen Family Models"
    },
    {
      "item_id": "item_032bb0dd80fe46a4961411cd78e46918",
      "role": "low_signal",
      "summary": "Gumroad (Gumclaw) is hiring design engineers for a trial period, with potential remote continuation.",
      "title": "Gumclaw hiring design engineers for trial period"
    },
    {
      "item_id": "item_035852b5af484a7987171b64d626fd6d",
      "role": "report",
      "summary": "You can read more about our results here: microsoft.com/en-us/Investor… 💬 17 🔄 9 ❤️ 156 👀 45401 📊 28 ⚡ Powered by xgo.ing",
      "title": "You can read more about our results here: https://t.co/En8ZukcLTN"
    },
    {
      "item_id": "item_037b630dac164eda9e9f0c6b3195b6a7",
      "role": "firsthand",
      "summary": "Mike Krieger announced he is joining Anthropic's Labs team to build products, praising Opus 4.5 and Claude Code, while Ami Vora leads the product team scaling Claude.",
      "title": "Mike Krieger joins Anthropic Labs"
    },
    {
      "item_id": "item_03f02d3c452f464484fe228c45f5eefe",
      "role": "report",
      "summary": "Meta plans to use space-based solar power for data centers via Overview Energy's 1000 satellites.",
      "title": "Meta planning to power AI data centers with solar energy from space"
    },
    {
      "item_id": "item_05dc673d8c4b4422ad90cfd685eaa507",
      "role": "report",
      "summary": "New Redis data type just dropped - arrays, accessible by index, with a new text grep search mechanism antirez @antirez [blog post] Redis array: short story of a long development process => https://t.co/Q5paOZH2Vz 🔗 View Quoted Tweet 💬 10 🔄 18 ❤️ 211 👀 41904 📊 34 ⚡ Powered by xgo.ing",
      "title": "New Redis data type just dropped - arrays, accessible by index, with a new text grep search mechanis..."
    },
    {
      "item_id": "item_05e1fb0a12b14d6d9e9eb494e4cbb801",
      "role": "report",
      "summary": "Want to speak at Vector Space Day 2026? We're hosting our second full-day in-person event in San Francisco on June 11, and we're looking for engineers, researchers, and builders working on: - Search & AI Retrieval - Agents & Memory - Edge & Robotics AI The call for proposals closes May 6. Submit yours: forms.gle/SQ4phv4bPH1yDX… Already know you want to atte…",
      "title": "Want to speak at Vector Space Day 2026? We're hosting our second full-day in-person event in San Fr..."
    },
    {
      "item_id": "item_067aa89d5fd443968984d104f6eb7a3c",
      "role": "report",
      "summary": "Northwestern researchers built modular robot legs that each operate as fully independent machines, capable of various gaits learned in simulation.",
      "title": "This robot can be torn apart and still keeps moving. Northwestern researchers built modular robot l..."
    },
    {
      "item_id": "item_087c4e17cd8a46e182a2ad3a53218061",
      "role": "report",
      "summary": "We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image generation but also transforms the entire design process with increased quality. Your browser does not support the video tag. 🔗 View on Twitter 💬 23 🔄 23 ❤️ 518 👀 51279 📊 124 ⚡ Powered by xgo.ing",
      "title": "We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image..."
    }
  ],
  "warnings_distribution": {
    "advertisement": 1,
    "aggregator": 1,
    "aggregator_list": 1,
    "claims from unofficial source": 2,
    "claims frontier-level intelligence": 1,
    "commentary_on_announcement": 1,
    "contains product promotion": 1,
    "contains_opinion_in_quoted_tweet": 1,
    "duplicate_content": 1,
    "early preview": 1,
    "emojis_and_engagement_metrics": 1,
    "general_philosophy": 1,
    "heuristic_card": 35,
    "historical claims": 1,
    "limited_context": 2,
    "low_signal": 2,
    "low_signal_event_promotion": 1,
    "marketing": 2,
    "marketing content": 1,
    "marketing_content": 2,
    "marketing_promotion": 3,
    "marketing_tone": 1,
    "minimal_card": 96,
    "model not named": 1,
    "no_news": 1,
    "no_verifiable_facts": 1,
    "only_links": 1,
    "opinion": 1,
    "opinion_dominant": 1,
    "opinion_included": 2,
    "opinion_only": 5,
    "opinion_piece": 4,
    "personal anecdote": 1,
    "promotional": 4,
    "promotional content": 1,
    "promotional_content": 6,
    "promotional_tone": 1,
    "prompts_only": 1,
    "recruitment": 1,
    "recruitment_post": 1,
    "retweet_content": 1,
    "similar_to_item_e36ed39b9d6248af99c2a9bcc123e893": 1,
    "social_media_claim": 1,
    "social_media_short": 2,
    "social_media_source": 1,
    "speculative": 1,
    "summary of external blog": 1,
    "summary of third-party report": 1,
    "summary_only": 4,
    "technical_supposition": 1,
    "too_short": 1,
    "truncated_urls": 1,
    "tweet": 1,
    "tweet_aggregator": 2,
    "tweet_promotion": 1,
    "unconfirmed_details": 1,
    "undesirable behaviors mentioned": 1,
    "user_claim_not_official": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.876,
  "candidate_pairs_considered": 484,
  "different": 453,
  "duplicate": 0,
  "examples": [
    {
      "candidate_item_title": "I tried running the same \"Generate an SVG of a pelican riding a bicycle\" prompt against 21 different...",
      "confidence": 0.95,
      "new_item_title": "From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T17:30:29+00:00",
      "reason": "New item about character AI response time; candidate is about SVG generation with IBM Granite models. No shared entities or topic.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Read more: https://t.co/3YEhHmqg3g",
      "confidence": 0.95,
      "new_item_title": "From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T17:30:29+00:00",
      "reason": "New item about character AI response time; candidate is a tweet link about Meta buying something. No shared entities or topic.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Cache is scoped per API key, so different keys under the same account stay isolated. Cache hits don'...",
      "confidence": 0.95,
      "new_item_title": "From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T17:30:29+00:00",
      "reason": "New item about character AI response time; candidate is about API cache scoping. No shared entities or topic.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Work less, make more",
      "confidence": 0.95,
      "new_item_title": "From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T17:30:29+00:00",
      "reason": "New item about character AI response time; candidate is a generic motivational post. No shared entities or topic.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Build it. Break it. Fix it. From campaign trackers to financial planners, @CalStateEastBay students...",
      "confidence": 0.95,
      "new_item_title": "From when the user stops speaking to when the Character starts replying is just 1.75 seconds. Under ...",
      "primary_relation": "different",
      "published_at": "2026-05-04T17:30:29+00:00",
      "reason": "New item about character AI response time; candidate is about Codex challenge with students. No shared entities or topic.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Gemini 3.1 Pro is out and it’s a step function improvement across many domains. It’s rolling out to ...",
      "confidence": 0.9,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item discusses Opus 4.7 coding benchmarks; candidate is about Gemini 3.1 Pro release. No overlap in content.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "We're incrementally rolling out Nano Banana Pro to Antigravity. It's not only a step change in image...",
      "confidence": 0.9,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item is about Opus 4.7 coding benchmarks; candidate is about Nano Banana Pro image generation. Unrelated topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "Kimi K2.6 is now available in Windsurf! Available for free for the next 2 weeks for Pro, Teams, and...",
      "confidence": 0.9,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item discusses Opus 4.7 coding improvements; candidate is about Kimi K2.6 availability in Windsurf. No shared event or topic.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "DeepSeek v4 Pro还是可以的。 几轮对话，实现一个工具，用xbox手柄控制电脑应用和浏览器。 当遥控器，躺床上刷小说和看视频。",
      "confidence": 0.9,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item is about Opus 4.7 benchmarks; candidate is about DeepSeek v4 Pro usage example. Different products and contexts.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    },
    {
      "candidate_item_title": "v0 Auto picks the right model for your prompt, whether that's Mini for quick edits, Pro for most tas...",
      "confidence": 0.9,
      "new_item_title": "Tip 3: There is a big jump on coding tasks like - SWE-Bench Pro 64.3% - SWE-Bench Verified 87.6% -...",
      "primary_relation": "different",
      "published_at": "2026-04-16T15:31:39+00:00",
      "reason": "New item focuses on Opus 4.7 coding performance; candidate is about v0 Auto model selection. No overlap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-poe-poe-platform"
    }
  ],
  "fold_candidates": 7,
  "llm_item_relation_calls": 97,
  "low_confidence_examples": [
    {
      "candidate_item_title": "Really fun to try this app while in Sydney this week, which uses our tools to help fans deep dive in...",
      "confidence": 0.5,
      "new_item_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "primary_relation": "different",
      "published_at": "2026-05-04T16:57:40+00:00",
      "reason": "The new item is a summary of multiple AI topics (data leaks, cloud OS, AI use at work) while the candidate is a tweet about a fun cricket app in Sydney. No meaningful overlap.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "Introducing Windsurf 2.0. Manage all your agents from one place and delegate work to the cloud with...",
      "confidence": 0.5,
      "new_item_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "primary_relation": "different",
      "published_at": "2026-05-04T16:57:40+00:00",
      "reason": "The new item discusses AI agent data leaks and research, while the candidate announces Windsurf 2.0 for agent management. Different angles, not same event.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "Bring your workflow to Codex in just a few clicks. Import settings, plugins, agents, project config...",
      "confidence": 0.5,
      "new_item_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "primary_relation": "different",
      "published_at": "2026-05-04T16:57:40+00:00",
      "reason": "The new item is a research focus article, while the candidate is about importing workflow to Codex. No direct connection.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "https://t.co/iMifqBlNHZ",
      "confidence": 0.5,
      "new_item_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "primary_relation": "different",
      "published_at": "2026-05-04T16:57:40+00:00",
      "reason": "The candidate is a tweet about a Stripe link recreation, unrelated to the new item's topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "When debt levels reach extreme sizes relative to income, governments are left with a limited set of ...",
      "confidence": 0.5,
      "new_item_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "primary_relation": "different",
      "published_at": "2026-05-04T16:57:40+00:00",
      "reason": "The candidate is about government debt and monetary policy, totally unrelated to AI research topics in the new item.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-microsoft-research-msftresearch"
    },
    {
      "candidate_item_title": "kicking off a bunch of codex tasks, running around with my kid in the sunshine, and then coming back...",
      "confidence": 0.25,
      "new_item_title": "5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...",
      "primary_relation": "different",
      "published_at": "2026-05-09T19:16:31+00:00",
      "reason": "Topics are unrelated: new item is about a model named 5.5, candidate is about codex tasks.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-sam-altman-sama"
    },
    {
      "candidate_item_title": "what would you most like to see improve in our next model?",
      "confidence": 0.3,
      "new_item_title": "5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...",
      "primary_relation": "different",
      "published_at": "2026-05-09T19:16:31+00:00",
      "reason": "Candidate asks what to improve in next model, new item is a comment on model 5.5's name.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-sam-altman-sama"
    },
    {
      "candidate_item_title": "It's an unimpressive-sounding word, but one of the most powerful motivations is the motivation of th...",
      "confidence": 0.2,
      "new_item_title": "5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...",
      "primary_relation": "different",
      "published_at": "2026-05-09T19:16:31+00:00",
      "reason": "Candidate about hobbyist motivation, new item about model naming.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-sam-altman-sama"
    },
    {
      "candidate_item_title": "ok other than more goblins, i think this reasonably well matches what we are prioritizing!",
      "confidence": 0.2,
      "new_item_title": "5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...",
      "primary_relation": "different",
      "published_at": "2026-05-09T19:16:31+00:00",
      "reason": "Candidate about prioritizing goblins, new item about model 5.5.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-sam-altman-sama"
    },
    {
      "candidate_item_title": "v0 is heading to SXSW to build agents. Join us live to make your own and walk away production-ready...",
      "confidence": 0.2,
      "new_item_title": "5.5 is an autistic genius with very strange taste in naming shocking that we would make such a thin...",
      "primary_relation": "different",
      "published_at": "2026-05-09T19:16:31+00:00",
      "reason": "Candidate about v0 at SXSW, new item about model 5.5.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-sam-altman-sama"
    }
  ],
  "near_duplicate": 7,
  "related_with_new_info": 23,
  "related_with_new_info_count": 23,
  "relations_by_primary_relation": {
    "different": 453,
    "near_duplicate": 7,
    "related_with_new_info": 23,
    "uncertain": 1
  },
  "uncertain_count": 1
}
```

## 6. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 20
  },
  "attached_existing_clusters": 0,
  "avg_confidence": 0.6,
  "avg_items_per_cluster": 1.0,
  "candidate_clusters_considered": 20,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "core_facts": [
        "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new research on how to actually structure AI use at work. msft.it/6016vKxQm Your browser does not support the video tag. 🔗 View on Twitter 💬 7 🔄 13 ❤️ 50 👀 9018 📊 18 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2fd731e980504b92bcb3e87e7cc828ad"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Local LLM execution demo",
      "core_facts": [
        "NVIDIA AI posted about running a 121B model locally on DGX Spark, with Hermes agent autonomously running tests and reporting results."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3586ece7f7dd4d0ea65773c4f304d370"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
      "core_facts": [
        "Ray Dalio tweets about the conflict between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_20646704dff34c81be8f0574610f4612"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Notebooks integration with Gemini App launched",
      "core_facts": [
        "NotebookLM announces that notebooks are now available in the Gemini App for Free and Paid users on mobile, with expansion to more countries and free users planned."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_9ac7138b5a254e63a242469ef2e3b0b7"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mem0 and BasisSet 2026 AI Fellowship opening",
      "core_facts": [
        "Mem0 partners with BasisSet for 2026 AI Fellowship on agentic memory track; apply by May 1."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f452aeb604f1408b9cefb23d173ab32f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mike Krieger on AI & I podcast",
      "core_facts": [
        "Mike Krieger discusses building agent-native products with Dan Shipper on the AI & I podcast."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_9f15a4e890b248438ad2edf69e07f0c0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "The Book of Elon by Eric Jorgenson",
      "core_facts": [
        "Promotion of 'The Book of Elon' by Eric Jorgenson, a compilation of Elon Musk's ideas."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c4265f28396b4865bdeefbf7afd99dc8"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total /...",
      "core_facts": [
        "LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total / 17B active, ~15x larger!) on every major coding benchmark — including SWE-bench Verified (77.2 vs. 76.2), SWE-bench Pro (53.5 vs. 50.9), Terminal-Bench 2.0 (59.3 vs. 52.5), and SkillsBench (48.2 vs. 30.0). It also surpasses all peer-scale dense models by a w…"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_7e380ba74030420b8b1775d2ace0bb08"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Recraft shares image generation prompts for campaign style",
      "core_facts": [
        "Recraft posts 4 example prompts for generating images with specific styles and text overlays."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_13129eb757e54a268b774cbb0771d3e1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Qdrant attending AI Dev Conference",
      "core_facts": [
        "Qdrant is live at AI Dev Conference, inviting attendees to visit their booth."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d4b901574ed248ada87c4e4017af5407"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "𝗬𝗼𝘂𝗿 𝗖𝗹𝗮𝘂𝗱𝗲 𝗖𝗼𝗱𝗲 𝗺𝗶𝗴𝗵𝘁 𝗯𝗲 𝗾𝘂𝗶𝗲𝘁𝗹𝘆 𝘄𝗿𝗶𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝘄𝗿𝗼𝗻𝗴 ...",
      "core_facts": [
        "𝗬𝗼𝘂𝗿 𝗖𝗹𝗮𝘂𝗱𝗲 𝗖𝗼𝗱𝗲 𝗺𝗶𝗴𝗵𝘁 𝗯𝗲 𝗾𝘂𝗶𝗲𝘁𝗹𝘆 𝘄𝗿𝗶𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝘄𝗿𝗼𝗻𝗴 𝗠𝗶𝗹𝘃𝘂𝘀 𝗰𝗼𝗱𝗲. 𝗛𝗼𝘄𝗲𝘃𝗲𝗿, 𝘆𝗼𝘂 𝗰𝗮𝗻 𝗿𝗲𝗱𝘂𝗰𝗲 𝘁𝗵𝗶𝘀 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗠𝗶𝗹𝘃𝘂𝘀 𝗦𝗸𝗶𝗹𝗹. Claude Code writes the wrong code because it could be confidently hallucinating details. 𝗖𝗼𝗺𝗺𝗼𝗻 𝗳𝗮𝗶𝗹𝘂𝗿𝗲 𝗽𝗼𝗶𝗻𝘁𝘀: • Collection schema: wrong field type, missing analyzer config, or bad primary-key setup. • BM25 full-text search: missing Functio…"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a8d9bf92985a4204a3cb45c78687954a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anthropic announcement and WSJ scoop",
      "core_facts": [
        "The Rundown AI tweeted about an announcement from Anthropic and a WSJ scoop."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d6597d16facc4c20b1ecde20f7b5c8e5"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Critique of government Innovation Centers",
      "core_facts": [
        "You can't get the same effect from the Innovation Center set up by the provincial government. You have to fill out forms to get space there, it's locked at night, and you can't make holes in the walls. You might even have to deal with bureaucrats hired to help you."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_7249afecd6ea4714b0e9b396bb5e9ed7"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Gumroad hiring trial design engineers",
      "core_facts": [
        "Gumroad (Gumclaw) is hiring design engineers for a trial period, with potential remote continuation."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_032bb0dd80fe46a4961411cd78e46918"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "SAIL opens applications for Postdoctoral Fellowships",
      "core_facts": [
        "SAIL is accepting applications for SAIL Postdoctoral Fellowships; full consideration by December 15."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_a7f4d07c11ef490899325e77b1a6aa4d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Commentary on Hollywood AI sentiment and Chinese cdrama",
      "core_facts": [
        "Richard Socher comments on Hollywood's anti-AI sentiment and quotes Susan Zhang describing a Chinese cdrama about solar power and brain-computer interfaces."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_fa3d13b9305a4f7d8982798d0138354c"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "History of tensor engine naming conventions",
      "core_facts": [
        "Yann LeCun recounts the history of the tensor engine and naming conventions from SN3 (Lush) in 1992 to PyTorch."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_002d2254c8824601b74bc973e71cd884"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Technical deep dive on RLHF precision mismatch",
      "core_facts": [
        "Thomas Wolf and Amine Dirhoussi present a deep dive into a numerical precision issue in RLHF when training in FP32 and inference in BF16. They decompose the importance sampling ratio into policy change and precision gap, finding that the precision gap is structured and correlated with advantage, but disabling clipping resolves the issue."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f14ce30de1434ed5893a8a81e2da1fe0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Windsurf promotes GPT-5.5",
      "core_facts": [
        "Windsurf promotes GPT-5.5, claiming it is a giant leap for handling ambiguity and key for long-horizon tasks in parallel agents."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c9c4f9840a1b4c309a184fcecb5cb84f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Jeff Dean speaking at Startup School 2026",
      "core_facts": [
        "Y Combinator announced that Jeff Dean will speak at Startup School 2026."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_e36ed39b9d6248af99c2a9bcc123e893"
      ]
    }
  ],
  "created_clusters": 20,
  "follow_up_event": {
    "false": 20
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 0,
  "relations": {
    "new_info": 16,
    "source_material": 4
  },
  "same_event": {
    "true": 20
  },
  "same_topic": {
    "true": 20
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 20,
  "top_clusters": [
    {
      "cluster_id": "cluster_7430ff76808b41849266a67b099fb534",
      "cluster_title": "Research Focus: AI agents leaking enterprise data, a smarter OS for cloud deployment, and new resear...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_83e13d15d80e4907aa79a9177a635178",
      "cluster_title": "Local LLM execution demo",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_b44a8b8594fd44efac723c3a2c713d86",
      "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_7d964ed198bb461abd7852de0b7f92c5",
      "cluster_title": "Notebooks integration with Gemini App launched",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_ebc6e2a3647b4120be2e5cf8ec201a85",
      "cluster_title": "Mem0 and BasisSet 2026 AI Fellowship opening",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_9014394b4943427b826bda46ad3d1b89",
      "cluster_title": "Mike Krieger on AI & I podcast",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_37284eb10b6d4355a0f8a2527e615149",
      "cluster_title": "The Book of Elon by Eric Jorgenson",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_d4a02bf34c8c4384a639b14427d56178",
      "cluster_title": "LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total /...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_2967d761e77a48358861da77e13b9a74",
      "cluster_title": "Recraft shares image generation prompts for campaign style",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_c6a5a8c8a647465790596d7981ad6a41",
      "cluster_title": "Qdrant attending AI Dev Conference",
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
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2fd731e980504b92bcb3e87e7cc828ad"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Local LLM execution demo",
    "core_facts": [
      "NVIDIA AI posted about running a 121B model locally on DGX Spark, with Hermes agent autonomously running tests and reporting results."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_3586ece7f7dd4d0ea65773c4f304d370"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Ray Dalio on the battle between feelings and rational thinking",
    "core_facts": [
      "Ray Dalio tweets about the conflict between subconscious feelings (amygdala) and conscious rational thinking (prefrontal cortex)."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_20646704dff34c81be8f0574610f4612"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Notebooks integration with Gemini App launched",
    "core_facts": [
      "NotebookLM announces that notebooks are now available in the Gemini App for Free and Paid users on mobile, with expansion to more countries and free users planned."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_9ac7138b5a254e63a242469ef2e3b0b7"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Mem0 and BasisSet 2026 AI Fellowship opening",
    "core_facts": [
      "Mem0 partners with BasisSet for 2026 AI Fellowship on agentic memory track; apply by May 1."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f452aeb604f1408b9cefb23d173ab32f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Mike Krieger on AI & I podcast",
    "core_facts": [
      "Mike Krieger discusses building agent-native products with Dan Shipper on the AI & I podcast."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_9f15a4e890b248438ad2edf69e07f0c0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "The Book of Elon by Eric Jorgenson",
    "core_facts": [
      "Promotion of 'The Book of Elon' by Eric Jorgenson, a compilation of Elon Musk's ideas."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c4265f28396b4865bdeefbf7afd99dc8"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total /...",
    "core_facts": [
      "LM Performance：With only 27B parameters, Qwen3.6-27B outperforms the Qwen3.5-397B-A17B (397B total / 17B active, ~15x larger!) on every major coding benchmark — including SWE-bench Verified (77.2 vs. 76.2), SWE-bench Pro (53.5 vs. 50.9), Terminal-Bench 2.0 (59.3 vs. 52.5), and SkillsBench (48.2 vs. 30.0). It also surpasses all peer-scale dense models by a w…"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_7e380ba74030420b8b1775d2ace0bb08"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Recraft shares image generation prompts for campaign style",
    "core_facts": [
      "Recraft posts 4 example prompts for generating images with specific styles and text overlays."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_13129eb757e54a268b774cbb0771d3e1"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Qdrant attending AI Dev Conference",
    "core_facts": [
      "Qdrant is live at AI Dev Conference, inviting attendees to visit their booth."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d4b901574ed248ada87c4e4017af5407"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "𝗬𝗼𝘂𝗿 𝗖𝗹𝗮𝘂𝗱𝗲 𝗖𝗼𝗱𝗲 𝗺𝗶𝗴𝗵𝘁 𝗯𝗲 𝗾𝘂𝗶𝗲𝘁𝗹𝘆 𝘄𝗿𝗶𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝘄𝗿𝗼𝗻𝗴 ...",
    "core_facts": [
      "𝗬𝗼𝘂𝗿 𝗖𝗹𝗮𝘂𝗱𝗲 𝗖𝗼𝗱𝗲 𝗺𝗶𝗴𝗵𝘁 𝗯𝗲 𝗾𝘂𝗶𝗲𝘁𝗹𝘆 𝘄𝗿𝗶𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝘄𝗿𝗼𝗻𝗴 𝗠𝗶𝗹𝘃𝘂𝘀 𝗰𝗼𝗱𝗲. 𝗛𝗼𝘄𝗲𝘃𝗲𝗿, 𝘆𝗼𝘂 𝗰𝗮𝗻 𝗿𝗲𝗱𝘂𝗰𝗲 𝘁𝗵𝗶𝘀 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗠𝗶𝗹𝘃𝘂𝘀 𝗦𝗸𝗶𝗹𝗹. Claude Code writes the wrong code because it could be confidently hallucinating details. 𝗖𝗼𝗺𝗺𝗼𝗻 𝗳𝗮𝗶𝗹𝘂𝗿𝗲 𝗽𝗼𝗶𝗻𝘁𝘀: • Collection schema: wrong field type, missing analyzer config, or bad primary-key setup. • BM25 full-text search: missing Functio…"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_a8d9bf92985a4204a3cb45c78687954a"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Anthropic announcement and WSJ scoop",
    "core_facts": [
      "The Rundown AI tweeted about an announcement from Anthropic and a WSJ scoop."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d6597d16facc4c20b1ecde20f7b5c8e5"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Critique of government Innovation Centers",
    "core_facts": [
      "You can't get the same effect from the Innovation Center set up by the provincial government. You have to fill out forms to get space there, it's locked at night, and you can't make holes in the walls. You might even have to deal with bureaucrats hired to help you."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_7249afecd6ea4714b0e9b396bb5e9ed7"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Gumroad hiring trial design engineers",
    "core_facts": [
      "Gumroad (Gumclaw) is hiring design engineers for a trial period, with potential remote continuation."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_032bb0dd80fe46a4961411cd78e46918"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "SAIL opens applications for Postdoctoral Fellowships",
    "core_facts": [
      "SAIL is accepting applications for SAIL Postdoctoral Fellowships; full consideration by December 15."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_a7f4d07c11ef490899325e77b1a6aa4d"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Commentary on Hollywood AI sentiment and Chinese cdrama",
    "core_facts": [
      "Richard Socher comments on Hollywood's anti-AI sentiment and quotes Susan Zhang describing a Chinese cdrama about solar power and brain-computer interfaces."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_fa3d13b9305a4f7d8982798d0138354c"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "History of tensor engine naming conventions",
    "core_facts": [
      "Yann LeCun recounts the history of the tensor engine and naming conventions from SN3 (Lush) in 1992 to PyTorch."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_002d2254c8824601b74bc973e71cd884"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Technical deep dive on RLHF precision mismatch",
    "core_facts": [
      "Thomas Wolf and Amine Dirhoussi present a deep dive into a numerical precision issue in RLHF when training in FP32 and inference in BF16. They decompose the importance sampling ratio into policy change and precision gap, finding that the precision gap is structured and correlated with advantage, but disabling clipping resolves the issue."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f14ce30de1434ed5893a8a81e2da1fe0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Windsurf promotes GPT-5.5",
    "core_facts": [
      "Windsurf promotes GPT-5.5, claiming it is a giant leap for handling ambiguity and key for long-horizon tasks in parallel agents."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c9c4f9840a1b4c309a184fcecb5cb84f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Jeff Dean speaking at Startup School 2026",
    "core_facts": [
      "Y Combinator announced that Jeff Dean will speak at Startup School 2026."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_e36ed39b9d6248af99c2a9bcc123e893"
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
    "socialmedia-microsoft-research-msftresearch": 6336,
    "socialmedia-mike-krieger-mikeyk": 5545,
    "socialmedia-naval-naval": 10964,
    "socialmedia-nvidia-ai-nvidiaai": 5436,
    "socialmedia-orange-ai-oran-ge": 6061,
    "socialmedia-perplexity-perplexity-ai": 5704,
    "socialmedia-philipp-schmid-philschmid": 5665,
    "socialmedia-pika-pika-labs": 11485,
    "socialmedia-poe-poe-platform": 5501,
    "socialmedia-qdrant-qdrant-engine": 10823,
    "socialmedia-recraft-recraftai": 9104,
    "socialmedia-rowan-cheung-rowancheung": 14620,
    "socialmedia-runway-runwayml": 23404,
    "socialmedia-sahil-lavingia-shl": 14500,
    "socialmedia-sam-altman-sama": 40699,
    "socialmedia-satya-nadella-satyanadella": 27618,
    "socialmedia-scott-wu-scottwu46": 21896,
    "socialmedia-simon-willison-simonw": 32219,
    "socialmedia-skywork-skywork-ai": 26581,
    "socialmedia-stanford-ai-lab-stanfordailab": 5499,
    "socialmedia-sualeh-asif-sualehasif996": 10116,
    "socialmedia-suhail-suhail": 20918,
    "socialmedia-taranjeet-taranjeetio": 10817,
    "socialmedia-the-rundown-ai-therundownai": 21752,
    "socialmedia-thomas-wolf-thom-wolf": 7086,
    "socialmedia-v0-v0": 13009,
    "socialmedia-varun-mohan-mohansolo": 16209,
    "socialmedia-vista8": 16352,
    "socialmedia-windsurf-windsurf-ai": 28620,
    "socialmedia-xai-xai": 5535
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 475,
  "reviews_suppressed_due_to_insufficient_data": 57,
  "sources_recomputed": 57,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5032,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6336,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5545,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10964,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 3038,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5436,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5273,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5418,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4883,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6061,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5032,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6336,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5545,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.6666666666666666,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6336,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5545,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10964,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5436,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-paul-graham-paulg",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10823,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.2857142857142857,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 5499,
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
      "total_items": 7,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4352,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-y-combinator-ycombinator",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 9,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6336,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5545,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10964,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5436,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-paul-graham-paulg",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6336,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5545,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10964,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5436,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
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
      "source_id": "socialmedia-paul-graham-paulg",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 10823,
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
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    },
    {
      "created_at": "2026-05-17T04:59:51.121327+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.2857142857142857,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 7,
      "updated_at": "2026-05-17T04:59:51.121327+00:00"
    }
  ]
}
```

## 9. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 26646.7,
    "cache_hit_tokens": 50304,
    "cache_miss_tokens": 0,
    "calls": 41,
    "failed": 7,
    "input_tokens": 122428,
    "llm_call_count": 41,
    "operation_count": 41,
    "output_tokens": 108319,
    "p50_latency_ms": 27470,
    "p95_latency_ms": 34376,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 7,
    "skipped": 0,
    "success": 34,
    "task_type": "item_card",
    "total_tokens": 230747
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9502.6,
    "cache_hit_tokens": 73600,
    "cache_miss_tokens": 0,
    "calls": 97,
    "failed": 1,
    "input_tokens": 182023,
    "llm_call_count": 97,
    "operation_count": 296,
    "output_tokens": 102595,
    "p50_latency_ms": 8950,
    "p95_latency_ms": 14768,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 1,
    "skipped": 199,
    "success": 96,
    "task_type": "item_relation",
    "total_tokens": 284618
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 6040.3,
    "cache_hit_tokens": 133120,
    "cache_miss_tokens": 0,
    "calls": 82,
    "failed": 1,
    "input_tokens": 150369,
    "llm_call_count": 82,
    "operation_count": 274,
    "output_tokens": 43021,
    "p50_latency_ms": 5624,
    "p95_latency_ms": 9614,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 1,
    "skipped": 192,
    "success": 81,
    "task_type": "item_cluster_relation",
    "total_tokens": 193390
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 6987.7,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3793,
    "llm_call_count": 3,
    "operation_count": 23,
    "output_tokens": 2092,
    "p50_latency_ms": 7603,
    "p95_latency_ms": 8051,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 20,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 5885
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
  "actual_calls": 223,
  "actual_tokens": 714640,
  "avg_latency_ms": 11347.7,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 6987.7,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 4,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 7603,
      "p95_latency_ms": 8051,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 5885
    },
    "cluster_card_rebuild": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 4,
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
      "avg_latency_ms": 26646.7,
      "cache_hit_tokens": 50304,
      "calls": 41,
      "concurrency": 4,
      "db_lock_errors": 0,
      "failed": 7,
      "p50_latency_ms": 27470,
      "p95_latency_ms": 34376,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 7,
      "success": 34,
      "task_type": "item_card",
      "total_tokens": 230747
    },
    "item_cluster_relation": {
      "avg_latency_ms": 6040.3,
      "cache_hit_tokens": 133120,
      "calls": 82,
      "concurrency": 4,
      "db_lock_errors": 0,
      "failed": 1,
      "p50_latency_ms": 5624,
      "p95_latency_ms": 9614,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 1,
      "success": 81,
      "task_type": "item_cluster_relation",
      "total_tokens": 193390
    },
    "item_relation": {
      "avg_latency_ms": 9502.6,
      "cache_hit_tokens": 73600,
      "calls": 97,
      "concurrency": 4,
      "db_lock_errors": 0,
      "failed": 1,
      "p50_latency_ms": 8950,
      "p95_latency_ms": 14768,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 1,
      "success": 96,
      "task_type": "item_relation",
      "total_tokens": 284618
    },
    "json_repair": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 4,
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
      "concurrency": 4,
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
  "cache_hit_rate": 0.3618,
  "cache_hit_tokens": 258560,
  "calls_per_sec": 0.1809,
  "db_lock_errors": 0,
  "duration_seconds": 1232.673,
  "final_failures": 9,
  "max_concurrency": 4,
  "p50_latency_ms": 8263,
  "p95_latency_ms": 29632,
  "parse_failures": 1,
  "rate_limit_errors": 0,
  "repair_retry_count": 9,
  "tokens_per_sec": 579.75
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
      "consumed_tokens": 5885,
      "remaining_budget": 50115,
      "skipped": 20,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 256000,
      "calls": 41,
      "consumed_tokens": 230747,
      "remaining_budget": 25253,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_cluster_relation": {
      "budget": 192000,
      "calls": 82,
      "consumed_tokens": 193390,
      "remaining_budget": 0,
      "skipped": 192,
      "skipped_due_to_budget": 192
    },
    "item_relation": {
      "budget": 272000,
      "calls": 97,
      "consumed_tokens": 284618,
      "remaining_budget": 0,
      "skipped": 199,
      "skipped_due_to_budget": 199
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
  "final_failures": 9,
  "llm_parse_failures": 0,
  "repair_retry_count": 9,
  "review_queue_entries_due_to_failure": 393,
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
    "concurrency": 4,
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
  "cluster_signal_count": 20,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "9 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 15. Readiness Assessment

```json
{
  "cluster_signal_count": 20,
  "reasons": [
    "Use dry-run reports for manual review before write-real-db.",
    "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    "9 LLM failures observed in this run."
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
