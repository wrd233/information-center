"""Scan outputs/runs/ directory for file-based run reports.

Used as fallback when rss_ingest_runs table is empty but run artifacts exist on disk.
"""

import logging
import os
import re
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

RUN_DIR_PATTERNS = [
    re.compile(r"^rss_run_"),
    re.compile(r"ingest"),
    re.compile(r"live_"),
]


def _is_run_directory(dirname: str) -> bool:
    for pat in RUN_DIR_PATTERNS:
        if pat.search(dirname):
            return True
    return False


def _resolve_safe_path(base: Path, requested: str) -> Optional[Path]:
    """Resolve a path within base, rejecting path traversal."""
    try:
        resolved = (base / requested).resolve()
        base_resolved = base.resolve()
        if str(resolved).startswith(str(base_resolved)):
            return resolved
    except (ValueError, OSError):
        pass
    return None


def _parse_report_metrics(report_path: Path) -> dict[str, Any]:
    """Extract key metrics from a final_report.md or report.md file."""
    metrics: dict[str, Any] = {}
    if not report_path.exists():
        return metrics

    try:
        content = report_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return metrics

    # Store first 2000 chars as preview
    metrics["report_preview"] = content[:2000]

    # Try to extract common metric patterns
    patterns = {
        "opml_sources": r"(?:OPML sources|Source count|Total sources)[:\s]*(\d+)",
        "imported_to_registry": r"(?:Imported to registry|Imported)[:\s]*(\d+)",
        "first_pass_new": r"(?:First pass new|New items)[:\s]*(\d+)",
        "first_pass_duplicate": r"(?:First pass dup|Duplicate items)[:\s]*(\d+)",
        "success_count": r"(?:Success)[:\s]*(\d+)",
        "failure_count": r"(?:Fail|Failed)[:\s]*(\d+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            try:
                metrics[key] = int(match.group(1))
            except ValueError:
                metrics[key] = match.group(1)

    return metrics


def count_file_runs(outputs_path: Path) -> int:
    """Count run directories in the outputs path."""
    if not outputs_path.exists():
        return 0
    try:
        count = 0
        for child in outputs_path.iterdir():
            if child.is_dir() and _is_run_directory(child.name):
                count += 1
        return count
    except Exception:
        return 0


def list_file_runs(
    outputs_path: Path,
    *,
    limit: int = 30,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """List file-based runs from the outputs/runs directory."""
    if not outputs_path.exists():
        return [], 0

    run_dirs: list[dict] = []
    try:
        for child in outputs_path.iterdir():
            if not child.is_dir():
                continue
            if not _is_run_directory(child.name):
                continue

            entry: dict[str, Any] = {
                "run_dir_name": child.name,
                "run_path": str(child),
                "mtime": None,
                "final_report_path": None,
                "has_report_md": False,
                "has_final_report": False,
                "metrics": {},
                "files": [],
            }

            try:
                entry["mtime"] = os.path.getmtime(str(child))
            except OSError:
                pass

            # Check for report files
            final_report = child / "final_report.md"
            report_md = child / "report.md"

            if final_report.exists():
                entry["final_report_path"] = str(final_report)
                entry["has_final_report"] = True
                entry["metrics"] = _parse_report_metrics(final_report)
            elif report_md.exists():
                entry["final_report_path"] = str(report_md)
                entry["has_report_md"] = True
                entry["metrics"] = _parse_report_metrics(report_md)

            # List other files
            try:
                for f in child.iterdir():
                    if f.is_file():
                        entry["files"].append(f.name)
            except Exception:
                pass

            run_dirs.append(entry)
    except Exception:
        pass

    run_dirs.sort(key=lambda d: d.get("mtime") or 0, reverse=True)
    total = len(run_dirs)
    return run_dirs[offset : offset + limit], total


def get_file_run_detail(outputs_path: Path, run_dir_name: str) -> Optional[dict]:
    """Get details for a single file-based run."""
    run_dir = _resolve_safe_path(outputs_path, run_dir_name)
    if run_dir is None or not run_dir.exists() or not run_dir.is_dir():
        return None

    entry: dict[str, Any] = {
        "run_dir_name": run_dir.name,
        "run_path": str(run_dir),
        "mtime": None,
        "final_report_path": None,
        "has_final_report": False,
        "report_content": None,
    }

    try:
        entry["mtime"] = os.path.getmtime(str(run_dir))
    except OSError:
        pass

    final_report = run_dir / "final_report.md"
    report_md = run_dir / "report.md"

    report_to_read = None
    if final_report.exists():
        report_to_read = final_report
        entry["has_final_report"] = True
    elif report_md.exists():
        report_to_read = report_md
        entry["has_final_report"] = True

    if report_to_read:
        entry["final_report_path"] = str(report_to_read)
        try:
            entry["report_content"] = report_to_read.read_text(encoding="utf-8", errors="replace")
        except Exception:
            entry["report_content"] = "(could not read report)"

    return entry
