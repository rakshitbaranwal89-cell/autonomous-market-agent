"""Paper fills with explicit fee, spread, and slippage assumptions."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from .models import Fill, OrderIntent, Quote, Side


@dataclass(frozen=True)
class ExecutionCosts:
    fee_rate: Decimal = Decimal("0.001")
    slippage_bps: Decimal = Decimal("5")

    def __post_init__(self) -> None:
        if self.fee_rate < 0 or self.slippage_bps < 0:
            raise ValueError("cost assumptions cannot be negative")


class PaperBroker:
    """Provider-neutral simulation; it accepts quotes rather than fetching markets."""

    def __init__(self, costs: ExecutionCosts = ExecutionCosts()) -> None:
        self._costs = costs

    def execute(self, intent: OrderIntent, quote: Quote) -> Fill:
        if intent.symbol != quote.symbol:
            raise ValueError("quote symbol does not match order")
        base = quote.ask if intent.side is Side.BUY else quote.bid
        slip = self._costs.slippage_bps / Decimal("10000")
        price = base * (Decimal("1") + slip if intent.side is Side.BUY else Decimal("1") - slip)
        fees = intent.quantity * price * self._costs.fee_rate
        return Fill(
            order_id=intent.order_id,
            symbol=intent.symbol,
            side=intent.side,
            quantity=intent.quantity,
            price=price,
            fees=fees,
            filled_at=datetime.now(timezone.utc),
        )
