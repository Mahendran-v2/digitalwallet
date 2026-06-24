from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile


class WalletRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_id: int
    user_id: int
    balance: Decimal
    updated_at: datetime


class AmountRequest(BaseModel):
    amount: Decimal = Field(gt=Decimal("0.00"), max_digits=14, decimal_places=2)


class TransferCreate(BaseModel):
    receiver_id: int = Field(gt=0)
    amount: Decimal = Field(gt=Decimal("0.00"), max_digits=14, decimal_places=2)


class FraudAlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_id: int
    transaction_id: int
    reason: str
    risk_score: int
    created_at: datetime


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: int
    sender_id: int
    receiver_id: int
    amount: Decimal
    status: str
    timestamp: datetime
    fraud_alerts: list[FraudAlertRead] = []


class AnalyticsSummary(BaseModel):
    total_users: int
    total_transactions: int
    total_money_transferred: Decimal
    fraud_alerts: int
    active_users: int