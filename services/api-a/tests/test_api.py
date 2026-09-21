from fastapi.testclient import TestClient

from api_a.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["name"] == "catalog-api"


def test_item_uses_shared_schema() -> None:
    response = client.get("/api/v1/items/7")

    assert response.status_code == 200
    assert response.json()["status"] == "active"
    assert "description" in response.json()


def test_openapi_exposes_shared_item_fields() -> None:
    schema = client.get("/openapi.json").json()
    item_schema = schema["components"]["schemas"]["Item"]

    assert {"id", "name", "description", "status"}.issubset(item_schema["properties"])
