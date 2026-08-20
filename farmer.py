from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.all_models import Farmer, Farm, Field
from app.schemas.all_schemas import OnboardingRequest, FarmerBase

router = APIRouter(prefix="/farmer", tags=["farmer"])

@router.post("/onboard")
def onboard(req: OnboardingRequest, auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        farmer = Farmer(user_id=user.id)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)

    if req.farmer.name:
        farmer.name = req.farmer.name
    if req.farmer.phone:
        farmer.phone = req.farmer.phone
    db.commit()

    farm_area = req.farm.area or req.farm.total_area or "2.5 acres"
    water_src = req.farm.waterSource or req.farm.water_source or "Canal irrigation"

    # Create or update farm
    existing_farm = db.query(Farm).filter(Farm.farmer_id == farmer.id).first()
    if not existing_farm:
        existing_farm = Farm(
            farmer_id=farmer.id,
            name=req.farm.name or "My Farm",
            total_area=farm_area,
            location=req.farm.location,
            soil_type=req.farm.soil_type,
            water_source=water_src,
            current_crop=req.farm.crop,
            status="Healthy"
        )
        db.add(existing_farm)
    else:
        existing_farm.name = req.farm.name or existing_farm.name
        existing_farm.total_area = farm_area or existing_farm.total_area
        existing_farm.location = req.farm.location or existing_farm.location
        existing_farm.soil_type = req.farm.soil_type or existing_farm.soil_type
        existing_farm.water_source = water_src or existing_farm.water_source
        existing_farm.current_crop = req.farm.crop or existing_farm.current_crop

    db.commit()
    db.refresh(existing_farm)

    # Ensure field memory entry exists
    field = db.query(Field).filter(Field.farm_id == existing_farm.id).first()
    if not field:
        field = Field(farm_id=existing_farm.id, name="Main Field", current_crop=existing_farm.current_crop)
        db.add(field)
        db.commit()
        db.refresh(field)

    # Ensure active CropCycle exists in Farm Memory
    from app.models.all_models import CropCycle, FarmActivity
    from datetime import datetime
    active_cycle = db.query(CropCycle).filter(CropCycle.farmer_id == farmer.id, CropCycle.status == "ACTIVE").first()
    if not active_cycle and existing_farm.current_crop:
        active_cycle = CropCycle(
            farmer_id=farmer.id,
            farm_id=existing_farm.id,
            field_id=field.id,
            crop_name=existing_farm.current_crop,
            sowing_date=datetime.now().strftime("%Y-%m-%d"),
            current_stage="Vegetative",
            status="ACTIVE"
        )
        db.add(active_cycle)

    # Log initial onboarding activity
    existing_act = db.query(FarmActivity).filter(FarmActivity.farmer_id == farmer.id).first()
    if not existing_act:
        init_act = FarmActivity(
            farmer_id=farmer.id,
            farm_id=existing_farm.id,
            field_id=field.id,
            activity_type="LAND_PREPARATION",
            activity_date=datetime.now().strftime("%Y-%m-%d"),
            description=f"Onboarded farm and prepared land for {existing_farm.current_crop} cultivation."
        )
        db.add(init_act)

    db.commit()

    return {
        "success": True,
        "farmer": {"id": farmer.id, "name": farmer.name, "phone": farmer.phone},
        "farm": {
            "id": existing_farm.id,
            "name": existing_farm.name,
            "crop": existing_farm.current_crop,
            "area": existing_farm.total_area,
            "location": existing_farm.location,
            "soil": existing_farm.soil_type,
            "waterSource": existing_farm.water_source,
            "status": existing_farm.status
        }
    }

@router.get("/profile")
def get_profile(auth_data = Depends(get_current_user)):
    user, farmer = auth_data
    return {
        "farmer": {"id": farmer.id if farmer else None, "name": farmer.name if farmer else None, "phone": farmer.phone if farmer else None}
    }

@router.put("/profile")
def update_profile(req: FarmerBase, auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        farmer = Farmer(user_id=user.id)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)

    if req.name:
        farmer.name = req.name
    if req.phone:
        farmer.phone = req.phone
    if req.preferred_language:
        farmer.preferred_language = req.preferred_language
    db.commit()
    db.refresh(farmer)

    return {
        "success": True,
        "farmer": {"id": farmer.id, "name": farmer.name, "phone": farmer.phone, "email": farmer.email, "preferred_language": farmer.preferred_language}
    }

