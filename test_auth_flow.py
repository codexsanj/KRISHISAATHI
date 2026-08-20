import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_auth_and_saathi_flow():
    # 1. Register new user
    identifier = "newfarmer@krishisaathi.app"
    password = "password123"
    reg_res = client.post("/api/auth/register", json={"identifier": identifier, "password": password})
    assert reg_res.status_code in [200, 400] # 400 if already exists

    # 2. Login
    login_res = client.post("/api/auth/login", json={"identifier": identifier, "password": password})
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Verify GET /api/auth/me
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data.get("isAuthenticated") is True

    # 4. Onboard farm
    onboard_res = client.post("/api/farmer/onboard", json={
        "farmer": {"name": "Test Farmer", "phone": "+91 99999 88888"},
        "farm": {
            "name": "Test Green Farm",
            "area": "3.5 acres",
            "crop": "Wheat",
            "soil_type": "Loamy",
            "water_source": "Canal irrigation",
            "location": "Bengaluru, Karnataka"
        }
    }, headers=headers)
    assert onboard_res.status_code == 200

    # 5. Call Saathi Chat with authenticated token
    questions = [
        "What crop should I grow after wheat?",
        "What is crop rotation?",
        "What is NPK fertilizer?",
        "What should I do today?",
        "Should I irrigate today?",
        "What if rainfall decreases by 20%?"
    ]

    for q in questions:
        chat_res = client.post("/api/chat", json={"message": q}, headers=headers)
        assert chat_res.status_code == 200, f"Failed for question: {q}"
        res_data = chat_res.json()
        assert "answer" in res_data or "message" in res_data
        answer = res_data.get("answer") or res_data.get("message")
        assert len(answer) > 10
        assert "user not found" not in answer.lower()
