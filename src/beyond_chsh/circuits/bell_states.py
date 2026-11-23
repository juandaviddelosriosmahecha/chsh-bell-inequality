"""Bell-state and partially-entangled state preparation.

Alice is qubit 0, Bob is qubit 1 (see theory.probabilities for the ordering
convention). All constructors return a 2-qubit ``QuantumCircuit`` with NO
measurements; measurement bases are added separately in ``chsh``.
"""

from __future__ import annotations

from enum import Enum


class BellState(str, Enum):
    """The four maximally entangled Bell states."""

    PHI_PLUS = "phi_plus"  # (|00> + |11>)/sqrt(2)
    PHI_MINUS = "phi_minus"  # (|00> - |11>)/sqrt(2)
    PSI_PLUS = "psi_plus"  # (|01> + |10>)/sqrt(2)
    PSI_MINUS = "psi_minus"  # (|01> - |10>)/sqrt(2)


def _new_circuit():
    from qiskit import QuantumCircuit  # lazy import

    return QuantumCircuit(2)


def prepare_bell_state(state: BellState = BellState.PHI_PLUS):
    """Return a circuit preparing the requested Bell state from |00>."""
    qc = _new_circuit()
    qc.h(0)
    qc.cx(0, 1)
    if state in (BellState.PHI_MINUS, BellState.PSI_MINUS):
        qc.z(0)
    if state in (BellState.PSI_PLUS, BellState.PSI_MINUS):
        qc.x(1)
    qc.barrier()
    return qc


def prepare_partially_entangled(theta: float):
    """Return a circuit preparing cos(theta)|00> + sin(theta)|11>.

    ``theta = pi/4`` recovers |Phi+>. Smaller angles give weaker entanglement,
    used to explore configurations with similar CHSH but different statistics.
    """
    qc = _new_circuit()
    qc.ry(2.0 * theta, 0)
    qc.cx(0, 1)
    qc.barrier()
    return qc
