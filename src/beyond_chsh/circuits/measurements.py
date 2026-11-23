"""Measurement-basis rotations.

The measurement at angle ``theta`` is implemented as ``RY(-2*theta)`` applied
before a computational-basis (Z) measurement. This matches the v1.0.0
convention and makes the analytic correlator E(alpha, beta) = cos(2(alpha-beta))
exact for the |Phi+> state (see theory.correlators).

    theta = 0       -> Z basis
    theta = pi/4    -> X basis
    theta = +-pi/8  -> intermediate CHSH-optimal bases
"""

from __future__ import annotations


def apply_measurement_rotation(circuit, qubit: int, theta: float) -> None:
    """Apply RY(-2*theta) to select a measurement basis.

    Parameters
    ----------
    circuit:
        A ``qiskit.QuantumCircuit``.
    qubit:
        Target qubit index.
    theta:
        Basis angle in radians.
    """
    circuit.ry(-2.0 * theta, qubit)
