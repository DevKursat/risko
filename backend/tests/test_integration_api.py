import time
import pytest
import httpx
from fastapi import status

# Base URL for the running backend service inside the container
BASE_URL = "http://127.0.0.1:8000"


def wait_for_server(timeout: int = 10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = httpx.get(f"{BASE_URL}/health", timeout=1.0)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    raise RuntimeError("Backend server not reachable at {BASE_URL}")


def _load_app_from_backend_main():
    # Prefer importing the backend package directly; fall back to file load if needed.
    try:
        import importlib
        module = importlib.import_module("backend.main")
        return getattr(module, "app")
    except Exception:
        # Fallback: load by path (last resort)
        import importlib.util
        from pathlib import Path
        here = Path(__file__).resolve()
        candidates = [Path("/app/backend/main.py"), here.parents[2] / "main.py", here.parents[1] / "main.py", Path("/app/main.py")]
        candidate = None
        for c in candidates:
            if c and c.exists():
                candidate = c
                break
        if candidate is None:
            raise FileNotFoundError("Could not locate backend main.py to load app for tests")

        spec = importlib.util.spec_from_file_location("backend_main", str(candidate))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "app")


def test_health_check():
    wait_for_server()
    resp = httpx.get(f"{BASE_URL}/health")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data.get("status") == "healthy"


def test_risk_analysis_success():
    wait_for_server()
    payload = {"address": "Ankara, Çankaya"}
    resp = httpx.post(f"{BASE_URL}/api/v1/risk/analyze", json=payload, timeout=10.0)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    # Expected keys
    assert "address" in data
    assert "overall_risk_score" in data
    assert "risk_level" in data


def test_risk_analysis_invalid_input():
    wait_for_server()
    payload = {"location": "test"}
    resp = httpx.post(f"{BASE_URL}/api/v1/risk/analyze", json=payload)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
