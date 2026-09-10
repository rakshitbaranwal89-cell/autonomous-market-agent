"""Realized-P&L allocation and separate operating-cost accounting."""

from dataclasses import dataclass
from decimal import Decimal


ZERO = Decimal("0")


@dataclass(frozen=True)
class ProfitAllocation:
    realized_net_profit: Decimal
    agent_reserve: Decimal
    user_allocation: Decimal


def allocate_realized_profit(realized_net_profit: Decimal) -> ProfitAllocation:
    """Allocate only positive realized net profit; losses are never allocated."""
    distributable = max(realized_net_profit, ZERO)
    agent_reserve = distributable * Decimal("0.70")
    user_allocation = distributable - agent_reserve
    return ProfitAllocation(realized_net_profit, agent_reserve, user_allocation)


@dataclass
class OperatingCostLedger:
    """Costs do not alter a trade's permitted risk or sizing."""

    monthly_budget: Decimal
    spent: Decimal = ZERO

    def __post_init__(self) -> None:
        if self.monthly_budget < ZERO or self.spent < ZERO:
            raise ValueError("budgets and spending cannot be negative")

    @property
    def remaining(self) -> Decimal:
        return max(self.monthly_budget - self.spent, ZERO)

    def can_afford(self, proposed_cost: Decimal) -> bool:
        return proposed_cost >= ZERO and proposed_cost <= self.remaining

    def record(self, actual_cost: Decimal) -> None:
        if actual_cost < ZERO:
            raise ValueError("cost cannot be negative")
        if not self.can_afford(actual_cost):
            raise ValueError("operating-cost budget exceeded")
        self.spent += actual_cost
