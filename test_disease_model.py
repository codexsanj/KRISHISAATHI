#!/usr/bin/env python3
"""
Standalone PyTorch Crop Disease Model Inference CLI

Usage:
    python scripts/test_disease_model.py <image_path> [crop]

Examples:
    python scripts/test_disease_model.py ginger_leaf.jpg Ginger
    python scripts/test_disease_model.py wheat_rust.jpg Wheat
    python scripts/test_disease_model.py healthy_rice.jpg Rice
    python scripts/test_disease_model.py mystery_leaf.jpg         # no crop → no isolation

Prints:
    Image, MD5 hash, request_id, crop isolation applied,
    Top-1 prediction + confidence, Top-3 with probabilities,
    Status, WHY section, Symptoms label, Treatment availability,
    Sources, Thresholds
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ai.disease_detection.disease_engine import disease_engine, CFG


def divider(char="─", width=60):
    print(char * width)


def print_result(result: dict, image_path: str):
    divider("═")
    print(f" IMAGE INFERENCE REPORT")
    divider("═")
    print(f"  Image File    : {os.path.basename(image_path)}")
    print(f"  Request ID    : {result.get('request_id')}")
    print(f"  Image MD5     : {result.get('image_hash', '')}")
    print(f"  Model         : {result.get('model_version')}")
    print(f"  Class Mapping : {result.get('class_mapping_version')}")
    print(f"  Crop Specified: {result.get('crop', '(none)')}")
    print(f"  Crop Isolation: {'YES — only matching classes evaluated' if result.get('crop') else 'NO — all 23 classes evaluated'}")

    divider()
    top1 = result.get("prediction_details", {})
    print(f"  TOP-1 Prediction : {top1.get('class', result.get('prediction'))}")
    print(f"  Confidence       : {top1.get('confidence', result.get('confidence', 0)) * 100:.1f}%")
    print(f"  Status           : {result.get('status')}")
    print(f"  Display Title    : {result.get('display_title')}")
    print(f"  Confidence Status: {result.get('confidence_status')}")

    divider()
    print("  TOP 3 PROBABILITIES")
    print(f"    1. {result.get('prediction')} — {result.get('confidence', 0)*100:.1f}%")
    for i, alt in enumerate(result.get("alternatives", []), start=2):
        print(f"    {i}. {alt.get('class')} — {alt.get('confidence', 0)*100:.1f}%")

    divider()
    print(f"  Severity      : {result.get('severity')}")
    print(f"  Causal Agent  : {result.get('causal_agent', '—')}")
    print(f"  Symptoms Label: {result.get('symptoms_label', 'Symptoms')}")
    print(f"  Symptoms      : {result.get('symptoms', '—')[:120]}...")

    divider()
    print("  WHY (Confidence-Aware):")
    print(f"    {result.get('why', '—')}")

    divider()
    print(f"  Treatment Available: {result.get('treatment_available')}")
    if result.get("treatment"):
        t = result["treatment"]
        print(f"  Active Ingredients : {', '.join(t.get('active_ingredients', []))}")
        print(f"  Chemical Guidance  : {str(t.get('chemical_management', ''))[:120]}...")
        print(f"  Safety Notice      : {str(t.get('safety_notice', ''))[:100]}...")
    else:
        print(f"  Management Note    : {result.get('management', '')[:200]}")

    if result.get("recommended_action"):
        divider()
        print(f"  Recommended Next Step: {result.get('recommended_action')}")

    divider()
    print("  When to Escalate:")
    print(f"    {result.get('when_to_escalate', '—')}")

    divider()
    print("  SOURCES:")
    for s in result.get("sources", []):
        print(f"    • {s}")

    divider()
    print(f"  Diagnosis Threshold : {CFG.DIAGNOSIS_THRESHOLD * 100:.0f}%")
    print(f"  Treatment Threshold : {CFG.TREATMENT_THRESHOLD * 100:.0f}%")
    divider("═")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_disease_model.py <image_path> [crop_name]")
        print("       crop_name is optional (e.g. Ginger, Wheat, Rice, Tomato)")
        sys.exit(1)

    image_path = sys.argv[1]
    crop = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(image_path):
        print(f"Error: '{image_path}' not found.")
        sys.exit(1)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    result = disease_engine.analyze_image(
        image_bytes=image_bytes,
        crop=crop,
        filename=os.path.basename(image_path),
    )

    print_result(result, image_path)


if __name__ == "__main__":
    main()
