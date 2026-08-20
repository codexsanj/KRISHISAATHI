from fastapi import APIRouter, Query, UploadFile, File, Form, HTTPException
from typing import Optional
from app.ai.pest_risk.pest_engine import pest_engine
from app.schemas.all_schemas import PestRiskResponse

router = APIRouter(prefix="/pest", tags=["pest"])

# ── GET /api/pest/risk — statistical risk assessment ──────────────────────────
@router.get("/risk", response_model=PestRiskResponse)
def get_pest_risk(
    crop: str = Query("Cotton"),
    temp: float = Query(32.0),
    humidity: float = Query(65.0)
):
    return pest_engine.predict_risk(crop, temp, humidity)


# ── POST /api/pest/detect — image-based pest detection ────────────────────────
@router.post("/detect")
async def detect_pest_from_image(
    file: UploadFile = File(...),
    crop: Optional[str] = Form(None)
):
    """
    Accept a JPEG/PNG/WebP leaf/crop photo and run YOLO-based pest detection.

    - If the model is available:  returns detections with class, confidence, bbox.
    - If the model is unavailable: returns status='model_unavailable' with an honest message.
    - If the file is invalid:      returns HTTP 422 with a clear error message.
    """
    # Validate content type
    allowed_types = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
    ct = (file.content_type or "").lower()
    if ct not in allowed_types:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: '{file.content_type}'. "
                   f"Please upload a JPEG, PNG, or WebP image."
        )

    # Read and validate file size (max 10 MB)
    image_bytes = await file.read()
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > 10.0:
        raise HTTPException(
            status_code=422,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed size is 10 MB."
        )
    if len(image_bytes) < 512:
        raise HTTPException(
            status_code=422,
            detail="The uploaded file appears to be empty or corrupt."
        )

    # Run detection engine
    result = pest_engine.analyze_image(image_bytes, crop=crop)
    return result
