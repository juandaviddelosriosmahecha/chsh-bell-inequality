"""Regression tests pinning the validated scientific results of v1.0.0.

v1.0.0 established, for the optimal CHSH angles on |Phi+>:
    E00 = E01 = E10 = +1/sqrt(2),  E11 = -1/sqrt(2),  S = 2*sqrt(2).
These must never silently change.
"""

import math

import pytest

from beyond_chsh.theory.bell_inequalities import chsh_value
from beyond_chsh.theory.correlators import CorrelatorSet

V1_CORRELATORS = (0.7071067811865476, 0.7071067811865476, 0.7071067811865476, -0.7071067811865476)
V1_S = 2.8284271247461903


def test_v1_correlators_preserved():
    assert CorrelatorSet.analytic_optimal().as_tuple() == pytest.approx(V1_CORRELATORS)


def test_v1_chsh_value_preserved():
    assert chsh_value(CorrelatorSet.analytic_optimal()) == pytest.approx(V1_S)
    assert V1_S == pytest.approx(2 * math.sqrt(2))
