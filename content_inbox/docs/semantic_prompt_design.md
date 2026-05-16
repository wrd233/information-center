# Semantic Prompt Design

Prompt files live in `prompts/` and are loaded by `app.semantic.prompts`.

Files:

- `item_card_v1.md`
- `item_relation_v1.md`
- `item_cluster_relation_v1.md`
- `cluster_card_patch_v1.md`
- `source_review_v1.md`

Design rules:

- Stable system prompt prefix for DeepSeek context caching.
- Variable item/cluster data goes in the final user `Input JSON` block.
- Prompt text always includes the word JSON and an example JSON output.
- `primary_relation` is single-choice; `secondary_roles` is annotation-only.
- Prompts explicitly warn not to delete items, not to treat `same_topic` as `same_event`, and not to discard `related_with_new_info`, `new_info`, `analysis`, or `experience`.
- First-stage implementation uses JSON Output plus Pydantic validation and one repair retry.
