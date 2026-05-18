# API Contract

The new primary backend surface is `/api/*` with this envelope:

```json
{ "ok": true, "data": {}, "error": null, "meta": {} }
```

Errors use:

```json
{ "ok": false, "data": null, "error": { "code": "ERROR_CODE", "message": "Human readable", "details": {} }, "meta": {} }
```

Primary groups: environment, sources, runs, items, dedupe-groups, clusters, events, entities, relations, claims, topics, timeline, review-queue, evidence, briefings, saved-views, agent-query, reports.
