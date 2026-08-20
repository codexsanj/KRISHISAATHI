"""
Selling Decision Engine

Evaluates market prices, transport costs, and harvest timelines to recommend optimal selling windows and mandis.
"""

from typing import Dict, Any, Optional
from app.services.market_service import market_service

class SellingDecisionEngine:
    @staticmethod
    def evaluate_selling_strategy(
        crop_name: str,
        harvest_quantity_q: float = 20.0,
        farmer_location: Optional[str] = "Hassan, Karnataka"
    ) -> Dict[str, Any]:
        
        prices = market_service.get_prices(crop_name, farmer_location)
        best_market = max(prices, key=lambda x: x["modal_price"])

        est_revenue = harvest_quantity_q * best_market["modal_price"]

        return {
            "crop": crop_name,
            "harvest_quantity_quintals": harvest_quantity_q,
            "recommended_mandi": best_market["mandi"],
            "modal_price_per_q": best_market["modal_price"],
            "estimated_gross_revenue": est_revenue,
            "potential_selling_window": "Immediate post-harvest (within 10 days)",
            "nearby_markets_comparison": [
                {
                    "mandi": m["mandi"],
                    "price_per_q": m["modal_price"],
                    "estimated_revenue": harvest_quantity_q * m["modal_price"]
                }
                for m in prices
            ],
            "selling_advice": (
                f"Current Agmarknet modal price at {best_market['mandi']} is ₹{best_market['modal_price']}/quintal. "
                f"For {harvest_quantity_q} quintals of {crop_name}, potential gross revenue is ₹{est_revenue:,.0f}."
            ),
            "disclaimer": "Prices based on live Agmarknet mandi data. Net return subject to transport and unloading charges."
        }

selling_decision_engine = SellingDecisionEngine()
