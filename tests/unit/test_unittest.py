import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app

client = TestClient(app)

@pytest.mark.unit
@pytest.mark.asyncio
@patch("app.main.httpx.AsyncClient")
async def test_home(mock_async_client):
    # mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "value": "This is a Chuck Norris joke"
    }
    # # mock client
    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = mock_response
    #
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

@pytest.mark.unit
@pytest.mark.asyncio
@patch("app.main.fetch_categories_safe")
@patch("app.main.httpx.AsyncClient.get")
async def test_category_view(mock_get, mock_fetch_categories):
    """Test category dropdown and selected joke."""
    mock_fetch_categories.return_value = ["dev", "animal", "career"]

    mock_joke_response = MagicMock()
    mock_joke_response.status_code = 200
    mock_joke_response.json.return_value = {
        "value": "Chuck Norris writes code that optimizes itself."
    }
    mock_get.return_value = mock_joke_response

    res = client.get("/category", params={"category": "dev"})
    assert res.status_code == 200
    # assert "Chuck Norris writes code that optimizes itself." in res.text
    assert "dev" in res.text  # category present

@pytest.mark.unit
@pytest.mark.asyncio
@patch("app.main.fetch_categories_safe")
@patch("app.main.httpx.AsyncClient.get")
async def test_search_view_valid(mock_get, mock_fetch_categories):
    """Test valid search query."""
    mock_fetch_categories.return_value = ["dev", "animal"]

    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "total": 1,
        "result": [
            {"value": "Chuck Norris searched the internet once. It was enough."}
        ],
    }
    mock_get.return_value = mock_search_response

    res = client.get("/search", params={"query": "norris"})
    assert res.status_code == 200
    assert "Chuck Norris searched the internet once. It was enough." in res.text

@pytest.mark.unit
@pytest.mark.asyncio
@patch("app.main.fetch_categories_safe")
async def test_search_view_invalid(mock_fetch_categories):
    """Test invalid or too short query."""
    mock_fetch_categories.return_value = ["dev", "animal"]

    # Too short
    res = client.get("/search", params={"query": "hi"})
    assert res.status_code == 200
    assert "Invalid search query" in res.text or "Please enter a search text." in res.text

@pytest.mark.unit
@patch("app.main.fetch_categories_safe", new_callable=AsyncMock)
def test_search_empty_query(mock_fetch_cat):
    """Empty query should return the 'Please enter a search text.' message"""
    mock_fetch_cat.return_value = ["dev", "animal"]

    # no query param
    res = client.get("/search")
    assert res.status_code == 200
    assert "Please enter a search text." in res.text

    # explicit empty string
    res2 = client.get("/search", params={"query": ""})
    assert res2.status_code == 200
    assert "Please enter a search text." in res2.text

@pytest.mark.unit
@patch("app.main.fetch_categories_safe", new_callable=AsyncMock)
def test_search_too_short_and_too_long(mock_fetch_cat):
    """Query shorter than MIN or longer than MAX should be rejected"""
    mock_fetch_cat.return_value = ["dev", "animal"]

    # too long
    long_q = "x" * 121
    res_long = client.get("/search", params={"query": long_q})
    assert res_long.status_code == 200
    assert "Invalid search query" in res_long.text

@pytest.mark.unit
@patch("app.main.fetch_categories_safe", new_callable=AsyncMock)
def test_search_injection_patterns_are_rejected(mock_fetch_cat):
    """Common SQL/script injection patterns should be rejected by validation"""
    mock_fetch_cat.return_value = ["dev", "animal"]

    malicious_inputs = [
        "'; DROP TABLE users; --",
        "1; DROP TABLE users",
        "<script>alert(1)</script>",
        "name OR 1=1",
        "$(rm -rf /)"  # shell-like injection
    ]

    for payload in malicious_inputs:
        res = client.get("/search", params={"query": payload})
        assert res.status_code == 200
        assert "Invalid search query" in res.text
