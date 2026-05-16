"""Items / Inbox routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
import sqlite3
from typing import Optional

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
def list_items(
    request: Request,
    source_id: Optional[str] = None,
    source_name: Optional[str] = None,
    source_category: Optional[str] = None,
    content_type: Optional[str] = None,
    keyword: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_score: Optional[str] = None,
    page: int = 1,
    page_size: int = 50,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    filters = {
        "source_id": source_id,
        "source_name": source_name,
        "source_category": source_category,
        "content_type": content_type,
        "keyword": keyword,
        "date_from": date_from,
        "date_to": date_to,
        "min_score": min_score,
        "page": max(1, page),
        "page_size": min(max(1, page_size), 200),
    }

    if not db_available:
        return templates.TemplateResponse("items/list.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "items", "items": [], "total_items": 0, "filters": filters,
        })

    min_score_val = float(min_score) if min_score else None
    items, total = repo.list_items(
        conn,
        source_id=source_id,
        source_name=source_name,
        source_category=source_category,
        content_type=content_type,
        keyword=keyword,
        date_from=date_from,
        date_to=date_to,
        min_score=min_score_val,
        limit=filters["page_size"],
        offset=(filters["page"] - 1) * filters["page_size"],
    )

    return templates.TemplateResponse("items/list.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "items", "items": items, "total_items": total, "filters": filters,
    })


@router.get("/items/rows", response_class=HTMLResponse)
def list_items_rows(
    request: Request,
    source_id: Optional[str] = None,
    source_name: Optional[str] = None,
    source_category: Optional[str] = None,
    content_type: Optional[str] = None,
    keyword: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_score: Optional[str] = None,
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
        return templates.TemplateResponse("items/_rows.html", {
            "request": request, "items": [],
        })

    min_score_val = float(min_score) if min_score else None
    items, _ = repo.list_items(
        conn,
        source_id=source_id, source_name=source_name,
        source_category=source_category, content_type=content_type,
        keyword=keyword, date_from=date_from, date_to=date_to,
        min_score=min_score_val,
        limit=page_size, offset=(page - 1) * page_size,
    )

    return templates.TemplateResponse("items/_rows.html", {
        "request": request, "items": items,
    })


@router.get("/items/{item_id}", response_class=HTMLResponse)
def item_detail(
    request: Request,
    item_id: str,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    if not db_available:
        return templates.TemplateResponse("items/detail.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "items", "item": None,
        })

    item = repo.get_item(conn, item_id)
    if not item:
        return templates.TemplateResponse("items/detail.html", {
            "request": request, "db_available": True, "db_path": str(settings.database_path),
            "active_page": "items", "item": None, "not_found": True, "item_id": item_id,
        }, status_code=404)

    return templates.TemplateResponse("items/detail.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "items", "item": item,
    })
