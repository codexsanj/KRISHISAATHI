from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.all_models import Farm, Field, FarmActivity, CropCycle, ExpenseRecord, SaleRecord, HarvestRecord
from app.schemas.all_schemas import FarmBase, FarmActivityCreate, CropCycleCreate, ExpenseCreate, SaleCreate
from app.ai.farm_intelligence.crop_lifecycle_engine import crop_lifecycle_engine
from app.ai.farm_intelligence.farm_profit_engine import farm_profit_engine
from app.services.weather_service import weather_service

router = APIRouter(prefix="/farms", tags=["farm"])


@router.get("")
def get_farms(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return []
    farms = db.query(Farm).filter(Farm.farmer_id == farmer.id).all()
    return [
        {
            "id": f.id,
            "name": f.name,
            "crop": f.current_crop,
            "area": f.total_area,
            "location": f.location,
            "soil": f.soil_type,
            "waterSource": f.water_source,
            "status": f.status
        } for f in farms
    ]


@router.post("")
def create_farm(req: FarmBase, auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    farm = Farm(
        farmer_id=farmer.id,
        name=req.name,
        total_area=req.total_area or req.area or "2.5 acres",
        location=req.location or "Hassan, Karnataka",
        soil_type=req.soil_type or "Loamy",
        water_source=req.water_source or req.waterSource or "Canal irrigation",
        current_crop=req.crop or "Ginger",
        status="Healthy"
    )
    db.add(farm)
    db.commit()
    db.refresh(farm)
    
    # Create default field
    field = Field(farm_id=farm.id, name="Main Field", current_crop=farm.current_crop)
    db.add(field)
    db.commit()
    db.refresh(field)

    # Automatically create initial crop cycle
    crop_cycle = CropCycle(
        farmer_id=farmer.id,
        farm_id=farm.id,
        field_id=field.id,
        crop_name=farm.current_crop,
        sowing_date=datetime.now().strftime("%Y-%m-%d"),
        current_stage="Vegetative",
        status="ACTIVE"
    )
    db.add(crop_cycle)

    # Automatically log initial LAND_PREPARATION activity
    act = FarmActivity(
        farmer_id=farmer.id,
        farm_id=farm.id,
        field_id=field.id,
        activity_type="LAND_PREPARATION",
        activity_date=datetime.now().strftime("%Y-%m-%d"),
        description=f"Farm created and land prepared for {farm.current_crop} cultivation."
    )
    db.add(act)
    db.commit()

    return {
        "id": farm.id,
        "name": farm.name,
        "crop": farm.current_crop,
        "area": farm.total_area,
        "location": farm.location,
        "soil": farm.soil_type,
        "waterSource": farm.water_source,
        "status": farm.status
    }


@router.get("/profile")
def get_farm_profile(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return {"farmer": None, "farm": None}

    farm = db.query(Farm).filter(Farm.farmer_id == farmer.id).first()
    active_cycle = db.query(CropCycle).filter(CropCycle.farmer_id == farmer.id, CropCycle.status == "ACTIVE").first() if farmer else None

    lifecycle_info = None
    if farm and farm.current_crop:
        s_date = active_cycle.sowing_date if active_cycle else None
        lifecycle_info = crop_lifecycle_engine.get_lifecycle_info(farm.current_crop, s_date)

    return {
        "farmer": {
            "id": farmer.id,
            "name": farmer.name,
            "phone": farmer.phone,
            "email": farmer.email,
            "preferred_language": farmer.preferred_language
        },
        "farm": {
            "id": farm.id if farm else None,
            "name": farm.name if farm else None,
            "crop": farm.current_crop if farm else None,
            "area": farm.total_area if farm else None,
            "location": farm.location if farm else None,
            "soil_type": farm.soil_type if farm else None,
            "water_source": farm.water_source if farm else None,
            "status": farm.status if farm else "Healthy"
        } if farm else None,
        "crop_cycle": {
            "id": active_cycle.id if active_cycle else None,
            "crop_name": active_cycle.crop_name if active_cycle else (farm.current_crop if farm else None),
            "sowing_date": active_cycle.sowing_date if active_cycle else None,
            "current_stage": lifecycle_info["current_stage"] if lifecycle_info else "Vegetative",
            "crop_age_days": lifecycle_info["crop_age_days"] if lifecycle_info else 30,
            "harvest_window": lifecycle_info["harvest_window"] if lifecycle_info else "N/A"
        } if (active_cycle or (farm and farm.current_crop)) else None
    }


@router.get("/timeline")
@router.get("/history")
def get_farm_timeline(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return []

    activities = db.query(FarmActivity).filter(FarmActivity.farmer_id == farmer.id).order_by(FarmActivity.activity_date.desc(), FarmActivity.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "activity_type": a.activity_type,
            "date": a.activity_date,
            "description": a.description,
            "quantity": a.quantity,
            "unit": a.unit,
            "cost": a.cost,
            "notes": a.notes,
            "weather_snapshot": a.weather_snapshot,
            "created_at": a.created_at.isoformat()
        } for a in activities
    ]


@router.post("/activity")
def log_farm_activity(req: FarmActivityCreate, auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        raise HTTPException(status_code=401, detail="Authentication required")

    farm = db.query(Farm).filter(Farm.farmer_id == farmer.id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm profile not found")

    w_snapshot = weather_service.get_current_weather(farm.location)

    act = FarmActivity(
        farmer_id=farmer.id,
        farm_id=farm.id,
        field_id=req.field_id,
        crop_cycle_id=req.crop_cycle_id,
        activity_type=req.activity_type.upper(),
        activity_date=req.activity_date or datetime.now().strftime("%Y-%m-%d"),
        activity_time=req.activity_time or datetime.now().strftime("%H:%M"),
        description=req.description,
        quantity=req.quantity,
        unit=req.unit,
        cost=req.cost or 0.0,
        notes=req.notes,
        image_reference=req.image_reference,
        weather_snapshot=w_snapshot
    )
    db.add(act)

    # If activity includes a cost > 0, log an expense record
    if req.cost and req.cost > 0:
        exp = ExpenseRecord(
            farmer_id=farmer.id,
            farm_id=farm.id,
            crop_cycle_id=req.crop_cycle_id,
            category=req.activity_type,
            amount=req.cost,
            expense_date=req.activity_date,
            description=f"Activity cost: {req.description}"
        )
        db.add(exp)

    db.commit()
    db.refresh(act)

    return {
        "id": act.id,
        "status": "success",
        "activity_type": act.activity_type,
        "date": act.activity_date,
        "description": act.description
    }


@router.get("/analytics")
def get_farm_analytics(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return {"total_activities": 0, "profit_summary": None}

    total_acts = db.query(FarmActivity).filter(FarmActivity.farmer_id == farmer.id).count()
    crop_cycles = db.query(CropCycle).filter(CropCycle.farmer_id == farmer.id).all()
    profit_summary = farm_profit_engine.compute_farm_profit(db, farmer.id)

    return {
        "total_activities": total_acts,
        "total_crop_cycles": len(crop_cycles),
        "profit_summary": profit_summary,
        "crop_cycles": [
            {
                "id": c.id,
                "crop_name": c.crop_name,
                "sowing_date": c.sowing_date,
                "current_stage": c.current_stage,
                "status": c.status
            } for c in crop_cycles
        ]
    }
