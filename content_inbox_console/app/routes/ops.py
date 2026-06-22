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
        env_data = data(env_response, {})
        context["environment"] = env_data.get("environment", {})
        context["legacy_database"] = env_data.get("legacy_database", {})
        context["preview_manifest"] = env_data.get("preview_manifest")
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


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value not in (None, "")}


def scope_for_run(run_id: str | None, *, selected: bool = False, context_goal: str | None = None, legacy: bool = False) -> dict[str, Any]:
    if legacy:
        return {
            "label": "Scope: Legacy / 全库",
            "detail": "可能包含历史遗留内容，不是默认 Inbox Operating Loop 数据。",
            "kind": "legacy",
            "run_id": "",
        }
    if context_goal:
        return {
            "label": f"Scope: Context Pack {context_goal}",
            "detail": f"基于 {run_id or 'latest registry_full run'} 的上下文包。",
            "kind": "context_pack",
            "run_id": run_id or "",
        }
    if run_id:
        return {
            "label": f"Scope: {'Selected Run' if selected else 'Latest Inbox Run'}",
            "detail": run_id,
            "kind": "selected_run" if selected else "latest_run",
            "run_id": run_id,
        }
    return {
        "label": "Scope: Latest Inbox Run",
        "detail": "暂无 registry_full Inbox Run。",
        "kind": "empty",
        "run_id": "",
    }


def selected_inbox_run(api: BackendClient, run_id: str = "") -> tuple[dict[str, Any], str, dict[str, Any]]:
    status_r = api.get("/api/inbox-loop/status")
    loop_status = data(status_r, {})
    latest = loop_status.get("latest_run") or {}
    selected = run_id or latest.get("run_id") or ""
    return loop_status, selected, scope_for_run(selected, selected=bool(run_id))


def output_scope_matches(output: dict[str, Any], run_id: str) -> bool:
    scope = output.get("scope") or {}
    return bool(run_id and (scope.get("run_id") == run_id or output.get("object_id") == run_id))


@router.get("/", response_class=HTMLResponse)
def root() -> RedirectResponse:
    return RedirectResponse("/dashboard", status_code=302)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    api = client(request)
    env_r = api.get("/api/environment")
    loop_r = api.get("/api/inbox-loop/status")
    sources_r = api.get("/api/sources", {"limit": 8})
    runs_r = api.get("/api/runs", {"limit": 8})
    briefings_r = api.get("/api/briefings/daily")
    reports_r = api.get("/api/reports")
    env = data(env_r, {}).get("environment", {})
    sources = data(sources_r, {}).get("sources", [])
    runs = data(runs_r, {}).get("runs", [])
    loop_status = data(loop_r, {})
    latest_run = (loop_status.get("latest_run") or {}).get("run_id") or ""
    operating_r = api.get(f"/api/inbox-loop/runs/{latest_run}/operating-view") if latest_run else {"ok": True, "data": {}}
    operating = data(operating_r, {})
    trusted_events = operating.get("trusted_events", [])
    weak_signals = operating.get("weak_signals", [])
    agent_queue = operating.get("agent_queue", [])
    user_escalations = operating.get("user_escalations", [])
    next_actions: list[dict[str, str]] = []
    if not env.get("is_fresh_database"):
        next_actions.append({"label": "先确认环境", "href": "/environment", "text": "当前不是 Fresh DB，危险操作已禁用。"})
    elif not sources:
        next_actions.append({"label": "准备信息源", "href": "/sources", "text": "当前没有活跃信息源，先建立 daily/manual loop 的输入。"})
    elif not latest_run:
        next_actions.append({"label": "运行 Inbox Loop", "href": "/inbox-loop", "text": "还没有 registry_full run，先生成今日默认数据范围。"})
    else:
        next_actions.append({"label": "查看今日情报", "href": f"/today-intel?run_id={latest_run}", "text": "从 latest registry_full run 消费可信事件、弱信号和异常摘要。"})
    if user_escalations:
        next_actions.append({"label": "需要你裁决", "href": f"/agent-processing?run_id={latest_run}", "text": f"有 {len(user_escalations)} 项需要人类裁决。"})
    elif agent_queue:
        next_actions.append({"label": "Agent 处理", "href": f"/agent-processing?run_id={latest_run}", "text": f"有 {len(agent_queue)} 项待 Agent 初筛或写入 decision ledger。"})
    if trusted_events and not [item for item in data(briefings_r, {}).get("briefings", []) if output_scope_matches(item, latest_run)]:
        next_actions.append({"label": "查看输出记录", "href": f"/outputs?run_id={latest_run}", "text": "可信事件已有，可从 run/context 页面触发带 scope 的输出。"})
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
            "last_run": runs[0] if runs else None,
            "trusted_events": trusted_events,
            "weak_signals": weak_signals,
            "agent_queue": agent_queue,
            "user_escalations": user_escalations,
            "briefings": data(briefings_r, {}).get("briefings", []),
            "reports": data(reports_r, {}).get("reports", []),
            "inbox_loop": loop_status,
            "scope": scope_for_run(latest_run),
            "operating": operating,
            "next_actions": next_actions[:4],
            "error": err(env_r) or err(loop_r) or err(sources_r) or err(runs_r) or err(operating_r) or err(briefings_r) or err(reports_r),
        },
    )


@router.get("/inbox-loop", response_class=HTMLResponse)
def inbox_loop(request: Request):
    api = client(request)
    status_r = api.get("/api/inbox-loop/status")
    loop_status = data(status_r, {})
    latest = loop_status.get("latest_run") or {}
    run_id = latest.get("run_id")
    summary_r = api.get(f"/api/inbox-loop/runs/{run_id}/summary") if run_id else {"ok": True, "data": {}}
    diagnostics_r = api.get(f"/api/inbox-loop/runs/{run_id}/diagnostics") if run_id else {"ok": True, "data": {}}
    operating_r = api.get(f"/api/inbox-loop/runs/{run_id}/operating-view") if run_id else {"ok": True, "data": {}}
    return render(
        request,
        "ops/inbox_loop.html",
        {
            "active_page": "inbox_loop",
            "loop_status": loop_status,
            "run_summary": data(summary_r, {}),
            "diagnostics": data(diagnostics_r, {}),
            "operating": data(operating_r, {}),
            "scope": scope_for_run(run_id),
            "manual_result": {},
            "error": err(status_r) or err(summary_r) or err(diagnostics_r) or err(operating_r),
        },
    )


@router.post("/inbox-loop/run", response_class=HTMLResponse)
async def inbox_loop_run(request: Request):
    form = await form_fields(request)
    force = str(form.get("force") or "") == "1"
    run_sync = str(form.get("run_synchronously") or "") == "1"
    max_sources = int(form.get("max_sources") or 10000)
    max_items = int(form.get("max_items_per_source") or 20)
    payload = {
        "force": force,
        "run_synchronously": run_sync,
        "limits": {
            "max_sources": max_sources,
            "max_items_per_source": max_items,
            "probe_limit": max_items,
            "old_source_no_anchor_limit": max_items,
        },
    }
    response = client(request).post("/api/inbox-loop/runs", payload)
    run_id = data(response, {}).get("run_id")
    if run_id and not run_sync:
        return RedirectResponse(f"/runs/{run_id}", status_code=303)
    api = client(request)
    status_r = api.get("/api/inbox-loop/status")
    latest = data(status_r, {}).get("latest_run") or {}
    latest_id = run_id or latest.get("run_id")
    summary_r = api.get(f"/api/inbox-loop/runs/{latest_id}/summary") if latest_id else {"ok": True, "data": {}}
    diagnostics_r = api.get(f"/api/inbox-loop/runs/{latest_id}/diagnostics") if latest_id else {"ok": True, "data": {}}
    operating_r = api.get(f"/api/inbox-loop/runs/{latest_id}/operating-view") if latest_id else {"ok": True, "data": {}}
    return render(
        request,
        "ops/inbox_loop.html",
        {
            "active_page": "inbox_loop",
            "loop_status": data(status_r, {}),
            "run_summary": data(summary_r, {}),
            "diagnostics": data(diagnostics_r, {}),
            "operating": data(operating_r, {}),
            "scope": scope_for_run(latest_id, selected=bool(run_id)),
            "manual_result": data(response, {}),
            "error": err(response) or err(status_r) or err(summary_r),
        },
    )


@router.get("/today-intel", response_class=HTMLResponse)
def today_intel(request: Request, run_id: str = ""):
    api = client(request)
    loop_status, selected_run, scope = selected_inbox_run(api, run_id)
    summary_r = api.get(f"/api/inbox-loop/runs/{selected_run}/summary") if selected_run else {"ok": True, "data": {}}
    operating_r = api.get(f"/api/inbox-loop/runs/{selected_run}/operating-view") if selected_run else {"ok": True, "data": {}}
    return render(
        request,
        "ops/today_intel.html",
        {
            "active_page": "today_intel",
            "loop_status": loop_status,
            "run_id": selected_run,
            "scope": scope,
            "run_summary": data(summary_r, {}),
            "operating": data(operating_r, {}),
            "error": err(summary_r) or err(operating_r),
        },
    )


@router.get("/agent-processing", response_class=HTMLResponse)
@router.get("/triage", response_class=HTMLResponse)
def agent_processing(request: Request, run_id: str = "", goal: str = "review_decisions"):
    api = client(request)
    loop_status, selected_run, scope = selected_inbox_run(api, run_id)
    packets_r = api.get("/api/inbox-loop/triage-packets", clean_params({"run_id": selected_run, "limit": 20}))
    ledger_r = api.get("/api/inbox-loop/decision-ledger", clean_params({"run_id": selected_run, "limit": 50}))
    operating_r = api.get(f"/api/inbox-loop/runs/{selected_run}/operating-view") if selected_run else {"ok": True, "data": {}}
    context_r = api.get("/api/context-packs/" + goal, clean_params({"run_id": selected_run})) if goal in {"daily_brief", "review_decisions"} else {"ok": True, "data": {}}
    return render(
        request,
        "ops/triage.html",
        {
            "active_page": "agent_processing",
            "loop_status": loop_status,
            "run_id": selected_run,
            "goal": goal,
            "scope": scope,
            "packet": data(packets_r, {}),
            "ledger": data(ledger_r, {}),
            "operating": data(operating_r, {}),
            "context_pack": data(context_r, {}).get("context_pack", {}),
            "decision_result": {},
            "error": err(packets_r) or err(ledger_r) or err(operating_r) or err(context_r),
        },
    )


@router.get("/source-health", response_class=HTMLResponse)
def source_health(request: Request, run_id: str = ""):
    api = client(request)
    loop_status, selected_run, scope = selected_inbox_run(api, run_id)
    summary_r = api.get(f"/api/inbox-loop/runs/{selected_run}/summary") if selected_run else {"ok": True, "data": {}}
    diagnostics_r = api.get(f"/api/inbox-loop/runs/{selected_run}/diagnostics") if selected_run else {"ok": True, "data": {}}
    operating_r = api.get(f"/api/inbox-loop/runs/{selected_run}/operating-view") if selected_run else {"ok": True, "data": {}}
    return render(
        request,
        "ops/source_health.html",
        {
            "active_page": "source_health",
            "loop_status": loop_status,
            "run_id": selected_run,
            "scope": scope,
            "run_summary": data(summary_r, {}),
            "diagnostics": data(diagnostics_r, {}),
            "operating": data(operating_r, {}),
            "error": err(summary_r) or err(diagnostics_r) or err(operating_r),
        },
    )


@router.get("/outputs", response_class=HTMLResponse)
def outputs(request: Request, run_id: str = ""):
    api = client(request)
    loop_status, selected_run, scope = selected_inbox_run(api, run_id)
    briefings_r = api.get("/api/briefings/daily")
    reports_r = api.get("/api/reports")
    briefings = data(briefings_r, {}).get("briefings", [])
    reports = data(reports_r, {}).get("reports", [])
    current_outputs = [
        {"type_label": "简报", **item} for item in briefings if output_scope_matches(item, selected_run)
    ] + [
        {"type_label": "报告", **item} for item in reports if output_scope_matches(item, selected_run)
    ]
    legacy_outputs = [
        {"type_label": "简报", **item} for item in briefings if not output_scope_matches(item, selected_run)
    ] + [
        {"type_label": "报告", **item} for item in reports if not output_scope_matches(item, selected_run)
    ]
    return render(
        request,
        "ops/outputs.html",
        {
            "active_page": "outputs",
            "loop_status": loop_status,
            "run_id": selected_run,
            "scope": scope,
            "current_outputs": current_outputs,
            "legacy_outputs": legacy_outputs,
            "error": err(briefings_r) or err(reports_r),
        },
    )


@router.get("/context-query", response_class=HTMLResponse)
def context_query(request: Request, query: str = "", run_id: str = "", goal: str = "daily_brief", format: str = "human", target_type: str = "", target_id: str = ""):
    api = client(request)
    _loop_status, selected_run, _scope = selected_inbox_run(api, run_id)
    params = clean_params({"run_id": selected_run, "target_type": target_type, "target_id": target_id})
    context_r = api.get("/api/context-packs/" + goal, params) if goal in {"daily_brief", "review_decisions", "research_object"} else {"ok": True, "data": {}}
    result = {}
    error = err(context_r)
    if query:
        response = api.post(
            "/api/agent-query/preview",
            {
                "query": query,
                "format": format,
                "goal": goal,
                "run_id": selected_run,
                "target_type": target_type or None,
                "target_id": target_id or None,
            },
        )
        result = data(response, {})
        error = error or err(response)
    context_pack = data(context_r, {}).get("context_pack", {})
    return render(
        request,
        "ops/context_query.html",
        {
            "active_page": "context_query",
            "query": query,
            "format": format,
            "goal": goal,
            "run_id": selected_run,
            "target_type": target_type,
            "target_id": target_id,
            "scope": scope_for_run(selected_run, context_goal=goal),
            "context_pack": context_pack,
            "result": result,
            "error": error,
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
    return render(request, "ops/runs.html", {"active_page": "runs", "scope": {"label": "Scope: Run Registry", "detail": "所有运行记录；registry_full run 是 Inbox Loop 默认数据范围。", "kind": "run_registry"}, "runs": data(response, {}).get("runs", []), "error": err(response)})


@router.get("/runs/new", response_class=HTMLResponse)
def run_wizard(request: Request):
    api = client(request)
    env = data(api.get("/api/environment"), {}).get("environment", {})
    sources = data(api.get("/api/sources", {"status": "active", "limit": 500}), {}).get("sources", [])
    return render(request, "ops/run_wizard.html", {"active_page": "runs_new", "environment": env, "sources": sources})


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
    return render(request, "ops/run_preview.html", {"active_page": "runs_new", "preview": data(response, {}), "payload": json.dumps(payload), "error": err(response)})


@router.post("/runs/start", response_class=HTMLResponse)
async def run_start(request: Request):
    form = await form_fields(request)
    payload_json = str(form.get("payload_json") or "{}")
    payload = json.loads(payload_json)
    response = client(request).post("/api/runs", payload)
    run_id = data(response, {}).get("run_id")
    if run_id:
        return RedirectResponse(f"/runs/{run_id}", status_code=303)
    return render(request, "ops/run_preview.html", {"active_page": "runs_new", "preview": {}, "payload": payload_json, "error": err(response)})


@router.get("/runs/{run_id}", response_class=HTMLResponse)
def run_detail(request: Request, run_id: str):
    api = client(request)
    summary = api.get(f"/api/runs/{run_id}/summary")
    loop_summary = api.get(f"/api/inbox-loop/runs/{run_id}/summary")
    diagnostics = api.get(f"/api/inbox-loop/runs/{run_id}/diagnostics")
    operating = api.get(f"/api/inbox-loop/runs/{run_id}/operating-view")
    ledger = api.get("/api/inbox-loop/decision-ledger", {"run_id": run_id, "limit": 50})
    events = api.get(f"/api/runs/{run_id}/events")
    items = api.get(f"/api/runs/{run_id}/items")
    return render(
        request,
        "ops/run_detail.html",
        {
            "active_page": "runs",
            "run_id": run_id,
            "scope": scope_for_run(run_id, selected=True),
            "summary": data(summary, {}),
            "loop_summary": data(loop_summary, {}),
            "diagnostics": data(diagnostics, {}),
            "operating": data(operating, {}),
            "decision_ledger": data(ledger, {}),
            "events": data(events, {}).get("events", []),
            "items": data(items, {}).get("items", []),
            "error": err(summary),
        },
    )


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
    return render(request, "ops/items.html", {"active_page": "items", "scope": scope_for_run(run_id, selected=bool(run_id)) if run_id else scope_for_run(None, legacy=True), "items": data(response, {}).get("items", []), "run_id": run_id or "", "keyword": keyword or "", "error": err(response)})


@router.get("/items/{item_id}", response_class=HTMLResponse)
def item_detail(request: Request, item_id: str):
    response = client(request).get(f"/api/items/{item_id}")
    ledger = client(request).get("/api/inbox-loop/decision-ledger", {"target_type": "item", "target_id": item_id, "limit": 30})
    return render(request, "ops/item_detail.html", {"active_page": "items", "item_id": item_id, "data": data(response, {}), "decision_ledger": data(ledger, {}), "error": err(response) or err(ledger)})


@router.get("/dedupe-groups", response_class=HTMLResponse)
def dedupe_groups(request: Request):
    response = client(request).get("/api/dedupe-groups")
    return render(request, "ops/simple_list.html", {"active_page": "dedupe", "title": "去重组", "items": data(response, {}).get("dedupe_groups", []), "scope": scope_for_run(None, legacy=True), "error": err(response)})


def simple_page(request: Request, active: str, title: str, api_path: str, key: str):
    response = client(request).get(api_path)
    return render(request, "ops/simple_list.html", {"active_page": active, "title": title, "items": data(response, {}).get(key, []), "scope": scope_for_run(None, legacy=True), "error": err(response)})


@router.get("/clusters", response_class=HTMLResponse)
def clusters(request: Request):
    return simple_page(request, "clusters", "聚合线索", "/api/clusters", "clusters")


@router.get("/clusters/{cluster_id}", response_class=HTMLResponse)
def cluster_detail(request: Request, cluster_id: str):
    response = client(request).get(f"/api/clusters/{cluster_id}")
    ledger = client(request).get("/api/inbox-loop/decision-ledger", {"target_type": "cluster", "target_id": cluster_id, "limit": 30})
    return render(request, "ops/object_detail.html", {"active_page": "clusters", "title": "Cluster Detail", "data": data(response, {}), "decision_ledger": data(ledger, {}), "error": err(response) or err(ledger)})


@router.post("/clusters/{cluster_id}/create-event")
def cluster_create_event(request: Request, cluster_id: str):
    client(request).post(f"/api/clusters/{cluster_id}/create-event", {})
    return RedirectResponse("/events", status_code=303)


@router.get("/events", response_class=HTMLResponse)
def events(request: Request):
    response = client(request).get("/api/events")
    return render(request, "ops/events.html", {"active_page": "legacy_events", "scope": scope_for_run(None, legacy=True), "items": data(response, {}).get("events", []), "error": err(response)})


@router.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail(request: Request, event_id: str):
    response = client(request).get(f"/api/events/{event_id}")
    ledger = client(request).get("/api/inbox-loop/decision-ledger", {"target_type": "event", "target_id": event_id, "limit": 30})
    return render(request, "ops/object_detail.html", {"active_page": "events", "title": "Event Detail", "data": data(response, {}), "decision_ledger": data(ledger, {}), "error": err(response) or err(ledger)})


@router.get("/entities", response_class=HTMLResponse)
def entities(request: Request):
    return simple_page(request, "entities", "实体", "/api/entities", "entities")


@router.get("/relations", response_class=HTMLResponse)
def relations(request: Request):
    return simple_page(request, "relations", "关系", "/api/relations", "relations")


@router.get("/claims", response_class=HTMLResponse)
def claims(request: Request):
    return simple_page(request, "claims", "断言", "/api/claims", "claims")


@router.get("/topics", response_class=HTMLResponse)
def topics(request: Request):
    return simple_page(request, "topics", "主题", "/api/topics", "topics")


@router.get("/timeline", response_class=HTMLResponse)
def timeline(request: Request):
    return simple_page(request, "timeline", "时间线", "/api/timeline", "timeline")


@router.get("/evidence", response_class=HTMLResponse)
def evidence(request: Request):
    return simple_page(request, "evidence", "证据", "/api/evidence", "evidence")


@router.get("/saved-views", response_class=HTMLResponse)
def saved_views(request: Request):
    return simple_page(request, "saved_views", "视图", "/api/saved-views", "saved_views")


@router.get("/review-queue", response_class=HTMLResponse)
def review_queue(request: Request, status: str = "pending", decision_source: str = ""):
    params: dict[str, Any] = {"status": status}
    if decision_source:
        params["decision_source"] = decision_source
    response = client(request).get("/api/review-queue", params)
    return render(request, "ops/review_queue.html", {
        "active_page": "legacy_review",
        "scope": scope_for_run(None, legacy=True),
        "status": status,
        "decision_source": decision_source,
        "reviews": data(response, {}).get("reviews", []),
        "total": data(response, {}).get("total", 0),
        "review_types": data(response, {}).get("review_types", {}),
        "error": err(response),
    })


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
    return render(request, "ops/briefings.html", {"active_page": "legacy_briefings", "scope": scope_for_run(None, legacy=True), "briefings": data(response, {}).get("briefings", []), "error": err(response)})


@router.post("/briefings/daily/generate")
def briefing_generate(request: Request):
    client(request).post("/api/briefings/daily/generate", {})
    return RedirectResponse("/briefings", status_code=303)


@router.get("/reports", response_class=HTMLResponse)
def reports(request: Request):
    response = client(request).get("/api/reports")
    return render(request, "ops/reports.html", {"active_page": "legacy_reports", "scope": scope_for_run(None, legacy=True), "reports": data(response, {}).get("reports", []), "error": err(response)})


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
        response = client(request).post("/api/agent-query/preview", {"query": query, "format": format, "scope_type": "legacy_full"})
        result = data(response, {})
        error = err(response)
    return render(request, "ops/agent_query.html", {"active_page": "legacy_agent_query", "scope": scope_for_run(None, legacy=True), "query": query, "format": format, "result": result, "error": error})


@router.post("/triage/decisions", response_class=HTMLResponse)
@router.post("/agent-processing/decisions", response_class=HTMLResponse)
async def triage_decision(request: Request):
    form = await form_fields(request)
    reason_codes = [part.strip() for part in str(form.get("reason_codes") or "").split(",") if part.strip()]
    evidence_ids = [part.strip() for part in str(form.get("evidence_ids") or "").split(",") if part.strip()]
    payload = {
        "run_id": str(form.get("run_id") or "") or None,
        "packet_id": str(form.get("packet_id") or "") or None,
        "target_type": str(form.get("target_type") or ""),
        "target_id": str(form.get("target_id") or ""),
        "decision": str(form.get("decision") or "research"),
        "confidence": float(form.get("confidence") or 0.5),
        "reason_codes": reason_codes,
        "evidence_ids": evidence_ids,
        "notes": str(form.get("notes") or ""),
        "should_escalate_to_user": str(form.get("should_escalate_to_user") or "") == "1",
        "actor": "console",
    }
    response = client(request).post("/api/inbox-loop/agent-decisions", payload)
    api = client(request)
    run_id = payload["run_id"] or ""
    packets_r = api.get("/api/inbox-loop/triage-packets", {"run_id": run_id or None, "limit": 20})
    ledger_r = api.get("/api/inbox-loop/decision-ledger", {"run_id": run_id or None, "limit": 50})
    operating_r = api.get(f"/api/inbox-loop/runs/{run_id}/operating-view") if run_id else {"ok": True, "data": {}}
    context_r = api.get("/api/context-packs/review_decisions", {"run_id": run_id or None})
    return render(
        request,
        "ops/triage.html",
        {
            "active_page": "agent_processing",
            "run_id": run_id,
            "goal": "review_decisions",
            "scope": scope_for_run(run_id, selected=True),
            "packet": data(packets_r, {}),
            "ledger": data(ledger_r, {}),
            "operating": data(operating_r, {}),
            "context_pack": data(context_r, {}).get("context_pack", {}),
            "decision_result": data(response, {}),
            "error": err(response) or err(packets_r) or err(ledger_r) or err(operating_r),
        },
    )


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


@router.get("/preview-checklist", response_class=HTMLResponse)
def preview_checklist(request: Request):
    return render(request, "ops/preview_checklist.html", {"active_page": "preview_checklist"})
