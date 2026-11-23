"""Unit tests: entropy, min-entropy, bias, certified bound."""

import math

import pytest

from beyond_chsh.theory.entropy import (
    chsh_certified_min_entropy_bound,
    measurement_bias,
    min_entropy,
    shannon_entropy,
    shannon_entropy_with_error,
)


def test_uniform_binary_entropy_is_one_bit():
    assert shannon_entropy([0.5, 0.5]) == pytest.approx(1.0)
    assert min_entropy([0.5, 0.5]) == pytest.approx(1.0)


def test_deterministic_distribution_has_zero_entropy():
    assert shannon_entropy([1.0, 0.0]) == pytest.approx(0.0)
    assert min_entropy([1.0, 0.0]) == pytest.approx(0.0)


def test_min_entropy_le_shannon():
    p = [0.7, 0.2, 0.1]
    assert min_entropy(p) <= shannon_entropy(p) + 1e-12


def test_measurement_bias_fair_vs_biased():
    assert measurement_bias([0.5, 0.5]) == pytest.approx(0.0)
    assert measurement_bias([0.9, 0.1]) == pytest.approx(0.4)


def test_certified_bound_zero_below_classical():
    assert chsh_certified_min_entropy_bound(2.0) == 0.0
    assert chsh_certified_min_entropy_bound(1.5) == 0.0


def test_certified_bound_positive_and_monotone():
    b_mid = chsh_certified_min_entropy_bound(2.5)
    b_max = chsh_certified_min_entropy_bound(2 * math.sqrt(2))
    assert 0.0 < b_mid < b_max
    # At Tsirelson's bound the single-bit min-entropy bound is 1 bit.
    assert b_max == pytest.approx(1.0, abs=1e-9)


def test_entropy_with_error_returns_observed_kind():
    est = shannon_entropy_with_error([500, 500])
    assert est.kind == "observed"
    assert est.value == pytest.approx(1.0)
    assert est.std_error >= 0.0
