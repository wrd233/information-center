# Operational v3 Real-Use Closeout Progress

Generated at: 2026-06-01

## Verdict

**PARTIAL_READY**

The synthetic/golden operational quality gate is passing and the main event aggregation recall gap has been closed on the benchmark. A bounded real-data dry-run smoke also produced materialized multi-item event clusters plus briefing/report samples from the real inbox copied into a temporary evaluation DB. The remaining blocker for READY is live DeepSeek validation and a scoped real-write rehearsal; neither was performed in this environment.

## 本轮改动总览

- Repaired deterministic event signature extraction for phrasing that previously blocked candidate generation.
- Normalized release/funding/policy variants that appeared in the FN trace:
  - "rolls out / rolled out" -> `release`
  - DeepSeek `V4.1` -> canonical `DeepSeek V4`
  - Anthropic funding/financing/valuation wording -> canonical funding-round product
  - AI Act guidance/published/issued wording -> `policy`
- Preserved review-safe LLM behavior from the existing semantic judge path: LLM proposals remain review/dry-run only, with no new large-scale auto-merge authority.
- Added a read-only real-use smoke utility that copies real inbox rows into a temporary DB, runs operational v3 dedupe/event materialization, and emits briefing/report/audit evidence.
- Fixed cluster provenance so the representative item remains `source_material` instead of being overwritten as `same_event_repeat`.
- Fixed a SQLite schema-initialization race where concurrent startup could fail on duplicate `ALTER TABLE ... ADD COLUMN`.
- Refreshed the operational quality report and real/synthetic report previews.

## 修改文件列表

- `content_inbox/app/semantic/signatures.py`
- `content_inbox/app/semantic/operational_pipeline.py`
- `content_inbox/app/storage.py`
- `content_inbox/scripts/evaluate_ops_quality.py`
- `content_inbox/scripts/real_use_smoke.py`
- `content_inbox/tests/test_semantic_signature_fixtures.py`
- `content_inbox/tests/test_semantic_phase1.py`
- `content_inbox/docs/ops_quality_eval_20260531.md`
- `content_inbox/docs/real_use_smoke_operational_v3_20260601/real_use_smoke_report.md`
- `content_inbox/docs/real_use_smoke_operational_v3_20260601/real_use_smoke_summary.json`
- `content_inbox/docs/real_smoke_operational_v3_20260601/semantic_quality_report.md`
- `content_inbox/docs/real_smoke_operational_v3_20260601/semantic_quality_summary.json`
- `content_inbox/docs/operational_v3_real_use_closeout_20260601.md`

## 使用了哪些真实数据

Two validation scopes were used:

- Synthetic/golden operational fixture from `scripts/evaluate_ops_quality.py`.
- Real inbox read-only sample from `content_inbox/data/content_inbox.sqlite3`: 40 items, `sample_mode=event_hotspots`, across the real DB scope of 3278 inbox items and 469 sources. The sample was copied into a temporary SQLite evaluation DB before any pipeline writes.

## 是否修改/清空/重建了数据

No real DB writes, clearing, or rebuilds were performed. The real source DB was read for a bounded smoke sample only. All semantic pipeline writes happened in temporary evaluation DBs:

- `/var/folders/.../content_inbox_semantic_eval_*.sqlite3`
- `/var/folders/.../content_inbox_real_use_smoke_*.sqlite3`

## 备份位置

None needed for this pass because no real runtime database was modified. The real-use smoke was dry-run/temp-copy only.

## DeepSeek live API 使用情况

No live DeepSeek request was made.

Controlled command:

```bash
cd content_inbox && PYTHONPATH=. python3 -m app.semantic.cli live-smoke all --limit 3 --max-calls 5
```

Result: skipped safely with `CONTENT_INBOX_LLM_ENABLE_LIVE is not 1`.

## LLM 调用量与失败量

- Quality eval operational relation calls: `0`
- Live smoke calls: `0`
- Live smoke failures: `0`
- Live smoke skipped: `1`, because live mode was disabled
- Real-use smoke LLM calls: `0`

## 去重指标变化

Current quality eval:

- process dedupe precision/recall/F1: `100.0% / 100.0% / 100.0%`
- Gold duplicate pairs: `4`
- Missed duplicate examples: `[]`

## 事件聚合指标变化

Baseline immediately before this pass, from the refreshed report diff:

- event cluster precision/recall/F1: `100.0% / 27.3% / 42.9%`
- FN examples included Anthropic funding, DeepSeek V4.1, OpenAI GPT-5.5 rollout variants, and AI Act guidance.

Current quality eval:

- event cluster precision/recall/F1: `100.0% / 100.0% / 100.0%`
- clusters: `5`
- multi-item cluster rate: `80.0%`
- false positive examples: `[]`
- false negative examples: `[]`

## 报告生成样例路径

- `content_inbox/docs/ops_quality_eval_20260531.md`
- `content_inbox/docs/real_use_smoke_operational_v3_20260601/real_use_smoke_report.md`
- `content_inbox/docs/real_smoke_operational_v3_20260601/semantic_quality_report.md`

The synthetic and real-use smoke report previews both show briefing/report output consuming materialized event clusters rather than raw item lists. The run report states: `输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。`

Real-use smoke result:

- sampled real items: `40`
- generated clusters: `7`
- multi-item clusters: `2`
- ready events: `7`
- pending reviews: `40`
- sample multi-item clusters: OpenAI/Codex browser integration (`3` items), Anthropic Claude event (`2` items)

## Golden set / fixture 改进

- Added focused signature fixture coverage for the recall-repair phrases that previously caused no-candidate or split-cluster failures:
  - OpenAI GPT-5.5 rollout wording
  - DeepSeek V4.1 Chinese release wording
  - Anthropic $2B funding wording
  - European Commission AI Act guidance wording

## FN/FP trace 主要发现

Before the signature repair, the FN trace showed the dominant failure was upstream of relation judgment:

- Several same-event pairs had no candidate because one side did not produce a concrete comparable event signature.
- Funding wording was misclassified as adoption/valuation without a stable event product.
- Policy guidance wording split into `technical_blog`/`other` instead of a shared policy event action.
- DeepSeek V4.1 variants canonicalized inconsistently.

After the repair:

- FN list: `[]`
- FP list: `[]`

Real smoke does not have gold labels, so it emits qualitative trace instead of measured FN/FP:

- candidate pairs: `45`
- candidate statuses: `{'rejected': 36, 'review': 5, 'auto_merge': 4}`
- cluster item relations after provenance fix: `{'same_event_repeat': 3, 'source_material': 7}`
- main remaining real-data issue: many social/thread posts are correctly pushed to eventness review, but this keeps pending review volume high without live LLM/card enrichment.

## 测试命令与结果

```bash
cd content_inbox && PYTHONPATH=. pytest -q tests/test_semantic_signature_fixtures.py tests/test_semantic_phase1.py -q
```

Result: passed, with the existing semantic phase skip preserved.

```bash
cd content_inbox && PYTHONPATH=. pytest -q
```

Result: `293 passed, 11 skipped in 7.49s`.

```bash
cd content_inbox && PYTHONPATH=. python3 scripts/evaluate_ops_quality.py
```

Result: all threshold results passed.

```bash
cd content_inbox && PYTHONPATH=. python3 -m app.semantic.cli evaluate --dry-run --limit 40 --max-calls 0 --max-candidates 5 --batch-size 5 --sample-mode event_hotspots --output docs/real_smoke_operational_v3_20260601 --phase-label operational_v3_real_smoke
```

Result: succeeded; 40 real items copied to temp DB; no source DB writes; semantic evaluator verdict remained `NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE` because live/card fallback rate, Chinese event detection, and scoped write rehearsal gates were not satisfied.

```bash
cd content_inbox && PYTHONPATH=. python3 scripts/real_use_smoke.py --limit 40 --sample-mode event_hotspots --output docs/real_use_smoke_operational_v3_20260601
```

Result: succeeded; 40 real items sampled; 7 clusters, 2 multi-item clusters, 7 ready events, 40 pending reviews; generated real-use briefing/report preview from temp DB.

```bash
cd content_inbox && PYTHONPATH=. python3 -m app.semantic.cli live-smoke all --limit 3 --max-calls 5
```

Result: skipped safely because live mode is disabled.

## 当前是否达到“去重、聚合、报告生成可用”

**Partially.**

- 去重: ready on the current operational benchmark.
- 事件聚合: ready on the current operational benchmark, with recall/F1 now above target while precision remains `100.0%`.
- 报告生成: benchmark gates pass, and real-use smoke produced briefing/report samples from materialized temp-DB event clusters. Real write/live validation is still pending.

## 剩余风险

- No live DeepSeek validation was performed because live mode is disabled.
- Real smoke shows social/thread-heavy samples still create high review volume and depend on live/card enrichment for better readiness.
- Funding-round canonicalization is intentionally conservative by actor/date/amount; same-company same-day funding edge cases may still need LLM review.
- The LLM relation judge currently contributes proposals/review evidence, not automatic merges.

## 下一轮建议

1. Enable a tiny DeepSeek live smoke with `CONTENT_INBOX_LLM_ENABLE_LIVE=1`, `--max-calls 5`, and temporary DB only.
2. Run one scoped real-write rehearsal only after creating an explicit backup and using the existing `--confirm-scoped-semantic-write api.xgo.ing` guard.
3. Add FP-heavy real examples for same company/product but different actions on the same day.
4. Promote the real-use smoke clusters/review samples into a small stable fixture so messy social/thread behavior stays covered.
