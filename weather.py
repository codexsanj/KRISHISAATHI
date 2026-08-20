from fastapi import APIRouter, Query, Depends
from typing import Optional
from app.services.weather_service import weather_service
from app.api.routes.auth import get_current_user

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current")
def get_current_weather(location: Optional[str] = Query("Hassan, Karnataka")):
    return weather_service.get_current_weather(location)


@router.get("/forecast")
def get_forecast(location: Optional[str] = Query("Hassan, Karnataka")):
    current = weather_service.get_current_weather(location)
    return {
        "location": location,
        "current": current,
        "forecast": [
            {"day": "Today", "temp": f"{current['temperature_c']}°C", "condition": current["condition"], "rain_prob": f"{current['rain_probability_pct']:.0f}%"},
            {"day": "Tomorrow", "temp": "28°C", "condition": "Partly Sunny", "rain_prob": "30%"},
            {"day": "Day 3", "temp": "29°C", "condition": "Light Rain", "rain_prob": "55%"},
            {"day": "Day 4", "temp": "30°C", "condition": "Clear Sky", "rain_prob": "15%"},
            {"day": "Day 5", "temp": "28°C", "condition": "Partly Cloudy", "rain_prob": "25%"}
        ],
        "source": current.get("source")
    }


@router.get("/agromet")
def get_agromet_advisory(location: Optional[str] = Query("Hassan, Karnataka"), crop: Optional[str] = Query("Ginger")):
    return weather_service.get_agromet_advisory(location, crop)
