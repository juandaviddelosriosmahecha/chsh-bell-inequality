"""Integration tests that require the optional 'quantum' extra (Qiskit + Aer).

Skipped automatically when Qiskit is not installed. Hardware tests live behind
the 'hardware' marker and are deselected by default (see pyproject.toml).
"""

import math

import pytest

qiskit = pytest.importorskip("qiskit")
pytest.importorskip("qiskit_aer")

pytestmark = pytest.mark.qiskit


def test_ideal_sampled_reproduces_tsirelson_within_noise():
    from beyond_chsh.backends.ideal import run_ideal_sampled
    from beyond_chsh.theory.bell_inequalities import evaluate_chsh

    dists = run_ideal_sampled(shots=20000, seed=1)
    res = evaluate_chsh(dists)
    # Finite-shot estimate should sit within ~5 sigma of 2*sqrt(2).
    assert abs(res.S - 2 * math.sqrt(2)) < 5 * res.uncertainty + 0.05
    assert res.violates_classical


def test_depolarizing_noise_reduces_S():
    from beyond_chsh.backends.noisy import run_noisy_sampled
    from beyond_chsh.noise.channels import NoiseSpec
    from beyond_chsh.theory.bell_inequalities import evaluate_chsh

    clean = evaluate_chsh(run_noisy_sampled(NoiseSpec(depolarizing=0.0), shots=20000, seed=2))
    noisy = evaluate_chsh(run_noisy_sampled(NoiseSpec(depolarizing=0.3), shots=20000, seed=2))
    assert noisy.S < clean.S
