# Semantic Quality Report

## 1. Run Metadata

```json
{
  "actual_calls": 49,
  "actual_tokens": 212231,
  "batch_size": 5,
  "cache_hit_tokens": 49920,
  "cache_miss_tokens": 0,
  "concurrency": 4,
  "db_path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "dry_run": true,
  "duration_seconds": 398.016,
  "evaluation_db_path": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_semantic_eval_kaow3o83.sqlite3",
  "finished_at": "2026-05-16T18:40:24.073857+00:00",
  "git_commit": "038fec7dcde63c6e80bf9ff73031abfaafb9c25b",
  "include_archived": false,
  "items_sampled": 150,
  "live": true,
  "max_calls": 350,
  "max_candidates": 5,
  "max_items": 150,
  "model": "deepseek-v4-flash",
  "recall_strategy": "lexical/entity/time/source hybrid",
  "run_id": "semantic_eval_20260516_183346_027971",
  "sample_mode": "source_scope_full",
  "source_filter": null,
  "source_url_prefix": "api.xgo.ing",
  "started_at": "2026-05-16T18:33:46.027971+00:00",
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
    "max_created_at": "2026-05-16T18:33:46.194108+00:00",
    "min_created_at": "2026-05-16T18:33:46.102296+00:00"
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
  "avg_confidence": 0.647,
  "content_role_distribution": {
    "aggregator": 5,
    "analysis": 10,
    "commentary": 33,
    "firsthand": 17,
    "low_signal": 33,
    "report": 16,
    "source_material": 36
  },
  "entity_count_distribution": {
    "0": 5,
    "1": 27,
    "2": 33,
    "3": 30,
    "4": 15,
    "5": 19,
    "6": 9,
    "7": 5,
    "8": 3,
    "10": 3,
    "22": 1
  },
  "heuristic_card_fallback_count": 15,
  "item_cards_failed": 3,
  "item_cards_generated": 150,
  "item_cards_generated_or_reused": 150,
  "item_cards_reused": 0,
  "samples": [
    {
      "item_id": "item_0007092833ab46608e948bb5b4d0df3c",
      "role": "low_signal",
      "summary": "A short anecdote about using OpenClaw to create a fake website for price matching.",
      "title": "-Electronics store says it will price match -Guy pulls out his phone and sends OpenClaw a message to vibecode fake website listing the exact item for 50% off"
    },
    {
      "item_id": "item_007cb4e1b8e443a7becbcd805f4257e9",
      "role": "commentary",
      "summary": "Jan Leike praises work by Jiaxin Wen, Liang Qiu, Joe Benton, and Jan Kirchner, linking to an Anthropic blog post.",
      "title": "Awesome work by Jiaxin Wen, Liang Qiu, Joe Benton, Jan Kirchner"
    },
    {
      "item_id": "item_0513ec76f9bf4899a3e5a9eacca6d7ca",
      "role": "commentary",
      "summary": "Lex Fridman promotes his full conversation with Lars Brownworth about Vikings, with timestamps.",
      "title": "Here's my conversation with historian Lars Brownworth all about the Vikings"
    },
    {
      "item_id": "item_06b60771ce84426f9a241a00d23615c0",
      "role": "source_material",
      "summary": "Jina AI v5-text uses decoder-only backbones, last-token pooling, four LoRA adapters, and 32K context length (4x over v3).",
      "title": "Jina AI v5-text details"
    },
    {
      "item_id": "item_0753fe49e9dd4815b84d7534695e7570",
      "role": "commentary",
      "summary": "AI at Meta retweeted a quote from Nainish Rai claiming that Muse Spark infers product logic from screenshots, beyond image-to-code.",
      "title": "5/ https://t.co/mtEUo3Appi"
    },
    {
      "item_id": "item_09af6638b62549b7acb7ca24b5ba8da5",
      "role": "low_signal",
      "summary": "From browsing to doing (video).",
      "title": "From browsing → doing."
    },
    {
      "item_id": "item_09b218045ea14265bc422087888b55c1",
      "role": "source_material",
      "summary": "Ian Goodfellow announces PHAN is accepting project proposals to reduce airborne disease transmission.",
      "title": "In Public Health Action Network we’re about to go through an internal expert review process..."
    },
    {
      "item_id": "item_0bc895330bbf4d6b8d611b9da7084b30",
      "role": "source_material",
      "summary": "Jina AI announced their official CLI for agents.",
      "title": "Our official CLI for agents"
    },
    {
      "item_id": "item_0e447f5e4eab4c3f8ef574e22107d379",
      "role": "report",
      "summary": "AI needs to be connected to the physical world, proud to be supporting ! William Fedus @LiamFedus Today, @ekindogus and I are excited to introduce @periodiclabs . Our goal is to create an AI scientist. Science works by conjecturing how the world might be, running experiments, and learning from the results. Intelligence is necessary, but not sufficient. New…",
      "title": "AI needs to be connected to the physical world, proud to be supporting !"
    },
    {
      "item_id": "item_15e52eab51d84011bec2e7e4a8446999",
      "role": "commentary",
      "summary": "Binyuan Hui posts a farewell tweet about Qwen and mentions Junyang Lin stepping down.",
      "title": "bye qwen, me too."
    }
  ],
  "warnings_distribution": {
    "Contains April Fool's Day disclaimer, but content appears genuine.": 1,
    "advertisement": 1,
    "aggregator_content": 2,
    "anecdotal": 1,
    "benchmark_numbers_from_third_party": 1,
    "claim not verified": 1,
    "claim_unverified": 1,
    "claims_unverified": 1,
    "context_missing": 1,
    "heuristic_card": 15,
    "long_personal_post": 1,
    "low_signal": 3,
    "low_signal_content": 1,
    "marketing": 1,
    "marketing_content": 1,
    "marketing_question": 1,
    "no_content": 2,
    "opinion": 2,
    "opinion_included": 1,
    "opinion_only": 2,
    "opinion_piece": 2,
    "personal narrative": 1,
    "personal reflection": 1,
    "promotional": 3,
    "promotional_claim": 1,
    "promotional_content": 5,
    "quoted_tweet_not_separated": 1,
    "short_content": 1,
    "social_media_short": 4,
    "social_update": 1,
    "speculation": 1,
    "summary_only": 26,
    "third_party_opinion": 2,
    "third_party_report": 1,
    "too_short": 14,
    "truncated_link": 1,
    "truncated_url": 1,
    "unofficial_announcement": 1,
    "unrelated_to_ai_models": 1,
    "unspecified_authenticity": 1,
    "unverified claim": 1,
    "unverified claims": 1,
    "unverified_benchmark": 1,
    "unverified_benchmark_claims": 1,
    "vague": 1,
    "weak_signal": 1
  }
}
```

## 5. Item-Item Relation Quality

```json
{
  "avg_confidence": 0.89,
  "candidate_pairs_considered": 95,
  "different": 73,
  "duplicate": 0,
  "examples": [
    {
      "candidate_item_title": "My former Brain colleague @AndrewDai just launched @ElorianAI",
      "confidence": 0.9,
      "new_item_title": "Yes it's the tractable form of brain upload. There's a ton of scifi on brain uploads that requires w...",
      "primary_relation": "different",
      "published_at": "2026-04-10T15:32:10+00:00",
      "reason": "The new item discusses brain upload via LLMs, while the candidate is about the launch of ElorianAI, an unrelated AI lab.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrej-karpathy-karpathy"
    },
    {
      "candidate_item_title": "Someone recently suggested to me that the reason OpenClaw moment was so big is because it's the firs...",
      "confidence": 0.9,
      "new_item_title": "Yes it's the tractable form of brain upload. There's a ton of scifi on brain uploads that requires w...",
      "primary_relation": "different",
      "published_at": "2026-04-10T15:32:10+00:00",
      "reason": "The new item speculates on brain upload, while the candidate discusses the OpenClaw moment's virality among non-technical users.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrej-karpathy-karpathy"
    },
    {
      "candidate_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "confidence": 0.9,
      "new_item_title": "Yes it's the tractable form of brain upload. There's a ton of scifi on brain uploads that requires w...",
      "primary_relation": "different",
      "published_at": "2026-04-10T15:32:10+00:00",
      "reason": "The new item is about brain upload, while the candidate announces availability of Muse Spark, a separate AI product.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrej-karpathy-karpathy"
    },
    {
      "candidate_item_title": "Your @openclaw experience just got better with @mem0ai plugin",
      "confidence": 0.9,
      "new_item_title": "Yes it's the tractable form of brain upload. There's a ton of scifi on brain uploads that requires w...",
      "primary_relation": "different",
      "published_at": "2026-04-10T15:32:10+00:00",
      "reason": "The new item discusses brain upload, while the candidate is about a plugin for OpenClaw with memory features.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrej-karpathy-karpathy"
    },
    {
      "candidate_item_title": "Here's my conversation with historian Lars Brownworth all about the Vikings, from the start of the V...",
      "confidence": 0.9,
      "new_item_title": "Yes it's the tractable form of brain upload. There's a ton of scifi on brain uploads that requires w...",
      "primary_relation": "different",
      "published_at": "2026-04-10T15:32:10+00:00",
      "reason": "The new item is AI-related speculation, while the candidate is about a history podcast episode on Vikings.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-andrej-karpathy-karpathy"
    },
    {
      "candidate_item_title": "5/ https://t.co/mtEUo3Appi",
      "confidence": 0.9,
      "new_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "primary_relation": "related_with_new_info",
      "published_at": "2026-04-09T21:52:29+00:00",
      "reason": "Both discuss Muse Spark; new item adds availability details.",
      "secondary_roles": [
        "new_fact_hint"
      ],
      "should_fold": false,
      "source": "socialmedia-ai-at-meta-aiatmeta"
    },
    {
      "candidate_item_title": "🔜",
      "confidence": 0.9,
      "new_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "primary_relation": "related_with_new_info",
      "published_at": "2026-04-09T21:52:29+00:00",
      "reason": "Both about Muse Spark; candidate mentions API coming soon, new item confirms availability.",
      "secondary_roles": [
        "same_event_hint",
        "new_fact_hint"
      ],
      "should_fold": false,
      "source": "socialmedia-ai-at-meta-aiatmeta"
    },
    {
      "candidate_item_title": "Yes it's the tractable form of brain upload. There's a ton of scifi on brain uploads that requires w...",
      "confidence": 1.0,
      "new_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "primary_relation": "different",
      "published_at": "2026-04-09T21:52:29+00:00",
      "reason": "Unrelated topics: brain upload vs Muse Spark availability.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-ai-at-meta-aiatmeta"
    },
    {
      "candidate_item_title": "It's a really good model! Excited for more people to try it",
      "confidence": 1.0,
      "new_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "primary_relation": "different",
      "published_at": "2026-04-09T21:52:29+00:00",
      "reason": "Unrelated: Composer 2 vs Muse Spark.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-ai-at-meta-aiatmeta"
    },
    {
      "candidate_item_title": "Making improvements one step at a time for Marble. In the case of generating bigger worlds, it's qui...",
      "confidence": 1.0,
      "new_item_title": "Try Muse Spark today via the Meta AI app or https://t.co/SSo3nt4aQ4.",
      "primary_relation": "different",
      "published_at": "2026-04-09T21:52:29+00:00",
      "reason": "Unrelated: Marble updates vs Muse Spark.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-ai-at-meta-aiatmeta"
    }
  ],
  "fold_candidates": 4,
  "llm_item_relation_calls": 19,
  "low_confidence_examples": [
    {
      "candidate_item_title": "New research result: we use Claude to make fully autonomous progress on scalable oversight research,...",
      "confidence": 0.4,
      "new_item_title": "Awesome work by @jiaxinwen22, @liangqiu_1994, Joe Benton, and @janhkirchner! For more details, chec...",
      "primary_relation": "different",
      "published_at": "2026-04-14T19:43:38+00:00",
      "reason": "The new item praises different researchers and does not mention scalable oversight research.",
      "secondary_roles": [],
      "should_fold": false,
      "source": "socialmedia-jan-leike-janleike"
    }
  ],
  "near_duplicate": 4,
  "related_with_new_info": 18,
  "related_with_new_info_count": 18,
  "relations_by_primary_relation": {
    "different": 73,
    "near_duplicate": 4,
    "related_with_new_info": 18
  },
  "uncertain_count": 0
}
```

## 6. Item-Cluster Relation Quality

```json
{
  "actions": {
    "attach_to_cluster": 22
  },
  "attached_existing_clusters": 0,
  "avg_confidence": 0.6,
  "avg_items_per_cluster": 1.0,
  "candidate_clusters_considered": 22,
  "cluster_samples": [
    {
      "cluster_status": "active",
      "cluster_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "core_facts": [
        "FishAudio promoted a TGIF RELAX audio track produced by monster_library, with hashtags #TTS #FishAudio #Voiceover."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_498fe1091c964c26bc1c40cbcc21bd20"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Speculation on brain upload via LLMs",
      "core_facts": [
        "Andrej Karpathy argues that a lossy, approximate brain upload via LLM simulators is imminent and describes a hypothetical startup."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d8b226b3baec4e018926c8a4b5fd900d"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Muse Spark API announcement",
      "core_facts": [
        "AI at Meta announced that the Muse Spark API will be released soon, noticing excitement among developers."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_86387fd9b60f4df1aadf44edc9775299"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Junyang Lin's reflections on the agent era",
      "core_facts": [
        "Junyang Lin shares three thoughts on the agent era: critical thinking with agents, designing well-structured organizations, and newbies having advantages."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d77e8cb90c224020a834e6604ab98eac"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Claude Opus 4.7 benchmark results",
      "core_facts": [
        "SWE-Bench Pro 64.3%, SWE-Bench Verified 87.6%, TerminalBench 69.4%. Coding performance improved meaningfully in Opus 4.7 vs 4.6."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_985c748f45d84f7eb4e71fed818bb964"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Alignment research commentary",
      "core_facts": [
        "Jan Leike tweets that most alignment research is not crisp and requires research taste, explaining why AAR focuses on scalable oversight."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ea913b4e773949f188316bf6440fa22e"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "This life is fucking amazing. I'm so grateful to be alive, with all of you on this miracle of a plan...",
      "core_facts": [
        "Lex Fridman writes a long personal tweet expressing gratitude, discussing world leader conversations, personal struggles, and plans to talk to more everyday people."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_8174b6743f44456f97d90a2c03362cb0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Release of Mem0 OpenClaw Plugin v1.0.4",
      "core_facts": [
        "Taranjeet announces Mem0 OpenClaw Plugin v1.0.4 with long-term memory features."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d873003ca5704943ac119396b2166cc2"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Dia browser feature advertisement",
      "core_facts": [
        "Dia browser advertises a feature to compare 15 open tabs and make a decision."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f52e19e1ae5c4fc99aa2b74b7bc3b574"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "1000 -> 10,000 ✅",
      "core_facts": [
        "1000 -> 10,000 ✅ Suhail @Suhail 0 -> 1000 ✅"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_ffeee2c69ade474290c2beb7909fc63b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Podcast on agent-native product development",
      "core_facts": [
        "Mike Krieger of Anthropic Labs discusses building agent-native products, team structures, and the need to iterate quickly."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_f3a221e5d3e84af3987d38f6c201a0c5"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "From browsing → doing.",
      "core_facts": [
        "From browsing to doing (video)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_09af6638b62549b7acb7ca24b5ba8da5"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "LiteLLM compromise and implications for agentic software security",
      "core_facts": [
        "Discussion on how agentic frameworks pose new security risks, referencing compromised LiteLLM release."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_c57329df897a49e481ccbfd759e029e4"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Midjourney v8 preview available",
      "core_facts": [
        "Instructions to access Midjourney v8 preview on alpha.midjourney.com."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_d0b5f3d81a5d4ddf943dbee879fc1f18"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "AI SDK reaches 10 million weekly downloads",
      "core_facts": [
        "AI SDK has passed 10 million downloads per week."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3365e74fb233484f93c7809f71bf5760"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "https://t.co/yiFQMTL90G",
      "core_facts": [
        "Link to Flowise GitHub repository."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_cbf6533357a44c08931b978ee1dee0bf"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "AI-for-code continues to grow while other verticals lag",
      "core_facts": [
        "Adam D'Angelo observes that code keeps getting 100x bigger while other AI verticals grow slower, contrary to earlier predictions."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_bc7adc2e71f245d5a92dac88be8dda6b"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Technical details of v5-text embedding model by Jina AI",
      "core_facts": [
        "Jina AI v5-text uses decoder-only backbones, last-token pooling, four LoRA adapters, and 32K context length (4x over v3)."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_06b60771ce84426f9a241a00d23615c0"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Happy Ramadan!",
      "core_facts": [
        "Happy Ramadan!"
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_7e44524158cf4dd0a001f46be597486a"
      ]
    },
    {
      "cluster_status": "active",
      "cluster_title": "Solomei AI builds Callimacus on Groq",
      "core_facts": [
        "Solomei AI built Callimacus on Groq for brands like Brunello Cucinelli."
      ],
      "item_count": 1,
      "known_angles": [],
      "representative_items": [
        "item_3882481533134b529ee8ea71e1ff8aff"
      ]
    }
  ],
  "created_clusters": 22,
  "follow_up_event": {
    "false": 22
  },
  "manual_review_suggestions": {
    "high_uncertain": [],
    "possible_miscluster": [],
    "possible_missplit": [],
    "top_review_items_or_clusters": []
  },
  "multi_item_cluster_count": 0,
  "relations": {
    "new_info": 17,
    "source_material": 5
  },
  "same_event": {
    "true": 22
  },
  "same_topic": {
    "true": 22
  },
  "should_notify_count": 0,
  "should_update_cluster_card_count": 22,
  "top_clusters": [
    {
      "cluster_id": "cluster_d89cf4ad806a41b5a54e1a4742f4b810",
      "cluster_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_37bd65622dc7435dbed0b63da8350c39",
      "cluster_title": "Speculation on brain upload via LLMs",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_74dbc4c6fc104240bc083ff26f9dacbe",
      "cluster_title": "Muse Spark API announcement",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_5f6db939c2f14f76a468b8e329110001",
      "cluster_title": "Junyang Lin's reflections on the agent era",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_8b1cb5a50b544fc19bc209f8082c108d",
      "cluster_title": "Claude Opus 4.7 benchmark results",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_76529fde0e824b11b57cf6bc81281fde",
      "cluster_title": "Alignment research commentary",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_7d537bdabd0445cab36411cfb407c9c7",
      "cluster_title": "This life is fucking amazing. I'm so grateful to be alive, with all of you on this miracle of a plan...",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_f29d3eb8460047d98bffa02299f62536",
      "cluster_title": "Release of Mem0 OpenClaw Plugin v1.0.4",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_1a04f86488bd40cab5dd6ed88d5beea9",
      "cluster_title": "Dia browser feature advertisement",
      "item_count": 1
    },
    {
      "cluster_id": "cluster_75ecf062218844bb8102f26e3f98aee2",
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
    "cluster_title": "TGIF, RELAX Audio powered by @FishAudio Produced by @monster_library #TTS #FishAudio #Voiceover",
    "core_facts": [
      "FishAudio promoted a TGIF RELAX audio track produced by monster_library, with hashtags #TTS #FishAudio #Voiceover."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_498fe1091c964c26bc1c40cbcc21bd20"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Speculation on brain upload via LLMs",
    "core_facts": [
      "Andrej Karpathy argues that a lossy, approximate brain upload via LLM simulators is imminent and describes a hypothetical startup."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d8b226b3baec4e018926c8a4b5fd900d"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Muse Spark API announcement",
    "core_facts": [
      "AI at Meta announced that the Muse Spark API will be released soon, noticing excitement among developers."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_86387fd9b60f4df1aadf44edc9775299"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Junyang Lin's reflections on the agent era",
    "core_facts": [
      "Junyang Lin shares three thoughts on the agent era: critical thinking with agents, designing well-structured organizations, and newbies having advantages."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d77e8cb90c224020a834e6604ab98eac"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Claude Opus 4.7 benchmark results",
    "core_facts": [
      "SWE-Bench Pro 64.3%, SWE-Bench Verified 87.6%, TerminalBench 69.4%. Coding performance improved meaningfully in Opus 4.7 vs 4.6."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_985c748f45d84f7eb4e71fed818bb964"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Alignment research commentary",
    "core_facts": [
      "Jan Leike tweets that most alignment research is not crisp and requires research taste, explaining why AAR focuses on scalable oversight."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ea913b4e773949f188316bf6440fa22e"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "This life is fucking amazing. I'm so grateful to be alive, with all of you on this miracle of a plan...",
    "core_facts": [
      "Lex Fridman writes a long personal tweet expressing gratitude, discussing world leader conversations, personal struggles, and plans to talk to more everyday people."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_8174b6743f44456f97d90a2c03362cb0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Release of Mem0 OpenClaw Plugin v1.0.4",
    "core_facts": [
      "Taranjeet announces Mem0 OpenClaw Plugin v1.0.4 with long-term memory features."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d873003ca5704943ac119396b2166cc2"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Dia browser feature advertisement",
    "core_facts": [
      "Dia browser advertises a feature to compare 15 open tabs and make a decision."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f52e19e1ae5c4fc99aa2b74b7bc3b574"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "1000 -> 10,000 ✅",
    "core_facts": [
      "1000 -> 10,000 ✅ Suhail @Suhail 0 -> 1000 ✅"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_ffeee2c69ade474290c2beb7909fc63b"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Podcast on agent-native product development",
    "core_facts": [
      "Mike Krieger of Anthropic Labs discusses building agent-native products, team structures, and the need to iterate quickly."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_f3a221e5d3e84af3987d38f6c201a0c5"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "From browsing → doing.",
    "core_facts": [
      "From browsing to doing (video)."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_09af6638b62549b7acb7ca24b5ba8da5"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "LiteLLM compromise and implications for agentic software security",
    "core_facts": [
      "Discussion on how agentic frameworks pose new security risks, referencing compromised LiteLLM release."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_c57329df897a49e481ccbfd759e029e4"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Midjourney v8 preview available",
    "core_facts": [
      "Instructions to access Midjourney v8 preview on alpha.midjourney.com."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_d0b5f3d81a5d4ddf943dbee879fc1f18"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "AI SDK reaches 10 million weekly downloads",
    "core_facts": [
      "AI SDK has passed 10 million downloads per week."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_3365e74fb233484f93c7809f71bf5760"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "https://t.co/yiFQMTL90G",
    "core_facts": [
      "Link to Flowise GitHub repository."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_cbf6533357a44c08931b978ee1dee0bf"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "AI-for-code continues to grow while other verticals lag",
    "core_facts": [
      "Adam D'Angelo observes that code keeps getting 100x bigger while other AI verticals grow slower, contrary to earlier predictions."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_bc7adc2e71f245d5a92dac88be8dda6b"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Technical details of v5-text embedding model by Jina AI",
    "core_facts": [
      "Jina AI v5-text uses decoder-only backbones, last-token pooling, four LoRA adapters, and 32K context length (4x over v3)."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_06b60771ce84426f9a241a00d23615c0"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Happy Ramadan!",
    "core_facts": [
      "Happy Ramadan!"
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_7e44524158cf4dd0a001f46be597486a"
    ]
  },
  {
    "cluster_status": "active",
    "cluster_title": "Solomei AI builds Callimacus on Groq",
    "core_facts": [
      "Solomei AI built Callimacus on Groq for brands like Brunello Cucinelli."
    ],
    "item_count": 1,
    "known_angles": [],
    "representative_items": [
      "item_3882481533134b529ee8ea71e1ff8aff"
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
    "socialmedia-ai-at-meta-aiatmeta": 8796,
    "socialmedia-ai-breakfast-aibreakfast": 2794,
    "socialmedia-ai-sdk-aisdk": 0,
    "socialmedia-alex-albert-alexalbert": 6219,
    "socialmedia-aman-sanger-amanrsanger": 0,
    "socialmedia-andrej-karpathy-karpathy": 2516,
    "socialmedia-andrew-ng-andrewyng": 9189,
    "socialmedia-arthur-mensch-arthurmensch": 0,
    "socialmedia-barsee-128054-heybarsee": 0,
    "socialmedia-berkeley-ai-research-berkeley-ai": 0,
    "socialmedia-binyuan-hui-huybery": 0,
    "socialmedia-dario-amodei-darioamodei": 0,
    "socialmedia-dia-diabrowser": 0,
    "socialmedia-dify-dify-ai": 0,
    "socialmedia-fei-fei-li-drfeifei": 0,
    "socialmedia-fellou-fellouai": 0,
    "socialmedia-fish-audio-fishaudio": 5684,
    "socialmedia-flowiseai-flowiseai": 0,
    "socialmedia-geoffrey-hinton-geoffreyhinton": 0,
    "socialmedia-groq-inc-groqinc": 0,
    "socialmedia-hugging-face-huggingface": 0,
    "socialmedia-ian-goodfellow-goodfellow-ian": 0,
    "socialmedia-ideogram-ideogram-ai": 0,
    "socialmedia-jan-leike-janleike": 6924,
    "socialmedia-jim-fan-drjimfan": 0,
    "socialmedia-junyang-lin-justinlin610": 5899,
    "socialmedia-mike-krieger-mikeyk": 2368,
    "socialmedia-poe-poe-platform": 2802,
    "socialmedia-v0-v0": 2981
  },
  "low_candidates": [],
  "pending_reviews_created": 281,
  "sources_recomputed": 41,
  "sources_with_insufficient_data": [
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2794,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 6219,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2516,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 5684,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 3,
      "llm_total_tokens": 2802,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-poe-poe-platform",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    }
  ],
  "top_sources_by_duplicate_rate": [
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 6,
      "llm_total_tokens": 8796,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2794,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 6219,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2516,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 0.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 2,
      "llm_total_tokens": 9189,
      "llm_yield_score": 0.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 0.0,
      "priority_suggestion": "normal",
      "report_value_avg": 0.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-andrew-ng-andrewyng",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 4,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-arthur-mensch-arthurmensch",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    }
  ],
  "top_sources_by_incremental_value_avg": [
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 6,
      "llm_total_tokens": 8796,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2516,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 5684,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-flowiseai-flowiseai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 3.375,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_item_rate": 0.5,
      "source_material_rate": 0.5,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    }
  ],
  "top_sources_by_llm_yield": [
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 6,
      "llm_total_tokens": 8796,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.2,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-jina-ai-jinaai",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-taranjeet-taranjeetio",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 3.375,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_item_rate": 0.5,
      "source_material_rate": 0.5,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2516,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 5684,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-flowiseai-flowiseai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    }
  ],
  "top_sources_by_report_value_avg": [
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 6,
      "llm_total_tokens": 8796,
      "llm_yield_score": 4.0,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-ai-at-meta-aiatmeta",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 3,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-ai-sdk-aisdk",
      "source_item_rate": 1.0,
      "source_material_rate": 1.0,
      "total_items": 6,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 2516,
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 1,
      "llm_total_tokens": 5684,
      "llm_yield_score": 2.75,
      "near_duplicate_rate": 0.5,
      "new_event_rate": 1.0,
      "priority_suggestion": "new_source_under_evaluation",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "none",
      "source_id": "socialmedia-fish-audio-fishaudio",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 2,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-flowiseai-flowiseai",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
      "duplicate_rate": 0.0,
      "incremental_value_avg": 3.0,
      "llm_high_value_outputs": 0,
      "llm_priority": "new_source_under_evaluation",
      "llm_processed_items": 0,
      "llm_total_tokens": 0,
      "llm_yield_score": 3.375,
      "near_duplicate_rate": 0.0,
      "new_event_rate": 1.0,
      "priority_suggestion": "normal",
      "report_value_avg": 3.0,
      "representative_item_rate": 0.0,
      "review_status": "pending",
      "source_id": "socialmedia-groq-inc-groqinc",
      "source_item_rate": 0.5,
      "source_material_rate": 0.5,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    },
    {
      "created_at": "2026-05-16T18:40:24.050921+00:00",
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
      "source_id": "socialmedia-ian-goodfellow-goodfellow-ian",
      "source_item_rate": 0.0,
      "source_material_rate": 0.0,
      "total_items": 5,
      "updated_at": "2026-05-16T18:40:24.050921+00:00"
    }
  ]
}
```

## 9. Token / Latency / Cache Summary

```json
[
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 26179.4,
    "cache_hit_tokens": 34048,
    "cache_miss_tokens": 0,
    "calls": 30,
    "failed": 3,
    "input_tokens": 75080,
    "llm_call_count": 30,
    "operation_count": 30,
    "output_tokens": 80979,
    "p50_latency_ms": 24612,
    "p95_latency_ms": 36350,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 3,
    "skipped": 0,
    "success": 27,
    "task_type": "item_card",
    "total_tokens": 156059
  },
  {
    "avg_candidates_per_call": null,
    "avg_latency_ms": 12725.6,
    "cache_hit_tokens": 15872,
    "cache_miss_tokens": 0,
    "calls": 19,
    "failed": 0,
    "input_tokens": 30428,
    "llm_call_count": 19,
    "operation_count": 147,
    "output_tokens": 25744,
    "p50_latency_ms": 11491,
    "p95_latency_ms": 18572,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 128,
    "success": 19,
    "task_type": "item_relation",
    "total_tokens": 56172
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
    "operation_count": 124,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 124,
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
    "operation_count": 25,
    "output_tokens": 0,
    "p50_latency_ms": 0,
    "p95_latency_ms": 0,
    "parse_failures": 0,
    "rate_limit_errors": 0,
    "retry_count": 0,
    "skipped": 25,
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
  "actual_calls": 49,
  "actual_tokens": 212231,
  "avg_latency_ms": 20962.6,
  "by_task": {
    "cluster_card_patch": {
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
      "task_type": "cluster_card_patch",
      "total_tokens": 0
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
      "avg_latency_ms": 26179.4,
      "cache_hit_tokens": 34048,
      "calls": 30,
      "concurrency": 4,
      "db_lock_errors": 0,
      "failed": 3,
      "p50_latency_ms": 24612,
      "p95_latency_ms": 36350,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 3,
      "success": 27,
      "task_type": "item_card",
      "total_tokens": 156059
    },
    "item_cluster_relation": {
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
      "task_type": "item_cluster_relation",
      "total_tokens": 0
    },
    "item_relation": {
      "avg_latency_ms": 12725.6,
      "cache_hit_tokens": 15872,
      "calls": 19,
      "concurrency": 4,
      "db_lock_errors": 0,
      "failed": 0,
      "p50_latency_ms": 11491,
      "p95_latency_ms": 18572,
      "parse_failures": 0,
      "rate_limit_errors": 0,
      "retry_count": 0,
      "success": 19,
      "task_type": "item_relation",
      "total_tokens": 56172
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
  "cache_hit_rate": 0.2352,
  "cache_hit_tokens": 49920,
  "calls_per_sec": 0.1231,
  "db_lock_errors": 0,
  "duration_seconds": 398.016,
  "final_failures": 3,
  "max_concurrency": 4,
  "p50_latency_ms": 20752,
  "p95_latency_ms": 33846,
  "parse_failures": 0,
  "rate_limit_errors": 0,
  "repair_retry_count": 3,
  "tokens_per_sec": 533.22
}
```

## 11. Errors / Fallbacks / Retries

```json
{
  "db_lock_errors": 0,
  "final_failures": 3,
  "llm_parse_failures": 0,
  "repair_retry_count": 3,
  "review_queue_entries_due_to_failure": 252,
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
    "concurrency": 4,
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
  "cluster_signal_count": 22,
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
