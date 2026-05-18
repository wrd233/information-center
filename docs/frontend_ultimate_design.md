# content_inbox_console Operational Console Design

`content_inbox_console` is the main frontend control plane for content-inbox. The current release moves it from direct SQLite observation to backend API-driven operations.

Primary navigation: Dashboard, Environment, Sources, Ingest Runs, Information, Dedupe Groups, Clusters, Events, Entities, Relations, Claims, Topics, Timeline, Review Queue, Briefings, Reports, Agent Query, Settings.

The console uses FastAPI, Jinja, HTMX, and a small backend API client in `content_inbox_console/app/backend_client.py`. All operational writes go through the `content_inbox` backend `/api/*` contract.
