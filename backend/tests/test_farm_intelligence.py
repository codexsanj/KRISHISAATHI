import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app
from app.ai.farm_intelligence.crop_lifecycle_engine import crop_lifecycle_engine
from app.ai.farm_intelligence.crop_recommendation_engine import crop_recommendation_engine
from app.ai.farm_intelligence.sowing_decision_engine import sowing_decision_engine
from app.ai.farm_intelligence.daily_farm_plan_engine import daily_farm_plan_engine
from app.services.weather_service import weather_service
from app.services.market_service import market_service
from app.ai.farm_intelligence.selling_decision_engine import selling_decision_engine

client = TestClient(app)


def test_crop_lifecycle_engine():
    res = crop_lifecycle_engine.get_lifecycle_info("Ginger", "2026-06-01")
    assert res["crop_name"] == "Ginger"
    assert res["crop_age_days"] >= 0
    assert "current_stage" in res
    assert "harvest_window" in res
    assert len(res["task_milestones"]) > 0


def test_crop_recommendation_engine():
    recs = crop_recommendation_engine.get_recommendations("Hassan, Karnataka", "Loamy", "Canal")
    assert len(recs) >= 3
    assert recs[0]["suitability_score"] >= recs[1]["suitability_score"]
    assert "reasons" in recs[0]


def test_sowing_decision_engine():
    sow_info = sowing_decision_engine.evaluate_sowing_window("Ginger", "Hassan", rainfall_forecast_mm=10.0)
    assert sow_info["crop"] == "Ginger"
    assert "recommended_window" in sow_info
    assert sow_info["is_favorable"] is True


def test_daily_farm_plan_engine():
    plan = daily_farm_plan_engine.generate_daily_plan("Ginger", "2026-06-01", rain_probability_pct=15.0)
    assert plan["crop"] == "Ginger"
    assert len(plan["today_tasks"]) > 0
    assert "weather_summary" in plan


def test_weather_and_market_services():
    w = weather_service.get_current_weather("Hassan, Karnataka")
    assert "temperature_c" in w
    assert "rain_probability_pct" in w

    m = market_service.get_prices("Ginger")
    assert len(m) > 0
    assert m[0]["modal_price"] > 0

    sell_strat = selling_decision_engine.evaluate_selling_strategy("Ginger", 10.0)
    assert sell_strat["estimated_gross_revenue"] > 0


def test_farm_intelligence_authenticated_flow():
    # 1. Register test farmer
    ts = int(datetime.now().timestamp())
    identifier = f"farmer_intel_{ts}@test.com"
    reg_r = client.post("/api/auth/register", json={"identifier": identifier, "password": "password123"})
    assert reg_r.status_code == 200
    token = reg_r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Onboard Farm
    onboard_data = {
        "farmer": {"name": "Intel Farmer", "phone": "9876543210", "preferred_language": "English"},
        "farm": {"name": "Green Acre", "total_area": "4.5 acres", "location": "Hassan, Karnataka", "crop": "Ginger", "soil_type": "Loamy", "water_source": "Canal"}
    }
    ob_r = client.post("/api/farmer/onboard", json=onboard_data, headers=headers)
    assert ob_r.status_code == 200

    # 3. Fetch Farm Profile
    prof_r = client.get("/api/farms/profile", headers=headers)
    assert prof_r.status_code == 200
    prof_json = prof_r.json()
    assert prof_json["farmer"]["name"] == "Intel Farmer"
    assert prof_json["farm"]["crop"] == "Ginger"

    # 4. Log Farm Activity
    act_data = {
        "activity_type": "FERTILIZER",
        "activity_date": "2026-08-20",
        "description": "Applied 25kg NPK fertilizer to Ginger crop",
        "cost": 1250.0
    }
    act_r = client.post("/api/farms/activity", json=act_data, headers=headers)
    assert act_r.status_code == 200
    assert act_r.json()["status"] == "success"

    # 5. Fetch Farm History Timeline
    hist_r = client.get("/api/farms/timeline", headers=headers)
    assert hist_r.status_code == 200
    timeline = hist_r.json()
    assert len(timeline) >= 2 # Initial creation + logged activity

    # 6. Fetch Today's Farm Plan & Recommendations
    plan_r = client.get("/api/recommendations/today", headers=headers)
    assert plan_r.status_code == 200
    assert plan_r.json()["crop"] == "Ginger"

    rec_r = client.get("/api/recommendations/crops", headers=headers)
    assert rec_r.status_code == 200
    assert len(rec_r.json()["recommendations"]) >= 3

    # 7. Ask Saathi Chat Farm Memory History Questions
    chat_q1 = client.post("/api/chat", json={"message": "What did I plant last season?"}, headers=headers)
    assert chat_q1.status_code == 200
    assert "Ginger" in chat_q1.json()["answer"]

    chat_q2 = client.post("/api/chat", json={"message": "How much did I spend?"}, headers=headers)
    assert chat_q2.status_code == 200
    assert "1,250" in chat_q2.json()["answer"] or "Total Recorded Cost" in chat_q2.json()["answer"]
