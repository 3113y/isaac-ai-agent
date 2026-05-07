"""
Tests for the FastAPI application endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from isaac_agent.api import app
from isaac_agent.core.agent import MainAgent


@pytest.fixture
def client():
    """Create a test client. The API lifespan creates a MainAgent on startup."""
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    """Tests for GET /health"""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "agent_ready" in data
        assert data["version"] == "0.1.0"

    def test_health_response_schema(self, client):
        response = client.get("/health")
        data = response.json()
        assert isinstance(data["status"], str)
        assert isinstance(data["agent_ready"], bool)
        assert isinstance(data["version"], str)


class TestInfoEndpoint:
    """Tests for GET /info"""

    def test_info_returns_workflow_info(self, client):
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Isaac AI Agent"
        assert "stages" in data
        assert "has_llm" in data
        assert "max_iterations" in data


class TestTemplatesEndpoint:
    """Tests for GET /templates"""

    def test_list_templates(self, client):
        response = client.get("/templates")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert "stats" in data
        assert "MOD_INIT" in data["templates"]
        assert len(data["templates"]) >= 6

    def test_get_specific_template(self, client):
        response = client.get("/templates/MOD_INIT")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "MOD_INIT"
        assert "RegisterMod" in data["code"]
        assert "description" in data

    def test_get_nonexistent_template_returns_404(self, client):
        response = client.get("/templates/NONEXISTENT_TEMPLATE")
        assert response.status_code == 404


class TestAPISearchEndpoint:
    """Tests for GET /api/search"""

    def test_search_api_returns_results(self, client):
        response = client.get("/api/search?query=GetPlayer")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "GetPlayer"
        assert "results" in data

    def test_search_api_empty_query(self, client):
        response = client.get("/api/search?query=")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data


class TestAPICategoriesEndpoint:
    """Tests for GET /api/categories"""

    def test_categories_returns_list(self, client):
        response = client.get("/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) > 0


class TestGenerateEndpoint:
    """Tests for POST /generate"""

    def test_generate_with_fallback_parser(self, client):
        """Generate a mod without LLM — uses fallback keyword parser."""
        response = client.post("/generate", json={
            "user_input": "create a custom item that gives coins to the player",
        })
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["status"] in ("success", "partial")
        assert "generated_code" in data
        assert len(data["generated_code"]) > 0

        # Verify code artifact structure
        artifact = data["generated_code"][0]
        assert "scaffold_type" in artifact
        assert "lua_code" in artifact
        assert len(artifact["lua_code"]) > 0

    def test_generate_entity_mod(self, client):
        """Generate an entity-based mod."""
        response = client.post("/generate", json={
            "user_input": "spawn a custom enemy that explodes on death",
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["generated_code"]) > 0

    def test_generate_invalid_llm_provider(self, client):
        """Test with an invalid LLM provider returns 400."""
        response = client.post("/generate", json={
            "user_input": "test mod",
            "llm_provider": "nonexistent_provider_xyz",
        })
        assert response.status_code == 400

    def test_generate_empty_input(self, client):
        """Test with empty user input still processes."""
        response = client.post("/generate", json={
            "user_input": "",
        })
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
