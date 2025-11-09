import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.mark.unit
@patch("httpx.AyncClient.get")
def test_home(mock_get):
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
        "id": "test_id",
        "url": "https://api.chucknorris.io/jokes/test_id",
        "value": "Chuck Norris can divide by zero."
    }
    mock_get.return_value = mock_response

    response = client.get("/")
    assert response.status_code == 200
    assert "Chuck Norris can divide by zero." in response.text

@pytest.mark.unit
def test_health():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}