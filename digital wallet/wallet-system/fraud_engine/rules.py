from __future__ import annotations

from decimal import Decimal


def evaluate_transaction(
    amount: Decimal,
    transfers_last_minute: int,
    average_amount: Decimal | None,
) -> list[tuple[str, int]]:
    alerts: list[tuple[str, int]] = []

    if amount > Decimal("50000.00"):
        alerts.append(("Transaction amount is greater than INR 50,000", 45))

    if transfers_last_minute > 10:
        alerts.append(("More than 10 transfers from this user in one minute", 35))

    if average_amount and average_amount > 0 and amount > (average_amount * Decimal("5")):
        alerts.append(("Transfer amount is more than 5x this user's average transfer", 30))

    return alerts