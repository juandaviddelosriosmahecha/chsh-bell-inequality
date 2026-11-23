"""Joint and marginal probability distributions from measurement counts.

Conventions (made explicit to fix the ambiguity in the v1.0.0 notebook)
-----------------------------------------------------------------------
* Alice is physical qubit 0, Bob is physical qubit 1.
* Qiskit count bitstrings are big-endian over classical bits: for a 2-bit
  string ``s = s[0] s[1]``, ``s[0]`` is the most significant bit (classical
  bit c1, mapped from qubit 1 = Bob) and ``s[1]`` is the least significant bit
  (classical bit c0, mapped from qubit 0 = Alice). See
  https://docs.quantum.ibm.com/guides/bit-ordering .
  Therefore, from a Qiskit string ``s``:  ``a_bit = int(s[-1])`` (Alice),
  ``b_bit = int(s[-2])`` (Bob).
* Outcomes are reported in the eigenvalue convention ``{+1, -1}`` where bit 0
  maps to +1 and bit 1 maps to -1 (standard Z-eigenvalue mapping). This is the
  convention required by the correlator E = sum_{a,b} a b P(a,b|x,y).

A :class:`JointDistribution` stores ``P(a, b | x, y)`` for the four outcome
pairs ``(a, b)`` with ``a, b in {+1, -1}`` for a single setting ``(x, y)``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

# Ordered outcome labels in the {+1, -1} convention. Index layout:
#   0 -> (+1, +1)   1 -> (+1, -1)   2 -> (-1, +1)   3 -> (-1, -1)
OUTCOMES: tuple[tuple[int, int], ...] = ((+1, +1), (+1, -1), (-1, +1), (-1, -1))


def _bit_to_eigenvalue(bit: int) -> int:
    """Map a computational-basis bit to its Z eigenvalue: 0 -> +1, 1 -> -1."""
    return 1 - 2 * int(bit)


def counts_to_joint(
    counts: Mapping[str, float],
    *,
    alice_bit: int = -1,
    bob_bit: int = -2,
) -> JointDistribution:
    """Extract P(a, b | x, y) from a Qiskit-style counts dictionary.

    Parameters
    ----------
    counts:
        Mapping from measured bitstring to count (or probability). Bitstrings
        may contain spaces (Qiskit multi-register separators), which are
        stripped. Empty input raises ``ValueError``.
    alice_bit, bob_bit:
        Index into the (space-stripped) bitstring for Alice's and Bob's bit.
        Defaults follow the big-endian Qiskit convention: Alice = qubit 0 =
        last character, Bob = qubit 1 = second-to-last character.

    Returns
    -------
    JointDistribution
        Normalised joint probabilities with Poissonian/multinomial shot count.
    """
    if not counts:
        raise ValueError("counts is empty; cannot build a distribution")

    totals = np.zeros(4, dtype=float)
    shots = 0.0
    for bitstring, c in counts.items():
        if c < 0:
            raise ValueError(f"negative count {c} for outcome {bitstring!r}")
        clean = bitstring.replace(" ", "")
        a = _bit_to_eigenvalue(clean[alice_bit])
        b = _bit_to_eigenvalue(clean[bob_bit])
        totals[OUTCOMES.index((a, b))] += c
        shots += c

    if shots <= 0:
        raise ValueError("total counts sum to zero")

    return JointDistribution(probs=totals / shots, shots=int(round(shots)))


@dataclass(frozen=True)
class JointDistribution:
    """A joint distribution P(a, b | x, y) for one measurement setting.

    Attributes
    ----------
    probs:
        Length-4 array ordered as :data:`OUTCOMES`, summing to 1.
    shots:
        Number of samples the distribution was estimated from. Used downstream
        for multinomial uncertainty. ``shots=0`` denotes an exact (analytic)
        distribution with no sampling noise.
    """

    probs: np.ndarray
    shots: int = 0

    def __post_init__(self) -> None:
        p = np.asarray(self.probs, dtype=float)
        if p.shape != (4,):
            raise ValueError("probs must have shape (4,)")
        if np.any(p < -1e-12):
            raise ValueError("probabilities must be non-negative")
        if not np.isclose(p.sum(), 1.0, atol=1e-9):
            raise ValueError(f"probabilities must sum to 1 (got {p.sum():.6f})")
        object.__setattr__(self, "probs", np.clip(p, 0.0, 1.0))

    def p(self, a: int, b: int) -> float:
        """Return P(a, b) for outcomes a, b in {+1, -1}."""
        return float(self.probs[OUTCOMES.index((a, b))])

    def marginal_alice(self) -> dict[int, float]:
        """P(a) = sum_b P(a, b), returned as {+1: ..., -1: ...}."""
        return {
            +1: self.p(+1, +1) + self.p(+1, -1),
            -1: self.p(-1, +1) + self.p(-1, -1),
        }

    def marginal_bob(self) -> dict[int, float]:
        """P(b) = sum_a P(a, b), returned as {+1: ..., -1: ...}."""
        return {
            +1: self.p(+1, +1) + self.p(-1, +1),
            -1: self.p(+1, -1) + self.p(-1, -1),
        }

    def correlator(self) -> float:
        """E = sum_{a,b} a*b*P(a,b) = P(++) - P(+-) - P(-+) + P(--)."""
        signs = np.array([a * b for a, b in OUTCOMES], dtype=float)
        return float(np.dot(signs, self.probs))

    def as_vector(self) -> np.ndarray:
        """Return the length-4 probability vector (copy)."""
        return self.probs.copy()
