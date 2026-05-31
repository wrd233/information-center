# 事件去重与聚合深度诊断

生成时间: 2026-05-31T12:17:36.341213+00:00

## 第一性原理定义

你的目标不是把“相似标题”放在一起，而是把多条信息映射到同一个现实世界事件，并保留它们之间的信息增量。一个合格事件聚合系统至少要回答四个问题：

1. 这是不是事件，还是日报、综述、教程、观点、主题线索？
2. 如果是事件，它的主体、对象、动作、时间窗口是什么？
3. 两条内容是同一事件、同一主题不同事件、同一产品不同进展，还是纯重复？
4. 合并后是否新增事实、角度或证据，是否值得进入简报？

本轮状态: **不通过**。当前作战台接入的是 lightweight 标题规则，语义聚合模块存在但没有进入这条 console pipeline。

## 对照实验

| 方法 | Precision | Recall | F1 | TP | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| 当前 lightweight 完全标题 | 54.5% | 30.0% | 38.7% | 6 | 5 | 14 |
| semantic signature 精确匹配 | 100.0% | 45.0% | 62.1% | 9 | 0 | 11 |
| semantic candidate high | 68.8% | 55.0% | 61.1% | 11 | 5 | 9 |
| semantic candidate medium+ | 8.9% | 55.0% | 15.4% | 11 | 112 | 9 |

Gold same-event pair 数: 20；Gold 非事件 pair 数: 10。

### 当前 lightweight 失败样例

- 误合并: `[('daily_digest_a', 'daily_digest_b'), ('daily_digest_a', 'daily_digest_c'), ('daily_digest_b', 'daily_digest_c'), ('generic_title_a', 'generic_title_b'), ('market_wrap_a', 'market_wrap_b')]`
- 漏合并: `[('anthropic_funding_a', 'anthropic_funding_b'), ('deepseek_cn_a', 'deepseek_cn_b'), ('deepseek_cn_a', 'guid_a'), ('deepseek_cn_a', 'guid_b'), ('deepseek_cn_b', 'guid_a'), ('deepseek_cn_b', 'guid_b'), ('openai_punctuation_variant', 'openai_variant_a'), ('openai_punctuation_variant', 'openai_variant_b'), ('openai_variant_a', 'openai_variant_b'), ('openai_variant_a', 'url_tracking_a'), ('openai_variant_a', 'url_tracking_b'), ('openai_variant_b', 'url_tracking_a')]`

### semantic candidate 失败样例

- high 阈值误合并: `[('daily_digest_a', 'daily_digest_b'), ('daily_digest_a', 'daily_digest_c'), ('daily_digest_b', 'daily_digest_c'), ('generic_title_a', 'generic_title_b'), ('market_wrap_a', 'market_wrap_b')]`
- high 阈值漏合并: `[('anthropic_funding_a', 'anthropic_funding_b'), ('openai_punctuation_variant', 'openai_variant_a'), ('openai_variant_a', 'openai_variant_b'), ('openai_variant_a', 'url_tracking_a'), ('openai_variant_a', 'url_tracking_b'), ('openai_variant_b', 'url_tracking_a'), ('openai_variant_b', 'url_tracking_b'), ('policy_a', 'policy_b'), ('title_date_a', 'title_date_b')]`
- medium+ 阈值误合并: `[('anthropic_funding_b', 'background_25'), ('anthropic_funding_b', 'background_55'), ('background_01', 'background_07'), ('background_01', 'background_31'), ('background_02', 'background_08'), ('background_02', 'background_32'), ('background_02', 'background_56'), ('background_03', 'background_09'), ('background_03', 'background_33'), ('background_03', 'background_57'), ('background_04', 'background_10'), ('background_04', 'background_28')]`
- medium+ 阈值漏合并: `[('anthropic_funding_a', 'anthropic_funding_b'), ('openai_punctuation_variant', 'openai_variant_a'), ('openai_variant_a', 'openai_variant_b'), ('openai_variant_a', 'url_tracking_a'), ('openai_variant_a', 'url_tracking_b'), ('openai_variant_b', 'url_tracking_a'), ('openai_variant_b', 'url_tracking_b'), ('policy_a', 'policy_b'), ('title_date_a', 'title_date_b')]`

## 根因拆解

### 1. 接入根因

console pipeline 调用的是 `generate_information_objects()`，其聚合键是 `normalized_title(title)`。这意味着：

- 同一事件只要标题改写，就会漏合并。
- 不同事件只要标题模板相同，就会误合并。
- digest / roundup / market wrap 这类非事件也会被创建为事件。
- 事件类型、摘要、增量价值没有真实推断，只是占位字段。

### 2. 当前 DB 信号

```json
{
  "exists": true,
  "path": "/Users/wangrundong/work/infomation-center/content_inbox/data/content_inbox.sqlite3",
  "table_counts": {
    "rss_sources": 151,
    "rss_ingest_runs": 763,
    "item_run_links": 200,
    "inbox_items": 3278,
    "event_clusters": 1257,
    "cluster_items": 207,
    "events": 198,
    "review_queue": 226,
    "dedupe_groups": 0,
    "dedupe_group_items": 0,
    "item_cards": 90,
    "item_relations": 86,
    "cluster_cards": 10,
    "llm_call_logs": 86
  },
  "source_status_stats": [
    {
      "status": "active",
      "n": 150
    },
    {
      "status": "broken",
      "n": 1
    }
  ],
  "item_seen_stats": {
    "items": 3278,
    "items_seen_multiple": 861,
    "max_seen": 10,
    "avg_seen": 1.62,
    "total_seen": 5315
  },
  "cluster_integrity": {
    "clusters": 1257,
    "clusters_without_cluster_items": 1052,
    "item_count_mismatch": 0
  },
  "clusters_by_creator": [
    {
      "created_by": "legacy",
      "clusters": 1052,
      "multi_clusters": 34,
      "avg_items": 1.03,
      "max_items": 3
    },
    {
      "created_by": "lightweight_rule",
      "clusters": 198,
      "multi_clusters": 2,
      "avg_items": 1.01,
      "max_items": 2
    },
    {
      "created_by": "rule",
      "clusters": 7,
      "multi_clusters": 0,
      "avg_items": 1.0,
      "max_items": 1
    }
  ],
  "cluster_relation_stats": [
    {
      "primary_relation": "same_topic",
      "same_event": 0,
      "decision_source": "lightweight_rule",
      "n": 196
    },
    {
      "primary_relation": "new_info",
      "same_event": 1,
      "decision_source": "rule",
      "n": 7
    },
    {
      "primary_relation": "same_event",
      "same_event": 1,
      "decision_source": "lightweight_rule",
      "n": 4
    }
  ],
  "event_type_stats": [
    {
      "event_type": "unknown",
      "status": "needs_review",
      "n": 198
    }
  ],
  "clustering_json_stats": [
    {
      "relation": "skipped_low_value",
      "n": 1969
    },
    {
      "relation": "new_event",
      "n": 1052
    },
    {
      "relation": "embedding_failed",
      "n": 217
    },
    {
      "relation": "incremental_update",
      "n": 28
    },
    {
      "relation": "duplicate",
      "n": 6
    },
    {
      "relation": "disabled",
      "n": 5
    },
    {
      "relation": "uncertain",
      "n": 1
    }
  ],
  "signature_scan": {
    "items_scanned": 3278,
    "semantic_levels": [
      [
        "reject",
        1703
      ],
      [
        "thread_signature",
        884
      ],
      [
        "event_signature",
        672
      ],
      [
        "content_signature",
        19
      ]
    ],
    "top_actions": [
      [
        "other",
        1158
      ],
      [
        "pricing",
        523
      ],
      [
        "feature_update",
        250
      ],
      [
        "integration",
        211
      ],
      [
        "tutorial",
        137
      ],
      [
        "event",
        126
      ],
      [
        "funding",
        121
      ],
      [
        "release",
        115
      ],
      [
        "company_launch",
        108
      ],
      [
        "adoption_metric",
        103
      ],
      [
        "technical_blog",
        96
      ],
      [
        "availability",
        81
      ],
      [
        "benchmark",
        65
      ],
      [
        "research_paper",
        64
      ],
      [
        "case_study",
        50
      ]
    ],
    "top_actors": [
      [
        "Anthropic",
        171
      ],
      [
        "Google",
        130
      ],
      [
        "DeepSeek",
        80
      ],
      [
        "OpenAI/Codex",
        69
      ],
      [
        "OpenAI",
        54
      ],
      [
        "Cursor",
        33
      ],
      [
        "Microsoft",
        25
      ],
      [
        "ChatGPT",
        24
      ],
      [
        "NVIDIA",
        21
      ],
      [
        "Notion",
        20
      ],
      [
        "Meta",
        17
      ],
      [
        "GPT-5.5",
        15
      ],
      [
        "Replit",
        15
      ],
      [
        "Perplexity",
        14
      ],
      [
        "Claude",
        13
      ]
    ],
    "top_products": [
      [
        "Codex",
        63
      ],
      [
        "Claude Code",
        30
      ],
      [
        "aggregated from sources",
        20
      ],
      [
        "bridge",
        16
      ],
      [
        "GPT-5.5",
        16
      ],
      [
        "DeepSeek V4",
        12
      ],
      [
        "codex",
        10
      ],
      [
        "GPT Image",
        10
      ],
      [
        "Gemini API",
        10
      ],
      [
        "Claude Opus",
        9
      ],
      [
        "DeepSeek-V4 Preview",
        8
      ],
      [
        "claudeai",
        7
      ],
      [
        "Gemma 4",
        7
      ],
      [
        "kcm6872.top",
        6
      ],
      [
        "i51 co",
        6
      ]
    ],
    "top_invalid_reasons": [
      [
        "semantic_level_reject",
        1703
      ],
      [
        "missing_concrete_actor_or_product",
        1700
      ],
      [
        "weak_action_without_entity",
        1047
      ],
      [
        "semantic_level_thread_signature",
        884
      ],
      [
        "invalid_product_generic_phrase",
        20
      ],
      [
        "semantic_level_content_signature",
        19
      ],
      [
        "invalid_product_fragment_without_actor",
        13
      ],
      [
        "generic_tokens_only",
        1
      ]
    ],
    "signature_groups": 631,
    "multi_signature_groups": 24,
    "items_in_multi_signature_groups": 56,
    "exact_title_groups": 3214,
    "multi_exact_title_groups": 33,
    "items_in_multi_exact_title_groups": 97
  }
}
```

默认大库提供了更接近真实使用的信号：source/item 数量足够，但历史 legacy cluster、embedding cluster、当前 operational cluster 三套形态混在一起，且大量 cluster 缺少可解释的 `cluster_items` 链接。因此它能说明当前路径和数据债务，但不能直接作为人工标注准确率。

大库额外观察:

- item 去重已经在写入阶段折叠重复：`seen_count > 1` 的 item 很多，但 `dedupe_groups` 为空，后置去重阶段没有解释重复来源。
- legacy cluster 数量多，但多数没有 `cluster_items`，只能看摘要，不能追溯每条证据。
- operational lightweight cluster 几乎都是单成员；多成员样例主要来自完全标题一致，容易被低质泛标题污染。
- signature scan 显示只有一部分 item 能形成可用事件签名，说明事件聚合前必须先做 eventness 和 alias/normalization。

### 3. semantic 模块自身的能力与不足

semantic candidate scorer 明显比完全标题更接近真实需求：它考虑 actor/product/action/time/source diversity/generic overlap。但本轮合成测试显示它还不能直接作为最终答案：

- 根因计数: `{'product_mismatch_or_missing': 9, 'action_mismatch_or_missing': 8, 'a_thread_signature': 4, 'b_thread_signature': 2, 'semantic_level_reject': 2, 'a_reject': 2, 'b_reject': 2, 'actor_mismatch_or_missing': 2}`
- 对 OpenAI GPT-5.5 这类标题，产品抽取常把 `OpenAI launches GPT`、`OpenAI GPT 5.5`、`GPT-5.5` 视作不同产品，导致同事件漏合。
- 对 DeepSeek V4.1 这类中英文混写，中文别名和产品版本标准化不足。
- 对政策类事件，`EU` / `European Commission` 与 `AI Act` 的 actor/product/action 表达不稳定。
- signature 精确匹配偏保守，适合作为高精度 seed，不适合作为唯一聚合依据。

signature/candidate 失败样例:

```json
[
  {
    "pair": [
      "anthropic_funding_a",
      "anthropic_funding_b"
    ],
    "priority": "medium",
    "lane": "same_thread",
    "score": 2.021,
    "signature_a": {
      "level": "thread_signature",
      "actor": "Anthropic",
      "product": "",
      "action": "adoption_metric",
      "key": null,
      "invalid": [
        "semantic_level_thread_signature"
      ]
    },
    "signature_b": {
      "level": "thread_signature",
      "actor": "Anthropic",
      "product": "",
      "action": "funding",
      "key": null,
      "invalid": [
        "semantic_level_thread_signature"
      ]
    },
    "disqualifiers": [],
    "evidence": [
      "shared_weighted_entities:anthropic",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.224,
      "entity_overlap_weighted": 1.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 0.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "openai_punctuation_variant",
      "openai_variant_a"
    ],
    "priority": "medium",
    "lane": "same_thread",
    "score": 5.842,
    "signature_a": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5",
      "action": "release",
      "key": "openai|gpt55|release|2026-05-30",
      "invalid": []
    },
    "signature_b": {
      "level": "thread_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5 model aimed at coding agents",
      "action": "other",
      "key": null,
      "invalid": [
        "semantic_level_thread_signature"
      ]
    },
    "disqualifiers": [],
    "evidence": [
      "shared_weighted_entities:coding, gpt-5.5, gpt55, openai",
      "shared_event_phrases:agent",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.447,
      "entity_overlap_weighted": 4.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 1.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "openai_variant_a",
      "openai_variant_b"
    ],
    "priority": "medium",
    "lane": "same_thread",
    "score": 4.825,
    "signature_a": {
      "level": "thread_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5 model aimed at coding agents",
      "action": "other",
      "key": null,
      "invalid": [
        "semantic_level_thread_signature"
      ]
    },
    "signature_b": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT 5.5 model launches for software agents",
      "action": "integration",
      "key": "openai|gpt55modellaunchesforsoftwareagents|integration|2026-05-30",
      "invalid": []
    },
    "disqualifiers": [],
    "evidence": [
      "shared_weighted_entities:gpt-5.5, gpt55, openai",
      "shared_event_phrases:agent",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.408,
      "entity_overlap_weighted": 3.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 1.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "openai_variant_a",
      "url_tracking_a"
    ],
    "priority": "medium",
    "lane": "same_thread",
    "score": 9.239,
    "signature_a": {
      "level": "thread_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5 model aimed at coding agents",
      "action": "other",
      "key": null,
      "invalid": [
        "semantic_level_thread_signature"
      ]
    },
    "signature_b": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5",
      "action": "release",
      "key": "openai|gpt55|release|2026-05-30",
      "invalid": []
    },
    "disqualifiers": [],
    "evidence": [
      "high_title_similarity",
      "shared_weighted_entities:coding, gpt-5.5, gpt55, openai",
      "same_actor_product_action_72h",
      "shared_event_phrases:agent",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.596,
      "entity_overlap_weighted": 4.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 1.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 1.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "openai_variant_a",
      "url_tracking_b"
    ],
    "priority": "medium",
    "lane": "same_thread",
    "score": 9.239,
    "signature_a": {
      "level": "thread_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5 model aimed at coding agents",
      "action": "other",
      "key": null,
      "invalid": [
        "semantic_level_thread_signature"
      ]
    },
    "signature_b": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5",
      "action": "release",
      "key": "openai|gpt55|release|2026-05-30",
      "invalid": []
    },
    "disqualifiers": [],
    "evidence": [
      "high_title_similarity",
      "shared_weighted_entities:coding, gpt-5.5, gpt55, openai",
      "same_actor_product_action_72h",
      "shared_event_phrases:agent",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.596,
      "entity_overlap_weighted": 4.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 1.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 1.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "openai_variant_b",
      "url_tracking_a"
    ],
    "priority": "medium",
    "lane": "exploratory_recall",
    "score": 5.918,
    "signature_a": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT 5.5 model launches for software agents",
      "action": "integration",
      "key": "openai|gpt55modellaunchesforsoftwareagents|integration|2026-05-30",
      "invalid": []
    },
    "signature_b": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5",
      "action": "release",
      "key": "openai|gpt55|release|2026-05-30",
      "invalid": []
    },
    "disqualifiers": [],
    "evidence": [
      "shared_weighted_entities:gpt-5.5, gpt55, launches, openai",
      "shared_event_phrases:agent, launch",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.548,
      "entity_overlap_weighted": 4.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 0.5,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "openai_variant_b",
      "url_tracking_b"
    ],
    "priority": "medium",
    "lane": "exploratory_recall",
    "score": 6.143,
    "signature_a": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT 5.5 model launches for software agents",
      "action": "integration",
      "key": "openai|gpt55modellaunchesforsoftwareagents|integration|2026-05-30",
      "invalid": []
    },
    "signature_b": {
      "level": "event_signature",
      "actor": "OpenAI",
      "product": "GPT-5.5",
      "action": "release",
      "key": "openai|gpt55|release|2026-05-30",
      "invalid": []
    },
    "disqualifiers": [],
    "evidence": [
      "shared_weighted_entities:gpt-5.5, gpt55, launches, openai",
      "shared_event_phrases:agent, launch",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.548,
      "entity_overlap_weighted": 4.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 1.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 1.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "policy_a",
      "policy_b"
    ],
    "priority": "suppress",
    "lane": "suppressed",
    "score": 5.253,
    "signature_a": {
      "level": "reject",
      "actor": "",
      "product": "",
      "action": "technical_blog",
      "key": null,
      "invalid": [
        "missing_concrete_actor_or_product",
        "semantic_level_reject"
      ]
    },
    "signature_b": {
      "level": "reject",
      "actor": "",
      "product": "",
      "action": "other",
      "key": null,
      "invalid": [
        "missing_concrete_actor_or_product",
        "weak_action_without_entity",
        "semantic_level_reject"
      ]
    },
    "disqualifiers": [
      "semantic_level_reject"
    ],
    "evidence": [
      "shared_weighted_entities:act, ai act, aiact, guidance",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 0.401,
      "entity_overlap_weighted": 4.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 0.0,
      "event_action_overlap": 0.0,
      "event_phrase_overlap": 0.0,
      "time_proximity": 1.0,
      "source_diversity": 1.0,
      "same_source_penalty": 0.0,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  },
  {
    "pair": [
      "title_date_a",
      "title_date_b"
    ],
    "priority": "must_run",
    "lane": "deterministic",
    "score": 6.6,
    "signature_a": {
      "level": "reject",
      "actor": "",
      "product": "",
      "action": "adoption_metric",
      "key": null,
      "invalid": [
        "missing_concrete_actor_or_product",
        "semantic_level_reject"
      ]
    },
    "signature_b": {
      "level": "reject",
      "actor": "",
      "product": "",
      "action": "adoption_metric",
      "key": null,
      "invalid": [
        "missing_concrete_actor_or_product",
        "semantic_level_reject"
      ]
    },
    "disqualifiers": [
      "semantic_level_reject"
    ],
    "evidence": [
      "high_title_similarity",
      "shared_weighted_entities:evaluation, institute, publishes, results, safety",
      "close_time_window"
    ],
    "score_components": {
      "title_similarity": 1.0,
      "entity_overlap_weighted": 5.0,
      "event_signature_match": 0.0,
      "concrete_event_match": 0.0,
      "product_overlap": 0.0,
      "actor_overlap": 0.0,
      "event_action_overlap": 1.0,
      "event_phrase_overlap": 0.0,
      "time_proximity": 1.0,
      "source_diversity": 0.0,
      "same_source_penalty": -0.45,
      "boilerplate_penalty": 0.0,
      "proxy_domain_penalty": 0.0,
      "generic_entity_penalty": 0.0
    }
  }
]
```

## 当前不足

1. 事件定义层缺失：没有先判断 item 是否是事件。
2. 事件身份层过弱：lightweight 只有标题；semantic 有 signature，但没有接入 console。
3. 同事件关系层缺少分级：duplicate、near_duplicate、same_event_new_info、same_topic_different_event 应分开。
4. 聚合决策缺少负特征：generic title、digest、wide time window、same source boilerplate 应强力降权。
5. 事件对象质量不足：event_type、summary、importance、confidence、evidence 目前无法承载简报。
6. 去重和聚合边界不清：URL/GUID/title-date 是 item 去重；same-event 是事件聚合；现在报告层没有解释这两者的关系。

## 深入改进方向

### Phase 1: 先修 console 接入和规则基线

- 把 `generate_information_objects()` 拆成 `classify_item_eventness -> build_event_signature -> candidate_pairs -> decide_relation -> materialize_event_cluster`。
- digest/newsletter/roundup/market wrap/tutorial/opinion 默认不建 event，进入 topic 或 review。
- item 去重补 `http/https` 可配置 canonicalization，并在 dedupe stage 展示 `seen_count` 与重复来源。
- lightweight cluster 不再用完全标题，至少使用 actor/product/action/date bucket + title token overlap。

### Phase 2: 使用 semantic 模块做候选召回

- 接入 `extract_event_signature()` 和 `assess_candidate()` 作为候选生成器。
- signature exact 作为高精度 seed；candidate medium 进入 review；candidate high 自动合并。
- 建立 alias map：OpenAI GPT-5.5/GPT 5.5/GPT-5.5、DeepSeek/深度求索、EU/European Commission 等。
- 对 generic title 和 digest title 加 hard negative 规则。

### Phase 3: 引入 LLM 或真实 API 做困难 pair 裁决

- 只对 high-uncertain/medium pair 调 LLM，输入是结构化 signature、证据、负特征，而不是全文乱扔。
- LLM 输出必须包含 relation_type、same_event、new_facts、disqualifiers、confidence。
- 低风险策略：自动合并只允许 high confidence same_event；其余进 review_queue。

### Phase 4: 事件对象和简报质量

- event_type 最小集合：release、funding、policy、partnership、earnings、security、benchmark、market、digest_non_event。
- event_summary 必须包含主体、动作、对象、时间、来源数量、增量事实。
- briefing/report 从 event cluster card 生成，而不是直接列 event title 和 opaque review id。

## 建议质量门

- same-event pair F1 >= 0.80，recall >= 0.75。
- generic/digest false positive rate <= 2%。
- eventness precision >= 0.90。
- event_type known rate >= 0.80。
- auto-merge precision >= 0.95；auto-merge recall 可以先低，召回交给 review。
