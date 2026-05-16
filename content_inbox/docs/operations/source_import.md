# Source Import

CSV import converts source lists into the `rss_sources` registry.

Dry run:

```bash
PYTHONPATH=. python -m app.cli sources import-csv \
  --csv ../rsshub/rss_opml/rss_sources.csv \
  --dry-run \
  --json
```

Apply:

```bash
PYTHONPATH=. python -m app.cli sources import-csv \
  --csv ../rsshub/rss_opml/rss_sources.csv \
  --upsert \
  --source-id-column source_id \
  --json
```

Supported column aliases include `title`, `name`, `source_name`, `源名称`, `category`, `category_path`, `source_category`, `分类`, `feed_url`, `rss_url`, `url`, `local_xml_url`, and `xml_url`.

Backfill existing inbox rows:

```bash
PYTHONPATH=. python -m app.cli sources backfill-items --dry-run --json
PYTHONPATH=. python -m app.cli sources backfill-items --apply --json
```

Backfill matches by feed URL first, then by unique `source_name + source_category`. Ambiguous and unmatched rows are not written.
