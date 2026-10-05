from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )
        
    hashed = get_password_hash(user_in.password)
    user = User(
        email=user_in.email.lower(),
        full_name=user_in.full_name,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/guest-demo", response_model=Token)
def get_guest_demo_token(db: Session = Depends(get_db)):
    """Provides a instant demo user token for 1-click live testing without registration"""
    demo_email = "guest.demo@airesume.io"
    user = db.query(User).filter(User.email == demo_email).first()
    if not user:
        user = User(
            email=demo_email,
            full_name="Alex Rivera (Demo User)",
            hashed_password=get_password_hash("demopassword123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(user.id, expires_delta=timedelta(days=30))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
