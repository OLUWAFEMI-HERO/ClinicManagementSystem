from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from sqlmodel import Session
from ..models import User, PatientProfile, DoctorProfile
from ..database import engine
from ..auth import get_user_by_username, get_password_hash, create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, role: str = "patient", full_name: str = None):
    if role not in ("patient", "doctor"):
        raise HTTPException(status_code=400, detail="Invalid role")
    with Session(engine) as session:
        if get_user_by_username(username):
            raise HTTPException(400, detail="Username already exists")
        user = User(username=username, full_name=full_name, role=role,
                    hashed_password=get_password_hash(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        profile = PatientProfile(user_id=user.id) if role == "patient" else DoctorProfile(user_id=user.id)
        session.add(profile)
        session.commit()
        return {"msg": "registered", "user_id": user.id}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")
    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}
