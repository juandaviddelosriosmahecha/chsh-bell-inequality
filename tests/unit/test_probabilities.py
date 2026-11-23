"""Unit tests: counts parsing, bit ordering, normalisation, marginals."""

import numpy as np
import pytest

from beyond_chsh.theory.probabilities import JointDistribution, counts_to_joint


def test_bit_ordering_alice_is_last_char():
    # Qiskit big-endian: '10' means c1(Bob)=1, c0(Alice)=0.
    # Alice bit 0 -> +1 ; Bob bit 1 -> -1. So this is outcome (a=+1, b=-1).
    d = counts_to_joint({"10": 100})
    assert d.p(+1, -1) == pytest.approx(1.0)
    assert d.marginal_alice()[+1] == pytest.approx(1.0)
    assert d.marginal_bob()[-1] == pytest.approx(1.0)


def test_counts_with_register_spaces_are_stripped():
    d = counts_to_joint({"1 0": 10, "0 1": 10})
    assert d.probs.sum() == pytest.approx(1.0)


def test_normalisation_and_shots():
    d = counts_to_joint({"00": 25, "01": 25, "10": 25, "11": 25})
    assert d.probs.sum() == pytest.approx(1.0)
    assert d.shots == 100
    assert d.correlator() == pytest.approx(0.0)


def test_marginals_sum_to_one():
    d = counts_to_joint({"00": 30, "01": 20, "10": 10, "11": 40})
    ma, mb = d.marginal_alice(), d.marginal_bob()
    assert ma[+1] + ma[-1] == pytest.approx(1.0)
    assert mb[+1] + mb[-1] == pytest.approx(1.0)


def test_empty_counts_raises():
    with pytest.raises(ValueError):
        counts_to_joint({})


def test_negative_counts_raise():
    with pytest.raises(ValueError):
        counts_to_joint({"00": -1, "11": 2})


def test_bad_probability_vector_raises():
    with pytest.raises(ValueError):
        JointDistribution(probs=np.array([0.5, 0.6, 0.0, 0.0]))
