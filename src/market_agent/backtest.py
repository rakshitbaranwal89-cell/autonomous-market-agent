"""Transparent backtest calculations with an explicit out-of-sample partition."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class TradeOutcome:
    net_pnl: Decimal


@dataclass(frozen=True)
class SegmentMetrics:
    trades: int
    net_pnl: Decimal
    win_rate: Decimal
    max_drawdown: Decimal


@dataclass(frozen=True)
class BacktestReport:
    in_sample: SegmentMetrics
    out_of_sample: SegmentMetrics


def metrics(outcomes: list[TradeOutcome]) -> SegmentMetrics:
    if not outcomes:
        return SegmentMetrics(0, Decimal("0"), Decimal("0"), Decimal("0"))
    equity = peak = Decimal("0")
    max_drawdown = Decimal("0")
    wins = 0
    for outcome in outcomes:
        equity += outcome.net_pnl
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, peak - equity)
        wins += outcome.net_pnl > 0
    return SegmentMetrics(
        trades=len(outcomes),
        net_pnl=equity,
        win_rate=Decimal(wins) / Decimal(len(outcomes)),
        max_drawdown=max_drawdown,
    )


def evaluate_out_of_sample(outcomes: list[TradeOutcome], train_fraction: Decimal = Decimal("0.70")) -> BacktestReport:
    if not Decimal("0") < train_fraction < Decimal("1"):
        raise ValueError("train_fraction must be between 0 and 1")
    cut = int(len(outcomes) * train_fraction)
    return BacktestReport(metrics(outcomes[:cut]), metrics(outcomes[cut:]))
