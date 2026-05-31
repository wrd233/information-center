# 作战台信息质量评估报告

生成时间: 2026-05-31T17:38:35.599212+00:00

## 结论

整体状态: **不通过**。本次离线评估使用合成样例，不读取真实运行数据。

核心发现:

- 处理时去重 F1: 100.0%，召回 100.0%。
- 事件聚合 F1: 42.9%，召回 27.3%。
- 自动合并 precision: 100.0%。
- medium review rate: 100.0%。
- alias hit count: 17。
- review apply sample: ok。
- source scoring profiles/signals: 23/82。
- operational DeepSeek relation calls: 0。
- 事件类型识别率: 100.0%。
- 事件摘要具体率: 100.0%。
- 实体召回: 97.0%。
- 每日简报质量分: 88.9%。
- 运行报告质量分: 100.0%。
- Run endpoint 报告质量分: 88.9%。

## 指标标准

| 模块 | 指标 | 合格线 | 说明 |
|---|---:|---:|---|
| 处理时去重 | duplicate pair F1 | 95% | URL tracking、GUID、同源标题日期应稳定识别；scheme 差异等应按产品策略纳入。 |
| 去重阶段 | multi-item group rate | 视场景 | 阶段输出应能解释真实重复组；如果重复已在写入时折叠，阶段应明确展示 seen_count/重复来源。 |
| 事件聚合 | same-event pair F1 | 80% | 同一事件多标题应合并，泛标题/日报/同主题不同事不能误合。 |
| 事件聚合 | same-event recall | 75% | 不能只靠完全相同标题，否则跨来源新闻会大量漏合。 |
| 事件提取 | known event_type rate | 70% | 至少应区分发布、融资、政策、财报、合作、安全等。 |
| 事件提取 | specific summary rate | 80% | 摘要应描述发生了什么，而不是模板句。 |
| 事件提取 | entity recall | 70% | 核心公司、模型、政策名需要进入实体/证据。 |
| 简报 | structure+coverage score | 80% | 有标题、分区、事件/审核覆盖、数量/状态、中文一致性、足够信息密度。 |
| 报告 | structure+context score | 75% | 有对象上下文、生成时间、统计、问题/结论，而不是只给占位信息。 |

## 测试集

- 合成条目: 86
- 入库唯一条目: 82
- Gold 重复 pair: 4
- Gold 同事件 pair: 11
- Gold 非事件条目: 5

样例覆盖 URL tracking 去重、HTTP/HTTPS 规范化、GUID 去重、同源标题日期去重、跨来源同事件变体、中英文标题变体、泛标题误合并、日报/聚合内容非事件、同主题不同事件。

## 结果

### 去重

- 处理时去重 precision/recall/F1: 100.0% / 100.0% / 100.0%
- 未识别重复样例: `[]`
- 去重阶段 groups: 82
- 去重阶段多成员 groups: 0 (0.0%)

### 事件聚合

- precision/recall/F1: 100.0% / 27.3% / 42.9%
- clusters: 3
- 多条目 cluster 比率: 33.3%
- 误合并 pair 样例: `[]`
- 漏合并 pair 样例: `[('anthropic_funding_a', 'anthropic_funding_b'), ('deepseek_cn_a', 'deepseek_cn_b'), ('deepseek_cn_a', 'guid_a'), ('deepseek_cn_b', 'guid_a'), ('openai_punctuation_variant', 'openai_variant_a'), ('openai_variant_a', 'openai_variant_b'), ('openai_variant_a', 'url_tracking_a'), ('policy_a', 'policy_b')]`

### Candidate 诊断

- candidate counts by priority: `{'low': 7, 'high': 1, 'medium': 1, 'must_run': 1}`
- candidate counts by lane: `{'same_thread': 3, 'exploratory_recall': 4, 'same_event_recall': 2, 'exact_signature_alias': 1}`
- candidate counts by status: `{'review': 8, 'auto_merge': 2}`
- disqualifier counts: `{}`
- medium review rate: 100.0%
- alias hit count: 17

### Review Apply 与 Source Scoring

- review apply sample: `{'attempted': True, 'review_id': 78, 'ok': True, 'apply_result': {'applied': True, 'action': 'event_relation_approved', 'event_id': 'event_52285f514277588f', 'cluster_id': 'cluster_9292e895fe7b3e7f', 'item_ids': ['item_996ec456324e4e64ad7ad30bb594f244', 'item_a18982e2336544fd8dcb9765eebd8c1a']}}`
- source scoring dimension totals: `{'discovery_value': 4.0, 'fact_value': 4.0, 'incremental_value': 2.0, 'interpretation_value': 0.0, 'duplicate_noise': 3.0, 'non_event_noise': 77.0, 'review_acceptance': 2.0}`
- source scoring example profile: `{'source_id': 'site_a', 'discovery_value_avg': 2.0, 'fact_value_avg': 2.0, 'incremental_value_avg': 0.0, 'interpretation_value_avg': 0.0, 'duplicate_noise_rate': 0.0, 'non_event_noise_rate': 0.0, 'review_acceptance': 1.0, 'llm_yield_score': 3.0, 'priority_suggestion': 'new_source_under_evaluation'}`
- operational DeepSeek relation stats: `{'operational_relation_calls': 0, 'live_ok_calls': 0, 'failed_or_skipped_calls': 0, 'total_tokens': 0}`

### 事件提取

- events: 3
- event_type known rate: 100.0%
- summary specific rate: 100.0%
- review coverage: 2900.0%
- 非事件条目被生成候选事件比率: 0.0%
- entity recall: 97.0% (98/101)

### 简报和报告

- 每日简报质量分: 88.9%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`
- 每周简报质量分: 88.9%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`
- 运行报告质量分: 100.0%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': True, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`
- Run endpoint 报告质量分: 88.9%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`

每日简报预览:

```markdown
# 每日简报 2026-05-31

## 可信事件
- OpenAI release GPT-5.5（可信事件，置信度 0.98）
- OpenAI integration major API（可信事件，置信度 0.98）
- DeepSeek release DeepSeek V4（可信事件，置信度 0.98）

## 待审核
- eventness_review item:item_0a9dba87db3b488e8123359db5f514e6
- eventness_review item:item_0c402fb56c974d0ead662722f53f9f98
- eventness_review item:item_13fab38298994b4db3633331515d48c2
- eventness_review item:item_1c8862d2c12e489bbdb59d74f55eadc6
- eventness_review item:item_20501b28f57e4433a9d5d95255943557
- eventness_review item:item_232eac2e48214401b94da047f4edad46
- eventness_review item:item_24d2c0e194a74172987eda0633d28654
- eventness_review item:item_2b38e0b8b7a042609a7c22394e7a26d7
- eventness_review item:item_2bde36798e3848b3b2f49d333c55d688
- eventness_review item:item_2ed9d293e592462f833c5edd4cfdb133
```

运行报告预览:

```markdown
# 运行报告

生成时间: 2026-05-31T17:38:35.583600+00:00

关联对象: run run_quality_eval_e1912f6c70

## 可信事件
- OpenAI release GPT-5.5：release，置信度 0.98，cluster cluster_1be3f3059f449572
- OpenAI integration major API：integration，置信度 0.98，cluster cluster_9292e895fe7b3e7f
- DeepSeek release DeepSeek V4：release，置信度 0.98，cluster cluster_ee6e44e0884d81fd

## 质量概览
- 可信事件数: 3
- 全部事件数: 3
- 待审核项: 87
- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。

```

Run endpoint 报告预览:

```markdown
# 运行报告 run_quality_eval_e1912f6c70

状态: success

新增条目: 0

信息源数量: 0

## 可信事件
- OpenAI release GPT-5.5：release，置信度 0.98
- OpenAI integration major API：integration，置信度 0.98
- DeepSeek release DeepSeek V4：release，置信度 0.98

## 质量概览
- 可信事件数: 3
- 待审核项: 87
- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。

```

## 问题追踪

1. operational v3 已不使用规范化标题作为事件主键，但当前 rule-only 自动合并仍偏保守，跨语言、政策表述改写、融资改写等 false negative 仍多。
2. 泛标题和日报类内容已被 eventness gate 挡住；后续风险主要是 review/LLM 放宽时误把同主题不同事件升为 same-event。
3. 事件对象已具备类型、摘要和证据，但同一事件的新增事实仍主要等待 LLM/review apply 补足。
4. 去重阶段在写入后重复已折叠的情况下几乎只产生单成员 group，不能解释重复来源和 seen_count。
5. 实体抽取和 alias registry 对中文别名、政策名、产品名仍需从 false negative 样例继续扩充。
6. Run endpoint 报告仍较薄；通用 report 生成已切到可信事件输入并通过质量门。

## 建议修复顺序

1. 先把评估脚本固化为回归命令，并把上述阈值作为非阻断质量门。
2. 保持当前 high-confidence auto-merge precision，把 medium/high-uncertain 的召回增量交给 schema-bound LLM 与 review apply。
3. 继续扩充 digest/newsletter/roundup/navigation hard negatives，并监控 hard-negative LLM 调用数保持 0。
4. 从 false negative 样例补 alias/signature/action 规则，优先覆盖跨语言产品发布、政策 guidance、融资 round 改写。
5. 去重报告需要从 `seen_count`、latest_raw、item_run_links 展示重复来源，而不是期待多个同 dedupe_key item 同时存在。
6. Run endpoint 报告已切到可信事件输入；下一步补充 source scoring 明细和风险解释段落。

## 原始指标 JSON

```json
{
  "dataset": {
    "synthetic_items": 86,
    "stored_unique_items": 82,
    "gold_duplicate_pairs": 4,
    "gold_same_event_pairs": 11,
    "gold_non_event_items": 5,
    "temp_db": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_quality_eval_5v1v7gnd/quality_eval.db"
  },
  "process_dedupe": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "process_dedupe_failures": [],
  "dedupe_stage": {
    "groups": 82,
    "multi_item_groups": 0,
    "multi_item_group_rate": 0.0
  },
  "event_clustering": {
    "tp": 3,
    "fp": 0,
    "fn": 8,
    "precision": 1.0,
    "recall": 0.2727272727272727,
    "f1": 0.42857142857142855,
    "auto_merge_precision": 1.0,
    "clusters": 3,
    "multi_item_event_rate": 0.3333333333333333,
    "false_positive_pairs": [],
    "false_negative_pairs": [
      [
        "anthropic_funding_a",
        "anthropic_funding_b"
      ],
      [
        "deepseek_cn_a",
        "deepseek_cn_b"
      ],
      [
        "deepseek_cn_a",
        "guid_a"
      ],
      [
        "deepseek_cn_b",
        "guid_a"
      ],
      [
        "openai_punctuation_variant",
        "openai_variant_a"
      ],
      [
        "openai_variant_a",
        "openai_variant_b"
      ],
      [
        "openai_variant_a",
        "url_tracking_a"
      ],
      [
        "policy_a",
        "policy_b"
      ]
    ]
  },
  "event_extraction": {
    "events": 3,
    "event_type_known_rate": 1.0,
    "event_summary_specific_rate": 1.0,
    "review_entries": 87,
    "review_coverage": 29.0,
    "non_event_candidate_rate": 0.0,
    "entity_recall": 0.9702970297029703,
    "matched_entities": 98,
    "expected_entities": 101
  },
  "candidate_diagnostics": {
    "total_candidates": 10,
    "by_priority": {
      "low": 7,
      "high": 1,
      "medium": 1,
      "must_run": 1
    },
    "by_lane": {
      "same_thread": 3,
      "exploratory_recall": 4,
      "same_event_recall": 2,
      "exact_signature_alias": 1
    },
    "by_status": {
      "review": 8,
      "auto_merge": 2
    },
    "medium_review_rate": 1.0,
    "disqualifiers": {},
    "alias_hit_count": 17
  },
  "review_apply": {
    "attempted": true,
    "review_id": 78,
    "ok": true,
    "apply_result": {
      "applied": true,
      "action": "event_relation_approved",
      "event_id": "event_52285f514277588f",
      "cluster_id": "cluster_9292e895fe7b3e7f",
      "item_ids": [
        "item_996ec456324e4e64ad7ad30bb594f244",
        "item_a18982e2336544fd8dcb9765eebd8c1a"
      ]
    }
  },
  "source_scoring": {
    "recompute_ok": true,
    "profile_count": 23,
    "signal_count": 82,
    "example_profile": {
      "source_id": "site_a",
      "discovery_value_avg": 2.0,
      "fact_value_avg": 2.0,
      "incremental_value_avg": 0.0,
      "interpretation_value_avg": 0.0,
      "duplicate_noise_rate": 0.0,
      "non_event_noise_rate": 0.0,
      "review_acceptance": 1.0,
      "llm_yield_score": 3.0,
      "priority_suggestion": "new_source_under_evaluation"
    },
    "dimension_totals": {
      "discovery_value": 4.0,
      "fact_value": 4.0,
      "incremental_value": 2.0,
      "interpretation_value": 0.0,
      "duplicate_noise": 3.0,
      "non_event_noise": 77.0,
      "review_acceptance": 2.0
    }
  },
  "deepseek": {
    "operational_relation_calls": 0,
    "live_ok_calls": 0,
    "failed_or_skipped_calls": 0,
    "total_tokens": 0
  },
  "outputs": {
    "daily_briefing": {
      "score": 0.8888888888888888,
      "checks": {
        "has_h1": true,
        "has_section": true,
        "has_list": true,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": false,
        "scaffold_localized": true,
        "status_labels_localized": true,
        "not_too_thin": true
      }
    },
    "weekly_briefing": {
      "score": 0.8888888888888888,
      "checks": {
        "has_h1": true,
        "has_section": true,
        "has_list": true,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": false,
        "scaffold_localized": true,
        "status_labels_localized": true,
        "not_too_thin": true
      }
    },
    "run_report": {
      "score": 1.0,
      "checks": {
        "has_h1": true,
        "has_section": true,
        "has_list": true,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": true,
        "scaffold_localized": true,
        "status_labels_localized": true,
        "not_too_thin": true
      }
    },
    "run_endpoint_report": {
      "score": 0.8888888888888888,
      "checks": {
        "has_h1": true,
        "has_section": true,
        "has_list": true,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": false,
        "scaffold_localized": true,
        "status_labels_localized": true,
        "not_too_thin": true
      }
    },
    "daily_briefing_preview": "# 每日简报 2026-05-31\n\n## 可信事件\n- OpenAI release GPT-5.5（可信事件，置信度 0.98）\n- OpenAI integration major API（可信事件，置信度 0.98）\n- DeepSeek release DeepSeek V4（可信事件，置信度 0.98）\n\n## 待审核\n- eventness_review item:item_0a9dba87db3b488e8123359db5f514e6\n- eventness_review item:item_0c402fb56c974d0ead662722f53f9f98\n- eventness_review item:item_13fab38298994b4db3633331515d48c2\n- eventness_review item:item_1c8862d2c12e489bbdb59d74f55eadc6\n- eventness_review item:item_20501b28f57e4433a9d5d95255943557\n- eventness_review item:item_232eac2e48214401b94da047f4edad46\n- eventness_review item:item_24d2c0e194a74172987eda0633d28654\n- eventness_review item:item_2b38e0b8b7a042609a7c22394e7a26d7\n- eventness_review item:item_2bde36798e3848b3b2f49d333c55d688\n- eventness_review item:item_2ed9d293e592462f833c5edd4cfdb133",
    "run_report_preview": "# 运行报告\n\n生成时间: 2026-05-31T17:38:35.583600+00:00\n\n关联对象: run run_quality_eval_e1912f6c70\n\n## 可信事件\n- OpenAI release GPT-5.5：release，置信度 0.98，cluster cluster_1be3f3059f449572\n- OpenAI integration major API：integration，置信度 0.98，cluster cluster_9292e895fe7b3e7f\n- DeepSeek release DeepSeek V4：release，置信度 0.98，cluster cluster_ee6e44e0884d81fd\n\n## 质量概览\n- 可信事件数: 3\n- 全部事件数: 3\n- 待审核项: 87\n- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。\n",
    "run_endpoint_report_preview": "# 运行报告 run_quality_eval_e1912f6c70\n\n状态: success\n\n新增条目: 0\n\n信息源数量: 0\n\n## 可信事件\n- OpenAI release GPT-5.5：release，置信度 0.98\n- OpenAI integration major API：integration，置信度 0.98\n- DeepSeek release DeepSeek V4：release，置信度 0.98\n\n## 质量概览\n- 可信事件数: 3\n- 待审核项: 87\n- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。\n"
  },
  "threshold_results": {
    "process_dedupe_pair_f1": true,
    "event_cluster_pair_f1": false,
    "event_cluster_pair_recall": false,
    "event_type_known_rate": true,
    "event_summary_specific_rate": true,
    "entity_recall": true,
    "briefing_quality_score": true,
    "report_quality_score": true
  }
}
```
