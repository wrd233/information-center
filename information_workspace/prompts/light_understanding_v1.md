# light_understanding_v1

Version: 1.3

## Task

Read one material and produce compact, faithful light understanding for the Material library.

## Input Variables

- `material_id`
- `title`
- `source_name`
- `source_type`
- `published_at`
- `content_text`
- `upstream_score`
- `upstream_reason`

## Output JSON Schema

```json
{
  "summary": "string, 2-4 concise sentences faithful to the material",
  "content_facets": ["news|article|opinion|technical|noise|uncertain"],
  "importance_reason": "string, specific value or limited value for long-term library/Event/Topic use",
  "uncertainties": ["string"]
}
```

## Rules

- Use only allowed facets: `news`, `article`, `opinion`, `technical`, `noise`, `uncertain`.
- Do not add entities, keywords, sentiment, stance, or topic labels.
- Do not invent facts, dates, causes, names, or outcomes not present in the material.
- Use `uncertain` when the source, timing, context, or claim reliability is unclear.
- If you include the `uncertain` facet, `uncertainties` must contain at least one concrete uncertainty note.
- Use `noise` only for ads, fragments, boilerplate, empty context, or clearly low-value content.
- Do not mark a material as `noise` merely because it is synthetic, a test fixture, generated text, or includes a disclaimer that it is not real news. Synthetic materials can still be useful `news`, `article`, `opinion`, `technical`, or `uncertain` fixtures.
- If `metadata.fixture_group` is not `noise`, require clear low-value content evidence before using the `noise` facet.
- Hard constraint for this evaluation corpus: when `metadata.synthetic=true` and `metadata.fixture_group` is present and not exactly `noise`, do not include the `noise` facet. Use `uncertain` for weak or unclear non-noise fixtures.
- If a material has a coherent domain, scenario, evidence role, technical detail, Topic value, Event value, or export evidence role, prefer the non-noise facets that describe its content.
- Noise remains a Material; do not mark it ignored.

## Semantic Quality Checks

- Summary is faithful and does not change chronology.
- Importance reason is concrete, not generic.
- Uncertainties capture missing context, conflicts, or unsupported claims.
- `uncertain` never appears with an empty `uncertainties` list.
- `noise` is reserved for actual low-value content, not for synthetic labeling alone.

## Example Input

```json
{"title":"Synthetic observability team changes alert routing","source_type":"agent","content_text":"A synthetic incident note says the observability team tested a new routing rule for APM alerts. The note does not include production impact."}
```

## Example Output

```json
{
  "summary": "A synthetic incident note describes a test of a new APM alert routing rule. It does not report production impact or a confirmed outage.",
  "content_facets": ["technical", "uncertain"],
  "importance_reason": "Useful for tracking operations workflow changes, but limited because the note lacks production impact and rollout status.",
  "uncertainties": ["Whether the routing rule was deployed beyond a test", "Whether users or production systems were affected"]
}
```

## Negative Example

If metadata is `{"synthetic": true, "fixture_group": "topic_material"}`, do not output `noise` just because the material is synthetic. A Topic fixture with coherent content should be classified as `article`, `technical`, `opinion`, or `uncertain` according to content.
