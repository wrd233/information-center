from __future__ import annotations

from app.adapters.base import BaseAdapter


class NativeAdapter(BaseAdapter):
    def resolve_url(self, source: dict) -> str:
        feed_url = source.get("feed_url")
        if not feed_url:
            raise ValueError("native source has no feed_url")
        return str(feed_url)

