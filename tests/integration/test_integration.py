import requests
import os
import time
import pytest

BASE_URL = os.getenv("BASE_URL")

def wait_for_service(url, timeout=10):
    for _ in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    raise TimeoutError(f"Service {url} not ready after {timeout}s")

@pytest.mark.integration
def test_healthz():
    wait_for_service(f"{BASE_URL}/healthz")
    r = requests.get(f"{BASE_URL}/healthz")
    assert r.status_code == 200

@pytest.mark.integration
def test_home():
    wait_for_service(f"{BASE_URL}/")
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert "Chuck Norris" in r.text

@pytest.mark.integration
def test_category_view():
    wait_for_service(f"{BASE_URL}/category?category=dev")
    r = requests.get(f"{BASE_URL}/category", params={"category": "dev"})
    assert r.status_code == 200
    assert "Chuck Norris" in r.text or "dev" in r.text

@pytest.mark.integration
def test_search_view():
    wait_for_service(f"{BASE_URL}/search?query=chuck")
    r = requests.get(f"{BASE_URL}/search", params={"query": "beer"})
    assert r.status_code == 200
    assert "beer" in r.text or "chuck" in r.text