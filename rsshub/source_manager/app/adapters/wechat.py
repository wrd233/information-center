from __future__ import annotations

from app.adapters.base import BaseAdapter


class WechatAdapter(BaseAdapter):
    def resolve_url(self, source: dict) -> str:
        identity = source.get("wechat_identity") or {}
        feed_url = source.get("feed_url") or identity.get("feed_url")
        if feed_url:
            return str(feed_url)
        adapter_id = source.get("adapter_id") or "wechat_local"
        base_url = str(self.config.adapters.get(adapter_id, {}).get("base_url", "http://127.0.0.1:8003")).rstrip("/")
        mp_id = identity.get("mp_id") or identity.get("fakeid") or identity.get("biz")
        if not mp_id:
            raise ValueError("wechat source has no feed_url or mp identity")
        return f"{base_url}/feed/{mp_id}.atom"

