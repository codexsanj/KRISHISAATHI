from fastapi import APIRouter, Query
from app.services.irrigation_service import irrigation_engine

router = APIRouter(prefix="/irrigation", tags=["irrigation"])

@router.get("/advisory")
def get_irrigation_advisory(crop: str = Query("Wheat"), soil: str = Query("Loamy"), rain_prob: float = Query(60.0)):
    return irrigation_engine.evaluate(crop, soil, rain_prob)
