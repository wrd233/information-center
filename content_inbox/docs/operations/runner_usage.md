# Runner Usage

`scripts/run_rss_sources_to_content_inbox.py` is a batch ingestion runner and report generator. It is not the stable Agent query CLI.

CSV mode remains the default:

```bash
PYTHONPATH=. python scripts/run_rss_sources_to_content_inbox.py \
  --source-mode csv \
  --csv ../rsshub/rss_opml/rss_sources.csv \
  --count 20 \
  --no-screen
```

Registry mode reads `active` sources from the Source API and ingests by `source_id`:

```bash
PYTHONPATH=. python scripts/run_rss_sources_to_content_inbox.py \
  --source-mode registry \
  --count 20 \
  --no-screen \
  --incremental-mode until_existing
```

Artifacts are written under the configured output directory:

- `selected_sources.csv`
- `source_results.csv`
- `failed_sources.csv`
- `report.md`
- `run_state.json`
- `metadata.json`

`run_state.json` includes `schema_version`; `metadata.json` records `source_mode` for downstream report consumers.
