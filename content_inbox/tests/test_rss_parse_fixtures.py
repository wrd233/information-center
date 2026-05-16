from __future__ import annotations

from pathlib import Path

import pytest

from app.processor import build_dedupe_key, normalize_content
from app.rss import parse_feed


FIXTURES = Path(__file__).parent / "fixtures"


def fixture_uri(name: str) -> str:
    return (FIXTURES / name).as_uri()


def test_parse_rss_basic_maps_core_fields() -> None:
    meta, items = parse_feed(fixture_uri("rss_basic.xml"), limit=10)

    assert meta == {
        "feed_url": fixture_uri("rss_basic.xml"),
        "source_name": "Fixture Basic RSS",
        "feed_title": "Fixture Basic RSS",
        "total_items_found": 2,
    }
    assert len(items) == 2
    first = items[0]
    assert first.title == "Basic RSS Item One"
    assert first.url == "https://fixtures.example.com/items/one?utm_source=newsletter"
    assert first.guid == "basic-1"
    assert first.published_at == "2026-05-16T01:00:00+00:00"
    assert first.author == "editor@example.com"
    assert first.summary == "First basic RSS item with emoji 🚀."
    assert first.content_text == "First basic RSS item with emoji 🚀."


def test_parse_atom_basic_maps_atom_fields() -> None:
    meta, items = parse_feed(fixture_uri("atom_basic.xml"), limit=10)

    assert meta["source_name"] == "Fixture Basic Atom"
    assert meta["total_items_found"] == 1
    item = items[0]
    assert item.title == "Atom Entry One"
    assert item.url == "https://fixtures.example.com/atom/one"
    assert item.guid == "atom-1"
    assert item.published_at == "2026-05-16T03:30:00Z"
    assert item.author == "Atom Author"
    assert item.summary == "Atom entry summary."
    assert item.content_text == "<p>Atom entry full content.</p>"


def test_parse_html_summary_is_safe_and_normalization_cleans_html() -> None:
    _meta, items = parse_feed(fixture_uri("rss_html_summary.xml"), limit=1)

    assert items[0].summary == "<p>Hello <strong>HTML</strong> &amp; emoji ✨.</p>"
    normalized = normalize_content(items[0])
    assert normalized.summary == "Hello HTML & emoji ✨."
    assert normalized.content_text == "Full HTML content."


@pytest.mark.parametrize(
    ("fixture", "expected_url", "expected_guid"),
    [
        ("rss_missing_guid.xml", "https://fixtures.example.com/missing-guid", None),
        ("rss_missing_link.xml", None, "missing-link-guid"),
        ("rss_missing_link_guid.xml", None, None),
    ],
)
def test_parse_missing_link_and_guid_variants(
    fixture: str, expected_url: str | None, expected_guid: str | None
) -> None:
    _meta, items = parse_feed(fixture_uri(fixture), source_name="Fixture Source", limit=1)

    assert len(items) == 1
    assert items[0].url == expected_url
    assert items[0].guid == expected_guid
    assert build_dedupe_key(normalize_content(items[0]))


def test_parse_bad_date_preserves_original_value_without_failing() -> None:
    _meta, items = parse_feed(fixture_uri("rss_bad_date.xml"), limit=1)

    assert len(items) == 1
    assert items[0].published_at == "not a valid rss date"


def test_parse_empty_feed_succeeds_with_no_items() -> None:
    meta, items = parse_feed(fixture_uri("rss_empty.xml"), limit=5)

    assert meta["feed_title"] == "Fixture Empty RSS"
    assert meta["total_items_found"] == 0
    assert items == []


def test_parse_malformed_feed_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="failed to parse feed"):
        parse_feed(fixture_uri("rss_malformed.xml"), limit=5)


def test_parse_limit_applies_before_conversion() -> None:
    meta, items = parse_feed(fixture_uri("rss_many_items.xml"), limit=3)

    assert meta["total_items_found"] == 10
    assert [item.title for item in items] == [
        "Many Item 01",
        "Many Item 02",
        "Many Item 03",
    ]
