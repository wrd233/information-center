#!/bin/bash
# Commands executed during live_myrss_opml_ingest test
# Date: 2026-05-16

# Step 2: OPML refresh
bash rsshub/rss_opml/export_opml.command

# Step 3: OPML -> CSV (Python inline script)
python3 -c "
import xml.etree.ElementTree as ET, csv, json, os
tree = ET.parse('rsshub/rss_opml/exports/myrss(本机用).opml')
body = tree.getroot().find('body')
feeds = []
def extract(elem, cat_path=''):
    for child in elem.findall('outline'):
        t, u = child.get('title','') or child.get('text',''), child.get('xmlUrl','')
        if u: feeds.append({'title': t, 'category_path': cat_path.strip('/'), 'xmlUrl': u})
        else: extract(child, f'{cat_path}/{t}' if cat_path else t)
extract(body)
with open('$ARTIFACT_DIR/opml_derived_sources.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['title','category_path','local_xml_url'])
    w.writeheader()
    for feed in feeds: w.writerow({'title': feed['title'], 'category_path': feed['category_path'], 'local_xml_url': feed['xmlUrl']})
"

# Step 4: Server startup (port 8788, temp DB)
cd content_inbox
CONTENT_INBOX_PORT=8788 CONTENT_INBOX_DB=content_inbox/data/live_ingest_test.sqlite3 PYTHONPATH=. nohup python3 -m app.server > "$ARTIFACT_DIR/server.log" 2>&1 &

# Step 5: Import to registry
PYTHONPATH=. python3 -m app.cli sources import-csv --api-base http://127.0.0.1:8788 --csv "$ARTIFACT_DIR/opml_derived_sources.csv" --upsert --default-status active

# Step 6: First pass (until_existing, concurrency=24)
PYTHONPATH=. python3 scripts/run_rss_sources_to_content_inbox.py --api-base http://127.0.0.1:8788 --source-mode registry --all --no-screen --concurrency 24 --timeout 60 --limit-per-source 30 --incremental-mode until_existing --probe-limit 30 --new-source-initial-limit 30

# Step 7: Second pass (fixed_limit, concurrency=32)
PYTHONPATH=. python3 scripts/run_rss_sources_to_content_inbox.py --api-base http://127.0.0.1:8788 --source-mode registry --all --no-screen --concurrency 32 --timeout 60 --limit-per-source 30 --incremental-mode fixed_limit

# Step 8: Queries
PYTHONPATH=. python3 -m app.cli sources list --api-base http://127.0.0.1:8788 --json --limit 500 > "$ARTIFACT_DIR/source_health_after_second_pass.json"
PYTHONPATH=. python3 -m app.cli runs list --api-base http://127.0.0.1:8788 --json --limit 20 > "$ARTIFACT_DIR/runs_after.json"
