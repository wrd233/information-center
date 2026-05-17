# Event Signature Quality Report

- total_items: 20
- accepted_signature_count: 1
- rejected_signature_count: 19
- borderline_signature_count: 0
- valid_signature_rate: 0.05

## Invalid Reasons

{
  "missing_concrete_actor_or_product": 11,
  "missing_concrete_event_action": 19,
  "weak_action_without_entity": 11
}

## Top Signatures

[
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
    "action": "funding",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.7,
    "date_bucket": "2026-05-16",
    "invalid_reasons": [],
    "is_concrete": true,
    "item_id": "item_ccd79db5948543df9ef8b5b040aa544a",
    "object": "Form 990",
    "product_or_model": "coordinated opposition campaigns around our Utah projects",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": "unknown|coordinatedoppositioncampaignsaroundourutahprojects|funding|2026-05-16",
    "source_id": "socialmedia-marc-andreessen-127482-127480-pmarca",
    "source_item_ids": [
      "item_ccd79db5948543df9ef8b5b040aa544a"
    ],
    "source_name": "Marc Andreessen 🇺🇸(@pmarca)",
    "source_type": "social",
    "supporting_tokens": [
      "activity",
      "against",
      "aggressive",
      "aka",
      "alliance",
      "american",
      "amount",
      "an",
      "appears",
      "arabella",
      "audit",
      "back",
      "been",
      "behind",
      "box",
      "by",
      "called",
      "campaigns",
      "capacity",
      "center"
    ],
    "time_window_hours": 72.0,
    "title": "Concerning."
  }
]

## Rejected Examples

[
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.5,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_af382c80ea774c2c8767929d81e21c55",
    "object": "genaisummit26",
    "product_or_model": "SF 2026",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-ai-will-financeyf5",
    "source_item_ids": [
      "item_af382c80ea774c2c8767929d81e21c55"
    ],
    "source_name": "AI Will(@FinanceYF5)",
    "source_type": "social",
    "supporting_tokens": [
      "arts",
      "by",
      "code",
      "eventbrite",
      "eventbrite.com",
      "financeyf5",
      "fine",
      "genai",
      "genaisummit26",
      "luma",
      "luma.com",
      "natetepper",
      "of",
      "offer",
      "palace",
      "sf",
      "sta",
      "summit",
      "一次的地方",
      "专属"
    ],
    "time_window_hours": 72.0,
    "title": "@NateTepper GenAI Summit SF 2026：湾区数万人大会！ 🔗 Will粉丝专属购票链接（可享受15%优惠）： 专属Code：WILL 专属链接： Luma：https:/..."
  },
  {
    "action": "other",
    "actor": "Claude",
    "actor_type": "organization",
    "concreteness_score": 0.8,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_f67243a37bc5418e90a8e45086c47ad6",
    "object": "in 60",
    "product_or_model": "Claude Code",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-ai-will-financeyf5",
    "source_item_ids": [
      "item_f67243a37bc5418e90a8e45086c47ad6"
    ],
    "source_name": "AI Will(@FinanceYF5)",
    "source_type": "social",
    "supporting_tokens": [
      "bands",
      "bollinger",
      "by",
      "callable",
      "candles",
      "claude",
      "cli",
      "code",
      "company",
      "connect",
      "does",
      "financial",
      "full",
      "fundamentals",
      "here",
      "in",
      "indicators",
      "language",
      "natural",
      "not"
    ],
    "time_window_hours": 72.0,
    "title": "金融分析的门槛正在被 AI 降低。 QVeris CLI 把 candles、RSI、布林带、公司基本面接进 Claude Code，用户不用写复杂脚本，也能让 agent 调工具跑分析。 这类小..."
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_23a5dc395df64370bc502a4bf26b5d1d",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-vista8",
    "source_item_ids": [
      "item_23a5dc395df64370bc502a4bf26b5d1d"
    ],
    "source_name": "向阳乔木(@vista8)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "skill",
      "优秀模型",
      "就是顶级翻译学习",
      "工具"
    ],
    "time_window_hours": 72.0,
    "title": "优秀模型 + Skill 就是顶级翻译学习工具。"
  },
  {
    "action": "other",
    "actor": "Anthropic",
    "actor_type": "organization",
    "concreteness_score": 0.48,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_edd2e2a4edf04a3ab9850e65ee25d7a7",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-ai-will-financeyf5",
    "source_item_ids": [
      "item_edd2e2a4edf04a3ab9850e65ee25d7a7"
    ],
    "source_name": "AI Will(@FinanceYF5)",
    "source_type": "social",
    "supporting_tokens": [
      "anthropic",
      "by",
      "index",
      "openai",
      "ramp",
      "tryramp",
      "上超越",
      "仅增长",
      "显示",
      "最新一期",
      "根据",
      "的企业在使用",
      "的数据",
      "的采用率翻了四倍",
      "过去一年",
      "首次在企业采用率"
    ],
    "time_window_hours": 72.0,
    "title": "Anthropic 首次在企业采用率上超越 OpenAI。 根据 tryramp 的数据，最新一期 Ramp AI Index 显示，34.4% 的企业在使用 Anthropic，OpenAI 为 ..."
  },
  {
    "action": "other",
    "actor": "Anthropic",
    "actor_type": "organization",
    "concreteness_score": 0.8,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_28e4e83bd46645248c84db9be971c792",
    "object": "Gemini Flash",
    "product_or_model": "Claude Opus",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-vista8",
    "source_item_ids": [
      "item_28e4e83bd46645248c84db9be971c792"
    ],
    "source_name": "向阳乔木(@vista8)",
    "source_type": "social",
    "supporting_tokens": [
      "anthropic",
      "arena",
      "b2b",
      "by",
      "claude",
      "flash",
      "gemini",
      "google",
      "opus",
      "token",
      "vercel",
      "一次",
      "万个项目",
      "个月十万亿个",
      "个月翻近一倍",
      "个模型",
      "份额越高",
      "便宜量大",
      "却占了",
      "原文见评论"
    ],
    "time_window_hours": 72.0,
    "title": "哪个模型最牛逼？arena榜都被刷烂了。 要看就看 Vercel的最新报告。 20万个项目，7个月十万亿个 token的消耗分析，有些结论有意思： 1. 按费用消耗 Anthropic 占 61..."
  },
  {
    "action": "other",
    "actor": "vercel",
    "actor_type": "organization",
    "concreteness_score": 0.8,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_afc540a05b514eae87b97f6f5e8d811a",
    "object": "",
    "product_or_model": "pVTjim12Ce",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-vista8",
    "source_item_ids": [
      "item_afc540a05b514eae87b97f6f5e8d811a"
    ],
    "source_name": "向阳乔木(@vista8)",
    "source_type": "social",
    "supporting_tokens": [
      "ai-gatewa",
      "bhyueybctw",
      "blog.qiaomu.ai",
      "by",
      "pvtjim12ce",
      "vercel-ai-gate",
      "vercel.com",
      "原文",
      "翻译"
    ],
    "time_window_hours": 72.0,
    "title": "原文：https://t.co/pVTjim12Ce 翻译：https://t.co/BhYuEybcTW"
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_eb8362be434c4275b51663cda6a50d61",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-nvidia-ai-nvidiaai",
    "source_item_ids": [
      "item_eb8362be434c4275b51663cda6a50d61"
    ],
    "source_name": "NVIDIA AI(@NVIDIAAI)",
    "source_type": "social",
    "supporting_tokens": [
      "astronomy",
      "based",
      "box",
      "by",
      "capabilities",
      "chance",
      "compute",
      "confident",
      "cruz",
      "deploying",
      "desk",
      "develop",
      "developer",
      "dgx",
      "first",
      "future",
      "good",
      "gpu-accelerated",
      "headed",
      "if"
    ],
    "time_window_hours": 72.0,
    "title": "If Luigi knows you, there’s a good chance a box is headed to your desk soon"
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_b775bb7e31734fa5bc3eaa7798c43e48",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-orange-ai-oran-ge",
    "source_item_ids": [
      "item_b775bb7e31734fa5bc3eaa7798c43e48"
    ],
    "source_name": "orange.ai(@oran_ge)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "game",
      "in",
      "skin",
      "也就不能做出正确",
      "人只有在真实的环",
      "人类学研究表明",
      "人类的决策过程主",
      "再用智慧去寻找证",
      "决定",
      "决定是正确的",
      "在压力下产生这些",
      "境里才能做出正确",
      "如果决策者本人不",
      "定之后",
      "就不能身临其境地",
      "我们往往是做出决",
      "所起的作用并不大",
      "承担决策失误的风",
      "据以便证明自己的"
    ],
    "time_window_hours": 72.0,
    "title": "人只有在真实的环境里才能做出正确的决定。 人类学研究表明，人类的决策过程主要是由激素推动的，知识，经验，理智在这个过程中所起的作用并不大。 我们往往是做出决定之后，再用智慧去寻找证据以便证明自己的决定..."
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_cb012df29f564fd7a9c387eab75f01f2",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-orange-ai-oran-ge",
    "source_item_ids": [
      "item_cb012df29f564fd7a9c387eab75f01f2"
    ],
    "source_name": "orange.ai(@oran_ge)",
    "source_type": "social",
    "supporting_tokens": [
      "by",
      "实践是获得真理和",
      "获悉真相的唯一途"
    ],
    "time_window_hours": 72.0,
    "title": "实践是获得真理和获悉真相的唯一途径。"
  },
  {
    "action": "other",
    "actor": "",
    "actor_type": "unknown",
    "concreteness_score": 0.18,
    "date_bucket": "2026-05-15",
    "invalid_reasons": [
      "missing_concrete_actor_or_product",
      "weak_action_without_entity",
      "missing_concrete_event_action"
    ],
    "is_concrete": false,
    "item_id": "item_5003e0afa4fd4dbeb1ae9165e9b91884",
    "object": "",
    "product_or_model": "",
    "semantic_run_id": "semantic_eval_20260517_104124_987779",
    "signature_key": null,
    "source_id": "socialmedia-nvidia-ai-nvidiaai",
    "source_item_ids": [
      "item_5003e0afa4fd4dbeb1ae9165e9b91884"
    ],
    "source_name": "NVIDIA AI(@NVIDIAAI)",
    "source_type": "social",
    "supporting_tokens": [
      "arcee_ai",
      "by",
      "closed",
      "xeophon"
    ],
    "time_window_hours": 72.0,
    "title": "@xeophon @arcee_ai Open > closed"
  }
]
