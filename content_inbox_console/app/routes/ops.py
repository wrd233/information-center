from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qs

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.backend_client import BackendClient, data


router = APIRouter()


def client(request: Request) -> BackendClient:
    return BackendClient(request.app.state.settings.api_base)


def render(request: Request, template: str, context: dict[str, Any]) -> HTMLResponse:
    context.setdefault("request", request)
    context.setdefault("api_base", request.app.state.settings.api_base)
    context.setdefault("db_available", True)
    context.setdefault("db_path", "")
    return request.app.state.templates.TemplateResponse(request, template, context)


def err(response: dict[str, Any]) -> str | None:
    if response.get("ok"):
        return None
    error = response.get("error") or {}
    return f"{error.get('code', 'ERROR')}: {error.get('message', 'Unknown backend error')}"


async def form_fields(request: Request) -> dict[str, str]:
    raw = (await request.body()).decode("utf-8", errors="replace")
    parsed = parse_qs(raw, keep_blank_values=True)
    return {key: values[-1] if values else "" for key, values in parsed.items()}


@router.get("/", response_class=HTMLResponse)
def root() -> RedirectResponse:
    return RedirectResponse("/dashboard", status_code=302)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    api = client(request)
    env_r = api.get("/api/environment")
    sources_r = api.get("/api/sources", {"limit": 8})
    runs_r = api.get("/api/runs", {"limit": 8})
    events_r = api.get("/api/events", {"limit": 6})
    reviews_r = api.get("/api/review-queue", {"limit": 6})
    return render(
        request,
        "ops/dashboard.html",
        {
            "active_page": "dashboard",
            "environment": data(env_r, {}).get("environment", {}),
            "legacy_database": data(env_r, {}).get("legacy_database", {}),
            "sources": data(sources_r, {}).get("sources", []),
            "source_stats": data(sources_r, {}).get("stats", {}),
            "runs": data(runs_r, {}).get("runs", []),
            "events": data(events_r, {}).get("events", []),
            "reviews": data(reviews_r, {}).get("reviews", []),
            "error": err(env_r) or err(sources_r) or err(runs_r),
        },
    )


@router.get("/environment", response_class=HTMLResponse)
def environment(request: Request):
    api = client(request)
    env_r = api.get("/api/environment")
    health_r = api.get("/api/environment/health")
    return render(request, "ops/environment.html", {"active_page": "environment", "environment": data(env_r, {}).get("environment", {}), "legacy_database": data(env_r, {}).get("legacy_database", {}), "checks": data(health_r, {}).get("checks", []), "error": err(env_r) or err(health_r)})


@router.post("/environment/init-fresh", response_class=HTMLResponse)
async def environment_init(request: Request):
    form = await form_fields(request)
    database_label = str(form.get("database_label") or "")
    payload = {"database_label": database_label} if database_label else {}
    client(request).post("/api/environment/init-fresh", payload)
    return RedirectResponse("/environment", status_code=303)


@router.get("/sources", response_class=HTMLResponse)
def sources(request: Request, status: str | None = None, keyword: str | None = None):
    api = client(request)
    response = api.get("/api/sources", {"status": status, "keyword": keyword, "limit": 200})
    return render(request, "ops/sources.html", {"active_page": "sources", "sources": data(response, {}).get("sources", []), "stats": data(response, {}).get("stats", {}), "status": status or "", "keyword": keyword or "", "error": err(response)})


@router.post("/sources/import/preview", response_class=HTMLResponse)
async def sources_import_preview(request: Request):
    form = await form_fields(request)
    format = str(form.get("format") or "urls")
    content = str(form.get("content") or "")
    response = client(request).post("/api/sources/import/preview", {"format": format, "content": content})
    return render(request, "ops/sources.html", {"active_page": "sources", "sources": [], "stats": {}, "import_preview": data(response, {}), "error": err(response), "status": "", "keyword": ""})


@router.post("/sources/import/commit", response_class=HTMLResponse)
async def sources_import_commit(request: Request):
    form = await form_fields(request)
    operation_id = str(form.get("operation_id") or "")
    client(request).post("/api/sources/import/commit", {"operation_id": operation_id})
    return RedirectResponse("/sources", status_code=303)


@router.post("/sources/bulk", response_class=HTMLResponse)
async def sources_bulk(request: Request):
    form = await form_fields(request)
    action = str(form.get("action") or "disable")
    source_ids = str(form.get("source_ids") or "")
    ids = [part.strip() for part in source_ids.split(",") if part.strip()]
    path = {
        "enable": "/api/sources/bulk-enable",
        "disable": "/api/sources/bulk-disable",
        "archive": "/api/sources/bulk-archive",
        "delete": "/api/sources/bulk-delete",
    }.get(action, "/api/sources/bulk-disable")
    client(request).post(path, {"source_ids": ids})
    return RedirectResponse("/sources", status_code=303)


@router.get("/sources/{source_id}", response_class=HTMLResponse)
def source_detail(request: Request, source_id: str):
    response = client(request).get(f"/api/sources/{source_id}")
    return render(request, "ops/source_detail.html", {"active_page": "sources", "source_id": source_id, "data": data(response, {}), "error": err(response)})


@router.get("/runs", response_class=HTMLResponse)
def runs(request: Request):
    response = client(request).get("/api/runs", {"limit": 100})
    return render(request, "ops/runs.html", {"active_page": "runs", "runs": data(response, {}).get("runs", []), "error": err(response)})


@router.get("/runs/new", response_class=HTMLResponse)
def run_wizard(request: Request):
    api = client(request)
    env = data(api.get("/api/environment"), {}).get("environment", {})
    sources = data(api.get("/api/sources", {"status": "active", "limit": 500}), {}).get("sources", [])
    return render(request, "ops/run_wizard.html", {"active_page": "runs", "environment": env, "sources": sources})


def run_form_payload(source_ids: str, mode: str, published_from: str, published_to: str, max_items_per_source: int, max_total_items: int) -> dict[str, Any]:
    ids = [part.strip() for part in source_ids.split(",") if part.strip()]
    return {
        "mode": mode,
        "source_scope": {"type": "selected", "source_ids": ids},
        "time_filter": {"published_from": published_from or None, "published_to": published_to or None, "timezone": "Asia/Shanghai"},
        "limits": {"max_sources": len(ids) or 100, "max_items_per_source": max_items_per_source, "max_total_items": max_total_items},
        "options": {"force_refetch": False, "stop_on_first_existing": False},
    }


@router.post("/runs/preview", response_class=HTMLResponse)
async def run_preview(request: Request):
    form = await form_fields(request)
    source_ids = str(form.get("source_ids") or "")
    mode = str(form.get("mode") or "dry_run")
    published_from = str(form.get("published_from") or "")
    published_to = str(form.get("published_to") or "")
    max_items_per_source = int(form.get("max_items_per_source") or 20)
    max_total_items = int(form.get("max_total_items") or 200)
    payload = run_form_payload(source_ids, mode, published_from, published_to, max_items_per_source, max_total_items)
    response = client(request).post("/api/runs/preview", payload)
    return render(request, "ops/run_preview.html", {"active_page": "runs", "preview": data(response, {}), "payload": json.dumps(payload), "error": err(response)})


@router.post("/runs/start", response_class=HTMLResponse)
async def run_start(request: Request):
    form = await form_fields(request)
    payload_json = str(form.get("payload_json") or "{}")
    payload = json.loads(payload_json)
    response = client(request).post("/api/runs", payload)
    run_id = data(response, {}).get("run_id")
    if run_id:
        return RedirectResponse(f"/runs/{run_id}", status_code=303)
    return render(request, "ops/run_preview.html", {"active_page": "runs", "preview": {}, "payload": payload_json, "error": err(response)})


@router.get("/runs/{run_id}", response_class=HTMLResponse)
def run_detail(request: Request, run_id: str):
    api = client(request)
    summary = api.get(f"/api/runs/{run_id}/summary")
    events = api.get(f"/api/runs/{run_id}/events")
    items = api.get(f"/api/runs/{run_id}/items")
    return render(request, "ops/run_detail.html", {"active_page": "runs", "run_id": run_id, "summary": data(summary, {}), "events": data(events, {}).get("events", []), "items": data(items, {}).get("items", []), "error": err(summary)})


@router.post("/runs/{run_id}/cancel")
def run_cancel(request: Request, run_id: str):
    client(request).post(f"/api/runs/{run_id}/cancel", {})
    return RedirectResponse(f"/runs/{run_id}", status_code=303)


@router.get("/information", response_class=HTMLResponse)
@router.get("/items", response_class=HTMLResponse)
def items(request: Request, run_id: str | None = None, keyword: str | None = None):
    response = client(request).get("/api/items", {"run_id": run_id, "keyword": keyword, "limit": 100})
    return render(request, "ops/items.html", {"active_page": "items", "items": data(response, {}).get("items", []), "run_id": run_id or "", "keyword": keyword or "", "error": err(response)})


@router.get("/items/{item_id}", response_class=HTMLResponse)
def item_detail(request: Request, item_id: str):
    response = client(request).get(f"/api/items/{item_id}")
    return render(request, "ops/item_detail.html", {"active_page": "items", "item_id": item_id, "data": data(response, {}), "error": err(response)})


@router.get("/dedupe-groups", response_class=HTMLResponse)
def dedupe_groups(request: Request):
    response = client(request).get("/api/dedupe-groups")
    return render(request, "ops/simple_list.html", {"active_page": "dedupe", "title": "Dedupe Groups", "items": data(response, {}).get("dedupe_groups", []), "error": err(response)})


def simple_page(request: Request, active: str, title: str, api_path: str, key: str):
    response = client(request).get(api_path)
    return render(request, "ops/simple_list.html", {"active_page": active, "title": title, "items": data(response, {}).get(key, []), "error": err(response)})


@router.get("/clusters", response_class=HTMLResponse)
def clusters(request: Request):
    return simple_page(request, "clusters", "Clusters", "/api/clusters", "clusters")


@router.get("/clusters/{cluster_id}", response_class=HTMLResponse)
def cluster_detail(request: Request, cluster_id: str):
    response = client(request).get(f"/api/clusters/{cluster_id}")
    return render(request, "ops/object_detail.html", {"active_page": "clusters", "title": "Cluster Detail", "data": data(response, {}), "error": err(response)})


@router.get("/events", response_class=HTMLResponse)
def events(request: Request):
    return simple_page(request, "events", "Events", "/api/events", "events")


@router.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail(request: Request, event_id: str):
    response = client(request).get(f"/api/events/{event_id}")
    return render(request, "ops/object_detail.html", {"active_page": "events", "title": "Event Detail", "data": data(response, {}), "error": err(response)})


@router.get("/entities", response_class=HTMLResponse)
def entities(request: Request):
    return simple_page(request, "entities", "Entities", "/api/entities", "entities")


@router.get("/relations", response_class=HTMLResponse)
def relations(request: Request):
    return simple_page(request, "relations", "Relations", "/api/relations", "relations")


@router.get("/claims", response_class=HTMLResponse)
def claims(request: Request):
    return simple_page(request, "claims", "Claims", "/api/claims", "claims")


@router.get("/topics", response_class=HTMLResponse)
def topics(request: Request):
    return simple_page(request, "topics", "Topics", "/api/topics", "topics")


@router.get("/timeline", response_class=HTMLResponse)
def timeline(request: Request):
    return simple_page(request, "timeline", "Timeline", "/api/timeline", "timeline")


@router.get("/review-queue", response_class=HTMLResponse)
def review_queue(request: Request):
    return simple_page(request, "review", "Review Queue", "/api/review-queue", "reviews")


@router.post("/review-queue/{review_id}/resolve")
def review_resolve(request: Request, review_id: int):
    client(request).post(f"/api/review-queue/{review_id}/resolve", {"status": "resolved"})
    return RedirectResponse("/review-queue", status_code=303)


@router.get("/briefings", response_class=HTMLResponse)
def briefings(request: Request):
    response = client(request).get("/api/briefings/daily")
    return render(request, "ops/briefings.html", {"active_page": "briefings", "briefings": data(response, {}).get("briefings", []), "error": err(response)})


@router.post("/briefings/daily/generate")
def briefing_generate(request: Request):
    client(request).post("/api/briefings/daily/generate", {})
    return RedirectResponse("/briefings", status_code=303)


@router.get("/reports", response_class=HTMLResponse)
def reports(request: Request):
    response = client(request).get("/api/reports")
    return render(request, "ops/reports.html", {"active_page": "reports", "reports": data(response, {}).get("reports", []), "error": err(response)})


@router.post("/reports/generate")
async def report_generate(request: Request):
    form = await form_fields(request)
    report_type = str(form.get("report_type") or "summary")
    client(request).post("/api/reports/generate", {"report_type": report_type})
    return RedirectResponse("/reports", status_code=303)


@router.get("/agent-query", response_class=HTMLResponse)
def agent_query(request: Request, query: str = ""):
    result = {}
    error = None
    if query:
        response = client(request).post("/api/agent-query/preview", {"query": query, "format": "compact"})
        result = data(response, {})
        error = err(response)
    return render(request, "ops/agent_query.html", {"active_page": "agent", "query": query, "result": result, "error": error})


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return render(request, "ops/settings.html", {"active_page": "settings"})
