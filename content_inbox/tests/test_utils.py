from app.utils import normalize_url


class TestNormalizeUrl:
    def test_strips_utm_params(self):
        assert normalize_url(
            "http://example.com/a?utm_source=twitter&id=123"
        ) == normalize_url("http://example.com/a?id=123")

    def test_strips_fbclid_and_gclid(self):
        assert normalize_url(
            "http://example.com/a?fbclid=abc&id=1"
        ) == normalize_url("http://example.com/a?id=1")

        assert normalize_url(
            "http://example.com/a?gclid=xyz&id=1"
        ) == normalize_url("http://example.com/a?id=1")

    def test_strips_multiple_tracking_params(self):
        url = normalize_url(
            "http://example.com/a?utm_source=twitter&id=123&fbclid=abc&page=2"
        )
        assert "utm_source" not in url
        assert "fbclid" not in url
        assert "id=123" in url
        assert "page=2" in url

    def test_sorts_query_params(self):
        assert normalize_url("http://example.com/a?b=2&a=1") == normalize_url(
            "http://example.com/a?a=1&b=2"
        )

    def test_strips_fragment_does_not_affect_query(self):
        assert normalize_url("http://example.com/a?id=1#section") == normalize_url(
            "http://example.com/a?id=1"
        )

    def test_preserves_business_params(self):
        url = normalize_url("http://example.com/a?id=123&page=2")
        assert "id=123" in url
        assert "page=2" in url

    def test_strips_tracking_but_keeps_others(self):
        url = normalize_url("http://example.com/a?utm_source=twitter&id=123&fbclid=abc")
        assert "utm_source" not in url
        assert "fbclid" not in url
        assert "id=123" in url

    def test_lowercases_scheme_and_host(self):
        assert normalize_url("HTTP://EXAMPLE.COM/Path") == normalize_url(
            "http://example.com/Path"
        )

    def test_removes_trailing_slash(self):
        a = normalize_url("http://example.com/path/")
        b = normalize_url("http://example.com/path")
        assert a == b

    def test_handles_no_query_params(self):
        assert normalize_url("http://example.com/path") is not None

    def test_all_tracking_params_removed_returns_no_query(self):
        url = normalize_url("http://example.com/a?utm_source=x&utm_medium=y")
        assert url is not None
        assert "?" not in url

    def test_handles_none_input(self):
        assert normalize_url(None) is None

    def test_handles_empty_string(self):
        assert normalize_url("") is None

    def test_source_param_stripped(self):
        url = normalize_url("http://example.com/a?source=twitter&id=1")
        assert "source" not in url
        assert "id=1" in url
