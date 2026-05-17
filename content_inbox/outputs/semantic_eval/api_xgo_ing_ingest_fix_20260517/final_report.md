# api.xgo.ing Source Scope Fix — Final Report

**Date:** 2026-05-17
**Run by:** Claude Code in plan mode

## 1. Executive Summary

Successfully registered 151 `api.xgo.ing*` RSS sources in `rss_sources`, backfilled source linkage on 728 existing `inbox_items`, and fixed the `evaluate --source-url-prefix` query to resolve through `rss_sources`. The `--source-url-prefix api.xgo.ing` flag now correctly finds 146 sources and samples items from them.

## 2. DB Path and Backup

| Item | Value |
|------|-------|
| Real DB path | `content_inbox/data/content_inbox.sqlite3` |
| Backup path | `content_inbox/data/backups/content_inbox.sqlite3.before_api_xgo_fix_20260517_004523.sqlite3` |

## 3. Root Cause Analysis

**Three independent problems combined to cause 0 hits:**

1. **`rss_sources` table was empty (0 rows).** All 501 sources only existed in `rsshub/rss_opml/rss_sources.csv`. The `rss_sources` registry table was never populated — batch runs used the `POST /api/rss/analyze` endpoint which bypasses the registry.

2. **`inbox_items.source_id` and `inbox_items.feed_url` were 100% NULL (2497/2497 items).** These columns were added via schema migration (`ensure_column`) after historical items were ingested. No backfill had been run.

3. **`source_scope_where()` only searched `inbox_items` directly with LIKE patterns.** It never joined `rss_sources` to resolve source scope. With `source_id=NULL` and `feed_url=NULL`, matching on any field was impossible even though 728 items from api.xgo.ing sources existed in the DB.

## 4. Before Fix — Probe Summary

```
rss_sources:            0 total, 0 matched
inbox_items:            2497 total, 0 with 'xgo' or 'api.xgo.ing' in any field
source_id NULL:         2497 (100%)
feed_url NULL:          2497 (100%)
api.xgo.ing items:      728 (hidden — source_name matched but no indexable field contained 'xgo')
```

## 5. Fix Actions

| Action | Result |
|--------|--------|
| Import 151 api.xgo.ing sources from CSV → `rss_sources` | 151 imported, 0 conflicts |
| Backfill `source_id` and `feed_url` on 728 `inbox_items` | 728 updated (source_id + feed_url set) |
| Fix `source_scope_where()` to resolve through `rss_sources` | Now joins `rss_sources` by `feed_url` prefix, then uses `source_id IN (...)` for item lookup |
| Add `probe-source-scope` CLI command | Diagnostic report with 4-case classification |
| Add `fix-source-linkage` CLI command | Dry-run safe, backup-before-write |
| Add `ingest-source-scope` CLI command | Lists/ingests sources matching URL prefix |

## 6. After Fix — Probe Summary

```
rss_sources:            151 total, 151 matched (api.xgo.ing)
inbox_items:            2497 total, 728 with source_id and feed_url from api.xgo.ing
Sources with items:     146 (of 151)
Sources with 0 items:   5 (HTML entity encoding in CSV names)
source_id NULL:         1769 (non-api.xgo.ing items)
feed_url NULL:          1769 (non-api.xgo.ing items)
Latest item:            2026-05-05
```

## 7. Evaluate Verification

```bash
PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --source-url-prefix api.xgo.ing \
  --sample-mode source_scope_full \
  --max-items 20 --max-calls 0 --dry-run
```

**Result:** `items_sampled=20`, `source_scope.matched_source_count=146`

The source scope report now shows **146 matched sources** with proper `feed_url` values (no NULLs for api.xgo.ing sources).

## 8. Zero-Item Sources (5)

| source_id | source_name | Issue |
|-----------|-------------|-------|
| `socialmedia-barsee-128054-heybarsee` | Barsee &#128054;(@heyBarsee) | HTML entity in CSV name |
| `socialmedia-kevin-weil-127482-127480-kevinweil` | Kevin Weil &#127482;&#127480;(@kevinweil) | HTML entity in CSV name |
| `socialmedia-llamaindex-129433-llama-index` | LlamaIndex &#129433;(@llama_index) | HTML entity in CSV name |
| `socialmedia-marc-andreessen-127482-127480-pmarca` | Marc Andreessen &#127482;&#127480;(@pmarca) | HTML entity in CSV name |
| `socialmedia-clem-129303-clementdelangue` | clem &#129303;(@ClementDelangue) | HTML entity in CSV name |

These 5 sources have HTML entities in their CSV names that don't match the Unicode in `inbox_items.source_name`. Items may exist under different source_names. Run `POST /api/rss/sources/{id}/ingest` for each to fetch new items.

## 9. Tests

```bash
cd content_inbox
PYTHONPATH=. pytest -q
# 219 passed, 11 skipped in 4.07s
```

Existing tests pass. No regression in `test_evaluate_source_scope_filter_and_report_sections`.

## 10. Files Changed

| File | Change |
|------|--------|
| `app/semantic/probe.py` | **NEW** — probe, fix, ingest, backup functions |
| `app/semantic/evaluate.py` | Add `_resolve_source_url_prefix()`, modify `source_scope_where()` to accept `conn` and resolve through `rss_sources`, update call sites |
| `app/semantic/cli.py` | Add `probe-source-scope`, `fix-source-linkage`, `ingest-source-scope` subcommands + human-readable probe report |
| `content_inbox/data/backups/` | Backup created before writes |
| `content_inbox/data/content_inbox.sqlite3` | 151 sources imported, 728 items backfilled |
| `outputs/semantic_eval/` | Probe and evaluate reports |
| Console UI | **NOT MODIFIED** |

## 11. Remaining Risks

1. **1769 non-api.xgo.ing items** still have NULL `source_id`/`feed_url`. The `fix-source-linkage` command can repair these if all sources are registered first.
2. **5 zero-item sources** have encoding issues in CSV names. May need manual name normalization or re-ingestion.
3. **Latest item date is 2026-05-05** (12 days ago). Some sources may have fresher content. Run `ingest-source-scope api.xgo.ing --apply` to fetch new items through the registry.
4. **Backfill was run directly via Python, not via the `fix-source-linkage` CLI.** The CLI's idempotent update logic is verified via dry-run. Future backfills should use the CLI.

## 12. Recommended Next Commands

```bash
# 1. Ingest fresh items for api.xgo.ing sources (requires running service)
PYTHONPATH=. python3 -m content_inbox.semantic ingest-source-scope api.xgo.ing --apply

# 2. Run semantic evaluation with LLM (dry-run, no real DB writes)
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. python3 -m content_inbox.semantic evaluate \
  --source-url-prefix api.xgo.ing \
  --sample-mode source_scope_full \
  --max-items 50 --max-calls 100 --batch-size 5 --concurrency 2 \
  --live --dry-run \
  --output-dir outputs/semantic_eval/api_xgo_semantic_smoke
```
