"""Sources routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
import sqlite3
from typing import Optional

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository

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
            "active_page": "sources", "sources": [], "total_sources": 0, "filters": filters,
        })

    sources, total = repo.list_sources(
        conn, status=status, keyword=keyword, sort_by=sort_by,
        limit=filters["page_size"], offset=(filters["page"] - 1) * filters["page_size"],
    )

    return templates.TemplateResponse("sources/list.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "sources", "sources": sources, "total_sources": total, "filters": filters,
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
        return templates.TemplateResponse("sources/detail.html", {
            "request": request, "db_available": True, "db_path": str(settings.database_path),
            "active_page": "sources", "src": None, "not_found": True, "source_id": source_id,
        }, status_code=404)

    recent_items = repo.list_items_by_source(conn, source_id, limit=20)

    return templates.TemplateResponse("sources/detail.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "sources", "src": src, "recent_items": recent_items,
        "status": src.get("status", ""),
    })
