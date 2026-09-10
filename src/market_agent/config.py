"""Configuration types. Secrets intentionally do not belong here."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class ExecutionMode(StrEnum):
    PAPER = "paper"
    LIVE = "live"


@dataclass(frozen=True)
class RiskLimits:
    """Hard limits enforced independently of any model output."""

    max_future_live_cap_inr: Decimal = Decimal("500.00")
    max_order_notional_inr: Decimal = Decimal("100.00")
    max_total_exposure_inr: Decimal = Decimal("500.00")
    max_daily_loss_inr: Decimal = Decimal("50.00")
    max_fractional_kelly: Decimal = Decimal("0.25")

    def __post_init__(self) -> None:
        if any(value < 0 for value in self.__dict__.values()):
            raise ValueError("Risk limits cannot be negative")
        if self.max_fractional_kelly > Decimal("1"):
            raise ValueError("Fractional Kelly cap cannot exceed 1")


@dataclass(frozen=True)
class AgentConfig:
    """The executable product policy. LIVE is deliberately unsupported."""

    mode: ExecutionMode = ExecutionMode.PAPER
    base_currency: str = "INR"
    limits: RiskLimits = RiskLimits()
    astra_enabled: bool = False
    monthly_api_budget_inr: Decimal = Decimal("0.00")

    def __post_init__(self) -> None:
        if self.mode is not ExecutionMode.PAPER:
            raise ValueError("Live execution is not implemented; only paper mode is allowed")
        if self.base_currency != "INR":
            raise ValueError("The initial deployment is India-first and uses INR only")
        if self.monthly_api_budget_inr < 0:
            raise ValueError("API budget cannot be negative")
