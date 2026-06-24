from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import distinct, func, select
from sqlalchemy.orm import Session

from backend.auth.security import get_current_user
from backend.database import get_db
from backend.models import FraudAlert, Transaction, User
from backend.schemas import AnalyticsSummary, FraudAlertRead, TransactionRead

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def summary(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_users = db.scalar(select(func.count(User.id))) or 0
    total_transactions = db.scalar(select(func.count(Transaction.transaction_id))) or 0
    total_money = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0))) or Decimal("0.00")
    fraud_alerts = db.scalar(select(func.count(FraudAlert.alert_id))) or 0
    active_senders = select(Transaction.sender_id).distinct()
    active_receivers = select(Transaction.receiver_id).distinct()
    active_users = db.scalar(
        select(func.count(distinct(User.id))).where(
            User.id.in_(active_senders.union(active_receivers))
        )
    ) or 0

    return AnalyticsSummary(
        total_users=total_users,
        total_transactions=total_transactions,
        total_money_transferred=Decimal(str(total_money)),
        fraud_alerts=fraud_alerts,
        active_users=active_users,
    )


@router.get("/transactions", response_model=list[TransactionRead])
def all_transactions(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(db.scalars(select(Transaction).order_by(Transaction.timestamp.desc()).limit(250)))


@router.get("/fraud-alerts", response_model=list[FraudAlertRead])
def fraud_alerts(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(db.scalars(select(FraudAlert).order_by(FraudAlert.created_at.desc()).limit(250)))