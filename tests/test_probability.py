from decimal import Decimal
import unittest

from market_agent.probability import brier_score, expected_value_per_unit
from market_agent.sizing import fractional_kelly_fraction


class ProbabilityTests(unittest.TestCase):
    def test_expected_value_and_kelly_are_conservative(self) -> None:
        self.assertEqual(expected_value_per_unit(Decimal("0.6"), Decimal("1"), Decimal("1")), Decimal("0.2"))
        fraction = fractional_kelly_fraction(Decimal("0.6"), Decimal("2"), Decimal("0.25"))
        self.assertEqual(fraction, Decimal("0.2"))

    def test_brier_score_rejects_invalid_outcomes(self) -> None:
        self.assertEqual(brier_score([(Decimal("0.5"), 1)]), Decimal("0.25"))
        with self.assertRaises(ValueError):
            brier_score([(Decimal("0.5"), 2)])
