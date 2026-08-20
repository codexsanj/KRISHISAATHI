import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.market_service import market_service

client = TestClient(app)


def test_market_service_40_plus_crops():
    crops = market_service.get_supported_crops()
    assert len(crops) >= 40
    assert "Rice" in crops
    assert "Wheat" in crops
    assert "Ginger" in crops
    assert "Tomato" in crops
    assert "Onion" in crops


def test_market_search():
    res_gin = market_service.search_commodities("gin")
    assert "Ginger" in res_gin

    res_tom = market_service.search_commodities("tom")
    assert "Tomato" in res_tom


def test_normalized_price_contract():
    prices = market_service.get_prices("Ginger")
    assert len(prices) > 0
    top = prices[0]
    assert isinstance(top["modal_price"], float)
    assert isinstance(top["price_per_quintal"], float)
    assert top["modal_price"] > 0
    assert top["unit"] == "₹/quintal"
    assert "mandi" in top


def test_historical_prices():
    hist = market_service.get_historical_prices("Ginger", days=30)
    assert hist["commodity"] == "Ginger"
    assert len(hist["history"]) > 0
    assert hist["history"][0]["modal_price"] > 0


def test_market_api_endpoints():
    # 1. Supported crops list
    r1 = client.get("/api/market/crops")
    assert r1.status_code == 200
    assert r1.json()["count"] >= 40

    # 2. Search crops
    r2 = client.get("/api/market/crops/search?q=rice")
    assert r2.status_code == 200
    assert "Rice" in r2.json()["matches"]

    # 3. States & Districts
    r3 = client.get("/api/market/states")
    assert r3.status_code == 200
    assert "Karnataka" in r3.json()

    r4 = client.get("/api/market/districts?state=Karnataka")
    assert r4.status_code == 200
    assert "Hassan" in r4.json()

    # 4. Popular crops summary
    r5 = client.get("/api/market/popular")
    assert r5.status_code == 200
    assert len(r5.json()) >= 12

    # 5. Price history
    r6 = client.get("/api/market/prices/history?crop=Tomato&days=30")
    assert r6.status_code == 200
    assert r6.json()["commodity"] == "Tomato"

    # 6. Market comparison
    r7 = client.get("/api/market/compare?crop=Onion")
    assert r7.status_code == 200
    assert "comparison" in r7.json()

    # 7. Selling strategy
    r8 = client.get("/api/market/selling?crop=Ginger&quantity_q=15")
    assert r8.status_code == 200
    assert r8.json()["estimated_gross_revenue"] > 0


def test_saathi_chat_market_queries():
    chat_r = client.post("/api/chat", json={"message": "What is today's ginger price in Hassan?"})
    assert chat_r.status_code == 200
    answer = chat_r.json()["answer"]
    assert "Ginger" in answer
    assert "Modal Price" in answer or "Hassan APMC" in answer
