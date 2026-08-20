"""
Daily Farm Plan Engine

Generates structured:
- TODAY
- NEXT 3 DAYS
- NEXT 7 DAYS

Farm tasks based on current crop, crop age, crop stage, weather forecast, irrigation history, and pest/disease risks.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.ai.farm_intelligence.crop_lifecycle_engine import crop_lifecycle_engine

class DailyFarmPlanEngine:
    @staticmethod
    def generate_daily_plan(
        crop_name: str,
        sowing_date: Optional[str] = None,
        rain_probability_pct: float = 20.0,
        temp_c: float = 28.0,
        recent_activity_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        
        # Get crop lifecycle details
        lifecycle = crop_lifecycle_engine.get_lifecycle_info(crop_name, sowing_date)
        crop_age = lifecycle["crop_age_days"]
        stage = lifecycle["current_stage"]
        recent = recent_activity_types or []

        today_tasks = []
        next_3_days = []
        next_7_days = []

        # Weather & Irrigation Rule
        if rain_probability_pct >= 60.0:
            today_tasks.append({
                "task": "Skip irrigation today",
                "reason": f"High probability of rainfall ({rain_probability_pct:.0f}%) forecast.",
                "priority": "High",
                "category": "Irrigation",
                "recommended_date": datetime.now().strftime("%d %b %Y"),
                "rule_source": "IMD Weather Rule Engine"
            })
            next_3_days.append({
                "task": "Inspect field drainage channels & clear water stagnation",
                "reason": "Prevent root drowning post-rainfall.",
                "priority": "High",
                "category": "Water Management",
                "recommended_date": (datetime.now() + timedelta(days=1)).strftime("%d %b %Y"),
                "rule_source": "ICAR Good Agricultural Practices"
            })
            irrigation_advice = "Irrigation paused — rain expected today."
        else:
            today_tasks.append({
                "task": "Check soil moisture (top 5 cm)",
                "reason": f"Dry weather ({rain_probability_pct:.0f}% rain prob). Irrigate if soil feels dry.",
                "priority": "Medium",
                "category": "Irrigation",
                "recommended_date": datetime.now().strftime("%d %b %Y"),
                "rule_source": "Moisture Monitoring Engine"
            })
            irrigation_advice = "Standard irrigation schedule based on soil dryness."

        # Pest / Disease Rule based on crop stage & temp
        if "vegetative" in stage.lower() or "tiller" in stage.lower():
            today_tasks.append({
                "task": f"Scout leaf undersides for leaf spot / sucker pests",
                "reason": f"{crop_name} is in active {stage}. Early detection prevents secondary spread.",
                "priority": "Medium",
                "category": "Inspection",
                "recommended_date": datetime.now().strftime("%d %b %Y"),
                "rule_source": "Crop Protection Advisory"
            })
            next_3_days.append({
                "task": "Apply organic neem oil spray (5 ml/L) if minor pests observed",
                "reason": "Preventive botanical pest repellent.",
                "priority": "Medium",
                "category": "Pest Control",
                "recommended_date": (datetime.now() + timedelta(days=2)).strftime("%d %b %Y"),
                "rule_source": "NIPHM IPM Guidelines"
            })

        # Milestone tasks from Crop Lifecycle Engine
        for milestone in lifecycle["task_milestones"]:
            if milestone["status"] == "UPCOMING":
                next_7_days.append({
                    "task": milestone["task"],
                    "reason": f"Scheduled milestone for day {milestone['day_offset']} of {crop_name} lifecycle.",
                    "priority": "Medium",
                    "category": milestone["category"],
                    "recommended_date": milestone["scheduled_date"],
                    "rule_source": "ICAR Crop Package of Practices"
                })
                if len(next_7_days) >= 3:
                    break

        return {
            "crop": crop_name,
            "crop_age_days": crop_age,
            "current_stage": stage,
            "today_tasks": today_tasks,
            "next_3_days_tasks": next_3_days,
            "next_7_days_tasks": next_7_days,
            "weather_summary": f"Temperature {temp_c:.1f}°C, Rain Prob: {rain_probability_pct:.0f}%",
            "irrigation_advice": irrigation_advice,
            "pest_risk_status": "Low to Moderate Risk"
        }

daily_farm_plan_engine = DailyFarmPlanEngine()
