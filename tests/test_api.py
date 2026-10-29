import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_exact_decimal_result():
    response = client.post("/api/calculate", json={"first": "0.1", "second": "0.2", "operation": "add"})
    assert response.status_code == 200
    assert response.json() == {"result": "0.3", "expression": "0.1 + 0.2"}


def test_api_subtraction():
    response = client.post("/api/calculate", json={"first": "-10", "second": "-3", "operation": "subtract"})
    assert response.status_code == 200
    assert response.json()["result"] == "-7"


@pytest.mark.parametrize("change", [
    {"operation": "multiply"}, {"first": "hello"}, {"first": ""},
    {"first": "NaN"}, {"first": "Infinity"}, {"first": True},
    {"first": None}, {"first": "1e10000"},
    {"first": "0.0000000000001"}, {"first": "9" * 31},
    {"extra": "not allowed"},
])
def test_api_rejects_invalid_inputs(change):
    payload = {"first": "2", "second": "3", "operation": "add"}
    payload.update(change)
    assert client.post("/api/calculate", json=payload).status_code == 422


def test_missing_input():
    assert client.post("/api/calculate", json={"first": "2", "operation": "add"}).status_code == 422


def test_frontend_assets_and_health():
    assert client.get("/health").json() == {"status": "ok"}
    response = client.get("/")
    assert response.status_code == 200
    assert "calculator-form" in response.text
    assert client.get("/static/styles.css").status_code == 200
    assert client.get("/static/app.js").status_code == 200
