from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.security import get_current_user
from backend.database import get_db
from backend.models import User
from backend.schemas import UserProfile, UserUpdate
from backend.services import user_service

router = APIRouter(tags=["users"])


@router.get("/profile", response_model=UserProfile)
def profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserProfile)
def update_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_user(db, current_user, payload)