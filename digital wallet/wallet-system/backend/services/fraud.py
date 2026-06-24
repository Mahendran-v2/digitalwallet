from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import FraudAlert, Transaction
from fraud_engine import evaluate_transaction


def evaluate_and_record(db: Session, transaction: Transaction) -> list[FraudAlert]:
    one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

    transfer_count = db.scalar(
        select(func.count(Transaction.transaction_id)).where(
            Transaction.sender_id == transaction.sender_id,
            Transaction.timestamp >= one_minute_ago,
        )
    ) or 0

    average_amount = db.scalar(
        select(func.avg(Transaction.amount)).where(
            Transaction.sender_id == transaction.sender_id,
            Transaction.transaction_id != transaction.transaction_id,
        )
    )
    average_decimal = Decimal(str(average_amount)) if average_amount is not None else None

    rule_hits = evaluate_transaction(
        amount=Decimal(str(transaction.amount)),
        transfers_last_minute=int(transfer_count),
        average_amount=average_decimal,
    )

    alerts: list[FraudAlert] = []
    for reason, score in rule_hits:
        alert = FraudAlert(transaction_id=transaction.transaction_id, reason=reason, risk_score=min(score, 100))
        alerts.append(alert)
        db.add(alert)

    if alerts:
        transaction.status = "flagged"
        db.add(transaction)

    return alerts
