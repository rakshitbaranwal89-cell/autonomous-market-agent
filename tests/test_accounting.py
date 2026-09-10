from decimal import Decimal
import unittest

from market_agent.accounting import OperatingCostLedger, allocate_realized_profit


class AccountingTests(unittest.TestCase):
    def test_profit_is_split_70_30_only_when_realized_profit_is_positive(self) -> None:
        allocation = allocate_realized_profit(Decimal("100"))
        self.assertEqual(allocation.agent_reserve, Decimal("70.00"))
        self.assertEqual(allocation.user_allocation, Decimal("30.00"))
        loss = allocate_realized_profit(Decimal("-5"))
        self.assertEqual(loss.agent_reserve, Decimal("0"))
        self.assertEqual(loss.user_allocation, Decimal("0"))

    def test_cost_budget_fails_closed(self) -> None:
        ledger = OperatingCostLedger(Decimal("10"))
        ledger.record(Decimal("9"))
        self.assertFalse(ledger.can_afford(Decimal("2")))
        with self.assertRaises(ValueError):
            ledger.record(Decimal("2"))
