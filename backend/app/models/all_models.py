from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False) # Phone or Email
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="FARMER") # FARMER, EXPERT, ADMIN
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer_profile = relationship("Farmer", back_populates="user", uselist=False)

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    preferred_language = Column(String, default="Hindi")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="farmer_profile")
    farms = relationship("Farm", back_populates="farmer")

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    name = Column(String, nullable=False)
    total_area = Column(String, nullable=True) # e.g. "2.5 acres"
    location = Column(String, nullable=True) # e.g. "Bengaluru, Karnataka"
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    soil_type = Column(String, nullable=True) # e.g. "Loamy"
    water_source = Column(String, nullable=True) # e.g. "Canal irrigation"
    current_crop = Column(String, nullable=True) # e.g. "Wheat"
    status = Column(String, default="Healthy")
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="farms")
    fields = relationship("Field", back_populates="farm")

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    name = Column(String, nullable=False) # e.g. "North Field"
    area_acres = Column(Float, default=1.0)
    current_crop = Column(String, nullable=True)
    crop_stage = Column(String, default="Vegetative")
    soil_ph = Column(Float, default=6.5)
    nitrogen = Column(Float, default=40.0)
    phosphorus = Column(Float, default=30.0)
    potassium = Column(Float, default=20.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="fields")

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    temperature_c = Column(Float)
    humidity_pct = Column(Float)
    condition = Column(String)
    rain_probability_pct = Column(Float)
    rainfall_mm = Column(Float, default=0.0)
    is_forecast = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MarketRecord(Base):
    __tablename__ = "market_records"

    id = Column(Integer, primary_key=True, index=True)
    commodity = Column(String, index=True)
    mandi_name = Column(String, index=True)
    location = Column(String)
    modal_price_per_q = Column(Float)
    min_price_per_q = Column(Float)
    max_price_per_q = Column(Float)
    trend_pct = Column(Float, default=0.0)
    record_date = Column(String) # YYYY-MM-DD
    created_at = Column(DateTime, default=datetime.utcnow)

class Advisory(Base):
    __tablename__ = "advisories"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    category = Column(String) # Priority, Irrigation, Disease, Pest, Market
    title = Column(String)
    due_label = Column(String, nullable=True)
    what_text = Column(Text)
    when_text = Column(Text)
    why_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    alert_type = Column(String) # weather, pest, disease, market, irrigation
    title = Column(String)
    description = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    title = Column(String, default="New Conversation")
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    sender = Column(String) # "user" or "saathi" / "assistant"
    text = Column(Text, nullable=True)
    intent = Column(String, nullable=True)
    sources = Column(JSON, nullable=True)
    structured_data = Column(JSON, nullable=True)
    is_what_if = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    query = Column(Text)
    parsed_params = Column(JSON)
    baseline_state = Column(JSON)
    simulated_state = Column(JSON)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExpertCase(Base):
    __tablename__ = "expert_cases"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    crop = Column(String)
    issue_description = Column(Text)
    image_url = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    status = Column(String, default="OPEN") # OPEN, RESOLVED
    expert_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CropCycle(Base):
    __tablename__ = "crop_cycles"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)
    crop_name = Column(String, nullable=False)
    variety = Column(String, nullable=True)
    area_acres = Column(Float, default=1.0)
    sowing_date = Column(String, nullable=True) # YYYY-MM-DD
    expected_harvest_date = Column(String, nullable=True) # YYYY-MM-DD
    current_stage = Column(String, default="Sowing/Germination")
    status = Column(String, default="ACTIVE") # ACTIVE, COMPLETED, CANCELLED
    season = Column(String, nullable=True) # Kharif, Rabi, Zaid
    previous_crop = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class FarmActivity(Base):
    __tablename__ = "farm_activities"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)
    crop_cycle_id = Column(Integer, ForeignKey("crop_cycles.id"), nullable=True)
    activity_type = Column(String, nullable=False, index=True) # e.g. LAND_PREPARATION, SEEDING, IRRIGATION, FERTILIZER, PEST_INSPECTION, DISEASE_DETECTED, HARVEST, SALE, EXPENSE
    activity_date = Column(String, nullable=False, index=True) # YYYY-MM-DD
    activity_time = Column(String, nullable=True) # HH:MM
    description = Column(Text, nullable=False)
    quantity = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    cost = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    image_reference = Column(String, nullable=True)
    weather_snapshot = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class HarvestRecord(Base):
    __tablename__ = "harvest_records"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    crop_cycle_id = Column(Integer, ForeignKey("crop_cycles.id"), nullable=False)
    harvest_date = Column(String, nullable=False)
    yield_quantity = Column(Float, nullable=False)
    yield_unit = Column(String, default="Quintals")
    quality_grade = Column(String, default="Grade A")
    storage_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SaleRecord(Base):
    __tablename__ = "sale_records"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    crop_cycle_id = Column(Integer, ForeignKey("crop_cycles.id"), nullable=True)
    harvest_record_id = Column(Integer, ForeignKey("harvest_records.id"), nullable=True)
    sale_date = Column(String, nullable=False)
    buyer_type = Column(String, default="Mandi Trader")
    mandi_name = Column(String, nullable=True)
    quantity_sold = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False) # e.g. per Quintal
    total_revenue = Column(Float, nullable=False)
    transport_cost = Column(Float, default=0.0)
    net_revenue = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExpenseRecord(Base):
    __tablename__ = "expense_records"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    crop_cycle_id = Column(Integer, ForeignKey("crop_cycles.id"), nullable=True)
    category = Column(String, nullable=False) # SEED, FERTILIZER, PESTICIDE, LABOUR, IRRIGATION, EQUIPMENT, TRANSPORT, OTHER
    amount = Column(Float, nullable=False)
    expense_date = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    crop_cycle_id = Column(Integer, ForeignKey("crop_cycles.id"), nullable=True)
    engine_name = Column(String, nullable=False)
    recommendation_type = Column(String, nullable=False) # CROP_SELECTION, SOWING_WINDOW, DAILY_PLAN, IRRIGATION, MARKET_SELL
    structured_payload = Column(JSON, nullable=False)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class RegionalCropData(Base):
    __tablename__ = "regional_crop_data"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True, nullable=False)
    district = Column(String, index=True, nullable=False)
    season = Column(String, index=True, nullable=False)
    crop_name = Column(String, index=True, nullable=False)
    area_ha = Column(Float, default=0.0)
    production_tonnes = Column(Float, default=0.0)
    yield_kg_ha = Column(Float, default=0.0)
    data_year = Column(Integer, default=2024)

