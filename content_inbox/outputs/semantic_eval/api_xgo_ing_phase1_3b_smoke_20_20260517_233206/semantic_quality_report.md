# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 12,
  "actual_tokens": 44027,
  "backup_path": null,
  "batch_size": 5,
  "cache_hit_tokens": 9600,
  "cache_miss_tokens": 0,
  "concurrency": 3,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 109.382,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_1rnucceq.sqlite3",
  "finished_at": "2026-05-17T15:33:56.171876+00:00",
  "git_commit": "74333606e67438d4b7ed72b9ecf0c738fb56a481",
  "include_archived": false,
  "items_sampled": 20,
  "live": true,
  "max_calls": 120,
  "max_candidates": 6,
  "max_items": 20,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260517_153206_789649",
  "sample_mode": "event_hotspots",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "stage_budget_profile": "phase1_3_advisory",
  "stage_budgets": {
    "cluster_card_patch": 8400,
    "item_card": 40800,
    "item_cluster_relation": 30000,
    "item_relation": 37200,
    "source_profile": 3600
  },
  "started_at": "2026-05-17T15:32:06.789649+00:00",
  "strong_model": null,
  "token_budget": 120000,
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
      "sampled_item_count": 8,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 2,
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
      "sampled_item_count": 3,
      "source_id": "socialmedia-openai-openai",
      "source_name": "OpenAI(@OpenAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/17687b1051204b2dbaed4ea4c9178f28",
      "item_count": 10,
      "latest_item_time": "2026-05-02T04:37:44+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 1,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-mem0-mem0ai",
      "source_name": "mem0(@mem0ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/48aae530e0bf413aa7d44380f418e2e3",
      "item_count": 9,
      "latest_item_time": "2026-05-14T09:27:33+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 9,
      "latest_item_time": "2026-05-05T20:47:13+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-paul-couvert-itspaulai",
      "source_name": "Paul Couvert(@itsPaulAi)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/900549ddadf04e839d3f7a17ebaba3fc",
      "item_count": 9,
      "latest_item_time": "2026-05-12T13:08:46+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-simon-willison-simonw",
      "source_name": "Simon Willison(@simonw)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6d7d398dd80b48d79669c92745d32cf6",
      "item_count": 9,
      "latest_item_time": "2026-05-06T12:03:54+00:00",
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 0,
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
      "sampled_item_count": 2,
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
      "sampled_item_count": 0,
      "source_id": "socialmedia-windsurf-windsurf-ai",
      "source_name": "Windsurf(@windsurf_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b1ab109f6afd42ab8ea32e17a19a3a3e",
      "item_count": 9,
      "latest_item_time": "2026-05-14T15:50:00+00:00",
      "sampled_item_count": 0,
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
  "items_sampled": 20,
  "items_too_short": 0,
  "items_with_raw_content": 20,
  "items_with_summary_only": 0,
  "languages": {
    "en_or_unknown": 10,
    "zh": 10
  },
  "source_count": 6,
  "time_range": {
    "max_created_at": "2026-05-17T15:32:07.505869+00:00",
    "min_created_at": "2026-05-17T15:32:07.491809+00:00"
  },
  "top_sources": [
    [
      "socialmedia-orange-ai-oran-ge",
      8
    ],
    [
      "socialmedia-marc-andreessen-127482-127480-pmarca",
      4
    ],
    [
      "socialmedia-openai-openai",
      3
    ],
    [
      "socialmedia-vista8",
      2
    ],
    [
      "socialmedia-nvidia-ai-nvidiaai",
      2
    ],
    [
      "socialmedia-ai-will-financeyf5",
      1
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.665,
  "avg_confidence_by_tier": {
    "full": 0.6,
    "minimal": 0.55,
    "standard": 0.77
  },
  "avg_tokens_by_tier": {
    "mixed_llm": 4973.3
  },
  "budget_skip_fallback_count": 0,
  "card_tier_distribution": {
    "full": 2,
    "minimal": 8,
    "standard": 10
  },
  "content_role_distribution": {
    "analysis": 1,
    "commentary": 6,
    "report": 9,
    "source_material": 4
  },
  "deterministic_minimal_card_count": 8,
  "entity_count_distribution": {
    "0": 1,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 3,
    "5": 2,
    "6": 3,
    "7": 4,
    "8": 1
  },
  "heuristic_card_fallback_count": 0,
  "item_cards_failed": 0,
  "item_cards_generated": 20,
  "item_cards_generated_or_reused": 20,
  "item_cards_reused": 0,
  "llm_failures_by_tier": {},
  "parse_error_fallback_count": 0,
  "samples": [
    {
      "item_id": "item_1234ea3f3b0e45958c0e20badb44521f",
      "role": "source_material",
      "summary": "OpenAI announced a new Chrome extension for Codex that automates repetitive browser tasks by writing and running code.",
      "title": "OpenAI releases Codex Chrome extension for browser automation"
    },
    {
      "item_id": "item_1884f9d6f83b413cbe182ce21bb4bf28",
      "role": "report",
      "summary": "上海电信将 Token 做成话费套餐，1元=25万token，支持30+大模型，话费账单支付，上海电信用户免费领2500万额度点。",
      "title": "上海电信推出 Token 话费套餐"
    },
    {
      "item_id": "item_1d52c6e0d1014db39beeef4eeee44d9a",
      "role": "source_material",
      "summary": "Codex now works directly in Chrome on macOS and Windows, with improved app/site handling and parallel tab execution.",
      "title": "Codex now works directly in Chrome on macOS and Windows"
    },
    {
      "item_id": "item_29aa8ad6ec684d979bbbdd41a73393c3",
      "role": "commentary",
      "summary": "Marc Andreessen shares Kevin O'Leary's allegation that opposition to Utah data centers is linked to Chinese funding via Arabella.",
      "title": "Kevin O'Leary claims Chinese funding behind Utah data center opposition"
    },
    {
      "item_id": "item_38ecb507430e4739bcd70d92e7ffd855",
      "role": "commentary",
      "summary": "Anthropological study says human decisions are driven by hormones, not reason. People make decisions then find evidence. Decision-makers must bear risk to produce the right hormones.",
      "title": "Quotation on decision-making: skin in the game"
    },
    {
      "item_id": "item_3c12452233e64f2aa013abaeeb44d41a",
      "role": "report",
      "summary": "原来一个人最真的信念 是凌晨随口说给朋友听的那版。 💬 1 🔄 0 ❤️ 1 👀 946 📊 1 ⚡ Powered by xgo.ing",
      "title": "原来一个人最真的信念 是凌晨随口说给朋友听的那版。"
    },
    {
      "item_id": "item_3da0bc512af944e09fe36e241aa68eb6",
      "role": "source_material",
      "summary": "Codex selects the best tool for each step in multi-tool tasks, using plugins, Chrome, or combinations as needed.",
      "title": "Codex chooses the best tool for each step"
    },
    {
      "item_id": "item_58051c3b13604298b85f1ddde9d866ec",
      "role": "report",
      "summary": "Substack revolution. Chris Best @chrisbest This misses a lot of traffic to custom domains too 🔗 View Quoted Tweet 💬 5 🔄 4 ❤️ 58 👀 27191 📊 8 ⚡ Powered by xgo.ing",
      "title": "Substack revolution."
    },
    {
      "item_id": "item_5d7e3ddc96c9459e93f96a3bb6de5a6f",
      "role": "analysis",
      "summary": "Vercel analyzed 200k projects and 10 trillion tokens over 7 months. Key findings: Anthropic 61% cost share, Google 38% token share; B2B produces 29.7% tokens but 40.7% cost; agent requests doubled from 31.6% to 58.9% in 6 months, consuming 2.6x tokens per request; large teams use 35 models on average.",
      "title": "Vercel report on LLM token consumption: Anthropic leads by cost, Google by tokens"
    },
    {
      "item_id": "item_730453ddeb1f43b49dc6f85e13d48aff",
      "role": "report",
      "summary": "实践是获得真理和获悉真相的唯一途径。 💬 0 🔄 1 ❤️ 4 👀 4727 📊 1 ⚡ Powered by xgo.ing",
      "title": "实践是获得真理和获悉真相的唯一途径。"
    }
  ],
  "warnings_distribution": {
    "deterministic_minimal_card": 8,
    "no_verifiable_facts": 1,
    "opinion_only": 2,
    "opinion_piece": 2,
    "social_media_single_source": 1,
    "unsubstantiated_claim": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.94,
  "candidate_lane_distribution": {
    "exploratory_recall": 14,
    "precision_event": 6,
    "same_thread": 88,
    "suppressed": 252,
    "unknown": 78
  },
  "candidate_pairs_considered": 24,
  "candidate_priority_distribution": {
    "low": 166,
    "medium": 5,
    "must_run": 15,
    "suppress": 252
  },
  "candidates_suppressed_without_llm": 252,
  "cluster_eligible_count": 0,
  "different": 21,
  "duplicate": 0,
  "duplicate_direction_suppressed_count": 6,
  "event_relation_type_distribution": {
    "different": 21,
    "same_event": 1,
    "same_product_different_event": 2
  },
  "examples": [
    {
      "candidate_item_title": "With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigati...",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Both announce the same Codex Chrome extension.",
      "secondary_roles": [],
      "should_fold": true,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "confidence": 0.9,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "same_product_different_event",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Describes a different feature of Codex, not the extension release.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Nuclear power plants were always ultra-safe as well; total global deaths from civilian nuclear power...",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Unrelated topic about Utah data centers.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Concerning.",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Unrelated topic about Utah data center opposition.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Interesting.",
      "confidence": 0.9,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Generic quote tweet, unrelated to Codex.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "原文：https://t.co/pVTjim12Ce 翻译：https://t.co/BhYuEybcTW",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Unrelated translation of Vercel AI Gateway blog.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigati...",
      "confidence": 0.9,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "same_product_different_event",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "Codex Chrome extension release vs. tool selection feature",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Nuclear power plants were always ultra-safe as well; total global deaths from civilian nuclear power...",
      "confidence": 0.95,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "Unrelated data center safety debate",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Concerning.",
      "confidence": 0.95,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "Unrelated funding allegation about data centers",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "If Luigi knows you, there’s a good chance a box is headed to your desk soon",
      "confidence": 0.95,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "NVIDIA radio astronomy kit unrelated to Codex",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    }
  ],
  "fold_candidates": 1,
  "high_priority_skips": 0,
  "llm_item_relation_calls": 5,
  "low_confidence_examples": [],
  "must_run_skips": 0,
  "near_duplicate": 1,
  "pair_conflict_count": 0,
  "raw_relation_count": 24,
  "related_with_new_info": 0,
  "related_with_new_info_count": 0,
  "relations_by_primary_relation": {
    "different": 21,
    "near_duplicate": 1,
    "same_product_different_event": 2
  },
  "uncertain_count": 0,
  "unique_relation_pair_count": 24
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
    "low": 166,
    "medium": 5,
    "must_run": 15,
    "suppress": 252
  },
  "candidates_suppressed_without_llm": 252,
  "warning": "must_run/high should remain scarce; inspect candidate_generation.jsonl if inflated"
}
```

## 8. Relation Precision Review

```json
{
  "event_relation_type_distribution": {
    "different": 21,
    "same_event": 1,
    "same_product_different_event": 2
  },
  "examples": [
    {
      "candidate_item_title": "With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigati...",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "near_duplicate",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Both announce the same Codex Chrome extension.",
      "secondary_roles": [],
      "should_fold": true,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "confidence": 0.9,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "same_product_different_event",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Describes a different feature of Codex, not the extension release.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Nuclear power plants were always ultra-safe as well; total global deaths from civilian nuclear power...",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Unrelated topic about Utah data centers.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Concerning.",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Unrelated topic about Utah data center opposition.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Interesting.",
      "confidence": 0.9,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Generic quote tweet, unrelated to Codex.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "原文：https://t.co/pVTjim12Ce 翻译：https://t.co/BhYuEybcTW",
      "confidence": 0.95,
      "new_item_title": "Codex now works directly in Chrome on macOS and Windows. It’s even better at working with apps and ...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:50+00:00",
      "reason": "Unrelated translation of Vercel AI Gateway blog.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "With the new Chrome extension, Codex can quickly move through repetitive browser work, like navigati...",
      "confidence": 0.9,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "same_product_different_event",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "Codex Chrome extension release vs. tool selection feature",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Nuclear power plants were always ultra-safe as well; total global deaths from civilian nuclear power...",
      "confidence": 0.95,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "Unrelated data center safety debate",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "Concerning.",
      "confidence": 0.95,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "Unrelated funding allegation about data centers",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    },
    {
      "candidate_item_title": "If Luigi knows you, there’s a good chance a box is headed to your desk soon",
      "confidence": 0.95,
      "new_item_title": "If a task needs multiple tools, Codex chooses the best one for each step. It uses plugins when they...",
      "primary_relation": "different",
      "published_at": "2026-05-07T20:08:51+00:00",
      "reason": "NVIDIA radio astronomy kit unrelated to Codex",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-openai-openai"
    }
  ],
  "near_duplicate": 1,
  "related_with_new_info": 0
}
```

## 9. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 5
  },
  "attached_existing_clusters": 0,
  "avg_confidence": 0.6,
  "avg_items_per_cluster": 1.0,
  "candidate_clusters_considered": 5,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "Codex chooses best tool for each step",
      "core_facts": [
        "Codex selects the best tool for each step in multi-tool tasks, using plugins, Chrome, or combinations as needed."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3da0bc512af944e09fe36e241aa68eb6"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Vercel releases LLM consumption report",
      "core_facts": [
        "Vercel analyzed 200k projects and 10 trillion tokens over 7 months. Key findings: Anthropic 61% cost share, Google 38% token share; B2B produces 29.7% tokens but 40.7% cost; agent requests doubled from 31.6% to 58.9% in 6 months, consuming 2.6x tokens per request; large teams use 35 models on average."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5d7e3ddc96c9459e93f96a3bb6de5a6f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Stelline Developer Kit ships to scientists",
      "core_facts": [
        "NVIDIA AI announces Stelline Developer Kit, based on DGX Spark, for GPU-accelerated signal processing in radio astronomy. First units shipping to scientists."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_dbd9212304e94d388c4ba4d55d47b9ca"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Notion launches Developer Platform",
      "core_facts": [
        "Notion announced Developer Platform including CLI (ntn), Workers, database sync, agent tools, webhooks, External Agents API, and Agents SDK."
      ],
      "item_count": 1,
      "known_angles": [
        "Orange.ai comments that Notion finally has a CLI."
      ],
      "representative_items": [
        "item_b00357ca5f6c4133a875723a6f8ac837"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "上海电信推出 Token 话费套餐",
      "core_facts": [
        "上海电信将 Token 做成话费套餐，1元=25万token，支持30+大模型，话费账单支付，上海电信用户免费领2500万额度点。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_1884f9d6f83b413cbe182ce21bb4bf28"
      ]
    }
  ],
  "created_clusters": 5,
  "effective_multi_item_cluster_count": 0,
  "follow_up_event": {
    "false": 5
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 0,
  "relations": {
    "new_info": 3,
    "source_material": 2
  },
  "reported_multi_item_cluster_count": 0,
  "reviewed_multi_item_cluster_count": 0,
  "same_event": {
    "true": 5
  },
  "same_topic": {
    "true": 5
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 5,
  "suspect_multi_item_cluster_count": 0,
  "top_clusters": [
    {
      "cluster_id": "cluster_6e6de02e221f49e88efffbf1ee94df9f",
      "cluster_title": "Codex chooses best tool for each step",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_0a84f34fe8004fab9c61b52e56e30bac",
      "cluster_title": "Vercel releases LLM consumption report",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_f614f318e1614c7298a689d366563ac8",
      "cluster_title": "Stelline Developer Kit ships to scientists",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_8162820579e644118ee11fe042db36a8",
      "cluster_title": "Notion launches Developer Platform",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_bf8c21d8a9bd44cfb83286e629e2188a",
      "cluster_title": "上海电信推出 Token 话费套餐",
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
      "cluster_title": "Codex chooses best tool for each step",
      "core_facts": [
        "Codex selects the best tool for each step in multi-tool tasks, using plugins, Chrome, or combinations as needed."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3da0bc512af944e09fe36e241aa68eb6"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Vercel releases LLM consumption report",
      "core_facts": [
        "Vercel analyzed 200k projects and 10 trillion tokens over 7 months. Key findings: Anthropic 61% cost share, Google 38% token share; B2B produces 29.7% tokens but 40.7% cost; agent requests doubled from 31.6% to 58.9% in 6 months, consuming 2.6x tokens per request; large teams use 35 models on average."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_5d7e3ddc96c9459e93f96a3bb6de5a6f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Stelline Developer Kit ships to scientists",
      "core_facts": [
        "NVIDIA AI announces Stelline Developer Kit, based on DGX Spark, for GPU-accelerated signal processing in radio astronomy. First units shipping to scientists."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_dbd9212304e94d388c4ba4d55d47b9ca"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Notion launches Developer Platform",
      "core_facts": [
        "Notion announced Developer Platform including CLI (ntn), Workers, database sync, agent tools, webhooks, External Agents API, and Agents SDK."
      ],
      "item_count": 1,
      "known_angles": [
        "Orange.ai comments that Notion finally has a CLI."
      ],
      "representative_items": [
        "item_b00357ca5f6c4133a875723a6f8ac837"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "上海电信推出 Token 话费套餐",
      "core_facts": [
        "上海电信将 Token 做成话费套餐，1元=25万token，支持30+大模型，话费账单支付，上海电信用户免费领2500万额度点。"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_1884f9d6f83b413cbe182ce21bb4bf28"
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
  "stage_budget_profile": "phase1_3_advisory",
  "stages": {
    "cluster_card_patch": {
      "budget": 8400,
      "calls": 3,
      "consumed_tokens": 6158,
      "remaining_budget": 2242,
      "skipped": 5,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 40800,
      "calls": 3,
      "consumed_tokens": 14920,
      "remaining_budget": 25880,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_cluster_relation": {
      "budget": 30000,
      "calls": 1,
      "consumed_tokens": 5038,
      "remaining_budget": 24962,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_relation": {
      "budget": 37200,
      "calls": 5,
      "consumed_tokens": 17911,
      "remaining_budget": 19289,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "source_profile": {
      "budget": 3600,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 3600,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 120000
}
```

## 12. Cost / Yield

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 20829.7,
    "cache_hit_tokens": 2944,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 8689,
    "llm_call_count": 3,
    "operation_count": 3,
    "output_tokens": 6231,
    "p50_latency_ms": 22659,
    "p95_latency_ms": 27558,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 3,
    "task_type": "item_card",
    "total_tokens": 14920
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 13011.6,
    "cache_hit_tokens": 5120,
    "cache_miss_tokens": 0,
    "calls": 5,
    "failed": 0,
    "input_tokens": 11119,
    "llm_call_count": 5,
    "operation_count": 5,
    "output_tokens": 6792,
    "p50_latency_ms": 12510,
    "p95_latency_ms": 17674,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 5,
    "task_type": "item_relation",
    "total_tokens": 17911
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 22973.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 1,
    "failed": 0,
    "input_tokens": 3143,
    "llm_call_count": 1,
    "operation_count": 1,
    "output_tokens": 1895,
    "p50_latency_ms": 22973,
    "p95_latency_ms": 22973,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 1,
    "task_type": "item_cluster_relation",
    "total_tokens": 5038
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9122.3,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3793,
    "llm_call_count": 3,
    "operation_count": 8,
    "output_tokens": 2365,
    "p50_latency_ms": 8883,
    "p95_latency_ms": 13245,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 5,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6158
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
    "cluster_title": "Codex chooses best tool for each step",
    "core_facts": [
      "Codex selects the best tool for each step in multi-tool tasks, using plugins, Chrome, or combinations as needed."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_3da0bc512af944e09fe36e241aa68eb6"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Vercel releases LLM consumption report",
    "core_facts": [
      "Vercel analyzed 200k projects and 10 trillion tokens over 7 months. Key findings: Anthropic 61% cost share, Google 38% token share; B2B produces 29.7% tokens but 40.7% cost; agent requests doubled from 31.6% to 58.9% in 6 months, consuming 2.6x tokens per request; large teams use 35 models on average."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_5d7e3ddc96c9459e93f96a3bb6de5a6f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Stelline Developer Kit ships to scientists",
    "core_facts": [
      "NVIDIA AI announces Stelline Developer Kit, based on DGX Spark, for GPU-accelerated signal processing in radio astronomy. First units shipping to scientists."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_dbd9212304e94d388c4ba4d55d47b9ca"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Notion launches Developer Platform",
    "core_facts": [
      "Notion announced Developer Platform including CLI (ntn), Workers, database sync, agent tools, webhooks, External Agents API, and Agents SDK."
    ],
    "item_count": 1,
    "known_angles": [
      "Orange.ai comments that Notion finally has a CLI."
    ],
    "representative_items": [
      "item_b00357ca5f6c4133a875723a6f8ac837"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "上海电信推出 Token 话费套餐",
    "core_facts": [
      "上海电信将 Token 做成话费套餐，1元=25万token，支持30+大模型，话费账单支付，上海电信用户免费领2500万额度点。"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_1884f9d6f83b413cbe182ce21bb4bf28"
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
    "socialmedia-ai-will-financeyf5": 3829,
    "socialmedia-marc-andreessen-127482-127480-pmarca": 0,
    "socialmedia-nvidia-ai-nvidiaai": 1684,
    "socialmedia-openai-openai": 15527,
    "socialmedia-orange-ai-oran-ge": 4474,
    "socialmedia-vista8": 3593
  },
  "low_candidates": [],
  "pending_reviews_created": 0,
  "pending_reviews_created_all_types": 18,
  "reviews_suppressed_due_to_insufficient_data": 6,
  "sources_recomputed": 6,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3829,
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
      "total_items": 1,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 1684,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 15527,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4474,
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
      "total_items": 8,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3593,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-vista8",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3829,
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
      "total_items": 1,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 1684,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 15527,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4474,
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
      "total_items": 8,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3593,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-vista8",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 1684,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 15527,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4474,
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
      "total_items": 8,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3593,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-vista8",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3829,
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
      "total_items": 1,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 1684,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 15527,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4474,
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
      "total_items": 8,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3593,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-vista8",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3829,
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
      "total_items": 1,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 1684,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 15527,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.3333333333333333,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-openai-openai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 4474,
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
      "total_items": 8,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3593,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-vista8",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 3829,
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
      "total_items": 1,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    },
    {
      "created_at": "2026-05-17T15:33:56.165955+00:00",
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
      "total_items": 4,
      "updated_at": "2026-05-17T15:33:56.165955+00:00"
    }
  ]
}
```

## 15. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 20829.7,
    "cache_hit_tokens": 2944,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 8689,
    "llm_call_count": 3,
    "operation_count": 3,
    "output_tokens": 6231,
    "p50_latency_ms": 22659,
    "p95_latency_ms": 27558,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 3,
    "task_type": "item_card",
    "total_tokens": 14920
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 13011.6,
    "cache_hit_tokens": 5120,
    "cache_miss_tokens": 0,
    "calls": 5,
    "failed": 0,
    "input_tokens": 11119,
    "llm_call_count": 5,
    "operation_count": 5,
    "output_tokens": 6792,
    "p50_latency_ms": 12510,
    "p95_latency_ms": 17674,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 5,
    "task_type": "item_relation",
    "total_tokens": 17911
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 22973.0,
    "cache_hit_tokens": 0,
    "cache_miss_tokens": 0,
    "calls": 1,
    "failed": 0,
    "input_tokens": 3143,
    "llm_call_count": 1,
    "operation_count": 1,
    "output_tokens": 1895,
    "p50_latency_ms": 22973,
    "p95_latency_ms": 22973,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 0,
    "success": 1,
    "task_type": "item_cluster_relation",
    "total_tokens": 5038
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 9122.3,
    "cache_hit_tokens": 1536,
    "cache_miss_tokens": 0,
    "calls": 3,
    "failed": 0,
    "input_tokens": 3793,
    "llm_call_count": 3,
    "operation_count": 8,
    "output_tokens": 2365,
    "p50_latency_ms": 8883,
    "p95_latency_ms": 13245,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 5,
    "success": 3,
    "task_type": "cluster_card_patch",
    "total_tokens": 6158
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
  "actual_calls": 12,
  "actual_tokens": 44027,
  "avg_latency_ms": 14823.9,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 9122.3,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 8883,
      "p95_latency_ms": 13245,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6158
    },
    "cluster_card_rebuild": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 3,
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
      "avg_latency_ms": 20829.7,
      "cache_hit_tokens": 2944,
      "calls": 3,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 22659,
      "p95_latency_ms": 27558,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "item_card",
      "total_tokens": 14920
    },
    "item_cluster_relation": {
      "avg_latency_ms": 22973.0,
      "cache_hit_tokens": 0,
      "calls": 1,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 22973,
      "p95_latency_ms": 22973,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 1,
      "task_type": "item_cluster_relation",
      "total_tokens": 5038
    },
    "item_relation": {
      "avg_latency_ms": 13011.6,
      "cache_hit_tokens": 5120,
      "calls": 5,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 12510,
      "p95_latency_ms": 17674,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 5,
      "task_type": "item_relation",
      "total_tokens": 17911
    },
    "json_repair": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 3,
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
      "concurrency": 3,
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
  "cache_hit_rate": 0.218,
  "cache_hit_tokens": 9600,
  "calls_per_sec": 0.1097,
  "db_lock_errors": 0,
  "duration_seconds": 109.382,
  "final_failures": 0,
  "max_concurrency": 3,
  "p50_latency_ms": 13245,
  "p95_latency_ms": 22973,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 0,
  "tokens_per_sec": 402.51
}
```

## 17. Stage Budget Summary

```json
{
  "downstream_starved": false,
  "stage_budget_profile": "phase1_3_advisory",
  "stages": {
    "cluster_card_patch": {
      "budget": 8400,
      "calls": 3,
      "consumed_tokens": 6158,
      "remaining_budget": 2242,
      "skipped": 5,
      "skipped_due_to_budget": 0
    },
    "item_card": {
      "budget": 40800,
      "calls": 3,
      "consumed_tokens": 14920,
      "remaining_budget": 25880,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_cluster_relation": {
      "budget": 30000,
      "calls": 1,
      "consumed_tokens": 5038,
      "remaining_budget": 24962,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "item_relation": {
      "budget": 37200,
      "calls": 5,
      "consumed_tokens": 17911,
      "remaining_budget": 19289,
      "skipped": 0,
      "skipped_due_to_budget": 0
    },
    "source_profile": {
      "budget": 3600,
      "calls": 0,
      "consumed_tokens": 0,
      "remaining_budget": 3600,
      "skipped": 0,
      "skipped_due_to_budget": 0
    }
  },
  "total_token_budget": 120000
}
```

## 18. Errors / Fallbacks / Retries

```json
{
  "db_lock_errors": 0,
  "failed_batch_count": 0,
  "fallback_rate": 0.0,
  "final_failures": 0,
  "heuristic_fallback_count": 0,
  "item_card_count": 20,
  "llm_card_count": 3,
  "llm_parse_failures": 0,
  "repair_retry_count": 0,
  "review_queue_entries_due_to_failure": 0,
  "single_retry_success_count": 0,
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
    "concurrency": 3,
    "iteration": "phase1_2f",
    "max_calls": 120,
    "max_items": 20,
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
      "name": "chinese_event_detection_rate",
      "passed": false,
      "reason": "Chinese event-like items must not all be rejected",
      "threshold": ">= 0.5",
      "value": 0.2
    },
    {
      "name": "effective_multi_item_clusters",
      "passed": false,
      "reason": "dry-run produced useful same-event clusters",
      "threshold": ">= 1",
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
      "value": 1.0
    },
    {
      "name": "chinese_event_detection_rate",
      "passed": false,
      "reason": "Chinese event-like items must not all be rejected",
      "threshold": ">= 0.5",
      "value": 0.2
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
      "passed": false,
      "reason": "dry-run produced useful same-event clusters",
      "threshold": ">= 1",
      "value": 0
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
  "actual_calls": 12,
  "actual_tokens": 44027,
  "avg_latency_ms": 14823.9,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 9122.3,
      "cache_hit_tokens": 1536,
      "calls": 3,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 8883,
      "p95_latency_ms": 13245,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "cluster_card_patch",
      "total_tokens": 6158
    },
    "cluster_card_rebuild": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 3,
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
      "avg_latency_ms": 20829.7,
      "cache_hit_tokens": 2944,
      "calls": 3,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 22659,
      "p95_latency_ms": 27558,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 3,
      "task_type": "item_card",
      "total_tokens": 14920
    },
    "item_cluster_relation": {
      "avg_latency_ms": 22973.0,
      "cache_hit_tokens": 0,
      "calls": 1,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 22973,
      "p95_latency_ms": 22973,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 1,
      "task_type": "item_cluster_relation",
      "total_tokens": 5038
    },
    "item_relation": {
      "avg_latency_ms": 13011.6,
      "cache_hit_tokens": 5120,
      "calls": 5,
      "concurrency": 3,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 12510,
      "p95_latency_ms": 17674,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 5,
      "task_type": "item_relation",
      "total_tokens": 17911
    },
    "json_repair": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 3,
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
      "concurrency": 3,
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
  "cache_hit_rate": 0.218,
  "cache_hit_tokens": 9600,
  "calls_per_sec": 0.1097,
  "db_lock_errors": 0,
  "duration_seconds": 109.382,
  "final_failures": 0,
  "max_concurrency": 3,
  "p50_latency_ms": 13245,
  "p95_latency_ms": 22973,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 0,
  "tokens_per_sec": 402.51
}
```

## 14. Readiness Assessment

```json
{
  "blockers": [
    {
      "name": "chinese_event_detection_rate",
      "passed": false,
      "reason": "Chinese event-like items must not all be rejected",
      "threshold": ">= 0.5",
      "value": 0.2
    },
    {
      "name": "effective_multi_item_clusters",
      "passed": false,
      "reason": "dry-run produced useful same-event clusters",
      "threshold": ">= 1",
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
      "value": 1.0
    },
    {
      "name": "chinese_event_detection_rate",
      "passed": false,
      "reason": "Chinese event-like items must not all be rejected",
      "threshold": ">= 0.5",
      "value": 0.2
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
      "passed": false,
      "reason": "dry-run produced useful same-event clusters",
      "threshold": ">= 1",
      "value": 0
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
