from __future__ import annotations

from app.adapters.base import BaseAdapter


class RsshubAdapter(BaseAdapter):
    def resolve_url(self, source: dict) -> str:
        adapter_id = source.get("adapter_id") or "rsshub_local"
        adapter = self.config.adapters.get(adapter_id, {})
        base_url = str(adapter.get("base_url", "http://127.0.0.1:1200")).rstrip("/")
        route_path = str(source.get("route_path") or "").strip()
        if not route_path.startswith("/"):
            route_path = "/" + route_path
        return base_url + route_path

