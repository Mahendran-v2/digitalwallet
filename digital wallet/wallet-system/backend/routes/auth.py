from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.security import create_access_token
from backend.database import get_db
from backend.schemas import Token, UserCreate, UserLogin, UserProfile
from backend.services import user_service

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserProfile, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, payload)
    return Token(access_token=create_access_token(user.id), user=user)

Filter files
