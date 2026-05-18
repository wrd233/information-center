# Frontend Real Run Readiness

Real-write is intentionally gated by `CONTENT_INBOX_ENABLE_REAL_RUNS=1`. The console defaults to dry-run and selected sources.

Required operator flow:

1. Open Environment and confirm the fresh DB path.
2. Import sources with preview and commit.
3. Create a run from the wizard.
4. Preview impact.
5. Start dry-run first.
6. Start real-write only after confirmation and backend enablement.
7. Observe Run Detail events, source progress, and items.

The console has no hidden legacy database fallback.
