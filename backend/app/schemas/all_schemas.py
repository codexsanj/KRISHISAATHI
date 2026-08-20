from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

# Auth
class UserRegister(BaseModel):
    identifier: str
    password: str

class UserLogin(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    farmer: Optional[Dict[str, Any]] = None
    farm: Optional[Dict[str, Any]] = None

# Farmer & Farm
class FarmerBase(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_language: Optional[str] = "Hindi"

class FarmBase(BaseModel):
    name: str
    total_area: Optional[str] = None
    area: Optional[str] = None
    crop: Optional[str] = None
    location: Optional[str] = None
    soil_type: Optional[str] = None
    water_source: Optional[str] = None
    waterSource: Optional[str] = None
    status: Optional[str] = "Healthy"

class OnboardingRequest(BaseModel):
    farmer: FarmerBase
    farm: FarmBase

# Advisory & Snapshots
class PriorityActionSchema(BaseModel):
    iconLabel: str
    title: str
    dueLabel: str
    what: str
    when: str
    why: str
    ctaLabel: Optional[str] = "View recommendation"

class FarmSnapshotSchema(BaseModel):
    weather: Dict[str, str]
    irrigation: Dict[str, str]
    cropHealth: Dict[str, str]
    market: Dict[str, str]

class AlertSchema(BaseModel):
    id: str
    type: str
    title: str
    description: str
    is_read: Optional[bool] = False

# Chat & Simulation
class ChatRequest(BaseModel):
    message: str
    farm_id: Optional[int] = None
    session_id: Optional[int] = None

class StructuredResponse(BaseModel):
    what: Optional[str] = None
    when: Optional[str] = None
    why: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    message: Optional[str] = None
    intent: Optional[str] = "GENERAL_AGRICULTURE"
    structured: Optional[StructuredResponse] = None
    confidence: float = 0.95
    sources: List[str] = []
    actions: List[Dict[str, Any]] = []
    what: Optional[str] = None
    when: Optional[str] = None
    why: Optional[str] = None
    requires_expert: bool = False
    is_what_if: bool = False
    session_id: Optional[int] = None
    simulation: Optional[Dict[str, Any]] = None

class SimulationRequest(BaseModel):
    query: str
    farm_id: Optional[int] = None

class SimulationResponse(BaseModel):
    parsed_params: Dict[str, Any]
    current_state: Dict[str, Any]
    simulated_state: Dict[str, Any]
    deltas: Dict[str, Any]
    explanation: str
    structured: StructuredResponse

# Health & Disease
class DiseaseDetectResponse(BaseModel):
    status: Optional[str] = "success"
    request_id: Optional[str] = None
    image_hash: Optional[str] = None
    crop: Optional[str] = None
    prediction: str
    confidence: float
    display_title: Optional[str] = None
    prediction_details: Optional[Dict[str, Any]] = None
    alternatives: Optional[List[Dict[str, Any]]] = None
    severity: str
    symptoms: Optional[str] = None
    what: str
    when: str
    why: str
    prevention: Optional[str] = None
    management: Optional[str] = None
    when_to_escalate: Optional[str] = None
    possible_causes: Optional[List[str]] = None
    recommended_action: Optional[str] = None
    requires_expert: bool = False
    model_version: Optional[str] = None
    supported_classes: Optional[List[str]] = None
    is_fallback: Optional[bool] = False
    image_url: Optional[str] = None
    sources: Optional[List[str]] = None

class PestRiskResponse(BaseModel):
    risk_level: str
    pest_type: str
    probability: float
    title: str
    description: str
    engine: Optional[str] = None


class PestDetection(BaseModel):
    pest_class: str = ""
    confidence: float = 0.0
    bbox: Optional[List[float]] = None


class PestDetectResponse(BaseModel):
    status: str  # "success" | "model_unavailable" | "error"
    message: Optional[str] = None
    detections: List[PestDetection] = []
    model: Optional[str] = None
    model_version: Optional[str] = None
    supported_classes: Optional[List[str]] = None
    crop: Optional[str] = None

# Market
class MarketItemSchema(BaseModel):
    crop: str
    mandi: str
    price_per_quintal: float
    date: str
    trend_pct: float
    trend_direction: str

class MarketTrendSchema(BaseModel):
    crop: str
    recommendation: str
    best_window: str
    price_trend: str
    forecast: str

# Expert
class ExpertCaseCreate(BaseModel):
    crop: str
    issue_description: str
    image_url: Optional[str] = None

class ExpertCaseResponse(BaseModel):
    case_id: str
    status: str
    assigned_to: str
    message: str

# Farm Activity & Memory Schemas
class FarmActivityCreate(BaseModel):
    crop_cycle_id: Optional[int] = None
    field_id: Optional[int] = None
    activity_type: str # LAND_PREPARATION, SEEDING, IRRIGATION, FERTILIZER, PEST_INSPECTION, DISEASE_DETECTED, HARVEST, SALE, EXPENSE, etc.
    activity_date: str # YYYY-MM-DD
    activity_time: Optional[str] = None
    description: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    cost: Optional[float] = 0.0
    notes: Optional[str] = None
    image_reference: Optional[str] = None

class FarmActivityResponse(BaseModel):
    id: int
    farmer_id: int
    farm_id: int
    field_id: Optional[int] = None
    crop_cycle_id: Optional[int] = None
    activity_type: str
    activity_date: str
    activity_time: Optional[str] = None
    description: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    cost: Optional[float] = 0.0
    notes: Optional[str] = None
    image_reference: Optional[str] = None
    weather_snapshot: Optional[Dict[str, Any]] = None
    created_at: Any

class CropCycleCreate(BaseModel):
    field_id: Optional[int] = None
    crop_name: str
    variety: Optional[str] = None
    area_acres: Optional[float] = 1.0
    sowing_date: Optional[str] = None
    season: Optional[str] = None
    previous_crop: Optional[str] = None
    notes: Optional[str] = None

class CropCycleResponse(BaseModel):
    id: int
    farmer_id: int
    farm_id: int
    field_id: Optional[int] = None
    crop_name: str
    variety: Optional[str] = None
    area_acres: float
    sowing_date: Optional[str] = None
    expected_harvest_date: Optional[str] = None
    current_stage: str
    status: str
    season: Optional[str] = None
    previous_crop: Optional[str] = None
    crop_age_days: Optional[int] = 0
    created_at: Any

class ExpenseCreate(BaseModel):
    crop_cycle_id: Optional[int] = None
    category: str # SEED, FERTILIZER, PESTICIDE, LABOUR, IRRIGATION, EQUIPMENT, TRANSPORT, OTHER
    amount: float
    expense_date: str
    description: str

class SaleCreate(BaseModel):
    crop_cycle_id: Optional[int] = None
    harvest_record_id: Optional[int] = None
    sale_date: str
    buyer_type: Optional[str] = "Mandi Trader"
    mandi_name: Optional[str] = None
    quantity_sold: float
    price_per_unit: float
    transport_cost: Optional[float] = 0.0
    notes: Optional[str] = None

class FarmProfitSummary(BaseModel):
    crop_name: str
    total_recorded_cost: float
    total_revenue: float
    gross_return: float
    net_profit: float
    expense_breakdown: Dict[str, float]
    is_estimated: bool = False

class DailyPlanTask(BaseModel):
    task: str
    reason: str
    priority: str # High, Medium, Low
    category: str # Irrigation, Pest, Fertilizer, Inspection, General
    recommended_date: str
    rule_source: str

class DailyPlanResponse(BaseModel):
    crop: str
    crop_age_days: int
    current_stage: str
    today_tasks: List[DailyPlanTask]
    next_3_days_tasks: List[DailyPlanTask]
    next_7_days_tasks: List[DailyPlanTask]
    weather_summary: str
    irrigation_advice: str
    pest_risk_status: str

class CropRecommendationItem(BaseModel):
    crop: str
    suitability_score: int
    reasons: List[str]
    risks: List[str]
    expected_season: str
    expected_sowing_window: str
    water_requirement: str
    market_outlook: str

