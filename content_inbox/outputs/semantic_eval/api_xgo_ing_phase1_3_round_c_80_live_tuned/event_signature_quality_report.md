# Event Signature Quality Report

- total_items: 80
- accepted_signature_count: 11
- rejected_signature_count: 69
- borderline_signature_count: 0
- valid_signature_rate: 0.1375

## Invalid Reasons

{
  "missing_concrete_actor_or_product": 33,
  "missing_concrete_event_action": 66,
  "weak_action_without_entity": 31
}

## Top Signatures

[
  {
    "examples": [
      "Security is Job #0 for AI Engineers. Our friends at @snyksec are bringing the AI Security Summit to..."
    ],
    "item_count": 1,
    "signature_key": "unknown|may14|security|2026-05-12"
  },
  {
    "examples": [
      "paper: https://t.co/fkR2wVD129"
    ],
    "item_count": 1,
    "signature_key": "unknown|fkr2wvd129|paper|2026-05-13"
  },
  {
    "examples": [
      "paper: https://t.co/nRjIqRD2fg"
    ],
    "item_count": 1,
    "signature_key": "unknown|nrjiqrd2fg|paper|2026-05-13"
  },
  {
    "examples": [
      "Curious what people are running locally these days 👀"
    ],
    "item_count": 1,
    "signature_key": "unknown|forupdatesfrommyphonehermesagent|featureupdate|2026-05-13"
  },
  {
    "examples": [
      "clarifying how much “task horizon” falls off as a function of the increasing accuracy criterion dir..."
    ],
    "item_count": 1,
    "signature_key": "unknown|for50|benchmark|2026-05-13"
  },
  {
    "examples": [
      "OpenShell v0.0.40 🔀 local-domain service routing in the gateway ☸️ k8s node scheduling + toleratio..."
    ],
    "item_count": 1,
    "signature_key": "nvidia|k8s|security|2026-05-13"
  },
  {
    "examples": [
      "Modern (@mdrnhq) is building the AI-native operating system for IT, with secure agents that automate..."
    ],
    "item_count": 1,
    "signature_key": "unknown|withsecureagents|launch|2026-05-13"
  },
  {
    "examples": [
      "田渊栋 (前 Meta FAIR Director) 以联合创始人身份正式官宣新公司：Recursive @Recursive_SI Recursive 的使命是构建递归自改进超智能 (Recur..."
    ],
    "item_count": 1,
    "signature_key": "meta|our25|launch|2026-05-14"
  },
  {
    "examples": [
      "PLAN0 (@PLAN0AI) turns architectural plans into construction cost estimates and analytics in minutes..."
    ],
    "item_count": 1,
    "signature_key": "unknown|plan0|launch|2026-05-14"
  },
  {
    "examples": [
      "YouArt (@YouArtStudio) empowers storytellers to create AI films and series with leading video agents..."
    ],
    "item_count": 1,
    "signature_key": "unknown|filmsandserieswithleadingvideoagents|launch|2026-05-14"
  },
  {
    "examples": [
      "Concerning."
    ],
    "item_count": 1,
    "signature_key": "unknown|coordinatedoppositioncampaignsaroundourutahprojects|funding|2026-05-16"
  }
]

## Accepted Examples

[
  {
    "action": "security",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-12",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_3067df504cf4433888188c024bac275c",
    "object": "",
    "product_or_model": "May 14",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|may14|security|2026-05-12",
    "source_id": "socialmedia-ai-engineer-aidotengineer",
    "source_item_ids": [
      "item_3067df504cf4433888188c024bac275c"
    ],
    "source_name": "AI Engineer(@aiDotEngineer)",
    "source_type": "social",
    "supporting_tokens": [
      "abstract",
      "act",
      "ai.engineer",
      "at",
      "being",
      "bringing",
      "by",
      "engineers",
      "eu",
      "friends",
      "governance",
      "grab",
      "here",
      "is",
      "job",
      "london",
      "may",
      "meets",
      "on",
      "our"
    ],
    "time_window_hours": 72.0,
    "title": "Security is Job #0 for AI Engineers. Our friends at @snyksec are bringing the AI Security Summit to..."
  },
  {
    "action": "paper",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_6425c9a49e3544649568bd7036bfcdb8",
    "object": "",
    "product_or_model": "fkR2wVD129",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|fkr2wvd129|paper|2026-05-13",
    "source_id": "socialmedia-ak-akhaliq",
    "source_item_ids": [
      "item_6425c9a49e3544649568bd7036bfcdb8"
    ],
    "source_name": "AK(@_akhaliq)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "fkr2wvd129",
      "huggingface.co",
      "papers"
    ],
    "time_window_hours": 72.0,
    "title": "paper: https://t.co/fkR2wVD129"
  },
  {
    "action": "paper",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_b86f4bea90924975a2f1aef786aff460",
    "object": "",
    "product_or_model": "nRjIqRD2fg",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|nrjiqrd2fg|paper|2026-05-13",
    "source_id": "socialmedia-ak-akhaliq",
    "source_item_ids": [
      "item_b86f4bea90924975a2f1aef786aff460"
    ],
    "source_name": "AK(@_akhaliq)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "huggingface.co",
      "nrjiqrd2fg",
      "papers"
    ],
    "time_window_hours": 72.0,
    "title": "paper: https://t.co/nRjIqRD2fg"
  },
  {
    "action": "feature_update",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_6ec5265251ab401284ced9735bc9d28d",
    "object": "all 8",
    "product_or_model": "for updates from my phone. hermes agent",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|forupdatesfrommyphonehermesagent|featureupdate|2026-05-13",
    "source_id": "socialmedia-nvidia-ai-nvidiaai",
    "source_item_ids": [
      "item_6ec5265251ab401284ced9735bc9d28d"
    ],
    "source_name": "NVIDIA AI(@NVIDIAAI)",
    "source_type": "social",
    "supporting_tokens": [
      "alive",
      "asked",
      "autonomously",
      "back",
      "be",
      "by",
      "came",
      "curious",
      "days",
      "dgx",
      "didn",
      "done",
      "future",
      "green",
      "here",
      "hermes",
      "is",
      "it",
      "just",
      "locally"
    ],
    "time_window_hours": 72.0,
    "title": "Curious what people are running locally these days 👀"
  },
  {
    "action": "benchmark",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_428448fad72a46e18b3ee3561e59776b",
    "object": "up 80",
    "product_or_model": "for 50",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|for50|benchmark|2026-05-13",
    "source_id": "socialmedia-gary-marcus-garymarcus",
    "source_item_ids": [
      "item_428448fad72a46e18b3ee3561e59776b"
    ],
    "source_name": "Gary Marcus(@GaryMarcus)",
    "source_type": "social",
    "supporting_tokens": [
      "accuracy",
      "always",
      "as",
      "bad",
      "be",
      "below",
      "but",
      "by",
      "clarify",
      "clarifying",
      "criterion",
      "definitely",
      "dir",
      "directly",
      "edelman",
      "engineering",
      "estimation",
      "etc",
      "falls",
      "function"
    ],
    "time_window_hours": 72.0,
    "title": "clarifying how much “task horizon” falls off as a function of the increasing accuracy criterion dir..."
  },
  {
    "action": "security",
    "actor": "NVIDIA",
    "actor_type": "organization",
    "concreteness_score": 1.0,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_9353d0480b5d4303bb2e9d8bb3983f5a",
    "object": "",
    "product_or_model": "k8s",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "nvidia|k8s|security|2026-05-13",
    "source_id": "socialmedia-nvidia-ai-nvidiaai",
    "source_item_ids": [
      "item_9353d0480b5d4303bb2e9d8bb3983f5a"
    ],
    "source_name": "NVIDIA AI(@NVIDIAAI)",
    "source_type": "social",
    "supporting_tokens": [
      "alongside",
      "by",
      "cli",
      "control",
      "debug",
      "fixes",
      "gateway",
      "github.com",
      "in",
      "k8s",
      "leaks",
      "local-domain",
      "longer",
      "no",
      "node",
      "nvidia",
      "openshe",
      "openshell",
      "os",
      "routing"
    ],
    "time_window_hours": 72.0,
    "title": "OpenShell v0.0.40 🔀 local-domain service routing in the gateway ☸️ k8s node scheduling + toleratio..."
  },
  {
    "action": "launch",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_56610f563a81415c9ed9aac9437f6ae0",
    "object": "",
    "product_or_model": "with secure agents",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|withsecureagents|launch|2026-05-13",
    "source_id": "socialmedia-y-combinator-ycombinator",
    "source_item_ids": [
      "item_56610f563a81415c9ed9aac9437f6ae0"
    ],
    "source_name": "Y Combinator(@ycombinator)",
    "source_type": "social",
    "supporting_tokens": [
      "ai-native",
      "alextomovski",
      "automate",
      "building",
      "by",
      "congrats",
      "desk",
      "devices",
      "does",
      "end-to-end",
      "help",
      "is",
      "it",
      "mdrnhq",
      "mkujkugamh",
      "modern",
      "not",
      "off-boarding",
      "on",
      "operating"
    ],
    "time_window_hours": 72.0,
    "title": "Modern (@mdrnhq) is building the AI-native operating system for IT, with secure agents that automate..."
  },
  {
    "action": "launch",
    "actor": "Meta",
    "actor_type": "organization",
    "concreteness_score": 1.0,
    "date_bucket": "2026-05-14",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_336cf2f457b647ff8a59fdd5d590c528",
    "object": "",
    "product_or_model": "Our 25",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "meta|our25|launch|2026-05-14",
    "source_id": "socialmedia-meng-shao-shao-meng",
    "source_item_ids": [
      "item_336cf2f457b647ff8a59fdd5d590c528"
    ],
    "source_name": "meng shao(@shao__meng)",
    "source_type": "social",
    "supporting_tokens": [
      "advance",
      "agentic",
      "alexey",
      "algorithm",
      "amd",
      "an",
      "architecture",
      "at",
      "automatically",
      "be",
      "bring",
      "building",
      "by",
      "caiming",
      "ceo",
      "change",
      "clune",
      "conviction",
      "could",
      "deepmind"
    ],
    "time_window_hours": 72.0,
    "title": "田渊栋 (前 Meta FAIR Director) 以联合创始人身份正式官宣新公司：Recursive @Recursive_SI Recursive 的使命是构建递归自改进超智能 (Recur..."
  },
  {
    "action": "launch",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-14",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_ce3cfb151a984123a49a53b5d7a4db4b",
    "object": "PLAN0AI",
    "product_or_model": "PLAN0",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|plan0|launch|2026-05-14",
    "source_id": "socialmedia-y-combinator-ycombinator",
    "source_item_ids": [
      "item_ce3cfb151a984123a49a53b5d7a4db4b"
    ],
    "source_name": "Y Combinator(@ycombinator)",
    "source_type": "social",
    "supporting_tokens": [
      "abaratiiii",
      "analytics",
      "architectural",
      "bloomberg",
      "building",
      "by",
      "congrats",
      "construction",
      "cost",
      "dimitris",
      "does",
      "estimates",
      "in",
      "launches",
      "minutes",
      "not",
      "of",
      "on",
      "plan0",
      "plan0ai"
    ],
    "time_window_hours": 72.0,
    "title": "PLAN0 (@PLAN0AI) turns architectural plans into construction cost estimates and analytics in minutes..."
  },
  {
    "action": "launch",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-14",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_cf0515fcd3a14c0d890cd7abc5f5e646",
    "object": "zhenghy723",
    "product_or_model": "films and series with leading video agents",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": "unknown|filmsandserieswithleadingvideoagents|launch|2026-05-14",
    "source_id": "socialmedia-y-combinator-ycombinator",
    "source_item_ids": [
      "item_cf0515fcd3a14c0d890cd7abc5f5e646"
    ],
    "source_name": "Y Combinator(@ycombinator)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "congrats",
      "create",
      "does",
      "early",
      "earn",
      "edmakethings",
      "empowers",
      "fans",
      "films",
      "funded",
      "leading",
      "not",
      "oewws4cb2",
      "on",
      "revenue",
      "series",
      "storytellers",
      "subscription",
      "support"
    ],
    "time_window_hours": 72.0,
    "title": "YouArt (@YouArtStudio) empowers storytellers to create AI films and series with leading video agents..."
  }
]

## Rejected Examples

[
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-12",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_2e8748de572e4ee38e1aa1186dad65fe",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-lenny-rachitsky-lennysan",
    "source_item_ids": [
      "item_2e8748de572e4ee38e1aa1186dad65fe"
    ],
    "source_name": "Lenny Rachitsky(@lennysan)",
    "source_type": "social",
    "supporting_tokens": [
      "advice",
      "by",
      "grant",
      "great",
      "lee",
      "thisisgrantlee"
    ],
    "time_window_hours": 72.0,
    "title": "Great advice"
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-12",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_0be43f87ff76474aadee26a8741e9e31",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-lenny-rachitsky-lennysan",
    "source_item_ids": [
      "item_0be43f87ff76474aadee26a8741e9e31"
    ],
    "source_name": "Lenny Rachitsky(@lennysan)",
    "source_type": "social",
    "supporting_tokens": [
      "banger",
      "by",
      "tdrobbo",
      "tom",
      "verrilli"
    ],
    "time_window_hours": 72.0,
    "title": "Banger"
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.5,
    "date_bucket": "2026-05-12",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_a3ecca2a219e4d7b89c51bdee8157c0d",
    "object": "",
    "product_or_model": "Nemotron 3",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-nvidia-ai-nvidiaai",
    "source_item_ids": [
      "item_a3ecca2a219e4d7b89c51bdee8157c0d"
    ],
    "source_name": "NVIDIA AI(@NVIDIAAI)",
    "source_type": "social",
    "supporting_tokens": [
      "ask",
      "broadcasts",
      "by",
      "experts",
      "labs",
      "nano",
      "nemotron",
      "nwqposev",
      "omni"
    ],
    "time_window_hours": 72.0,
    "title": "Ask the Experts: Nemotron 3 Nano Omni | Nemotron Labs https://t.co/35NWqpOseV"
  },
  {
    "action": "other",
    "actor": "Google",
    "actor_type": "organization",
    "concreteness_score": 0.48,
    "date_bucket": "2026-05-12",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_a5427d9ae1a34bbebcce09738422f478",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-imxiaohu",
    "source_item_ids": [
      "item_a5427d9ae1a34bbebcce09738422f478"
    ],
    "source_name": "小互(@imxiaohu)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "does",
      "gemini",
      "google",
      "googlebook",
      "laptop",
      "not",
      "on",
      "os",
      "support",
      "tag",
      "video",
      "your",
      "东西",
      "为核心的",
      "主动组织操作",
      "人打开",
      "人操作功能",
      "他们想做的已经不",
      "以前电脑逻辑"
    ],
    "time_window_hours": 72.0,
    "title": "Google 刚刚发布了一个新东西：Googlebook 根据Google 自己的表述： 他们想做的已经不再是传统意义上的“操作系统”，而是一个以 Gemini 为核心的 AI Laptop 平台..."
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_063c93ebca06426ea4816cba64452dcc",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-orange-ai-oran-ge",
    "source_item_ids": [
      "item_063c93ebca06426ea4816cba64452dcc"
    ],
    "source_name": "orange.ai(@oran_ge)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "ch",
      "cheap",
      "is",
      "knowhow",
      "not",
      "talk",
      "不存在个人英雄主",
      "出来",
      "可能存在一定的组",
      "啥的没那么重要",
      "大实话了哈哈",
      "大模型这事儿现在",
      "太简单了",
      "把事情踏踏实实做",
      "织英雄主义",
      "这期播客实在是太",
      "重要的是把事情做",
      "靠谱"
    ],
    "time_window_hours": 72.0,
    "title": "这期播客实在是太大实话了哈哈 大模型这事儿现在太简单了 不存在个人英雄主义 可能存在一定的组织英雄主义 knowhow 啥的没那么重要，重要的是把事情做出来，把事情踏踏实实做好 talk is ch..."
  },
  {
    "action": "other",
    "actor": "Gemini",
    "actor_type": "organization",
    "concreteness_score": 0.8,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_8a1c922a42aa475695ac012267fb87da",
    "object": "Claude Code",
    "product_or_model": "Gemini Intelligence",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-the-rundown-ai-therundownai",
    "source_item_ids": [
      "item_8a1c922a42aa475695ac012267fb87da"
    ],
    "source_name": "The Rundown AI(@TheRundownAI)",
    "source_type": "social",
    "supporting_tokens": [
      "amazon",
      "analyst",
      "android",
      "by",
      "circles",
      "claude",
      "code",
      "community",
      "compute",
      "gemini",
      "google",
      "googlebooks",
      "in",
      "incentives",
      "intelligence",
      "more",
      "orbital",
      "scoreboard",
      "spacex",
      "stories"
    ],
    "time_window_hours": 72.0,
    "title": "Top stories in AI today: - New Googlebooks, Gemini Intelligence for Android - Google circles SpaceX..."
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.5,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_faf5b65812884bf1b19d5ef1539b2b7b",
    "object": "",
    "product_or_model": "yZgH0hEATU",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-the-rundown-ai-therundownai",
    "source_item_ids": [
      "item_faf5b65812884bf1b19d5ef1539b2b7b"
    ],
    "source_name": "The Rundown AI(@TheRundownAI)",
    "source_type": "social",
    "supporting_tokens": [
      "android-ente",
      "by",
      "more",
      "therundown.ai",
      "yzgh0heatu"
    ],
    "time_window_hours": 72.0,
    "title": "Read more: https://t.co/yZgH0hEATU"
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.5,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_b7b9d50b750c4d22a656b312736efd60",
    "object": "",
    "product_or_model": "U1",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-ak-akhaliq",
    "source_item_ids": [
      "item_b7b9d50b750c4d22a656b312736efd60"
    ],
    "source_name": "AK(@_akhaliq)",
    "source_type": "social",
    "supporting_tokens": [
      "architecture",
      "by",
      "generation",
      "multimodal",
      "neo-unify",
      "sensenova-u1",
      "understanding",
      "unifying"
    ],
    "time_window_hours": 72.0,
    "title": "SenseNova-U1 Unifying Multimodal Understanding and Generation with NEO-unify Architecture"
  },
  {
    "action": "benchmark",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.38,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [
      "missing_concrete_actor_or_product"
    ],
    "is_concrete": false,
    "item_id": "item_91246a627dc04ee8b94c637bff54d8de",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-ak-akhaliq",
    "source_item_ids": [
      "item_91246a627dc04ee8b94c637bff54d8de"
    ],
    "source_name": "AK(@_akhaliq)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "egocentric",
      "egomemreason",
      "long-horizon",
      "memory-driven",
      "reasoning",
      "understanding",
      "video"
    ],
    "time_window_hours": 72.0,
    "title": "EgoMemReason A Memory-Driven Reasoning Benchmark for Long-Horizon Egocentric Video Understanding"
  },
  {
    "action": "other",
    "actor": "Nvidia",
    "actor_type": "organization",
    "concreteness_score": 0.48,
    "date_bucket": "2026-05-13",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_4e57b89e89224128951f7fd22403b804",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104806_662651",
    "signature_key": null,
    "source_id": "socialmedia-the-rundown-ai-therundownai",
    "source_item_ids": [
      "item_4e57b89e89224128951f7fd22403b804"
    ],
    "source_name": "The Rundown AI(@TheRundownAI)",
    "source_type": "social",
    "supporting_tokens": [
      "asked",
      "became",
      "by",
      "cap",
      "ceo",
      "company",
      "extremely",
      "first",
      "fridman",
      "getting",
      "growth",
      "he",
      "hit",
      "huang",
      "if",
      "in",
      "inevitable",
      "is",
      "jensen",
      "lex"
    ],
    "time_window_hours": 72.0,
    "title": "NEW: Nvidia became the first company to hit a $5.5T market cap today. CEO Jensen Huang, when asked..."
  }
]
