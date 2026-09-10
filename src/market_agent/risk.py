"""Hard, explainable pre-trade controls. These are not AI-overridable."""

from dataclasses import dataclass
from decimal import Decimal

from .config import AgentConfig, ExecutionMode
from .models import OrderIntent, Quote


@dataclass(frozen=True)
class RiskDecision:
    approved: bool
    reasons: tuple[str, ...]
    proposed_notional: Decimal


class RiskEngine:
    def __init__(self, config: AgentConfig) -> None:
        self._config = config

    def assess(
        self,
        intent: OrderIntent,
        quote: Quote,
        cash_available: Decimal,
        current_exposure: Decimal,
        realized_daily_pnl: Decimal,
    ) -> RiskDecision:
        reasons: list[str] = []
        proposed_notional = intent.quantity * (quote.ask if intent.side.value == "buy" else quote.bid)
        limits = self._config.limits
        if self._config.mode is not ExecutionMode.PAPER:
            reasons.append("live execution is disabled")
        if quote.symbol != intent.symbol:
            reasons.append("quote symbol does not match order symbol")
        if proposed_notional > cash_available:
            reasons.append("insufficient settled paper cash; borrowing is prohibited")
        if proposed_notional > limits.max_order_notional_inr:
            reasons.append("order exceeds deterministic notional cap")
        if current_exposure + proposed_notional > limits.max_total_exposure_inr:
            reasons.append("order exceeds total exposure cap")
        if realized_daily_pnl <= -limits.max_daily_loss_inr:
            reasons.append("daily loss limit reached")
        if intent.model_probability is None or intent.market_probability is None:
            reasons.append("missing probability evidence")
        return RiskDecision(not reasons, tuple(reasons), proposed_notional)
