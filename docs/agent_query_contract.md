# Agent Query Contract

`POST /api/agent-query/preview` accepts:

```json
{ "query": "AI model releases", "format": "compact", "limit": 10 }
```

It returns `human`, `markdown`, `json`, and `context_pack` formats backed by real item search.
