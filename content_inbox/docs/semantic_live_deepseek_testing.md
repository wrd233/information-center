# Semantic Live DeepSeek Testing

Live semantic tests are disabled by default.

Requirements:

```bash
export CONTENT_INBOX_LLM_ENABLE_LIVE=1
export CONTENT_INBOX_DEEPSEEK_API_KEY="..."
```

Smoke test:

```bash
PYTHONPATH=. python -m content_inbox.semantic live-smoke all --limit 3 --max-calls 10
```

Safety boundaries:

- No API key is printed.
- No long original content is printed.
- Default live smoke DB is temporary.
- Real DB writes require both `--db-path` and `--write-real-db`.
- `llm_call_logs` records model, prompt/schema version, input fingerprint, latency, status, token usage, cache token fields when present, raw output, parsed JSON, and errors.

Pytest live marker:

```bash
CONTENT_INBOX_LLM_ENABLE_LIVE=1 PYTHONPATH=. pytest -q -m live_deepseek
```
