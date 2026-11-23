"""Unit tests: distances, divergences, bootstrap, multiple-comparison control."""

import numpy as np
import pytest

from beyond_chsh.analysis.statistics import (
    benjamini_hochberg,
    bootstrap_statistic,
    classical_fidelity,
    hellinger,
    jensen_shannon,
    total_variation,
)


def test_distances_zero_for_identical():
    p = [0.25, 0.25, 0.25, 0.25]
    assert total_variation(p, p) == pytest.approx(0.0)
    assert hellinger(p, p) == pytest.approx(0.0)
    assert jensen_shannon(p, p) == pytest.approx(0.0)
    assert classical_fidelity(p, p) == pytest.approx(1.0)


def test_distances_handle_zero_probabilities():
    p = [1.0, 0.0]
    q = [0.0, 1.0]
    assert total_variation(p, q) == pytest.approx(1.0)
    assert hellinger(p, q) == pytest.approx(1.0)
    assert jensen_shannon(p, q) == pytest.approx(1.0)  # bits, max for disjoint
    assert classical_fidelity(p, q) == pytest.approx(0.0)


def test_distance_bounds():
    rng = np.random.default_rng(1)
    for _ in range(100):
        p = rng.dirichlet(np.ones(4))
        q = rng.dirichlet(np.ones(4))
        assert 0.0 <= total_variation(p, q) <= 1.0
        assert 0.0 <= hellinger(p, q) <= 1.0
        assert 0.0 <= jensen_shannon(p, q) <= 1.0 + 1e-9
        assert 0.0 <= classical_fidelity(p, q) <= 1.0 + 1e-9


def test_bootstrap_is_reproducible_with_seed():
    counts = np.array([250, 250, 250, 250])
    stat = lambda p: p[0]  # noqa: E731
    a = bootstrap_statistic(counts, stat, n_resamples=500, seed=7)
    b = bootstrap_statistic(counts, stat, n_resamples=500, seed=7)
    assert a == b
    assert a["point"] == pytest.approx(0.25)
    assert a["ci_low"] <= a["point"] <= a["ci_high"]


def test_benjamini_hochberg_rejects_small_pvalues():
    pvals = np.array([0.001, 0.2, 0.03, 0.9])
    reject = benjamini_hochberg(pvals, alpha=0.05)
    assert reject[0]  # smallest p-value rejected
    assert not reject[3]  # largest not rejected
