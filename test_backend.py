import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_auth_register_and_login():
    reg_payload = {"identifier": "testfarmer@krishisaathi.app", "password": "password123"}
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code in [200, 400] # 200 or 400 if already exists

    login_payload = {"identifier": "testfarmer@krishisaathi.app", "password": "password123"}
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    assert token is not None

def test_weather_and_market():
    res_w = client.get("/api/weather/current")
    assert res_w.status_code == 200
    assert "temperature_c" in res_w.json()

    res_m = client.get("/api/market/current")
    assert res_m.status_code == 200
    assert len(res_m.json()) > 0

def test_saathi_chat():
    payload = {"message": "Should I irrigate today?"}
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "structured" in data
    assert data["structured"]["what"] is not None

def test_what_if_simulation():
    query = "What if rainfall decreases by 20%, irrigation is reduced by 15%, and fertilizer cost increases by 10%?"
    payload = {"query": query}
    res = client.post("/api/simulation", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["parsed_params"]["rainfall_change_pct"] == -20.0
    assert data["parsed_params"]["irrigation_change_pct"] == -15.0
    assert data["parsed_params"]["fertilizer_cost_change_pct"] == 10.0
    assert "simulated_state" in data
    assert "explanation" in data
