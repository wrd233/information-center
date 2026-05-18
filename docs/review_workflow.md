# Review Workflow

The review queue stores review type, target type/id, suggestion JSON, reason, status, reviewer, note, and timestamps.

Resolve:

```bash
curl -X POST http://127.0.0.1:8787/api/review-queue/1/resolve \
  -H 'Content-Type: application/json' \
  -d '{"status":"resolved","note":"accepted"}'
```
