# event_match_v1

Version: 1

## Task

Decide whether new materials match active official Events and whether the match is strong enough to attach as core, background, conflicting, or no-new-info support.

## Input Variables

- `material`
- `active_events`

## Output JSON Schema

```json
{
  "matches": [
    {
      "event_id": "string",
      "match_strength": "strong|medium|weak|none",
      "role": "core_update|background|supporting_no_new_info|conflicting|weak_related",
      "reason": "string",
      "new_information": true,
      "doubts": ["string"]
    }
  ]
}
```

## Rules

- Strong matches need specific overlap with the Event center description.
- Weakly related materials should not pollute official Events.
- User focus is a high-weight signal, but facts still need material evidence.
- Do not update Event time for no-new-info support.

## Semantic Quality Checks

- Match reason points to actual material evidence.
- New information is not just repeated background.
- Conflicts are not silently merged into known facts.
