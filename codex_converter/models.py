from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Status(StrEnum):
    CONVERTIBLE = "convertible"
    SKIPPED = "skipped"
    UNSUPPORTED = "unsupported"
    CONFLICT = "conflict"
    WRITTEN = "written"
    PLANNED = "planned"
    ERROR = "error"


@dataclass(frozen=True)
class ReportEntry:
    kind: str
    source: Path
    status: Status
    detail: str
    target: Path | None = None

