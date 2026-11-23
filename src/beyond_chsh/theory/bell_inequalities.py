"""CHSH parameter, bounds, and no-signalling checks with uncertainties."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .correlators import SETTINGS, CorrelatorSet
from .probabilities import JointDistribution

CLASSICAL_BOUND = 2.0
TSIRELSON_BOUND = 2.0 * math.sqrt(2.0)  # ~2.8284, quantum maximum for CHSH


def chsh_value(correlators: CorrelatorSet) -> float:
    """S = E00 + E01 + E10 - E11."""
    E = correlators.E
    return E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)]


def chsh_uncertainty(dists: dict[tuple[int, int], JointDistribution]) -> float:
    """Standard error of S from multinomial shot noise on each correlator.

    Var(E_xy) = (1 - E_xy^2) / shots for a {+1,-1}-valued observable estimated
    from ``shots`` independent samples. The four settings are measured on
    independent circuits, so their variances add. Settings with ``shots == 0``
    (analytic) contribute zero variance.
    """
    var = 0.0
    for xy in SETTINGS:
        d = dists[xy]
        if d.shots > 0:
            e = d.correlator()
            var += (1.0 - e * e) / d.shots
    return math.sqrt(var)


@dataclass(frozen=True)
class CHSHResult:
    """CHSH value with uncertainty and bound classification."""

    S: float
    uncertainty: float

    @property
    def violates_classical(self) -> bool:
        """True if |S| exceeds 2 by more than one standard error."""
        return abs(self.S) - self.uncertainty > CLASSICAL_BOUND

    @property
    def within_tsirelson(self) -> bool:
        """True if |S| does not exceed the quantum bound beyond one sigma."""
        return abs(self.S) <= TSIRELSON_BOUND + self.uncertainty


def evaluate_chsh(dists: dict[tuple[int, int], JointDistribution]) -> CHSHResult:
    """Compute S and its uncertainty directly from the four distributions."""
    cs = CorrelatorSet.from_distributions(dists)
    return CHSHResult(S=chsh_value(cs), uncertainty=chsh_uncertainty(dists))


def no_signalling_deviation(
    dists: dict[tuple[int, int], JointDistribution],
) -> dict[str, float]:
    """Quantify violation of the no-signalling (marginal consistency) condition.

    No-signalling requires Alice's marginal P(a|x) to be independent of Bob's
    input y, and symmetrically for Bob. We report the maximum absolute
    deviation of each marginal across the other party's input.

    NOTE: an observed nonzero deviation is a statistical/experimental artefact
    (finite samples, crosstalk, readout error). It must NOT be interpreted as
    physical superluminal signalling. Compare against the statistical scale
    returned in ``std_scale``.
    """
    # Alice marginal P(a=+1 | x) should not depend on y.
    a_x0 = [dists[(0, y)].marginal_alice()[+1] for y in (0, 1)]
    a_x1 = [dists[(1, y)].marginal_alice()[+1] for y in (0, 1)]
    # Bob marginal P(b=+1 | y) should not depend on x.
    b_y0 = [dists[(x, 0)].marginal_bob()[+1] for x in (0, 1)]
    b_y1 = [dists[(x, 1)].marginal_bob()[+1] for x in (0, 1)]

    dev_alice = max(abs(a_x0[0] - a_x0[1]), abs(a_x1[0] - a_x1[1]))
    dev_bob = max(abs(b_y0[0] - b_y0[1]), abs(b_y1[0] - b_y1[1]))

    # Rough statistical scale: sqrt(p(1-p)/N) for a marginal, taking the
    # smallest sample size involved as a conservative estimate.
    shots = [d.shots for d in dists.values() if d.shots > 0]
    n = min(shots) if shots else 0
    std_scale = math.sqrt(0.25 / n) if n > 0 else float("nan")

    return {
        "deviation_alice": dev_alice,
        "deviation_bob": dev_bob,
        "max_deviation": max(dev_alice, dev_bob),
        "std_scale": std_scale,
        # z-score of the largest deviation relative to statistical noise.
        "z_score": (max(dev_alice, dev_bob) / std_scale) if n > 0 else float("nan"),
    }
