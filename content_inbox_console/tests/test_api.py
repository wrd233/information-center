"""API tests for content_inbox_console."""

from pathlib import Path


class TestHealthAndDashboard:
    def test_redirect_root_to_dashboard(self, populated_client):
        response = populated_client.get("/", follow_redirects=False)
        assert response.status_code == 302

    def test_dashboard_page(self, populated_client):
        response = populated_client.get("/dashboard")
        assert response.status_code == 200
        html = response.text
        assert "Dashboard" in html
        assert "Test Source 1" in html
        assert "2" in html  # total sources

    def test_dashboard_stats_api(self, populated_client):
        response = populated_client.get("/api/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["db_available"] is True
        assert data["total_sources"] == 2
        assert data["total_items"] == 2
        assert data["total_runs"] == 1
        assert data["total_clusters"] == 1


class TestItemsAPI:
    def test_items_page(self, populated_client):
        response = populated_client.get("/items")
        assert response.status_code == 200
        html = response.text
        assert "Test Article 1" in html
        assert "Test Article 2" in html

    def test_items_with_filter(self, populated_client):
        response = populated_client.get("/items?source_id=source_1")
        assert response.status_code == 200
        html = response.text
        assert "Test Article 1" in html
        assert "Test Article 2" not in html

    def test_items_with_keyword(self, populated_client):
        response = populated_client.get("/items?keyword=Article 2")
        assert response.status_code == 200
        html = response.text
        assert "Test Article 2" in html
        assert "Test Article 1" not in html

    def test_items_htmx_rows(self, populated_client):
        response = populated_client.get("/items/rows", headers={"HX-Request": "true"})
        assert response.status_code == 200
        # HTMX rows fragment should contain table rows
        assert "<tr>" in response.text

    def test_items_pagination(self, populated_client):
        response = populated_client.get("/items?page_size=1&page=1")
        assert response.status_code == 200
        html = response.text
        assert "Next" in html or "page" in html.lower()

    def test_item_detail(self, populated_client):
        response = populated_client.get("/items/item_1")
        assert response.status_code == 200
        html = response.text
        assert "Test Article 1" in html
        assert "source_1" in html
        assert "suggested_action" in html or "read" in html

    def test_item_not_found(self, populated_client):
        response = populated_client.get("/items/nonexistent")
        assert response.status_code == 404


class TestSourcesAPI:
    def test_sources_page(self, populated_client):
        response = populated_client.get("/sources")
        assert response.status_code == 200
        html = response.text
        assert "Test Source 1" in html
        assert "Test Source 2" in html

    def test_sources_with_status_filter(self, populated_client):
        response = populated_client.get("/sources?status=broken")
        assert response.status_code == 200
        html = response.text
        assert "Test Source 2" in html
        assert "Test Source 1" not in html

    def test_sources_htmx_rows(self, populated_client):
        response = populated_client.get("/sources/rows")
        assert response.status_code == 200
        assert "<tr>" in response.text

    def test_source_detail(self, populated_client):
        response = populated_client.get("/sources/source_1")
        assert response.status_code == 200
        html = response.text
        assert "Test Source 1" in html
        assert "https://example.com/feed1.xml" in html

    def test_source_not_found(self, populated_client):
        response = populated_client.get("/sources/nonexistent")
        assert response.status_code == 404


class TestRunsAPI:
    def test_runs_page(self, populated_client):
        response = populated_client.get("/runs")
        assert response.status_code == 200
        html = response.text
        assert "run_1" in html

    def test_runs_htmx_rows(self, populated_client):
        response = populated_client.get("/runs/rows")
        assert response.status_code == 200
        assert "<tr>" in response.text

    def test_run_detail(self, populated_client):
        response = populated_client.get("/runs/run_1")
        assert response.status_code == 200
        html = response.text
        assert "run_1" in html
        assert "Test Source 1" in html
        assert "Test Source 2" in html

    def test_run_not_found(self, populated_client):
        response = populated_client.get("/runs/nonexistent")
        assert response.status_code == 404


class TestClustersAPI:
    def test_clusters_page(self, populated_client):
        response = populated_client.get("/clusters")
        assert response.status_code == 200
        html = response.text
        assert "Test Cluster" in html

    def test_cluster_detail(self, populated_client):
        response = populated_client.get("/clusters/cluster_1")
        assert response.status_code == 200
        html = response.text
        assert "Test Cluster" in html
        assert "AI" in html

    def test_cluster_not_found(self, populated_client):
        response = populated_client.get("/clusters/nonexistent")
        assert response.status_code == 404


class TestErrorStates:
    def test_empty_database(self, client: "TestClient"):
        """Verify empty database shows empty states, not errors."""
        from app.dependencies import get_db_connection

        response = client.get("/dashboard")
        assert response.status_code == 200
        html = response.text
        # Should show empty states
        assert "No sources" in html or "No runs" in html or "empty-state" in html.lower()

    def test_empty_items(self, client: "TestClient"):
        response = client.get("/items")
        assert response.status_code == 200
        html = response.text
        assert "No items" in html or "empty-state" in html.lower() or "Loading" in html
