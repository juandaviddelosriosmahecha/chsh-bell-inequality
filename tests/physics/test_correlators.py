"""Physics correctness: analytic correlators, CHSH value, and bounds."""

import math

import numpy as np
import pytest

from beyond_chsh.theory.bell_inequalities import (
    CLASSICAL_BOUND,
    TSIRELSON_BOUND,
    chsh_value,
    evaluate_chsh,
)
from beyond_chsh.theory.correlators import (
    CorrelatorSet,
    analytic_joint,
    phi_plus_correlator,
)


def test_phi_plus_correlator_identity():
    # E(alpha, beta) = cos(2(alpha - beta)).
    for a, b in [(0.0, 0.0), (0.0, math.pi / 8), (math.pi / 4, -math.pi / 8)]:
        assert phi_plus_correlator(a, b) == pytest.approx(math.cos(2 * (a - b)))


def test_optimal_correlators_reproduce_tsirelson():
    cs = CorrelatorSet.analytic_optimal()
    E00, E01, E10, E11 = cs.as_tuple()
    assert E00 == pytest.approx(1 / math.sqrt(2))
    assert E01 == pytest.approx(1 / math.sqrt(2))
    assert E10 == pytest.approx(1 / math.sqrt(2))
    assert E11 == pytest.approx(-1 / math.sqrt(2))
    assert chsh_value(cs) == pytest.approx(TSIRELSON_BOUND)


def test_analytic_joint_normalised_and_consistent():
    d = analytic_joint(0.0, math.pi / 8)
    assert d.probs.sum() == pytest.approx(1.0)
    # Correlator from the joint equals the analytic prediction.
    assert d.correlator() == pytest.approx(phi_plus_correlator(0.0, math.pi / 8))


def test_chsh_respects_classical_bound_for_product_state():
    # Aligned bases (all angle 0) give a classical, non-violating configuration.
    angles = {0: 0.0, 1: 0.0}
    dists = {
        (x, y): analytic_joint(angles[x], angles[y])
        for (x, y) in [(0, 0), (0, 1), (1, 0), (1, 1)]
    }
    res = evaluate_chsh(dists)
    assert abs(res.S) <= CLASSICAL_BOUND + 1e-9


def test_tsirelson_is_upper_bound_over_random_angles():
    rng = np.random.default_rng(0)
    for _ in range(200):
        a = {0: rng.uniform(-np.pi, np.pi), 1: rng.uniform(-np.pi, np.pi)}
        b = {0: rng.uniform(-np.pi, np.pi), 1: rng.uniform(-np.pi, np.pi)}
        dists = {
            (x, y): analytic_joint(a[x], b[y])
            for (x, y) in [(0, 0), (0, 1), (1, 0), (1, 1)]
        }
        assert abs(chsh_value(CorrelatorSet.from_distributions(dists))) <= TSIRELSON_BOUND + 1e-9
