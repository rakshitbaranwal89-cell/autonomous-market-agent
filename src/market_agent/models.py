"""Small, provider-independent domain types."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum


class Side(StrEnum):
    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True)
class Quote:
    symbol: str
    bid: Decimal
    ask: Decimal
    observed_at: datetime

    def __post_init__(self) -> None:
        if not self.symbol:
            raise ValueError("symbol is required")
        if self.bid <= 0 or self.ask <= 0 or self.bid > self.ask:
            raise ValueError("quote must have positive bid <= ask")

    @property
    def mid(self) -> Decimal:
        return (self.bid + self.ask) / Decimal("2")


@dataclass(frozen=True)
class OrderIntent:
    order_id: str
    symbol: str
    side: Side
    quantity: Decimal
    rationale: str
    model_probability: Decimal | None = None
    market_probability: Decimal | None = None
    created_at: datetime = datetime.now(timezone.utc)

    def __post_init__(self) -> None:
        if not self.order_id or not self.symbol or not self.rationale:
            raise ValueError("order_id, symbol, and rationale are required")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        for probability in (self.model_probability, self.market_probability):
            if probability is not None and not Decimal("0") <= probability <= Decimal("1"):
                raise ValueError("probabilities must be between 0 and 1")


@dataclass(frozen=True)
class Fill:
    order_id: str
    symbol: str
    side: Side
    quantity: Decimal
    price: Decimal
    fees: Decimal
    filled_at: datetime

    @property
    def notional(self) -> Decimal:
        return self.quantity * self.price
