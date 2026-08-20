from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.models.all_models import User, Farmer, Farm
from app.schemas.all_schemas import UserRegister, UserLogin, Token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Resolve the current authenticated user from the JWT token.
    Falls back to the first DB user ONLY when no token is present (dev mode / tests).
    NEVER creates a fake 'Demo Farmer' for real users.
    """
    if not token:
        # No token — dev/test fallback to first user in DB
        user = db.query(User).first()
        if not user:
            return None, None
        farmer = db.query(Farmer).filter(Farmer.user_id == user.id).first()
        return user, farmer

    sub = decode_access_token(token)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please log in again."
        )

    # Lookup user by integer ID or string identifier
    user = None
    if str(sub).isdigit():
        user = db.query(User).filter(User.id == int(sub)).first()
    if not user:
        user = db.query(User).filter(User.identifier == str(sub)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found. Please log in again."
        )

    farmer = db.query(Farmer).filter(Farmer.user_id == user.id).first()
    # Do NOT auto-create Demo Farmer. Return None farmer if profile incomplete.
    return user, farmer


@router.post("/register", response_model=Token)
def register(req: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.identifier == req.identifier).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this phone/email already exists")

    hashed = get_password_hash(req.password)
    user = User(identifier=req.identifier, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    is_email = "@" in req.identifier
    farmer = Farmer(
        user_id=user.id,
        email=req.identifier if is_email else None,
        phone=req.identifier if not is_email else None
    )
    db.add(farmer)
    db.commit()
    db.refresh(farmer)

    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "farmer": {"id": farmer.id, "name": farmer.name, "phone": farmer.phone, "email": farmer.email}
    }


@router.post("/login", response_model=Token)
def login(req: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.identifier == req.identifier).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid phone/email or password")

    farmer = db.query(Farmer).filter(Farmer.user_id == user.id).first()
    farm = db.query(Farm).filter(Farm.farmer_id == farmer.id).first() if farmer else None

    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "farmer": {
            "id": farmer.id if farmer else None,
            "name": farmer.name if farmer else None,
            "phone": farmer.phone if farmer else None,
            "email": farmer.email if farmer else None
        },
        "farm": {
            "id": farm.id,
            "name": farm.name,
            "crop": farm.current_crop,
            "current_crop": farm.current_crop,
            "area": farm.total_area,
            "location": farm.location,
            "soil": farm.soil_type,
            "soil_type": farm.soil_type,
            "waterSource": farm.water_source,
            "water_source": farm.water_source,
            "status": farm.status
        } if farm else None
    }


@router.get("/me")
def me(auth_data=Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    farm = db.query(Farm).filter(Farm.farmer_id == farmer.id).first() if farmer else None

    return {
        "isAuthenticated": True,
        "onboardingComplete": bool(farm),
        "farmer": {
            "id": farmer.id if farmer else None,
            "name": farmer.name if farmer else None,
            "phone": farmer.phone if farmer else None,
            "email": farmer.email if farmer else None
        } if farmer else None,
        # Return ACTUAL farm data or None — NEVER fake demo data
        "farm": {
            "id": farm.id,
            "name": farm.name,
            "crop": farm.current_crop,
            "current_crop": farm.current_crop,
            "area": farm.total_area,
            "location": farm.location,
            "soil": farm.soil_type,
            "soil_type": farm.soil_type,
            "waterSource": farm.water_source,
            "water_source": farm.water_source,
            "status": farm.status
        } if farm else None
    }
