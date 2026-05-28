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
    if "environment" not in context:
        env_response = client(request).get("/api/environment")
        context["environment"] = data(env_response, {}).get("environment", {})
    if "databases" not in context:
        dbs_response = client(request).get("/api/environment/databases")
        context["databases"] = data(dbs_response, {}).get("databases", [])
    if "error_reason" not in context:
        context["error_reason"] = request.query_params.get("error", "")
    return request.app.state.templates.TemplateResponse(request, template, context)


def err(response: dict[str, Any]) -> str | None:
    if response.get("ok"):
        return None
    error = response.get("error") or {}
    return f"{error.get('code', 'ERROR')}: {error.get('message', 'Unknown backend error')}"


def selected_source_ids(form: dict[str, str]) -> list[str]:
    raw = form.get("source_ids", "")
    return [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]


async def form_fields(request: Request) -> dict[str, str]:
    raw = (await request.body()).decode("utf-8", errors="replace")
    parsed = parse_qs(raw, keep_blank_values=True)
    return {key: ",".join(values) if key == "source_ids" else (values[-1] if values else "") for key, values in parsed.items()}


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
    briefings_r = api.get("/api/briefings/daily")
    reports_r = api.get("/api/reports")
    env = data(env_r, {}).get("environment", {})
    sources = data(sources_r, {}).get("sources", [])
    runs = data(runs_r, {}).get("runs", [])
    events = data(events_r, {}).get("events", [])
    reviews = data(reviews_r, {}).get("reviews", [])
    next_actions: list[dict[str, str]] = []
    last_run = runs[0] if runs else None
    last_mode = ((last_run or {}).get("request") or {}).get("mode")
    if not env.get("is_fresh_database"):
        next_actions.append({"label": "先确认环境", "href": "/environment", "text": "当前不是 Fresh DB，危险操作已禁用。"})
    elif not sources:
        next_actions.append({"label": "导入 source", "href": "/sources", "text": "当前没有 source，从这里开始准备信息入口。"})
    elif not runs:
        next_actions.append({"label": "创建 dry-run", "href": "/runs/new", "text": "已有 source，先 dry-run 验证抓取范围，不写库。"})
    elif last_mode == "dry_run" and last_run.get("status") in {"success", "completed"}:
        next_actions.append({"label": "执行 real-write", "href": "/runs/new", "text": "dry-run 已完成，确认后可用相同 source 范围写入。"})
    elif last_mode == "real_write" and events:
        next_actions.append({"label": "处理 review queue", "href": "/review-queue", "text": "已有 event/review，建议人工确认候选事件。"})
    elif last_mode == "real_write":
        next_actions.append({"label": "执行 pipeline", "href": f"/runs/{last_run['run_id']}", "text": "real-write 完成后继续 dedupe/semantic/events。"})
    if reviews:
        next_actions.append({"label": "进入待审核", "href": "/review-queue", "text": f"当前有 {len(reviews)} 条待处理 review。"})
    if events and not data(briefings_r, {}).get("briefings", []):
        next_actions.append({"label": "生成 briefing", "href": "/briefings", "text": "已有 event，可以生成每日简报。"})
    return render(
        request,
        "ops/dashboard.html",
        {
            "active_page": "dashboard",
            "environment": env,
            "legacy_database": data(env_r, {}).get("legacy_database", {}),
            "sources": sources,
            "source_stats": data(sources_r, {}).get("stats", {}),
            "runs": runs,
            "last_run": last_run,
            "events": events,
            "reviews": reviews,
            "briefings": data(briefings_r, {}).get("briefings", []),
            "reports": data(reports_r, {}).get("reports", []),
            "next_actions": next_actions[:4],
            "error": err(env_r) or err(sources_r) or err(runs_r) or err(briefings_r) or err(reports_r),
        },
    )


@router.get("/environment", response_class=HTMLResponse)
def environment(request: Request):
    api = client(request)
    env_r = api.get("/api/environment")
    health_r = api.get("/api/environment/health")
    return render(request, "ops/environment.html", {"active_page": "environment", "environment": data(env_r, {}).get("environment", {}), "legacy_database": data(env_r, {}).get("legacy_database", {}), "checks": data(health_r, {}).get("checks", []), "error": err(env_r) or err(health_r)})


@router.get("/reset", response_class=HTMLResponse)
def data_reset(request: Request):
    api = client(request)
    env_r = api.get("/api/environment")
    options_r = api.get("/api/environment/reset-options")
    runs_r = api.get("/api/runs", {"limit": 40})
    sources_r = api.get("/api/sources", {"limit": 200})
    return render(
        request,
        "ops/data_reset.html",
        {
            "active_page": "reset",
            "environment": data(env_r, {}).get("environment", {}),
            "legacy_database": data(env_r, {}).get("legacy_database", {}),
            "reset_options": data(options_r, {}).get("levels", []),
            "reset_enabled": data(options_r, {}).get("enabled", False),
            "runs": data(runs_r, {}).get("runs", []),
            "sources": data(sources_r, {}).get("sources", []),
            "error": err(env_r) or err(options_r) or err(runs_r) or err(sources_r),
        },
    )


@router.post("/environment/switch", response_class=HTMLResponse)
async def environment_switch(request: Request):
    form = await form_fields(request)
    database_path = str(form.get("database_path") or "")
    response = client(request).post("/api/environment/switch", {"database_path": database_path})
    if not response.get("ok"):
        error_msg = err(response) or "switch_failed"
        return RedirectResponse(f"/?error={error_msg}", status_code=303)
    referer = request.headers.get("Referer", "/dashboard")
    return RedirectResponse(referer, status_code=303)


@router.post("/environment/init-fresh", response_class=HTMLResponse)
async def environment_init(request: Request):
    form = await form_fields(request)
    database_label = str(form.get("database_label") or "")
    payload = {"database_label": database_label} if database_label else {}
    client(request).post("/api/environment/init-fresh", payload)
    return RedirectResponse("/environment", status_code=303)


@router.post("/environment/reset/preview", response_class=HTMLResponse)
async def environment_reset_preview(request: Request):
    form = await form_fields(request)
    level = str(form.get("level") or "clear_runs_items_keep_sources")
    raw_source_ids = str(form.get("source_ids") or "")
    payload = {
        "level": level,
        "run_id": str(form.get("run_id") or ""),
        "source_ids": [part.strip() for part in raw_source_ids.replace("\n", ",").split(",") if part.strip()],
        "archive_sources": str(form.get("archive_sources") or "") == "1",
    }
    response = client(request).post("/api/environment/reset/preview", payload)
    env_r = client(request).get("/api/environment")
    health_r = client(request).get("/api/environment/health")
    options_r = client(request).get("/api/environment/reset-options")
    runs_r = client(request).get("/api/runs", {"limit": 40})
    sources_r = client(request).get("/api/sources", {"limit": 200})
    template = "ops/data_reset.html" if request.url.path.startswith("/reset") else "ops/environment.html"
    context = {
        "active_page": "reset" if template.endswith("data_reset.html") else "environment",
        "environment": data(env_r, {}).get("environment", {}),
        "legacy_database": data(env_r, {}).get("legacy_database", {}),
        "checks": data(health_r, {}).get("checks", []),
        "reset_options": data(options_r, {}).get("levels", []),
        "reset_enabled": data(options_r, {}).get("enabled", False),
        "runs": data(runs_r, {}).get("runs", []),
        "sources": data(sources_r, {}).get("sources", []),
        "reset_preview": data(response, {}),
        "error": err(response),
    }
    return render(
        request,
        template,
        context,
    )


@router.post("/environment/reset/commit", response_class=HTMLResponse)
async def environment_reset_commit(request: Request):
    form = await form_fields(request)
    level = str(form.get("level") or "")
    operation_id = str(form.get("operation_id") or "")
    confirmation = str(form.get("confirmation") or "")
    raw_source_ids = str(form.get("source_ids") or "")
    payload = {
        "level": level,
        "operation_id": operation_id,
        "confirmation": confirmation,
        "run_id": str(form.get("run_id") or ""),
        "source_ids": [part.strip() for part in raw_source_ids.replace("\n", ",").split(",") if part.strip()],
        "archive_sources": str(form.get("archive_sources") or "") == "1",
    }
    response = client(request).post("/api/environment/reset/commit", payload)
    if not response.get("ok"):
        return RedirectResponse(f"/reset?error={err(response) or 'reset_failed'}", status_code=303)
    return RedirectResponse("/reset", status_code=303)


@router.post("/reset/preview", response_class=HTMLResponse)
async def reset_preview(request: Request):
    return await environment_reset_preview(request)


@router.post("/reset/commit", response_class=HTMLResponse)
async def reset_commit(request: Request):
    return await environment_reset_commit(request)


@router.get("/sources", response_class=HTMLResponse)
def sources(request: Request, status: str | None = None, keyword: str | None = None):
    api = client(request)
    response = api.get("/api/sources", {"status": status, "keyword": keyword, "limit": 200})
    return render(request, "ops/sources.html", {"active_page": "sources", "sources": data(response, {}).get("sources", []), "stats": data(response, {}).get("stats", {}), "status": status or "", "keyword": keyword or "", "error": err(response)})


@router.post("/sources/check", response_class=HTMLResponse)
async def source_check(request: Request):
    form = await form_fields(request)
    payload = {
        "feed_url": str(form.get("feed_url") or ""),
        "source_name": str(form.get("source_name") or ""),
        "source_category": str(form.get("source_category") or ""),
    }
    response = client(request).post("/api/sources/check", payload)
    sources_response = client(request).get("/api/sources", {"limit": 200})
    return render(request, "ops/sources.html", {"active_page": "sources", "sources": data(sources_response, {}).get("sources", []), "stats": data(sources_response, {}).get("stats", {}), "check_result": data(response, {}), "draft_source": payload, "status": "", "keyword": "", "error": err(response)})


@router.post("/sources/add", response_class=HTMLResponse)
async def source_add(request: Request):
    form = await form_fields(request)
    tags = [part.strip() for part in str(form.get("tags") or "").split(",") if part.strip()]
    payload = {
        "source_name": str(form.get("source_name") or form.get("title") or ""),
        "feed_url": str(form.get("feed_url") or ""),
        "source_category": str(form.get("category") or ""),
        "status": str(form.get("status") or "active"),
        "priority": int(form.get("priority") or 3),
        "tags": tags,
        "notes": str(form.get("notes") or ""),
        "config": {"site_url": str(form.get("site_url") or ""), "screen": False},
    }
    client(request).post("/api/sources", payload)
    return RedirectResponse("/sources", status_code=303)


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
    if form.get("preview") == "1":
        response = client(request).post("/api/sources/bulk/preview", {"action": action, "source_ids": ids})
        sources_response = client(request).get("/api/sources", {"limit": 200})
        return render(request, "ops/sources.html", {"active_page": "sources", "sources": data(sources_response, {}).get("sources", []), "stats": data(sources_response, {}).get("stats", {}), "bulk_preview": data(response, {}), "status": "", "keyword": "", "error": err(response)})
    path = {
        "enable": "/api/sources/bulk-enable",
        "disable": "/api/sources/bulk-disable",
        "archive": "/api/sources/bulk-archive",
        "delete": "/api/sources/bulk-delete",
    }.get(action, "/api/sources/bulk-disable")
    client(request).post(path, {"source_ids": ids})
    return RedirectResponse("/sources", status_code=303)


@router.post("/sources/bulk/commit", response_class=HTMLResponse)
async def sources_bulk_commit(request: Request):
    form = await form_fields(request)
    client(request).post("/api/sources/bulk/commit", {"operation_id": str(form.get("operation_id") or "")})
    return RedirectResponse("/sources", status_code=303)


@router.post("/sources/export", response_class=HTMLResponse)
async def sources_export(request: Request):
    form = await form_fields(request)
    fmt = str(form.get("format") or "json")
    response = client(request).post("/api/sources/export", {"format": fmt})
    sources_response = client(request).get("/api/sources", {"limit": 200})
    return render(
        request,
        "ops/sources.html",
        {
            "active_page": "sources",
            "sources": data(sources_response, {}).get("sources", []),
            "stats": data(sources_response, {}).get("stats", {}),
            "export_result": data(response, {}),
            "status": "",
            "keyword": "",
            "error": err(response),
        },
    )


@router.get("/sources/{source_id}", response_class=HTMLResponse)
def source_detail(request: Request, source_id: str):
    response = client(request).get(f"/api/sources/{source_id}")
    return render(request, "ops/source_detail.html", {"active_page": "sources", "source_id": source_id, "data": data(response, {}), "error": err(response)})


@router.post("/sources/{source_id}/edit")
async def source_edit(request: Request, source_id: str):
    form = await form_fields(request)
    payload = {
        "source_name": str(form.get("source_name") or ""),
        "source_category": str(form.get("source_category") or ""),
        "feed_url": str(form.get("feed_url") or ""),
        "status": str(form.get("status") or "active"),
        "priority": int(form.get("priority") or 3),
        "notes": str(form.get("notes") or ""),
        "tags": [part.strip() for part in str(form.get("tags") or "").split(",") if part.strip()],
    }
    client(request).patch(f"/api/sources/{source_id}", payload)
    return RedirectResponse(f"/sources/{source_id}", status_code=303)


@router.post("/sources/{source_id}/archive")
def source_archive(request: Request, source_id: str):
    client(request).post(f"/api/sources/{source_id}/archive", {})
    return RedirectResponse("/sources", status_code=303)


@router.post("/sources/{source_id}/restore")
def source_restore(request: Request, source_id: str):
    client(request).post(f"/api/sources/{source_id}/restore", {})
    return RedirectResponse(f"/sources/{source_id}", status_code=303)


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


def run_form_payload(
    source_ids: str,
    scope_type: str,
    mode: str,
    published_from: str,
    published_to: str,
    max_sources: int,
    max_items_per_source: int,
    max_total_items: int,
    source_timeout_seconds: int,
    run_timeout_minutes: int,
) -> dict[str, Any]:
    ids = [part.strip() for part in source_ids.split(",") if part.strip()]
    return {
        "mode": mode,
        "source_scope": {"type": scope_type, "source_ids": ids},
        "time_filter": {"published_from": published_from or None, "published_to": published_to or None, "timezone": "Asia/Shanghai"},
        "limits": {
            "max_sources": max_sources or len(ids) or 20,
            "max_items_per_source": max_items_per_source,
            "max_total_items": max_total_items,
            "source_timeout_seconds": source_timeout_seconds,
            "run_timeout_minutes": run_timeout_minutes,
        },
        "options": {"force_refetch": False, "stop_on_first_existing": False},
    }


@router.post("/runs/preview", response_class=HTMLResponse)
async def run_preview(request: Request):
    form = await form_fields(request)
    source_ids = str(form.get("source_ids") or "")
    scope_type = str(form.get("scope_type") or "selected")
    mode = str(form.get("mode") or "dry_run")
    published_from = str(form.get("published_from") or "")
    published_to = str(form.get("published_to") or "")
    max_sources = int(form.get("max_sources") or 20)
    max_items_per_source = int(form.get("max_items_per_source") or 20)
    max_total_items = int(form.get("max_total_items") or 200)
    source_timeout_seconds = int(form.get("source_timeout_seconds") or 30)
    run_timeout_minutes = int(form.get("run_timeout_minutes") or 30)
    payload = run_form_payload(source_ids, scope_type, mode, published_from, published_to, max_sources, max_items_per_source, max_total_items, source_timeout_seconds, run_timeout_minutes)
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


@router.post("/runs/{run_id}/pipeline/{stage}")
def run_pipeline_stage(request: Request, run_id: str, stage: str):
    client(request).post(f"/api/runs/{run_id}/pipeline/{stage}", {})
    return RedirectResponse(f"/runs/{run_id}", status_code=303)


@router.post("/runs/{run_id}/briefing")
def run_briefing(request: Request, run_id: str):
    client(request).post(f"/api/runs/{run_id}/briefing", {})
    return RedirectResponse(f"/runs/{run_id}", status_code=303)


@router.post("/runs/{run_id}/report")
def run_report(request: Request, run_id: str):
    client(request).post(f"/api/runs/{run_id}/report", {})
    return RedirectResponse(f"/runs/{run_id}", status_code=303)


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


@router.post("/clusters/{cluster_id}/create-event")
def cluster_create_event(request: Request, cluster_id: str):
    client(request).post(f"/api/clusters/{cluster_id}/create-event", {})
    return RedirectResponse("/events", status_code=303)


@router.get("/events", response_class=HTMLResponse)
def events(request: Request):
    response = client(request).get("/api/events")
    return render(request, "ops/events.html", {"active_page": "events", "items": data(response, {}).get("events", []), "error": err(response)})


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


@router.get("/evidence", response_class=HTMLResponse)
def evidence(request: Request):
    return simple_page(request, "evidence", "Evidence", "/api/evidence", "evidence")


@router.get("/saved-views", response_class=HTMLResponse)
def saved_views(request: Request):
    return simple_page(request, "saved_views", "Saved Views", "/api/saved-views", "saved_views")


@router.get("/review-queue", response_class=HTMLResponse)
def review_queue(request: Request, status: str = "pending"):
    response = client(request).get("/api/review-queue", {"status": status})
    return render(request, "ops/review_queue.html", {"active_page": "review", "status": status, "reviews": data(response, {}).get("reviews", []), "error": err(response)})


@router.post("/review-queue/{review_id}/resolve")
def review_resolve(request: Request, review_id: int):
    client(request).post(f"/api/review-queue/{review_id}/resolve", {"status": "resolved"})
    return RedirectResponse("/review-queue", status_code=303)


@router.post("/review-queue/{review_id}/dismiss")
def review_dismiss(request: Request, review_id: int):
    client(request).post(f"/api/review-queue/{review_id}/resolve", {"status": "dismissed"})
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
def agent_query(request: Request, query: str = "", format: str = "human"):
    result = {}
    error = None
    if query:
        response = client(request).post("/api/agent-query/preview", {"query": query, "format": format})
        result = data(response, {})
        error = err(response)
    return render(request, "ops/agent_query.html", {"active_page": "agent", "query": query, "format": format, "result": result, "error": error})


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return render(request, "ops/settings.html", {"active_page": "settings"})


# ── HTMX Fragment Routes ──

@router.get("/runs/{run_id}/fragment/status", response_class=HTMLResponse)
def run_status_fragment(request: Request, run_id: str):
    api = client(request)
    summary = api.get(f"/api/runs/{run_id}/summary")
    return render(request, "ops/fragments/run_status.html", {
        "run_id": run_id,
        "summary": data(summary, {}),
    })


@router.get("/runs/{run_id}/fragment/timeline", response_class=HTMLResponse)
def run_timeline_fragment(request: Request, run_id: str):
    api = client(request)
    events_r = api.get(f"/api/runs/{run_id}/events")
    return render(request, "ops/fragments/run_timeline.html", {
        "run_id": run_id,
        "events": data(events_r, {}).get("events", []),
    })


@router.get("/dashboard/fragment/recent", response_class=HTMLResponse)
def dashboard_runs_fragment(request: Request):
    api = client(request)
    runs_r = api.get("/api/runs", {"limit": 8})
    return render(request, "ops/fragments/dashboard_recent.html", {
        "runs": data(runs_r, {}).get("runs", []),
    })
