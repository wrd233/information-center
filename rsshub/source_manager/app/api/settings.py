from __future__ import annotations

from fastapi import APIRouter, Request


router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def get_settings(request: Request) -> dict:
    config = request.app.state.config
    return {
        "ok": True,
        "database_path": str(config.database_path),
        "config_path": str(config.config_path),
        "server": config.server,
        "adapters": config.adapters,
        "export_profiles": config.export_profiles,
        "categories": config.categories,
        "health": {"consecutive_failure_threshold": config.health_threshold},
        "fetch": {
            "scan_limit": config.fetch_scan_limit,
            "stop_after_existing_streak": config.stop_after_existing_streak,
            "summary_excerpt_max_chars": config.summary_excerpt_max_chars,
        },
        "batch_fetch": {
            "default_max_concurrent_sources": config.default_max_concurrent_sources,
            "hard_limit": config.hard_concurrency_limit,
        },
        "docs_url": "/docs",
    }

