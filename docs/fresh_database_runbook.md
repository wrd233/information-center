# Fresh Database Runbook

Default backend DB:

```bash
CONTENT_INBOX_DB_PATH=content_inbox/data/environments/fresh_default/content_inbox.db
```

Create a timestamped fresh DB:

```bash
curl -X POST http://127.0.0.1:8787/api/environment/init-fresh \
  -H 'Content-Type: application/json' \
  -d '{"database_label":"fresh_20260518_manual"}'
```

Confirm:

```bash
curl http://127.0.0.1:8787/api/environment
```
