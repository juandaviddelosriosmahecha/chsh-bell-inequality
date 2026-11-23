"""Infer a Werner-state visibility v from observed CHSH correlators.

A common phenomenological model for a noisy |Phi+> is the Werner state
    rho = v |Phi+><Phi+| + (1 - v) I/4,
for which every ideal correlator is rescaled by v: E_noisy = v * E_ideal, and
S_noisy = v * 2*sqrt(2). This gives a single interpretable "visibility" number
that summarises how close the experiment is to the ideal quantum prediction.
"""

from __future__ import annotations

from ..theory.bell_inequalities import TSIRELSON_BOUND
from ..theory.correlators import SETTINGS, CorrelatorSet


def estimate_visibility(observed: CorrelatorSet) -> float:
    """Least-squares visibility v minimising sum (E_obs - v E_ideal)^2."""
    ideal = CorrelatorSet.analytic_optimal()
    num = sum(observed.E[xy] * ideal.E[xy] for xy in SETTINGS)
    den = sum(ideal.E[xy] ** 2 for xy in SETTINGS)
    return num / den if den else float("nan")


def visibility_from_S(S: float) -> float:
    """Visibility implied by an observed CHSH value: v = S / (2 sqrt 2)."""
    return S / TSIRELSON_BOUND


def werner_threshold_for_violation() -> float:
    """Minimum visibility to violate the classical bound: v > 2 / (2 sqrt 2)."""
    return 2.0 / TSIRELSON_BOUND  # = 1/sqrt(2) ~ 0.7071
