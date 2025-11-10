import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
@patch("main.httpx.AsyncClient")
async def test_home(mock_async_client):
    # mock response
    mock_response = AsyncMock()
    mock_response.json.return_value = {"value": "This is a Chuck Norris joke"}

    # mock client
    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = mock_response
    mock_async_client.return_value.__aenter__.return_value = mock_client_instance

    # Test
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert "This is a Chuck Norris joke" in response.text

@pytest.mark.unit
def test_health():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}