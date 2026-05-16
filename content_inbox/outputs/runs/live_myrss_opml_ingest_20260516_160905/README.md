# Live RSS Full Ingestion & Dedupe Test Artifacts

- **Test date:** 2026-05-16
- **OPML source:** rsshub/rss_opml/exports/myrss(本机用).opml
- **Server:** Local Python on port 8788
- **Database:** content_inbox/data/live_ingest_test.sqlite3

## Files

| File | Description |
|---|---|
| `final_report.md` | Complete test report |
| `commands.sh` | All commands executed |
| `opml_sync.log` | OPML refresh output |
| `opml_summary.json` | OPML metadata (501 feeds, categories, sample) |
| `opml_derived_sources.csv` | Temp CSV generated from OPML |
| `source_registry_after_import.json` | Registry state after import |
| `source_health_after_second_pass.json` | Source health after both passes |
| `runner_first_pass.stdout.log` | First pass full output |
| `runner_first_pass_report.md` | First pass generated report |
| `runner_first_pass_failed_sources.csv` | First pass failure details |
| `runner_first_pass_source_results.csv` | First pass per-source results |
| `runner_first_pass_metadata.json` | First pass metadata |
| `runner_second_pass.stdout.log` | Second pass full output |
| `runner_second_pass_report.md` | Second pass generated report |
| `runner_second_pass_failed_sources.csv` | Second pass failure details |
| `runner_second_pass_metadata.json` | Second pass metadata |
| `runs_after.json` | Run history after both passes |
| `dedupe_summary.json` | SQLite dedupe statistics |
| `server.log` | Server output |

## Key Results

- 501 OPML feeds → 501 registry sources → 500 attempted
- First pass: 11,173 new, 0 dup, 46 failed (9.2%)
- Second pass: 519 new, 11,075 dup (95.5% dedupe rate), 32 failed (6.4%)
- Dedupe v2: 11,082 items correctly seen twice
- No code files modified
