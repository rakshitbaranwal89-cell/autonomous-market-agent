"""Optional research-only boundary for a future Astra integration.

No API request is made here. A production adapter must be enabled by explicit local
configuration, charge its cost ledger before requests, and emit auditable research
notes. It must never be passed a broker credential or risk-control capability.
"""

from dataclasses import dataclass

from .accounting import OperatingCostLedger


@dataclass(frozen=True)
class ResearchNote:
    text: str
    source: str = "astra"


class AstraResearchGate:
    def __init__(self, enabled: bool, cost_ledger: OperatingCostLedger) -> None:
        self._enabled = enabled
        self._cost_ledger = cost_ledger

    def permit_request(self, estimated_cost_inr: object) -> bool:
        """Only a budget gate; the caller still needs an explicit integration."""
        if not self._enabled:
            return False
        if not hasattr(estimated_cost_inr, "as_tuple"):
            raise TypeError("estimated cost must be a Decimal")
        return self._cost_ledger.can_afford(estimated_cost_inr)  # type: ignore[arg-type]
