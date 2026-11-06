import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_income_statement_response():
    with TestClient(app) as client:
        response = client.get(
            "/income-statement",
            params={"start": "2026-01-01", "end": "2026-03-31"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["company"] == "Northwind Coffee Roasters"
    assert body["currency"] == "USD"
    assert body["start"] == "2026-01-01"
    assert body["end"] == "2026-03-31"
    assert body["revenue"]["total"] == "37850.50"
    assert body["revenue"]["accounts"][2]["amount"] == "-800.25"
    assert body["net_income"] == "-44480.14"


@pytest.mark.parametrize("params", [
    {},
    {"start": "2026-01-01"},
    {"start": "bad-date", "end": "2026-03-31"},
    {"start": "2026-02-30", "end": "2026-03-31"},
    {"start": "2026-04-01", "end": "2026-03-31"},
])
def test_income_statement_rejects_invalid_dates(params):
    with TestClient(app) as client:
        response = client.get("/income-statement", params=params)
    assert response.status_code == 422
