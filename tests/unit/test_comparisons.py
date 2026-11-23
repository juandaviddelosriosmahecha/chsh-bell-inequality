"""Unit tests: iso-CHSH configuration search and joint distance."""

import math

import pytest

from beyond_chsh.analysis.comparisons import (
    Configuration,
    find_iso_chsh_configuration,
    joint_distance,
)


def test_optimal_configuration_has_expected_chsh():
    cfg = Configuration(
        alice_angles={0: 0.0, 1: math.pi / 4},
        bob_angles={0: math.pi / 8, 1: -math.pi / 8},
    )
    assert cfg.chsh() == pytest.approx(2 * math.sqrt(2))


def test_identical_configs_have_zero_distance():
    cfg = Configuration(alice_angles={0: 0.0, 1: 0.3}, bob_angles={0: 0.1, 1: -0.1})
    assert joint_distance(cfg, cfg) == pytest.approx(0.0)


def test_iso_chsh_search_hits_target():
    target = 2.4
    cfg = find_iso_chsh_configuration(target, seed=1)
    assert cfg is not None
    assert cfg.chsh() == pytest.approx(target, abs=1e-3)


def test_iso_chsh_search_rejects_unphysical_target():
    assert find_iso_chsh_configuration(3.5) is None
