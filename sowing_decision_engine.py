"""
Sowing Decision Engine

Determines optimal sowing window based on crop, location, season, soil, and weather forecast/rainfall.
"""

from typing import Dict, Any, Optional

class SowingDecisionEngine:
    @staticmethod
    def evaluate_sowing_window(
        crop_name: str,
        location: Optional[str] = None,
        season: Optional[str] = "Kharif",
        rainfall_forecast_mm: float = 12.0,
        temp_max_c: float = 30.0,
        soil_moisture_ok: bool = True
    ) -> Dict[str, Any]:
        c_clean = (crop_name or "Ginger").capitalize()

        # Decision Logic
        confidence = "High"
        is_favorable = True
        risk_notes = []

        if rainfall_forecast_mm > 50.0:
            is_favorable = False
            recommended_window = "Delay sowing by 5–7 days"
            reason = "Excess heavy rainfall (>50 mm) forecast may cause seed wash-out or waterlogging."
            risk_notes.append("Risk of seed/rhizome rotting due to water stagnation.")
            confidence = "Medium"
        elif temp_max_c > 38.0:
            is_favorable = False
            recommended_window = "Delay sowing until temperatures drop below 35°C"
            reason = "High surface temperature (>38°C) desiccates emerging seedlings."
            risk_notes.append("Heat stress damages delicate root tips.")
        else:
            recommended_window = "15 June – 05 July (Optimal Kharif Window)"
            reason = f"Current soil moisture and ambient temperature ({temp_max_c}°C) are favorable for {c_clean} germination."
            risk_notes.append("Ensure 30 cm raised beds for adequate field drainage.")

        return {
            "crop": c_clean,
            "season": season,
            "recommended_window": recommended_window,
            "is_favorable": is_favorable,
            "confidence": confidence,
            "reason": reason,
            "weather_risks": risk_notes,
            "optimal_conditions": {
                "soil_temp_range": "20°C – 32°C",
                "soil_moisture": "60–70% field capacity",
                "bed_type": "Raised beds (30 cm height)" if "ginger" in c_clean.lower() else "Ridges and furrows"
            }
        }

sowing_decision_engine = SowingDecisionEngine()
