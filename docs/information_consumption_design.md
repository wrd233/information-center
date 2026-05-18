# Information Consumption Design

The information layer is built from real ingested items:

- `semantic_extractions`: lightweight rule extraction with low/medium confidence.
- `entities` and `item_entities`: extracted terms and item links.
- `event_clusters` and `cluster_items`: normalized-title/source/topic grouping.
- `events` and `event_items`: candidate events from clusters.
- `review_queue`: review tasks for low-confidence generated objects.
- `briefings` and `reports`: Markdown/JSON exportable summaries.

Advanced LLM semantic enrichment can replace or augment the lightweight processor later.
