# Autonomous Market Agent

An India-first foundation for researching and paper-testing market strategies. It is deliberately **not** a live-trading system.

## Non-negotiable safety model

- Paper trading is the only supported execution mode.
- The live-money ceiling is represented as a future policy value (`INR 500`) but no code path can place a live order.
- No leverage, borrowing, deposits, withdrawals, transfers, geographic workarounds, or broker credentials.
- Deterministic risk code decides whether a proposed order is valid. Research/AI code cannot override it.
- No return claims. A strategy without out-of-sample evidence after costs is rejected.
- Every order decision, fill, and cost is auditable.
- API/research costs are separate from trading P&L. Running out of operating budget disables paid research; it never raises trading risk.

## What exists now

- Decimal-based probability, expected-value, sizing, and risk modules.
- A realistic-enough paper execution model with spread, slippage, and fee handling.
- A backtest runner with explicit in-sample/out-of-sample split metrics.
- Realized-profit accounting: 70% operating/reinvestment reserve, 30% user allocation.
- An optional, disabled-by-default Astra interface that can only return research notes.
- JSONL audit logging and standard-library unit tests.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Configuration

Copy `config.example.toml` to a local file outside version control. Do not put secrets in this repository. The `OPENAI_API_KEY` environment variable is intentionally only read when the optional Astra layer is enabled by a human-controlled configuration.

## Live trading

Live trading is out of scope. Any future proposal requires a fresh legal/compliance review, broker-specific implementation review, explicit user approval, and a separate security threat model.
