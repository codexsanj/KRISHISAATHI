from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.all_models import ExpertCase
from app.schemas.all_schemas import ExpertCaseCreate, ExpertCaseResponse

router = APIRouter(prefix="/expert", tags=["expert"])

@router.post("/cases", response_model=ExpertCaseResponse)
def create_expert_case(
    req: ExpertCaseCreate,
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, farmer = auth_data
    case = ExpertCase(
        farmer_id=farmer.id if farmer else 1,
        crop=req.crop,
        issue_description=req.issue_description,
        image_url=req.image_url,
        confidence=0.45,
        status="OPEN"
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    return {
        "case_id": f"EXP-{case.id}",
        "status": "Escalated",
        "assigned_to": "KVK Senior Agronomist",
        "message": "Your case has been successfully escalated to an agricultural expert. You will receive advice via notification within 4 hours."
    }

@router.get("/cases")
def list_expert_cases(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return []
    cases = db.query(ExpertCase).filter(ExpertCase.farmer_id == farmer.id).all()
    return [
        {
            "case_id": f"EXP-{c.id}",
            "crop": c.crop,
            "issue": c.issue_description,
            "status": c.status,
            "response": c.expert_response,
            "created_at": c.created_at.isoformat()
        } for c in cases
    ]
