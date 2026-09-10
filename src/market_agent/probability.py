"""Deterministic probability, EV, and calibration calculations."""

from collections.abc import Iterable
from decimal import Decimal


ZERO = Decimal("0")
ONE = Decimal("1")


def validate_probability(value: Decimal) -> Decimal:
    if not ZERO <= value <= ONE:
        raise ValueError("probability must be in [0, 1]")
    return value


def implied_probability(decimal_odds: Decimal) -> Decimal:
    if decimal_odds <= ONE:
        raise ValueError("decimal odds must exceed 1")
    return ONE / decimal_odds


def expected_value_per_unit(win_probability: Decimal, win_payout: Decimal, loss: Decimal) -> Decimal:
    """Expected net profit for a one-unit stake, after caller-supplied costs."""
    validate_probability(win_probability)
    if win_payout < ZERO or loss < ZERO:
        raise ValueError("payout and loss must be non-negative magnitudes")
    return (win_probability * win_payout) - ((ONE - win_probability) * loss)


def brier_score(predictions_and_outcomes: Iterable[tuple[Decimal, int]]) -> Decimal:
    """Lower is better. Outcomes must be 0 or 1."""
    values: list[Decimal] = []
    for probability, outcome in predictions_and_outcomes:
        validate_probability(probability)
        if outcome not in (0, 1):
            raise ValueError("outcome must be 0 or 1")
        values.append((probability - Decimal(outcome)) ** 2)
    if not values:
        raise ValueError("at least one prediction is required")
    return sum(values, ZERO) / Decimal(len(values))
