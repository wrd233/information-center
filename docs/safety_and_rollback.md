# Safety And Rollback

Safety defaults:

- Fresh DB only.
- Dry-run by default.
- Selected sources by default.
- Import and bulk changes are preview-first.
- Real-write requires `CONTENT_INBOX_ENABLE_REAL_RUNS=1`.

Rollback v1 supports preview and soft rollback for items linked to a run with status `inserted`. It sets `inbox_items.deleted_at` and `rollback_run_id`.
