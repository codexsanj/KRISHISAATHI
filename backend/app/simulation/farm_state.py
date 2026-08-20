import copy
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.all_models import Farm

class FarmStateManager:
    """Manages baseline farm state and creates transient cloned copies for What-If simulations."""
    def get_baseline_state(self, db: Session, farm_id: Optional[int] = None) -> Dict[str, Any]:
        farm = None
        if farm_id:
            farm = db.query(Farm).filter(Farm.id == farm_id).first()

        if farm:
            return {
                "farm_id": farm.id,
                "crop": farm.current_crop or "Wheat",
                "area_acres": 2.5,
                "soil": farm.soil_type or "Loamy",
                "water_source": farm.water_source or "Canal irrigation",
                "yield_q_per_acre": 18.5,
                "water_req_mm": 450.0,
                "pest_risk": "Low",
                "input_cost_inr": 12000.0,
                "revenue_inr": 41625.0, # 18.5 * 2.5 * 900
                "profit_inr": 29625.0,
                "market_price_per_q": 2250.0
            }

        # Default fallback baseline for demo
        return {
            "farm_id": 1,
            "crop": "Wheat",
            "area_acres": 2.5,
            "soil": "Loamy",
            "water_source": "Canal irrigation",
            "yield_q_per_acre": 18.5,
            "water_req_mm": 450.0,
            "pest_risk": "Low",
            "input_cost_inr": 12000.0,
            "revenue_inr": 41625.0,
            "profit_inr": 29625.0,
            "market_price_per_q": 2250.0
        }

    def create_simulated_state(self, baseline: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        simulated = copy.deepcopy(baseline)
        
        # Crop Change
        if params.get("crop_change"):
            simulated["crop"] = params["crop_change"]
            if params["crop_change"] == "Maize":
                simulated["yield_q_per_acre"] = 22.0
                simulated["water_req_mm"] = 500.0
                simulated["market_price_per_q"] = 1950.0
                simulated["input_cost_inr"] = 11000.0
            elif params["crop_change"] == "Cotton":
                simulated["yield_q_per_acre"] = 12.0
                simulated["water_req_mm"] = 650.0
                simulated["market_price_per_q"] = 6420.0
                simulated["input_cost_inr"] = 18000.0

        # Rainfall & Irrigation impact on yield
        rain_delta = params.get("rainfall_change_pct", 0.0)
        irr_delta = params.get("irrigation_change_pct", 0.0)
        total_water_delta = rain_delta * 0.4 + irr_delta * 0.6

        if total_water_delta < 0:
            yield_impact_pct = total_water_delta * 0.6 # e.g. -20% water -> -12% yield
            simulated["yield_q_per_acre"] = round(simulated["yield_q_per_acre"] * (1 + yield_impact_pct / 100.0), 2)
            simulated["pest_risk"] = "Moderate" if total_water_delta < -15 else "Low"
        elif total_water_delta > 0:
            simulated["yield_q_per_acre"] = round(simulated["yield_q_per_acre"] * 1.05, 2)

        # Water requirement
        simulated["water_req_mm"] = round(simulated["water_req_mm"] * (1 + irr_delta / 100.0), 1)

        # Input cost impact
        fert_delta = params.get("fertilizer_cost_change_pct", 0.0)
        simulated["input_cost_inr"] = round(simulated["input_cost_inr"] * (1 + fert_delta / 100.0), 2)

        # Market price impact
        price_delta = params.get("market_price_change_pct", 0.0)
        if price_delta != 0:
            simulated["market_price_per_q"] = round(simulated["market_price_per_q"] * (1 + price_delta / 100.0), 2)

        # Recalculate financial outcomes
        total_yield_q = simulated["yield_q_per_acre"] * simulated["area_acres"]
        simulated["revenue_inr"] = round(total_yield_q * simulated["market_price_per_q"], 2)
        simulated["profit_inr"] = round(simulated["revenue_inr"] - simulated["input_cost_inr"], 2)

        return simulated

farm_state_manager = FarmStateManager()
