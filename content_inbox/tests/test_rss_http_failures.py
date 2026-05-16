from __future__ import annotations

import socket
import urllib.error

from app.rss_errors import classify_exception, retryable_for


def test_http_statuses_map_to_structured_error_codes() -> None:
    assert classify_exception(urllib.error.HTTPError("http://x", 404, "missing", {}, None))[0] == "rss_fetch_not_found"
    assert classify_exception(urllib.error.HTTPError("http://x", 429, "limited", {}, None))[0] == "rss_fetch_rate_limited"
    assert classify_exception(urllib.error.HTTPError("http://x", 502, "bad gateway", {}, None))[0] == "rss_fetch_server_error"


def test_timeout_and_connection_errors_are_retryable() -> None:
    timeout_code, _ = classify_exception(socket.timeout("timed out"))
    connection_code, _ = classify_exception(urllib.error.URLError("connection refused"))

    assert timeout_code == "rss_fetch_timeout"
    assert connection_code == "rss_fetch_connection_error"
    assert retryable_for(timeout_code) is True
    assert retryable_for(connection_code) is True
