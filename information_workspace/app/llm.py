from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import hashlib
import json
import re
import time
import uuid

import httpx

from .config import BASE_DIR, Settings
from .schemas import CONTENT_FACETS
from .time_utils import timestamp_slug, utc_now


PROMPT_DIR = BASE_DIR / "prompts"


@dataclass(frozen=True)
class Prompt:
    name: str
    path: Path
    text: str
    version: str
    sha256: str


class LLMError(RuntimeError):
    pass


def load_prompt(file_name: str) -> Prompt:
    path = PROMPT_DIR / file_name
    text = path.read_text(encoding="utf-8")
    version = "unknown"
    for line in text.splitlines():
        if line.lower().startswith("version:"):
            version = line.split(":", 1)[1].strip()
            break
    return Prompt(
        name=file_name,
        path=path,
        text=text,
        version=version,
        sha256=hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
    )


def render_prompt(prompt: Prompt, input_data: dict[str, Any]) -> str:
    return (
        prompt.text
        + "\n\n## Runtime Input JSON\n\n```json\n"
        + json.dumps(input_data, ensure_ascii=False, indent=2)
        + "\n```\n\nReturn only JSON."
    )


def _extract_json(raw: str) -> Any:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()
    return json.loads(text)


def validate_light_understanding(value: Any) -> tuple[bool, str]:
    if not isinstance(value, dict):
        return False, "result is not an object"
    required = ["summary", "content_facets", "importance_reason", "uncertainties"]
    for key in required:
        if key not in value:
            return False, f"missing {key}"
    if not isinstance(value["summary"], str) or not value["summary"].strip():
        return False, "summary must be a non-empty string"
    if not isinstance(value["content_facets"], list) or not value["content_facets"]:
        return False, "content_facets must be a non-empty list"
    invalid = [facet for facet in value["content_facets"] if facet not in CONTENT_FACETS]
    if invalid:
        return False, f"invalid facets: {invalid}"
    if not isinstance(value["importance_reason"], str) or not value["importance_reason"].strip():
        return False, "importance_reason must be a non-empty string"
    if not isinstance(value["uncertainties"], list) or any(
        not isinstance(item, str) for item in value["uncertainties"]
    ):
        return False, "uncertainties must be a list of strings"
    if "uncertain" in value["content_facets"] and not value["uncertainties"]:
        return False, "uncertain facet requires at least one uncertainty note"
    return True, "valid"


def validate_event_candidates(value: Any) -> tuple[bool, str]:
    if not isinstance(value, dict) or not isinstance(value.get("candidates"), list):
        return False, "missing candidates list"
    for candidate in value["candidates"]:
        if not isinstance(candidate, dict):
            return False, "candidate is not an object"
        for key in ["title", "material_ids", "reason", "confidence", "doubts"]:
            if key not in candidate:
                return False, f"candidate missing {key}"
        if not isinstance(candidate["material_ids"], list):
            return False, "candidate material_ids must be list"
    return True, "valid"


def validate_topic_structure(value: Any) -> tuple[bool, str]:
    if not isinstance(value, dict) or not isinstance(value.get("structure"), dict):
        return False, "missing structure"
    structure = value["structure"]
    if not isinstance(structure.get("nodes"), list):
        return False, "structure.nodes must be list"
    return True, "valid"


def validate_event_update(value: Any) -> tuple[bool, str]:
    if not isinstance(value, dict):
        return False, "result is not an object"
    center = value.get("center_description")
    if not isinstance(center, dict):
        return False, "missing center_description"
    for key in ["main_thread", "known_facts", "recent_changes", "open_questions"]:
        if key not in center:
            return False, f"center_description missing {key}"
    return True, "valid"


def semantic_check(task_name: str, parsed: Any, input_data: dict[str, Any]) -> dict[str, Any]:
    notes: list[str] = []
    status = "passed"
    if task_name == "light_understanding" and isinstance(parsed, dict):
        content = str(input_data.get("content_text", ""))
        metadata = input_data.get("metadata") or {}
        fixture_group = metadata.get("fixture_group")
        summary = parsed.get("summary", "")
        if len(summary) > max(800, len(content) * 2):
            status = "warning"
            notes.append("summary is unexpectedly long compared with source")
        if "noise" in parsed.get("content_facets", []) and len(content) > 600:
            notes.append("long material marked noise; review recommended")
            status = "warning"
        if "noise" in parsed.get("content_facets", []) and fixture_group and fixture_group != "noise":
            notes.append(f"non-noise fixture_group marked noise: {fixture_group}")
            status = "warning"
        if "uncertain" in parsed.get("content_facets", []) and not parsed.get("uncertainties"):
            status = "warning"
            notes.append("uncertain facet without uncertainty notes")
    elif task_name in {"event_candidate", "topic_structure", "event_update"}:
        if not parsed:
            status = "warning"
            notes.append("empty parsed result")
    return {"status": status, "notes": notes, "checked_at": utc_now()}


def validate_task_output(task_name: str, value: Any) -> tuple[bool, str]:
    if task_name == "light_understanding":
        return validate_light_understanding(value)
    if task_name == "event_candidate":
        return validate_event_candidates(value)
    if task_name == "topic_structure":
        return validate_topic_structure(value)
    if task_name in {"topic_local_refresh", "event_update"}:
        return validate_topic_structure(value) if task_name == "topic_local_refresh" else validate_event_update(value)
    return True, "valid"


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def provider(self) -> str:
        return self.settings.llm_provider

    @property
    def model(self) -> str:
        return self.settings.deepseek_model

    def run_json_task(
        self,
        *,
        task_name: str,
        prompt_file: str,
        input_data: dict[str, Any],
        input_material_ids: list[str] | None = None,
        trace_mode: str = "business_summary",
        trace_dir: Path | None = None,
    ) -> dict[str, Any]:
        prompt = load_prompt(prompt_file)
        rendered_prompt = render_prompt(prompt, input_data)
        trace_root = trace_dir or self.settings.outputs_dir / "llm_traces" / timestamp_slug()
        trace_root.mkdir(parents=True, exist_ok=True)
        trace_path = trace_root / f"{task_name}_{uuid.uuid4().hex[:12]}.json"

        raw_model_output = ""
        parsed_json: Any = None
        validation = {"valid": False, "message": "not run"}
        repair_attempts: list[dict[str, Any]] = []
        retry_attempts: list[dict[str, Any]] = []
        final_status = "failed"
        error_summary = ""

        try:
            if self.provider == "mock":
                raw_model_output = json.dumps(self._mock_response(task_name, input_data), ensure_ascii=False)
            elif self.provider == "deepseek":
                if not self.settings.deepseek_api_key:
                    raise LLMError("DeepSeek API key is not configured")
                raw_model_output = self._call_deepseek(rendered_prompt)
            else:
                raise LLMError(f"Unsupported LLM provider: {self.provider}")

            try:
                parsed_json = _extract_json(raw_model_output)
            except Exception as parse_exc:  # noqa: BLE001
                repair = self._repair_json(
                    task_name=task_name,
                    invalid_output=raw_model_output,
                    validation_error=f"JSON parse failed: {parse_exc}",
                    trace_dir=trace_root,
                )
                repair_attempts.append(repair)
                if repair.get("parsed_json") is None:
                    raise LLMError(f"JSON parse failed: {parse_exc}") from parse_exc
                parsed_json = repair["parsed_json"]
            ok, message = validate_task_output(task_name, parsed_json)
            validation = {"valid": ok, "message": message}
            if not ok:
                repair = self._repair_json(
                    task_name=task_name,
                    invalid_output=raw_model_output,
                    validation_error=message,
                    trace_dir=trace_root,
                )
                repair_attempts.append(repair)
                if repair.get("parsed_json") is not None:
                    parsed_json = repair["parsed_json"]
                    ok, message = validate_task_output(task_name, parsed_json)
                    validation = {"valid": ok, "message": message, "after_repair": True}
            if not validation["valid"] and self.provider == "deepseek":
                retry_record: dict[str, Any] = {"status": "started"}
                try:
                    retry_raw = self._call_deepseek(rendered_prompt)
                    retry_record["raw_model_output"] = retry_raw
                    try:
                        retry_parsed = _extract_json(retry_raw)
                    except Exception as retry_parse_exc:  # noqa: BLE001
                        retry_repair = self._repair_json(
                            task_name=task_name,
                            invalid_output=retry_raw,
                            validation_error=f"retry JSON parse failed: {retry_parse_exc}",
                            trace_dir=trace_root,
                        )
                        retry_record["repair"] = retry_repair
                        retry_parsed = retry_repair.get("parsed_json")
                    if retry_parsed is not None:
                        retry_ok, retry_message = validate_task_output(task_name, retry_parsed)
                        retry_record["schema_validation_result"] = {"valid": retry_ok, "message": retry_message}
                        if retry_ok:
                            parsed_json = retry_parsed
                            validation = {"valid": True, "message": "valid", "after_retry": True}
                            raw_model_output = retry_raw
                            retry_record["status"] = "succeeded"
                        else:
                            retry_record["status"] = "failed"
                            retry_record["error"] = retry_message
                    else:
                        retry_record["status"] = "failed"
                        retry_record["error"] = "retry produced no parseable JSON"
                except Exception as retry_exc:  # noqa: BLE001
                    retry_record["status"] = "failed"
                    retry_record["error"] = str(retry_exc)
                retry_attempts.append(retry_record)
            if not validation["valid"]:
                raise LLMError(validation["message"])
            final_status = "succeeded"
        except Exception as exc:  # noqa: BLE001
            error_summary = str(exc)
            final_status = "failed"

        semantic = semantic_check(task_name, parsed_json, input_data) if parsed_json is not None else {
            "status": "failed",
            "notes": [error_summary or "no parsed output"],
            "checked_at": utc_now(),
        }
        trace = {
            "created_at": utc_now(),
            "task_name": task_name,
            "provider": self.provider,
            "model": self.model,
            "prompt_file": prompt.name,
            "prompt_version": prompt.version,
            "prompt_sha256": prompt.sha256,
            "input_material_ids": input_material_ids or [],
            "input_snapshot_mode": trace_mode,
            "rendered_prompt": rendered_prompt,
            "raw_model_output": raw_model_output,
            "parsed_json": parsed_json,
            "schema_validation_result": validation,
            "semantic_check": semantic,
            "repair_attempts": repair_attempts,
            "retry_attempts": retry_attempts,
            "final_status": final_status,
            "error_summary": error_summary,
        }
        trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "status": final_status,
            "parsed_json": parsed_json,
            "trace_path": str(trace_path),
            "semantic_check": semantic,
            "error_summary": error_summary,
            "provider": self.provider,
            "model": self.model,
            "prompt_file": prompt.name,
            "prompt_version": prompt.version,
        }

    def _call_deepseek(self, rendered_prompt: str) -> str:
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = httpx.post(
                    "https://api.deepseek.com/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.deepseek_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.settings.deepseek_model,
                        "messages": [
                            {"role": "system", "content": "You return only valid JSON for the requested schema."},
                            {"role": "user", "content": rendered_prompt},
                        ],
                        "temperature": 0.2,
                        "response_format": {"type": "json_object"},
                    },
                    timeout=90,
                )
                response.raise_for_status()
                payload = response.json()
                return payload["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as exc:
                last_error = exc
                if exc.response.status_code < 500 or attempt == 2:
                    raise
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt == 2:
                    raise
            time.sleep(1.5 * (attempt + 1))
        raise LLMError(str(last_error) if last_error else "DeepSeek call failed")

    def _repair_json(
        self,
        *,
        task_name: str,
        invalid_output: str,
        validation_error: str,
        trace_dir: Path,
    ) -> dict[str, Any]:
        if self.provider == "mock":
            return {"status": "skipped", "reason": "mock output should already be valid"}
        if not self.settings.deepseek_api_key:
            return {"status": "skipped", "reason": "no DeepSeek key configured"}
        prompt = load_prompt("json_repair_v1.md")
        rendered = render_prompt(
            prompt,
            {
                "task_name": task_name,
                "schema_description": task_name,
                "invalid_output": invalid_output,
                "validation_error": validation_error,
            },
        )
        try:
            raw = self._call_deepseek(rendered)
            parsed = _extract_json(raw)
            return {"status": "succeeded", "raw_output": raw, "parsed_json": parsed}
        except Exception as exc:  # noqa: BLE001
            return {"status": "failed", "error": str(exc), "trace_dir": str(trace_dir)}

    def _mock_response(self, task_name: str, input_data: dict[str, Any]) -> dict[str, Any]:
        if task_name == "light_understanding":
            text = str(input_data.get("content_text", ""))
            metadata = input_data.get("metadata") or {}
            group = str(metadata.get("fixture_group", "")).lower()
            title = str(input_data.get("title", "this synthetic material"))
            facets: list[str] = []
            if "noise" in group or "coupon" in text.lower() or len(text.strip()) < 80:
                facets.append("noise")
            if "uncertain" in group or "unconfirmed" in text.lower():
                facets.append("uncertain")
            if "technical" in group or any(word in text.lower() for word in ["api", "schema", "zabbix", "apm"]):
                facets.append("technical")
            if "opinion" in group or "argues" in text.lower():
                facets.append("opinion")
            if "article" in group or len(text) > 900:
                facets.append("article")
            if not facets:
                facets.append("news")
            first_sentence = re.split(r"(?<=[.!?])\s+", text.strip())[0][:280]
            uncertainties = []
            if "uncertain" in facets:
                uncertainties.append("Synthetic item intentionally lacks enough context for a firm classification.")
            if "conflicting" in group:
                uncertainties.append("Fixture group includes conflicting reports that need later verification.")
            return {
                "summary": f"{title}: {first_sentence}",
                "content_facets": sorted(set(facets)),
                "importance_reason": "Useful as a labeled synthetic fixture for ingestion, retrieval, Event/Topic, or export validation.",
                "uncertainties": uncertainties,
            }
        if task_name == "event_candidate":
            materials = input_data.get("materials") or []
            groups: dict[str, list[dict[str, Any]]] = {}
            for material in materials:
                meta = material.get("metadata") or {}
                if material.get("ignored") or "noise" in material.get("content_facets", []):
                    continue
                event_key = meta.get("event_key") or meta.get("fixture_group") or "general"
                groups.setdefault(str(event_key), []).append(material)
            candidates = []
            for key, items in groups.items():
                if not items:
                    continue
                candidates.append(
                    {
                        "title": f"Synthetic event: {key.replace('_', ' ')}",
                        "material_ids": [item["id"] for item in items[:8]],
                        "reason": "Materials share synthetic event metadata or fixture grouping.",
                        "confidence": 0.78 if len(items) > 1 else 0.55,
                        "possible_existing_event_id": None,
                        "doubts": [] if len(items) > 1 else ["Single-material candidate requires user review."],
                    }
                )
            return {"candidates": candidates}
        if task_name == "event_update":
            materials = input_data.get("new_materials") or []
            titles = [item.get("title", "material") for item in materials[:3]]
            return {
                "has_meaningful_update": bool(materials),
                "center_description": {
                    "main_thread": "Synthetic event center generated from selected materials.",
                    "known_facts": titles or ["No material facts supplied."],
                    "recent_changes": titles[:1],
                    "open_questions": ["Confirm whether synthetic fixture conflicts should change the event center."],
                },
                "update_reason": "Mock output for test-only Event center generation.",
                "supporting_material_ids": [item.get("id") for item in materials],
                "no_new_info_material_ids": [],
                "conflict_notes": [],
            }
        if task_name in {"topic_structure", "topic_local_refresh"}:
            materials = input_data.get("materials") or []
            nodes = []
            for index, material in enumerate(materials[:5], start=1):
                nodes.append(
                    {
                        "id": f"node-{index}",
                        "title": material.get("title", f"Material {index}")[:80],
                        "items": [
                            {
                                "type": "material",
                                "text": "Synthetic structure item anchored to one material.",
                                "material_ids": [material.get("id")],
                            }
                        ],
                        "children": [],
                    }
                )
            if not nodes:
                nodes.append(
                    {
                        "id": "node-1",
                        "title": "Initial structure",
                        "items": [{"type": "to_verify", "text": "No materials supplied.", "material_ids": []}],
                        "children": [],
                    }
                )
            return {
                "structure": {"title": input_data.get("topic", {}).get("title", "Candidate structure"), "nodes": nodes},
                "material_groups": [
                    {"name": "Synthetic inputs", "material_ids": [item.get("id") for item in materials], "reason": "Grouped for test-only structure generation."}
                ],
                "verification_points": ["Review evidence quality before accepting this candidate."],
                "conflict_points": [],
                "notes": "Mock provider output; valid for tests only.",
            }
        return {}
