from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.all_models import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
def get_alerts(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if farmer:
        alerts = db.query(Alert).filter(Alert.farmer_id == farmer.id).all()
        if alerts:
            return [{"id": str(a.id), "type": a.alert_type, "title": a.title, "description": a.description} for a in alerts]

    # Baseline demo alerts
    return [
        {
            "id": "1",
            "type": "weather",
            "title": "Rain advisory",
            "description": "Light showers expected tomorrow — delay fertilizer application."
        },
        {
            "id": "2",
            "type": "pest",
            "title": "Pest activity rising",
            "description": "Regional cotton pest risk is moderate this week."
        }
    ]
