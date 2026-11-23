"""Entropy and randomness estimators, with rigorous categorical separation.

This module deliberately distinguishes four conceptually different quantities,
because conflating them is a common and serious error:

1. OBSERVED entropy   -- Shannon / min-entropy of an empirically observed
   output distribution. Descriptive only; assumes the samples are what they
   appear to be. Functions: :func:`shannon_entropy`, :func:`min_entropy`.

2. MODEL-conditioned entropy -- entropy predicted under an explicit noise
   model. Reported together with the model assumptions by the caller.

3. CONDITIONAL entropy given side information H(A|E). Requires a model of the
   adversary's side information; not computable from output counts alone.

4. CERTIFIED randomness -- a lower bound on the min-entropy of the raw output
   that is VALID under a stated security scenario (device assumptions, i.i.d.
   vs general, trusted/untrusted measurements). See
   :func:`chsh_certified_min_entropy_bound`, which states its assumptions and
   references explicitly and must not be used outside that scenario.

All entropies are in bits (log base 2).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

_LOG2 = math.log(2.0)


def _as_prob_vector(p) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    if np.any(p < -1e-12):
        raise ValueError("probabilities must be non-negative")
    s = p.sum()
    if not math.isclose(s, 1.0, abs_tol=1e-9):
        raise ValueError(f"probabilities must sum to 1 (got {s:.6f})")
    return np.clip(p, 0.0, 1.0)


def shannon_entropy(p) -> float:
    """Shannon entropy H(X) = -sum p log2 p, with 0*log0 := 0."""
    p = _as_prob_vector(p)
    nz = p[p > 0]
    return float(-np.sum(nz * np.log(nz)) / _LOG2)


def min_entropy(p) -> float:
    """Min-entropy H_inf(X) = -log2(max_i p_i)."""
    p = _as_prob_vector(p)
    pmax = float(np.max(p))
    if pmax <= 0:
        raise ValueError("distribution has no support")
    return float(-math.log(pmax) / _LOG2)


def measurement_bias(p) -> float:
    """Bias of a two-outcome distribution: |p0 - p1| / 2 scaled to [0, 0.5].

    Returns max_i p_i - 1/len for a general alphabet; for a binary variable
    this equals |p0 - 0.5|. A fair coin has bias 0.
    """
    p = _as_prob_vector(p)
    return float(np.max(p) - 1.0 / len(p))


@dataclass(frozen=True)
class EntropyEstimate:
    """An entropy value with a bootstrap or analytic uncertainty, in bits."""

    value: float
    std_error: float
    kind: str  # one of: "observed", "model", "conditional", "certified"


def shannon_entropy_with_error(counts: np.ndarray) -> EntropyEstimate:
    """Observed Shannon entropy with a Basharin first-order bias note.

    ``counts`` are integer counts per outcome. The plug-in estimator is
    negatively biased; we report the standard plug-in value and a bootstrap-
    style analytic standard error delta-method approximation:
    Var(H) ~ (1/N) * [ sum p (log2 p)^2 - H^2 ].
    """
    counts = np.asarray(counts, dtype=float)
    n = counts.sum()
    if n <= 0:
        raise ValueError("counts sum to zero")
    p = counts / n
    h = shannon_entropy(p)
    nz = p[p > 0]
    log2p = np.log(nz) / _LOG2
    var = (np.sum(nz * log2p**2) - h**2) / n
    return EntropyEstimate(value=h, std_error=math.sqrt(max(var, 0.0)), kind="observed")


def chsh_certified_min_entropy_bound(S: float) -> float:
    """Device-independent min-entropy lower bound per CHSH violation (one bit).

    SECURITY SCENARIO (must hold for this bound to be valid):
      * Device-independent (DI) setting: measurement devices are untrusted but
        assumed non-signalling and i.i.d. across rounds.
      * The reported S is a faithful estimate of the true quantum value, with
        measurement settings chosen with trusted, private randomness.
      * Quantum adversary bounded by quantum theory (not merely no-signalling).

    Under these assumptions the single-round min-entropy of one output bit is
    lower-bounded by (Pironio et al., Nature 464, 1021 (2010); Acin-Masanes
    reviews):

        H_inf >= 1 - log2( 1 + sqrt(2 - S^2 / 4) )     for  2 <= S <= 2*sqrt(2).

    Returns 0 for S <= 2 (no certifiable randomness) and clips the argument to
    the physical CHSH range.

    WARNING: conventional IBM Quantum hardware does NOT satisfy the DI
    assumptions (trusted lab, no loophole closure, finite i.i.d. statistics).
    Applying this bound to such data certifies nothing cryptographically; it is
    provided for theoretical comparison only. See docs/methodology.md.
    """
    if S <= CLASSICAL_S:
        return 0.0
    s = min(S, TSIRELSON_S)
    arg = 2.0 - (s * s) / 4.0
    arg = max(arg, 0.0)
    bound = 1.0 - math.log2(1.0 + math.sqrt(arg))
    return max(bound, 0.0)


CLASSICAL_S = 2.0
TSIRELSON_S = 2.0 * math.sqrt(2.0)
