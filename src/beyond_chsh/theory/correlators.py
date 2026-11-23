"""Correlators E_xy and analytic predictions for the CHSH scenario.

The analytic model treats each party's measurement as a projective
measurement of ``cos(2a) Z + sin(2a) X`` obtained from applying ``RY(-2a)``
before a Z measurement, matching the v1.0.0 circuit convention
``apply_u_theta(q, a) = RY(-2a)``.

For the Bell state |Phi+> = (|00> + |11>)/sqrt(2), the correlator between
Alice at angle ``alpha`` and Bob at angle ``beta`` is::

    E(alpha, beta) = cos(2 alpha - 2 beta)

This identity is used as ground truth in the physics test suite.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .probabilities import OUTCOMES, JointDistribution

# Canonical CHSH settings order: (x, y) in {(0,0), (0,1), (1,0), (1,1)}.
SETTINGS: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))

# Optimal angles reproducing |S| = 2*sqrt(2) (as in v1.0.0).
ALICE_ANGLES: dict[int, float] = {0: 0.0, 1: np.pi / 4}
BOB_ANGLES: dict[int, float] = {0: np.pi / 8, 1: -np.pi / 8}


def phi_plus_correlator(alpha: float, beta: float) -> float:
    """Analytic correlator E(alpha, beta) = cos(2(alpha - beta)) for |Phi+>."""
    return float(np.cos(2.0 * (alpha - beta)))


def analytic_joint(alpha: float, beta: float) -> JointDistribution:
    """Exact P(a, b | alpha, beta) for |Phi+> with no sampling noise.

    For |Phi+>, P(a, b) = (1 + a*b*cos(2(alpha-beta))) / 4 with a, b in {+1,-1}.
    """
    e = phi_plus_correlator(alpha, beta)
    probs = np.array([(1.0 + a * b * e) / 4.0 for a, b in OUTCOMES], dtype=float)
    return JointDistribution(probs=probs, shots=0)


def correlators_from_distributions(
    dists: dict[tuple[int, int], JointDistribution],
) -> dict[tuple[int, int], float]:
    """Compute E_xy for each setting from its joint distribution."""
    return {xy: dists[xy].correlator() for xy in SETTINGS}


@dataclass(frozen=True)
class CorrelatorSet:
    """The four CHSH correlators keyed by setting, plus derived quantities."""

    E: dict[tuple[int, int], float]

    @classmethod
    def from_distributions(
        cls, dists: dict[tuple[int, int], JointDistribution]
    ) -> CorrelatorSet:
        return cls(E=correlators_from_distributions(dists))

    @classmethod
    def analytic_optimal(cls) -> CorrelatorSet:
        """Ideal |Phi+> correlators at the optimal CHSH angles."""
        E = {
            (x, y): phi_plus_correlator(ALICE_ANGLES[x], BOB_ANGLES[y])
            for (x, y) in SETTINGS
        }
        return cls(E=E)

    def as_tuple(self) -> tuple[float, float, float, float]:
        return tuple(self.E[xy] for xy in SETTINGS)  # type: ignore[return-value]
