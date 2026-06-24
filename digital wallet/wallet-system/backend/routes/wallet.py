from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.security import get_current_user
from backend.database import get_db
from backend.models import User
from backend.schemas import AmountRequest, WalletRead
from backend.services import wallet_service

router = APIRouter(tags=["wallets"])


@router.get("/wallet", response_model=WalletRead)
def wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallet_service.get_wallet_for_user(db, current_user.id)


@router.post("/wallet/add", response_model=WalletRead)
def add_money(
    payload: AmountRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallet_service.add_money(db, current_user, payload)


@router.post("/wallet/withdraw", response_model=WalletRead)
def withdraw_money(
    payload: AmountRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallet_service.withdraw_money(db, current_user, payload)