"""Sources routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
import sqlite3
from typing import Optional

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository
from app.repositories.observed_sources import list_observed_sources, list_observed_source_items

router = APIRouter()


@router.get("/sources", response_class=HTMLResponse)
def list_sources(
    request: Request,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: str = "source_name",
    page: int = 1,
    page_size: int = 50,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    filters = {
        "status": status,
        "keyword": keyword,
        "sort_by": sort_by,
        "page": max(1, page),
        "page_size": min(max(1, page_size), 200),
    }

    if not db_available:
        return templates.TemplateResponse("sources/list.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "sources", "sources": [], "total_sources": 0,
            "observed_sources": [], "total_observed": 0,
            "show_registered": False, "show_observed": False, "filters": filters,
        })

    registered, reg_total = repo.list_sources(
        conn, status=status, keyword=keyword, sort_by=sort_by,
        limit=filters["page_size"], offset=(filters["page"] - 1) * filters["page_size"],
    )

    show_observed = False
    observed: list[dict] = []
    obs_total = 0
    if reg_total == 0:
        show_observed = True
        observed, obs_total = list_observed_sources(
            conn, keyword=keyword,
            limit=filters["page_size"], offset=(filters["page"] - 1) * filters["page_size"],
        )

    return templates.TemplateResponse("sources/list.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "sources",
        "sources": registered, "total_sources": reg_total,
        "observed_sources": observed, "total_observed": obs_total,
        "show_registered": reg_total > 0,
        "show_observed": show_observed,
        "filters": filters,
    })


@router.get("/sources/rows", response_class=HTMLResponse)
def list_sources_rows(
    request: Request,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: str = "source_name",
    page: int = 1,
    page_size: int = 50,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)

    page = max(1, page)
    page_size = min(max(1, page_size), 200)

    if not db_available:
        return templates.TemplateResponse("sources/_rows.html", {
            "request": request, "sources": [],
        })

    sources, _ = repo.list_sources(
        conn, status=status, keyword=keyword, sort_by=sort_by,
        limit=page_size, offset=(page - 1) * page_size,
    )

    return templates.TemplateResponse("sources/_rows.html", {
        "request": request, "sources": sources,
    })


@router.get("/sources/{source_id}", response_class=HTMLResponse)
def source_detail(
    request: Request,
    source_id: str,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    if not db_available:
        return templates.TemplateResponse("sources/detail.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "sources", "src": None,
        })

    src = repo.get_source(conn, source_id)
    if not src:
        # Check if it's an observed source key
        obs_sources, obs_total = list_observed_sources(conn, keyword=None)
        observed_match = None
        for obs in obs_sources:
            if obs.get("observed_source_key") == source_id or obs.get("source_name") == source_id:
                observed_match = obs
                break

        if observed_match:
            obs_items, obs_item_total = list_observed_source_items(conn, observed_match["observed_source_key"], limit=50)
            return templates.TemplateResponse("sources/detail.html", {
                "request": request, "db_available": True, "db_path": str(settings.database_path),
                "active_page": "sources",
                "src": observed_match,
                "is_observed": True,
                "recent_items": obs_items,
                "status": "observed",
            })

        return templates.TemplateResponse("sources/detail.html", {
            "request": request, "db_available": True, "db_path": str(settings.database_path),
            "active_page": "sources", "src": None, "not_found": True, "source_id": source_id,
        }, status_code=404)

    recent_items = repo.list_items_by_source(conn, source_id, limit=20)

    return templates.TemplateResponse("sources/detail.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "sources", "src": src, "recent_items": recent_items,
        "is_observed": False,
        "status": src.get("status", ""),
    })
