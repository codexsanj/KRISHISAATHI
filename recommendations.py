from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.ai.farm_intelligence.crop_recommendation_engine import crop_recommendation_engine
from app.ai.farm_intelligence.daily_farm_plan_engine import daily_farm_plan_engine
from app.ai.farm_intelligence.sowing_decision_engine import sowing_decision_engine
from app.services.weather_service import weather_service
from app.models.all_models import CropCycle

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/crops")
def get_crop_recommendations(
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, farmer = auth_data
    farm = farmer.farms[0] if (farmer and farmer.farms) else None

    location = farm.location if farm else "Hassan, Karnataka"
    soil = farm.soil_type if farm else "Loamy"
    water = farm.water_source if farm else "Irrigation"

    recs = crop_recommendation_engine.get_recommendations(
        location=location,
        soil_type=soil,
        water_source=water
    )
    return {
        "location": location,
        "soil_type": soil,
        "recommendations": recs
    }


@router.get("/today")
def get_today_farm_plan(
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, farmer = auth_data
    farm = farmer.farms[0] if (farmer and farmer.farms) else None
    active_cycle = db.query(CropCycle).filter(CropCycle.farmer_id == farmer.id, CropCycle.status == "ACTIVE").first() if farmer else None

    crop_name = farm.current_crop if farm else "Ginger"
    sowing_date = active_cycle.sowing_date if active_cycle else None
    location = farm.location if farm else "Hassan, Karnataka"

    weather = weather_service.get_current_weather(location)
    plan = daily_farm_plan_engine.generate_daily_plan(
        crop_name=crop_name,
        sowing_date=sowing_date,
        rain_probability_pct=weather.get("rain_probability_pct", 20.0),
        temp_c=weather.get("temperature_c", 27.0)
    )
    return plan


@router.get("/sowing")
def get_sowing_recommendation(
    crop: Optional[str] = "Ginger",
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, farmer = auth_data
    farm = farmer.farms[0] if (farmer and farmer.farms) else None
    location = farm.location if farm else "Hassan, Karnataka"

    weather = weather_service.get_current_weather(location)
    sow_info = sowing_decision_engine.evaluate_sowing_window(
        crop_name=crop,
        location=location,
        rainfall_forecast_mm=weather.get("rainfall_mm", 0.0),
        temp_max_c=weather.get("temperature_c", 28.0)
    )
    return sow_info
