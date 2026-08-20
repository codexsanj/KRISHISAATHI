import re
from typing import Dict, Any

class ScenarioParser:
    """Parses natural language What-If queries into structured scenario parameters."""
    def parse(self, query: str) -> Dict[str, Any]:
        q = query.lower()
        params = {
            "rainfall_change_pct": 0.0,
            "irrigation_change_pct": 0.0,
            "fertilizer_cost_change_pct": 0.0,
            "crop_change": None,
            "market_price_change_pct": 0.0,
            "area_change_acres": 0.0
        }

        # Rainfall change
        rain_match = re.search(r"rainfall\s+(decreases|falls|drops|reduces|increases|rises)?\s*by\s*(\d+)%", q)
        if rain_match:
            direction = rain_match.group(1) or "decreases"
            val = float(rain_match.group(2))
            params["rainfall_change_pct"] = -val if direction in ["decreases", "falls", "drops", "reduces"] else val

        # Irrigation change
        irr_match = re.search(r"irrigation\s+(is\s+)?(reduced|decreased|cut|increased)\s*by\s*(\d+)%", q)
        if irr_match:
            direction = irr_match.group(2)
            val = float(irr_match.group(3))
            params["irrigation_change_pct"] = -val if direction in ["reduced", "decreased", "cut"] else val

        # Fertilizer cost change
        fert_match = re.search(r"fertilizer\s*(cost|price)?\s*(increases|rises|grows|decreases)\s*by\s*(\d+)%", q)
        if fert_match:
            direction = fert_match.group(2)
            val = float(fert_match.group(3))
            params["fertilizer_cost_change_pct"] = val if direction in ["increases", "rises", "grows"] else -val

        # Crop change (e.g. "grow maize instead", "grow rice")
        if "grow maize" in q or "maize instead" in q:
            params["crop_change"] = "Maize"
        elif "grow rice" in q or "rice instead" in q:
            params["crop_change"] = "Rice"
        elif "grow cotton" in q or "cotton instead" in q:
            params["crop_change"] = "Cotton"

        # Market price change
        mkt_match = re.search(r"market\s*price\s*(falls|decreases|drops|rises|increases)\s*by\s*(\d+)%", q)
        if mkt_match:
            direction = mkt_match.group(1)
            val = float(mkt_match.group(2))
            params["market_price_change_pct"] = -val if direction in ["falls", "decreases", "drops"] else val

        return params

scenario_parser = ScenarioParser()
