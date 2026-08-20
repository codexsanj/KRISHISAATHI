from fastapi import APIRouter
from app.schemas.all_schemas import PriorityActionSchema

router = APIRouter(prefix="/advisory", tags=["advisory"])

@router.get("/today", response_model=PriorityActionSchema)
def get_today_priority_advisory():
    return {
        "iconLabel": "Pest risk",
        "title": "Apply neem spray to cotton field",
        "dueLabel": "Due by 4 PM",
        "what": "Spray neem oil solution on affected leaves in the north field.",
        "when": "Today before 4 PM — avoid midday heat for best absorption.",
        "why": "Early pest signs detected on cotton leaves; treatment now prevents spread to adjacent crops.",
        "ctaLabel": "View recommendation"
    }
