from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from backend.models import Transaction, User, Wallet
from backend.schemas import AmountRequest, TransferCreate
from backend.services.fraud_service import evaluate_and_record


def get_wallet_for_user(db: Session, user_id: int) -> Wallet:
    wallet = db.scalar(select(Wallet).where(Wallet.user_id == user_id))
    if wallet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return wallet


def add_money(db: Session, user: User, payload: AmountRequest) -> Wallet:
    wallet = get_wallet_for_user(db, user.id)
    wallet.balance = Decimal(str(wallet.balance)) + payload.amount
    wallet.updated_at = datetime.now(timezone.utc)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def withdraw_money(db: Session, user: User, payload: AmountRequest) -> Wallet:
    wallet = get_wallet_for_user(db, user.id)
    if Decimal(str(wallet.balance)) < payload.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

    wallet.balance = Decimal(str(wallet.balance)) - payload.amount
    wallet.updated_at = datetime.now(timezone.utc)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def transfer_money(db: Session, sender: User, payload: TransferCreate) -> Transaction:
    if sender.id == payload.receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot transfer money to yourself")

    receiver = db.get(User, payload.receiver_id)
    if receiver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    sender_wallet = get_wallet_for_user(db, sender.id)
    receiver_wallet = get_wallet_for_user(db, receiver.id)

    if Decimal(str(sender_wallet.balance)) < payload.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

    sender_wallet.balance = Decimal(str(sender_wallet.balance)) - payload.amount
    receiver_wallet.balance = Decimal(str(receiver_wallet.balance)) + payload.amount
    sender_wallet.updated_at = datetime.now(timezone.utc)
    receiver_wallet.updated_at = datetime.now(timezone.utc)

    transaction = Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=payload.amount,
        status="success",
    )

    db.add_all([sender_wallet, receiver_wallet, transaction])
    db.flush()
    evaluate_and_record(db, transaction)
    db.commit()

    return db.scalar(
        select(Transaction)
        .options(selectinload(Transaction.fraud_alerts))
        .where(Transaction.transaction_id == transaction.transaction_id)
    )


def list_user_transactions(db: Session, user: User) -> list[Transaction]:
    return list(
        db.scalars(
            select(Transaction)
            .options(selectinload(Transaction.fraud_alerts))
            .where(or_(Transaction.sender_id == user.id, Transaction.receiver_id == user.id))
            .order_by(Transaction.timestamp.desc())
        )
    )
