from fastapi import APIRouter
from app.services.weather_service import weather_service
from app.services.market_service import market_service
from app.schemas.all_schemas import FarmSnapshotSchema

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard", response_model=FarmSnapshotSchema)
def get_dashboard_snapshot():
    weather = weather_service.get_weather()
    market = market_service.get_market_trends()
    return {
        "weather": {
            "value": f"{weather['temperature_c']:.0f}°C",
            "label": weather["condition"],
            "detail": weather["detail"]
        },
        "irrigation": {
            "value": "Due",
            "label": "North field",
            "detail": "Rain expected tomorrow"
        },
        "cropHealth": {
            "value": "Healthy",
            "label": "2 of 3 fields",
            "detail": "No major issues"
        },
        "market": {
            "value": market["crop"],
            "label": "+4.2%",
            "detail": "Nearby mandi prices"
        }
    }
