import pytest
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_auth_me_no_hardcoded_demo_farmer():
    """Verify /api/auth/me returns actual user data and None for farm if incomplete, NEVER Demo Farmer/Wheat."""
    reg_resp = client.post("/api/auth/register", json={
        "identifier": "farmer_ragi_test@krishi.in",
        "password": "pass1234password"
    })
    assert reg_resp.status_code in [200, 400]

    login_resp = client.post("/api/auth/login", json={
        "identifier": "farmer_ragi_test@krishi.in",
        "password": "pass1234password"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200
    data = me_resp.json()

    assert data["isAuthenticated"] is True
    assert data["farmer"]["email"] == "farmer_ragi_test@krishi.in"
    assert data["farmer"]["name"] != "Demo Farmer"
    assert data["farm"] is None  # Farm not setup yet — MUST NOT substitute Demo Farmer!


def test_saathi_missing_farm_profile():
    """When user has no farm profile, farm-specific queries ask to complete profile."""
    client.post("/api/auth/register", json={
        "identifier": "nofarm_test@krishi.in",
        "password": "pass1234password"
    })
    login_resp = client.post("/api/auth/login", json={
        "identifier": "nofarm_test@krishi.in",
        "password": "pass1234password"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/chat", json={"message": "What should I do today?"}, headers=headers)
    assert resp.status_code == 200
    answer = resp.json()["answer"]
    assert "farm profile" in answer.lower() or "farm setup" in answer.lower()
    assert "wheat" not in answer.lower()
    assert "bengaluru" not in answer.lower()


def test_saathi_farmer_context_isolation():
    """Farmer A (Ragi in Mandya) and Farmer B (Tomato in Kolar) receive their OWN context, NEVER Wheat/Bengaluru."""

    # 1. Setup Farmer A: Ragi, Mandya, Red Soil
    client.post("/api/auth/register", json={"identifier": "farmer_a_iso@krishi.in", "password": "password123"})
    login_a = client.post("/api/auth/login", json={"identifier": "farmer_a_iso@krishi.in", "password": "password123"})
    token_a = login_a.json()["access_token"]
    client.post("/api/farmer/onboard", json={
        "farmer": {"name": "Ramesh Gowda", "phone": "+919111111111"},
        "farm": {"name": "Mandya Ragi Farm", "crop": "Ragi", "location": "Mandya, Karnataka", "soil_type": "Red"}
    }, headers={"Authorization": f"Bearer {token_a}"})

    # 2. Setup Farmer B: Tomato, Kolar, Sandy Soil
    client.post("/api/auth/register", json={"identifier": "farmer_b_iso@krishi.in", "password": "password123"})
    login_b = client.post("/api/auth/login", json={"identifier": "farmer_b_iso@krishi.in", "password": "password123"})
    token_b = login_b.json()["access_token"]
    client.post("/api/farmer/onboard", json={
        "farmer": {"name": "Suresh Reddy", "phone": "+919222222222"},
        "farm": {"name": "Kolar Tomato Farm", "crop": "Tomato", "location": "Kolar, Karnataka", "soil_type": "Sandy"}
    }, headers={"Authorization": f"Bearer {token_b}"})

    # Ask Farmer A: "What can I do today?"
    resp_a = client.post("/api/chat", json={"message": "What can I do today?"}, headers={"Authorization": f"Bearer {token_a}"})
    ans_a = resp_a.json()["answer"]
    assert "Ragi" in ans_a
    assert "Tomato" not in ans_a
    assert "Wheat" not in ans_a

    # Ask Farmer B: "What can I do today?"
    resp_b = client.post("/api/chat", json={"message": "What can I do today?"}, headers={"Authorization": f"Bearer {token_b}"})
    ans_b = resp_b.json()["answer"]
    assert "Tomato" in ans_b
    assert "Ragi" not in ans_b
    assert "Wheat" not in ans_b


def test_saathi_part3_all_13_questions():
    """Verify all 13 required test questions work accurately."""
    questions = [
        ("hello", ["hi", "saathi", "help"]),
        ("What is NPK?", ["nitrogen", "phosphorus", "potassium"]),
        ("What is crop rotation?", ["crop rotation", "legume", "nitrogen"]),
        ("What can I do today?", ["farm profile", "today", "action", "ragi", "wheat", "tomato"]),
        ("How much water does rice need?", ["1000", "2000", "rice", "paddy", "water"]),
        ("What fertilizer is suitable for ragi?", ["ragi", "npk", "60:30:30"]),
        ("What is today's weather?", ["weather", "temperature", "rain"]),
        ("Should I irrigate today?", ["irrigation", "water", "farm profile", "crop"]),
        ("What if rainfall decreases by 20%?", ["simulation", "yield", "rainfall", "decrease"]),
        ("How can I control pests?", ["pest", "scouting", "neem"]),
        ("My tomato leaves are yellow.", ["yellow", "blight", "nitrogen", "tomato"]),
        ("Why?", ["yellow", "leaf", "blight", "nitrogen"]),
        ("What should I do next?", ["inspect", "field", "spray", "management"])
    ]

    for query, expected_keywords in questions:
        resp = client.post("/api/chat", json={"message": query})
        assert resp.status_code == 200, f"Failed on query: {query}"
        answer = resp.json()["answer"].lower()
        matched = any(kw in answer for kw in expected_keywords)
        assert matched, f"Query '{query}' response did not contain expected keywords {expected_keywords}. Got: {answer}"


def test_pest_image_upload_pipeline():
    """Verify POST /api/pest/detect accepts JPEG/PNG multipart uploads and returns honest model_unavailable/success response."""

    # 1. Test with valid JPEG image
    img_data = b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"\x00" * 1000
    files = {"file": ("pest_leaf.jpg", io.BytesIO(img_data), "image/jpeg")}
    data = {"crop": "Cotton"}

    resp = client.post("/api/pest/detect", files=files, data=data)
    assert resp.status_code == 200
    res_json = resp.json()
    assert res_json["status"] in ["model_unavailable", "success"]
    assert "supported_classes" in res_json
    assert "aphid" in res_json["supported_classes"]

    # 2. Test with invalid file type (e.g. text file)
    bad_files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    bad_resp = client.post("/api/pest/detect", files=bad_files)
    assert bad_resp.status_code == 422
    assert "unsupported file type" in bad_resp.json()["detail"].lower()


def test_disease_upload_remains_functional():
    """Verify disease upload POST /api/health/disease-detect still works independently."""
    from PIL import Image
    img = Image.new("RGB", (224, 224), color=(30, 140, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_data = buf.getvalue()

    files = {"file": ("leaf.jpg", io.BytesIO(img_data), "image/jpeg")}
    data = {"crop": "Rice"}

    resp = client.post("/api/health/disease-detect", files=files, data=data)
    assert resp.status_code == 200
    res_json = resp.json()
    assert res_json["status"] in ["high_confidence", "medium_confidence", "low_confidence", "success", "uncertain"]
    assert "prediction" in res_json
    assert res_json["confidence"] > 0.0
