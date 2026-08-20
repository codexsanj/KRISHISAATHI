"""
Smart Crop Recommendation Engine

Calculates transparent suitability scores for crops based on multi-factor scoring:
- Location / District / State suitability
- Soil type & pH match
- Season suitability (Kharif, Rabi, Zaid)
- Water availability & source
- Historical crop rotation
- Market outlook & regional prevalence
"""

from typing import Dict, Any, List, Optional

RECOMMENDABLE_CROPS: List[Dict[str, Any]] = [
    {
        "crop": "Ragi (Finger Millet)",
        "base_score": 85,
        "ideal_seasons": ["Kharif", "Late Kharif"],
        "ideal_soil": ["Red Loamy", "Sandy Loam", "Laterite"],
        "ideal_ph": (5.5, 7.5),
        "water_req": "Low to Moderate (Rainfed suitable)",
        "market_outlook": "High demand for nutrient-dense millet; MSP support available.",
        "reasons": [
            "Highly resilient to dry spells & rainfall fluctuations",
            "Suited for Red Loamy / Sandy Loam soils of Karnataka",
            "Low fertilizer and pesticide input cost",
            "Strong market price stability"
        ],
        "risks": ["Susceptible to blast in prolonged high humidity"]
    },
    {
        "crop": "Maize",
        "base_score": 82,
        "ideal_seasons": ["Kharif", "Rabi"],
        "ideal_soil": ["Loamy", "Deep Alluvial", "Red Sandy"],
        "ideal_ph": (6.0, 7.5),
        "water_req": "Moderate (450–600 mm)",
        "market_outlook": "Strong demand from poultry feed industry & ethanol units.",
        "reasons": [
            "Short duration (90–110 days) allowing double cropping",
            "High yield potential (40–50 quintals/ha)",
            "Excellent rotation option after leguminous crops"
        ],
        "risks": ["Fall Armyworm pest risk requires early monitoring"]
    },
    {
        "crop": "Ginger",
        "base_score": 80,
        "ideal_seasons": ["Kharif"],
        "ideal_soil": ["Sandy Loam", "Clay Loam", "Humus Rich"],
        "ideal_ph": (5.5, 6.8),
        "water_req": "High (1500–2000 mm / Supplemental Drip)",
        "market_outlook": "High-value commercial spice crop; premium prices for quality rhizomes.",
        "reasons": [
            "High net return per acre (₹1.5L - ₹3.0L potential)",
            "Ideal for well-drained raised bed farming",
            "Well-suited for Hassan, Shivamogga, Kodagu regions"
        ],
        "risks": ["Requires strict drainage to prevent Rhizome Rot (Soft Rot)"]
    },
    {
        "crop": "Groundnut",
        "base_score": 77,
        "ideal_seasons": ["Kharif", "Summer"],
        "ideal_soil": ["Sandy Loam", "Red Sandy"],
        "ideal_ph": (6.0, 7.5),
        "water_req": "Moderate (500–600 mm)",
        "market_outlook": "Steady demand for oilseed crushing and direct pod sales.",
        "reasons": [
            "Leguminous crop that fixes atmospheric nitrogen into soil",
            "Improves soil fertility for subsequent cereal crops",
            "Good drought tolerance"
        ],
        "risks": ["Pod borer and Tikka leaf spot in wet conditions"]
    },
    {
        "crop": "Tomato",
        "base_score": 75,
        "ideal_seasons": ["Kharif", "Rabi", "Summer"],
        "ideal_soil": ["Loamy", "Red Loam"],
        "ideal_ph": (6.0, 7.0),
        "water_req": "Moderate-High (Drip Fertigation)",
        "market_outlook": "High local mandi demand with periodic price spikes.",
        "reasons": [
            "Quick cash returns within 75–90 days",
            "High productivity per acre under drip irrigation",
            "Multiple harvest pickings over 60 days"
        ],
        "risks": ["Market price volatility and Early/Late Blight fungal risks"]
    }
]

class CropRecommendationEngine:
    """Calculates ranked crop suitability scores based on farm context."""

    @staticmethod
    def get_recommendations(
        location: Optional[str] = None,
        soil_type: Optional[str] = None,
        water_source: Optional[str] = None,
        current_season: Optional[str] = "Kharif",
        previous_crop: Optional[str] = None,
        soil_ph: float = 6.5
    ) -> List[Dict[str, Any]]:
        results = []

        soil_clean = (soil_type or "Loamy").lower()
        water_clean = (water_source or "Irrigation").lower()
        season_clean = (current_season or "Kharif").capitalize()
        prev_crop_clean = (previous_crop or "").lower()

        for c_info in RECOMMENDABLE_CROPS:
            score = c_info["base_score"]
            reasons = list(c_info["reasons"])
            risks = list(c_info["risks"])

            # Season Match (+5)
            if season_clean in c_info["ideal_seasons"]:
                score += 5
                reasons.append(f"Ideal fit for current {season_clean} season")
            else:
                score -= 8
                risks.append(f"Non-peak season for {c_info['crop']}")

            # Soil Type Match (+5)
            soil_matched = any(s.lower() in soil_clean for s in c_info["ideal_soil"])
            if soil_matched:
                score += 5
                reasons.append(f"Well-suited for {soil_type or 'Loamy'} soil")
            else:
                score -= 3

            # Soil pH Match
            ph_min, ph_max = c_info["ideal_ph"]
            if ph_min <= soil_ph <= ph_max:
                score += 3
            else:
                score -= 4
                risks.append(f"Soil pH {soil_ph} is outside ideal range ({ph_min}–{ph_max})")

            # Crop Rotation Check (+5 for leguminous/cereal rotation)
            if prev_crop_clean:
                if "ginger" in prev_crop_clean and c_info["crop"] in ["Ragi (Finger Millet)", "Maize"]:
                    score += 7
                    reasons.append(f"Excellent crop rotation following {previous_crop}")
                elif "legume" in prev_crop_clean or "groundnut" in prev_crop_clean:
                    score += 5
                    reasons.append("Benefits from residual nitrogen of previous leguminous crop")

            # Clamp score between 50 and 98
            final_score = min(98, max(50, score))

            results.append({
                "crop": c_info["crop"],
                "suitability_score": final_score,
                "reasons": reasons[:4],
                "risks": risks[:2],
                "expected_season": c_info["ideal_seasons"][0],
                "expected_sowing_window": "15 June – 10 July",
                "water_requirement": c_info["water_req"],
                "market_outlook": c_info["market_outlook"]
            })

        # Sort by suitability score descending
        results.sort(key=lambda x: x["suitability_score"], reverse=True)
        return results


crop_recommendation_engine = CropRecommendationEngine()
