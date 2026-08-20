from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.simulation.scenario_parser import scenario_parser
from app.simulation.farm_state import farm_state_manager

class SimulationEngine:
    """Natural language What-If simulation orchestrator."""
    def run_simulation(self, db: Session, query: str, farm_id: Optional[int] = None) -> Dict[str, Any]:
        params = scenario_parser.parse(query)
        baseline = farm_state_manager.get_baseline_state(db, farm_id)
        simulated = farm_state_manager.create_simulated_state(baseline, params)

        # Calculate deltas
        yield_delta_pct = round(((simulated["yield_q_per_acre"] - baseline["yield_q_per_acre"]) / baseline["yield_q_per_acre"]) * 100.0, 1)
        profit_delta_inr = round(simulated["profit_inr"] - baseline["profit_inr"], 2)
        profit_delta_pct = round((profit_delta_inr / baseline["profit_inr"]) * 100.0, 1) if baseline["profit_inr"] else 0.0
        water_delta_pct = round(((simulated["water_req_mm"] - baseline["water_req_mm"]) / baseline["water_req_mm"]) * 100.0, 1)

        deltas = {
            "yield_change_pct": yield_delta_pct,
            "profit_change_inr": profit_delta_inr,
            "profit_change_pct": profit_delta_pct,
            "water_change_pct": water_delta_pct
        }

        # Formulate structured explanation
        if profit_delta_inr < 0:
            what = f"Expected yield changes by {yield_delta_pct}% ({simulated['yield_q_per_acre']} q/acre) and overall profit decreases by ₹{abs(profit_delta_inr):,.0f} ({profit_delta_pct}%)."
            when = "Re-evaluate water and fertilizer management before skipping planned irrigation schedules."
            why = "Water reduction combined with input price increases places moisture and financial stress on the crop during critical growth phases."
        elif params.get("crop_change"):
            what = f"Switching to {simulated['crop']} changes yield to {simulated['yield_q_per_acre']} q/acre with projected net profit of ₹{simulated['profit_inr']:,.0f}."
            when = "Plan crop rotation prior to the upcoming sowing season window."
            why = f"Different market prices (₹{simulated['market_price_per_q']}/q) and input requirements shift total revenue and profitability."
        else:
            what = f"Yield increases by {yield_delta_pct}% with positive net return of ₹{profit_delta_inr:,.0f}."
            when = "Maintain regular input schedules."
            why = "Favorable scenario conditions support optimal crop development."

        explanation = f"WHAT: {what}\nWHEN: {when}\nWHY: {why}"

        return {
            "query": query,
            "parsed_params": params,
            "current_state": baseline,
            "simulated_state": simulated,
            "deltas": deltas,
            "explanation": explanation,
            "structured": {
                "what": what,
                "when": when,
                "why": why
            }
        }

simulation_engine = SimulationEngine()
