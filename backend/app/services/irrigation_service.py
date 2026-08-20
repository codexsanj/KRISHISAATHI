from typing import Dict, Any

class IrrigationDecisionEngine:
    """Deterministic Irrigation Decision Engine."""
    def evaluate(self, crop: str = "Wheat", soil_type: str = "Loamy", rain_prob: float = 60.0) -> Dict[str, Any]:
        if rain_prob >= 50.0:
            decision = "SKIP"
            what = "Hold irrigation for the north field today."
            when = "Reassess tomorrow morning after checking soil moisture."
            why = f"Rain is likely tomorrow ({rain_prob:.0f}% chance). Your {soil_type.lower()} soil retains moisture well — over-irrigation now could waterlog the roots."
        elif rain_prob >= 30.0:
            decision = "DELAY"
            what = "Delay planned irrigation until evening."
            when = "Check rain forecast again at 5 PM."
            why = "Moderate rainfall probability detected. Delaying saves water if cloud cover brings light showers."
        else:
            decision = "IRRIGATE"
            what = "Apply 25mm irrigation to your crop field."
            when = "Irrigate early morning between 6 AM and 9 AM."
            why = "No rain expected in the next 48 hours and crop evapotranspiration demand is high."

        return {
            "decision": decision,
            "what": what,
            "when": when,
            "why": why,
            "confidence": 0.95,
            "engine": "Deterministic Irrigation Decision Engine v1.0"
        }

irrigation_engine = IrrigationDecisionEngine()
