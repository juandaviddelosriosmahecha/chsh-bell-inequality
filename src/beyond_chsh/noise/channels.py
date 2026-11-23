"""Noise channels: Qiskit-Aer NoiseModel builders plus analytic predictions.

The analytic predictions (numpy only) let the physics test-suite verify how the
CHSH correlators respond to each channel WITHOUT running a simulator, and give
the ground truth that the Aer simulation is checked against.

For the |Phi+> state, a symmetric single-qubit depolarizing channel with
parameter ``p`` on each qubit rescales every correlator by (1 - p)^2 ... (the
exact factor depends on the channel; the helpers below encode the standard
results for the channels we sweep).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NoiseSpec:
    """A reproducible description of a noise configuration."""

    depolarizing: float = 0.0  # per-qubit depolarizing probability p in [0, 1]
    readout_error: float = 0.0  # symmetric bit-flip readout probability
    amplitude_damping: float = 0.0  # gamma in [0, 1]
    phase_damping: float = 0.0  # lambda in [0, 1]


def depolarizing_correlator_factor(p: float) -> float:
    """Multiplicative factor applied to E for single-qubit depolarizing on both
    qubits.

    A single-qubit depolarizing channel shrinks each Pauli expectation by
    (1 - p). Acting independently on both qubits, the two-qubit correlator
    <P_A P_B> shrinks by (1 - p)^2.
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0, 1]")
    return (1.0 - p) ** 2


def readout_correlator_factor(q: float) -> float:
    """Factor from symmetric readout bit-flip with flip probability q on each
    qubit.

    A single-bit symmetric flip maps a +-1 outcome's expectation by (1 - 2q).
    Independent flips on both measured qubits give (1 - 2q)^2.
    """
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0, 1]")
    return (1.0 - 2.0 * q) ** 2


def phase_damping_correlator_factor(lam: float) -> float:
    """Factor for phase damping (dephasing) with parameter lambda on both
    qubits.

    Dephasing shrinks off-diagonal coherence by sqrt(1 - lambda); the resulting
    XX/XY-type correlator for |Phi+> scales by (1 - lambda). ZZ is unaffected.
    This helper returns the coherence-limited factor (1 - lambda) used for the
    X/intermediate bases relevant to CHSH.
    """
    if not 0.0 <= lam <= 1.0:
        raise ValueError("lambda must be in [0, 1]")
    return 1.0 - lam


def build_noise_model(spec: NoiseSpec):
    """Build a qiskit-aer ``NoiseModel`` from a :class:`NoiseSpec` (lazy import).

    NOTE: exact Aer API (``depolarizing_error``, ``ReadoutError``,
    ``amplitude_damping_error``, ``phase_damping_error``) must be verified
    against the installed qiskit-aer 0.17.2 before a production run.
    """
    from qiskit_aer.noise import (
        NoiseModel,
        ReadoutError,
        amplitude_damping_error,
        depolarizing_error,
        phase_damping_error,
    )

    model = NoiseModel()
    if spec.depolarizing > 0:
        err1 = depolarizing_error(spec.depolarizing, 1)
        model.add_all_qubit_quantum_error(err1, ["ry", "h", "x", "z"])
    if spec.amplitude_damping > 0:
        model.add_all_qubit_quantum_error(
            amplitude_damping_error(spec.amplitude_damping), ["ry", "h"]
        )
    if spec.phase_damping > 0:
        model.add_all_qubit_quantum_error(
            phase_damping_error(spec.phase_damping), ["ry", "h"]
        )
    if spec.readout_error > 0:
        q = spec.readout_error
        model.add_all_qubit_readout_error(ReadoutError([[1 - q, q], [q, 1 - q]]))
    return model
