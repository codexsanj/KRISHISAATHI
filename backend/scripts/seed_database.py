import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.all_models import User, Farmer, Farm, Field, WeatherRecord, MarketRecord, Alert

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create demo user
        existing_user = db.query(User).filter(User.identifier == "demo@krishisaathi.app").first()
        if not existing_user:
            user = User(
                identifier="demo@krishisaathi.app",
                hashed_password=get_password_hash("demo1234"),
                role="FARMER"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            farmer = Farmer(
                user_id=user.id,
                name="Demo Farmer",
                phone="+91 98765 43210",
                email="demo@krishisaathi.app",
                preferred_language="Hindi"
            )
            db.add(farmer)
            db.commit()
            db.refresh(farmer)

            farm = Farm(
                farmer_id=farmer.id,
                name="Green Valley Farm",
                total_area="2.5 acres",
                location="Bengaluru, Karnataka",
                soil_type="Loamy",
                water_source="Canal irrigation",
                current_crop="Wheat",
                status="Healthy"
            )
            db.add(farm)
            db.commit()
            db.refresh(farm)

            field = Field(
                farm_id=farm.id,
                name="North Field",
                area_acres=2.5,
                current_crop="Wheat",
                crop_stage="Grain filling",
                soil_ph=6.5
            )
            db.add(field)
            db.commit()

        # 2. Seed weather records
        if not db.query(WeatherRecord).first():
            w = WeatherRecord(
                location="Bengaluru, Karnataka",
                temperature_c=32.0,
                humidity_pct=65.0,
                condition="Partly cloudy",
                rain_probability_pct=60.0,
                rainfall_mm=12.5
            )
            db.add(w)
            db.commit()

        # 3. Seed market records
        if not db.query(MarketRecord).first():
            m1 = MarketRecord(
                commodity="Wheat",
                mandi_name="Bengaluru Main Mandi",
                location="Bengaluru",
                modal_price_per_q=2250.0,
                min_price_per_q=2100.0,
                max_price_per_q=2400.0,
                trend_pct=4.2,
                record_date="2026-08-20"
            )
            m2 = MarketRecord(
                commodity="Cotton",
                mandi_name="Hubballi Mandi",
                location="Hubballi",
                modal_price_per_q=6420.0,
                min_price_per_q=6200.0,
                max_price_per_q=6700.0,
                trend_pct=3.2,
                record_date="2026-08-20"
            )
            db.add(m1)
            db.add(m2)
            db.commit()

        print("Database seeded successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
