# Semantic Phase 1 Status

Implemented:

- idempotent semantic tables and light `inbox_items` status columns
- item cards with batch generation and heuristic fallback
- item-item relation with deterministic rules and one-new-item/many-candidates LLM judge
- item-cluster relation with one-new-item/many-candidates LLM judge
- cluster card patch/rebuild with versioning
- cluster lifecycle statuses: active, cooling, archived, reopened, merged
- source profile recompute with priority suggestions
- review queue approve/reject
- semantic CLI and backend-only `/api/semantic/*` endpoints
- live DeepSeek smoke with temporary DB default

Deferred:

- vector indexes for item_cards and cluster_cards
- strict tool-call mode
- full cluster merge/split UI
- console UI integration

No console UI files are part of this implementation.
