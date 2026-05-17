from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import BASE_DIR
from app.semantic.evidence import write_json
from app.storage import InboxStore


CONFIRMATION_VALUE = "api.xgo.ing"


def create_db_backup(db_path: Path) -> Path:
    backup_dir = BASE_DIR / "data" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{db_path.stem}_semantic_phase1_3_{stamp}{db_path.suffix}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def validate_scoped_write_request(
    *,
    write_real_db: bool,
    dry_run: bool,
    source_url_prefix: str | None,
    confirmation: str | None,
) -> tuple[bool, str]:
    if not write_real_db:
        return True, "not a real write"
    if dry_run:
        return False, "write_real_db cannot be combined with dry_run"
    if not source_url_prefix or "api.xgo.ing" not in source_url_prefix:
        return False, "real semantic writes require source_url_prefix scoped to api.xgo.ing"
    if confirmation != CONFIRMATION_VALUE:
        return False, f"real semantic writes require --confirm-scoped-semantic-write {CONFIRMATION_VALUE}"
    return True, "scoped semantic write confirmed"


def write_rehearsal_report(
    *,
    run_dir: Path,
    db_path: Path,
    backup_path: Path,
    summary: dict[str, Any],
    command: str,
) -> dict[str, str]:
    report_path = run_dir / "real_write_rehearsal_report.md"
    diff_path = run_dir / "real_write_rehearsal_diff.json"
    sql_path = run_dir / "real_write_rehearsal_verification.sql.txt"
    rollback_path = run_dir / "real_write_rehearsal_rollback_instructions.md"
    counts = semantic_row_counts(InboxStore(db_path))
    write_json(diff_path, {"semantic_row_counts_after_write": counts, "summary": summary})
    sql_path.write_text(
        "\n".join(
            [
                "SELECT COUNT(*) FROM item_cards;",
                "SELECT COUNT(*) FROM item_relations;",
                "SELECT COUNT(*) FROM event_clusters;",
                "SELECT COUNT(*) FROM cluster_items;",
                "SELECT COUNT(*) FROM source_profiles;",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    rollback_path.write_text(
        f"To roll back this scoped semantic rehearsal, stop any running service and restore:\n\ncp {backup_path} {db_path}\n",
        encoding="utf-8",
    )
    report_path.write_text(
        "\n".join(
            [
                "# Phase 1.3 Real Write Rehearsal",
                "",
                f"- command: `{command}`",
                f"- db_path: `{db_path}`",
                f"- backup_path: `{backup_path}`",
                f"- semantic_row_counts_after_write: `{counts}`",
                "",
                "Rollback instructions are in `real_write_rehearsal_rollback_instructions.md`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "report": str(report_path),
        "diff": str(diff_path),
        "verification_sql": str(sql_path),
        "rollback": str(rollback_path),
    }


def semantic_row_counts(store: InboxStore) -> dict[str, int]:
    tables = ["item_cards", "item_relations", "event_clusters", "cluster_items", "source_profiles", "llm_call_logs"]
    out: dict[str, int] = {}
    with store.connect() as conn:
        for table in tables:
            try:
                row = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()
                out[table] = int(row["n"] or 0)
            except Exception:
                out[table] = 0
    return out

