from typing import Dict, Any, List, Optional
import io


# Actual supported pest classes (what a YOLO model trained on PlantDoc/IP102 would support)
SUPPORTED_PEST_CLASSES = [
    "aphid", "whitefly", "thrips", "mealybug", "bollworm", "stem_borer",
    "leaf_miner", "spider_mite", "jassid", "armyworm"
]


class PestRiskEngine:
    """Pest Risk Engine: statistical prediction + image-based detection stub."""

    # ── Statistical risk prediction (text-based) ─────────────────────────────
    def predict_risk(self, crop: str = "Cotton", temp: float = 32.0, humidity: float = 65.0) -> Dict[str, Any]:
        crop_l = (crop or "").lower()

        if temp > 30.0 and humidity > 60.0:
            risk_level = "Moderate"
            prob = 0.65
            pest_type = f"{crop} Aphids & Whitefly" if crop else "General Sucking Pests"
            title = f"{crop} pest activity rising" if crop else "Pest activity elevated"
            desc = (f"Regional {crop} pest risk is moderate this week due to warm, humid weather. "
                    f"Inspect leaf undersides for aphids or whitefly eggs.") if crop else \
                   "Warm humid conditions elevate sucking pest activity. Scout your fields."
        elif humidity > 80.0:
            risk_level = "High"
            prob = 0.85
            pest_type = "Pink Bollworm / Stem Borer"
            title = f"High Pest Outbreak Risk — {crop}" if crop else "High Pest Outbreak Risk"
            desc = ("High humidity elevates pest egg hatching rates. "
                    "Install pheromone traps and inspect fields immediately.")
        else:
            risk_level = "Low"
            prob = 0.20
            pest_type = "None reported"
            title = "Low Pest Risk"
            desc = "Current weather conditions are unfavourable for major pest surges."

        return {
            "risk_level": risk_level,
            "pest_type": pest_type,
            "probability": prob,
            "title": title,
            "description": desc,
            "engine": "Statistical Pest Risk Model v1.0"
        }

    # ── Image-based pest detection ────────────────────────────────────────────
    def analyze_image(self, image_bytes: bytes, crop: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a pest image using the YOLO detection model.

        Since the trained YOLO weights are not yet bundled in this repository,
        this method returns an honest 'model_unavailable' status rather than
        fabricating detections.

        When YOLO weights are available, replace the body of this method with:
            model = YOLO('weights/pest_yolo_v8.pt')
            results = model.predict(image_array)
            detections = [...]
            return {"status": "success", "detections": detections, ...}
        """
        # Validate image bytes
        size_kb = len(image_bytes) / 1024.0
        if size_kb < 0.5:
            return {
                "status": "error",
                "message": "The uploaded file is empty or too small to be a valid image.",
                "detections": [],
                "model": "pest_yolo",
                "model_version": None,
                "supported_classes": SUPPORTED_PEST_CLASSES,
                "crop": crop
            }

        # Verify image can be opened (basic sanity check)
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()
        except Exception:
            # PIL not available or not a valid image — still try to proceed
            pass

        # YOLO model weights not available in this installation
        # Return honest model_unavailable instead of fabricating results
        return {
            "status": "model_unavailable",
            "message": (
                "The YOLO pest detection model is currently unavailable. "
                "Please upload the trained model weights to enable real-time pest detection. "
                "You can still use the statistical pest risk assessment above."
            ),
            "detections": [],
            "model": "pest_yolo_v8",
            "model_version": "not_loaded",
            "supported_classes": SUPPORTED_PEST_CLASSES,
            "crop": crop
        }


pest_engine = PestRiskEngine()
