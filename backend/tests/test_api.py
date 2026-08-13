import pytest
from fastapi.testclient import TestClient

from qualityforge.api import app

pytestmark = pytest.mark.unit

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_stack() -> None:
    response = client.get("/health/stack")
    assert response.status_code == 200
    body = response.json()
    assert body["llm_provider"] == "ollama"
    assert body["vector_backend"] == "chroma"


def test_create_run() -> None:
    response = client.post(
        "/v1/runs",
        json={
            "id": "QF-1",
            "title": "Shopper can open the cart",
            "text": "As a shopper I can open the cart from https://example.com",
            "jira_key": "QF-1",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["requirement"]["jira_key"] == "QF-1"
    assert body["dom"]["url"] == "https://example.com"
    assert body["results"][0]["status"] == "passed"
