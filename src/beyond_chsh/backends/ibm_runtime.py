"""IBM Quantum hardware backend via Qiskit Runtime (SamplerV2, counts route).

Design choices driven by the project requirements:
  * Credentials come from environment variables (.env), never from source.
  * Uses SamplerV2 so we recover full counts -> joint distributions (the
    Estimator route returns only expectation values and discards the
    distribution information this project studies).
  * Records job ids, backend name, shots, transpiled depth/gate counts, and
    any available calibration metadata.
  * Sets ``mode='hardware'`` ONLY here, and only for real-device execution.

API COMPATIBILITY: the Qiskit Runtime API changes across releases. The calls
below target qiskit-ibm-runtime ~0.45 and qiskit ~2.3 but MUST be verified
against the official documentation before a real run:
    https://docs.quantum.ibm.com/
Nothing in this module is executed by the default test suite.
"""

from __future__ import annotations

import os

from ..circuits.bell_states import BellState
from ..circuits.chsh import build_all_chsh_circuits
from ..data.schemas import ExperimentRecord, SettingRecord, new_experiment_id
from ..theory.correlators import ALICE_ANGLES, BOB_ANGLES, SETTINGS


def _load_service():
    """Create a QiskitRuntimeService from environment credentials."""
    from qiskit_ibm_runtime import QiskitRuntimeService

    token = os.environ.get("IBM_QUANTUM_TOKEN")
    instance = os.environ.get("IBM_QUANTUM_INSTANCE") or None
    if not token:
        raise RuntimeError(
            "IBM_QUANTUM_TOKEN not set. Copy .env.example to .env and fill it in."
        )
    return QiskitRuntimeService(channel="ibm_quantum", token=token, instance=instance)


def run_on_hardware(
    shots: int = 5000,
    *,
    backend_name: str | None = None,
    optimization_level: int = 1,
    state: BellState = BellState.PHI_PLUS,
) -> ExperimentRecord:
    """Run the four CHSH circuits on real IBM hardware and return a full record.

    Parameters
    ----------
    shots:
        Shots per circuit.
    backend_name:
        Explicit backend (e.g. 'ibm_torino'). If None, pick the least busy
        operational device with >= 2 qubits.
    optimization_level:
        Transpiler optimization level.
    state:
        Bell state to prepare.
    """
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import SamplerV2 as Sampler

    service = _load_service()
    if backend_name:
        backend = service.backend(backend_name)
    else:
        backend = service.least_busy(simulator=False, operational=True, min_num_qubits=2)

    pm = generate_preset_pass_manager(backend=backend, optimization_level=optimization_level)

    circuits = build_all_chsh_circuits(state=state)
    isa_circuits = {xy: pm.run(qc) for xy, qc in circuits.items()}

    sampler = Sampler(mode=backend)
    sampler.options.default_shots = shots

    job = sampler.run(list(isa_circuits.values()))
    result = job.result()

    settings: list[SettingRecord] = []
    depth: dict[str, int] = {}
    for idx, xy in enumerate(SETTINGS):
        x, y = xy
        isa = isa_circuits[xy]
        # SamplerV2 returns per-pub bit arrays; get_counts() aggregates them.
        counts = result[idx].data.meas.get_counts()
        settings.append(
            SettingRecord(
                x=x,
                y=y,
                alice_angle=ALICE_ANGLES[x],
                bob_angle=BOB_ANGLES[y],
                counts={k: int(v) for k, v in counts.items()},
                shots=shots,
            )
        )
        depth[f"{x}{y}"] = isa.depth()

    try:
        props = backend.properties()
        calibration = {"last_update_date": str(getattr(props, "last_update_date", None))}
    except Exception:  # noqa: BLE001
        calibration = None

    return ExperimentRecord(
        experiment_id=new_experiment_id(),
        mode="hardware",
        config={
            "shots": shots,
            "optimization_level": optimization_level,
            "state": state.value,
        },
        settings=settings,
        backend_name=backend.name,
        job_ids=[job.job_id()],
        calibration=calibration,
        transpiled_depth=depth,
        notes="Executed on real IBM Quantum hardware via SamplerV2.",
    )
