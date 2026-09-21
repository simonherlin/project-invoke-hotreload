from fastapi.testclient import TestClient

from api_b.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["name"] == "orders-api"


def test_order_uses_shared_schema() -> None:
    response = client.get("/api/v1/orders/3")

    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_openapi_exposes_shared_item_fields() -> None:
    schema = client.get("/openapi.json").json()
    item_schema = schema["components"]["schemas"]["Item"]

    assert "status" in item_schema["properties"]
