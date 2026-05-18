# Briefing Design

Daily and weekly briefings are generated from recent events and pending reviews.

Endpoints:

- `GET /api/briefings/daily`
- `POST /api/briefings/daily/generate`
- `GET /api/briefings/weekly`
- `POST /api/briefings/weekly/generate`

Briefings are persisted and exportable as Markdown via `body_markdown`.
