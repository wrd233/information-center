from __future__ import annotations

from pathlib import Path

from app.adapters.base import CheckResultData, FeedEntry, FeedResult
from app.config import load_config
from app.models.schemas import RatingAdjustmentRequest, SourceCreate
from app.services.check_service import CheckService
from app.services.export_service import ExportService
from app.services.fetch_service import FetchService
from app.services.import_service import ImportService
from app.services.rating_service import RatingService
from app.services.source_service import SourceService
from app.storage.db import Database
from app.storage.schema import ensure_schema
from app.utils.ids import new_source_id
from app.utils.time import utc_now
from app.utils.url_normalize import normalize_url


def service(tmp_path: Path) -> SourceService:
    config = load_config()
    db = Database(tmp_path / "source_manager.sqlite3")
    return SourceService(db, config)


class FakeAdapter:
    def __init__(self, entries: list[FeedEntry] | None = None, fail: bool = False):
        self.entries = entries or []
        self.fail = fail

    def resolve_url(self, source: dict) -> str:
        return source.get("feed_url") or "http://127.0.0.1:1200/example"

    def check(self, source: dict) -> CheckResultData:
        if self.fail:
            return CheckResultData(False, self.resolve_url(source), 0, utc_now(), "failed")
        return CheckResultData(True, self.resolve_url(source), len(self.entries), utc_now())

    def fetch(self, source: dict, include_raw: bool = False) -> FeedResult:
        if self.fail:
            raise RuntimeError("fetch failed")
        return FeedResult(self.resolve_url(source), "fake", self.entries)


def create_native(svc: SourceService):
    return svc.create(
        SourceCreate(
            source_type="native",
            display_name="Example",
            feed_url="https://example.com/feed.xml",
            status="active",
        )
    )


def test_source_id_format() -> None:
    source_id = new_source_id()
    assert source_id.startswith("src_")
    assert len(source_id) == 16


def test_ensure_schema_preserves_existing_rows(tmp_path: Path) -> None:
    db_path = tmp_path / "source_manager.sqlite3"
    svc = service(tmp_path)
    created = create_native(svc)
    ensure_schema(db_path)
    assert SourceService(Database(db_path), load_config()).get(created.source_id)


def test_single_database_path_config() -> None:
    config = load_config()
    assert config.database_path.name == "source_manager.sqlite3"
    assert "rsshub/source_manager/data/source_manager.sqlite3" in str(config.database_path)


def test_rating_default_clamp_and_adjustment(tmp_path: Path) -> None:
    svc = service(tmp_path)
    created = svc.create(
        SourceCreate(source_type="native", display_name="Rating", feed_url="https://example.com/rss", rating=150)
    )
    assert created.rating == 100
    updated = RatingService(svc).adjust(
        created.source_id,
        RatingAdjustmentRequest(delta=-200, reason="duplicate_noise"),
    )
    assert updated is not None
    assert updated.rating == 0


def test_status_flow_check_does_not_break_fetch_does(tmp_path: Path) -> None:
    svc = service(tmp_path)
    source = create_native(svc)
    svc.adapter_for = lambda source: FakeAdapter(fail=True)  # type: ignore[method-assign]
    check = CheckService(svc).check_one(source.source_id)
    assert check is not None
    assert check.status == "failed"
    assert svc.get(source.source_id).status == "active"  # type: ignore[union-attr]

    fetcher = FetchService(svc)
    for _ in range(3):
        fetcher.fetch_one(source.source_id)
    assert svc.get(source.source_id).status == "broken"  # type: ignore[union-attr]

    svc.adapter_for = lambda source: FakeAdapter(entries=[FeedEntry("g1", "https://example.com/a", "A", None, "S")])  # type: ignore[method-assign]
    fetcher.fetch_one(source.source_id)
    assert svc.get(source.source_id).status == "active"  # type: ignore[union-attr]


def test_entry_identity_and_summary_limit(tmp_path: Path) -> None:
    svc = service(tmp_path)
    fetcher = FetchService(svc)
    entry = FeedEntry("guid", "HTTPS://Example.com/path/?utm_source=x&a=1#frag", "Title", "2026-01-01", "x" * 800)
    assert fetcher.identity_key("src_test", entry) == "https://example.com/path?a=1"
    record = fetcher.entry_record("src_test", entry)
    assert len(record["summary_excerpt"]) == 500
    assert normalize_url(entry.url) == "https://example.com/path?a=1"


def test_fetch_scan_limit_existing_streak_and_run_entries(tmp_path: Path) -> None:
    svc = service(tmp_path)
    source = create_native(svc)
    entries = [FeedEntry(f"g{i}", f"https://example.com/{i}", f"T{i}", None, "S") for i in range(12)]
    svc.adapter_for = lambda source: FakeAdapter(entries=entries)  # type: ignore[method-assign]
    fetcher = FetchService(svc)
    first = fetcher.fetch_one(source.source_id)
    assert first and first["fetch_run"]["new_count"] == 12
    second = fetcher.fetch_one(source.source_id)
    assert second and second["fetch_run"]["existing_count"] == 10
    assert second["fetch_run"]["stopped_reason"] == "existing_streak_reached"


def test_csv_opml_preview_duplicate_and_export(tmp_path: Path) -> None:
    svc = service(tmp_path)
    imports = ImportService(svc)
    csv_text = "display_name,source_type,category,tags,rating,status,feed_url\nOne,native,AI,a|b,80,active,https://example.com/feed\n"
    preview = imports.preview("csv", csv_text, "sources.csv")
    assert preview["summary"]["new"] == 1
    commit = imports.commit("csv", csv_text, filename="sources.csv")
    assert commit["summary"]["created"] == 1
    preview_again = imports.preview("csv", csv_text, "sources.csv")
    assert preview_again["summary"]["duplicate"] == 1
    opml = """<?xml version="1.0"?><opml version="2.0"><body><outline text="AI"><outline text="Two" xmlUrl="https://two.example/rss" /></outline></body></opml>"""
    assert imports.preview("opml", opml)["summary"]["new"] == 1
    broken_csv = "display_name,feed_url,status\nBroken,https://broken.example/rss,broken\n"
    assert imports.preview("csv", broken_csv)["items"][0]["source"]["status"] == "paused"

    exports = ExportService(svc)
    clean = exports.csv("clean")
    full = exports.csv("full")
    assert "source_id,display_name,source_type" in clean
    assert "last_fetch_scanned_count" not in clean
    assert "last_fetch_scanned_count" in full
