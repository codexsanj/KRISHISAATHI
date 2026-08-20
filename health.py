from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.ai.disease_detection.disease_engine import disease_engine
from app.models.all_models import ExpertCase

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/disease-model")
async def get_disease_model_info() -> Dict[str, Any]:
    """
    Returns model availability, name, version, supported crops, supported
    diseases, class count, confidence thresholds, and preprocessing metadata.
    No authentication required — public endpoint for UI diagnostics.
    """
    return disease_engine.get_model_info()


@router.post("/disease-detect")
async def detect_disease(
    file: UploadFile = File(...),
    crop: Optional[str] = Form(None),
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    POST /api/health/disease-detect

    Runs the PyTorch crop disease classifier on the uploaded image.
    - Applies crop-aware class isolation (only classes for the specified crop
      are evaluated; cross-crop results are masked).
    - Returns top-1 prediction + top-2/3 alternatives with real model probabilities.
    - Confidence-gated treatment: chemical recommendations only shown >= 0.70.
    - Auto-logs expert escalation case for low-confidence uploads.
    """
    user, farmer = auth_data
    content = await file.read()

    result = disease_engine.analyze_image(
        image_bytes=content,
        crop=crop,
        filename=file.filename,
        content_type=file.content_type,
    )

    # Auto-escalate to expert queue for low/medium confidence or explicit requires_expert
    if result.get("requires_expert") and farmer:
        try:
            expert_case = ExpertCase(
                farmer_id=farmer.id,
                crop=crop or result.get("crop", "Unknown Crop"),
                issue_description=(
                    f"AI diagnosis status='{result.get('status')}' "
                    f"confidence={result.get('confidence', 0):.2f} "
                    f"prediction='{result.get('prediction')}' "
                    f"request_id='{result.get('request_id')}'"
                ),
                confidence=result.get("confidence", 0.0),
                status="OPEN",
            )
            db.add(expert_case)
            db.commit()
        except Exception:
            db.rollback()  # never let DB errors break the main response

    return result
