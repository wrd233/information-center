# Source Import And Export

Import is preview-first:

```bash
curl -X POST http://127.0.0.1:8787/api/sources/import/preview \
  -H 'Content-Type: application/json' \
  -d '{"format":"urls","content":"file:///feed.xml, Test Feed, Fixtures"}'
```

Commit with returned `operation_id`:

```bash
curl -X POST http://127.0.0.1:8787/api/sources/import/commit \
  -H 'Content-Type: application/json' \
  -d '{"operation_id":"op_x"}'
```

Export:

```bash
curl -X POST http://127.0.0.1:8787/api/sources/export -d '{"format":"json"}'
```
