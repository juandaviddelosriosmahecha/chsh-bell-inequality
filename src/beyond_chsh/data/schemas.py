"""Dataclasses describing a reproducible CHSH experiment record.

Every run captures enough metadata to reproduce the analysis without re-running
hardware: a unique id, the configuration, software versions, random seeds,
backend identity, raw counts, and execution metadata. Records serialise to
plain JSON (open format).
"""

from __future__ import annotations

import platform
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def new_experiment_id() -> str:
    """Return a short unique experiment id: timestamp + random suffix."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}-{uuid.uuid4().hex[:8]}"


def _software_versions() -> dict[str, str]:
    versions = {"python": sys.version.split()[0], "platform": platform.platform()}
    for mod in ("numpy", "scipy", "qiskit", "qiskit_aer", "qiskit_ibm_runtime"):
        try:
            m = __import__(mod)
            versions[mod] = getattr(m, "__version__", "unknown")
        except Exception:  # noqa: BLE001 - optional deps may be absent
            versions[mod] = "not installed"
    return versions


@dataclass
class SettingRecord:
    """Raw counts and resolved angles for one CHSH setting (x, y)."""

    x: int
    y: int
    alice_angle: float
    bob_angle: float
    counts: dict[str, int]
    shots: int


@dataclass
class ExperimentRecord:
    """A complete, self-describing CHSH experiment.

    ``mode`` is one of 'ideal', 'noisy', 'hardware' and is the single source of
    truth for whether results came from real hardware. It must never be set to
    'hardware' for a simulated run.
    """

    experiment_id: str
    mode: str
    config: dict
    settings: list[SettingRecord]
    backend_name: str | None = None
    job_ids: list[str] = field(default_factory=list)
    seed: int | None = None
    calibration: dict | None = None
    transpiled_depth: dict | None = None
    created_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    software: dict = field(default_factory=_software_versions)
    notes: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> ExperimentRecord:
        settings = [SettingRecord(**s) for s in d.pop("settings")]
        return cls(settings=settings, **d)
