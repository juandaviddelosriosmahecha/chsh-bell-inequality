"""Physics: analytic noise-response factors and visibility inference."""

import math

import pytest

from beyond_chsh.noise.channels import (
    depolarizing_correlator_factor,
    phase_damping_correlator_factor,
    readout_correlator_factor,
)
from beyond_chsh.noise.characterization import (
    estimate_visibility,
    visibility_from_S,
    werner_threshold_for_violation,
)
from beyond_chsh.theory.correlators import SETTINGS, CorrelatorSet, analytic_joint


def test_noise_factors_monotone_decreasing():
    assert depolarizing_correlator_factor(0.0) == pytest.approx(1.0)
    assert depolarizing_correlator_factor(1.0) == pytest.approx(0.0)
    assert readout_correlator_factor(0.5) == pytest.approx(0.0)
    assert phase_damping_correlator_factor(0.0) == pytest.approx(1.0)


def test_werner_threshold_is_one_over_sqrt2():
    assert werner_threshold_for_violation() == pytest.approx(1 / math.sqrt(2))


def test_visibility_inference_on_rescaled_correlators():
    # Build a Werner-like noisy set: ideal correlators scaled by v.
    v = 0.8
    ideal = CorrelatorSet.analytic_optimal()
    noisy = CorrelatorSet(E={xy: v * ideal.E[xy] for xy in SETTINGS})
    assert estimate_visibility(noisy) == pytest.approx(v)
    assert visibility_from_S(v * 2 * math.sqrt(2)) == pytest.approx(v)


def test_analytic_joint_stays_valid_under_scaling():
    # A rescaled correlator still corresponds to a valid distribution when
    # |v*E| <= 1, which holds for v in [0,1].
    d = analytic_joint(0.0, math.pi / 8)
    assert d.probs.min() >= 0.0
