"""Ideal backend: exact probabilities, or Aer statevector sampling with a seed.

The ``exact`` path needs no Qiskit: it returns analytic distributions straight
from theory.correlators, so baseline analysis runs anywhere. The ``sampled``
path uses Aer for finite-shot simulation (lazy import).
"""

from __future__ import annotations

import numpy as np

from ..circuits.bell_states import BellState
from ..theory.correlators import ALICE_ANGLES, BOB_ANGLES, SETTINGS, analytic_joint
from ..theory.probabilities import OUTCOMES, JointDistribution, counts_to_joint


def run_ideal_exact(
    *,
    alice_angles: dict[int, float] | None = None,
    bob_angles: dict[int, float] | None = None,
) -> dict[tuple[int, int], JointDistribution]:
    """Return exact P(a,b|x,y) for |Phi+> at the given angles (no sampling)."""
    a = alice_angles or ALICE_ANGLES
    b = bob_angles or BOB_ANGLES
    return {(x, y): analytic_joint(a[x], b[y]) for (x, y) in SETTINGS}


def run_ideal_sampled(
    shots: int = 8192,
    *,
    seed: int = 42,
    state: BellState = BellState.PHI_PLUS,
) -> dict[tuple[int, int], JointDistribution]:
    """Finite-shot ideal simulation via Aer, with a fixed seed for
    reproducibility."""
    from qiskit_aer import AerSimulator  # lazy import

    from ..circuits.chsh import build_all_chsh_circuits

    sim = AerSimulator()
    circuits = build_all_chsh_circuits(state=state)
    out: dict[tuple[int, int], JointDistribution] = {}
    for xy, qc in circuits.items():
        result = sim.run(qc, shots=shots, seed_simulator=seed).result()
        counts = result.get_counts()
        out[xy] = counts_to_joint(counts)
    return out


def sample_from_distribution(
    dist: JointDistribution, shots: int, *, seed: int | None = None
) -> JointDistribution:
    """Draw a multinomial finite-shot sample from an exact distribution.

    Lets us study finite-sample statistics (bootstrap, CHSH uncertainty)
    without any quantum backend at all.
    """
    rng = np.random.default_rng(seed)
    draw = rng.multinomial(shots, dist.probs)
    counts = {
        f"{(1 - b) // 2}{(1 - a) // 2}": int(n)  # big-endian: Bob bit, Alice bit
        for (a, b), n in zip(OUTCOMES, draw, strict=True)
    }
    return counts_to_joint(counts)
