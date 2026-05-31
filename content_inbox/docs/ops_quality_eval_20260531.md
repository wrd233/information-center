# 作战台信息质量评估报告

生成时间: 2026-05-31T12:17:27.792010+00:00

## 结论

整体状态: **不通过**。本次离线评估使用合成样例，不读取真实运行数据。

核心发现:

- 处理时去重 F1: 85.7%，召回 75.0%。
- 事件聚合 F1: 21.1%，召回 16.7%。
- 事件类型识别率: 0.0%。
- 事件摘要具体率: 0.0%。
- 实体召回: 97.1%。
- 每日简报质量分: 77.8%。
- 运行报告质量分: 66.7%。
- Run endpoint 报告质量分: 55.6%。

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
- 入库唯一条目: 83
- Gold 重复 pair: 4
- Gold 同事件 pair: 12
- Gold 非事件条目: 5

样例覆盖 URL tracking 去重、HTTP/HTTPS 规范化、GUID 去重、同源标题日期去重、跨来源同事件变体、中英文标题变体、泛标题误合并、日报/聚合内容非事件、同主题不同事件。

## 结果

### 去重

- 处理时去重 precision/recall/F1: 100.0% / 75.0% / 85.7%
- 未识别重复样例: `['http_https_b']`
- 去重阶段 groups: 83
- 去重阶段多成员 groups: 0 (0.0%)

### 事件聚合

- precision/recall/F1: 28.6% / 16.7% / 21.1%
- clusters: 77
- 多条目 cluster 比率: 6.5%
- 误合并 pair 样例: `[('daily_digest_a', 'daily_digest_b'), ('daily_digest_a', 'daily_digest_c'), ('daily_digest_b', 'daily_digest_c'), ('generic_title_a', 'generic_title_b'), ('market_wrap_a', 'market_wrap_b')]`
- 漏合并 pair 样例: `[('anthropic_funding_a', 'anthropic_funding_b'), ('deepseek_cn_a', 'deepseek_cn_b'), ('deepseek_cn_a', 'guid_a'), ('deepseek_cn_b', 'guid_a'), ('openai_punctuation_variant', 'openai_variant_a'), ('openai_punctuation_variant', 'openai_variant_b'), ('openai_variant_a', 'openai_variant_b'), ('openai_variant_a', 'url_tracking_a'), ('openai_variant_b', 'url_tracking_a'), ('policy_a', 'policy_b')]`

### 事件提取

- events: 77
- event_type known rate: 0.0%
- summary specific rate: 0.0%
- review coverage: 100.0%
- 非事件条目被生成候选事件比率: 100.0%
- entity recall: 97.1% (100/103)

### 简报和报告

- 每日简报质量分: 77.8%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': False, 'not_too_thin': True}`
- 每周简报质量分: 77.8%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': False, 'not_too_thin': True}`
- 运行报告质量分: 66.7%，检查项: `{'has_h1': True, 'has_section': False, 'has_list': False, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': True, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': False}`
- Run endpoint 报告质量分: 55.6%，检查项: `{'has_h1': True, 'has_section': False, 'has_list': False, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': False}`

每日简报预览:

```markdown
# 每日简报 2026-05-31

## 事件
- Microsoft market update 29（needs_review）
- Google security update 21（needs_review）
- Nvidia product update 44（needs_review）
- Nvidia product update 14（needs_review）
- Microsoft market update 41（needs_review）
- Market wrap: AI stocks rally（needs_review）
- Meta benchmark update 28（needs_review）
- Google security update 15（needs_review）
- NVIDIA unveils Rubin Ultra platform（needs_review）
- OpenAI signs new cloud capacity deal with Oracle（needs_review）

## 待审核
- event_candidate event:event_817118d142798288
- event_candidate event:event_d617b90e2368bd13
- event_candidate event:event_4ecf2d1949d60d71
- event_candidate event:event_f1d807601c6a0dc8
- event_candidate event:event_05843d2e02561006
- event_candidate event:event_07f34c672e41ce2f
- event_candidate event:event_7042ba7643234370
- event_candidate event:event_720dc0137165170b
- event_candidate event:event_50893e88ed0c9583
- event_candidate event:event_8d68318ea34376cf
```

运行报告预览:

```markdown
# 运行报告

生成时间: 2026-05-31T12:17:27.785354+00:00

关联对象: run run_quality_eval_6354108178

```

Run endpoint 报告预览:

```markdown
# 运行报告 run_quality_eval_6354108178

状态: success

新增条目: 0

信息源数量: 0

```

## 问题追踪

1. 当前事件聚合以规范化标题完全一致为核心，导致跨媒体改写标题的同一事件大量漏合。
2. 泛标题和日报标题会被完全标题规则误合并，且非事件内容也会生成候选事件。
3. 事件对象字段偏占位：`event_type=unknown`、摘要为模板句，无法支撑高质量简报。
4. 去重阶段在写入后重复已折叠的情况下几乎只产生单成员 group，不能解释重复来源和 seen_count。
5. 实体抽取偏英文大写 token，对中文别名、政策名、产品名覆盖不足。
6. 报告生成仍是占位实现，缺少来源、阶段、错误、事件、审核、质量风险等关键内容。

## 建议修复顺序

1. 先把评估脚本固化为回归命令，并把上述阈值作为非阻断质量门。
2. 事件聚合从完全标题改为 title token/entity/signature 多特征：实体重叠、动作词、时间窗、source diversity、digest/generic-title 降权。
3. 非事件过滤：digest/newsletter/roundup/navigation 类条目默认不生成 event，只进入 item 或 topic。
4. 事件摘要和类型用规则版 schema 起步：融资、发布、政策、合作、财报、安全、市场；摘要至少包含主体、动作、对象。
5. 去重报告需要从 `seen_count`、latest_raw、item_run_links 展示重复来源，而不是期待多个同 dedupe_key item 同时存在。
6. 简报/报告生成改为基于事件状态、重要性、证据、待审核项和来源健康度的结构化模板。

## 原始指标 JSON

```json
{
  "dataset": {
    "synthetic_items": 86,
    "stored_unique_items": 83,
    "gold_duplicate_pairs": 4,
    "gold_same_event_pairs": 12,
    "gold_non_event_items": 5,
    "temp_db": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_quality_eval_dtbk1u8m/quality_eval.db"
  },
  "process_dedupe": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "process_dedupe_failures": [
    "http_https_b"
  ],
  "dedupe_stage": {
    "groups": 83,
    "multi_item_groups": 0,
    "multi_item_group_rate": 0.0
  },
  "event_clustering": {
    "tp": 2,
    "fp": 5,
    "fn": 10,
    "precision": 0.2857142857142857,
    "recall": 0.16666666666666666,
    "f1": 0.2105263157894737,
    "clusters": 77,
    "multi_item_event_rate": 0.06493506493506493,
    "false_positive_pairs": [
      [
        "daily_digest_a",
        "daily_digest_b"
      ],
      [
        "daily_digest_a",
        "daily_digest_c"
      ],
      [
        "daily_digest_b",
        "daily_digest_c"
      ],
      [
        "generic_title_a",
        "generic_title_b"
      ],
      [
        "market_wrap_a",
        "market_wrap_b"
      ]
    ],
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
        "openai_punctuation_variant",
        "openai_variant_b"
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
        "openai_variant_b",
        "url_tracking_a"
      ],
      [
        "policy_a",
        "policy_b"
      ]
    ]
  },
  "event_extraction": {
    "events": 77,
    "event_type_known_rate": 0.0,
    "event_summary_specific_rate": 0.0,
    "review_entries": 77,
    "review_coverage": 1.0,
    "non_event_candidate_rate": 1.0,
    "entity_recall": 0.970873786407767,
    "matched_entities": 100,
    "expected_entities": 103
  },
  "outputs": {
    "daily_briefing": {
      "score": 0.7777777777777778,
      "checks": {
        "has_h1": true,
        "has_section": true,
        "has_list": true,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": false,
        "scaffold_localized": true,
        "status_labels_localized": false,
        "not_too_thin": true
      }
    },
    "weekly_briefing": {
      "score": 0.7777777777777778,
      "checks": {
        "has_h1": true,
        "has_section": true,
        "has_list": true,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": false,
        "scaffold_localized": true,
        "status_labels_localized": false,
        "not_too_thin": true
      }
    },
    "run_report": {
      "score": 0.6666666666666666,
      "checks": {
        "has_h1": true,
        "has_section": false,
        "has_list": false,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": true,
        "scaffold_localized": true,
        "status_labels_localized": true,
        "not_too_thin": false
      }
    },
    "run_endpoint_report": {
      "score": 0.5555555555555556,
      "checks": {
        "has_h1": true,
        "has_section": false,
        "has_list": false,
        "has_required_terms": true,
        "has_actionable_counts": true,
        "has_object_context": false,
        "scaffold_localized": true,
        "status_labels_localized": true,
        "not_too_thin": false
      }
    },
    "daily_briefing_preview": "# 每日简报 2026-05-31\n\n## 事件\n- Microsoft market update 29（needs_review）\n- Google security update 21（needs_review）\n- Nvidia product update 44（needs_review）\n- Nvidia product update 14（needs_review）\n- Microsoft market update 41（needs_review）\n- Market wrap: AI stocks rally（needs_review）\n- Meta benchmark update 28（needs_review）\n- Google security update 15（needs_review）\n- NVIDIA unveils Rubin Ultra platform（needs_review）\n- OpenAI signs new cloud capacity deal with Oracle（needs_review）\n\n## 待审核\n- event_candidate event:event_817118d142798288\n- event_candidate event:event_d617b90e2368bd13\n- event_candidate event:event_4ecf2d1949d60d71\n- event_candidate event:event_f1d807601c6a0dc8\n- event_candidate event:event_05843d2e02561006\n- event_candidate event:event_07f34c672e41ce2f\n- event_candidate event:event_7042ba7643234370\n- event_candidate event:event_720dc0137165170b\n- event_candidate event:event_50893e88ed0c9583\n- event_candidate event:event_8d68318ea34376cf",
    "run_report_preview": "# 运行报告\n\n生成时间: 2026-05-31T12:17:27.785354+00:00\n\n关联对象: run run_quality_eval_6354108178\n",
    "run_endpoint_report_preview": "# 运行报告 run_quality_eval_6354108178\n\n状态: success\n\n新增条目: 0\n\n信息源数量: 0\n"
  },
  "threshold_results": {
    "process_dedupe_pair_f1": false,
    "event_cluster_pair_f1": false,
    "event_cluster_pair_recall": false,
    "event_type_known_rate": false,
    "event_summary_specific_rate": false,
    "entity_recall": true,
    "briefing_quality_score": false,
    "report_quality_score": false
  }
}
```
