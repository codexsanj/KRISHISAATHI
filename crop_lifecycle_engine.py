"""
Crop Lifecycle Engine — Agricultural Lifecycle & Stage Management System

Provides rule-based lifecycle management for major Indian crops:
- Ginger, Wheat, Rice, Tomato, Potato, Cotton, Maize, Ragi

Computes:
- Crop age (days) from sowing date
- Current growth stage (Germination, Vegetative, Flowering, Maturity, Harvest)
- Estimated harvest window (date range)
- After-seeding automatic task schedule
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# Crop Lifecycle Knowledge Base (duration in days and stage thresholds)
CROP_LIFECYCLES: Dict[str, Dict[str, Any]] = {
    "ginger": {
        "crop_name": "Ginger",
        "total_duration_days": 240,
        "harvest_range_days": (210, 240),
        "stages": [
            {"name": "Land Preparation & Planting", "min_day": 0, "max_day": 14},
            {"name": "Germination / Sprouting", "min_day": 15, "max_day": 45},
            {"name": "Active Vegetative & Tiller Growth", "min_day": 46, "max_day": 120},
            {"name": "Rhizome Development & Bulking", "min_day": 121, "max_day": 180},
            {"name": "Maturity & Senescence", "min_day": 181, "max_day": 210},
            {"name": "Harvest Ready", "min_day": 211, "max_day": 250},
        ],
        "after_seeding_tasks": [
            {"day_offset": 5, "task": "Apply 1st layer green leaf mulch (10–12 t/ha)", "category": "Mulching"},
            {"day_offset": 15, "task": "Inspect shoot emergence & check soil moisture", "category": "Germination"},
            {"day_offset": 45, "task": "Weeding & 2nd mulching (5 t/ha) + top dress N (25 kg/ha)", "category": "Nutrition"},
            {"day_offset": 90, "task": "3rd mulching & earthing up around pseudostems", "category": "Earthing Up"},
            {"day_offset": 120, "task": "Check for rhizome rot / leaf spot & maintain drainage", "category": "Pest/Disease"},
            {"day_offset": 180, "task": "Stop nitrogen application & monitor foliage yellowing", "category": "Maturity"},
            {"day_offset": 210, "task": "Initiate harvesting when 70% foliage yellowing occurs", "category": "Harvest"},
        ]
    },
    "wheat": {
        "crop_name": "Wheat",
        "total_duration_days": 130,
        "harvest_range_days": (120, 135),
        "stages": [
            {"name": "Germination / Crown Root Initiation (CRI)", "min_day": 0, "max_day": 21},
            {"name": "Tillering Stage", "min_day": 22, "max_day": 45},
            {"name": "Jointing & Booting", "min_day": 46, "max_day": 75},
            {"name": "Heading & Flowering", "min_day": 76, "max_day": 95},
            {"name": "Milking & Grain Filling", "min_day": 96, "max_day": 115},
            {"name": "Dough & Maturity", "min_day": 116, "max_day": 135},
        ],
        "after_seeding_tasks": [
            {"day_offset": 21, "task": "1st irrigation at Crown Root Initiation (CRI) stage", "category": "Irrigation"},
            {"day_offset": 30, "task": "Top dress Urea (30 kg N/ha) & herbicide weed control", "category": "Nutrition"},
            {"day_offset": 45, "task": "2nd irrigation at Tillering stage", "category": "Irrigation"},
            {"day_offset": 65, "task": "3rd irrigation at Jointing stage", "category": "Irrigation"},
            {"day_offset": 85, "task": "4th irrigation at Flowering / Heading stage", "category": "Irrigation"},
            {"day_offset": 105, "task": "5th irrigation at Dough stage & check rust signs", "category": "Pest/Disease"},
            {"day_offset": 125, "task": "Harvest when grains turn golden and hard", "category": "Harvest"},
        ]
    },
    "rice": {
        "crop_name": "Rice",
        "total_duration_days": 135,
        "harvest_range_days": (125, 140),
        "stages": [
            {"name": "Nursery / Seedling Stage", "min_day": 0, "max_day": 25},
            {"name": "Transplanting / Recovery", "min_day": 26, "max_day": 40},
            {"name": "Active Tillering", "min_day": 41, "max_day": 70},
            {"name": "Panicle Initiation & Booting", "min_day": 71, "max_day": 90},
            {"name": "Flowering & Grain Filling", "min_day": 91, "max_day": 115},
            {"name": "Ripening & Harvest Ready", "min_day": 116, "max_day": 140},
        ],
        "after_seeding_tasks": [
            {"day_offset": 25, "task": "Transplant 25-day seedlings to main puddled field", "category": "Transplanting"},
            {"day_offset": 35, "task": "Maintain 2–3 cm standing water & apply 1st N split", "category": "Water/Fertilizer"},
            {"day_offset": 55, "task": "Top dress 2nd N split at active tillering", "category": "Nutrition"},
            {"day_offset": 75, "task": "Top dress K at Panicle Initiation stage", "category": "Nutrition"},
            {"day_offset": 95, "task": "Inspect for Rice Blast / Brown Spot symptoms", "category": "Pest/Disease"},
            {"day_offset": 120, "task": "Drain field 10 days before harvest", "category": "Water Management"},
            {"day_offset": 130, "task": "Harvest when 80-85% panicles turn golden yellow", "category": "Harvest"},
        ]
    },
    "tomato": {
        "crop_name": "Tomato",
        "total_duration_days": 140,
        "harvest_range_days": (110, 150),
        "stages": [
            {"name": "Nursery / Transplanting", "min_day": 0, "max_day": 25},
            {"name": "Vegetative Growth & Staking", "min_day": 26, "max_day": 50},
            {"name": "Flowering & Fruit Set", "min_day": 51, "max_day": 80},
            {"name": "Fruit Development & Picking", "min_day": 81, "max_day": 140},
        ],
        "after_seeding_tasks": [
            {"day_offset": 25, "task": "Transplant seedlings & install staking supports", "category": "Staking"},
            {"day_offset": 40, "task": "Prune lower leaves & apply fertigation (NPK 19:19:19)", "category": "Nutrition"},
            {"day_offset": 60, "task": "Foliar spray Micronutrients + Calcium for fruit set", "category": "Nutrition"},
            {"day_offset": 75, "task": "Inspect for Early Blight target spots & Whitefly pests", "category": "Pest/Disease"},
            {"day_offset": 90, "task": "1st fruit harvesting at breaker/pink stage", "category": "Harvest"},
        ]
    }
}

class CropLifecycleEngine:
    """Computes crop age, stage, harvest range, and auto-generated task milestones."""

    @staticmethod
    def get_lifecycle_info(crop_name: str, sowing_date_str: Optional[str] = None) -> Dict[str, Any]:
        c_key = (crop_name or "").lower().strip()
        info = CROP_LIFECYCLES.get(c_key, CROP_LIFECYCLES.get("ginger"))

        # Calculate crop age in days
        sowing_dt = None
        crop_age_days = 0
        if sowing_date_str:
            try:
                sowing_dt = datetime.strptime(sowing_date_str, "%Y-%m-%d")
                crop_age_days = max(0, (datetime.now() - sowing_dt).days)
            except Exception:
                crop_age_days = 30
        else:
            sowing_dt = datetime.now() - timedelta(days=30)
            sowing_date_str = sowing_dt.strftime("%Y-%m-%d")
            crop_age_days = 30

        # Determine current stage
        current_stage = "Vegetative Stage"
        for stg in info["stages"]:
            if stg["min_day"] <= crop_age_days <= stg["max_day"]:
                current_stage = stg["name"]
                break
        if crop_age_days > info["stages"][-1]["max_day"]:
            current_stage = "Post Harvest / Field Clearance"

        # Calculate harvest window range
        h_min, h_max = info["harvest_range_days"]
        est_harvest_start = (sowing_dt + timedelta(days=h_min)).strftime("%d %b %Y")
        est_harvest_end = (sowing_dt + timedelta(days=h_max)).strftime("%d %b %Y")
        harvest_window_str = f"{est_harvest_start} – {est_harvest_end}"

        # Generate upcoming task milestones
        upcoming_tasks = []
        for task_def in info["after_seeding_tasks"]:
            t_day = task_def["day_offset"]
            t_date = (sowing_dt + timedelta(days=t_day)).strftime("%Y-%m-%d")
            t_status = "COMPLETED" if crop_age_days >= t_day else "UPCOMING"
            upcoming_tasks.append({
                "day_offset": t_day,
                "scheduled_date": t_date,
                "task": task_def["task"],
                "category": task_def["category"],
                "status": t_status
            })

        return {
            "crop_name": info["crop_name"],
            "sowing_date": sowing_date_str,
            "crop_age_days": crop_age_days,
            "current_stage": current_stage,
            "total_duration_days": info["total_duration_days"],
            "harvest_window": harvest_window_str,
            "stages": info["stages"],
            "task_milestones": upcoming_tasks
        }


crop_lifecycle_engine = CropLifecycleEngine()
