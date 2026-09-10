from datetime import datetime, timezone
from decimal import Decimal
import unittest

from market_agent.config import AgentConfig, RiskLimits
from market_agent.models import OrderIntent, Quote, Side
from market_agent.paper import ExecutionCosts, PaperBroker
from market_agent.risk import RiskEngine


class RiskAndPaperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.quote = Quote("DEMO", Decimal("9"), Decimal("10"), datetime.now(timezone.utc))
        self.intent = OrderIntent("o-1", "DEMO", Side.BUY, Decimal("5"), "paper test", Decimal("0.6"), Decimal("0.5"))

    def test_hard_risk_limit_rejects_oversized_order(self) -> None:
        config = AgentConfig(limits=RiskLimits(max_order_notional_inr=Decimal("20")))
        decision = RiskEngine(config).assess(self.intent, self.quote, Decimal("100"), Decimal("0"), Decimal("0"))
        self.assertFalse(decision.approved)
        self.assertIn("order exceeds deterministic notional cap", decision.reasons)

    def test_paper_buy_crosses_ask_and_applies_costs(self) -> None:
        fill = PaperBroker(ExecutionCosts(Decimal("0.001"), Decimal("10"))).execute(self.intent, self.quote)
        self.assertGreater(fill.price, self.quote.ask)
        self.assertGreater(fill.fees, Decimal("0"))
