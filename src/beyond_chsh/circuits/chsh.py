"""CHSH circuit assembly: Bell state + per-party measurement rotations + measure.

Uses the sampling (counts) route so that full joint distributions P(a,b|x,y)
and marginals can be reconstructed. The expectation-value (Estimator) route in
the v1.0.0 notebook returns only E_xy and is kept in backends.ibm_runtime as an
option, but it discards the distribution information this project studies.
"""

from __future__ import annotations

from ..theory.correlators import ALICE_ANGLES, BOB_ANGLES, SETTINGS
from .bell_states import BellState, prepare_bell_state
from .measurements import apply_measurement_rotation


def build_chsh_circuit(
    x: int,
    y: int,
    *,
    state: BellState = BellState.PHI_PLUS,
    alice_angles: dict[int, float] | None = None,
    bob_angles: dict[int, float] | None = None,
):
    """Build the measured CHSH circuit for inputs (x, y).

    Parameters
    ----------
    x, y:
        Alice's and Bob's measurement-setting choices in {0, 1}.
    state:
        Which Bell state to prepare.
    alice_angles, bob_angles:
        Optional override maps {setting: angle}. Default to the CHSH-optimal
        angles that give |S| = 2*sqrt(2).
    """
    a_ang = alice_angles or ALICE_ANGLES
    b_ang = bob_angles or BOB_ANGLES

    qc = prepare_bell_state(state)
    apply_measurement_rotation(qc, 0, a_ang[x])  # Alice = qubit 0
    apply_measurement_rotation(qc, 1, b_ang[y])  # Bob = qubit 1
    qc.measure_all()
    return qc


def build_all_chsh_circuits(
    *,
    state: BellState = BellState.PHI_PLUS,
    alice_angles: dict[int, float] | None = None,
    bob_angles: dict[int, float] | None = None,
) -> dict[tuple[int, int], object]:
    """Build the four CHSH circuits keyed by setting (x, y)."""
    return {
        (x, y): build_chsh_circuit(
            x, y, state=state, alice_angles=alice_angles, bob_angles=bob_angles
        )
        for (x, y) in SETTINGS
    }
