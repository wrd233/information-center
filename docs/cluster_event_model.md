# Cluster And Event Model

Clusters are stored in `event_clusters` with membership in `cluster_items`.

Event candidates are stored in `events` with membership in `event_items`.

The v1 heuristic groups by normalized title and marks single-item clusters as lower confidence. Manual event creation from cluster is supported by `/api/clusters/{cluster_id}/create-event`.
