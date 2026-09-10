"""Append-only JSON Lines audit log for decisions and simulated fills."""

import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any


def _json_default(value: Any) -> str | dict[str, Any]:
    if isinstance(value, (datetime, date, Decimal)):
        return str(value)
    if is_dataclass(value):
        return asdict(value)
    raise TypeError(f"cannot serialize {type(value)!r}")


class AuditLog:
    def __init__(self, path: Path) -> None:
        self._path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, payload: Any) -> None:
        record = {"event_type": event_type, "payload": payload, "recorded_at": datetime.utcnow().isoformat() + "Z"}
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, default=_json_default, sort_keys=True) + "\n")
