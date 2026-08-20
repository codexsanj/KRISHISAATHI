import os
from typing import Dict, Any, Optional, List
from app.core.config import settings

class LLMProvider:
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        raise NotImplementedError

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            self.available = True
        except Exception:
            self.available = False

    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.available:
            raise RuntimeError("Gemini API client not initialized.")
        system_instruction = (
            "You are Saathi, an agricultural assistant for Indian farmers.\n"
            "Rules:\n"
            "1. Answer ONLY the user's current question. Do not answer a different question.\n"
            "2. NEVER assume the farmer grows Wheat unless explicitly stated.\n"
            "3. NEVER assume the location is Bengaluru/Karnataka unless explicitly provided.\n"
            "4. NEVER assume the soil is Loamy unless explicitly provided.\n"
            "5. Use ONLY farm context provided in the prompt.\n"
            "6. If farm context is missing, say so. Do not invent it.\n"
            "7. For general agricultural questions, use reliable agricultural knowledge.\n"
            "8. Do not invent weather, market prices, or model confidence.\n"
        )
        full_prompt = f"{system_instruction}\n\n{prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text

class LocalFallbackLLMProvider(LLMProvider):
    """Grounded local agricultural AI response generator (NO hardcoded Wheat defaults)."""
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        context = context or {}
        # Extract only the actual user question (not the full context-enriched prompt)
        if "User Question:" in prompt:
            import re
            match = re.search(r"User Question: '(.+?)'", prompt)
            user_q = match.group(1) if match else prompt
        else:
            user_q = prompt
        q = user_q.lower()
        # Use actual farmer's crop if available; never default to Wheat
        crop = context.get("crop", None)
        if not crop or str(crop).lower() in ["your crop", "none", "", "your crop (not set)"]:
            crop = None
        crop_label = crop if crop else "your crop"
        # Never default to Bengaluru or Loamy — use None if not provided
        location = context.get("location", None) or "your area"
        soil = context.get("soil", None) or "your soil type"

        # Greetings (handled upstream, but guard here too)
        for greeting in ["hi", "hello", "hey", "namaste"]:
            if q.strip() == greeting or q.startswith(greeting + " "):
                return "Hi! I'm Saathi, your intelligent farming companion. How can I help you with your farm today?"

        # Topic 1: Crop Rotation
        if "crop rotation" in q or "rotate" in q or ("rotation" in q and "crop" in q):
            return ("**Crop Rotation** means growing different crop families sequentially on the same land across seasons.\n\n"
                    "**Key Benefits**:\n"
                    "• **Replenishes Soil Nitrogen**: Alternating Cereals (Wheat/Maize) with Legumes (Pulses/Chickpea) fixes atmospheric nitrogen.\n"
                    "• **Breaks Pest & Disease Cycles**: Pests specific to one crop family die off when a non-host crop is planted.\n"
                    "• **Improves Soil Structure**: Deep-rooted and shallow-rooted crops utilize different soil depths.\n\n"
                    "**Example**: Kharif Maize → Rabi Chickpea → Wheat is a classic rotation for Karnataka & Maharashtra.")

        # Topic 2: Water requirements
        if "water" in q and ("need" in q or "require" in q or "how much" in q):
            if "wheat" in q:
                return "Wheat requires **400 to 500 mm of water** across 4 to 6 irrigations. Key stages: Crown Root Initiation (CRI at 21 days), Tillering, Flowering, and Grain Filling."
            if "ragi" in q or "millet" in q or "finger millet" in q:
                return "Ragi (Finger Millet) is drought-tolerant and requires only **300 to 350 mm of water**. It thrives in rain-fed conditions with minimal supplemental irrigation."
            if "rice" in q or "paddy" in q:
                return "Rice (Paddy) requires **1000 to 2000 mm of water** per season depending on the variety. Transplanted paddy needs standing water (5 cm depth) especially during tillering and heading."
            if "maize" in q or "corn" in q:
                return "Maize requires **500 to 600 mm of water** distributed across key stages: Germination, Tasseling/Silking (critical), and Grain Filling."
            if "cotton" in q:
                return "Cotton requires **700 to 1200 mm of water** across 4 to 5 months. Critical irrigation stages are Square Formation, Flowering, and Boll Development."
            return f"{crop_label} generally requires adequate moisture during critical growth stages. Ensure soil remains moist but well-drained to prevent root rot."

        # Topic 3: NPK & Fertilizers
        if "npk" in q or "fertilizer" in q or "urea" in q:
            crop_npk = ""
            if crop:
                npk_guide = {
                    "wheat": "120:60:40 kg/ha",
                    "rice": "120:60:60 kg/ha",
                    "maize": "150:75:75 kg/ha",
                    "ragi": "60:30:30 kg/ha",
                    "cotton": "100:50:50 kg/ha",
                    "tomato": "200:100:150 kg/ha",
                }
                ratio = npk_guide.get(crop.lower(), "60:30:30 kg/ha (general guideline)")
                crop_npk = f" For **{crop}**, the recommended NPK ratio is **{ratio}**."
            return ("**NPK** refers to the three primary nutrients for plant growth:\n\n"
                    "• **N (Nitrogen)**: Promotes leafy green vegetative growth and chlorophyll production.\n"
                    "• **P (Phosphorus)**: Stimulates root development, flowering, and seed formation.\n"
                    "• **K (Potassium)**: Strengthens plant stalks, enhances drought resistance, and improves grain quality.\n\n"
                    f"{crop_npk} Soil test before application for best results.")

        # Topic 4: Yellow leaves / Symptoms
        if "yellow" in q and ("leaf" in q or "leaves" in q):
            return (f"Yellowing leaves in **{crop_label}** can indicate:\n\n"
                    "1. **Nitrogen Deficiency**: Older lower leaves turn pale green/yellow first. Apply balanced NPK or urea top-dressing.\n"
                    "2. **Fungal Blight or Leaf Spot**: Dark spots with yellow halos. Spray Neem Oil (5ml/L) or Copper Oxychloride.\n"
                    "3. **Over-watering / Waterlogging**: Roots deprived of oxygen. Check field drainage.\n\n"
                    "**Recommended**: Inspect lower leaf undersides for fungal spores or sucking pests (aphids/whiteflies).")

        # Topic 5: Soil Fertility & Types
        if "soil" in q or "fertility" in q:
            if "black soil" in q:
                return "**Black Soil (Regur)** is clay-rich and moisture-retentive. It is exceptionally well-suited for **Cotton**, **Soybean**, **Wheat**, and **Chickpea**."
            if "red soil" in q:
                return "**Red Soil** is well-drained and iron-rich. It suits **Groundnut**, **Ragi**, **Millets**, and **Pulses**. Add FYM to improve water retention."
            return ("To **improve soil fertility** naturally:\n\n"
                    "1. **Incorporate Organic Carbon**: Apply well-decomposed Farmyard Manure (FYM) or vermicompost (5–10 tonnes/ha).\n"
                    "2. **Use Green Manure**: Sow Dhaincha or Sunnhemp and plow it back before flowering.\n"
                    "3. **Apply Biofertilizers**: Seed treatment with *Azotobacter* (nitrogen fixation) and *PSB* (Phosphorus Solubilizing Bacteria).")

        # Topic 6: Sowing schedules
        if "sow" in q or "sowing" in q or "planting" in q or "when to grow" in q:
            if "wheat" in q:
                return "**Wheat Sowing**:\n• **Rabi**: October to November (ideal window: 15 Oct – 15 Nov)\n• **Seed Rate**: 100–125 kg/ha\n• **Row Spacing**: 22.5 cm"
            if "rice" in q or "paddy" in q:
                return "**Rice/Paddy Sowing**:\n• **Kharif**: Nursery in June, transplanting in July–August\n• **Seed Rate**: 20–25 kg/ha (nursery)\n• **Spacing**: 20×15 cm for transplanted paddy"
            if "maize" in q or "corn" in q:
                return "**Maize Sowing**:\n• **Kharif**: June–July with monsoon onset\n• **Rabi**: October–November\n• **Seed Rate**: 20 kg/ha | **Row spacing**: 60 cm apart"
            if "ragi" in q:
                return "**Ragi Sowing**:\n• **Kharif**: June–July\n• **Seed Rate**: 8–10 kg/ha\n• **Spacing**: 30×10 cm (direct sown), transplanted in lines"
            return f"Sowing times depend on the season (Kharif: June–July, Rabi: October–November) and crop. Ensure soil moisture is adequate before sowing **{crop_label}**."

        # Topic 7: Government Schemes
        if "scheme" in q or "government" in q or "pm-kisan" in q or "subsidy" in q:
            return ("**Key Government Agricultural Schemes for Farmers**:\n\n"
                    "1. **PM-KISAN**: Direct income support of ₹6,000/year in 3 installments.\n"
                    "2. **PM Fasal Bima Yojana (PMFBY)**: Low-premium crop insurance against natural calamities & pests.\n"
                    "3. **Soil Health Card Scheme**: Free soil testing and customized NPK recommendation cards.\n"
                    "4. **Kisan Credit Card (KCC)**: Institutional credit for farm inputs at 4% concessional interest.\n"
                    "5. **e-NAM**: Online national mandi platform for better price discovery.")

        # Topic 8: Pest & Disease Control
        if "pest" in q or "disease" in q or ("insect" in q and "crop" in q):
            return (f"For effective **pest & disease control** in **{crop_label}**:\n\n"
                    "1. **Scouting**: Inspect leaf undersides and field borders twice weekly.\n"
                    "2. **Organic Spray**: Neem Oil (5ml/L of water + a few drops of soap).\n"
                    "3. **Biological Control**: *Beauveria bassiana* for caterpillars; yellow sticky traps for aphids/whiteflies.\n"
                    "4. **Chemical**: Use Imidacloprid 17.8 SL (0.5 ml/L) only if pest threshold is crossed.")

        # Topic 9: Yield improvement
        if "slow" in q or "yield" in q or "growth" in q or "production" in q:
            return (f"To boost crop growth and **maximize yield** for **{crop_label}**:\n\n"
                    "1. Incorporate compost (5–10 tonnes/ha) to raise organic carbon.\n"
                    "2. Maintain timely weeding during the first 30 days.\n"
                    "3. Apply micronutrients — Zinc Sulfate (25 kg/ha) if leaves show interveinal chlorosis.\n"
                    "4. Ensure irrigation at critical growth stages (don't stress during flowering or grain filling).")

        # Topic 10: What crop should I grow / crop recommendation
        if ("what crop" in q and ("grow" in q or "plant" in q or "sow" in q)) or ("crop" in q and "recommend" in q) or ("after" in q and "crop" in q):
            if "after wheat" in q:
                return ("After **Wheat** (Rabi), you can grow:\n\n"
                        "• **Maize or Sorghum** (Kharif): Good nitrogen utilizer after wheat.\n"
                        "• **Chickpea or Moong (Pulses)**: Fixes atmospheric nitrogen back into soil.\n"
                        "• **Sunflower or Groundnut**: Good break crop for pest cycle disruption.\n\n"
                        "**Recommendation**: Moong (Green Gram) after wheat harvest is a high-value, short-duration Kharif option.")
            if "after rice" in q or "after paddy" in q:
                return ("After **Rice/Paddy** (Kharif), consider:\n\n"
                        "• **Wheat or Mustard** (Rabi): Classic Kharif–Rabi rotation.\n"
                        "• **Chickpea (Gram)**: Excellent nitrogen-fixing option for rice fallows.\n"
                        "• **Potato or Onion**: High-value vegetables in rice rotation.")
            loc_str = f" for **{location}**" if location != "your area" else ""
            return (f"Crop choice{loc_str} depends on season, soil, and water availability:\n\n"
                    "• **Kharif (Monsoon, June–Oct)**: Rice, Maize, Cotton, Soybean, Groundnut.\n"
                    "• **Rabi (Winter, Oct–Mar)**: Wheat, Mustard, Chickpea, Barley.\n"
                    "• **Zaid (Summer, Mar–Jun)**: Vegetables (Tomato, Cucumber), Watermelon, Mung.\n\n"
                    "Consult your local KVK (Krishi Vigyan Kendra) for region-specific variety recommendations.")

        # Topic 11: Irrigation timing / when to irrigate
        if "irrigate" in q or ("when" in q and "water" in q):
            return (f"Irrigation timing for **{crop_label}**:\n\n"
                    f"• Irrigate in early morning (6–9 AM) or late evening to minimize evaporation.\n"
                    f"• Check soil moisture at 6-inch depth — if dry, irrigate; if moist, skip.\n"
                    f"• Skip irrigation if rain probability exceeds 60% within the next 24 hours.\n"
                    f"• Critical stages requiring consistent moisture: Germination, Flowering, and Grain/Fruit Filling.")

        # General fallback — never assume crop, location, or soil type
        parts = []
        if crop_label != "your crop":
            parts.append(f"**{crop_label}**")
        if location != "your area":
            parts.append(f"in **{location}**")
        if soil != "your soil type":
            parts.append(f"({soil} soil)")
        context_str = " ".join(parts) if parts else "your farm"
        return (f"Based on agricultural best practices for {context_str}:\n\n"
                "Maintain regular field monitoring, ensure balanced NPK nutrient supply, and check weather forecasts "
                "before applying irrigation or pest treatments. For detailed advice, consult your local KVK or the "
                "ICAR recommendations for your crop and region.")

class LLMService:
    def __init__(self):
        key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        if key:
            try:
                self.provider = GeminiProvider(key)
            except Exception:
                self.provider = LocalFallbackLLMProvider()
        else:
            self.provider = LocalFallbackLLMProvider()

    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        try:
            return self.provider.generate(prompt, context)
        except Exception:
            return LocalFallbackLLMProvider().generate(prompt, context)

llm_service = LLMService()
