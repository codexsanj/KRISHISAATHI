from typing import List, Dict, Any

AGRI_KNOWLEDGE_BASE = [
    {
        "id": "doc_wheat_irrigation",
        "title": "ICAR Wheat Cultivation & Irrigation Package of Practices",
        "crop": "wheat",
        "topic": "irrigation water requirement wheat",
        "keywords": ["wheat", "water", "irrigation", "cri", "tillering", "grain filling", "crown root"],
        "content": "Wheat requires 400–500 mm of water across 4–6 irrigations. Critical stages for watering are Crown Root Initiation (CRI at 21 days after sowing), Tillering, Jointing, Flowering, and Grain Filling. Over-irrigation during rainy forecasts leads to root lodging and fungal rust."
    },
    {
        "id": "doc_cotton_pest",
        "title": "Kisan Call Centre Cotton Pest & Disease Advisory",
        "crop": "cotton",
        "topic": "pest disease management cotton aphid bollworm whitefly",
        "keywords": ["cotton", "pest", "aphid", "bollworm", "whitefly", "neem", "disease", "yellow"],
        "content": "Cotton is vulnerable to Pink Bollworm, Aphids, and Whiteflies during warm humid weather. Neem oil solution (5ml/L) or Beauveria bassiana bio-pesticide provides eco-friendly control. Yellowing of cotton leaves can indicate sucking pest attack or magnesium deficiency."
    },
    {
        "id": "doc_soil_types",
        "title": "IMD Agromet Advisory — Soil Types & Suitability",
        "crop": "general",
        "topic": "soil type fertility black red loamy sandy",
        "keywords": ["soil", "black soil", "loamy", "red soil", "sandy", "clay", "biofertilizer", "azotobacter", "psb"],
        "content": "Black soil (Regur) has high clay content and water retention, ideal for Cotton, Soybean, and Wheat. Loamy soil is balanced for most cereals. Red and sandy loam soils suit Ragi, Pulses, and Groundnut. Biofertilizers like Azotobacter and PSB improve soil nutrient uptake."
    },
    {
        "id": "doc_npk_fertilizer",
        "title": "ICAR Guide on Soil Fertility & Fertilizer Management (NPK)",
        "crop": "general",
        "topic": "npk nitrogen phosphorus potassium fertilizer nutrient deficiency",
        "keywords": ["npk", "nitrogen", "phosphorus", "potassium", "fertilizer", "urea", "deficiency", "compost", "manure", "nutrient"],
        "content": "NPK stands for Nitrogen (N), Phosphorus (P), and Potassium (K). Nitrogen promotes leafy growth; deficiency causes yellowing of older leaves. Phosphorus supports root development and early flowering. Potassium boosts disease resistance, drought tolerance, and grain weight. Organic compost and green manure significantly improve soil organic carbon."
    },
    {
        "id": "doc_crop_rotation",
        "title": "ICAR Principles of Crop Rotation & Sustainability",
        "crop": "general",
        "topic": "crop rotation legume cereal sustainability intercropping",
        "keywords": ["crop rotation", "rotation", "legume", "pulse", "intercrop", "nitrogen fixation", "sustainability", "chickpea", "mung"],
        "content": "Crop rotation involves growing different crop families sequentially (e.g., Cereals like Wheat/Maize followed by Legumes/Pulses like Chickpea or Mung Bean). Legumes fix atmospheric nitrogen in root nodules, breaking pest and fungal disease cycles while restoring soil nitrogen naturally."
    },
    {
        "id": "doc_tomato_disease",
        "title": "KCC Tomato Leaf Yellowing & Blight Management Guide",
        "crop": "tomato",
        "topic": "tomato blight disease yellow leaf symptoms alternaria fungal",
        "keywords": ["tomato", "yellow", "blight", "alternaria", "early blight", "late blight", "leaf spot", "fungal", "copper oxychloride", "neem"],
        "content": "Yellowing tomato leaves can be caused by Early Blight (Alternaria fungal spots), Nitrogen deficiency, or over-watering. Early Blight starts with dark brown concentric spots surrounded by yellow halos on lower leaves. Spraying Copper Oxychloride (2.5g/L) or Neem oil (5ml/L) controls fungal spread."
    },
    {
        "id": "doc_ragi",
        "title": "TNAU Cultivation Practices for Ragi (Finger Millet)",
        "crop": "ragi",
        "topic": "ragi finger millet nutrient water fertilizer sowing kharif",
        "keywords": ["ragi", "finger millet", "millet", "water", "fertilizer", "npk", "sowing", "kharif", "drought"],
        "content": "Ragi (Finger Millet) is a hardy climate-resilient crop needing only 300–350 mm of water. Recommended fertilizer dose is 60:30:30 NPK kg/ha. Apply half Nitrogen and full Phosphorus/Potassium at sowing, and remaining Nitrogen 30 days after sowing. Ragi is ideal for rain-fed conditions."
    },
    {
        "id": "doc_maize",
        "title": "ICAR Maize Sowing Time & Agronomy",
        "crop": "maize",
        "topic": "maize corn sowing kharif rabi growth irrigation",
        "keywords": ["maize", "corn", "sowing", "kharif", "rabi", "irrigation", "rainfall", "loamy", "seed rate"],
        "content": "Kharif Maize is sown with the onset of monsoon in June-July. Rabi Maize is sown in October-November. Seed rate is 20 kg/ha. Maize requires well-drained loamy soil with 500–600 mm rainfall/irrigation evenly distributed across growth stages: germination, tasseling, and grain filling."
    },
    {
        "id": "doc_rice_irrigation",
        "title": "ICAR Rice & Paddy Cultivation — Water Management",
        "crop": "rice",
        "topic": "rice paddy water irrigation flooding transplant kharif",
        "keywords": ["rice", "paddy", "water", "irrigation", "flood", "transplant", "kharif", "blast", "brown spot"],
        "content": "Rice requires 1000–2000 mm of water per season. Transplanted paddy needs 5 cm standing water during tillering and heading stages. Critical periods: active tillering and panicle initiation. Rice Blast (Magnaporthe oryzae) is common in humid conditions — apply Tricyclazole 75 WP at 0.6g/L."
    },
    {
        "id": "doc_pest_control",
        "title": "Integrated Pest Management (IPM) Guide for Field Crops",
        "crop": "general",
        "topic": "pest control ipm neem spray biological organic aphid stem borer",
        "keywords": ["pest", "control", "ipm", "neem", "organic", "spray", "aphid", "stem borer", "bollworm", "beauveria", "pheromone", "trap"],
        "content": "IPM (Integrated Pest Management) combines: 1) Scouting — inspect fields twice weekly for early detection. 2) Organic sprays — Neem oil (5ml/L) effective against sucking pests. 3) Biological control — Beauveria bassiana for caterpillars, yellow sticky traps for whiteflies/aphids. 4) Chemical threshold — use Imidacloprid 17.8 SL (0.5ml/L) only when pest count exceeds economic threshold."
    },
    {
        "id": "doc_govt_schemes",
        "title": "Ministry of Agriculture Govt Farming Schemes Guide",
        "crop": "general",
        "topic": "government scheme pm kisan pmfby kcc soil health card subsidy",
        "keywords": ["scheme", "government", "pm-kisan", "pmfby", "insurance", "kcc", "credit", "soil health card", "subsidy", "₹6000"],
        "content": "Key Indian Govt agricultural schemes: 1. PM-KISAN (direct financial support of ₹6,000/year in 3 installments). 2. PM Fasal Bima Yojana (PMFBY comprehensive crop insurance at low premium). 3. Soil Health Card Scheme (free soil nutrient testing and NPK recommendation). 4. Kisan Credit Card (KCC short-term credit at 4% interest rate). 5. e-NAM (online mandi platform for better price discovery)."
    },
    {
        "id": "doc_market",
        "title": "Agmarknet Mandi Price Optimization & Selling Advisory",
        "crop": "general",
        "topic": "market sell mandi price crop sell timing profit",
        "keywords": ["sell", "market", "mandi", "price", "profit", "agmarknet", "e-nam", "timing"],
        "content": "Selling produce within 7 to 14 days of peak mandi price trends yields optimal profit margins before market arrivals saturate supply. Compare prices across nearby mandis using e-NAM before transport. Monitor arrival data — when supply spikes, prices fall."
    },
    {
        "id": "doc_photosynthesis",
        "title": "Basics of Plant Physiology — Photosynthesis & Crop Growth",
        "crop": "general",
        "topic": "photosynthesis plant growth chlorophyll sunlight carbon dioxide",
        "keywords": ["photosynthesis", "chlorophyll", "sunlight", "carbon dioxide", "co2", "plant growth", "leaf", "light"],
        "content": "Photosynthesis is the process by which plants convert sunlight, CO2, and water into glucose and oxygen using chlorophyll in leaf cells. Adequate sunlight (6–8 hours), healthy leaf area index, and sufficient nitrogen (for chlorophyll synthesis) maximize photosynthetic efficiency and ultimately crop yield."
    }
]

class RAGEngine:
    """Query-specific RAG Retrieval Engine over ICAR/KCC agricultural guidance documents."""

    def search(self, query: str, top_k: int = 2) -> list:
        query_lower = query.lower()
        results = []

        for doc in AGRI_KNOWLEDGE_BASE:
            score = 0

            # Strong match: keyword list (most reliable)
            for kw in doc.get("keywords", []):
                if kw in query_lower:
                    score += 5

            # Crop match in query
            if doc["crop"] != "general" and doc["crop"] in query_lower:
                score += 4

            # Topic word match
            for topic_word in doc["topic"].lower().split():
                if len(topic_word) > 3 and topic_word in query_lower:
                    score += 2

            # Content word match (weak signal)
            for word in query_lower.split():
                if len(word) > 4 and word in doc["content"].lower():
                    score += 1

            if score > 0:
                results.append((score, doc))

        results.sort(key=lambda x: x[0], reverse=True)

        # CRITICAL: Return empty list if NO document matches the query.
        # Never inject ICAR Wheat document for unrelated questions.
        if not results:
            return []

        return [doc for score, doc in results[:top_k]]


rag_engine = RAGEngine()
