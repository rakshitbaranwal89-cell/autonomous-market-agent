"""Conservative sizing. Never creates leverage or borrowing."""

from decimal import Decimal

from .probability import ONE, ZERO, validate_probability


def fractional_kelly_fraction(
    win_probability: Decimal,
    decimal_odds: Decimal,
    fraction_cap: Decimal,
) -> Decimal:
    """Return a non-negative, capped Kelly fraction for a binary outcome."""
    validate_probability(win_probability)
    if decimal_odds <= ONE:
        raise ValueError("decimal odds must exceed 1")
    if not ZERO <= fraction_cap <= ONE:
        raise ValueError("fraction cap must be in [0, 1]")
    net_odds = decimal_odds - ONE
    full_kelly = ((net_odds * win_probability) - (ONE - win_probability)) / net_odds
    return min(max(full_kelly, ZERO), fraction_cap)


def stake_from_fraction(cash_available: Decimal, fraction: Decimal, max_notional: Decimal) -> Decimal:
    if cash_available < ZERO or max_notional < ZERO:
        raise ValueError("cash and cap must be non-negative")
    if not ZERO <= fraction <= ONE:
        raise ValueError("fraction must be in [0, 1]")
    return min(cash_available * fraction, max_notional)
