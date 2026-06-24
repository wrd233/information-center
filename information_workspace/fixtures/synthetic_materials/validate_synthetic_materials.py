from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import json
import sys


SOURCE_TYPES = {"rss", "web", "wechat", "upload", "document", "agent", "api", "unknown"}
REQUIRED_GROUPS = {
    "basic_news",
    "long_article",
    "opinion_piece",
    "technical_article",
    "noise",
    "uncertain",
    "exact_duplicate",
    "near_duplicate",
    "multi_source_same_event",
    "multi_day_event",
    "event_background",
    "conflicting_reports",
    "weakly_related_event",
    "topic_material",
    "topic_structure_refresh",
    "no_url_material",
    "missing_time_material",
    "agent_submitted_material",
    "upload_material",
    "export_evidence_pack",
}


def sha(text: str) -> str:
    return hashlib.sha256(" ".join(text.lower().split()).encode("utf-8")).hexdigest()


def load(path: Path) -> list[dict]:
    items = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
    return items


def validate(items: list[dict]) -> tuple[list[str], dict]:
    errors: list[str] = []
    if len(items) < 500:
        errors.append(f"expected >=500 items, got {len(items)}")
    group_counts = Counter()
    purpose_counts = Counter()
    content_counts = Counter()
    domain_counts = Counter()
    content_hash_counts = Counter()
    no_url = 0
    missing_time = 0
    lengths = []
    for index, item in enumerate(items, start=1):
        for key in ["title", "content_text", "source_name", "source_type", "metadata"]:
            if key not in item:
                errors.append(f"item {index}: missing {key}")
        if item.get("source_type") not in SOURCE_TYPES:
            errors.append(f"item {index}: invalid source_type {item.get('source_type')}")
        metadata = item.get("metadata") or {}
        if metadata.get("synthetic") is not True:
            errors.append(f"item {index}: metadata.synthetic must be true")
        group = metadata.get("fixture_group")
        if not group:
            errors.append(f"item {index}: missing fixture_group")
        purposes = metadata.get("test_purpose")
        if not isinstance(purposes, list) or not purposes:
            errors.append(f"item {index}: test_purpose must be a non-empty list")
            purposes = []
        if not metadata.get("expected_behavior"):
            errors.append(f"item {index}: missing expected_behavior")
        if metadata.get("generated_by") != "codex_goal_04":
            errors.append(f"item {index}: generated_by must be codex_goal_04")
        text = item.get("content_text") or ""
        if len(text) < 50:
            errors.append(f"item {index}: content_text too short")
        group_counts[group] += 1
        for purpose in purposes:
            purpose_counts[purpose] += 1
        content_counts[metadata.get("content_type", "unknown")] += 1
        domain_counts[metadata.get("domain_category", "unknown")] += 1
        content_hash_counts[sha(text)] += 1
        no_url += 0 if item.get("url") else 1
        missing_time += 0 if item.get("published_at") else 1
        lengths.append(len(text))
    missing_groups = REQUIRED_GROUPS - set(group_counts)
    if missing_groups:
        errors.append(f"missing required groups: {sorted(missing_groups)}")
    for group in REQUIRED_GROUPS:
        if group_counts[group] < 10:
            errors.append(f"group {group} has too few items: {group_counts[group]}")
    if no_url < 10:
        errors.append("expected at least 10 no-url materials")
    if missing_time < 10:
        errors.append("expected at least 10 missing-time materials")
    if content_hash_counts.most_common(1) and content_hash_counts.most_common(1)[0][1] > 8:
        errors.append("one duplicate hash appears too often")
    exact_duplicate_hashes = [count for count in content_hash_counts.values() if count > 1]
    if not exact_duplicate_hashes:
        errors.append("expected exact duplicate content hashes")
    primary = domain_counts["primary"]
    general = domain_counts["general"]
    if primary + general and primary / (primary + general) < 0.65:
        errors.append("primary domain ratio below 65 percent")
    report = {
        "total": len(items),
        "group_counts": dict(sorted(group_counts.items())),
        "purpose_counts": dict(sorted(purpose_counts.items())),
        "content_counts": dict(sorted(content_counts.items())),
        "domain_counts": dict(sorted(domain_counts.items())),
        "no_url": no_url,
        "missing_time": missing_time,
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "duplicate_hashes": sum(1 for count in content_hash_counts.values() if count > 1),
    }
    return errors, report


def write_report(path: Path, report: dict, errors: list[str]) -> None:
    lines = [
        "# Synthetic Corpus Validation",
        "",
        f"- Source: {path}",
        f"- Total: {report['total']}",
        f"- No URL: {report['no_url']}",
        f"- Missing time: {report['missing_time']}",
        f"- Length range: {report['min_length']} - {report['max_length']}",
        f"- Duplicate content hashes: {report['duplicate_hashes']}",
        f"- Result: {'FAILED' if errors else 'PASSED'}",
        "",
        "## Group Counts",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in report["group_counts"].items())
    lines.extend(["", "## Purpose Counts", ""])
    lines.extend(f"- {key}: {value}" for key, value in report["purpose_counts"].items())
    lines.extend(["", "## Content Counts", ""])
    lines.extend(f"- {key}: {value}" for key, value in report["content_counts"].items())
    lines.extend(["", "## Domain Counts", ""])
    lines.extend(f"- {key}: {value}" for key, value in report["domain_counts"].items())
    if errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in errors)
    out = path.parent / "REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "synthetic_materials_500.jsonl"
    items = load(path)
    errors, report = validate(items)
    write_report(path, report, errors)
    print(json.dumps({"ok": not errors, "errors": errors, "report": report}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
