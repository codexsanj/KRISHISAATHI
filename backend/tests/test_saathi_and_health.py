import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_test_jpeg():
    img = Image.new("RGB", (224, 224), color=(40, 140, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_saathi_greetings_and_specific_queries():
    # 1. Greeting "hi"
    r1 = client.post("/api/chat", json={"message": "hi"})
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["intent"] == "GREETING"
    assert "how can i help" in d1["answer"].lower() or "hi" in d1["answer"].lower()
    assert "wheat typically requires" not in d1["answer"].lower()

    # 2. "What is crop rotation?"
    r2 = client.post("/api/chat", json={"message": "What is crop rotation?"})
    assert r2.status_code == 200
    d2 = r2.json()
    assert "crop rotation" in d2["answer"].lower() or "rotation" in d2["answer"].lower()

    # 3. "What fertilizer should I use?"
    r3 = client.post("/api/chat", json={"message": "What fertilizer should I use?"})
    assert r3.status_code == 200
    d3 = r3.json()
    assert "npk" in d3["answer"].lower() or "fertilizer" in d3["answer"].lower() or "nitrogen" in d3["answer"].lower()

    # 4. "What is today's weather?"
    r4 = client.post("/api/chat", json={"message": "What is today's weather?"})
    assert r4.status_code == 200
    d4 = r4.json()
    assert d4["intent"] == "WEATHER"
    assert "weather" in d4["answer"].lower() or "temperature" in d4["answer"].lower()

    # 5. "What if rainfall decreases by 20%?"
    r5 = client.post("/api/chat", json={"message": "What if rainfall decreases by 20%?"})
    assert r5.status_code == 200
    d5 = r5.json()
    assert d5["is_what_if"] is True

    # 6. "How do I control pests?"
    r6 = client.post("/api/chat", json={"message": "How do I control pests?"})
    assert r6.status_code == 200
    d6 = r6.json()
    assert "pest" in d6["answer"].lower() or "neem" in d6["answer"].lower()

def test_crop_health_image_upload_pipeline():
    jpeg_bytes = create_test_jpeg()

    # 1. Upload for Tomato
    files = {"file": ("leaf_test.jpg", io.BytesIO(jpeg_bytes), "image/jpeg")}
    data = {"crop": "Tomato"}
    r1 = client.post("/api/health/disease-detect", files=files, data=data)
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["status"] in ["high_confidence", "medium_confidence", "low_confidence", "success", "uncertain"]
    assert d1["confidence"] > 0.0

    # 2. Upload for Cotton
    files = {"file": ("cotton_leaf.jpg", io.BytesIO(jpeg_bytes), "image/jpeg")}
    data = {"crop": "Cotton"}
    r2 = client.post("/api/health/disease-detect", files=files, data=data)
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["status"] in ["high_confidence", "medium_confidence", "low_confidence", "success", "uncertain"]
    assert d2["confidence"] > 0.0

    # 3. Empty/corrupted file error test
    files = {"file": ("empty.jpg", io.BytesIO(b"short"), "image/jpeg")}
    data = {"crop": "Cotton"}
    r3 = client.post("/api/health/disease-detect", files=files, data=data)
    assert r3.status_code == 200
    d3 = r3.json()
    assert d3["status"] == "error" or d3["requires_expert"] is True
