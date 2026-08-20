from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.services.irrigation_service import irrigation_engine
from app.services.weather_service import weather_service
from app.services.market_service import market_service
from app.ai.pest_risk.pest_engine import pest_engine
from app.ai.rag.rag_engine import rag_engine
from app.ai.llm.llm_service import llm_service
from app.simulation.simulation_engine import simulation_engine

from app.ai.farm_intelligence.crop_lifecycle_engine import crop_lifecycle_engine
from app.ai.farm_intelligence.crop_recommendation_engine import crop_recommendation_engine
from app.ai.farm_intelligence.sowing_decision_engine import sowing_decision_engine
from app.ai.farm_intelligence.daily_farm_plan_engine import daily_farm_plan_engine
from app.ai.farm_intelligence.selling_decision_engine import selling_decision_engine
from app.ai.farm_intelligence.farm_profit_engine import farm_profit_engine
from app.models.all_models import CropCycle, FarmActivity, ExpenseRecord, SaleRecord, HarvestRecord


CROPS_LIST = [
    "wheat", "rice", "paddy", "ragi", "maize", "corn",
    "cotton", "tomato", "potato", "chickpea", "groundnut",
    "sugarcane", "soybean", "mustard", "barley", "sorghum", "bajra",
    "ginger", "onion", "garlic", "chilli", "turmeric", "coriander", "cumin",
    "banana", "mango", "grapes", "pomegranate", "coconut", "apple", "orange",
    "papaya", "guava", "brinjal", "cabbage", "cauliflower", "gram", "tur", "urad", "moong"
]

NO_FARM_CONTEXT_MSG = (
    "I need your farm profile to give you personalized advice. "
    "Please complete your farm setup (crop, location, soil type) first, "
    "then I can answer farm-specific questions for you."
)

def _make_response(answer: str, intent: str, sources: List[str] = None,
                   structured: Dict = None, is_what_if: bool = False,
                   requires_expert: bool = False, actions: List = None) -> Dict[str, Any]:
    """Helper to build a consistent Saathi response dict."""
    return {
        "message": answer,
        "answer": answer,
        "intent": intent,
        "confidence": 0.95,
        "sources": sources or [],
        "actions": actions or [],
        "structured": structured,
        "what": structured.get("what") if structured else None,
        "when": structured.get("when") if structured else None,
        "why": structured.get("why") if structured else None,
        "requires_expert": requires_expert,
        "is_what_if": is_what_if,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


class SaathiRouter:
    """Central Conversational AI & Decision Router for Saathi."""

    def route_and_process(
        self,
        query: str,
        db: Session,
        farmer=None,
        farm=None,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        q = query.strip()
        q_lower = q.lower()
        history = history or []

        # ── 1. GREETINGS ──────────────────────────────────────────────────────
        greetings = {"hi", "hello", "hey", "namaste", "good morning",
                     "good afternoon", "good evening", "hi saathi", "hello saathi",
                     "halo", "hai"}
        # Clean greeting check — avoid matching "hello — follow-up: ..." or "hello world..."
        clean_q = q_lower.rstrip("!.,?")
        if clean_q in greetings or clean_q in {"hi saathi", "hello saathi", "hey saathi"}:
            name = (farmer.name.strip() if farmer and farmer.name else None)
            msg = f"Hi {name}! " if name else "Hi! "
            msg += "I'm Saathi, your intelligent farming companion. How can I help you with your farm today?"
            return _make_response(msg, "GREETING")

        # ── 2. THANKS / CONVERSATIONAL ────────────────────────────────────────
        if q_lower in {"thanks", "thank you", "thank you saathi", "thanks saathi", "ok", "okay"}:
            return _make_response(
                "You're welcome! Feel free to ask any farming question.",
                "CONVERSATIONAL"
            )

        # ── 3. EXTRACT CROP FROM QUERY (never assume) ─────────────────────────
        import re
        crop_mentioned_in_query = None
        for c in CROPS_LIST:
            if re.search(r'\b' + re.escape(c) + r'\b', q_lower):
                crop_mentioned_in_query = c.capitalize()
                if c == "corn":   crop_mentioned_in_query = "Maize"
                if c == "paddy":  crop_mentioned_in_query = "Rice"
                if c == "bajra":  crop_mentioned_in_query = "Pearl Millet"
                break

        # Farm context (from the authenticated farmer's actual DB record)
        farm_crop      = farm.current_crop.strip() if (farm and farm.current_crop) else None
        farm_location  = farm.location.strip()     if (farm and farm.location)     else None
        farm_soil      = farm.soil_type.strip()    if (farm and farm.soil_type)    else None
        farm_water     = farm.water_source.strip() if (farm and farm.water_source) else None

        # Prefer crop mentioned in user's query; fall back to farmer's actual farm crop; never assume
        crop = crop_mentioned_in_query or farm_crop

        # Display labels — explicit about what we know vs. don't know
        crop_display     = crop         if crop         else "your crop (not set)"
        location_display = farm_location if farm_location else None
        soil_display     = farm_soil     if farm_soil     else None

        # ── 4. MULTIPLE FIELDS HANDLING ───────────────────────────────────────
        # Check if farmer has multiple farms/fields with different crops
        if farm and farmer:
            all_farms = farmer.farms if hasattr(farmer, "farms") else []
            if len(all_farms) > 1 and not crop_mentioned_in_query:
                # Farm-specific question but ambiguous crop
                farm_crops = list({f.current_crop for f in all_farms if f.current_crop})
                if len(farm_crops) > 1:
                    # Question touches field-specific context
                    field_specific_keywords = {
                        "irrigate", "spray", "fertilize", "harvest", "sow",
                        "what should", "what can", "do today", "my crop", "my field"
                    }
                    if any(kw in q_lower for kw in field_specific_keywords):
                        crops_str = ", ".join(farm_crops)
                        msg = (f"I see you have multiple fields with different crops ({crops_str}). "
                               f"Which field or crop are you asking about?")
                        return _make_response(msg, "CLARIFICATION")

        # ── 4.5 FARMER MEMORY & HISTORY QUESTIONS ──────────────────────────────
        if farmer:
            # A. "What did I plant / grow / sow last season / previously?"
            if any(kw in q_lower for kw in ["what did i plant", "what did i grow", "last season", "previous crop", "crop history"]):
                cycles = db.query(CropCycle).filter(CropCycle.farmer_id == farmer.id).order_by(CropCycle.created_at.desc()).all()
                if cycles:
                    cycle_list = [f"• **{c.crop_name}** ({c.season or 'Kharif'}) — Sown: {c.sowing_date or 'N/A'}, Stage: {c.current_stage}, Status: {c.status}" for c in cycles]
                    msg = f"**Your Farm Crop History**:\n\n" + "\n".join(cycle_list)
                    return _make_response(msg, "FARM_MEMORY", sources=["PostgreSQL Farm Memory DB"])
                else:
                    return _make_response(f"Based on your farm records, your current active crop is **{crop_display}**. No previous crop cycles are recorded yet.", "FARM_MEMORY")

            # B. "When did I sow / plant my crop?"
            if any(kw in q_lower for kw in ["when did i sow", "when did i plant", "sowing date"]):
                latest_cycle = db.query(CropCycle).filter(CropCycle.farmer_id == farmer.id, CropCycle.status == "ACTIVE").first()
                if latest_cycle and latest_cycle.sowing_date:
                    msg = f"According to your farm records, you sowed **{latest_cycle.crop_name}** on **{latest_cycle.sowing_date}** (Current stage: {latest_cycle.current_stage})."
                    return _make_response(msg, "FARM_MEMORY", sources=["PostgreSQL Farm Memory DB"])
                elif farm and farm.current_crop:
                    msg = f"Your current registered crop is **{farm.current_crop}**. Sowing date is not explicitly logged yet — ask me to record your sowing date."
                    return _make_response(msg, "FARM_MEMORY")

            # C. "How much did I spend / expenses / cost?"
            if any(kw in q_lower for kw in ["how much did i spend", "my expenses", "total cost", "how much spent"]):
                profit_info = farm_profit_engine.compute_farm_profit(db, farmer.id)
                exp_break = ", ".join([f"{k}: ₹{v:,.0f}" for k, v in profit_info["expense_breakdown"].items() if v > 0])
                msg = (f"**Your Farm Expense Summary**:\n\n"
                       f"• **Total Recorded Cost**: ₹{profit_info['total_recorded_cost']:,.2f}\n"
                       f"• **Expense Breakdown**: {exp_break or 'No categorized expenses logged yet'}")
                return _make_response(msg, "FARM_MEMORY", sources=["PostgreSQL Farm Memory DB"])

            # D. "How much did I earn / revenue / sales / profit?"
            if any(kw in q_lower for kw in ["how much did i earn", "my revenue", "my profit", "sales history", "total revenue"]):
                profit_info = farm_profit_engine.compute_farm_profit(db, farmer.id)
                msg = (f"**Your Farm Financial Performance**:\n\n"
                       f"• **Total Revenue**: ₹{profit_info['total_revenue']:,.2f}\n"
                       f"• **Total Recorded Costs**: ₹{profit_info['total_recorded_cost']:,.2f}\n"
                       f"• **Net Profit**: ₹{profit_info['net_profit']:,.2f}\n"
                       f"• **Gross Return**: ₹{profit_info['gross_return']:,.2f}")
                return _make_response(msg, "FARM_MEMORY", sources=["PostgreSQL Farm Memory DB"])

            # E. "What activities / history did I log?"
            if any(kw in q_lower for kw in ["my activities", "activity history", "what did i do on", "what activities"]):
                activities = db.query(FarmActivity).filter(FarmActivity.farmer_id == farmer.id).order_by(FarmActivity.activity_date.desc()).limit(8).all()
                if activities:
                    act_list = [f"• **{a.activity_date}**: {a.activity_type} — {a.description}" for a in activities]
                    msg = f"**Your Recent Farm Activities Timeline**:\n\n" + "\n".join(act_list)
                    return _make_response(msg, "FARM_MEMORY", sources=["PostgreSQL Farm Memory DB"])

        # ── 4.6 SOWING WINDOW DECISION ─────────────────────────────────────────
        if any(kw in q_lower for kw in ["when to sow", "when should i sow", "sowing window", "sowing period"]):
            target_crop = crop or "Ginger"
            loc = location_display or "Hassan, Karnataka"
            w_data = weather_service.get_current_weather(loc)
            sow_res = sowing_decision_engine.evaluate_sowing_window(
                crop_name=target_crop,
                location=loc,
                rainfall_forecast_mm=w_data.get("rainfall_mm", 0.0),
                temp_max_c=w_data.get("temperature_c", 28.0)
            )
            msg = (f"**Sowing Decision for {target_crop}** ({loc}):\n\n"
                   f"• **Recommended Window**: {sow_res['recommended_window']}\n"
                   f"• **Decision**: {'Favorable for sowing' if sow_res['is_favorable'] else 'Caution advised'}\n"
                   f"• **Reason**: {sow_res['reason']}\n"
                   f"• **Optimal Conditions**: {sow_res['optimal_conditions']['soil_temp_range']}, {sow_res['optimal_conditions']['bed_type']}")
            return _make_response(msg, "SOWING_DECISION", sources=["Sowing Decision Engine", "IMD Weather Service"])

        # ── 4.7 SMART CROP RECOMMENDATIONS ────────────────────────────────────
        if any(kw in q_lower for kw in ["which crop should i grow", "what crop should i plant", "crop recommendation", "recommend crop"]):
            loc = location_display or "Hassan, Karnataka"
            soil = soil_display or "Loamy"
            water = farm_water or "Irrigation"
            recs = crop_recommendation_engine.get_recommendations(location=loc, soil_type=soil, water_source=water)
            top3 = recs[:3]
            rec_lines = [f"1. **{r['crop']}** (Suitability: {r['suitability_score']}%)\n   • Reasons: {', '.join(r['reasons'][:2])}\n   • Water req: {r['water_requirement']}" for r in top3]
            msg = f"**Top Smart Crop Recommendations for {loc} ({soil} soil)**:\n\n" + "\n\n".join(rec_lines)
            return _make_response(msg, "CROP_RECOMMENDATION", sources=["Smart Crop Recommendation Engine"])

        # ── 5. WEATHER ────────────────────────────────────────────────────────
        weather_keywords = {"weather", "rain tomorrow", "will it rain", "temperature", "forecast", "humidity"}
        if any(kw in q_lower for kw in weather_keywords):
            loc = location_display or "your area"
            w_data = weather_service.get_weather(loc)
            temp   = w_data.get("temperature_c", "N/A")
            cond   = w_data.get("condition", "N/A")
            rain   = w_data.get("rain_probability_pct", "N/A")
            humid  = w_data.get("humidity_pct", "N/A")
            loc_label = f" in {loc}" if location_display else ""
            msg = (f"**Today's Weather{loc_label}**:\n\n"
                   f"• **Temperature**: {temp}°C\n"
                   f"• **Condition**: {cond}\n"
                   f"• **Rain Probability**: {rain}%\n"
                   f"• **Humidity**: {humid}%")
            return _make_response(msg, "WEATHER", sources=["AgMet Weather Provider"])

        # ── 6. WHAT-IF SIMULATION ─────────────────────────────────────────────
        if "what if" in q_lower or "what happens if" in q_lower:
            sim_res = simulation_engine.run_simulation(db, q, farm.id if farm else None)
            s = sim_res.get("structured", {})
            return {
                **_make_response(
                    sim_res["explanation"], "WHAT_IF",
                    sources=["KrishiSaathi Simulation Engine"],
                    structured=s, is_what_if=True
                ),
                "simulation": sim_res
            }

        # ── 7. IRRIGATION ─────────────────────────────────────────────────────
        irrigate_kws = {"irrigate", "irrigation", "water my crop", "should i water"}
        if any(kw in q_lower for kw in irrigate_kws) or (
                "water" in q_lower and "should i" in q_lower):
            if not crop and not farm:
                return _make_response(NO_FARM_CONTEXT_MSG, "REQUIRES_PROFILE")
            if not crop:
                msg = ("To give you an irrigation recommendation, I need to know your crop. "
                       "Which crop are you growing, or please complete your farm profile.")
                return _make_response(msg, "CLARIFICATION")

            loc  = location_display or "your area"
            soil = soil_display or "your soil"
            w_data    = weather_service.get_weather(loc)
            rain_prob = w_data.get("rain_probability_pct", 50.0)
            res = irrigation_engine.evaluate(crop, soil, rain_prob)
            formatted = (f"**Irrigation Decision for {crop}**:\n\n"
                         f"• **WHAT**: {res['what']}\n"
                         f"• **WHEN**: {res['when']}\n"
                         f"• **WHY**: {res['why']}")
            return _make_response(
                formatted, "IRRIGATION",
                sources=["Irrigation Decision Engine", "AgMet Weather Service"],
                structured={"what": res["what"], "when": res["when"], "why": res["why"]},
                actions=[{"label": "View Farm", "route": "/farm"}]
            )

        # ── 8. TODAY'S PRIORITY ACTION (DYNAMIC) ─────────────────────────────
        today_kws = {"what should i do today", "what can i do today", "do today",
                     "priority today", "today's task", "today task"}
        if any(kw in q_lower for kw in today_kws):
            if not farm or not crop:
                if not farm:
                    return _make_response(NO_FARM_CONTEXT_MSG, "REQUIRES_PROFILE")
                return _make_response(
                    "Your farm profile doesn't have a crop set yet. "
                    "Please update your farm with the current crop so I can give you today's actions.",
                    "REQUIRES_PROFILE"
                )
            # Build dynamic action from real farm context
            loc       = location_display or "your area"
            soil      = soil_display or "your soil"
            w_data    = weather_service.get_weather(loc)
            rain_prob = w_data.get("rain_probability_pct", 50.0)
            rain_cond = w_data.get("condition", "partly cloudy")
            irr       = irrigation_engine.evaluate(crop, soil, rain_prob)
            pest_risk = pest_engine.predict_risk(crop)
            risk_lvl  = pest_risk.get("risk_level", "Low")

            # Compose priority based on actual data
            if irr["decision"] == "IRRIGATE":
                what = f"Apply irrigation to your {crop} field."
                when = irr["when"]
                why  = irr["why"]
            elif risk_lvl in ("Moderate", "High"):
                what = f"Inspect {crop} leaves for pest signs; apply neem spray (5ml/L) if damage found."
                when = "Today before 4 PM."
                why  = (f"Pest risk for {crop} is {risk_lvl} due to current weather conditions "
                        f"({rain_cond}, rain probability {rain_prob:.0f}%).")
            else:
                what = f"Monitor your {crop} field for any signs of stress or disease."
                when = "Morning walk-through before 9 AM."
                why  = (f"No urgent irrigation or pest action needed today. "
                        f"Conditions are {rain_cond} with {rain_prob:.0f}% rain probability.")

            formatted = (f"**Today's Priority Action for {crop}**:\n\n"
                         f"• **WHAT**: {what}\n"
                         f"• **WHEN**: {when}\n"
                         f"• **WHY**: {why}")
            return _make_response(
                formatted, "TODAY_ACTION",
                sources=["Irrigation Engine", "AgMet Weather", "Pest Risk Model"],
                structured={"what": what, "when": when, "why": why}
            )

        # ── 9. PEST & DISEASE RISK ────────────────────────────────────────────
        pest_kws = {"pest", "insect", "disease", "spray", "blight", "rust", "fungal", "control pest", "aphid"}
        if any(kw in q_lower for kw in pest_kws):
            target = crop or None
            if target:
                risk_res = pest_engine.predict_risk(target)
                what = f"Monitor {target} fields for early pest/disease signs."
                when = "Inspect today before 4 PM; apply neem spray (5ml/L) if damage found."
                why  = f"Current {target} pest risk: {risk_res['risk_level']}."
            else:
                what = "Scout your field edges and leaf undersides twice weekly."
                when = "Best done in morning when pests are less active."
                why  = "Early detection prevents major crop losses. Upload a leaf photo for disease diagnosis."
            # Also get RAG advice
            rag_docs = rag_engine.search(q, top_k=1)
            if rag_docs:
                what += f" {rag_docs[0]['content'][:120]}..."
            formatted = f"**Pest & Disease Advice{' for ' + target if target else ''}**:\n\n• **WHAT**: {what}\n• **WHEN**: {when}\n• **WHY**: {why}"
            sources = [d["title"] for d in rag_docs] if rag_docs else ["KrishiSaathi Pest Risk Model"]
            return _make_response(
                formatted, "PEST_DISEASE",
                sources=sources,
                structured={"what": what, "when": when, "why": why},
                actions=[{"label": "Upload Leaf Photo", "route": "/health"}]
            )

        # ── 10. MARKET & SELLING ──────────────────────────────────────────────
        market_kws = {"sell", "selling", "mandi", "price", "market", "rate", "cost of"}
        if any(kw in q_lower for kw in market_kws):
            target = crop or "Ginger"
            mkt_prices = market_service.get_prices(target)
            mkt_trend = market_service.get_market_trend(target)
            
            top_p = mkt_prices[0] if mkt_prices else {"modal_price": 4900, "mandi": "Hassan APMC", "date": "Today", "min_price": 4200, "max_price": 5400}
            
            what = f"Modal Mandi price for {target} at {top_p['mandi']} is ₹{top_p['modal_price']:,.0f}/quintal."
            when = f"Latest reported data date: {top_p['date']}."
            why = f"Price range across mandis is ₹{top_p['min_price']:,.0f} – ₹{top_p['max_price']:,.0f}/quintal ({mkt_trend.get('price_trend', 'stable')})."
            
            formatted = (f"**Market Intelligence for {target}**:\n\n"
                         f"• **Highest Reported Mandi**: {top_p['mandi']} ({top_p.get('state', 'Karnataka')})\n"
                         f"• **Modal Price**: ₹{top_p['modal_price']:,.0f} / quintal\n"
                         f"• **Price Range**: ₹{top_p['min_price']:,.0f} – ₹{top_p['max_price']:,.0f} / quintal\n"
                         f"• **Mandi Recommendation**: {mkt_trend.get('recommendation', 'Monitor nearby mandis before selling.')}")
            
            return _make_response(
                formatted, "MARKET",
                sources=["AGMARKNET / e-NAM Official Mandi Data"],
                structured={"what": what, "when": when, "why": why},
                actions=[{"label": "View Market Intelligence 2.0", "route": "/market"}]
            )

        # ── 11. FOLLOW-UP CONTEXT (only for ambiguous follow-up words like 'why?', 'what next?') ──
        follow_up_triggers = {"why?", "why", "what next?", "what next", "how?", "how", "and then?", "and then", "what should i do next?"}
        if (clean_q in follow_up_triggers or "follow-up:" in q_lower) and history:
            prev_user = [m for m in history if m.get("sender") in ("user", "human")]
            if prev_user:
                last_q = prev_user[-1].get("text", "")
                follow_up_q = f"{last_q} — context: {q}"
                # Re-route with combined context
                return self.route_and_process(follow_up_q, db, farmer, farm, history=[])

        # ── 12. GENERAL AGRICULTURE — RAG + LLM ───────────────────────────────
        rag_docs = rag_engine.search(q, top_k=2)
        rag_context = "\n---\n".join(
            [f"[{doc['title']}]: {doc['content']}" for doc in rag_docs]
        ) if rag_docs else ""

        # Build LLM context string
        ctx_parts = [f"User Question: '{q}'"]
        if farm_crop:      ctx_parts.append(f"Farmer's Crop: {farm_crop}")
        if farm_location:  ctx_parts.append(f"Location: {farm_location}")
        if farm_soil:      ctx_parts.append(f"Soil Type: {farm_soil}")
        if rag_context:    ctx_parts.append(f"Relevant Guidance:\n{rag_context}")
        prompt = "\n".join(ctx_parts)

        answer_text = llm_service.generate_response(
            prompt,
            context={"crop": farm_crop, "location": farm_location, "soil": farm_soil}
        )

        # Dynamic intent categorisation
        intent = "GENERAL_AGRICULTURE"
        if any(kw in q_lower for kw in ("npk", "fertilizer", "urea", "compost", "nutrient")):
            intent = "SOIL_FERTILIZER"
        elif any(kw in q_lower for kw in ("scheme", "government", "pm-kisan", "subsidy")):
            intent = "GOVERNMENT_SCHEME"
        elif any(kw in q_lower for kw in ("sow", "seed", "grow", "harvest", "crop rotation")):
            intent = "CROP"
        elif any(kw in q_lower for kw in ("soil", "black soil", "red soil", "fertility")):
            intent = "SOIL"

        sources = [doc["title"] for doc in rag_docs] if rag_docs else []

        return _make_response(answer_text, intent, sources=sources)


saathi_router = SaathiRouter()
