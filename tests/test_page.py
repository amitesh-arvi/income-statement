import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_page_defaults_to_q1_with_form_and_formatted_accounts():
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert 'type="date" id="start" name="start" value="2026-01-01"' in response.text
    assert 'type="date" id="end" name="end" value="2026-03-31"' in response.text
    assert "Marketing (legacy)" in response.text
    assert "(800.25)" in response.text
    assert "(44,480.14)" in response.text


def test_form_range_updates_statement_and_preserves_dates():
    with TestClient(app) as client:
        params = {"start": "2026-03-20", "end": "2026-03-20"}
        response = client.get("/", params=params)
        api = client.get("/income-statement", params=params).json()
    assert response.status_code == 200
    assert 'value="2026-03-20"' in response.text
    assert api["net_income"] == "100.00"
    assert '<td class="amount">100.00</td>' in response.text
    assert "(44,480.14)" not in response.text


@pytest.mark.parametrize(("params", "message"), [
    ({"start": "2026-04-01", "end": "2026-03-31"}, "Start date must be on or before end date."),
    ({"start": "2026-02-30"}, "Enter a valid start and end date."),
    ({"start": ""}, "Enter a valid start and end date."),
    ({"end": "bad-date"}, "Enter a valid start and end date."),
])
def test_page_shows_date_errors_in_html(params, message):
    with TestClient(app) as client:
        response = client.get("/", params=params)
    assert response.status_code == 422
    assert 'role="alert"' in response.text
    assert message in response.text
    assert '<table>' not in response.text
