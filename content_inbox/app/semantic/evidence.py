from __future__ import annotations

import csv
import json
import math
import shutil
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.semantic.candidates import (
    assess_candidate,
    hotspot_key_candidates,
    infer_event_relation_type,
    relation_cluster_eligible,
    relation_pair_key,
)
from app.semantic.relations import normalized_entity_terms, semantic_tokens
from app.storage import InboxStore


SNIPPET_CHARS = 500


def safe_json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def parse_json_list(value: Any) -> list[Any]:
    parsed = safe_json(value)
    return parsed if isinstance(parsed, list) else []


def parse_json_dict(value: Any) -> dict[str, Any]:
    parsed = safe_json(value)
    return parsed if isinstance(parsed, dict) else {}


def snippet(value: Any, limit: int = SNIPPET_CHARS) -> str:
    text = "" if value is None else str(value)
    text = " ".join(text.split())
    return text[:limit]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            out = {}
            for key in keys:
                value = row.get(key)
                if isinstance(value, (dict, list)):
                    out[key] = json.dumps(value, ensure_ascii=False, sort_keys=True)
                else:
                    out[key] = value
            writer.writerow(out)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def original_item_id(item: dict[str, Any]) -> str:
    raw = parse_json_dict(item.get("raw_json")) or parse_json_dict(item.get("latest_raw_json"))
    return str(raw.get("source_item_id") or item.get("item_id") or "")


def item_lookup(store: InboxStore) -> dict[str, dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute("SELECT * FROM inbox_items").fetchall()
    return {row["item_id"]: dict(row) for row in rows}


def call_lookup(store: InboxStore) -> dict[int, dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute("SELECT * FROM llm_call_logs").fetchall()
    return {int(row["id"]): dict(row) for row in rows}


def hotspot_groups(sampled_items: list[dict[str, Any]], semantic_run_id: str) -> tuple[list[dict[str, Any]], dict[str, str], dict[str, str]]:
    token_items: dict[str, list[dict[str, Any]]] = defaultdict(list)
    token_sources: dict[str, set[str]] = defaultdict(set)
    token_meta: dict[str, dict[str, Any]] = {}
    for item in sampled_items:
        keys = hotspot_key_candidates(item)
        item_keys = [keys["selected_hotspot_key"]] + keys.get("dominant_entities", [])[:5] + keys.get("dominant_event_phrases", [])[:3]
        for token in normalized_entity_terms(item_keys):
            if len(token) < 3:
                continue
            token_items[token].append(item)
            token_sources[token].add(item.get("source_id") or item.get("source_name") or "")
            token_meta.setdefault(token, keys)
    ordered = sorted(
        token_items,
        key=lambda token: (len(token_sources[token]), len(token_items[token]), len(token)),
        reverse=True,
    )
    item_to_group: dict[str, str] = {}
    item_to_key: dict[str, str] = {}
    groups: list[dict[str, Any]] = []
    for index, token in enumerate(ordered[:50], start=1):
        members = token_items[token]
        if len(members) < 2:
            continue
        gid = f"hotspot_{index:03d}_{token[:32]}"
        for item in members:
            item_to_group.setdefault(item["item_id"], gid)
            item_to_key.setdefault(item["item_id"], token)
        times = [item.get("published_at") or item.get("created_at") for item in members if item.get("published_at") or item.get("created_at")]
        groups.append({
            "semantic_run_id": semantic_run_id,
            "hotspot_group_id": gid,
            "hotspot_key": token,
            "raw_candidate_keys": token_meta.get(token, {}).get("raw_candidate_keys", []),
            "filtered_keys": token_meta.get(token, {}).get("filtered_keys", []),
            "selected_hotspot_key": token,
            "key_source": token_meta.get(token, {}).get("key_source", "fallback"),
            "proxy_domain_filtered": token_meta.get(token, {}).get("proxy_domain_filtered", False),
            "group_size": len(members),
            "time_window_start": min(times) if times else None,
            "time_window_end": max(times) if times else None,
            "dominant_entities": token_meta.get(token, {}).get("dominant_entities") or [token],
            "dominant_event_phrases": token_meta.get(token, {}).get("dominant_event_phrases", []),
            "dominant_keywords": [token],
            "source_count": len({item.get("source_id") or item.get("source_name") for item in members}),
            "source_diversity_score": round(len({item.get("source_id") or item.get("source_name") for item in members}) / max(len(members), 1), 3),
            "time_window_days": time_window_days(times),
            "item_ids": [item["item_id"] for item in members],
            "original_item_ids": [original_item_id(item) for item in members],
            "candidate_pair_count": 0,
            "relation_call_count": 0,
            "non_different_relation_count": 0,
            "cluster_candidate_created": False,
            "final_multi_item_cluster": False,
            "failure_reason": None,
        })
    return groups, item_to_group, item_to_key


def time_window_days(times: list[str]) -> float:
    if len(times) < 2:
        return 0.0
    try:
        parsed = [datetime.fromisoformat(str(value).replace("Z", "+00:00")) for value in times]
        return round((max(parsed) - min(parsed)).total_seconds() / 86400, 3)
    except Exception:
        return 0.0


def title_similarity(left: str, right: str) -> float:
    a = semantic_tokens(left or "")
    b = semantic_tokens(right or "")
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, math.sqrt(len(a) * len(b)))


def candidate_score(a: dict[str, Any], b: dict[str, Any]) -> tuple[float, str]:
    title_score = title_similarity(a.get("title") or "", b.get("title") or "") * 5
    entities_a = normalized_entity_terms(list(semantic_tokens(f"{a.get('title') or ''} {a.get('summary') or ''}")))
    entities_b = normalized_entity_terms(list(semantic_tokens(f"{b.get('title') or ''} {b.get('summary') or ''}")))
    overlap = len(entities_a & entities_b)
    cross_source = (a.get("source_id") or "") != (b.get("source_id") or "")
    score = title_score + overlap * 2 + (0.75 if cross_source else 0)
    reasons = [f"title_similarity={title_score:.2f}", f"entity_overlap={overlap}"]
    if cross_source:
        reasons.append("cross_source_bonus")
    return round(score, 3), "; ".join(reasons)


def export_evidence(
    *,
    run_dir: Path,
    source_store: InboxStore,
    target_store: InboxStore,
    metadata: dict[str, Any],
    summary: dict[str, Any],
    sampled_items: list[dict[str, Any]],
    phase_label: str,
    backup_path: str | None = None,
) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    semantic_run_id = metadata["run_id"]
    evidence_files: list[str] = []
    items_by_id = item_lookup(target_store)
    calls_by_id = call_lookup(target_store)
    hotspot_rows, item_to_hotspot, item_to_hotspot_key = hotspot_groups(sampled_items, semantic_run_id)

    semantic_items = build_semantic_items(semantic_run_id, sampled_items, item_to_hotspot, item_to_hotspot_key)
    item_cards, item_failures = build_item_cards(target_store, semantic_run_id, items_by_id, calls_by_id)
    relation_rows = build_relations(target_store, semantic_run_id, items_by_id, calls_by_id, item_to_hotspot)
    interesting_rows = interesting_relations(relation_rows)
    candidate_generation, candidate_suppression = build_candidate_evidence(target_store, semantic_run_id, items_by_id)
    cluster_candidates, cluster_attachments, clusters_final, cluster_diagnostics = build_cluster_evidence(
        target_store, semantic_run_id, items_by_id, calls_by_id, item_to_hotspot
    )
    llm_calls, llm_errors, budget_skips = build_llm_evidence(target_store, semantic_run_id)
    stage_metrics = {
        "semantic_run_id": semantic_run_id,
        "stage_budgets": summary.get("stage_budgets"),
        "token_cost": summary.get("token_cost"),
        "errors_fallbacks": summary.get("errors_fallbacks"),
        "concurrency": summary.get("concurrency"),
    }
    enrich_hotspots(hotspot_rows, relation_rows, cluster_candidates, clusters_final)

    file_specs = [
        ("semantic_items.jsonl", semantic_items, "jsonl"), ("semantic_items.csv", semantic_items, "csv"),
        ("item_cards.jsonl", item_cards, "jsonl"), ("item_cards.csv", item_cards, "csv"),
        ("item_card_failures.jsonl", item_failures, "jsonl"),
        ("relations_all.jsonl", relation_rows, "jsonl"), ("relations_all.csv", relation_rows, "csv"),
        ("relations_interesting.jsonl", interesting_rows, "jsonl"), ("relations_interesting.csv", interesting_rows, "csv"),
        ("candidate_generation.jsonl", candidate_generation, "jsonl"),
        ("candidate_suppression.jsonl", candidate_suppression, "jsonl"),
        ("event_hotspots.jsonl", hotspot_rows, "jsonl"),
        ("event_hotspot_items.csv", flatten_hotspot_items(hotspot_rows, items_by_id), "csv"),
        ("cluster_candidates.jsonl", cluster_candidates, "jsonl"),
        ("cluster_attachments.jsonl", cluster_attachments, "jsonl"),
        ("clusters_final.jsonl", clusters_final, "jsonl"),
        ("cluster_diagnostics.csv", cluster_diagnostics, "csv"),
        ("llm_calls.jsonl", llm_calls, "jsonl"),
        ("llm_errors.jsonl", llm_errors, "jsonl"),
        ("budget_skips.jsonl", budget_skips, "jsonl"),
    ]
    for name, rows, kind in file_specs:
        path = run_dir / name
        if kind == "jsonl":
            write_jsonl(path, rows)
        else:
            write_csv(path, rows)
        evidence_files.append(str(path))
    write_json(run_dir / "stage_metrics.json", stage_metrics)
    evidence_files.append(str(run_dir / "stage_metrics.json"))
    cost_metrics = cost_quality_metrics(summary, relation_rows, candidate_generation, candidate_suppression, clusters_final)
    write_json(run_dir / "cost_quality_metrics.json", cost_metrics)
    evidence_files.append(str(run_dir / "cost_quality_metrics.json"))
    comparison = phase_comparison(run_dir, cost_metrics)
    write_json(run_dir / "phase1_2d_vs_1_2e_comparison.json", comparison)
    evidence_files.append(str(run_dir / "phase1_2d_vs_1_2e_comparison.json"))

    manifest = {
        "phase": phase_label,
        "run_id": semantic_run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": metadata.get("git_commit"),
        "repo_path": str(Path.cwd().parent),
        "scope": "api.xgo.ing*" if metadata.get("source_url_prefix") else metadata.get("source_filter"),
        "sample_mode": metadata.get("sample_mode"),
        "item_count_requested": metadata.get("max_items"),
        "item_count_actual": metadata.get("items_sampled"),
        "concurrency": metadata.get("concurrency"),
        "stage_budget_profile": metadata.get("stage_budget_profile"),
        "semantic_write_real_db": bool(metadata.get("write_real_db")),
        "model_provider": "DeepSeek",
        "model_name": metadata.get("model"),
        "db_path": metadata.get("db_path"),
        "backup_path": backup_path,
        "output_dir": str(run_dir),
        "evidence_files": evidence_files,
        "warnings": metadata.get("warnings", []),
    }
    write_json(run_dir / "semantic_run_manifest.json", manifest)
    evidence_files.insert(0, str(run_dir / "semantic_run_manifest.json"))
    return {
        "manifest": manifest,
        "counts": {
            "semantic_items": len(semantic_items),
            "item_cards": len(item_cards),
            "item_card_failures": len(item_failures),
            "relations_all": len(relation_rows),
            "relations_interesting": len(interesting_rows),
            "candidate_generation": len(candidate_generation),
            "candidate_suppression": len(candidate_suppression),
            "event_hotspots": len(hotspot_rows),
            "cluster_candidates": len(cluster_candidates),
            "cluster_attachments": len(cluster_attachments),
            "clusters_final": len(clusters_final),
            "llm_calls": len(llm_calls),
            "llm_errors": len(llm_errors),
            "budget_skips": len(budget_skips),
        },
        "evidence_files": evidence_files,
    }


def build_semantic_items(run_id: str, items: list[dict[str, Any]], item_to_hotspot: dict[str, str], item_to_key: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for item in items:
        rows.append({
            "semantic_run_id": run_id,
            "dry_run_item_id": item["item_id"],
            "original_item_id": original_item_id(item),
            "source_id": item.get("source_id"),
            "source_name": item.get("source_name"),
            "feed_url": item.get("feed_url"),
            "title": item.get("title"),
            "url": item.get("url"),
            "guid": item.get("guid"),
            "dedupe_key": item.get("dedupe_key"),
            "dedupe_version": item.get("dedupe_version"),
            "published_at": item.get("published_at"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "language": None,
            "content_type": item.get("content_type"),
            "summary_snippet": snippet(item.get("summary")),
            "content_snippet": snippet(item.get("content_text")),
            "sample_reason": "event_hotspots",
            "hotspot_key": item_to_key.get(item["item_id"]),
            "hotspot_group_id": item_to_hotspot.get(item["item_id"]),
            "selected_for_item_card": True,
            "selected_for_relation": True,
            "selected_for_cluster": True,
        })
    return rows


def build_item_cards(store: InboxStore, run_id: str, items: dict[str, dict[str, Any]], calls: dict[int, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    with store.connect() as conn:
        cards = [dict(row) for row in conn.execute("SELECT * FROM item_cards WHERE is_current = 1").fetchall()]
        failed = [dict(row) for row in conn.execute("SELECT * FROM llm_call_logs WHERE task_type = 'item_card' AND status = 'failed'").fetchall()]
    rows = []
    for card in cards:
        item = items.get(card["item_id"], {})
        qh = parse_json_dict(card.get("quality_hints_json"))
        warnings = parse_json_list(card.get("warnings_json"))
        call = calls.get(int(card["llm_call_id"])) if card.get("llm_call_id") else None
        method = "minimal_rule" if card.get("model") == "minimal_rule" else "heuristic_fallback" if "heuristic_card" in warnings or card.get("model") == "heuristic" else "llm"
        rows.append({
            "semantic_run_id": run_id,
            "item_id": card["item_id"],
            "original_item_id": original_item_id(item) if item else card["item_id"],
            "source_id": item.get("source_id"),
            "title": item.get("title") or card.get("canonical_title"),
            "url": item.get("url"),
            "card_tier": qh.get("card_tier") or ("minimal" if card.get("model") == "minimal_rule" else "unknown"),
            "card_method": method,
            "card_success": True,
            "fallback": method == "heuristic_fallback",
            "fallback_reason": "LLM skipped or failed" if method == "heuristic_fallback" else None,
            "confidence": card.get("confidence"),
            "content_role": card.get("content_role"),
            "event_type": card.get("event_hint"),
            "entities": parse_json_list(card.get("entities_json")),
            "claims": parse_json_list(card.get("key_opinions_json")),
            "core_facts": parse_json_list(card.get("key_facts_json")),
            "summary": card.get("short_summary"),
            "tokens_input": call.get("prompt_tokens") if call else 0,
            "tokens_output": call.get("completion_tokens") if call else 0,
            "model": card.get("model"),
            "latency_ms": call.get("latency_ms") if call else 0,
            "llm_attempt_count": (parse_json_dict(call.get("request_json")).get("attempt_number") if call else 0) or 0,
            "batch_retry_count": 1 if call and parse_json_dict(call.get("request_json")).get("retry_strategy") == "same_batch" else 0,
            "single_retry_count": 1 if call and parse_json_dict(call.get("request_json")).get("retry_strategy") == "split_single" else 0,
            "json_repair_used": bool(call and (parse_json_dict(call.get("request_json")).get("retry_attempt") or 0) > 0),
        })
    failures = []
    for call in failed:
        request = parse_json_dict(call.get("request_json"))
        ids = request.get("item_ids") or split_ids(call.get("item_id"))
        for item_id in ids or [call.get("item_id")]:
            item = items.get(item_id or "", {})
            failures.append({
                "semantic_run_id": run_id,
                "item_id": item_id,
                "original_item_id": original_item_id(item) if item else item_id,
                "source_id": item.get("source_id") or call.get("source_id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "stage": "item_card",
                "error_type": classify_error(call.get("error")),
                "error_message": snippet(call.get("error"), 1000),
                "raw_response_snippet": snippet(call.get("raw_output")),
                "batch_id": request.get("batch_id"),
                "batch_size": request.get("batch_size") or len(ids or []),
                "attempt_number": request.get("attempt_number"),
                "retry_strategy": request.get("retry_strategy"),
                "affected_item_count": request.get("affected_item_count") or len(ids or []),
                "final_card_success": item_id in {row["item_id"] for row in rows},
                "final_method": "llm" if any(row["item_id"] == item_id and row["card_method"] == "llm" for row in rows) else "heuristic_fallback",
                "fallback_attempted": True,
                "fallback_success": item_id in {row["item_id"] for row in rows},
                "created_at": call.get("created_at"),
            })
    return rows, failures


def split_ids(value: Any) -> list[str]:
    if not value:
        return []
    return [part for part in str(value).split(",") if part]


def classify_error(error: Any) -> str:
    text = str(error or "").lower()
    if "json" in text or "validation" in text:
        return "parse_or_validation"
    if "rate" in text or "429" in text:
        return "rate_limit"
    if "timeout" in text or "timed out" in text:
        return "timeout"
    if not text:
        return "unknown"
    return "llm_error"


def build_relations(store: InboxStore, run_id: str, items: dict[str, dict[str, Any]], calls: dict[int, dict[str, Any]], item_to_hotspot: dict[str, str]) -> list[dict[str, Any]]:
    with store.connect() as conn:
        relations = [dict(row) for row in conn.execute("SELECT * FROM item_relations ORDER BY id").fetchall()]
        candidate_rows = []
        try:
            candidate_rows = [dict(row) for row in conn.execute("SELECT * FROM semantic_candidate_events ORDER BY id").fetchall()]
        except Exception:
            candidate_rows = []
    candidate_by_pair: dict[str, dict[str, Any]] = {}
    event_by_pair: dict[str, dict[str, Any]] = {}
    for row in candidate_rows:
        key = row.get("relation_pair_key")
        if not key:
            continue
        meta = parse_json_dict(row.get("metadata_json"))
        if row.get("status") in {"generated", "suppressed"} and key not in candidate_by_pair:
            candidate_by_pair[key] = row
        if row.get("status") in {"llm_relation_written", "rule_relation_written"}:
            event_by_pair[key] = {**row, "metadata": meta}
    rows = []
    seen_pair_keys: dict[str, str] = {}
    for rel in relations:
        a = items.get(rel["item_a_id"], {})
        b = items.get(rel["item_b_id"], {})
        call = calls.get(int(rel["llm_call_id"])) if rel.get("llm_call_id") else None
        pair_key = relation_pair_key(a, b) if a and b else f"{rel['item_a_id']}|{rel['item_b_id']}"
        assessment = assess_candidate(a, b)
        event_meta = event_by_pair.get(pair_key, {}).get("metadata", {})
        candidate = candidate_by_pair.get(pair_key, {})
        candidate_meta = parse_json_dict(candidate.get("metadata_json"))
        score = candidate.get("candidate_score") or assessment.candidate_score
        reason = candidate_meta.get("candidate_generation_reason") or "; ".join(assessment.same_event_evidence or assessment.disqualifiers)
        event_relation_type = event_meta.get("event_relation_type") or infer_event_relation_type(
            rel["primary_relation"],
            assessment,
            reason=rel.get("reason") or "",
            evidence=parse_json_list(rel.get("evidence_json")),
            new_information=parse_json_list(rel.get("new_information_json")),
        )
        cluster_eligible = bool(event_meta.get("cluster_eligible")) if "cluster_eligible" in event_meta else relation_cluster_eligible(rel["primary_relation"], event_relation_type)
        is_duplicate_direction = pair_key in seen_pair_keys
        duplicate_of = seen_pair_keys.get(pair_key)
        if not duplicate_of:
            seen_pair_keys[pair_key] = str(rel["id"])
        rows.append({
            "semantic_run_id": run_id,
            "relation_id": str(rel["id"]),
            "relation_pair_key": pair_key,
            "is_canonical_pair": not is_duplicate_direction,
            "is_duplicate_direction": is_duplicate_direction,
            "duplicate_of_relation_id": duplicate_of,
            "item_a_id": rel["item_a_id"],
            "item_b_id": rel["item_b_id"],
            "item_a_original_id": original_item_id(a) if a else rel["item_a_id"],
            "item_b_original_id": original_item_id(b) if b else rel["item_b_id"],
            "item_a_source_id": a.get("source_id"),
            "item_b_source_id": b.get("source_id"),
            "item_a_source_name": a.get("source_name"),
            "item_b_source_name": b.get("source_name"),
            "item_a_title": a.get("title"),
            "item_b_title": b.get("title"),
            "item_a_url": a.get("url"),
            "item_b_url": b.get("url"),
            "item_a_published_at": a.get("published_at"),
            "item_b_published_at": b.get("published_at"),
            "item_a_summary_snippet": snippet(a.get("summary") or a.get("content_text")),
            "item_b_summary_snippet": snippet(b.get("summary") or b.get("content_text")),
            "candidate_generation_reason": reason,
            "candidate_score": score,
            "candidate_priority": candidate.get("candidate_priority") or assessment.candidate_priority,
            "candidate_score_components": parse_json_dict(candidate.get("candidate_score_components_json")) or assessment.candidate_score_components,
            "candidate_suppression_reason": candidate.get("candidate_suppression_reason"),
            "hotspot_group_id": item_to_hotspot.get(rel["item_a_id"]) or item_to_hotspot.get(rel["item_b_id"]),
            "relation_label": rel["primary_relation"],
            "event_relation_type": event_relation_type,
            "cluster_eligible": cluster_eligible,
            "shared_entities": event_meta.get("shared_entities") or assessment.shared_entities,
            "shared_entities_weighted": event_meta.get("shared_entities_weighted") or assessment.shared_entities_weighted,
            "boilerplate_detected": bool(event_meta.get("boilerplate_detected", assessment.boilerplate_detected)),
            "generic_entity_overlap": bool(event_meta.get("generic_entity_overlap", assessment.generic_entity_overlap)),
            "same_event_evidence": event_meta.get("same_event_evidence") or assessment.same_event_evidence,
            "new_info_evidence": event_meta.get("new_info_evidence") or parse_json_list(rel.get("new_information_json")),
            "disqualifiers": event_meta.get("disqualifiers") or assessment.disqualifiers,
            "should_fold": bool(rel["should_fold"]),
            "confidence": rel.get("confidence"),
            "reason": rel.get("reason"),
            "evidence": parse_json_list(rel.get("evidence_json")),
            "tokens_input": call.get("prompt_tokens") if call else 0,
            "tokens_output": call.get("completion_tokens") if call else 0,
            "model": rel.get("model"),
            "latency_ms": call.get("latency_ms") if call else 0,
            "error": call.get("error") if call else None,
        })
    return rows


def build_candidate_evidence(store: InboxStore, run_id: str, items: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    with store.connect() as conn:
        try:
            rows = [dict(row) for row in conn.execute("SELECT * FROM semantic_candidate_events ORDER BY id").fetchall()]
        except Exception:
            return [], []
    generation: list[dict[str, Any]] = []
    suppression: list[dict[str, Any]] = []
    for row in rows:
        a = items.get(row.get("item_a_id") or "", {})
        b = items.get(row.get("item_b_id") or "", {})
        meta = parse_json_dict(row.get("metadata_json"))
        base = {
            "semantic_run_id": run_id,
            "candidate_event_id": row["id"],
            "stage": row.get("stage"),
            "item_a_id": row.get("item_a_id"),
            "item_b_id": row.get("item_b_id"),
            "item_a_original_id": original_item_id(a) if a else row.get("item_a_id"),
            "item_b_original_id": original_item_id(b) if b else row.get("item_b_id"),
            "item_a_title": a.get("title"),
            "item_b_title": b.get("title"),
            "relation_pair_key": row.get("relation_pair_key"),
            "candidate_priority": row.get("candidate_priority"),
            "candidate_score": row.get("candidate_score"),
            "candidate_score_components": parse_json_dict(row.get("candidate_score_components_json")),
            "candidate_suppression_reason": row.get("candidate_suppression_reason"),
            "status": row.get("status"),
            "metadata": meta,
            "created_at": row.get("created_at"),
        }
        generation.append(base)
        if row.get("status") == "suppressed" or row.get("candidate_priority") == "suppress":
            suppression.append({
                **base,
                "skip_reason": row.get("candidate_suppression_reason") or meta.get("candidate_suppression_reason") or "suppressed_low_value",
                "would_have_been_stage": row.get("stage"),
                "is_high_priority_skip": row.get("candidate_priority") in {"must_run", "high"},
            })
    return generation, suppression


def interesting_relations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    interesting = [
        row for row in rows
        if row["relation_label"] in {"duplicate", "near_duplicate", "related_with_new_info", "uncertain"}
        and not row.get("is_duplicate_direction")
    ]
    suspicious = sorted(
        [row for row in rows if row["relation_label"] == "different"],
        key=lambda row: (row.get("candidate_score") or 0, row.get("confidence") or 0),
        reverse=True,
    )[:30]
    for row in suspicious:
        row = dict(row)
        row["relation_label"] = "suspicious_different"
        interesting.append(row)
    return interesting


def build_cluster_evidence(
    store: InboxStore,
    run_id: str,
    items: dict[str, dict[str, Any]],
    calls: dict[int, dict[str, Any]],
    item_to_hotspot: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    with store.connect() as conn:
        cluster_items = [dict(row) for row in conn.execute("SELECT * FROM cluster_items ORDER BY id").fetchall()]
        clusters = [dict(row) for row in conn.execute("SELECT * FROM event_clusters ORDER BY created_at").fetchall()]
        relations = [dict(row) for row in conn.execute("SELECT * FROM item_relations ORDER BY id").fetchall()]
        reviews = [dict(row) for row in conn.execute("SELECT * FROM review_queue WHERE review_type IN ('same_topic','uncertain_cluster_relation')").fetchall()]
        skipped = [dict(row) for row in conn.execute("SELECT * FROM llm_call_logs WHERE task_type = 'item_cluster_relation' AND status = 'skipped'").fetchall()]
    candidates: list[dict[str, Any]] = []
    attachments: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    relation_by_item: dict[str, dict[str, Any]] = {}
    for rel in relations:
        if rel.get("primary_relation") in {"duplicate", "near_duplicate", "related_with_new_info"}:
            relation_by_item.setdefault(rel["item_a_id"], rel)
            relation_by_item.setdefault(rel["item_b_id"], rel)
    for ci in cluster_items:
        item = items.get(ci["item_id"], {})
        call = calls.get(int(ci["llm_call_id"])) if ci.get("llm_call_id") else None
        source_rel = relation_by_item.get(ci["item_id"])
        source_rel_item = items.get(source_rel["item_b_id"], {}) if source_rel else {}
        source_pair_key = relation_pair_key(item, source_rel_item) if item and source_rel_item else None
        source_event_type = "same_event" if source_rel and source_rel.get("primary_relation") in {"duplicate", "near_duplicate", "related_with_new_info"} else None
        source_cluster_eligible = bool(source_rel and source_event_type == "same_event")
        candidate_id = f"cluster_candidate_{ci['id']}"
        decision = "attached" if ci.get("decision_source") == "llm" else "attached_rule"
        candidates.append({
            "semantic_run_id": run_id,
            "cluster_candidate_id": candidate_id,
            "hotspot_group_id": item_to_hotspot.get(ci["item_id"]),
            "seed_item_id": ci["item_id"],
            "seed_original_item_id": original_item_id(item) if item else ci["item_id"],
            "candidate_item_ids": [ci["item_id"]],
            "candidate_original_item_ids": [original_item_id(item) if item else ci["item_id"]],
            "candidate_titles": [item.get("title")],
            "candidate_sources": [item.get("source_id")],
            "candidate_generation_reason": "cluster_items persisted decision",
            "candidate_score": ci.get("confidence") or 0,
            "created_cluster_id": ci["cluster_id"],
            "final_member_count": cluster_member_count(cluster_items, ci["cluster_id"]),
            "final_status": "multi_item" if cluster_member_count(cluster_items, ci["cluster_id"]) > 1 else "single_item",
            "diagnostic_reason": ci.get("reason"),
        })
        attachments.append({
            "semantic_run_id": run_id,
            "cluster_candidate_id": candidate_id,
            "cluster_id": ci["cluster_id"],
            "item_id": ci["item_id"],
            "original_item_id": original_item_id(item) if item else ci["item_id"],
            "item_title": item.get("title"),
            "item_url": item.get("url"),
            "decision": decision,
            "cluster_relation_label": ci["primary_relation"],
            "relation_pair_key": source_pair_key,
            "source_relation_id": str(source_rel["id"]) if source_rel else None,
            "source_relation_label": source_rel.get("primary_relation") if source_rel else None,
            "source_event_relation_type": source_event_type,
            "source_cluster_eligible": source_cluster_eligible,
            "cluster_relation_type": cluster_relation_type(ci["primary_relation"]),
            "attach_eligible": cluster_attach_eligible(ci["primary_relation"], source_cluster_eligible),
            "attach_disqualifiers": [] if cluster_attach_eligible(ci["primary_relation"], source_cluster_eligible) else ["not_same_event_eligible"],
            "decision_source": ci.get("decision_source"),
            "confidence": ci.get("confidence"),
            "reason": ci.get("reason"),
            "tokens_input": call.get("prompt_tokens") if call else 0,
            "tokens_output": call.get("completion_tokens") if call else 0,
            "model": ci.get("model"),
            "latency_ms": call.get("latency_ms") if call else 0,
        })
    for review in reviews:
        suggestion = parse_json_dict(review.get("suggestion_json"))
        item_id = review.get("target_id")
        item = items.get(item_id or "", {})
        candidate_id = f"cluster_candidate_review_{review['id']}"
        candidates.append({
            "semantic_run_id": run_id,
            "cluster_candidate_id": candidate_id,
            "hotspot_group_id": item_to_hotspot.get(item_id or ""),
            "seed_item_id": item_id,
            "seed_original_item_id": original_item_id(item) if item else item_id,
            "candidate_item_ids": [item_id],
            "candidate_original_item_ids": [original_item_id(item) if item else item_id],
            "candidate_titles": [item.get("title")],
            "candidate_sources": [item.get("source_id")],
            "candidate_generation_reason": "review_queue rejection/uncertainty",
            "candidate_score": suggestion.get("confidence") or 0,
            "created_cluster_id": suggestion.get("cluster_id"),
            "final_member_count": 0,
            "final_status": "rejected",
            "diagnostic_reason": suggestion.get("reason") or review.get("reason"),
        })
        attachments.append({
            "semantic_run_id": run_id,
            "cluster_candidate_id": candidate_id,
            "cluster_id": suggestion.get("cluster_id"),
            "item_id": item_id,
            "original_item_id": original_item_id(item) if item else item_id,
            "item_title": item.get("title"),
            "item_url": item.get("url"),
            "decision": "rejected" if review.get("review_type") == "same_topic" else "error" if review.get("review_type") == "uncertain_cluster_relation" else "skipped",
            "cluster_relation_label": suggestion.get("primary_relation") or review.get("review_type"),
            "relation_pair_key": None,
            "source_relation_id": None,
            "source_relation_label": None,
            "source_event_relation_type": suggestion.get("cluster_relation_type"),
            "source_cluster_eligible": False,
            "cluster_relation_type": suggestion.get("cluster_relation_type") or cluster_relation_type(suggestion.get("primary_relation") or review.get("review_type")),
            "attach_eligible": False,
            "attach_disqualifiers": suggestion.get("attach_disqualifiers") or ["review_or_rejected"],
            "decision_source": "review",
            "confidence": suggestion.get("confidence"),
            "reason": suggestion.get("reason") or review.get("reason"),
            "tokens_input": 0,
            "tokens_output": 0,
            "model": suggestion.get("model"),
            "latency_ms": 0,
        })
    for call in skipped:
        item_id = call.get("item_id")
        item = items.get(item_id or "", {})
        candidate_id = f"cluster_candidate_skip_{call['id']}"
        attachments.append({
            "semantic_run_id": run_id,
            "cluster_candidate_id": candidate_id,
            "cluster_id": call.get("cluster_id"),
            "item_id": item_id,
            "original_item_id": original_item_id(item) if item else item_id,
            "item_title": item.get("title"),
            "item_url": item.get("url"),
            "decision": "budget_skipped" if "budget" in (call.get("error") or "") else "skipped",
            "cluster_relation_label": None,
            "relation_pair_key": None,
            "source_relation_id": None,
            "source_relation_label": None,
            "source_event_relation_type": None,
            "source_cluster_eligible": False,
            "cluster_relation_type": "uncertain",
            "attach_eligible": False,
            "attach_disqualifiers": ["budget_skipped"],
            "decision_source": "budget_skipped",
            "confidence": 0,
            "reason": call.get("error"),
            "tokens_input": 0,
            "tokens_output": 0,
            "model": call.get("model"),
            "latency_ms": call.get("latency_ms") or 0,
        })
    final = []
    by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ci in cluster_items:
        by_cluster[ci["cluster_id"]].append(ci)
    for cluster in clusters:
        members = by_cluster.get(cluster["cluster_id"], [])
        member_items = [items.get(ci["item_id"], {}) for ci in members]
        times = [item.get("published_at") or item.get("created_at") for item in member_items if item]
        rel_counter = Counter(ci["primary_relation"] for ci in members)
        final.append({
            "semantic_run_id": run_id,
            "cluster_id": cluster["cluster_id"],
            "member_count": len(members),
            "member_item_ids": [ci["item_id"] for ci in members],
            "member_original_item_ids": [original_item_id(item) for item in member_items if item],
            "representative_title": cluster.get("cluster_title"),
            "cluster_title": cluster.get("cluster_title"),
            "cluster_summary": cluster.get("cluster_summary"),
            "source_count": len({item.get("source_id") for item in member_items if item}),
            "time_window_start": min(times) if times else None,
            "time_window_end": max(times) if times else None,
            "relation_summary": dict(rel_counter),
        })
    for candidate in candidates:
        diagnostics.append({
            "cluster_candidate_id": candidate["cluster_candidate_id"],
            "final_status": candidate["final_status"],
            "final_member_count": candidate["final_member_count"],
            "diagnostic_reason": candidate["diagnostic_reason"],
        })
    return candidates, attachments, final, diagnostics


def cluster_member_count(cluster_items: list[dict[str, Any]], cluster_id: str) -> int:
    return sum(1 for row in cluster_items if row["cluster_id"] == cluster_id)


def cluster_relation_type(primary_relation: str | None) -> str:
    if primary_relation == "source_material":
        return "source_material"
    if primary_relation == "repeat":
        return "same_event_repeat"
    if primary_relation in {"new_info", "analysis", "experience", "context"}:
        return "same_event_new_info"
    if primary_relation == "same_topic":
        return "same_topic_only"
    if primary_relation == "unrelated":
        return "different"
    return "uncertain"


def cluster_attach_eligible(primary_relation: str | None, source_cluster_eligible: bool) -> bool:
    return primary_relation in {"source_material", "repeat", "new_info", "analysis", "experience", "context"} and (
        source_cluster_eligible or primary_relation == "source_material"
    )


def build_llm_evidence(store: InboxStore, run_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    with store.connect() as conn:
        rows = [dict(row) for row in conn.execute("SELECT * FROM llm_call_logs ORDER BY id").fetchall()]
    calls = []
    errors = []
    skips = []
    for row in rows:
        request = parse_json_dict(row.get("request_json"))
        call = {
            "semantic_run_id": run_id,
            "call_id": str(row["id"]),
            "stage": row["task_type"],
            "model": row["model"],
            "prompt_variant": request.get("prompt_variant") or "full",
            "candidate_priority": request.get("candidate_priority") or ",".join(request.get("candidate_priorities") or []),
            "retry_attempt": request.get("retry_attempt", 0),
            "tokens_saved_estimate": request.get("tokens_saved_estimate", 0),
            "input_tokens": row.get("prompt_tokens") or 0,
            "output_tokens": row.get("completion_tokens") or 0,
            "latency_ms": row.get("latency_ms") or 0,
            "success": row.get("status") == "ok",
            "error_type": classify_error(row.get("error")) if row.get("status") == "failed" else None,
            "item_ids": request.get("item_ids") or split_ids(row.get("item_id")) or ([row.get("item_id")] if row.get("item_id") else []),
            "relation_id": None,
            "cluster_candidate_id": row.get("cluster_id"),
            "response_parse_success": row.get("status") == "ok",
        }
        calls.append(call)
        if row.get("status") == "failed":
            errors.append({**call, "error_message": snippet(row.get("error"), 1000), "raw_response_snippet": snippet(row.get("raw_output"))})
        if row.get("status") == "skipped":
            reason = row.get("error") or request.get("reason") or "skipped"
            skips.append({
                "semantic_run_id": run_id,
                "stage": row["task_type"],
                "skip_type": "token_budget" if "budget" in reason else "call_budget" if "max calls" in reason else "candidate_limit" if "candidate" in reason else "other",
                "skip_reason": reason,
                "would_have_been_stage": row["task_type"],
                "candidate_priority": request.get("candidate_priority") or ",".join(request.get("candidate_priorities") or []),
                "candidate_score": max(request.get("candidate_scores") or [0]) if isinstance(request.get("candidate_scores"), list) else request.get("candidate_score"),
                "is_high_priority_skip": any(priority in {"must_run", "high"} for priority in (request.get("candidate_priorities") or [request.get("candidate_priority")])),
                "item_id": row.get("item_id"),
                "relation_id": None,
                "cluster_candidate_id": row.get("cluster_id"),
                "reason": reason,
                "remaining_budget": {},
                "created_at": row.get("created_at"),
            })
    return calls, errors, skips


def flatten_hotspot_items(hotspots: list[dict[str, Any]], items: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for hotspot in hotspots:
        for item_id in hotspot["item_ids"]:
            item = items.get(item_id, {})
            rows.append({
                "semantic_run_id": hotspot["semantic_run_id"],
                "hotspot_group_id": hotspot["hotspot_group_id"],
                "hotspot_key": hotspot["hotspot_key"],
                "item_id": item_id,
                "original_item_id": original_item_id(item) if item else item_id,
                "source_id": item.get("source_id"),
                "source_name": item.get("source_name"),
                "title": item.get("title"),
                "published_at": item.get("published_at"),
                "url": item.get("url"),
            })
    return rows


def enrich_hotspots(hotspots: list[dict[str, Any]], relations: list[dict[str, Any]], candidates: list[dict[str, Any]], clusters: list[dict[str, Any]]) -> None:
    by_id = {hotspot["hotspot_group_id"]: hotspot for hotspot in hotspots}
    for rel in relations:
        gid = rel.get("hotspot_group_id")
        if gid in by_id:
            by_id[gid]["candidate_pair_count"] += 1
            by_id[gid]["relation_call_count"] += 1
            if rel.get("relation_label") != "different":
                by_id[gid]["non_different_relation_count"] += 1
    for candidate in candidates:
        gid = candidate.get("hotspot_group_id")
        if gid in by_id:
            by_id[gid]["cluster_candidate_created"] = True
    multi_items = {item_id for cluster in clusters if cluster.get("member_count", 0) > 1 for item_id in cluster.get("member_item_ids", [])}
    for hotspot in hotspots:
        hotspot["final_multi_item_cluster"] = any(item_id in multi_items for item_id in hotspot["item_ids"])
        if not hotspot["final_multi_item_cluster"]:
            hotspot["failure_reason"] = "no final multi-item cluster among hotspot members"


def cost_quality_metrics(
    summary: dict[str, Any],
    relations: list[dict[str, Any]],
    candidate_generation: list[dict[str, Any]],
    candidate_suppression: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
) -> dict[str, Any]:
    actual_tokens = int((summary.get("metadata") or {}).get("actual_tokens") or 0)
    actual_calls = int((summary.get("metadata") or {}).get("actual_calls") or 0)
    unique_pairs = {row.get("relation_pair_key") for row in relations if row.get("relation_pair_key")}
    non_different = [row for row in relations if row.get("relation_label") != "different"]
    eligible = [row for row in relations if row.get("cluster_eligible")]
    multi_clusters = [row for row in clusters if int(row.get("member_count") or 0) > 1]
    priority_counts = Counter(row.get("candidate_priority") or "unknown" for row in candidate_generation)
    suppression_counts = Counter(row.get("skip_reason") or row.get("candidate_suppression_reason") or "suppressed" for row in candidate_suppression)
    return {
        "actual_calls": actual_calls,
        "actual_tokens": actual_tokens,
        "tokens_by_stage": summary.get("token_cost"),
        "budget_skips": (summary.get("stage_budgets") or {}).get("stages"),
        "raw_relation_count": len(relations),
        "unique_relation_pair_count": len(unique_pairs),
        "duplicate_direction_suppressed_count": sum(1 for row in relations if row.get("is_duplicate_direction")),
        "non_different_count": len(non_different),
        "cluster_eligible_count": len(eligible),
        "multi_item_cluster_count": len(multi_clusters),
        "candidate_priority_distribution": dict(priority_counts),
        "candidate_suppression_count": len(candidate_suppression),
        "candidate_suppression_distribution": dict(suppression_counts),
        "non_different_per_100k_tokens": round(len(non_different) * 100000 / max(actual_tokens, 1), 3),
        "cluster_eligible_per_100k_tokens": round(len(eligible) * 100000 / max(actual_tokens, 1), 3),
        "multi_item_cluster_per_100k_tokens": round(len(multi_clusters) * 100000 / max(actual_tokens, 1), 3),
    }


def phase_comparison(run_dir: Path, current: dict[str, Any]) -> dict[str, Any]:
    baseline_path = run_dir.parent / "api_xgo_ing_phase1_2d_full_300_c5_20260517_140244" / "stage_metrics.json"
    baseline = {}
    if baseline_path.exists():
        try:
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        except Exception:
            baseline = {}
    return {
        "baseline_phase": "phase1_2d",
        "current_phase": "phase1_2e",
        "baseline_available": bool(baseline),
        "baseline_path": str(baseline_path),
        "current": current,
        "baseline_stage_metrics": baseline,
    }


def build_review_bundle(
    *,
    export_dir: Path,
    run_dir: Path,
    final_summary_md: Path,
    final_summary_json: Path,
    manifest: dict[str, Any],
    summary: dict[str, Any],
    ingest_summary: dict[str, Any] | None = None,
) -> dict[str, str]:
    export_dir.mkdir(parents=True, exist_ok=True)
    evidence_files = [Path(path) for path in manifest.get("evidence_files", []) if Path(path).exists()]
    phase = str(manifest.get("phase") or "phase1_2d")
    zip_path = export_dir / f"{phase}_review_evidence.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in evidence_files + [final_summary_md, final_summary_json, run_dir / "semantic_quality_report.md", run_dir / "semantic_quality_summary.json"]:
            if path.exists():
                zf.write(path, arcname=path.name)
    bundle = build_bundle_json(run_dir, manifest, summary, ingest_summary, evidence_files)
    bundle_json = export_dir / f"{phase}_review_bundle.json"
    write_json(bundle_json, bundle)
    bundle_md = export_dir / f"{phase}_review_bundle.md"
    bundle_md.write_text(build_bundle_markdown(bundle, zip_path), encoding="utf-8")
    return {"bundle_md": str(bundle_md), "bundle_json": str(bundle_json), "bundle_zip": str(zip_path)}


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
            if limit and len(rows) >= limit:
                break
    return rows


def build_bundle_json(run_dir: Path, manifest: dict[str, Any], summary: dict[str, Any], ingest_summary: dict[str, Any] | None, evidence_files: list[Path]) -> dict[str, Any]:
    relations = read_jsonl(run_dir / "relations_interesting.jsonl")
    suppressed = read_jsonl(run_dir / "candidate_suppression.jsonl", limit=500)
    cost = parse_path_json(run_dir / "cost_quality_metrics.json")
    comparison = parse_path_json(run_dir / "phase1_2d_vs_1_2e_comparison.json")
    relation_groups = defaultdict(list)
    for row in relations:
        relation_groups[row["relation_label"]].append(row)
    return {
        "export_metadata": {
            "phase": manifest.get("phase"),
            "repo_path": manifest.get("repo_path"),
            "git_commit": manifest.get("git_commit"),
            "export_time": datetime.now(timezone.utc).isoformat(),
            "db_path": manifest.get("db_path"),
            "backup_path": manifest.get("backup_path"),
            "semantic_run_output_dir": str(run_dir),
            "evidence_dir": str(run_dir),
            "concurrency": manifest.get("concurrency"),
            "scope": manifest.get("scope"),
            "write_real_db": manifest.get("semantic_write_real_db"),
            "read_only_export": True,
        },
        "ingest": {"summary": ingest_summary or {}, "sources": [], "items_added": [], "partial_write_suspects": []},
        "semantic": {
            "manifest": manifest,
            "summary": summary,
            "items": read_jsonl(run_dir / "semantic_items.jsonl", limit=500),
            "item_cards": {
                "summary": summary.get("item_cards"),
                "fallbacks": [row for row in read_jsonl(run_dir / "item_cards.jsonl") if row.get("fallback")],
                "failures": read_jsonl(run_dir / "item_card_failures.jsonl"),
            },
            "relations": {
                "summary": summary.get("item_relations"),
                "near_duplicate": relation_groups.get("near_duplicate", []),
                "related_with_new_info": relation_groups.get("related_with_new_info", []),
                "uncertain": relation_groups.get("uncertain", []),
                "suppressed_examples": suppressed[:100],
                "suspicious_different_sample": relation_groups.get("suspicious_different", []),
            },
            "clusters": {
                "summary": summary.get("item_clusters"),
                "candidates": read_jsonl(run_dir / "cluster_candidates.jsonl", limit=500),
                "attachments": read_jsonl(run_dir / "cluster_attachments.jsonl", limit=500),
                "final_clusters": read_jsonl(run_dir / "clusters_final.jsonl", limit=500),
            },
            "event_hotspots": read_jsonl(run_dir / "event_hotspots.jsonl", limit=200),
            "budget_skips": read_jsonl(run_dir / "budget_skips.jsonl", limit=500),
            "llm_errors": read_jsonl(run_dir / "llm_errors.jsonl", limit=200),
            "candidate_generation": read_jsonl(run_dir / "candidate_generation.jsonl", limit=500),
            "candidate_suppression": suppressed,
            "cost_quality_metrics": cost,
            "phase_comparison": comparison,
        },
        "evidence_files": [str(path) for path in evidence_files],
    }


def parse_path_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def build_bundle_markdown(bundle: dict[str, Any], zip_path: Path) -> str:
    semantic = bundle["semantic"]
    meta = bundle["export_metadata"]
    lines = [
        f"# {meta.get('phase') or 'Phase 1.2e'} Review Bundle",
        "",
        "## 1. Export metadata",
        "",
        f"- repo path: {meta.get('repo_path')}",
        f"- git commit: {meta.get('git_commit')}",
        f"- export time: {meta.get('export_time')}",
        f"- DB path: {meta.get('db_path')}",
        f"- backup path: {meta.get('backup_path')}",
        f"- semantic run output dir: {meta.get('semantic_run_output_dir')}",
        f"- evidence dir: {meta.get('evidence_dir')}",
        f"- concurrency: {meta.get('concurrency')}",
        f"- scope: {meta.get('scope')}",
        f"- write_real_db: {meta.get('write_real_db')}",
        f"- read-only export: {meta.get('read_only_export')}",
        "",
        "## 2. Files included",
        "",
        f"- evidence zip: {zip_path}",
    ]
    lines.extend(f"- {path}" for path in bundle.get("evidence_files", []))
    lines.extend([
        "",
        "## 3. Ingest summary",
        "",
        json.dumps(bundle.get("ingest", {}).get("summary", {}), ensure_ascii=False, indent=2, sort_keys=True),
        "",
        "## 4. Semantic coverage",
        "",
        json.dumps({
            "metadata": semantic.get("summary", {}).get("metadata"),
            "item_cards": semantic.get("summary", {}).get("item_cards"),
            "relations": semantic.get("summary", {}).get("item_relations", {}).get("relations_by_primary_relation"),
            "clusters": semantic.get("summary", {}).get("item_clusters"),
            "stage_budgets": semantic.get("summary", {}).get("stage_budgets"),
        }, ensure_ascii=False, indent=2, sort_keys=True)[:10000],
        "",
        "## 5. Item-card fallback/failure cases",
        "",
    ])
    failures = semantic["item_cards"]["failures"]
    if failures:
        for row in failures:
            lines.append(f"- FAILURE {row.get('item_id')} | {row.get('source_id')} | {row.get('title')} | {row.get('error_type')}: {row.get('error_message')}")
    else:
        lines.append("- No item-card failures recorded.")
    fallbacks = semantic["item_cards"]["fallbacks"]
    lines.append("")
    lines.append(f"Fallback count in bundle: {len(fallbacks)}. First 50:")
    for row in fallbacks[:50]:
        lines.append(f"- {row.get('item_id')} | {row.get('source_id')} | {row.get('title')} | {row.get('fallback_reason')}")
    lines.extend(["", "## 6. Relation evidence", ""])
    for label in ["near_duplicate", "related_with_new_info", "uncertain", "suspicious_different_sample"]:
        rows = semantic["relations"].get(label, [])
        lines.extend([f"### {label}", "", f"count: {len(rows)}"])
        for row in rows:
            lines.append(
                f"- A: {row.get('item_a_title')} ({row.get('item_a_source_name')}, {row.get('item_a_published_at')})\n"
                f"  B: {row.get('item_b_title')} ({row.get('item_b_source_name')}, {row.get('item_b_published_at')})\n"
                f"  confidence={row.get('confidence')} should_fold={row.get('should_fold')} reason={row.get('reason')}"
            )
        lines.append("")
    lines.extend([
        "## 7. Cluster diagnostics",
        "",
        json.dumps(semantic.get("clusters", {}).get("summary"), ensure_ascii=False, indent=2, sort_keys=True)[:10000],
        "",
        "## 8. Event hotspots",
        "",
    ])
    for hotspot in semantic.get("event_hotspots", [])[:50]:
        lines.append(f"- {hotspot.get('hotspot_group_id')} `{hotspot.get('hotspot_key')}` size={hotspot.get('group_size')} non_different={hotspot.get('non_different_relation_count')} multi_cluster={hotspot.get('final_multi_item_cluster')} reason={hotspot.get('failure_reason')}")
    lines.extend([
        "",
        "## 9. Source-profile review",
        "",
        json.dumps(semantic.get("summary", {}).get("source_profiles"), ensure_ascii=False, indent=2, sort_keys=True)[:10000],
        "",
        "## 10. Readiness recommendation",
        "",
        json.dumps(semantic.get("summary", {}).get("readiness_assessment"), ensure_ascii=False, indent=2, sort_keys=True),
        "",
        "## 11. Known gaps",
        "",
        "- Cluster candidate alternatives are reconstructed from persisted decisions/logs; the pre-LLM candidate list is only partially available unless future runs persist it at candidate-generation time.",
        "- Ingest source-level diagnostic CSVs are omitted when this phase runs without fresh ingest.",
    ])
    return "\n".join(lines) + "\n"


def copy_report_for_bundle(source: Path, target: Path) -> None:
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
