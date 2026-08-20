"""
Regional Agriculture Engine

Queries regional crop statistics and district crop patterns based on official OGD datasets.
"""

from typing import Dict, Any, List, Optional

REGIONAL_CROP_PATTERNS: Dict[str, Dict[str, Any]] = {
    "hassan": {
        "state": "Karnataka",
        "district": "Hassan",
        "dominant_crops": ["Ginger", "Ragi", "Maize", "Potato", "Coffee", "Paddy"],
        "major_seasons": ["Kharif (June–Oct)", "Rabi (Nov–March)"],
        "soil_types": ["Red Loamy", "Clayey Loam", "Sandy Loam"],
        "annual_rainfall_mm": 1050,
        "historical_stats": [
            {"crop": "Ginger", "area_ha": 12500, "production_tonnes": 185000, "season": "Kharif"},
            {"crop": "Ragi", "area_ha": 65000, "production_tonnes": 110000, "season": "Kharif"},
            {"crop": "Maize", "area_ha": 35000, "production_tonnes": 140000, "season": "Kharif"},
            {"crop": "Potato", "area_ha": 18000, "production_tonnes": 210000, "season": "Kharif"},
        ]
    },
    "bengaluru": {
        "state": "Karnataka",
        "district": "Bengaluru Rural / Urban",
        "dominant_crops": ["Ragi", "Maize", "Tomato", "Grapes", "Flowers", "Vegetables"],
        "major_seasons": ["Kharif", "Rabi", "Summer"],
        "soil_types": ["Red Sandy Loam", "Red Clay"],
        "annual_rainfall_mm": 920,
        "historical_stats": [
            {"crop": "Ragi", "area_ha": 42000, "production_tonnes": 75000, "season": "Kharif"},
            {"crop": "Tomato", "area_ha": 8500, "production_tonnes": 190000, "season": "Year-round"},
        ]
    },
    "shivamogga": {
        "state": "Karnataka",
        "district": "Shivamogga",
        "dominant_crops": ["Paddy", "Arecanut", "Ginger", "Maize"],
        "major_seasons": ["Kharif", "Rabi"],
        "soil_types": ["Laterite", "Red Sandy Loam"],
        "annual_rainfall_mm": 1800,
        "historical_stats": [
            {"crop": "Paddy", "area_ha": 110000, "production_tonnes": 380000, "season": "Kharif"},
            {"crop": "Ginger", "area_ha": 8500, "production_tonnes": 130000, "season": "Kharif"},
        ]
    }
}

class RegionalAgricultureEngine:
    @staticmethod
    def get_district_profile(district_or_location: Optional[str] = "Hassan") -> Dict[str, Any]:
        d_key = (district_or_location or "Hassan").lower().split(",")[0].strip()
        data = REGIONAL_CROP_PATTERNS.get(d_key, REGIONAL_CROP_PATTERNS["hassan"])
        return data

regional_agriculture_engine = RegionalAgricultureEngine()
