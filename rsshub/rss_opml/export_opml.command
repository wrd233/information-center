#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

REMOTE_BASE="${RSSHUB_REMOTE_BASE:-https://macmini-rsshub.tail99ecfa.ts.net}"
REMOTE_HTTP_BASE="${RSSHUB_REMOTE_HTTP_BASE:-http://macmini-rsshub.tail99ecfa.ts.net:1200}"
LOCAL_BASE="${RSSHUB_LOCAL_BASE:-http://127.0.0.1:1200}"

REMOTE_OPML="exports/myrss(远程用).opml"
LOCAL_OPML="exports/myrss(本机用).opml"
REMOTE_HTTP_OPML="exports/myrss(远程备用-HTTP).opml"

python3 scripts/excel_to_opml.py rss_sources.csv "$REMOTE_OPML" --title "My RSS"
python3 scripts/excel_to_opml.py rss_sources.csv "$LOCAL_OPML" --title "My RSS" --xml-url-column local_xml_url

node - "$REMOTE_OPML" "$REMOTE_HTTP_OPML" "$REMOTE_BASE" "$REMOTE_HTTP_BASE" <<'NODE'
const fs = require('fs');

const [, , input, output, remoteBase, remoteHttpBase] = process.argv;
const content = fs.readFileSync(input, 'utf8').replaceAll(remoteBase, remoteHttpBase);

fs.writeFileSync(output, content);
NODE

rm -f \
  exports/myrss.generated.opml \
  exports/myrss.local.generated.opml \
  exports/myrss.remote-http.generated.opml

echo "Done: $REMOTE_OPML"
echo "Done: $LOCAL_OPML"
echo "Done: $REMOTE_HTTP_OPML"
