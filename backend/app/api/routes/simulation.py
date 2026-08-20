from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.simulation.simulation_engine import simulation_engine
from app.schemas.all_schemas import SimulationRequest, SimulationResponse
from app.models.all_models import SimulationResult

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.post("", response_model=SimulationResponse)
def run_simulation(
    req: SimulationRequest,
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, farmer = auth_data
    result = simulation_engine.run_simulation(db, req.query, req.farm_id)

    if farmer:
        sim_rec = SimulationResult(
            farmer_id=farmer.id,
            query=req.query,
            parsed_params=result["parsed_params"],
            baseline_state=result["current_state"],
            simulated_state=result["simulated_state"],
            explanation=result["explanation"]
        )
        db.add(sim_rec)
        db.commit()

    return result

@router.get("/history")
def get_simulation_history(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return []
    sims = db.query(SimulationResult).filter(SimulationResult.farmer_id == farmer.id).order_by(SimulationResult.created_at.desc()).all()
    return [
        {
            "id": s.id,
            "query": s.query,
            "parsed_params": s.parsed_params,
            "deltas": s.simulated_state,
            "explanation": s.explanation,
            "created_at": s.created_at.isoformat()
        } for s in sims
    ]
