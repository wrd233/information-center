# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 173,
  "actual_tokens": 675294,
  "backup_path": null,
  "batch_size": 5,
  "cache_hit_tokens": 204032,
  "cache_miss_tokens": 0,
  "concurrency": 5,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 1252.876,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_skz1hexa.sqlite3",
  "finished_at": "2026-05-18T01:19:54.129110+00:00",
  "git_commit": "63bdcb566fdce47999298b50b48e93160f781bfd",
  "include_archived": false,
  "items_sampled": 300,
  "live": true,
  "max_calls": 650,
  "max_candidates": 8,
  "max_items": 300,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260518_005901_239042",
  "sample_mode": "event_hotspots",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "stage_budget_profile": "phase1_3_advisory",
  "stage_budgets": {
    "cluster_card_patch": 53200,
    "item_card": 258400,
    "item_cluster_relation": 190000,
    "item_relation": 235600,
    "source_profile": 22800
  },
  "started_at": "2026-05-18T00:59:01.239042+00:00",
  "strong_model": null,
  "token_budget": 760000,
  "vector_index": false,
  "warnings": [],
  "write_confirmation": null,
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
      "sampled_item_count": 22,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 20,
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_name": "NVIDIA AI(@NVIDIAAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/74e542992cf7441390c708f5601071d4",
      "item_count": 11,
      "latest_item_time": "2026-05-12T23:47:03+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 5,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_name": "ElevenLabs(@elevenlabsio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/931d6e88e067496cac6bf23f69d60f33",
      "item_count": 10,
      "latest_item_time": "2026-05-10T16:39:05+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_name": "Guillermo Rauch(@rauchg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/58894bf2934a426ca833c682da2bc810",
      "item_count": 10,
      "latest_item_time": "2026-05-11T17:00:14+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 2,
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_name": "AI Breakfast(@AiBreakfast)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7d19a619a1cc4a9896129211269d2c85",
      "item_count": 9,
      "latest_item_time": "2026-05-12T18:36:29+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 7,
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
      "sampled_item_count": 5,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-fellou-fellouai",
      "source_name": "Fellou(@FellouAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c04abb206bbf4f91b22795024d6c0614",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:11:06+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-firecrawl-firecrawl-dev",
      "source_name": "Firecrawl(@firecrawl_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/9f35c76341554bd78c2b9e63dc4fa5d8",
      "item_count": 9,
      "latest_item_time": "2026-05-06T23:42:49+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 5,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 5,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-hailuo-ai-minimax-hailuo-ai",
      "source_name": "Hailuo AI (MiniMax)(@Hailuo_AI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f299207df53745bca04a03db8d11c5aa",
      "item_count": 9,
      "latest_item_time": "2026-05-06T16:31:58+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-harrison-chase-hwchase17",
      "source_name": "Harrison Chase(@hwchase17)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a9aff6b016c143ed8728dd86eb70d7db",
      "item_count": 9,
      "latest_item_time": "2026-05-11T16:14:16+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 5,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-justine-moore-venturetwins",
      "source_name": "Justine Moore(@venturetwins)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/564237c3de274d58a04f064920817888",
      "item_count": 9,
      "latest_item_time": "2026-05-11T09:31:09+00:00",
      "sampled_item_count": 5,
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
      "sampled_item_count": 3,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-lovable-lovable-dev",
      "source_name": "Lovable(@lovable_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/320181c4651a41a08015946b55f704ab",
      "item_count": 9,
      "latest_item_time": "2026-05-06T15:01:44+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 5,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 5,
      "source_id": "socialmedia-openai-developers-openaidevs",
      "source_name": "OpenAI Developers(@OpenAIDevs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e503a90c035c4b1d8f8dd34907d15bf4",
      "item_count": 9,
      "latest_item_time": "2026-05-10T18:53:21+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_name": "OpenRouter(@OpenRouterAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c65c68f3713747bba863f92d6b5e996f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T18:12:41+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T20:47:13+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-recraft-recraftai",
      "source_name": "Recraft(@recraftai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/613f859e4bc440c5a28f40732840f5cf",
      "item_count": 9,
      "latest_item_time": "2026-05-11T17:34:29+00:00",
      "sampled_item_count": 4,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 4,
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
      "sampled_item_count": 4,
      "source_id": "socialmedia-simon-willison-simonw",
      "source_name": "Simon Willison(@simonw)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6d7d398dd80b48d79669c92745d32cf6",
      "item_count": 9,
      "latest_item_time": "2026-05-06T12:03:54+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-skywork-skywork-ai",
      "source_name": "Skywork(@Skywork_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fafa6df3c67644b1a367a177240e0173",
      "item_count": 9,
      "latest_item_time": "2026-04-21T22:41:39+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_name": "Aman Sanger(@amanrsanger)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fb1814c610c4af2911caa98c5c5ef82",
      "item_count": 8,
      "latest_item_time": "2026-05-05T21:08:54+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_name": "Amjad Masad(@amasad)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a3eb6beb2d894da3a9b7ab6d2e46790e",
      "item_count": 8,
      "latest_item_time": "2026-05-07T18:02:57+00:00",
      "sampled_item_count": 3,
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
      "sampled_item_count": 3,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 1,
      "source_id": "socialmedia-dotey",
      "source_name": "宝玉(@dotey)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5dbd038a8f5140938d0877511571797b",
      "item_count": 4,
      "latest_item_time": "2026-05-08T14:47:57+00:00",
      "sampled_item_count": 4,
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
  "items_sampled": 300,
  "items_too_short": 0,
  "items_with_raw_content": 300,
  "items_with_summary_only": 0,
  "languages": {
    "en_or_unknown": 253,
    "zh": 47
  },
  "source_count": 76,
  "time_range": {
    "max_created_at": "2026-05-18T00:59:03.336507+00:00",
    "min_created_at": "2026-05-18T00:59:03.131148+00:00"
  },
  "top_sources": [
    [
      "socialmedia-orange-ai-oran-ge",
      22
    ],
    [
      "socialmedia-nvidia-ai-nvidiaai",
      20
    ],
    [
      "socialmedia-browser-use-browser-use",
      7
    ],
    [
      "socialmedia-meng-shao-shao-meng",
      5
    ],
    [
      "socialmedia-jerry-liu-jerryjliu0",
      5
    ],
    [
      "socialmedia-kling-ai-kling-ai",
      5
    ],
    [
      "socialmedia-gary-marcus-garymarcus",
      5
    ],
    [
      "socialmedia-openrouter-openrouterai",
      5
    ],
    [
      "socialmedia-aadit-sheth-aaditsh",
      5
    ],
    [
      "socialmedia-cognition-cognition-labs",
      5
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.679,
  "avg_confidence_by_tier": {
    "full": 0.793,
    "minimal": 0.55,
    "standard": 0.729
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 4752.6
  },
  "budget_skip_fallback_count": 0,
  "card_tier_distribution": {
    "full": 58,
    "minimal": 104,
    "standard": 138
  },
  "content_role_distribution": {
    "aggregator": 4,
    "analysis": 26,
    "commentary": 40,
    "firsthand": 27,
    "low_signal": 16,
    "report": 113,
    "source_material": 74
  },
  "deterministic_minimal_card_count": 104,
  "entity_count_distribution": {
    "0": 5,
    "1": 20,
    "2": 45,
    "3": 66,
    "4": 48,
    "5": 49,
    "6": 27,
    "7": 19,
    "8": 13,
    "9": 3,
    "12": 2,
    "14": 1,
    "15": 1,
    "16": 1
  },
  "heuristic_card_fallback_count": 0,
  "item_cards_failed": 4,
  "item_cards_generated": 300,
  "item_cards_generated_or_reused": 300,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {
    "mixed_llm": 4
  },
  "parse_error_fallback_count": 0,
  "samples": [
    {
      "item_id": "item_003e1a8fae024e74b1aa30b08a8e8c52",
      "role": "source_material",
      "summary": "Cursor introduces always-on agents that monitor GitHub, investigate root causes, and open PRs with fixes.",
      "title": "Cursor can now automatically fix CI failures"
    },
    {
      "item_id": "item_01a5a431717d479caf6bf1f69dfd5e07",
      "role": "source_material",
      "summary": "Genspark announces new monthly show 'Genspark Shipped' with model selector, Microsoft Office integration, live poll, and community story. Registration at luma.com/sow0e7ym.",
      "title": "Genspark Shipped — new monthly show"
    },
    {
      "item_id": "item_0319c525d4e44f30999a4b3b88094acf",
      "role": "aggregator",
      "summary": "上海电信推出Token套餐：1元25万token，支持30+大模型，话费账单支付。",
      "title": "Shanghai Telecom offers token-based phone plan"
    },
    {
      "item_id": "item_0383dfaf0bf44392b776057c9180953c",
      "role": "firsthand",
      "summary": "Sam Wasserman built an NVIDIA AI Spark rig with a custom dual sparks monitoring dashboard.",
      "title": "NVIDIA AI Spark Rig Build"
    },
    {
      "item_id": "item_04241695f9a144a689113f7e9db84b91",
      "role": "source_material",
      "summary": "LlamaIndex (by Jerry Liu) was included in the CBInsights AI 100 list for 2026.",
      "title": "LlamaIndex on CBInsights AI 100 list for 2026"
    },
    {
      "item_id": "item_05394b5b614b47ee83cd065209d519b7",
      "role": "report",
      "summary": "Anthropic 提到的典型用法包括：同时派发多个想法、让不同 Agent 配合不同 skill 生成 PR、管理长期运行任务，比如 PR babysitter、dashboard updater，以及在多个任务之间快速切换。 claude.com/blog/agent-vie… 💬 1 🔄 0 ❤️ 1 👀 4025 📊 2 ⚡ Powered by xgo.ing",
      "title": "Anthropic 提到的典型用法包括：同时派发多个想法、让不同 Agent 配合不同 skill 生成 PR、管理长期运行任务，比如 PR babysitter、dashboard updater，..."
    },
    {
      "item_id": "item_067673d998c744dbb2ad7cbc70f3ff9a",
      "role": "source_material",
      "summary": "OpenAI Developers announce a contest: show Codex pets you hatched using /hatch, 10 winners get 30 days of ChatGPT Pro.",
      "title": "OpenAI Developers Codex Pet Contest"
    },
    {
      "item_id": "item_0701f5b62e3f438fb3d1d6904ccd823a",
      "role": "source_material",
      "summary": "Grok 4.3 is live on xAI API, with top leaderboard rankings in agentic tool calling and instruction following, and #1 in ValsAI enterprise domains. Supports 1M token context, priced at $1.25/M input and $2.50/M output.",
      "title": "xAI releases Grok 4.3"
    },
    {
      "item_id": "item_070f626f5d754f7dae1bee4c9fb637a9",
      "role": "source_material",
      "summary": "企业里的人+Agent 协作产品 Syncless 发布了 Yeuoly @Yeuoly1 x.com/i/article/2053… 🔗 View Quoted Tweet 💬 1 🔄 8 ❤️ 49 👀 27520 📊 17 ⚡ Powered by xgo.ing",
      "title": "企业里的人+Agent 协作产品 Syncless 发布了"
    },
    {
      "item_id": "item_0813ece9e037468e9d994234446c92b1",
      "role": "commentary",
      "summary": "Korea sells banana packs with bananas at different ripeness stages for daily consumption, solving the problem of bananas going bad.",
      "title": "Korea sells 'one-a-day' banana packs with different ripeness levels"
    }
  ],
  "warnings_distribution": {
    "affiliate_link": 1,
    "aggregator_post": 1,
    "boilerplate_tweet": 1,
    "brief_post": 1,
    "data source not specified": 1,
    "deterministic_minimal_card": 104,
    "duplicate content with previous post": 1,
    "launch announcement": 2,
    "low_detail": 1,
    "low_information": 1,
    "low_signal": 2,
    "marketing": 5,
    "marketing_event": 1,
    "no_event": 2,
    "no_technical_details": 1,
    "not original source": 1,
    "opinion": 3,
    "opinion heavy": 1,
    "opinion piece": 1,
    "opinion_based": 1,
    "opinion_only": 5,
    "opinion_piece": 3,
    "personal anecdote": 1,
    "personal_anecdote": 1,
    "personal_experience": 1,
    "personal_message": 1,
    "podcast summary": 1,
    "promotional": 10,
    "promotional content": 2,
    "promotional_content": 2,
    "promotional_language": 1,
    "reposted_content": 2,
    "republished_content": 1,
    "single anecdote": 1,
    "social_media": 1,
    "social_media_boilerplate": 6,
    "social_media_commentary": 1,
    "social_media_post": 10,
    "social_media_quote": 1,
    "social_post": 3,
    "source is social media": 1,
    "subjective": 2,
    "subjective claims": 1,
    "summary_only": 11,
    "thin_content": 1,
    "third_party_summary": 1,
    "too_short": 1,
    "unverified_claim": 1,
    "unverified_claims": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.849,
  "candidate_lane_distribution": {
    "deterministic": 2,
    "exploratory_recall": 1573,
    "precision_event": 50,
    "same_actor_product": 2,
    "same_event_recall": 157,
    "same_product_different_event": 114,
    "same_thread": 3802,
    "suppressed": 2483,
    "unknown": 521
  },
  "candidate_pairs_considered": 940,
  "candidate_priority_distribution": {
    "high": 53,
    "low": 4359,
    "medium": 1682,
    "must_run": 127,
    "suppress": 2483
  },
  "candidates_suppressed_without_llm": 2483,
  "cluster_eligible_count": 3,
  "different": 572,
  "duplicate": 1,
  "duplicate_direction_suppressed_count": 127,
  "event_relation_type_distribution": {
    "different": 71,
    "entity_overlap_only": 14,
    "same_account_boilerplate": 8,
    "same_event": 17,
    "same_product_different_event": 103,
    "same_thread": 664,
    "same_topic_only": 63
  },
  "examples": [
    {
      "candidate_item_title": "Use a template from our marketplace to automate CI investigations: https://t.co/ou0OHzwvtq",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "- Docs: https://t.co/qoUnGI1hcM - Cookbook: https://t.co/Hv16MQVGil - Cloudflare worker example repo...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Explore our developer guide (https://t.co/VXyi8qp0y8) and the Gemini API documentation (https://t.co...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Read more about it here: https://t.co/Y62XMaTOn3 https://t.co/Y62XMaTOn3",
      "confidence": 0.72,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "same_thread",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "deterministic same-thread lane",
      "secondary_roles": [
        "same_thread"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    },
    {
      "candidate_item_title": "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "New in Manus: Projects can now learn from every task. When a conversation produces reusable context...",
      "confidence": 0.72,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "same_thread",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "deterministic same-thread lane",
      "secondary_roles": [
        "same_thread"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    },
    {
      "candidate_item_title": "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been grea...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Introducing Recommended Connectors! Manus now helps set up what your task needs, when it needs it: ...",
      "confidence": 0.72,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "same_thread",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "deterministic same-thread lane",
      "secondary_roles": [
        "same_thread"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    },
    {
      "candidate_item_title": "- Docs: https://t.co/qoUnGI1hcM - Cookbook: https://t.co/Hv16MQVGil - Cloudflare worker example repo...",
      "confidence": 0.88,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "different",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    }
  ],
  "fold_candidates": 14,
  "high_priority_skips": 0,
  "item_relation_failures": 3,
  "item_relation_json_parse_failures": 3,
  "llm_item_relation_calls": 97,
  "low_confidence_examples": [],
  "must_run_skips": 0,
  "near_duplicate": 13,
  "pair_conflict_count": 0,
  "raw_relation_count": 940,
  "related_with_new_info": 4,
  "related_with_new_info_count": 4,
  "relations_by_primary_relation": {
    "different": 572,
    "duplicate": 1,
    "near_duplicate": 13,
    "related_with_new_info": 4,
    "same_product_different_event": 102,
    "same_thread": 248
  },
  "rule_relations": 984,
  "skipped_relation_llm_due_to_deterministic_decision": 453,
  "uncertain_count": 0,
  "unique_relation_pair_count": 928
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
    "high": 53,
    "low": 4359,
    "medium": 1682,
    "must_run": 127,
    "suppress": 2483
  },
  "candidates_suppressed_without_llm": 2483,
  "warning": "must_run/high should remain scarce; inspect candidate_generation.jsonl if inflated"
}
```

## 8. Relation Precision Review

```json
{
  "event_relation_type_distribution": {
    "different": 71,
    "entity_overlap_only": 14,
    "same_account_boilerplate": 8,
    "same_event": 17,
    "same_product_different_event": 103,
    "same_thread": 664,
    "same_topic_only": 63
  },
  "examples": [
    {
      "candidate_item_title": "Use a template from our marketplace to automate CI investigations: https://t.co/ou0OHzwvtq",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "- Docs: https://t.co/qoUnGI1hcM - Cookbook: https://t.co/Hv16MQVGil - Cloudflare worker example repo...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Explore our developer guide (https://t.co/VXyi8qp0y8) and the Gemini API documentation (https://t.co...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Read more about it here: https://t.co/Y62XMaTOn3 https://t.co/Y62XMaTOn3",
      "confidence": 0.72,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "same_thread",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "deterministic same-thread lane",
      "secondary_roles": [
        "same_thread"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    },
    {
      "candidate_item_title": "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "New in Manus: Projects can now learn from every task. When a conversation produces reusable context...",
      "confidence": 0.72,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "same_thread",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "deterministic same-thread lane",
      "secondary_roles": [
        "same_thread"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    },
    {
      "candidate_item_title": "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been grea...",
      "confidence": 0.88,
      "new_item_title": "Join the Runway team in Denver on June 4th at our annual CVPR Friends Dinner for conversation, cockt...",
      "primary_relation": "different",
      "published_at": "2026-05-05T14:22:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-runway-runwayml"
    },
    {
      "candidate_item_title": "Introducing Recommended Connectors! Manus now helps set up what your task needs, when it needs it: ...",
      "confidence": 0.72,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "same_thread",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "deterministic same-thread lane",
      "secondary_roles": [
        "same_thread"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    },
    {
      "candidate_item_title": "- Docs: https://t.co/qoUnGI1hcM - Cookbook: https://t.co/Hv16MQVGil - Cloudflare worker example repo...",
      "confidence": 0.88,
      "new_item_title": "Read the blog here: https://t.co/PUjeO6cyTp https://t.co/PUjeO6cyTp",
      "primary_relation": "different",
      "published_at": "2026-05-05T15:12:34+00:00",
      "reason": "weak thread lane without shared actor/product",
      "secondary_roles": [
        "weak_thread_lane"
      ],
      "should_fold": false,
      "source": "socialmedia-manusai-manusai-hq"
    }
  ],
  "near_duplicate": 13,
  "related_with_new_info": 4
}
```

## 9. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 100
  },
  "attached_existing_clusters": 3,
  "avg_confidence": 0.61,
  "avg_items_per_cluster": 1.031,
  "candidate_clusters_considered": 97,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters.",
      "core_facts": [
        "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters. Your browser does not support the video tag. 🔗 View on Twitter 💬 26 🔄 18 ❤️ 294 👀 17920 📊 59 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5da3277281e341328f7c32c2ef8ab521"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been grea...",
      "core_facts": [
        "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been greatly relaxed. ✨ Create freely now! #MiniMax a #Hailuo uo 💬 2 🔄 0 ❤️ 13 👀 1521 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_0e519a6df73043e39cc0e13039878d0b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one...",
      "core_facts": [
        "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one workspace, on one membership. 💬 3 🔄 1 ❤️ 11 👀 1163 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_6fe60ec847e841608bcc3db46a2e78f1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...",
      "core_facts": [
        "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Learn more: elevenlabs.io/blog/introduci… 💬 2 🔄 2 ❤️ 13 👀 2691 📊 4 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f4e93ae873c74b3dac04d38306ef0caf"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Explore our developer guide (https://t.co/VXyi8qp0y8) and the Gemini API documentation (https://t.co...",
      "core_facts": [
        "Explore our developer guide ( dev.to/googleai/multi… ) and the Gemini API documentation ( ai.google.dev/gemini-api/doc… ) to get started. 💬 0 🔄 1 ❤️ 2 👀 1393 📊 2 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_402455c7b47141eabbaddb400093987d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @an...",
      "core_facts": [
        "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @angjiang on claude platform! 💬 7 🔄 4 ❤️ 38 👀 5049 📊 14 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b705c48e5dba435a820b7f84a2c281ef"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
      "core_facts": [
        "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查更新 → 开冲 🚀 暂定限免两周，用得越多，限免越久。 都去用吧！ 邀请码： Mayday-CERX3N35 💬 6 🔄 0 ❤️ 11 👀 4044 📊 6 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_28be0a90fd9f47d98dc2bec0506619df"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs https://t.co/35NWqpOseV",
      "core_facts": [
        "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs x.com/i/broadcasts/1… 💬 10 🔄 15 ❤️ 61 👀 4995 📊 19 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_aa533262a79844338c339bf54bb86428"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s...",
      "core_facts": [
        "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s now easier than ever to get started. Try it today. 💬 2 🔄 4 ❤️ 46 👀 22659 📊 10 ⚡ Powered by xgo.ing"
      ],
      "item_count": 2,
      "known_angles": [],
      "representative_items": [
        "item_60c905d08c34476b9eec1abbb68ca599"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "企业里的人+Agent 协作产品 Syncless 发布了",
      "core_facts": [
        "企业里的人+Agent 协作产品 Syncless 发布了 Yeuoly @Yeuoly1 x.com/i/article/2053… 🔗 View Quoted Tweet 💬 1 🔄 8 ❤️ 49 👀 27520 📊 17 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_070f626f5d754f7dae1bee4c9fb637a9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。",
      "core_facts": [
        "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。 💬 2 🔄 2 ❤️ 10 👀 6278 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_60349083c5b54e3cb8d9b88d09771bdf"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 ...",
      "core_facts": [
        "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 32.3%。 过去一年，Anthropic 的采用率翻了四倍，而 OpenAI 仅增长 0.3%。 💬 4 🔄 0 ❤️ 6 👀 5079 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 2,
      "known_angles": [],
      "representative_items": [
        "item_0dddd1e479054b6c8373c1de5d2b1ce3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "GPT-5.5 is now available in Windsurf 2.0!",
      "core_facts": [
        "GPT-5.5 is now available in Windsurf 2.0! 💬 27 🔄 22 ❤️ 539 👀 90776 📊 96 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_de9de29e477a4bbb93428780cdc8f25d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anthropic launches enterprise services division",
      "core_facts": [
        "Anthropic built a $1.5B services company embedding engineers into enterprises to implement Claude across healthcare, manufacturing, finance, retail. Blackstone and Goldman portfolio companies are first customers. Anthropic partners with Accenture, Deloitte, PwC but new firm competes with them."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_476f1cbcee1f4ab29b9d9e399651ad48"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Cursor debug mode usage experience",
      "core_facts": [
        "Author used Cursor's debug mode to fix a bug in a Swift app where initial characters were cut off. Steps: instrument code, reproduce, read debug logs, implement fix, verify. Cursor fixed it first try."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ab269cc96e6e4f739337d964ea9233a9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Manus launches Recommended Connectors feature",
      "core_facts": [
        "Manus now recommends relevant connectors in context and helps enable them with user approval."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8f1d798750a54a1fb59a192778f61ac0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LlamaIndex makes CBInsights AI 100 list 2026",
      "core_facts": [
        "LlamaIndex (by Jerry Liu) was included in the CBInsights AI 100 list for 2026."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_04241695f9a144a689113f7e9db84b91"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Perplexity Computer launches Professional Finance",
      "core_facts": [
        "Perplexity Computer launched for professional finance, integrating licensed data from Morningstar, PitchBook, Daloopa, Carbon Arc and offering 35 dedicated finance workflows."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_4b3d7ccaa74841d79c92104043b4e1bc"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Firecrawl releases PHP SDK",
      "core_facts": [
        "Firecrawl released a PHP SDK for scraping pages to markdown, web searches, and dynamic site navigation."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_46a20db92cb24013992f915d25ab5c19"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Perplexity Computer traceability feature",
      "core_facts": [
        "Perplexity Computer shows traceable citations for numbers, linking to SEC filings, earnings transcripts, market data pages, or licensed sources."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_e07158be6a264b1b8dc8378ecad109f4"
      ]
    }
  ],
  "created_clusters": 97,
  "effective_multi_item_cluster_count": 3,
  "follow_up_event": {
    "false": 100
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 3,
  "relations": {
    "new_info": 54,
    "repeat": 1,
    "source_material": 45
  },
  "reported_multi_item_cluster_count": 3,
  "reviewed_multi_item_cluster_count": 3,
  "same_event": {
    "true": 100
  },
  "same_topic": {
    "false": 3,
    "true": 97
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 99,
  "suspect_multi_item_cluster_count": 0,
  "top_clusters": [
    {
      "cluster_id": "cluster_0e916033bacc4a52b50135b30902ef7c",
      "cluster_title": "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s...",
      "item_count": 2
    },
    {
      "cluster_id": "cluster_a3c1ae1e70c54ddf89ece204eb2f3bef",
      "cluster_title": "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 ...",
      "item_count": 2
    },
    {
      "cluster_id": "cluster_3961b3417359475b95622c90038caa7a",
      "cluster_title": "Perplexity announces premium health sources availability",
      "item_count": 2
    },
    {
      "cluster_id": "cluster_090808113218413ab87d83b35fc97bc6",
      "cluster_title": "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters.",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_3aa75e8dd4ba4334ac5fdde2cadfec1e",
      "cluster_title": "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been grea...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_e1df71e564ef4472a13275d0d19d506e",
      "cluster_title": "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_dd5d9a65b95644a7926dfcff4281df3d",
      "cluster_title": "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_ffc4c128b9f349d58a678b7b34bb7c23",
      "cluster_title": "Explore our developer guide (https://t.co/VXyi8qp0y8) and the Gemini API documentation (https://t.co...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_641553452a4440ed81b23f0b517143c1",
      "cluster_title": "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @an...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_d5a0ff55830049b8bfeae8cd952740a7",
      "cluster_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
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
      "cluster_title": "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters.",
      "core_facts": [
        "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters. Your browser does not support the video tag. 🔗 View on Twitter 💬 26 🔄 18 ❤️ 294 👀 17920 📊 59 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5da3277281e341328f7c32c2ef8ab521"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been grea...",
      "core_facts": [
        "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been greatly relaxed. ✨ Create freely now! #MiniMax a #Hailuo uo 💬 2 🔄 0 ❤️ 13 👀 1521 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_0e519a6df73043e39cc0e13039878d0b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one...",
      "core_facts": [
        "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one workspace, on one membership. 💬 3 🔄 1 ❤️ 11 👀 1163 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_6fe60ec847e841608bcc3db46a2e78f1"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...",
      "core_facts": [
        "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Learn more: elevenlabs.io/blog/introduci… 💬 2 🔄 2 ❤️ 13 👀 2691 📊 4 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f4e93ae873c74b3dac04d38306ef0caf"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Explore our developer guide (https://t.co/VXyi8qp0y8) and the Gemini API documentation (https://t.co...",
      "core_facts": [
        "Explore our developer guide ( dev.to/googleai/multi… ) and the Gemini API documentation ( ai.google.dev/gemini-api/doc… ) to get started. 💬 0 🔄 1 ❤️ 2 👀 1393 📊 2 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_402455c7b47141eabbaddb400093987d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @an...",
      "core_facts": [
        "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @angjiang on claude platform! 💬 7 🔄 4 ❤️ 38 👀 5049 📊 14 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b705c48e5dba435a820b7f84a2c281ef"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
      "core_facts": [
        "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查更新 → 开冲 🚀 暂定限免两周，用得越多，限免越久。 都去用吧！ 邀请码： Mayday-CERX3N35 💬 6 🔄 0 ❤️ 11 👀 4044 📊 6 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_28be0a90fd9f47d98dc2bec0506619df"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs https://t.co/35NWqpOseV",
      "core_facts": [
        "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs x.com/i/broadcasts/1… 💬 10 🔄 15 ❤️ 61 👀 4995 📊 19 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_aa533262a79844338c339bf54bb86428"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s...",
      "core_facts": [
        "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s now easier than ever to get started. Try it today. 💬 2 🔄 4 ❤️ 46 👀 22659 📊 10 ⚡ Powered by xgo.ing"
      ],
      "item_count": 2,
      "known_angles": [],
      "representative_items": [
        "item_60c905d08c34476b9eec1abbb68ca599"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "企业里的人+Agent 协作产品 Syncless 发布了",
      "core_facts": [
        "企业里的人+Agent 协作产品 Syncless 发布了 Yeuoly @Yeuoly1 x.com/i/article/2053… 🔗 View Quoted Tweet 💬 1 🔄 8 ❤️ 49 👀 27520 📊 17 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_070f626f5d754f7dae1bee4c9fb637a9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。",
      "core_facts": [
        "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。 💬 2 🔄 2 ❤️ 10 👀 6278 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_60349083c5b54e3cb8d9b88d09771bdf"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 ...",
      "core_facts": [
        "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 32.3%。 过去一年，Anthropic 的采用率翻了四倍，而 OpenAI 仅增长 0.3%。 💬 4 🔄 0 ❤️ 6 👀 5079 📊 5 ⚡ Powered by xgo.ing"
      ],
      "item_count": 2,
      "known_angles": [],
      "representative_items": [
        "item_0dddd1e479054b6c8373c1de5d2b1ce3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "GPT-5.5 is now available in Windsurf 2.0!",
      "core_facts": [
        "GPT-5.5 is now available in Windsurf 2.0! 💬 27 🔄 22 ❤️ 539 👀 90776 📊 96 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_de9de29e477a4bbb93428780cdc8f25d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Anthropic launches enterprise services division",
      "core_facts": [
        "Anthropic built a $1.5B services company embedding engineers into enterprises to implement Claude across healthcare, manufacturing, finance, retail. Blackstone and Goldman portfolio companies are first customers. Anthropic partners with Accenture, Deloitte, PwC but new firm competes with them."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_476f1cbcee1f4ab29b9d9e399651ad48"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Cursor debug mode usage experience",
      "core_facts": [
        "Author used Cursor's debug mode to fix a bug in a Swift app where initial characters were cut off. Steps: instrument code, reproduce, read debug logs, implement fix, verify. Cursor fixed it first try."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ab269cc96e6e4f739337d964ea9233a9"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Manus launches Recommended Connectors feature",
      "core_facts": [
        "Manus now recommends relevant connectors in context and helps enable them with user approval."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8f1d798750a54a1fb59a192778f61ac0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LlamaIndex makes CBInsights AI 100 list 2026",
      "core_facts": [
        "LlamaIndex (by Jerry Liu) was included in the CBInsights AI 100 list for 2026."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_04241695f9a144a689113f7e9db84b91"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Perplexity Computer launches Professional Finance",
      "core_facts": [
        "Perplexity Computer launched for professional finance, integrating licensed data from Morningstar, PitchBook, Daloopa, Carbon Arc and offering 35 dedicated finance workflows."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_4b3d7ccaa74841d79c92104043b4e1bc"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Firecrawl releases PHP SDK",
      "core_facts": [
        "Firecrawl released a PHP SDK for scraping pages to markdown, web searches, and dynamic site navigation."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_46a20db92cb24013992f915d25ab5c19"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Perplexity Computer traceability feature",
      "core_facts": [
        "Perplexity Computer shows traceable citations for numbers, linking to SEC filings, earnings transcripts, market data pages, or licensed sources."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_e07158be6a264b1b8dc8378ecad109f4"
      ]
    }
  ],
  "evidence_files": [
    "cluster_seed_candidates.jsonl",
    "cluster_seed_rejections.jsonl",
    "clusters_final.jsonl"
  ],
  "multi_item_cluster_count": 3
}
```

## 11. Budget Skip Quality

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "phase1_3_advisory",
  "stages": {
    "cluster_card_patch": {
      "budget": 53200,
      "calls": 3,
      "consumed_tokens": 6745,
      "remaining_budget": 46455,
      "skipped": 97,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 258400,
      "calls": 60,
      "consumed_tokens": 285153,
      "remaining_budget": 0,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_cluster_relation": {
      "budget": 190000,
      "calls": 13,
      "consumed_tokens": 99076,
      "remaining_budget": 90924,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_relation": {
      "budget": 235600,
      "calls": 97,
      "consumed_tokens": 284320,
      "remaining_budget": 0,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "source_profile": {
      "budget": 22800,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 22800,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 760000
}
```

## 12. Cost / Yield

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 22522.4,
    "cache_hit_tokens": 71168,
    "cache_miss_tokens": 0,
    "calls": 60,
    "failed": 4,
    "input_tokens": 152468,
    "llm_call_count": 60,
    "operation_count": 60,
    "output_tokens": 132685,
    "p50_latency_ms": 23426,
    "p95_latency_ms": 54036,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 4,
    "skipped": 0,
    "success": 56,
    "task_type": "item_card",
    "total_tokens": 285153
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9833.9,
    "cache_hit_tokens": 114816,
    "cache_miss_tokens": 0,
    "calls": 97,
    "failed": 3,
    "input_tokens": 179685,
    "llm_call_count": 97,
    "operation_count": 97,
    "output_tokens": 104635,
    "p50_latency_ms": 10093,
    "p95_latency_ms": 13718,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 3,
    "skipped": 0,
    "success": 94,
    "task_type": "item_relation",
    "total_tokens": 284320
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 15371.2,
    "cache_hit_tokens": 16512,
    "cache_miss_tokens": 0,
    "calls": 13,
    "failed": 1,
    "input_tokens": 79059,
    "llm_call_count": 13,
    "operation_count": 13,
    "output_tokens": 20017,
    "p50_latency_ms": 15398,
    "p95_latency_ms": 19307,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 1,
    "skipped": 0,
    "success": 12,
    "task_type": "item_cluster_relation",
    "total_tokens": 99076
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9734.3,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3623,
    "llm_call_count": 3,
    "operation_count": 100,
    "output_tokens": 3122,
    "p50_latency_ms": 9295,
    "p95_latency_ms": 10739,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 97,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6745
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
    "cluster_title": "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters.",
    "core_facts": [
      "GPT Image 2 is now in Lovable. Same prompts, new model. Here are some before and afters. Your browser does not support the video tag. 🔗 View on Twitter 💬 26 🔄 18 ❤️ 294 👀 17920 📊 59 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_5da3277281e341328f7c32c2ef8ab521"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been grea...",
    "core_facts": [
      "📢 Seedance 2.0 on Hailuo AI is now 65% cheaper! 🔓 Face generation restrictions have also been greatly relaxed. ✨ Create freely now! #MiniMax a #Hailuo uo 💬 2 🔄 0 ❤️ 13 👀 1521 📊 5 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_0e519a6df73043e39cc0e13039878d0b"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one...",
    "core_facts": [
      "GPT-5.5 and GPT Image 2 are both in Skywork. OpenAI's latest text and image models—available in one workspace, on one membership. 💬 3 🔄 1 ❤️ 11 👀 1163 📊 5 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_6fe60ec847e841608bcc3db46a2e78f1"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Le...",
    "core_facts": [
      "One agent, every channel, every modality. Meet your customers where they are with ElevenAgents. Learn more: elevenlabs.io/blog/introduci… 💬 2 🔄 2 ❤️ 13 👀 2691 📊 4 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f4e93ae873c74b3dac04d38306ef0caf"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Explore our developer guide (https://t.co/VXyi8qp0y8) and the Gemini API documentation (https://t.co...",
    "core_facts": [
      "Explore our developer guide ( dev.to/googleai/multi… ) and the Gemini API documentation ( ai.google.dev/gemini-api/doc… ) to get started. 💬 0 🔄 1 ❤️ 2 👀 1393 📊 2 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_402455c7b47141eabbaddb400093987d"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @an...",
    "core_facts": [
      "experiment: livetweeting the @AnthropicAI code with claude event! first up - @katelyn_lesse and @angjiang on claude platform! 💬 7 🔄 4 ❤️ 38 👀 5049 📊 14 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b705c48e5dba435a820b7f84a2c281ef"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查...",
    "core_facts": [
      "五月惊喜，ColaOS 新模型上线，限时免费尝鲜。 什么模型？先不剧透，试了你就知道了。 记得更新到最新版本，不然找不到。 努力让所有人都能遇到 Cola。欢迎多多分享邀请哦~ 打开Cola → 检查更新 → 开冲 🚀 暂定限免两周，用得越多，限免越久。 都去用吧！ 邀请码： Mayday-CERX3N35 💬 6 🔄 0 ❤️ 11 👀 4044 📊 6 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_28be0a90fd9f47d98dc2bec0506619df"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs https://t.co/35NWqpOseV",
    "core_facts": [
      "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs x.com/i/broadcasts/1… 💬 10 🔄 15 ❤️ 61 👀 4995 📊 19 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_aa533262a79844338c339bf54bb86428"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s...",
    "core_facts": [
      "LangSmith Fleet now has a free model powered by @FireworksAI_HQ for Developer and Plus plans. It’s now easier than ever to get started. Try it today. 💬 2 🔄 4 ❤️ 46 👀 22659 📊 10 ⚡ Powered by xgo.ing"
    ],
    "item_count": 2,
    "known_angles": [],
    "representative_items": [
      "item_60c905d08c34476b9eec1abbb68ca599"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "企业里的人+Agent 协作产品 Syncless 发布了",
    "core_facts": [
      "企业里的人+Agent 协作产品 Syncless 发布了 Yeuoly @Yeuoly1 x.com/i/article/2053… 🔗 View Quoted Tweet 💬 1 🔄 8 ❤️ 49 👀 27520 📊 17 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_070f626f5d754f7dae1bee4c9fb637a9"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。",
    "core_facts": [
      "开源一个月的时间，飞书 CLI 在 Github 破万星了。 相比同期的一些 CLI，飞书这个确实是群里口碑最好的。 为 Agent 做软件这件事，飞书践行得很好。 💬 2 🔄 2 ❤️ 10 👀 6278 📊 5 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_60349083c5b54e3cb8d9b88d09771bdf"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 ...",
    "core_facts": [
      "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 32.3%。 过去一年，Anthropic 的采用率翻了四倍，而 OpenAI 仅增长 0.3%。 💬 4 🔄 0 ❤️ 6 👀 5079 📊 5 ⚡ Powered by xgo.ing"
    ],
    "item_count": 2,
    "known_angles": [],
    "representative_items": [
      "item_0dddd1e479054b6c8373c1de5d2b1ce3"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "GPT-5.5 is now available in Windsurf 2.0!",
    "core_facts": [
      "GPT-5.5 is now available in Windsurf 2.0! 💬 27 🔄 22 ❤️ 539 👀 90776 📊 96 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_de9de29e477a4bbb93428780cdc8f25d"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Anthropic launches enterprise services division",
    "core_facts": [
      "Anthropic built a $1.5B services company embedding engineers into enterprises to implement Claude across healthcare, manufacturing, finance, retail. Blackstone and Goldman portfolio companies are first customers. Anthropic partners with Accenture, Deloitte, PwC but new firm competes with them."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_476f1cbcee1f4ab29b9d9e399651ad48"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Cursor debug mode usage experience",
    "core_facts": [
      "Author used Cursor's debug mode to fix a bug in a Swift app where initial characters were cut off. Steps: instrument code, reproduce, read debug logs, implement fix, verify. Cursor fixed it first try."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ab269cc96e6e4f739337d964ea9233a9"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Manus launches Recommended Connectors feature",
    "core_facts": [
      "Manus now recommends relevant connectors in context and helps enable them with user approval."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_8f1d798750a54a1fb59a192778f61ac0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "LlamaIndex makes CBInsights AI 100 list 2026",
    "core_facts": [
      "LlamaIndex (by Jerry Liu) was included in the CBInsights AI 100 list for 2026."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_04241695f9a144a689113f7e9db84b91"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Perplexity Computer launches Professional Finance",
    "core_facts": [
      "Perplexity Computer launched for professional finance, integrating licensed data from Morningstar, PitchBook, Daloopa, Carbon Arc and offering 35 dedicated finance workflows."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_4b3d7ccaa74841d79c92104043b4e1bc"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Firecrawl releases PHP SDK",
    "core_facts": [
      "Firecrawl released a PHP SDK for scraping pages to markdown, web searches, and dynamic site navigation."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_46a20db92cb24013992f915d25ab5c19"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Perplexity Computer traceability feature",
    "core_facts": [
      "Perplexity Computer shows traceable citations for numbers, linking to SEC filings, earnings transcripts, market data pages, or licensed sources."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_e07158be6a264b1b8dc8378ecad109f4"
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
    "socialmedia-aadit-sheth-aaditsh": 9315,
    "socialmedia-ai-breakfast-aibreakfast": 6738,
    "socialmedia-ai-engineer-aidotengineer": 9405,
    "socialmedia-aravind-srinivas-aravsrinivas": 16297,
    "socialmedia-chatgpt-chatgptapp": 6460,
    "socialmedia-clem-129303-clementdelangue": 6113,
    "socialmedia-cognition-cognition-labs": 14772,
    "socialmedia-dotey": 13215,
    "socialmedia-elevenlabs-elevenlabsio": 5840,
    "socialmedia-eric-zakariasson-ericzakariasson": 6140,
    "socialmedia-greg-brockman-gdb": 19118,
    "socialmedia-hugging-face-huggingface": 6847,
    "socialmedia-imxiaohu": 20318,
    "socialmedia-jerry-liu-jerryjliu0": 12678,
    "socialmedia-junyang-lin-justinlin610": 5618,
    "socialmedia-langchain-langchainai": 15649,
    "socialmedia-lmarena-ai-lmarena-ai": 9498,
    "socialmedia-meng-shao-shao-meng": 9282,
    "socialmedia-notion-notionhq": 9543,
    "socialmedia-nvidia-ai-nvidiaai": 18125,
    "socialmedia-openai-developers-openaidevs": 8573,
    "socialmedia-openai-openai": 28690,
    "socialmedia-orange-ai-oran-ge": 7530,
    "socialmedia-patrick-loeber-patloeber": 32729,
    "socialmedia-perplexity-perplexity-ai": 6047,
    "socialmedia-philipp-schmid-philschmid": 6420,
    "socialmedia-poe-poe-platform": 14219,
    "socialmedia-simon-willison-simonw": 6663,
    "socialmedia-the-rundown-ai-therundownai": 14479,
    "socialmedia-windsurf-windsurf-ai": 6465
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 286,
  "reviews_suppressed_due_to_insufficient_data": 76,
  "sources_recomputed": 76,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-a16z-a16z",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9315,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aadit-sheth-aaditsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6738,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 1.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9405,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 4961,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-ak-akhaliq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3213,
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
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2544,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-anthropic-anthropicai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 16297,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.3333333333333335,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aravind-srinivas-aravsrinivas",
      "source_item_rate": 0.3333333333333333,
      "source_material_rate": 0.3333333333333333,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4729,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-browser-use-browser-use",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 7,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6460,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6113,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-clem-129303-clementdelangue",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 14772,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2947,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 13215,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-dotey",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5840,
      "llm_yield_score": 3.583,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_item_rate": 0.6666666666666666,
      "source_material_rate": 0.6666666666666666,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2534,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-elvis-omarsar0",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3082,
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
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 1.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6847,
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
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-a16z-a16z",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9315,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aadit-sheth-aaditsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6738,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 1.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9405,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 4961,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-ak-akhaliq",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3213,
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
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9315,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aadit-sheth-aaditsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6738,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 1.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9405,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 4961,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3213,
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
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2544,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-anthropic-anthropicai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 16297,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.3333333333333335,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aravind-srinivas-aravsrinivas",
      "source_item_rate": 0.3333333333333333,
      "source_material_rate": 0.3333333333333333,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4729,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-browser-use-browser-use",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 7,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6460,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2544,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-anthropic-anthropicai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4729,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-browser-use-browser-use",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 7,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6460,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6113,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-clem-129303-clementdelangue",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2947,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 5400,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-firecrawl-firecrawl-dev",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-manusai-manusai-hq",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9543,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.25,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-notion-notionhq",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 8573,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-developers-openaidevs",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 28690,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.2,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 1,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 16297,
      "llm_yield_score": 3.25,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.3333333333333335,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aravind-srinivas-aravsrinivas",
      "source_item_rate": 0.3333333333333333,
      "source_material_rate": 0.3333333333333333,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9315,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-aadit-sheth-aaditsh",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6738,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 1.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 9405,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 4961,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
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
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3213,
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
      "total_items": 3,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2544,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-anthropic-anthropicai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4729,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-browser-use-browser-use",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 7,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    },
    {
      "created_at": "2026-05-18T01:19:54.061099+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6460,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-18T01:19:54.061099+00:00"
    }
  ]
}
```

## 15. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 22522.4,
    "cache_hit_tokens": 71168,
    "cache_miss_tokens": 0,
    "calls": 60,
    "failed": 4,
    "input_tokens": 152468,
    "llm_call_count": 60,
    "operation_count": 60,
    "output_tokens": 132685,
    "p50_latency_ms": 23426,
    "p95_latency_ms": 54036,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 4,
    "skipped": 0,
    "success": 56,
    "task_type": "item_card",
    "total_tokens": 285153
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9833.9,
    "cache_hit_tokens": 114816,
    "cache_miss_tokens": 0,
    "calls": 97,
    "failed": 3,
    "input_tokens": 179685,
    "llm_call_count": 97,
    "operation_count": 97,
    "output_tokens": 104635,
    "p50_latency_ms": 10093,
    "p95_latency_ms": 13718,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 3,
    "skipped": 0,
    "success": 94,
    "task_type": "item_relation",
    "total_tokens": 284320
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 15371.2,
    "cache_hit_tokens": 16512,
    "cache_miss_tokens": 0,
    "calls": 13,
    "failed": 1,
    "input_tokens": 79059,
    "llm_call_count": 13,
    "operation_count": 13,
    "output_tokens": 20017,
    "p50_latency_ms": 15398,
    "p95_latency_ms": 19307,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 1,
    "skipped": 0,
    "success": 12,
    "task_type": "item_cluster_relation",
    "total_tokens": 99076
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9734.3,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3623,
    "llm_call_count": 3,
    "operation_count": 100,
    "output_tokens": 3122,
    "p50_latency_ms": 9295,
    "p95_latency_ms": 10739,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 97,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6745
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
  "actual_calls": 173,
  "actual_tokens": 675294,
  "avg_latency_ms": 14648.9,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 9734.3,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 9295,
      "p95_latency_ms": 10739,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6745
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
      "avg_latency_ms": 22522.4,
      "cache_hit_tokens": 71168,
      "calls": 60,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 4,
      "p50_latency_ms": 23426,
      "p95_latency_ms": 54036,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 4,
      "success": 56,
      "task_type": "item_card",
      "total_tokens": 285153
    },
    "item_cluster_relation": {
      "avg_latency_ms": 15371.2,
      "cache_hit_tokens": 16512,
      "calls": 13,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 1,
      "p50_latency_ms": 15398,
      "p95_latency_ms": 19307,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 1,
      "success": 12,
      "task_type": "item_cluster_relation",
      "total_tokens": 99076
    },
    "item_relation": {
      "avg_latency_ms": 9833.9,
      "cache_hit_tokens": 114816,
      "calls": 97,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 3,
      "p50_latency_ms": 10093,
      "p95_latency_ms": 13718,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 3,
      "success": 94,
      "task_type": "item_relation",
      "total_tokens": 284320
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
  "cache_hit_rate": 0.3021,
  "cache_hit_tokens": 204032,
  "calls_per_sec": 0.1381,
  "db_lock_errors": 0,
  "duration_seconds": 1252.876,
  "final_failures": 8,
  "max_concurrency": 5,
  "p50_latency_ms": 11210,
  "p95_latency_ms": 30889,
  "parse_failures": 1,
  "rate_limit_errors": 0,
  "repair_retry_count": 8,
  "tokens_per_sec": 539.0
}
```

## 17. Stage Budget Summary

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "phase1_3_advisory",
  "stages": {
    "cluster_card_patch": {
      "budget": 53200,
      "calls": 3,
      "consumed_tokens": 6745,
      "remaining_budget": 46455,
      "skipped": 97,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 258400,
      "calls": 60,
      "consumed_tokens": 285153,
      "remaining_budget": 0,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_cluster_relation": {
      "budget": 190000,
      "calls": 13,
      "consumed_tokens": 99076,
      "remaining_budget": 90924,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_relation": {
      "budget": 235600,
      "calls": 97,
      "consumed_tokens": 284320,
      "remaining_budget": 0,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "source_profile": {
      "budget": 22800,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 22800,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 760000
}
```

## 18. Errors / Fallbacks / Retries

```json
{
  "db_lock_errors": 0,
  "failed_batch_count": 4,
  "fallback_rate": 0.0,
  "final_failures": 8,
  "heuristic_fallback_count": 0,
  "item_card_count": 300,
  "llm_card_count": 56,
  "llm_parse_failures": 0,
  "repair_retry_count": 8,
  "review_queue_entries_due_to_failure": 4,
  "single_retry_success_count": 20,
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
    "max_calls": 650,
    "max_items": 300,
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
  "blockers": [
    {
      "name": "small_scoped_real_write_rehearsal",
      "passed": false,
      "reason": "production readiness requires a scoped write rehearsal",
      "threshold": true,
      "value": false
    }
  ],
  "gates": [
    {
      "name": "heuristic_fallback_rate",
      "passed": true,
      "reason": "heuristic emergency fallback must stay low",
      "threshold": "< 0.1",
      "value": 0.0
    },
    {
      "name": "parse_failure_fallback_rate",
      "passed": true,
      "reason": "parse failures must not dominate cards",
      "threshold": "< 0.03",
      "value": 0.0
    },
    {
      "name": "budget_skip_fallback_rate",
      "passed": true,
      "reason": "budget fallback must not starve candidate-bearing cards",
      "threshold": "< 0.05",
      "value": 0.0
    },
    {
      "name": "skipped_must_run_candidates",
      "passed": true,
      "reason": "must-run candidates are protected",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "pair_relation_conflicts",
      "passed": true,
      "reason": "canonical pair verdicts cannot conflict",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "db_lock_errors",
      "passed": true,
      "reason": "no DB lock errors",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "event_signature_valid_rate",
      "passed": true,
      "reason": "signatures are concrete enough",
      "threshold": ">= 0.6",
      "value": 0.9813
    },
    {
      "name": "chinese_event_detection_rate",
      "passed": true,
      "reason": "Chinese event-like items must not all be rejected",
      "threshold": ">= 0.5",
      "value": 0.5143
    },
    {
      "name": "accepted_garbage_product_count",
      "passed": true,
      "reason": "URL/date/number/long-fragment products must be rejected",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "effective_multi_item_clusters",
      "passed": true,
      "reason": "dry-run produced useful same-event clusters",
      "threshold": ">= 1",
      "value": 3
    },
    {
      "name": "suspect_multi_item_clusters",
      "passed": true,
      "reason": "no suspect multi-item clusters accepted",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "small_scoped_real_write_rehearsal",
      "passed": false,
      "reason": "production readiness requires a scoped write rehearsal",
      "threshold": true,
      "value": false
    }
  ],
  "ready": false,
  "verdict": "NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE"
}
```

## 22. Recommendations

- Add vector indexes for item_cards and cluster_cards before larger runs.
- Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.
- Collect more source_signals before trusting source_profile priority suggestions.
- Run a larger dry-run before any write-real-db semantic pass.

## 10. Concurrency Summary

```json
{
  "actual_calls": 173,
  "actual_tokens": 675294,
  "avg_latency_ms": 14648.9,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 9734.3,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 9295,
      "p95_latency_ms": 10739,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6745
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
      "avg_latency_ms": 22522.4,
      "cache_hit_tokens": 71168,
      "calls": 60,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 4,
      "p50_latency_ms": 23426,
      "p95_latency_ms": 54036,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 4,
      "success": 56,
      "task_type": "item_card",
      "total_tokens": 285153
    },
    "item_cluster_relation": {
      "avg_latency_ms": 15371.2,
      "cache_hit_tokens": 16512,
      "calls": 13,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 1,
      "p50_latency_ms": 15398,
      "p95_latency_ms": 19307,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 1,
      "success": 12,
      "task_type": "item_cluster_relation",
      "total_tokens": 99076
    },
    "item_relation": {
      "avg_latency_ms": 9833.9,
      "cache_hit_tokens": 114816,
      "calls": 97,
      "concurrency": 5,
      "db_lock_errors": 0,
      "failed": 3,
      "p50_latency_ms": 10093,
      "p95_latency_ms": 13718,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 3,
      "success": 94,
      "task_type": "item_relation",
      "total_tokens": 284320
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
  "cache_hit_rate": 0.3021,
  "cache_hit_tokens": 204032,
  "calls_per_sec": 0.1381,
  "db_lock_errors": 0,
  "duration_seconds": 1252.876,
  "final_failures": 8,
  "max_concurrency": 5,
  "p50_latency_ms": 11210,
  "p95_latency_ms": 30889,
  "parse_failures": 1,
  "rate_limit_errors": 0,
  "repair_retry_count": 8,
  "tokens_per_sec": 539.0
}
```

## 14. Readiness Assessment

```json
{
  "blockers": [
    {
      "name": "small_scoped_real_write_rehearsal",
      "passed": false,
      "reason": "production readiness requires a scoped write rehearsal",
      "threshold": true,
      "value": false
    }
  ],
  "gates": [
    {
      "name": "heuristic_fallback_rate",
      "passed": true,
      "reason": "heuristic emergency fallback must stay low",
      "threshold": "< 0.1",
      "value": 0.0
    },
    {
      "name": "parse_failure_fallback_rate",
      "passed": true,
      "reason": "parse failures must not dominate cards",
      "threshold": "< 0.03",
      "value": 0.0
    },
    {
      "name": "budget_skip_fallback_rate",
      "passed": true,
      "reason": "budget fallback must not starve candidate-bearing cards",
      "threshold": "< 0.05",
      "value": 0.0
    },
    {
      "name": "skipped_must_run_candidates",
      "passed": true,
      "reason": "must-run candidates are protected",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "pair_relation_conflicts",
      "passed": true,
      "reason": "canonical pair verdicts cannot conflict",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "db_lock_errors",
      "passed": true,
      "reason": "no DB lock errors",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "event_signature_valid_rate",
      "passed": true,
      "reason": "signatures are concrete enough",
      "threshold": ">= 0.6",
      "value": 0.9813
    },
    {
      "name": "chinese_event_detection_rate",
      "passed": true,
      "reason": "Chinese event-like items must not all be rejected",
      "threshold": ">= 0.5",
      "value": 0.5143
    },
    {
      "name": "accepted_garbage_product_count",
      "passed": true,
      "reason": "URL/date/number/long-fragment products must be rejected",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "effective_multi_item_clusters",
      "passed": true,
      "reason": "dry-run produced useful same-event clusters",
      "threshold": ">= 1",
      "value": 3
    },
    {
      "name": "suspect_multi_item_clusters",
      "passed": true,
      "reason": "no suspect multi-item clusters accepted",
      "threshold": 0,
      "value": 0
    },
    {
      "name": "small_scoped_real_write_rehearsal",
      "passed": false,
      "reason": "production readiness requires a scoped write rehearsal",
      "threshold": true,
      "value": false
    }
  ],
  "ready": false,
  "verdict": "NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE"
}
```
