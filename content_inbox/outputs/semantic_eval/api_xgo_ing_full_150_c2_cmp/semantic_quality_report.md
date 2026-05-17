# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 44,
  "actual_tokens": 206094,
  "batch_size": 5,
  "cache_hit_tokens": 38016,
  "cache_miss_tokens": 0,
  "concurrency": 2,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 594.173,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_2b9x8xk8.sqlite3",
  "finished_at": "2026-05-16T18:27:31.904846+00:00",
  "git_commit": "038fec7dcde63c6e80bf9ff73031abfaafb9c25b",
  "include_archived": false,
  "items_sampled": 150,
  "live": true,
  "max_calls": 350,
  "max_candidates": 5,
  "max_items": 150,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260516_181737_691142",
  "sample_mode": "source_scope_full",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "started_at": "2026-05-16T18:17:37.691142+00:00",
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
  "matched_source_count": 147,
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "sources": [
    {
      "feed_url": "https://api.xgo.ing/rss/user/05f1492e43514dc3862a076d3697c390",
      "item_count": 25,
      "latest_item_time": "2026-05-15T19:17:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-nvidia-ai-nvidiaai",
      "source_name": "NVIDIA AI(@NVIDIAAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0277b0bbefd54df7bc6b7880122da8f7",
      "item_count": 25,
      "latest_item_time": "2026-05-16T10:18:27+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-orange-ai-oran-ge",
      "source_name": "orange.ai(@oran_ge)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/74e542992cf7441390c708f5601071d4",
      "item_count": 7,
      "latest_item_time": "2026-05-04T13:27:27+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-imxiaohu",
      "source_name": "小互(@imxiaohu)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/082097117b4543e9a741cd2580f936d3",
      "item_count": 7,
      "latest_item_time": "2026-04-24T07:24:53+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-junyang-lin-justinlin610",
      "source_name": "Junyang Lin(@JustinLin610)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/179bcc4b8e5d4274b6e9e935f9fd4434",
      "item_count": 6,
      "latest_item_time": "2026-05-05T06:23:31+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-aadit-sheth-aaditsh",
      "source_name": "Aadit Sheth(@aaditsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0e3ebaf288014c45b0d24b71fe37312b",
      "item_count": 6,
      "latest_item_time": "2026-04-27T11:31:05+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_name": "AI Breakfast(@AiBreakfast)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/22af005b21ec45b1a4503acca777b7f0",
      "item_count": 6,
      "latest_item_time": "2026-03-10T20:50:07+00:00",
      "sampled_item_count": 6,
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_name": "AI SDK(@aisdk)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/08b5488b20bc437c8bfc317a52e5c26d",
      "item_count": 6,
      "latest_item_time": "2026-04-30T16:21:35+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_name": "Andrew Ng(@AndrewYNg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0be252fedbe84ad7bea21be44b18da89",
      "item_count": 6,
      "latest_item_time": "2026-04-30T19:00:00+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-dify-dify-ai",
      "source_name": "Dify(@dify_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/1897eed387064dfab443764d6da50bc6",
      "item_count": 6,
      "latest_item_time": "2026-05-01T11:13:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-elevenlabs-elevenlabsio",
      "source_name": "ElevenLabs(@elevenlabsio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/221a88341acb475db221a12fed8208d0",
      "item_count": 6,
      "latest_item_time": "2026-04-30T17:30:36+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-notebooklm-notebooklm",
      "source_name": "NotebookLM(@NotebookLM)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/0c0856a69f9f49cf961018c32a0b0049",
      "item_count": 6,
      "latest_item_time": "2026-05-07T17:19:33+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-openai-openai",
      "source_name": "OpenAI(@OpenAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/17687b1051204b2dbaed4ea4c9178f28",
      "item_count": 6,
      "latest_item_time": "2026-05-02T04:37:44+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-poe-poe-platform",
      "source_name": "Poe(@poe_platform)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/12eba9c3db4940c5ab2a72bd00f9ff2c",
      "item_count": 6,
      "latest_item_time": "2026-04-30T14:02:05+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-replicate-replicate",
      "source_name": "Replicate(@replicate)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3953aa71e87a422eb9d7bf6ff1c7c43e",
      "item_count": 6,
      "latest_item_time": "2026-05-04T23:05:58+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-xai-xai",
      "source_name": "xAI(@xai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f3fedf817599470dbf8d8d11f0872475",
      "item_count": 5,
      "latest_item_time": "2026-05-04T21:00:03+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-a16z-a16z",
      "source_name": "a16z(@a16z)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3042b6f912b24f64982cc23f7bd59681",
      "item_count": 5,
      "latest_item_time": "2026-04-28T15:15:29+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_name": "Adam D'Angelo(@adamdangelo)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7d19a619a1cc4a9896129211269d2c85",
      "item_count": 5,
      "latest_item_time": "2026-05-04T22:34:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-engineer-aidotengineer",
      "source_name": "AI Engineer(@aiDotEngineer)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/aa74321087f9405a872fd9a76b743bf8",
      "item_count": 5,
      "latest_item_time": "2026-05-04T12:21:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ai-will-financeyf5",
      "source_name": "AI Will(@FinanceYF5)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/341f7b9f8d9b477e8bb200caa7f32c6e",
      "item_count": 5,
      "latest_item_time": "2026-05-04T21:27:41+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ak-akhaliq",
      "source_name": "AK(@_akhaliq)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3434c0d56ee0446f991fb6af42bfac4b",
      "item_count": 5,
      "latest_item_time": "2026-05-04T19:44:40+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-akshay-kothari-akothari",
      "source_name": "Akshay Kothari(@akothari)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/524525de0d69407b80f0a7d891fdc8df",
      "item_count": 5,
      "latest_item_time": "2026-04-20T17:19:14+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-alex-albert-alexalbert",
      "source_name": "Alex Albert(@alexalbert__)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a02496979a0e4d86baf2b72c24db52a4",
      "item_count": 5,
      "latest_item_time": "2026-03-24T23:59:57+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_name": "Aman Sanger(@amanrsanger)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fb1814c610c4af2911caa98c5c5ef82",
      "item_count": 5,
      "latest_item_time": "2026-05-05T03:57:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-amjad-masad-amasad",
      "source_name": "Amjad Masad(@amasad)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/edf707b5c0b248579085f66d7a3c5524",
      "item_count": 5,
      "latest_item_time": "2026-04-30T17:43:06+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_name": "Andrej Karpathy(@karpathy)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a3eb6beb2d894da3a9b7ab6d2e46790e",
      "item_count": 5,
      "latest_item_time": "2026-05-01T23:26:59+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-andrew-chen-andrewchen",
      "source_name": "andrew chen(@andrewchen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fc28a211471b496682feff329ec616e5",
      "item_count": 5,
      "latest_item_time": "2026-04-30T19:03:27+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-anthropic-anthropicai",
      "source_name": "Anthropic(@AnthropicAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5f13b32b124a41cfb659f903a84032b1",
      "item_count": 5,
      "latest_item_time": "2026-05-04T10:49:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-anton-osika-eu-acc-antonosika",
      "source_name": "Anton Osika – eu/acc(@antonosika)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/59e6b63ae9684d11be0ae13d9e7420f2",
      "item_count": 5,
      "latest_item_time": "2026-05-04T18:20:23+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-aravind-srinivas-aravsrinivas",
      "source_name": "Aravind Srinivas(@AravSrinivas)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d8121d969fb34c7daad2dd2aac4ba270",
      "item_count": 5,
      "latest_item_time": "2026-03-16T23:24:00+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_name": "Arthur Mensch(@arthurmensch)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e153fdd077df458b8298d975c060dcc3",
      "item_count": 5,
      "latest_item_time": "2026-05-04T23:25:51+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-augment-code-augmentcode",
      "source_name": "Augment Code(@augmentcode)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6bbf31cac345443585c3280320ba9009",
      "item_count": 5,
      "latest_item_time": "2026-04-29T15:45:00+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-berkeley-ai-research-berkeley-ai",
      "source_name": "Berkeley AI Research(@berkeley_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f54b2b40185943ce8f48a880110b7bc2",
      "item_count": 5,
      "latest_item_time": "2026-04-22T02:10:13+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-binyuan-hui-huybery",
      "source_name": "Binyuan Hui(@huybery)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/760ab7cd9708452c9ce1f9144b92a430",
      "item_count": 5,
      "latest_item_time": "2026-04-30T23:30:36+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-bolt-new-boltdotnew",
      "source_name": "bolt.new(@boltdotnew)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b8d7530f0b294405825013bbc1cc198f",
      "item_count": 5,
      "latest_item_time": "2026-05-05T01:47:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-browser-use-browser-use",
      "source_name": "Browser Use(@browser_use)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/66a6b39ddcfa42e39621e0ab293c1bdd",
      "item_count": 5,
      "latest_item_time": "2026-04-30T21:29:34+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cat-catwu",
      "source_name": "cat(@_catwu)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3877c31cdb554cffb750b3b683c98c4d",
      "item_count": 5,
      "latest_item_time": "2026-04-30T21:37:28+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-character-ai-character-ai",
      "source_name": "Character.AI(@character_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f7992687b8d74b14bf2341eb3a0a5ec4",
      "item_count": 5,
      "latest_item_time": "2026-05-04T20:20:08+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-chatgpt-chatgptapp",
      "source_name": "ChatGPT(@ChatGPTapp)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4cc14cbd15c74e189d537c415369e1a7",
      "item_count": 5,
      "latest_item_time": "2026-05-01T17:48:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cognition-cognition-labs",
      "source_name": "Cognition(@cognition_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/462aa134ed914f98b3491680ad9b36ed",
      "item_count": 5,
      "latest_item_time": "2026-04-30T13:11:45+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cohere-cohere",
      "source_name": "cohere(@cohere)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5287b4e0e13a4ab7ab7b1d56f9d88960",
      "item_count": 5,
      "latest_item_time": "2026-05-02T19:46:40+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-cursor-cursor-ai",
      "source_name": "Cursor(@cursor_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/49666ce6fe3e4cb786c6574684542ec5",
      "item_count": 5,
      "latest_item_time": "2026-04-07T18:14:19+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-dario-amodei-darioamodei",
      "source_name": "Dario Amodei(@DarioAmodei)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/42e6b4901b97498eab2ab64c07d56177",
      "item_count": 5,
      "latest_item_time": "2026-05-01T00:09:55+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-deeplearning-ai-deeplearningai",
      "source_name": "DeepLearning.AI(@DeepLearningAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/68b610deb24b47ae9a236811563cda86",
      "item_count": 5,
      "latest_item_time": "2026-04-29T02:20:52+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-deepseek-deepseek-ai",
      "source_name": "DeepSeek(@deepseek_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4a884d5e2f3740c5a26c9c093de6388a",
      "item_count": 5,
      "latest_item_time": "2026-05-02T11:34:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-demis-hassabis-demishassabis",
      "source_name": "Demis Hassabis(@demishassabis)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6384ee3c656c48fea5e8b3cdacece4d0",
      "item_count": 5,
      "latest_item_time": "2026-03-26T17:03:19+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-dia-diabrowser",
      "source_name": "Dia(@diabrowser)"
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
      "feed_url": "https://api.xgo.ing/rss/user/931d6e88e067496cac6bf23f69d60f33",
      "item_count": 5,
      "latest_item_time": "2026-05-04T21:05:55+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-elvis-omarsar0",
      "source_name": "elvis(@omarsar0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ddfdcdd4e390495c942f0b5da62af0fb",
      "item_count": 5,
      "latest_item_time": "2026-05-05T02:41:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-eric-jing-ericjing-ai",
      "source_name": "Eric Jing(@ericjing_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/65f321be670b4ffba7f40d0afd38c94d",
      "item_count": 5,
      "latest_item_time": "2026-05-04T11:01:36+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-eric-zakariasson-ericzakariasson",
      "source_name": "eric zakariasson(@ericzakariasson)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a4bfe44bfc0d4c949da21ebd3f5f42a5",
      "item_count": 5,
      "latest_item_time": "2026-04-07T16:48:36+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_name": "Fei-Fei Li(@drfeifei)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/326763c2f6154826babcfd71c5ab0f70",
      "item_count": 5,
      "latest_item_time": "2026-05-01T16:35:17+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-fellou-fellouai",
      "source_name": "Fellou(@FellouAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f8a106a09a7d404fb8de7eb0c5ddd2a2",
      "item_count": 5,
      "latest_item_time": "2026-05-04T16:33:18+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-figma-figma",
      "source_name": "Figma(@figma)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c04abb206bbf4f91b22795024d6c0614",
      "item_count": 5,
      "latest_item_time": "2026-05-04T23:14:12+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-firecrawl-firecrawl-dev",
      "source_name": "Firecrawl(@firecrawl_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/9f35c76341554bd78c2b9e63dc4fa5d8",
      "item_count": 5,
      "latest_item_time": "2026-05-04T18:45:40+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-fireworks-ai-fireworksai-hq",
      "source_name": "Fireworks AI(@FireworksAI_HQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4900b3dcd592424687582ff9e0f148ea",
      "item_count": 5,
      "latest_item_time": "2026-04-29T10:59:12+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_name": "Fish Audio(@FishAudio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/be74da51698d4cefb12b39830d6cd201",
      "item_count": 5,
      "latest_item_time": "2026-03-16T20:10:48+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-flowiseai-flowiseai",
      "source_name": "FlowiseAI(@FlowiseAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/35a38c5646d946fb894d8c30c1d9629e",
      "item_count": 5,
      "latest_item_time": "2026-05-05T03:08:36+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-gary-marcus-garymarcus",
      "source_name": "Gary Marcus(@GaryMarcus)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/71ffd342cb5d478185ef7d55bdfca011",
      "item_count": 5,
      "latest_item_time": "2026-05-05T02:48:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-genspark-genspark-ai",
      "source_name": "Genspark(@genspark_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/cb6169815e2e447e8e6148a4af3f9686",
      "item_count": 5,
      "latest_item_time": "2026-05-01T17:33:11+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_name": "Geoffrey Hinton(@geoffreyhinton)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/69d925d4a8d44221b03eecbe07bd0f74",
      "item_count": 5,
      "latest_item_time": "2026-05-04T23:11:31+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-ai-developers-googleaidevs",
      "source_name": "Google AI Developers(@googleaidevs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4de0bd2d5cef4333a0260dc8157054a7",
      "item_count": 5,
      "latest_item_time": "2026-05-01T16:10:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-ai-googleai",
      "source_name": "Google AI(@GoogleAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a99538443a484fcc846bdcc8f50745ec",
      "item_count": 5,
      "latest_item_time": "2026-05-01T16:01:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-deepmind-googledeepmind",
      "source_name": "Google DeepMind(@GoogleDeepMind)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6fb337feeec44ca38b79491b971d868d",
      "item_count": 5,
      "latest_item_time": "2026-05-04T18:39:22+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-google-gemini-app-geminiapp",
      "source_name": "Google Gemini App(@GeminiApp)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/af19d054e26a49129f23abfa82d9e268",
      "item_count": 5,
      "latest_item_time": "2026-05-04T13:48:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-greg-brockman-gdb",
      "source_name": "Greg Brockman(@gdb)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/771b32075fe54a83bdb6966de9647b4f",
      "item_count": 5,
      "latest_item_time": "2026-02-18T22:04:39+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_name": "Groq Inc(@GroqInc)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e8750659b8154dbfa0489f451e044af1",
      "item_count": 5,
      "latest_item_time": "2026-05-04T19:41:40+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-guillermo-rauch-rauchg",
      "source_name": "Guillermo Rauch(@rauchg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/831fac36aa0a49a9af79f35dc1c9b5d9",
      "item_count": 5,
      "latest_item_time": "2026-05-04T04:52:12+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-guizang-ai-op7418",
      "source_name": "歸藏(guizang.ai)(@op7418)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e65b5e59fcb544918c1ba17f5758f0f8",
      "item_count": 5,
      "latest_item_time": "2026-05-02T17:39:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-hailuo-ai-minimax-hailuo-ai",
      "source_name": "Hailuo AI (MiniMax)(@Hailuo_AI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f299207df53745bca04a03db8d11c5aa",
      "item_count": 5,
      "latest_item_time": "2026-05-04T18:02:27+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-harrison-chase-hwchase17",
      "source_name": "Harrison Chase(@hwchase17)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a9aff6b016c143ed8728dd86eb70d7db",
      "item_count": 5,
      "latest_item_time": "2026-05-04T23:05:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-heygen-heygen-official",
      "source_name": "HeyGen(@HeyGen_Official)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6e8e7b42cb434818810f87bcf77d86fb",
      "item_count": 5,
      "latest_item_time": "2026-04-29T13:55:43+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-hunyuan-txhunyuan",
      "source_name": "Hunyuan(@TXhunyuan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/57831559d22440debbfb2f2528e4ba84",
      "item_count": 5,
      "latest_item_time": "2026-04-09T18:58:45+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_name": "Ian Goodfellow(@goodfellow_ian)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a719880fe66e4156a111187f50dae91b",
      "item_count": 5,
      "latest_item_time": "2026-04-22T16:46:12+00:00",
      "sampled_item_count": 1,
      "source_id": "socialmedia-ideogram-ideogram-ai",
      "source_name": "Ideogram(@ideogram_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dceb5cd131b34c72a8376cba8ea5d864",
      "item_count": 5,
      "latest_item_time": "2026-04-14T19:43:38+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-jan-leike-janleike",
      "source_name": "Jan Leike(@janleike)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b1013166769c49f8aa3fbdc222867054",
      "item_count": 5,
      "latest_item_time": "2026-04-28T20:16:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jeff-dean-jeffdean",
      "source_name": "Jeff Dean(@JeffDean)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b3d904c0d7c446558ef3a1e7f2eb362b",
      "item_count": 5,
      "latest_item_time": "2026-05-05T02:49:49+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-jerry-liu-jerryjliu0",
      "source_name": "Jerry Liu(@jerryjliu0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c6cfe7c0d6b74849997073233fdea840",
      "item_count": 5,
      "latest_item_time": "2026-04-01T15:15:09+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-jim-fan-drjimfan",
      "source_name": "Jim Fan(@DrJimFan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f510f6e7eecf456ca7e2895a46752888",
      "item_count": 5,
      "latest_item_time": "2026-03-13T12:29:21+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-jina-ai-jinaai",
      "source_name": "Jina AI(@JinaAI_)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/44d9fa384087448a94d3c8595f8d535e",
      "item_count": 5,
      "latest_item_time": "2026-05-01T17:08:33+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-julien-chaumond-julien-c",
      "source_name": "Julien Chaumond(@julien_c)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/58894bf2934a426ca833c682da2bc810",
      "item_count": 5,
      "latest_item_time": "2026-05-04T20:00:13+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-justin-welsh-thejustinwelsh",
      "source_name": "Justin Welsh(@thejustinwelsh)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c61046471f174d86bc0eb76cb44a21c3",
      "item_count": 5,
      "latest_item_time": "2026-05-04T18:15:52+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-justine-moore-venturetwins",
      "source_name": "Justine Moore(@venturetwins)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/564237c3de274d58a04f064920817888",
      "item_count": 5,
      "latest_item_time": "2026-05-05T03:00:03+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-kling-ai-kling-ai",
      "source_name": "Kling AI(@Kling_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/862fee50a745423c87e2633b274caf1d",
      "item_count": 5,
      "latest_item_time": "2026-05-04T21:47:10+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-langchain-langchainai",
      "source_name": "LangChain(@LangChainAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a7be8b61a1264ea7984abfaea3eff686",
      "item_count": 5,
      "latest_item_time": "2026-05-01T04:59:53+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-latent-space-latentspacepod",
      "source_name": "Latent.Space(@latentspacepod)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dc2426bc8348495189b45451d1707a1c",
      "item_count": 5,
      "latest_item_time": "2026-05-02T23:47:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lee-robinson-leerob",
      "source_name": "Lee Robinson(@leerob)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/77d5ce4736854b0ebae603e4b54d3095",
      "item_count": 5,
      "latest_item_time": "2026-05-04T22:21:49+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lenny-rachitsky-lennysan",
      "source_name": "Lenny Rachitsky(@lennysan)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/adf65931519340f795e2336910b4cd15",
      "item_count": 5,
      "latest_item_time": "2026-04-09T17:56:46+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-lex-fridman-lexfridman",
      "source_name": "Lex Fridman(@lexfridman)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ca2fa444b6ea4b8b974fe148056e497a",
      "item_count": 5,
      "latest_item_time": "2026-05-05T03:22:45+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lijigang-com",
      "source_name": "李继刚(@lijigang_com)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a8f7e2238039461cbc8bf55f5f194498",
      "item_count": 5,
      "latest_item_time": "2026-03-10T17:08:44+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-lilian-weng-lilianweng",
      "source_name": "Lilian Weng(@lilianweng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f01b088d5a39473e854b07143df77ec5",
      "item_count": 5,
      "latest_item_time": "2026-05-01T21:55:13+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lmarena-ai-lmarena-ai",
      "source_name": "lmarena.ai(@lmarena_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4f63d960de644aeebd0aa97e4994dafe",
      "item_count": 5,
      "latest_item_time": "2026-05-04T22:53:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-logan-kilpatrick-officiallogank",
      "source_name": "Logan Kilpatrick(@OfficialLoganK)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/639cd13d44284e10ac89fbd1c5399767",
      "item_count": 5,
      "latest_item_time": "2026-05-01T09:33:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lovable-lovable-dev",
      "source_name": "Lovable(@lovable_dev)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/db648e4d4eae4822aa0d34f0faef7ad2",
      "item_count": 5,
      "latest_item_time": "2026-04-30T06:49:02+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-lovartai-lovart-ai",
      "source_name": "LovartAI(@lovart_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/320181c4651a41a08015946b55f704ab",
      "item_count": 5,
      "latest_item_time": "2026-05-01T15:16:07+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-manusai-manusai-hq",
      "source_name": "ManusAI(@ManusAI_HQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/94bb691baeff461686326af619beb116",
      "item_count": 5,
      "latest_item_time": "2026-05-01T23:08:57+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-mem0-mem0ai",
      "source_name": "mem0(@mem0ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/48aae530e0bf413aa7d44380f418e2e3",
      "item_count": 5,
      "latest_item_time": "2026-05-05T02:20:59+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-meng-shao-shao-meng",
      "source_name": "meng shao(@shao__meng)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/61f4b78554fb4b8fa5653ec5d924d15a",
      "item_count": 5,
      "latest_item_time": "2026-05-04T16:57:40+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-microsoft-research-msftresearch",
      "source_name": "Microsoft Research(@MSFTResearch)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/72dd496bfd9d44c5a5761a974630376d",
      "item_count": 5,
      "latest_item_time": "2026-04-30T22:04:00+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-midjourney-midjourney",
      "source_name": "Midjourney(@midjourney)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/424e67b19eed4500b7a440976bbd2ade",
      "item_count": 5,
      "latest_item_time": "2026-05-04T15:00:01+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-milvus-milvusio",
      "source_name": "Milvus(@milvusio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5d749cc613ec4069bb2a47334739e1b6",
      "item_count": 5,
      "latest_item_time": "2026-04-23T07:39:32+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-monica-im-hey-im-monica",
      "source_name": "Monica_IM(@hey_im_monica)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/394acfaff8c44e09936f5bc0b8504f2c",
      "item_count": 5,
      "latest_item_time": "2026-04-28T17:12:10+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-mustafa-suleyman-mustafasuleyman",
      "source_name": "Mustafa Suleyman(@mustafasuleyman)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b43bc203409e4c5a9c3ae86fe1ac00c9",
      "item_count": 5,
      "latest_item_time": "2026-05-05T03:38:58+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-naval-naval",
      "source_name": "Naval(@naval)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6ebdf0d91eef4c149acd0ef110635866",
      "item_count": 5,
      "latest_item_time": "2026-04-24T19:15:41+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-nick-st-pierre-nickfloats",
      "source_name": "Nick St. Pierre(@nickfloats)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f97a26863aec4425b021720d4f8e4ede",
      "item_count": 5,
      "latest_item_time": "2026-05-04T22:12:45+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-notion-notionhq",
      "source_name": "Notion(@NotionHQ)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6326c63a2dfa445bbde88bea0c3112c2",
      "item_count": 5,
      "latest_item_time": "2026-05-04T23:36:39+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ollama-ollama",
      "source_name": "ollama(@ollama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/971dc1fc90da449bac23e5fad8a33d55",
      "item_count": 5,
      "latest_item_time": "2026-05-05T00:08:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-openai-developers-openaidevs",
      "source_name": "OpenAI Developers(@OpenAIDevs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e503a90c035c4b1d8f8dd34907d15bf4",
      "item_count": 5,
      "latest_item_time": "2026-05-05T03:12:11+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-openrouter-openrouterai",
      "source_name": "OpenRouter(@OpenRouterAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c65c68f3713747bba863f92d6b5e996f",
      "item_count": 5,
      "latest_item_time": "2026-05-03T07:37:18+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-patrick-loeber-patloeber",
      "source_name": "Patrick Loeber(@patloeber)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b9912ac9a29042cf8c834419dc44cb1f",
      "item_count": 5,
      "latest_item_time": "2026-05-04T21:26:51+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-paul-couvert-itspaulai",
      "source_name": "Paul Couvert(@itsPaulAi)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/900549ddadf04e839d3f7a17ebaba3fc",
      "item_count": 5,
      "latest_item_time": "2026-05-04T22:07:09+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-paul-graham-paulg",
      "source_name": "Paul Graham(@paulg)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fdd601ea751949e7bec9e4cdad7c8e6c",
      "item_count": 5,
      "latest_item_time": "2026-05-04T18:06:02+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-perplexity-perplexity-ai",
      "source_name": "Perplexity(@perplexity_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ce352bbf72e44033985bc756db2ee0e2",
      "item_count": 5,
      "latest_item_time": "2026-05-04T16:15:29+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-philipp-schmid-philschmid",
      "source_name": "Philipp Schmid(@_philschmid)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/3306d8b253ec4e03aca3c2e9967e7119",
      "item_count": 5,
      "latest_item_time": "2026-05-02T01:52:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-pika-pika-labs",
      "source_name": "Pika(@pika_labs)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a55f6e33dd224235aabaabaaf9d58a06",
      "item_count": 5,
      "latest_item_time": "2026-05-04T15:00:02+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-qdrant-qdrant-engine",
      "source_name": "Qdrant(@qdrant_engine)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/80032d016d654eb4afe741ff34b7643d",
      "item_count": 5,
      "latest_item_time": "2026-05-01T15:14:01+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-qwen-alibaba-qwen",
      "source_name": "Qwen(@Alibaba_Qwen)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4838204097ed422eac24ad48e68dc3ff",
      "item_count": 5,
      "latest_item_time": "2026-05-04T15:45:26+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-ray-dalio-raydalio",
      "source_name": "Ray Dalio(@RayDalio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/acc648327c614d9b985b9fc3d737165b",
      "item_count": 5,
      "latest_item_time": "2026-05-04T11:33:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-recraft-recraftai",
      "source_name": "Recraft(@recraftai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/613f859e4bc440c5a28f40732840f5cf",
      "item_count": 5,
      "latest_item_time": "2026-05-04T21:14:46+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-replit-replit",
      "source_name": "Replit ⠕(@Replit)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/a636de3cbda0495daabd15b9fd298614",
      "item_count": 5,
      "latest_item_time": "2026-05-04T15:18:21+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-rowan-cheung-rowancheung",
      "source_name": "Rowan Cheung(@rowancheung)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e6bb4f612dd24db5bc1a6811e6dd5820",
      "item_count": 5,
      "latest_item_time": "2026-05-04T17:30:29+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-runway-runwayml",
      "source_name": "Runway(@runwayml)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baad3713defe4182844d2756b4c2c9ed",
      "item_count": 5,
      "latest_item_time": "2026-05-04T16:41:48+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-sahil-lavingia-shl",
      "source_name": "Sahil Lavingia(@shl)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/e30d4cd223f44bed9d404807105c8927",
      "item_count": 5,
      "latest_item_time": "2026-05-05T00:51:52+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-sam-altman-sama",
      "source_name": "Sam Altman(@sama)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/baa68dbd9a9e461a96fd9b2e3f35dcbf",
      "item_count": 5,
      "latest_item_time": "2026-05-02T12:11:51+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-satya-nadella-satyanadella",
      "source_name": "Satya Nadella(@satyanadella)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/5fca8ccd87344d388bc863304ed6fd86",
      "item_count": 5,
      "latest_item_time": "2026-05-04T17:57:54+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-scott-wu-scottwu46",
      "source_name": "Scott Wu(@ScottWu46)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/30ad80be93c84e44acc37d5ddf31db57",
      "item_count": 5,
      "latest_item_time": "2026-05-05T01:39:37+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-simon-willison-simonw",
      "source_name": "Simon Willison(@simonw)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/6d7d398dd80b48d79669c92745d32cf6",
      "item_count": 5,
      "latest_item_time": "2026-04-30T11:31:33+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-skywork-skywork-ai",
      "source_name": "Skywork(@Skywork_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/d5fc365556e641cba2278f501e8c6f92",
      "item_count": 5,
      "latest_item_time": "2026-04-23T07:26:58+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-stanford-ai-lab-stanfordailab",
      "source_name": "Stanford AI Lab(@StanfordAILab)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fafa6df3c67644b1a367a177240e0173",
      "item_count": 5,
      "latest_item_time": "2026-04-21T22:41:39+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-sualeh-asif-sualehasif996",
      "source_name": "Sualeh Asif(@sualehasif996)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/c961547e08df4396b3ab69367a07a1cd",
      "item_count": 5,
      "latest_item_time": "2026-03-20T14:13:18+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-suhail-suhail",
      "source_name": "Suhail(@Suhail)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8324d65a63dc42c584a8c08cc8323c9f",
      "item_count": 5,
      "latest_item_time": "2026-04-29T20:49:27+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-sundar-pichai-sundarpichai",
      "source_name": "Sundar Pichai(@sundarpichai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2de92402f4a24c90bb27e7580b93a878",
      "item_count": 5,
      "latest_item_time": "2026-04-24T21:21:51+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_name": "Taranjeet(@taranjeetio)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/83b1ea38940b4a1d81ea57d1ffb12ad7",
      "item_count": 5,
      "latest_item_time": "2026-05-04T20:03:19+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-the-rundown-ai-therundownai",
      "source_name": "The Rundown AI(@TheRundownAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4918efb13c47459b8dcaa79cfdf72d09",
      "item_count": 5,
      "latest_item_time": "2026-04-29T19:01:30+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-thomas-wolf-thom-wolf",
      "source_name": "Thomas Wolf(@Thom_Wolf)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/dbf37973e6fc4eae91d4be9669a78fc7",
      "item_count": 5,
      "latest_item_time": "2026-04-30T00:36:35+00:00",
      "sampled_item_count": 4,
      "source_id": "socialmedia-v0-v0",
      "source_name": "v0(@v0)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/7794c4268a504019a94af1778857a703",
      "item_count": 5,
      "latest_item_time": "2026-02-24T01:40:04+00:00",
      "sampled_item_count": 5,
      "source_id": "socialmedia-varun-mohan-mohansolo",
      "source_name": "Varun Mohan(@_mohansolo)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/9de19c78f7454ad08c956c1a00d237fe",
      "item_count": 5,
      "latest_item_time": "2026-05-05T01:39:10+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-vista8",
      "source_name": "向阳乔木(@vista8)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/2f1035ec6b28475987af06b600e1d04c",
      "item_count": 5,
      "latest_item_time": "2026-04-30T16:02:39+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-weaviate-vector-database-weaviate-io",
      "source_name": "Weaviate • vector database(@weaviate_io)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4a8273800ed34a069eecdb6c5c1b9ccf",
      "item_count": 5,
      "latest_item_time": "2026-04-30T17:14:35+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-windsurf-windsurf-ai",
      "source_name": "Windsurf(@windsurf_ai)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/b1ab109f6afd42ab8ea32e17a19a3a3e",
      "item_count": 5,
      "latest_item_time": "2026-05-04T22:44:52+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-y-combinator-ycombinator",
      "source_name": "Y Combinator(@ycombinator)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/f5f4f928dede472ea55053672ad27ab6",
      "item_count": 5,
      "latest_item_time": "2026-05-04T16:44:38+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-yann-lecun-ylecun",
      "source_name": "Yann LeCun(@ylecun)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/ef7c70f9568d45f4915169fef4ce90b4",
      "item_count": 4,
      "latest_item_time": "2026-04-24T12:03:30+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_name": "AI at Meta(@AIatMeta)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/fc16750ce50741f1b1f05ea1fb29436f",
      "item_count": 4,
      "latest_item_time": "2026-04-24T07:06:35+00:00",
      "sampled_item_count": 2,
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_name": "Hugging Face(@huggingface)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/78d7b99318b04b309b04000f7e24da29",
      "item_count": 4,
      "latest_item_time": "2026-04-16T15:36:13+00:00",
      "sampled_item_count": 3,
      "source_id": "socialmedia-mike-krieger-mikeyk",
      "source_name": "Mike Krieger(@mikeyk)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/8d2d03aea8af49818096da4ea00409d1",
      "item_count": 4,
      "latest_item_time": "2026-04-30T23:06:24+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-mistral-ai-mistralai",
      "source_name": "Mistral AI(@MistralAI)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/4d2d4165a7524217a08d3f57f27fa190",
      "item_count": 4,
      "latest_item_time": "2026-05-04T04:34:32+00:00",
      "sampled_item_count": 0,
      "source_id": "socialmedia-richard-socher-richardsocher",
      "source_name": "Richard Socher(@RichardSocher)"
    },
    {
      "feed_url": "https://api.xgo.ing/rss/user/244eb9fa77ce4fa3b7fa5ceba80027a4",
      "item_count": 2,
      "latest_item_time": "2025-05-23T14:50:37+00:00",
      "sampled_item_count": 2,
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
    "en_or_unknown": 150
  },
  "source_count": 41,
  "time_range": {
    "max_created_at": "2026-05-16T18:17:38.038971+00:00",
    "min_created_at": "2026-05-16T18:17:37.943991+00:00"
  },
  "top_sources": [
    [
      "socialmedia-junyang-lin-justinlin610",
      6
    ],
    [
      "socialmedia-ai-sdk-aisdk",
      6
    ],
    [
      "socialmedia-jan-leike-janleike",
      5
    ],
    [
      "socialmedia-ian-goodfellow-goodfellow-ian",
      5
    ],
    [
      "socialmedia-lex-fridman-lexfridman",
      5
    ],
    [
      "socialmedia-dario-amodei-darioamodei",
      5
    ],
    [
      "socialmedia-fei-fei-li-drfeifei",
      5
    ],
    [
      "socialmedia-jim-fan-drjimfan",
      5
    ],
    [
      "socialmedia-dia-diabrowser",
      5
    ],
    [
      "socialmedia-aman-sanger-amanrsanger",
      5
    ]
  ]
}
```

## 4. Item Card Quality

```json
{
  "avg_confidence": 0.652,
  "content_role_distribution": {
    "aggregator": 2,
    "analysis": 12,
    "commentary": 28,
    "firsthand": 9,
    "low_signal": 29,
    "report": 17,
    "source_material": 53
  },
  "entity_count_distribution": {
    "0": 4,
    "1": 26,
    "2": 27,
    "3": 32,
    "4": 27,
    "5": 18,
    "6": 8,
    "7": 2,
    "8": 3,
    "11": 2,
    "21": 1
  },
  "heuristic_card_fallback_count": 15,
  "item_cards_failed": 3,
  "item_cards_generated": 150,
  "item_cards_generated_or_reused": 150,
  "item_cards_reused": 0,
  "samples": [
    {
      "item_id": "item_011245f7f195487491d43cdbd222f77f",
      "role": "low_signal",
      "summary": "Groq Inc posted 'Happy Ramadan!'",
      "title": "Happy Ramadan!"
    },
    {
      "item_id": "item_024379e7ae9e44fea20ed3d72e54ad87",
      "role": "source_material",
      "summary": "Mistral AI introduces speech recognition models, claiming they are the world's best and open.",
      "title": "Our first shot at audio"
    },
    {
      "item_id": "item_04faba8580614a1d8785edb63548ef29",
      "role": "commentary",
      "summary": "Adam D'Angelo notes that AI-for-code continues to grow 100x while other verticals lag, citing Scott Wu.",
      "title": "This applies again today, e.g. people are saying the same exact thing now but code can still get *an..."
    },
    {
      "item_id": "item_07e767dc447240cfb5f2dd2efe0613b0",
      "role": "firsthand",
      "summary": "Ian Goodfellow shares his recovery from POTS version of Long COVID with help from Daniel Rossett, going from highly disabled to full exercise by September 2025.",
      "title": "Ian Goodfellow thanks Daniel Rossett for help recovering from Long COVID"
    },
    {
      "item_id": "item_07ec1d6244fa4eda8cc9adb3d9b0fcb0",
      "role": "low_signal",
      "summary": "Andrew Ng posts a Valentine's Day joke referencing AI temperature parameter.",
      "title": "To all my AI friends: Every time I see you, you raise my temperature parameter."
    },
    {
      "item_id": "item_08168486a8d9416eb0ff4cf15b2eb6a6",
      "role": "low_signal",
      "summary": "Fellou promotes its ability to track Silicon Valley VC activity.",
      "title": "A Super Useful Agentic Browser that gives me a daily pulse on the smartest signals from Silicon Valley VCs"
    },
    {
      "item_id": "item_0e94c7a731bd4cabbb627b2f08967fce",
      "role": "report",
      "summary": "I think robot pets are going to be a huge market. 💬 304 🔄 51 ❤️ 1101 👀 124870 📊 393 ⚡ Powered by xgo.ing",
      "title": "I think robot pets are going to be a huge market."
    },
    {
      "item_id": "item_0e9734e55b024f1e8a2dbc1559c8a9d8",
      "role": "source_material",
      "summary": "Thinking Machines announces Tinker API, a research tooling for fine-tuning with LoRA, beta waitlist open.",
      "title": "Thinking Machines launches Tinker API for fine-tuning with LoRA"
    },
    {
      "item_id": "item_0eabaeddd5bf453d8c4f0784ef03b18a",
      "role": "report",
      "summary": "AI SDK has passed 10 million downloads per week. Thank you to our community, from the contributors to the educators. 💬 6 🔄 13 ❤️ 145 👀 13819 📊 29 ⚡ Powered by xgo.ing",
      "title": "AI SDK has passed 10 million downloads per week. Thank you to our community, from the contributors ..."
    },
    {
      "item_id": "item_103c726e4eff445b85ba68202884e0cf",
      "role": "source_material",
      "summary": "v0 now allows creating private blob stores with auto-configured authenticated routes.",
      "title": "You can now create private blob stores in v0. The agent understands your configuration and automatically sets up authenticated routes so your files stay private."
    }
  ],
  "warnings_distribution": {
    "advertisement": 1,
    "aggregator_post": 1,
    "ambiguous_context": 1,
    "anecdotal_evidence": 1,
    "claim based on tweet, not verified": 1,
    "contains promotional language": 1,
    "context_missing": 1,
    "empty_tweet": 1,
    "heuristic_card": 15,
    "lacks_context": 1,
    "link_only": 1,
    "low_info": 1,
    "low_information": 1,
    "low_signal": 2,
    "marketing": 1,
    "missing_context": 1,
    "no_content": 1,
    "no_context": 1,
    "opinion_as_fact": 1,
    "opinion_only": 1,
    "opinion_quote": 1,
    "personal reflection, subjective": 1,
    "personal_opinion": 1,
    "promotional": 3,
    "promotional_content": 4,
    "quote_tweet": 1,
    "reply to another post, missing context": 1,
    "short": 1,
    "short_content": 2,
    "short_summary_only": 1,
    "social_media_promotion": 1,
    "source is individual, not official company account": 1,
    "speculation": 1,
    "subjective": 2,
    "subjective_claim": 1,
    "summary_only": 14,
    "thin content": 1,
    "third-party opinion": 1,
    "third-party report": 1,
    "third_party_announcement": 1,
    "too_short": 14,
    "tweet_with_limited_context": 1,
    "unsubstantiated_claims": 1,
    "unverified claim": 2,
    "unverified claims": 1,
    "unverified_claim": 2,
    "very short": 1,
    "very thin content, essay not linked": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.875,
  "candidate_pairs_considered": 72,
  "different": 55,
  "duplicate": 0,
  "examples": [
    {
      "candidate_item_title": "I'm excited about voice as a UI layer for existing visual applications — where speech and screen upd...",
      "confidence": 0.95,
      "new_item_title": "New version of Claude Code in the desktop app dropped today with tons of new features and performanc...",
      "primary_relation": "different",
      "published_at": "2026-04-14T20:01:44+00:00",
      "reason": "The new item is about a Claude Code desktop app update, while the candidate is about Vocal Bridge voice UI architecture. Different topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-alex-albert-alexalbert"
    },
    {
      "candidate_item_title": "Always great to chat with @danshipper ! Love what he and the team at @every are cooking up, we could...",
      "confidence": 0.95,
      "new_item_title": "New version of Claude Code in the desktop app dropped today with tons of new features and performanc...",
      "primary_relation": "different",
      "published_at": "2026-04-14T20:01:44+00:00",
      "reason": "The new item is about Claude Code desktop app update, while the candidate is about a podcast discussion on agent-native development. Different events.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-alex-albert-alexalbert"
    },
    {
      "candidate_item_title": "New research result: we use Claude to make fully autonomous progress on scalable oversight research,...",
      "confidence": 0.95,
      "new_item_title": "New version of Claude Code in the desktop app dropped today with tons of new features and performanc...",
      "primary_relation": "different",
      "published_at": "2026-04-14T20:01:44+00:00",
      "reason": "The new item is about Claude Code desktop app update, while the candidate is about research on scalable oversight using Claude. Different topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-alex-albert-alexalbert"
    },
    {
      "candidate_item_title": "Excited for this one — everything you need to ship production agents at scale, without having to spe...",
      "confidence": 0.95,
      "new_item_title": "New version of Claude Code in the desktop app dropped today with tons of new features and performanc...",
      "primary_relation": "different",
      "published_at": "2026-04-14T20:01:44+00:00",
      "reason": "The new item is about Claude Code desktop app update, while the candidate is about Claude Managed Agents launch. Different product updates.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-alex-albert-alexalbert"
    },
    {
      "candidate_item_title": "Claude Opus 4.7 is out! Handles ambiguous, multi-step work even better than 4.6. Cursor's internal b...",
      "confidence": 0.95,
      "new_item_title": "New version of Claude Code in the desktop app dropped today with tons of new features and performanc...",
      "primary_relation": "different",
      "published_at": "2026-04-14T20:01:44+00:00",
      "reason": "The new item is about Claude Code desktop app update, while the candidate is about Claude Opus 4.7 model release. Different topics.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-alex-albert-alexalbert"
    },
    {
      "candidate_item_title": "As AI agents accelerate coding, what is the future of software engineering? Some trends are clear, s...",
      "confidence": 0.8,
      "new_item_title": "New course: Spec-Driven Development with Coding Agents, built in partnership with @jetbrains, and ta...",
      "primary_relation": "related_with_new_info",
      "published_at": "2026-04-15T16:16:38+00:00",
      "reason": "Both items discuss AI in software engineering with Andrew Ng, but the new item introduces a specific course announcement with new details.",
      "secondary_roles": [
        "same_event_hint",
        "new_analysis_hint"
      ],
      "should_fold": false,
      "source": "socialmedia-andrew-ng-andrewyng"
    },
    {
      "candidate_item_title": "I'm excited about voice as a UI layer for existing visual applications — where speech and screen upd...",
      "confidence": 0.95,
      "new_item_title": "New course: Spec-Driven Development with Coding Agents, built in partnership with @jetbrains, and ta...",
      "primary_relation": "different",
      "published_at": "2026-04-15T16:16:38+00:00",
      "reason": "Different topic: voice UI vs. course on coding agents; only shared entity is Andrew Ng.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrew-ng-andrewyng"
    },
    {
      "candidate_item_title": "To all my AI friends: Every time I see you, you raise my temperature parameter. Happy Valentine’s ...",
      "confidence": 0.95,
      "new_item_title": "New course: Spec-Driven Development with Coding Agents, built in partnership with @jetbrains, and ta...",
      "primary_relation": "different",
      "published_at": "2026-04-15T16:16:38+00:00",
      "reason": "Unrelated Valentine's Day joke with low relevance.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrew-ng-andrewyng"
    },
    {
      "candidate_item_title": "New research result: we use Claude to make fully autonomous progress on scalable oversight research,...",
      "confidence": 0.95,
      "new_item_title": "New course: Spec-Driven Development with Coding Agents, built in partnership with @jetbrains, and ta...",
      "primary_relation": "different",
      "published_at": "2026-04-15T16:16:38+00:00",
      "reason": "Different research topic on scalable oversight, not about coding agent courses.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrew-ng-andrewyng"
    },
    {
      "candidate_item_title": "New version of Claude Code in the desktop app dropped today with tons of new features and performanc...",
      "confidence": 0.95,
      "new_item_title": "New course: Spec-Driven Development with Coding Agents, built in partnership with @jetbrains, and ta...",
      "primary_relation": "different",
      "published_at": "2026-04-15T16:16:38+00:00",
      "reason": "Claude Code desktop app update reaction, unrelated to the course announcement.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrew-ng-andrewyng"
    }
  ],
  "fold_candidates": 2,
  "llm_item_relation_calls": 14,
  "low_confidence_examples": [
    {
      "candidate_item_title": "The desert is never silent Video created by Betty Voice powered by @FishAudio #TTS #Voiceover #F...",
      "confidence": 0.3,
      "new_item_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "primary_relation": "different",
      "published_at": "2026-04-10T19:31:02+00:00",
      "reason": "Both mention FishAudio and TTS, but the topics are different (desert silence video vs relaxation audio).",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-fish-audio-fishaudio"
    },
    {
      "candidate_item_title": "unbelievable...",
      "confidence": 0.3,
      "new_item_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "primary_relation": "different",
      "published_at": "2026-04-10T19:31:02+00:00",
      "reason": "No shared entities or event hints; the new item is about FishAudio relaxation audio, candidate about Anthropic Project Glasswing.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-fish-audio-fishaudio"
    },
    {
      "candidate_item_title": "Someone recently suggested to me that the reason OpenClaw moment was so big is because it's the firs...",
      "confidence": 0.3,
      "new_item_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "primary_relation": "different",
      "published_at": "2026-04-10T19:31:02+00:00",
      "reason": "No shared entities or event hints; candidate discusses OpenClaw moment and agentic models.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-fish-audio-fishaudio"
    },
    {
      "candidate_item_title": "5/ https://t.co/mtEUo3Appi",
      "confidence": 0.3,
      "new_item_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "primary_relation": "different",
      "published_at": "2026-04-10T19:31:02+00:00",
      "reason": "No shared entities or event hints; candidate about Muse Spark image-to-code.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-fish-audio-fishaudio"
    },
    {
      "candidate_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "confidence": 0.3,
      "new_item_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "primary_relation": "different",
      "published_at": "2026-04-10T19:31:02+00:00",
      "reason": "No shared entities or event hints; candidate about Muse Spark availability.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-fish-audio-fishaudio"
    }
  ],
  "near_duplicate": 2,
  "related_with_new_info": 15,
  "related_with_new_info_count": 15,
  "relations_by_primary_relation": {
    "different": 55,
    "near_duplicate": 2,
    "related_with_new_info": 15
  },
  "uncertain_count": 0
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
      "cluster_title": "New course announcement on Spec-Driven Development with Coding Agents",
      "core_facts": [
        "Andrew Ng announces a new course on Spec-Driven Development with Coding Agents in partnership with JetBrains, taught by Paul Ewritt."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_10b3b4e273364cbc97bfe7cb825b3499"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Discussion on alignment research and AAR focus",
      "core_facts": [
        "Jan Leike discusses the need for research taste in alignment research and explains why the AAR is focused on scalable oversight."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_fbc0a479d2c7499298286095cc40bc4f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Claude Opus 4.7 is out! Handles ambiguous, multi-step work even better than 4.6. Cursor's internal b...",
      "core_facts": [
        "Claude Opus 4.7 is out! Handles ambiguous, multi-step work even better than 4.6. Cursor's internal bench cleared 70%, up from 58% on 4.6. Notion saw a 14% lift on their evals with a third of the tool errors 🔨 💬 12 🔄 4 ❤️ 96 👀 5943 📊 20 ⚡ Powered by xgo.ing"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_924bf44eeb5b4119a59612e7bb06b8c0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Muse Spark availability",
      "core_facts": [
        "AI at Meta encourages trying Muse Spark via the Meta AI app or meta.ai."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f59863fa95474594bfb077babc737505"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "OpenClaw moment",
      "core_facts": [
        "Someone recently suggested to me that the reason OpenClaw moment was so big is because it's the first time a large group of non-technical people (who otherwise only knew AI as synonymous with ChatGPT as a website) experienced the latest agentic models."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2bd5dac91c7c4b82a9baf74f852e9004"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Here's the links for my conversation with historian Lars Brownworth all about the Vikings.",
      "core_facts": [
        "Here's the links for my conversation with historian Lars Brownworth all about the Vikings. YouTube, Spotify, Podcast."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b822fbf9cd4247048e8865b998022430"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Hugging Face says 'Let's go!'",
      "core_facts": [
        "Hugging Face tweeted 'Let's go!' with no additional context."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d1193870702e4d52bc1c43e40cf25ab4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Comparing 15 open tabs? Decide with Dia.",
      "core_facts": [
        "Promotional tweet for Dia browser: helps users decide among open tabs."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8f5e94ac5ad142d683b09d6a20131a24"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "World Labs demonstrates world building with 100 million Gaussian splats",
      "core_facts": [
        "Fei-Fei Li shares a World Labs creation: a cyberpunk world built by a single creator using 100 million Gaussian splats generated in Marble."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_2733882e659e421088427aef91d0d464"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "1000 -> 10,000 ✅",
      "core_facts": [
        "Suhail tweets about a progression from 1000 to 10,000."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ac9eb38634b1411399857be4693485a5"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "v0 model auto-selection feature",
      "core_facts": [
        "v0 auto picks the right model (Mini, Pro, Max) for prompts."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_409eccfa6e504249a98017142fae3c54"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "EgoVerse ecosystem for robot learning",
      "core_facts": [
        "Jim Fan introduces EgoVerse, an ecosystem for robot learning from egocentric human data, with 1300+ hrs, 240 scenes, 2000+ tasks."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_b242f4433faf4e0895cef7452f376fe3"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "PHAN request for proposals",
      "core_facts": [
        "Public Health Action Network is accepting proposals for projects to reduce airborne disease transmission, such as breath-based detection or HVAC compliance verification."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d015df22d2fe497183d9ce492c52b123"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "See the performance difference side by side",
      "core_facts": [
        "See the performance difference side by side: demo link"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c3bd0a8890fa4568a1e4e29b2fbbb8bc"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Ramadan greeting",
      "core_facts": [
        "Groq Inc posted 'Happy Ramadan!'"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_011245f7f195487491d43cdbd222f77f"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Release of International AI Safety Report 2026",
      "core_facts": [
        "Geoffrey Hinton praises the International AI Safety Report 2026 as essential reading on AI risks."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c8686b7407254e9e833d74de24b237d0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "power outage affecting Waymo",
      "core_facts": [
        "Adam D'Angelo hopes that power outage issues don't impede Waymo's progress."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_63a7171dc2024519b7fd1be8ed27a895"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Mistral AI raises €1.7B Series C funding",
      "core_facts": [
        "Mistral AI raises €1.7B in Series C funding led by ASML, to accelerate AI research."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_6145efc6ebfc41938389720b58b4b9c0"
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
    "new_info": 14,
    "source_material": 4
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
      "cluster_id": "cluster_00aaa6dc3dfe4530bda177ee2b94c8a4",
      "cluster_title": "New course announcement on Spec-Driven Development with Coding Agents",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_2d06a89bd45745329f86119eb35a7b0e",
      "cluster_title": "Discussion on alignment research and AAR focus",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_ba9b1e55f850431ab044b36899a1bbd5",
      "cluster_title": "Claude Opus 4.7 is out! Handles ambiguous, multi-step work even better than 4.6. Cursor's internal b...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_fd7f1baa46864d3a81986ec55c9df39e",
      "cluster_title": "Muse Spark availability",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_fd32a50e9d4f43d9ac0b1101ae6d4d74",
      "cluster_title": "OpenClaw moment",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_50ee07a3a4ea402db421eef12a1817f3",
      "cluster_title": "Here's the links for my conversation with historian Lars Brownworth all about the Vikings.",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_ced16c14445748f8a4c37e6c57e15a10",
      "cluster_title": "Hugging Face says 'Let's go!'",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_1db2e8acf4394b7eae756dddae8eb66d",
      "cluster_title": "Comparing 15 open tabs? Decide with Dia.",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_64d8065c543e4cd98b147410b79a5297",
      "cluster_title": "World Labs demonstrates world building with 100 million Gaussian splats",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_6fa5105e5fad462a92fe2ff817171078",
      "cluster_title": "1000 -> 10,000 ✅",
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
    "cluster_title": "New course announcement on Spec-Driven Development with Coding Agents",
    "core_facts": [
      "Andrew Ng announces a new course on Spec-Driven Development with Coding Agents in partnership with JetBrains, taught by Paul Ewritt."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_10b3b4e273364cbc97bfe7cb825b3499"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Discussion on alignment research and AAR focus",
    "core_facts": [
      "Jan Leike discusses the need for research taste in alignment research and explains why the AAR is focused on scalable oversight."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_fbc0a479d2c7499298286095cc40bc4f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Claude Opus 4.7 is out! Handles ambiguous, multi-step work even better than 4.6. Cursor's internal b...",
    "core_facts": [
      "Claude Opus 4.7 is out! Handles ambiguous, multi-step work even better than 4.6. Cursor's internal bench cleared 70%, up from 58% on 4.6. Notion saw a 14% lift on their evals with a third of the tool errors 🔨 💬 12 🔄 4 ❤️ 96 👀 5943 📊 20 ⚡ Powered by xgo.ing"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_924bf44eeb5b4119a59612e7bb06b8c0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Muse Spark availability",
    "core_facts": [
      "AI at Meta encourages trying Muse Spark via the Meta AI app or meta.ai."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f59863fa95474594bfb077babc737505"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "OpenClaw moment",
    "core_facts": [
      "Someone recently suggested to me that the reason OpenClaw moment was so big is because it's the first time a large group of non-technical people (who otherwise only knew AI as synonymous with ChatGPT as a website) experienced the latest agentic models."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2bd5dac91c7c4b82a9baf74f852e9004"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Here's the links for my conversation with historian Lars Brownworth all about the Vikings.",
    "core_facts": [
      "Here's the links for my conversation with historian Lars Brownworth all about the Vikings. YouTube, Spotify, Podcast."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b822fbf9cd4247048e8865b998022430"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Hugging Face says 'Let's go!'",
    "core_facts": [
      "Hugging Face tweeted 'Let's go!' with no additional context."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d1193870702e4d52bc1c43e40cf25ab4"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Comparing 15 open tabs? Decide with Dia.",
    "core_facts": [
      "Promotional tweet for Dia browser: helps users decide among open tabs."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_8f5e94ac5ad142d683b09d6a20131a24"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "World Labs demonstrates world building with 100 million Gaussian splats",
    "core_facts": [
      "Fei-Fei Li shares a World Labs creation: a cyberpunk world built by a single creator using 100 million Gaussian splats generated in Marble."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_2733882e659e421088427aef91d0d464"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "1000 -> 10,000 ✅",
    "core_facts": [
      "Suhail tweets about a progression from 1000 to 10,000."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ac9eb38634b1411399857be4693485a5"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "v0 model auto-selection feature",
    "core_facts": [
      "v0 auto picks the right model (Mini, Pro, Max) for prompts."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_409eccfa6e504249a98017142fae3c54"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "EgoVerse ecosystem for robot learning",
    "core_facts": [
      "Jim Fan introduces EgoVerse, an ecosystem for robot learning from egocentric human data, with 1300+ hrs, 240 scenes, 2000+ tasks."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_b242f4433faf4e0895cef7452f376fe3"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "PHAN request for proposals",
    "core_facts": [
      "Public Health Action Network is accepting proposals for projects to reduce airborne disease transmission, such as breath-based detection or HVAC compliance verification."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d015df22d2fe497183d9ce492c52b123"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "See the performance difference side by side",
    "core_facts": [
      "See the performance difference side by side: demo link"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c3bd0a8890fa4568a1e4e29b2fbbb8bc"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Ramadan greeting",
    "core_facts": [
      "Groq Inc posted 'Happy Ramadan!'"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_011245f7f195487491d43cdbd222f77f"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Release of International AI Safety Report 2026",
    "core_facts": [
      "Geoffrey Hinton praises the International AI Safety Report 2026 as essential reading on AI risks."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c8686b7407254e9e833d74de24b237d0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "power outage affecting Waymo",
    "core_facts": [
      "Adam D'Angelo hopes that power outage issues don't impede Waymo's progress."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_63a7171dc2024519b7fd1be8ed27a895"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Mistral AI raises €1.7B Series C funding",
    "core_facts": [
      "Mistral AI raises €1.7B in Series C funding led by ASML, to accelerate AI research."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_6145efc6ebfc41938389720b58b4b9c0"
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
    "socialmedia-adam-d-angelo-adamdangelo": 0,
    "socialmedia-ai-at-meta-aiatmeta": 6224,
    "socialmedia-ai-breakfast-aibreakfast": 0,
    "socialmedia-ai-sdk-aisdk": 0,
    "socialmedia-alex-albert-alexalbert": 6087,
    "socialmedia-aman-sanger-amanrsanger": 0,
    "socialmedia-andrej-karpathy-karpathy": 2563,
    "socialmedia-andrew-ng-andrewyng": 3240,
    "socialmedia-arthur-mensch-arthurmensch": 0,
    "socialmedia-barsee-128054-heybarsee": 0,
    "socialmedia-berkeley-ai-research-berkeley-ai": 0,
    "socialmedia-binyuan-hui-huybery": 0,
    "socialmedia-dario-amodei-darioamodei": 0,
    "socialmedia-dia-diabrowser": 0,
    "socialmedia-dify-dify-ai": 0,
    "socialmedia-fei-fei-li-drfeifei": 0,
    "socialmedia-fellou-fellouai": 0,
    "socialmedia-fish-audio-fishaudio": 6471,
    "socialmedia-flowiseai-flowiseai": 0,
    "socialmedia-geoffrey-hinton-geoffreyhinton": 0,
    "socialmedia-groq-inc-groqinc": 0,
    "socialmedia-hugging-face-huggingface": 0,
    "socialmedia-ian-goodfellow-goodfellow-ian": 0,
    "socialmedia-ideogram-ideogram-ai": 0,
    "socialmedia-jan-leike-janleike": 10034,
    "socialmedia-jim-fan-drjimfan": 0,
    "socialmedia-jina-ai-jinaai": 0,
    "socialmedia-mike-krieger-mikeyk": 3108,
    "socialmedia-poe-poe-platform": 4074,
    "socialmedia-v0-v0": 3016
  },
  "low_candidates": [],
  "pending_reviews_created": 293,
  "sources_recomputed": 41,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 6087,
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
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2563,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-barsee-128054-heybarsee",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-dify-dify-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-fellou-fellouai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 6471,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-hugging-face-huggingface",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-ideogram-ideogram-ai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "total_items": 1,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 4074,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-poe-poe-platform",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 4,
      "llm_total_tokens": 6224,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-ai-breakfast-aibreakfast",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 1,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 6087,
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
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-aman-sanger-amanrsanger",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2563,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 3240,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
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
      "source_id": "socialmedia-barsee-128054-heybarsee",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 4,
      "llm_total_tokens": 6224,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2563,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 3240,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-dia-diabrowser",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 3240,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 3016,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-v0-v0",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 4,
      "llm_total_tokens": 6224,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2563,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-dia-diabrowser",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-adam-d-angelo-adamdangelo",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 4,
      "llm_total_tokens": 6224,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2563,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-andrej-karpathy-karpathy",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 3240,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-dia-diabrowser",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-fei-fei-li-drfeifei",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-geoffrey-hinton-geoffreyhinton",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    },
    {
      "created_at": "2026-05-16T18:27:31.882789+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:27:31.882789+00:00"
    }
  ]
}
```

## 9. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 24583.1,
    "cache_hit_tokens": 29056,
    "cache_miss_tokens": 0,
    "calls": 30,
    "failed": 3,
    "input_tokens": 76744,
    "llm_call_count": 30,
    "operation_count": 30,
    "output_tokens": 84533,
    "p50_latency_ms": 23930,
    "p95_latency_ms": 31253,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 3,
    "skipped": 0,
    "success": 27,
    "task_type": "item_card",
    "total_tokens": 161277
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 12661.4,
    "cache_hit_tokens": 8960,
    "cache_miss_tokens": 0,
    "calls": 14,
    "failed": 0,
    "input_tokens": 24247,
    "llm_call_count": 14,
    "operation_count": 148,
    "output_tokens": 20570,
    "p50_latency_ms": 11732,
    "p95_latency_ms": 16808,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 134,
    "success": 14,
    "task_type": "item_relation",
    "total_tokens": 44817
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
    "operation_count": 130,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 130,
    "success": 0,
    "task_type": "item_cluster_relation",
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
    "operation_count": 21,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 21,
    "success": 0,
    "task_type": "cluster_card_patch",
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
  "actual_calls": 44,
  "actual_tokens": 206094,
  "avg_latency_ms": 20789.8,
  "by_task": {
    "cluster_card_patch": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 2,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 0,
      "p95_latency_ms": 0,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 0,
      "task_type": "cluster_card_patch",
      "total_tokens": 0
    },
    "cluster_card_rebuild": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 2,
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
      "avg_latency_ms": 24583.1,
      "cache_hit_tokens": 29056,
      "calls": 30,
      "concurrency": 2,
      "db_lock_errors": 0,
      "failed": 3,
      "p50_latency_ms": 23930,
      "p95_latency_ms": 31253,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 3,
      "success": 27,
      "task_type": "item_card",
      "total_tokens": 161277
    },
    "item_cluster_relation": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 2,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 0,
      "p95_latency_ms": 0,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 0,
      "task_type": "item_cluster_relation",
      "total_tokens": 0
    },
    "item_relation": {
      "avg_latency_ms": 12661.4,
      "cache_hit_tokens": 8960,
      "calls": 14,
      "concurrency": 2,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 11732,
      "p95_latency_ms": 16808,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 14,
      "task_type": "item_relation",
      "total_tokens": 44817
    },
    "json_repair": {
      "avg_latency_ms": 0.0,
      "cache_hit_tokens": 0,
      "calls": 0,
      "concurrency": 2,
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
      "concurrency": 2,
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
  "cache_hit_rate": 0.1845,
  "cache_hit_tokens": 38016,
  "calls_per_sec": 0.0741,
  "db_lock_errors": 0,
  "duration_seconds": 594.173,
  "final_failures": 3,
  "max_concurrency": 2,
  "p50_latency_ms": 21257,
  "p95_latency_ms": 30208,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 3,
  "tokens_per_sec": 346.86
}
```

## 11. Errors / Fallbacks / Retries

```json
{
  "db_lock_errors": 0,
  "final_failures": 3,
  "llm_parse_failures": 0,
  "repair_retry_count": 3,
  "review_queue_entries_due_to_failure": 264,
  "skipped_due_to_max_calls": false,
  "skipped_due_to_missing_card": 0,
  "skipped_due_to_no_candidate": 0,
  "skipped_due_to_token_budget": false
}
```

## 12. Prompt Iteration Notes

```json
[
  {
    "changes": [
      "source scope filtering",
      "sample modes",
      "operation_count versus llm_call_count report split",
      "concurrency summary"
    ],
    "concurrency": 2,
    "iteration": "phase1_2_current",
    "max_calls": 350,
    "max_items": 150,
    "notes": "No enum expansion; prompt JSON contracts remain stable.",
    "sample_mode": "source_scope_full"
  }
]
```

## 13. Manual Review Suggestions

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
    "3 LLM failures observed in this run."
  ],
  "write_real_db_recommended_now": false
}
```

## 15. Recommendations

- Add vector indexes for item_cards and cluster_cards before larger runs.
- Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.
- Collect more source_signals before trusting source_profile priority suggestions.
- Run a larger dry-run before any write-real-db semantic pass.
- Increase token_budget or lower max_items for more complete evaluation.
