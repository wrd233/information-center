# LLM Prompts

## Purpose

This document describes how `information_workspace` uses DeepSeek, prompt files, schema-bound outputs, traces, repair, and prompt evaluation.

## Configuration

Runtime reads local `.env` or environment variables:

```text
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-v4-flash
INFORMATION_WORKSPACE_LLM_PROVIDER=deepseek
```

The API key must never be committed, logged, returned by API, or written to reports/traces.

## Prompt Files

Required prompt files live under `prompts/`:

- `light_understanding_v1.md`
- `event_candidate_v1.md`
- `event_match_v1.md`
- `event_update_v1.md`
- `topic_structure_v1.md`
- `topic_local_refresh_v1.md`
- `export_package_v1.md`
- `json_repair_v1.md`

Each file includes version, purpose, input variables, output schema, forbidden behavior, semantic checks, failure handling, and examples.

## Schema-Bound Tasks

The following tasks must output JSON and pass validation before state writes: light understanding, Event candidate, Event match, Event update, Topic structure, and Topic local refresh.

Light understanding stores only:

```json
{
  "summary": "string",
  "content_facets": ["news"],
  "importance_reason": "string",
  "uncertainties": []
}
```

Allowed facets are `news`, `article`, `opinion`, `technical`, `noise`, and `uncertain`.

## Repair And Retry

Invalid JSON or schema violations trigger a repair attempt using `json_repair_v1.md`. Repair may fix format and field shape only. If repair and bounded retry fail, the step fails and no dirty result is written.

## Trace

Full traces are stored in `outputs/llm_traces/<timestamp>/`. Test and prompt_eval traces preserve full input snapshots. Ordinary business traces store IDs, titles, snippets, and lengths by default.

Trace files include model, provider, prompt file/version/hash, input IDs, rendered prompt, raw output, parsed JSON, validation result, semantic check, repair attempts, retry attempts, final status, and error summary.

## Prompt Eval

`scripts/prompt_eval.py` runs selected tasks over material IDs, run IDs, or synthetic fixture filters. Reports include coverage, schema results, semantic quality notes, prompt versions, trace paths, and recommended prompt changes.

For the final DeepSeek gate, use:

```bash
python3 scripts/run_real_deepseek_validation.py --all-light --import-sample
```

This helper runs required real tasks, writes `outputs/test_runs/<timestamp>/real_deepseek_validation.md`, samples trace semantic checks, and stops before network use when no key is configured.

## Mock Boundary

Mock mode is allowed only for tests and local smoke when explicitly requested. Mock outputs are labeled `llm_provider=mock` and cannot count toward final READY.
