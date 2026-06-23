from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_DIR / "config.yaml"


@dataclass(frozen=True)
class AppConfig:
    root_dir: Path
    config_path: Path
    raw: dict[str, Any]
    database_path: Path

    @property
    def server(self) -> dict[str, Any]:
        return self.raw.get("server", {})

    @property
    def adapters(self) -> dict[str, dict[str, Any]]:
        return self.raw.get("adapters", {})

    @property
    def export_profiles(self) -> dict[str, dict[str, Any]]:
        return self.raw.get("export_profiles", {})

    @property
    def categories(self) -> list[str]:
        return list(self.raw.get("categories", []))

    @property
    def health_threshold(self) -> int:
        return int(self.raw.get("health", {}).get("consecutive_failure_threshold", 3))

    @property
    def fetch_scan_limit(self) -> int:
        return int(self.raw.get("fetch", {}).get("scan_limit", 50))

    @property
    def stop_after_existing_streak(self) -> int:
        return int(self.raw.get("fetch", {}).get("stop_after_existing_streak", 10))

    @property
    def summary_excerpt_max_chars(self) -> int:
        return int(self.raw.get("fetch", {}).get("summary_excerpt_max_chars", 500))

    @property
    def default_max_concurrent_sources(self) -> int:
        return int(
            self.raw.get("concurrency", {}).get(
                "default_max_concurrent_sources",
                self.raw.get("batch_fetch", {}).get("default_max_concurrent_sources", 7),
            )
        )

    @property
    def hard_concurrency_limit(self) -> int:
        return int(
            self.raw.get("concurrency", {}).get("hard_limit", self.raw.get("batch_fetch", {}).get("hard_limit", 10))
        )

    def adapter_max_concurrent_sources(self, source_type: str) -> int:
        configured = self.raw.get("concurrency", {}).get("adapters", {}).get(source_type)
        if configured is not None:
            return int(configured)
        for adapter in self.adapters.values():
            if adapter.get("type") == source_type and adapter.get("max_concurrent_sources") is not None:
                return int(adapter["max_concurrent_sources"])
        return self.default_max_concurrent_sources

    def timeout_config(self, source_type: str | None = None) -> dict[str, float]:
        defaults = {"connect_seconds": 3.0, "read_seconds": 8.0, "total_seconds": 12.0}
        configured = self.raw.get("timeouts", {})
        values = {**defaults, **(configured.get("default") or {})}
        if source_type and configured.get(source_type):
            values.update(configured[source_type])
        return {key: float(value) for key, value in values.items()}


def load_config(config_path: Path | None = None) -> AppConfig:
    path = config_path or CONFIG_PATH
    with path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}
    db_override = os.environ.get("SOURCE_MANAGER_DB_PATH")
    db_value = db_override or raw.get("database", {}).get("path", "data/source_manager.sqlite3")
    db_path = Path(db_value)
    if not db_path.is_absolute():
        db_path = ROOT_DIR / db_path
    return AppConfig(root_dir=ROOT_DIR, config_path=path, raw=raw, database_path=db_path.resolve())


settings = load_config()
