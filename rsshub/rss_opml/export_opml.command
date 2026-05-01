#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

REMOTE_BASE="${RSSHUB_REMOTE_BASE:-https://macmini-rsshub.tail99ecfa.ts.net}"
REMOTE_HTTP_BASE="${RSSHUB_REMOTE_HTTP_BASE:-http://macmini-rsshub.tail99ecfa.ts.net:1200}"
LOCAL_BASE="${RSSHUB_LOCAL_BASE:-http://127.0.0.1:1200}"

python3 scripts/excel_to_opml.py rss_sources.xlsx exports/myrss.generated.opml --title "My RSS"

node - "$REMOTE_BASE" "$LOCAL_BASE" <<'NODE'
const fs = require('fs');

const [, , remoteBase, localBase] = process.argv;
const input = 'exports/myrss.generated.opml';
const output = 'exports/myrss.local.generated.opml';
const content = fs.readFileSync(input, 'utf8').replaceAll(remoteBase, localBase);

fs.writeFileSync(output, content);
NODE

node - "$REMOTE_BASE" "$REMOTE_HTTP_BASE" <<'NODE'
const fs = require('fs');

const [, , remoteBase, remoteHttpBase] = process.argv;
const input = 'exports/myrss.generated.opml';
const output = 'exports/myrss.remote-http.generated.opml';
const content = fs.readFileSync(input, 'utf8').replaceAll(remoteBase, remoteHttpBase);

fs.writeFileSync(output, content);
NODE

echo "Done: exports/myrss.generated.opml"
echo "Done: exports/myrss.local.generated.opml"
echo "Done: exports/myrss.remote-http.generated.opml"
