"""Compare measurement configurations that share a similar CHSH value.

Experiment D: find physically realisable settings whose CHSH value S is
statistically compatible but whose joint distributions differ. We only search
over valid quantum models (|Phi+> with varying measurement angles and
partially entangled states), so every candidate is realisable by construction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from ..theory.bell_inequalities import chsh_value
from ..theory.correlators import SETTINGS, CorrelatorSet, analytic_joint
from .statistics import total_variation


@dataclass
class Configuration:
    """A set of four Alice/Bob angles and the resulting distributions."""

    alice_angles: dict[int, float]
    bob_angles: dict[int, float]

    def distributions(self):
        return {
            (x, y): analytic_joint(self.alice_angles[x], self.bob_angles[y])
            for (x, y) in SETTINGS
        }

    def chsh(self) -> float:
        return chsh_value(CorrelatorSet.from_distributions(self.distributions()))


def joint_distance(cfg_a: Configuration, cfg_b: Configuration) -> float:
    """Mean total-variation distance between the two configs' joint
    distributions."""
    da, db = cfg_a.distributions(), cfg_b.distributions()
    return float(
        np.mean([total_variation(da[xy].probs, db[xy].probs) for xy in SETTINGS])
    )


def find_iso_chsh_configuration(
    target_S: float, *, seed: int = 0
) -> Configuration | None:
    """Find angles realising a target CHSH value via constrained optimization.

    Returns a valid :class:`Configuration` (angles map to real projective
    measurements, so realisability is guaranteed) whose S is close to
    ``target_S``, or None if the target is outside the physical CHSH range.
    """
    if abs(target_S) > 2.0 * np.sqrt(2.0) + 1e-9:
        return None

    rng = np.random.default_rng(seed)

    def unpack(v):
        return (
            Configuration(
                alice_angles={0: v[0], 1: v[1]},
                bob_angles={0: v[2], 1: v[3]},
            )
        )

    def objective(v):
        return (unpack(v).chsh() - target_S) ** 2

    best = None
    for _ in range(20):
        x0 = rng.uniform(-np.pi, np.pi, size=4)
        res = minimize(objective, x0, method="Nelder-Mead")
        if res.fun < 1e-6:
            cand = unpack(res.x)
            if best is None:
                best = cand
    return best
