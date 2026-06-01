# 作战台信息质量评估报告

生成时间: 2026-06-01T01:50:27.673287+00:00

## 结论

整体状态: **不通过**。本次离线评估使用合成样例，不读取真实运行数据。

核心发现:

- 处理时去重 F1: 100.0%，召回 100.0%。
- 事件聚合 F1: 42.9%，召回 27.3%。
- 自动合并 precision: 100.0%。
- medium review rate: 100.0%。
- alias hit count: 215。
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
- clusters: 4
- 多条目 cluster 比率: 25.0%
- 误合并 pair 样例: `[]`
- 漏合并 pair 样例: `[('anthropic_funding_a', 'anthropic_funding_b'), ('deepseek_cn_a', 'deepseek_cn_b'), ('deepseek_cn_a', 'guid_a'), ('deepseek_cn_b', 'guid_a'), ('openai_punctuation_variant', 'openai_variant_a'), ('openai_variant_a', 'openai_variant_b'), ('openai_variant_a', 'url_tracking_a'), ('policy_a', 'policy_b')]`

### False Negative Trace

- Pair `anthropic_funding_a` / `anthropic_funding_b`:
  - anthropic_funding_a: actor='Anthropic', product='', action='adoption_metric', signature_key=None, item_card_present=True, card_entities=[Anthropic], card_event_hint='Anthropic raises $2B at $60B valuation', clusters=[]
  - anthropic_funding_b: actor='Anthropic', product='', action='funding', signature_key=None, item_card_present=True, card_entities=[Anthropic], card_event_hint='Anthropic closes new $2 billion financing round', clusters=[]
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `deepseek_cn_a` / `deepseek_cn_b`:
  - deepseek_cn_a: actor='DeepSeek', product='', action='release', signature_key=None, item_card_present=True, card_entities=[DeepSeek, 发布, V4.1, 模型], card_event_hint='DeepSeek 发布 V4.1 模型，推理延迟下降', clusters=[]
  - deepseek_cn_b: actor='DeepSeek', product='DeepSeek V4', action='release', signature_key='deepseek|deepseekv4|release|2026-05-30', item_card_present=True, card_entities=[深度求索推出, DeepSeek, V4.1, 主打低延迟推理], card_event_hint='深度求索推出 DeepSeek V4.1，主打低延迟推理', clusters=['cluster_ee6e44e0884d81fd']
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `deepseek_cn_a` / `guid_a`:
  - deepseek_cn_a: actor='DeepSeek', product='', action='release', signature_key=None, item_card_present=True, card_entities=[DeepSeek, 发布, V4.1, 模型], card_event_hint='DeepSeek 发布 V4.1 模型，推理延迟下降', clusters=[]
  - guid_a: actor='DeepSeek', product='', action='release', signature_key=None, item_card_present=True, card_entities=[DeepSeek, V4.1, V4.1.], card_event_hint='DeepSeek releases V4.1 model', clusters=[]
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `deepseek_cn_b` / `guid_a`:
  - deepseek_cn_b: actor='DeepSeek', product='DeepSeek V4', action='release', signature_key='deepseek|deepseekv4|release|2026-05-30', item_card_present=True, card_entities=[深度求索推出, DeepSeek, V4.1, 主打低延迟推理], card_event_hint='深度求索推出 DeepSeek V4.1，主打低延迟推理', clusters=['cluster_ee6e44e0884d81fd']
  - guid_a: actor='DeepSeek', product='', action='release', signature_key=None, item_card_present=True, card_entities=[DeepSeek, V4.1, V4.1.], card_event_hint='DeepSeek releases V4.1 model', clusters=[]
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `openai_punctuation_variant` / `openai_variant_a`:
  - openai_punctuation_variant: actor='OpenAI', product='GPT-5.5', action='release', signature_key='openai|gpt55|release|2026-05-30', item_card_present=True, card_entities=[OpenAI, GPT], card_event_hint='OpenAI launches GPT 5.5 for coding agents', clusters=['cluster_1be3f3059f449572']
  - openai_variant_a: actor='OpenAI', product='GPT-5.5', action='other', signature_key=None, item_card_present=True, card_entities=[OpenAI, GPT-5.5], card_event_hint='OpenAI rolls out GPT-5.5 model aimed at coding agents', clusters=[]
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `openai_variant_a` / `openai_variant_b`:
  - openai_variant_a: actor='OpenAI', product='GPT-5.5', action='other', signature_key=None, item_card_present=True, card_entities=[OpenAI, GPT-5.5], card_event_hint='OpenAI rolls out GPT-5.5 model aimed at coding agents', clusters=[]
  - openai_variant_b: actor='OpenAI', product='GPT-5.5', action='integration', signature_key='openai|gpt55|integration|2026-05-30', item_card_present=True, card_entities=[OpenAI, GPT], card_event_hint='OpenAI GPT 5.5 model launches for software agents', clusters=['cluster_1be3f3059f449572']
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `openai_variant_a` / `url_tracking_a`:
  - openai_variant_a: actor='OpenAI', product='GPT-5.5', action='other', signature_key=None, item_card_present=True, card_entities=[OpenAI, GPT-5.5], card_event_hint='OpenAI rolls out GPT-5.5 model aimed at coding agents', clusters=[]
  - url_tracking_a: actor='OpenAI', product='GPT-5.5', action='release', signature_key='openai|gpt55|release|2026-05-30', item_card_present=True, card_entities=[OpenAI, GPT-5.5], card_event_hint='OpenAI launches GPT-5.5 for coding agents', clusters=['cluster_1be3f3059f449572']
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated
- Pair `policy_a` / `policy_b`:
  - policy_a: actor='European Commission', product='AI Act', action='technical_blog', signature_key='europeancommission|aiact|technicalblog|2026-05-30', item_card_present=True, card_entities=[Act, The], card_event_hint='EU publishes final AI Act implementation guidance', clusters=['cluster_a1a20d64e03cad90']
  - policy_b: actor='European Commission', product='AI Act', action='other', signature_key=None, item_card_present=True, card_entities=[European, Commission, Act, The], card_event_hint='European Commission issues AI Act guidance for model providers', clusters=[]
  - candidate: present=False, priority=None, lane=None, status=None
  - relation: judged_as=None, reason_code=None, decision_source=None
  - review_queue: 0 entries
  - eval_failure: no_candidate_pair_generated

### Candidate 诊断

- candidate counts by priority: `{'low': 12, 'medium': 1, 'high': 1, 'must_run': 1}`
- candidate counts by lane: `{'same_thread': 3, 'exploratory_recall': 9, 'same_event_recall': 2, 'exact_signature_alias': 1}`
- candidate counts by status: `{'rejected': 12, 'review': 1, 'auto_merge': 2}`
- disqualifier counts: `{}`
- medium review rate: 100.0%
- alias hit count: 215

### Semantic Judge Dry-Run Proposals

- dry-run proposal count: 1
- live semantic judge calls: 0
- proposal policy: review_queue_or_dry_run_report_only
- proposals: `[{'proposal_status': 'dry_run_not_called', 'task_type': 'semantic_relation_judge', 'item_pair': ['openai_variant_b', 'url_tracking_a'], 'candidate_priority': 'medium', 'lane': 'same_event_recall', 'rule_relation_type': 'uncertain', 'rule_reason_code': 'different_event', 'rule_status': 'review', 'judge_input_evidence': {'same_actor': True, 'same_product': True, 'same_action': False, 'event_signature_match': False, 'positive_features': ['shared_weighted_entities:launches, openai', 'shared_event_phrases:agent, launch', 'close_time_window', 'shared_products:gpt-5.5, gpt55', 'shared_actors:openai'], 'negative_features': ['generic_overlap:agents'], 'disqualifiers': []}, 'proposal_policy': {'proposal_only': True, 'should_auto_merge': False, 'review_queue_or_dry_run_report_only': True}}]`

### Review Apply 与 Source Scoring

- review apply sample: `{'attempted': True, 'review_id': 77, 'ok': True, 'apply_result': {'applied': True, 'action': 'event_relation_approved', 'event_id': 'event_d6770cbf532ba00c', 'cluster_id': 'cluster_1be3f3059f449572', 'item_ids': ['item_3e85a19398cb481da4e9a4af9b6c683f', 'item_d189865f22804653bf78cccd72127385']}}`
- source scoring dimension totals: `{'discovery_value': 5.0, 'fact_value': 5.0, 'incremental_value': 2.0, 'interpretation_value': 0.0, 'duplicate_noise': 3.0, 'non_event_noise': 76.0, 'review_acceptance': 2.0}`
- source scoring example profile: `{'source_id': 'techcrunch', 'discovery_value_avg': 1.0, 'fact_value_avg': 1.0, 'incremental_value_avg': 2.0, 'interpretation_value_avg': 0.0, 'duplicate_noise_rate': 1.0, 'non_event_noise_rate': 0.0, 'review_acceptance': 1.0, 'llm_yield_score': 2.667, 'priority_suggestion': 'new_source_under_evaluation'}`
- operational DeepSeek relation stats: `{'operational_relation_calls': 0, 'live_ok_calls': 0, 'failed_or_skipped_calls': 0, 'total_tokens': 0}`

### 事件提取

- events: 4
- event_type known rate: 100.0%
- summary specific rate: 100.0%
- review coverage: 2000.0%
- 非事件条目被生成候选事件比率: 0.0%
- entity recall: 97.0% (98/101)

### 简报和报告

- 每日简报质量分: 88.9%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`
- 每周简报质量分: 88.9%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`
- 运行报告质量分: 100.0%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': True, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`
- Run endpoint 报告质量分: 88.9%，检查项: `{'has_h1': True, 'has_section': True, 'has_list': True, 'has_required_terms': True, 'has_actionable_counts': True, 'has_object_context': False, 'scaffold_localized': True, 'status_labels_localized': True, 'not_too_thin': True}`

每日简报预览:

```markdown
# 每日简报 2026-06-01

## 可信事件
- OpenAI release GPT-5.5（可信事件，置信度 0.98）
- OpenAI integration major API（可信事件，置信度 0.98）
- European Commission technical blog AI Act（可信事件，置信度 0.98）
- DeepSeek release DeepSeek V4（可信事件，置信度 0.98）

## 待审核
- eventness_review item:item_057990f7399442e0a1a314e772765260
- eventness_review item:item_06e3456286c940f8bda981d92f1c9e27
- eventness_review item:item_08f1a6c1101d437ea0dd9707e4ee34a9
- eventness_review item:item_09f84f97026f41cab67cefdf7f648a60
- eventness_review item:item_0b4cc453648b460d865b42f7f8e6f66c
- eventness_review item:item_0d24b2e317e043d7bb27697fe46f7209
- eventness_review item:item_1406567ddd4f42a88af25c45366c2776
- eventness_review item:item_1477bd8d898a4bd0a60f91ce32b60915
- eventness_review item:item_193297eabb5c4b9fae70bd48237083b9
- eventness_review item:item_1a5222c5cdbd461491c95f057acc5ccc
```

运行报告预览:

```markdown
# 运行报告

生成时间: 2026-06-01T01:50:27.656888+00:00

关联对象: run run_quality_eval_8433248c19

## 可信事件
- OpenAI release GPT-5.5：release，置信度 0.98，cluster cluster_1be3f3059f449572
- OpenAI integration major API：integration，置信度 0.98，cluster cluster_9292e895fe7b3e7f
- European Commission technical blog AI Act：technical_blog，置信度 0.98，cluster cluster_a1a20d64e03cad90
- DeepSeek release DeepSeek V4：release，置信度 0.98，cluster cluster_ee6e44e0884d81fd

## 质量概览
- 可信事件数: 4
- 全部事件数: 4
- 待审核项: 80
- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。

```

Run endpoint 报告预览:

```markdown
# 运行报告 run_quality_eval_8433248c19

状态: success

新增条目: 0

信息源数量: 0

## 可信事件
- OpenAI release GPT-5.5：release，置信度 0.98
- OpenAI integration major API：integration，置信度 0.98
- European Commission technical blog AI Act：technical_blog，置信度 0.98
- DeepSeek release DeepSeek V4：release，置信度 0.98

## 质量概览
- 可信事件数: 4
- 待审核项: 80
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
    "temp_db": "/var/folders/f_/12__g2851hv407x2tv3xbx580000gn/T/content_inbox_quality_eval_k3g77pms/quality_eval.db"
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
    "clusters": 4,
    "multi_item_event_rate": 0.25,
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
    ],
    "false_negative_traces": [
      {
        "pair": [
          "anthropic_funding_a",
          "anthropic_funding_b"
        ],
        "item_ids": [
          "item_d2917045499f4badadb0de3f3cb6e016",
          "item_7f5bac74eb8a4e439feff2ae6bbd86b3"
        ],
        "items": [
          {
            "case_id": "anthropic_funding_a",
            "item_id": "item_d2917045499f4badadb0de3f3cb6e016",
            "title": "Anthropic raises $2B at $60B valuation",
            "item_card": {
              "present": true,
              "canonical_title": "Anthropic raises $2B at $60B valuation",
              "language": "en",
              "entities": [
                "Anthropic"
              ],
              "event_hint": "Anthropic raises $2B at $60B valuation",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "Anthropic",
              "product_or_model": "",
              "action": "adoption_metric",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "action",
                  "alias": "raises",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "raised",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "raised $",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "raises $",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "valuation",
                  "canonical": "funding"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          },
          {
            "case_id": "anthropic_funding_b",
            "item_id": "item_7f5bac74eb8a4e439feff2ae6bbd86b3",
            "title": "Anthropic closes new $2 billion financing round",
            "item_card": {
              "present": true,
              "canonical_title": "Anthropic closes new $2 billion financing round",
              "language": "en",
              "entities": [
                "Anthropic"
              ],
              "event_hint": "Anthropic closes new $2 billion financing round",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "Anthropic",
              "product_or_model": "",
              "action": "funding",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "action",
                  "alias": "financing",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "round",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "closes",
                  "canonical": "funding"
                },
                {
                  "type": "action",
                  "alias": "closed",
                  "canonical": "funding"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "anthropic_funding_a": [],
            "anthropic_funding_b": []
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "deepseek_cn_a",
          "deepseek_cn_b"
        ],
        "item_ids": [
          "item_7bb1820784b143a395dc34a5343b61ab",
          "item_f61c4826d216460eb425769ff2719f72"
        ],
        "items": [
          {
            "case_id": "deepseek_cn_a",
            "item_id": "item_7bb1820784b143a395dc34a5343b61ab",
            "title": "DeepSeek 发布 V4.1 模型，推理延迟下降",
            "item_card": {
              "present": true,
              "canonical_title": "DeepSeek 发布 V4.1 模型，推理延迟下降",
              "language": "zh",
              "entities": [
                "DeepSeek",
                "发布",
                "V4.1",
                "模型",
                "推理延迟下降"
              ],
              "event_hint": "DeepSeek 发布 V4.1 模型，推理延迟下降",
              "content_role": "source_material",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "DeepSeek",
              "product_or_model": "",
              "action": "release",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "Deepseek",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "action",
                  "alias": "发布",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          },
          {
            "case_id": "deepseek_cn_b",
            "item_id": "item_f61c4826d216460eb425769ff2719f72",
            "title": "深度求索推出 DeepSeek V4.1，主打低延迟推理",
            "item_card": {
              "present": true,
              "canonical_title": "深度求索推出 DeepSeek V4.1，主打低延迟推理",
              "language": "zh",
              "entities": [
                "深度求索推出",
                "DeepSeek",
                "V4.1",
                "主打低延迟推理"
              ],
              "event_hint": "深度求索推出 DeepSeek V4.1，主打低延迟推理",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "DeepSeek",
              "product_or_model": "DeepSeek V4",
              "action": "release",
              "semantic_level": "event_signature",
              "signature_key": "deepseek|deepseekv4|release|2026-05-30",
              "is_concrete": true,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "深度求索",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "actor",
                  "alias": "Deepseek",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "product",
                  "alias": "DeepSeek V4.1",
                  "canonical": "DeepSeek V4"
                },
                {
                  "type": "product",
                  "alias": "deepseek v4",
                  "canonical": "DeepSeek V4"
                },
                {
                  "type": "action",
                  "alias": "推出",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": []
            },
            "clusters": [
              "cluster_ee6e44e0884d81fd"
            ]
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "deepseek_cn_a": [],
            "deepseek_cn_b": [
              "cluster_ee6e44e0884d81fd"
            ]
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "deepseek_cn_a",
          "guid_a"
        ],
        "item_ids": [
          "item_7bb1820784b143a395dc34a5343b61ab",
          "item_1d750424bc1244deb9453f0d2725d369"
        ],
        "items": [
          {
            "case_id": "deepseek_cn_a",
            "item_id": "item_7bb1820784b143a395dc34a5343b61ab",
            "title": "DeepSeek 发布 V4.1 模型，推理延迟下降",
            "item_card": {
              "present": true,
              "canonical_title": "DeepSeek 发布 V4.1 模型，推理延迟下降",
              "language": "zh",
              "entities": [
                "DeepSeek",
                "发布",
                "V4.1",
                "模型",
                "推理延迟下降"
              ],
              "event_hint": "DeepSeek 发布 V4.1 模型，推理延迟下降",
              "content_role": "source_material",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "DeepSeek",
              "product_or_model": "",
              "action": "release",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "Deepseek",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "action",
                  "alias": "发布",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          },
          {
            "case_id": "guid_a",
            "item_id": "item_1d750424bc1244deb9453f0d2725d369",
            "title": "DeepSeek releases V4.1 model",
            "item_card": {
              "present": true,
              "canonical_title": "DeepSeek releases V4.1 model",
              "language": "en",
              "entities": [
                "DeepSeek",
                "V4.1",
                "V4.1."
              ],
              "event_hint": "DeepSeek releases V4.1 model",
              "content_role": "source_material",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "DeepSeek",
              "product_or_model": "",
              "action": "release",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "Deepseek",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "action",
                  "alias": "released",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "deepseek_cn_a": [],
            "guid_a": []
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "deepseek_cn_b",
          "guid_a"
        ],
        "item_ids": [
          "item_f61c4826d216460eb425769ff2719f72",
          "item_1d750424bc1244deb9453f0d2725d369"
        ],
        "items": [
          {
            "case_id": "deepseek_cn_b",
            "item_id": "item_f61c4826d216460eb425769ff2719f72",
            "title": "深度求索推出 DeepSeek V4.1，主打低延迟推理",
            "item_card": {
              "present": true,
              "canonical_title": "深度求索推出 DeepSeek V4.1，主打低延迟推理",
              "language": "zh",
              "entities": [
                "深度求索推出",
                "DeepSeek",
                "V4.1",
                "主打低延迟推理"
              ],
              "event_hint": "深度求索推出 DeepSeek V4.1，主打低延迟推理",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "DeepSeek",
              "product_or_model": "DeepSeek V4",
              "action": "release",
              "semantic_level": "event_signature",
              "signature_key": "deepseek|deepseekv4|release|2026-05-30",
              "is_concrete": true,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "深度求索",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "actor",
                  "alias": "Deepseek",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "product",
                  "alias": "DeepSeek V4.1",
                  "canonical": "DeepSeek V4"
                },
                {
                  "type": "product",
                  "alias": "deepseek v4",
                  "canonical": "DeepSeek V4"
                },
                {
                  "type": "action",
                  "alias": "推出",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": []
            },
            "clusters": [
              "cluster_ee6e44e0884d81fd"
            ]
          },
          {
            "case_id": "guid_a",
            "item_id": "item_1d750424bc1244deb9453f0d2725d369",
            "title": "DeepSeek releases V4.1 model",
            "item_card": {
              "present": true,
              "canonical_title": "DeepSeek releases V4.1 model",
              "language": "en",
              "entities": [
                "DeepSeek",
                "V4.1",
                "V4.1."
              ],
              "event_hint": "DeepSeek releases V4.1 model",
              "content_role": "source_material",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "DeepSeek",
              "product_or_model": "",
              "action": "release",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "Deepseek",
                  "canonical": "DeepSeek"
                },
                {
                  "type": "action",
                  "alias": "released",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "deepseek_cn_b": [
              "cluster_ee6e44e0884d81fd"
            ],
            "guid_a": []
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "openai_punctuation_variant",
          "openai_variant_a"
        ],
        "item_ids": [
          "item_d349226500574d6fb18da4ca737e5fe8",
          "item_08f1a6c1101d437ea0dd9707e4ee34a9"
        ],
        "items": [
          {
            "case_id": "openai_punctuation_variant",
            "item_id": "item_d349226500574d6fb18da4ca737e5fe8",
            "title": "OpenAI launches GPT 5.5 for coding agents",
            "item_card": {
              "present": true,
              "canonical_title": "OpenAI launches GPT 5.5 for coding agents",
              "language": "en",
              "entities": [
                "OpenAI",
                "GPT"
              ],
              "event_hint": "OpenAI launches GPT 5.5 for coding agents",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "OpenAI",
              "product_or_model": "GPT-5.5",
              "action": "release",
              "semantic_level": "event_signature",
              "signature_key": "openai|gpt55|release|2026-05-30",
              "is_concrete": true,
              "alias_hits": [
                {
                  "type": "product",
                  "alias": "GPT 5.5",
                  "canonical": "GPT-5.5"
                },
                {
                  "type": "action",
                  "alias": "launch",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": []
            },
            "clusters": [
              "cluster_1be3f3059f449572"
            ]
          },
          {
            "case_id": "openai_variant_a",
            "item_id": "item_08f1a6c1101d437ea0dd9707e4ee34a9",
            "title": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
            "item_card": {
              "present": true,
              "canonical_title": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
              "language": "en",
              "entities": [
                "OpenAI",
                "GPT-5.5"
              ],
              "event_hint": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "OpenAI",
              "product_or_model": "GPT-5.5",
              "action": "other",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "product",
                  "alias": "gpt-5.5",
                  "canonical": "GPT-5.5"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "openai_punctuation_variant": [
              "cluster_1be3f3059f449572"
            ],
            "openai_variant_a": []
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "openai_variant_a",
          "openai_variant_b"
        ],
        "item_ids": [
          "item_08f1a6c1101d437ea0dd9707e4ee34a9",
          "item_3e85a19398cb481da4e9a4af9b6c683f"
        ],
        "items": [
          {
            "case_id": "openai_variant_a",
            "item_id": "item_08f1a6c1101d437ea0dd9707e4ee34a9",
            "title": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
            "item_card": {
              "present": true,
              "canonical_title": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
              "language": "en",
              "entities": [
                "OpenAI",
                "GPT-5.5"
              ],
              "event_hint": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "OpenAI",
              "product_or_model": "GPT-5.5",
              "action": "other",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "product",
                  "alias": "gpt-5.5",
                  "canonical": "GPT-5.5"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          },
          {
            "case_id": "openai_variant_b",
            "item_id": "item_3e85a19398cb481da4e9a4af9b6c683f",
            "title": "OpenAI GPT 5.5 model launches for software agents",
            "item_card": {
              "present": true,
              "canonical_title": "OpenAI GPT 5.5 model launches for software agents",
              "language": "en",
              "entities": [
                "OpenAI",
                "GPT"
              ],
              "event_hint": "OpenAI GPT 5.5 model launches for software agents",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "OpenAI",
              "product_or_model": "GPT-5.5",
              "action": "integration",
              "semantic_level": "event_signature",
              "signature_key": "openai|gpt55|integration|2026-05-30",
              "is_concrete": true,
              "alias_hits": [
                {
                  "type": "product",
                  "alias": "GPT 5.5",
                  "canonical": "GPT-5.5"
                },
                {
                  "type": "action",
                  "alias": "launch",
                  "canonical": "release"
                },
                {
                  "type": "action",
                  "alias": "launched",
                  "canonical": "release"
                },
                {
                  "type": "action",
                  "alias": "integration",
                  "canonical": "integration"
                }
              ],
              "invalid_reasons": []
            },
            "clusters": [
              "cluster_1be3f3059f449572"
            ]
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "openai_variant_a": [],
            "openai_variant_b": [
              "cluster_1be3f3059f449572"
            ]
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "openai_variant_a",
          "url_tracking_a"
        ],
        "item_ids": [
          "item_08f1a6c1101d437ea0dd9707e4ee34a9",
          "item_d189865f22804653bf78cccd72127385"
        ],
        "items": [
          {
            "case_id": "openai_variant_a",
            "item_id": "item_08f1a6c1101d437ea0dd9707e4ee34a9",
            "title": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
            "item_card": {
              "present": true,
              "canonical_title": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
              "language": "en",
              "entities": [
                "OpenAI",
                "GPT-5.5"
              ],
              "event_hint": "OpenAI rolls out GPT-5.5 model aimed at coding agents",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "OpenAI",
              "product_or_model": "GPT-5.5",
              "action": "other",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "product",
                  "alias": "gpt-5.5",
                  "canonical": "GPT-5.5"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          },
          {
            "case_id": "url_tracking_a",
            "item_id": "item_d189865f22804653bf78cccd72127385",
            "title": "OpenAI launches GPT-5.5 for coding agents",
            "item_card": {
              "present": true,
              "canonical_title": "OpenAI launches GPT-5.5 for coding agents",
              "language": "en",
              "entities": [
                "OpenAI",
                "GPT-5.5"
              ],
              "event_hint": "OpenAI launches GPT-5.5 for coding agents",
              "content_role": "source_material",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "OpenAI",
              "product_or_model": "GPT-5.5",
              "action": "release",
              "semantic_level": "event_signature",
              "signature_key": "openai|gpt55|release|2026-05-30",
              "is_concrete": true,
              "alias_hits": [
                {
                  "type": "product",
                  "alias": "gpt-5.5",
                  "canonical": "GPT-5.5"
                },
                {
                  "type": "action",
                  "alias": "launch",
                  "canonical": "release"
                },
                {
                  "type": "action",
                  "alias": "released",
                  "canonical": "release"
                }
              ],
              "invalid_reasons": []
            },
            "clusters": [
              "cluster_1be3f3059f449572"
            ]
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "openai_variant_a": [],
            "url_tracking_a": [
              "cluster_1be3f3059f449572"
            ]
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      },
      {
        "pair": [
          "policy_a",
          "policy_b"
        ],
        "item_ids": [
          "item_c17ce686f2604583979b6b9792cd7c40",
          "item_fe81fd24edf24d9c9ce6df11df8fe5f9"
        ],
        "items": [
          {
            "case_id": "policy_a",
            "item_id": "item_c17ce686f2604583979b6b9792cd7c40",
            "title": "EU publishes final AI Act implementation guidance",
            "item_card": {
              "present": true,
              "canonical_title": "EU publishes final AI Act implementation guidance",
              "language": "en",
              "entities": [
                "Act",
                "The"
              ],
              "event_hint": "EU publishes final AI Act implementation guidance",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "European Commission",
              "product_or_model": "AI Act",
              "action": "technical_blog",
              "semantic_level": "event_signature",
              "signature_key": "europeancommission|aiact|technicalblog|2026-05-30",
              "is_concrete": true,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "EU",
                  "canonical": "European Commission"
                },
                {
                  "type": "product",
                  "alias": "AI Act implementation",
                  "canonical": "AI Act"
                },
                {
                  "type": "action",
                  "alias": "publishes",
                  "canonical": "policy"
                },
                {
                  "type": "action",
                  "alias": "published",
                  "canonical": "policy"
                },
                {
                  "type": "action",
                  "alias": "guidance",
                  "canonical": "policy"
                },
                {
                  "type": "action",
                  "alias": "act",
                  "canonical": "policy"
                }
              ],
              "invalid_reasons": []
            },
            "clusters": [
              "cluster_a1a20d64e03cad90"
            ]
          },
          {
            "case_id": "policy_b",
            "item_id": "item_fe81fd24edf24d9c9ce6df11df8fe5f9",
            "title": "European Commission issues AI Act guidance for model providers",
            "item_card": {
              "present": true,
              "canonical_title": "European Commission issues AI Act guidance for model providers",
              "language": "en",
              "entities": [
                "European",
                "Commission",
                "Act",
                "The"
              ],
              "event_hint": "European Commission issues AI Act guidance for model providers",
              "content_role": "report",
              "confidence": 0.55,
              "warnings": [
                "deterministic_minimal_card"
              ]
            },
            "signature": {
              "present": true,
              "actor": "European Commission",
              "product_or_model": "AI Act",
              "action": "other",
              "semantic_level": "thread_signature",
              "signature_key": null,
              "is_concrete": false,
              "alias_hits": [
                {
                  "type": "actor",
                  "alias": "EU",
                  "canonical": "European Commission"
                },
                {
                  "type": "actor",
                  "alias": "Europe",
                  "canonical": "European Commission"
                },
                {
                  "type": "product",
                  "alias": "AI Act guidance",
                  "canonical": "AI Act"
                },
                {
                  "type": "action",
                  "alias": "guidance",
                  "canonical": "policy"
                },
                {
                  "type": "action",
                  "alias": "act",
                  "canonical": "policy"
                }
              ],
              "invalid_reasons": [
                "semantic_level_thread_signature"
              ]
            },
            "clusters": []
          }
        ],
        "candidate": {
          "present": false
        },
        "relation": {
          "judged_as": null,
          "reason_code": null,
          "status": null,
          "decision_source": null
        },
        "review_queue": [],
        "cluster_eval": {
          "same_cluster": false,
          "cluster_ids_by_item": {
            "policy_a": [
              "cluster_a1a20d64e03cad90"
            ],
            "policy_b": []
          },
          "counted_as_failure_because": "no_candidate_pair_generated"
        }
      }
    ]
  },
  "event_extraction": {
    "events": 4,
    "event_type_known_rate": 1.0,
    "event_summary_specific_rate": 1.0,
    "review_entries": 80,
    "review_coverage": 20.0,
    "non_event_candidate_rate": 0.0,
    "entity_recall": 0.9702970297029703,
    "matched_entities": 98,
    "expected_entities": 101
  },
  "candidate_diagnostics": {
    "total_candidates": 15,
    "by_priority": {
      "low": 12,
      "medium": 1,
      "high": 1,
      "must_run": 1
    },
    "by_lane": {
      "same_thread": 3,
      "exploratory_recall": 9,
      "same_event_recall": 2,
      "exact_signature_alias": 1
    },
    "by_status": {
      "rejected": 12,
      "review": 1,
      "auto_merge": 2
    },
    "medium_review_rate": 1.0,
    "disqualifiers": {},
    "alias_hit_count": 215
  },
  "semantic_judge": {
    "dry_run_proposal_count": 1,
    "dry_run_proposals": [
      {
        "proposal_status": "dry_run_not_called",
        "task_type": "semantic_relation_judge",
        "item_pair": [
          "openai_variant_b",
          "url_tracking_a"
        ],
        "candidate_priority": "medium",
        "lane": "same_event_recall",
        "rule_relation_type": "uncertain",
        "rule_reason_code": "different_event",
        "rule_status": "review",
        "judge_input_evidence": {
          "same_actor": true,
          "same_product": true,
          "same_action": false,
          "event_signature_match": false,
          "positive_features": [
            "shared_weighted_entities:launches, openai",
            "shared_event_phrases:agent, launch",
            "close_time_window",
            "shared_products:gpt-5.5, gpt55",
            "shared_actors:openai"
          ],
          "negative_features": [
            "generic_overlap:agents"
          ],
          "disqualifiers": []
        },
        "proposal_policy": {
          "proposal_only": true,
          "should_auto_merge": false,
          "review_queue_or_dry_run_report_only": true
        }
      }
    ],
    "live_calls": 0,
    "proposal_policy": "review_queue_or_dry_run_report_only"
  },
  "review_apply": {
    "attempted": true,
    "review_id": 77,
    "ok": true,
    "apply_result": {
      "applied": true,
      "action": "event_relation_approved",
      "event_id": "event_d6770cbf532ba00c",
      "cluster_id": "cluster_1be3f3059f449572",
      "item_ids": [
        "item_3e85a19398cb481da4e9a4af9b6c683f",
        "item_d189865f22804653bf78cccd72127385"
      ]
    }
  },
  "source_scoring": {
    "recompute_ok": true,
    "profile_count": 23,
    "signal_count": 82,
    "example_profile": {
      "source_id": "techcrunch",
      "discovery_value_avg": 1.0,
      "fact_value_avg": 1.0,
      "incremental_value_avg": 2.0,
      "interpretation_value_avg": 0.0,
      "duplicate_noise_rate": 1.0,
      "non_event_noise_rate": 0.0,
      "review_acceptance": 1.0,
      "llm_yield_score": 2.667,
      "priority_suggestion": "new_source_under_evaluation"
    },
    "dimension_totals": {
      "discovery_value": 5.0,
      "fact_value": 5.0,
      "incremental_value": 2.0,
      "interpretation_value": 0.0,
      "duplicate_noise": 3.0,
      "non_event_noise": 76.0,
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
    "daily_briefing_preview": "# 每日简报 2026-06-01\n\n## 可信事件\n- OpenAI release GPT-5.5（可信事件，置信度 0.98）\n- OpenAI integration major API（可信事件，置信度 0.98）\n- European Commission technical blog AI Act（可信事件，置信度 0.98）\n- DeepSeek release DeepSeek V4（可信事件，置信度 0.98）\n\n## 待审核\n- eventness_review item:item_057990f7399442e0a1a314e772765260\n- eventness_review item:item_06e3456286c940f8bda981d92f1c9e27\n- eventness_review item:item_08f1a6c1101d437ea0dd9707e4ee34a9\n- eventness_review item:item_09f84f97026f41cab67cefdf7f648a60\n- eventness_review item:item_0b4cc453648b460d865b42f7f8e6f66c\n- eventness_review item:item_0d24b2e317e043d7bb27697fe46f7209\n- eventness_review item:item_1406567ddd4f42a88af25c45366c2776\n- eventness_review item:item_1477bd8d898a4bd0a60f91ce32b60915\n- eventness_review item:item_193297eabb5c4b9fae70bd48237083b9\n- eventness_review item:item_1a5222c5cdbd461491c95f057acc5ccc",
    "run_report_preview": "# 运行报告\n\n生成时间: 2026-06-01T01:50:27.656888+00:00\n\n关联对象: run run_quality_eval_8433248c19\n\n## 可信事件\n- OpenAI release GPT-5.5：release，置信度 0.98，cluster cluster_1be3f3059f449572\n- OpenAI integration major API：integration，置信度 0.98，cluster cluster_9292e895fe7b3e7f\n- European Commission technical blog AI Act：technical_blog，置信度 0.98，cluster cluster_a1a20d64e03cad90\n- DeepSeek release DeepSeek V4：release，置信度 0.98，cluster cluster_ee6e44e0884d81fd\n\n## 质量概览\n- 可信事件数: 4\n- 全部事件数: 4\n- 待审核项: 80\n- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。\n",
    "run_endpoint_report_preview": "# 运行报告 run_quality_eval_8433248c19\n\n状态: success\n\n新增条目: 0\n\n信息源数量: 0\n\n## 可信事件\n- OpenAI release GPT-5.5：release，置信度 0.98\n- OpenAI integration major API：integration，置信度 0.98\n- European Commission technical blog AI Act：technical_blog，置信度 0.98\n- DeepSeek release DeepSeek V4：release，置信度 0.98\n\n## 质量概览\n- 可信事件数: 4\n- 待审核项: 80\n- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。\n"
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
