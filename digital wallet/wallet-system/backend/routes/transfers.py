from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.security import get_current_user
from backend.database import get_db
from backend.models import User
from backend.schemas import TransactionRead, TransferCreate
from backend.services import wallet_service

router = APIRouter(tags=["transfers"])


@router.post("/transfer", response_model=TransactionRead, status_code=201)
def transfer(
    payload: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallet_service.transfer_money(db, current_user, payload)


@router.get("/transactions", response_model=list[TransactionRead])
def transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallet_service.list_user_transactions(db, current_user)
