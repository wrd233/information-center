from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
import urllib.request
from typing import Any, TypeVar

from pydantic import BaseModel

from app.config import settings
from app.semantic import db
from app.semantic.prompts import build_messages
from app.storage import InboxStore

T = TypeVar("T", bound=BaseModel)


class SemanticLLMClient:
    def __init__(
        self,
        store: InboxStore,
        *,
        live: bool = False,
        model: str | None = None,
        max_calls: int | None = None,
        dry_run: bool = False,
        token_budget: int | None = None,
        global_call_limit: bool = False,
    ) -> None:
        self.store = store
        self.live = live
        self.model = model or os.getenv("CONTENT_INBOX_LLM_SMALL_MODEL") or settings.llm.get("model", "deepseek-v4-flash")
        self.max_calls = max_calls if max_calls is not None else int(os.getenv("CONTENT_INBOX_LIVE_MAX_CALLS", "20"))
        self.dry_run = dry_run or os.getenv("CONTENT_INBOX_LIVE_DRY_RUN") == "1"
        self.token_budget = token_budget if token_budget is not None else int(os.getenv("CONTENT_INBOX_LIVE_TOKEN_BUDGET", "0") or "0")
        self.global_call_limit = global_call_limit
        self.calls = 0

    def api_key(self) -> str:
        return (
            os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("CONTENT_INBOX_DEEPSEEK_API_KEY")
            or settings.llm_api_key()
        )

    def base_url(self) -> str:
        return (os.getenv("DEEPSEEK_BASE_URL") or settings.llm.get("base_url") or "https://api.deepseek.com").rstrip("/")

    def enabled(self) -> tuple[bool, str]:
        if not self.live:
            return False, "live LLM disabled"
        if os.getenv("CONTENT_INBOX_LLM_ENABLE_LIVE") != "1":
            return False, "CONTENT_INBOX_LLM_ENABLE_LIVE is not 1"
        if self.dry_run:
            return False, "live LLM dry-run"
        if not self.api_key():
            return False, "missing DeepSeek API key"
        if self.calls >= self.max_calls:
            return False, "live max calls reached"
        if self.global_call_limit and self.calls_recorded() >= self.max_calls:
            return False, "live max calls reached"
        if self.token_budget and self.tokens_used() >= self.token_budget:
            return False, "live token budget reached"
        return True, "enabled"

    def tokens_used(self) -> int:
        with self.store.connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(total_tokens), 0) AS total FROM llm_call_logs WHERE status = 'ok'"
            ).fetchone()
        return int(row["total"] or 0)

    def calls_recorded(self) -> int:
        with self.store.connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM llm_call_logs WHERE status IN ('ok', 'failed')"
            ).fetchone()
        return int(row["n"] or 0)

    def call_json(
        self,
        *,
        task_type: str,
        prompt_version: str,
        schema_version: str,
        input_data: dict[str, Any],
        output_model: type[T],
        max_tokens: int = 1200,
        item_id: str | None = None,
        source_id: str | None = None,
        cluster_id: str | None = None,
    ) -> tuple[T | None, int | None, str]:
        fingerprint = db.input_fingerprint({"task": task_type, "prompt": prompt_version, "input": input_data})
        ok, reason = self.enabled()
        if not ok:
            call_id = db.insert_llm_call_log(
                self.store,
                task_type=task_type,
                model=self.model,
                prompt_version=prompt_version,
                schema_version=schema_version,
                fingerprint=fingerprint,
                latency_ms=0,
                status="skipped",
                request={"reason": reason},
                error=reason,
                item_id=item_id,
                source_id=source_id,
                cluster_id=cluster_id,
            )
            return None, call_id, reason

        input_json = json.dumps(input_data, ensure_ascii=False, sort_keys=True)
        request_summary = {
            "model": self.model,
            "messages_count": 0,
            "item_ids": extract_item_ids(input_data),
            "candidate_item_ids": extract_candidate_item_ids(input_data),
            "cluster_ids": extract_cluster_ids(input_data),
        }
        request_body = {
            "model": self.model,
            "temperature": float(settings.llm.get("temperature", 0.2)),
            "max_tokens": int(os.getenv("CONTENT_INBOX_LIVE_MAX_OUTPUT_TOKENS", str(max_tokens))),
            "messages": build_messages(prompt_version, input_json),
            "response_format": {"type": "json_object"},
        }
        return self._call_with_validation(
            task_type=task_type,
            prompt_version=prompt_version,
            schema_version=schema_version,
            fingerprint=fingerprint,
            request_body=request_body,
            request_summary=request_summary,
            output_model=output_model,
            input_json=input_json,
            item_id=item_id,
            source_id=source_id,
            cluster_id=cluster_id,
        )

    def _call_with_validation(
        self,
        *,
        task_type: str,
        prompt_version: str,
        schema_version: str,
        fingerprint: str,
        request_body: dict[str, Any],
        request_summary: dict[str, Any],
        output_model: type[T],
        input_json: str,
        item_id: str | None,
        source_id: str | None,
        cluster_id: str | None,
    ) -> tuple[T | None, int | None, str]:
        last_error = ""
        for attempt in range(2):
            started = time.monotonic()
            try:
                payload = self._post(request_body)
                latency_ms = int((time.monotonic() - started) * 1000)
                raw = payload["choices"][0]["message"]["content"]
                parsed = json.loads(raw)
                validated = output_model.model_validate(parsed)
                request_summary = dict(request_summary)
                request_summary["messages_count"] = len(request_body.get("messages", []))
                call_id = db.insert_llm_call_log(
                    self.store,
                    task_type=task_type,
                    model=self.model,
                    prompt_version=prompt_version,
                    schema_version=schema_version,
                    fingerprint=fingerprint,
                    latency_ms=latency_ms,
                    status="ok",
                    request=request_summary,
                    raw_output=raw,
                    parsed_output=validated.model_dump(),
                    usage=payload.get("usage", {}),
                    item_id=item_id,
                    source_id=source_id,
                    cluster_id=cluster_id,
                )
                self.calls += 1
                return validated, call_id, "ok"
            except Exception as exc:
                last_error = str(exc)
                if attempt == 0:
                    request_body = dict(request_body)
                    request_body["messages"] = build_messages(prompt_version, input_json, repair_error=last_error)
                    continue
                latency_ms = int((time.monotonic() - started) * 1000)
                request_summary = dict(request_summary)
                request_summary["messages_count"] = len(request_body.get("messages", []))
                call_id = db.insert_llm_call_log(
                    self.store,
                    task_type=task_type,
                    model=self.model,
                    prompt_version=prompt_version,
                    schema_version=schema_version,
                    fingerprint=fingerprint,
                    latency_ms=latency_ms,
                    status="failed",
                    request=request_summary,
                    error=last_error,
                    item_id=item_id,
                    source_id=source_id,
                    cluster_id=cluster_id,
                )
                self.calls += 1
                return None, call_id, last_error
        return None, None, last_error

    def _post(self, body: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url()}/chat/completions",
            data=data,
            method="POST",
            headers={"content-type": "application/json", "authorization": f"Bearer {self.api_key()}"},
        )
        timeout = float(settings.llm.get("timeout_seconds", 60))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(f"DeepSeek API returned {exc.code}: {detail}") from exc
        except (urllib.error.URLError, socket.timeout) as exc:
            raise RuntimeError(f"DeepSeek request failed: {exc}") from exc


def extract_item_ids(value: Any) -> list[str]:
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("item_id"), str) and node["item_id"] not in found:
                found.append(node["item_id"])
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return found


def extract_candidate_item_ids(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        for key in ("candidate_item_cards", "candidate_items"):
            for item in value.get(key) or []:
                if isinstance(item, dict) and item.get("item_id") not in out:
                    out.append(item.get("item_id"))
    return [item_id for item_id in out if item_id]


def extract_cluster_ids(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        for cluster in value.get("candidate_clusters") or []:
            if isinstance(cluster, dict) and cluster.get("cluster_id") not in out:
                out.append(cluster.get("cluster_id"))
    return [cluster_id for cluster_id in out if cluster_id]
