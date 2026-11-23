"""Statistical distances, divergences, and resampling tools.

All distance functions take two probability vectors over the SAME ordered
alphabet. Zero probabilities are handled explicitly:
  * Total variation and Hellinger are well defined at zeros.
  * Jensen-Shannon divergence uses the mixture m = (p+q)/2 in the denominator,
    so individual zeros are safe; terms with p_i = 0 contribute 0 (0 log 0).
  * Classical fidelity sum sqrt(p_i q_i) is well defined at zeros.
"""

from __future__ import annotations

import math

import numpy as np

_LOG2 = math.log(2.0)


def _validate_pair(p, q) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    if p.shape != q.shape:
        raise ValueError("distributions must have the same shape")
    for name, v in (("p", p), ("q", q)):
        if np.any(v < -1e-12):
            raise ValueError(f"{name} has negative entries")
        if not math.isclose(v.sum(), 1.0, abs_tol=1e-9):
            raise ValueError(f"{name} must sum to 1 (got {v.sum():.6f})")
    return np.clip(p, 0.0, 1.0), np.clip(q, 0.0, 1.0)


def total_variation(p, q) -> float:
    """TV(p, q) = 1/2 sum |p_i - q_i|, in [0, 1]."""
    p, q = _validate_pair(p, q)
    return float(0.5 * np.sum(np.abs(p - q)))


def hellinger(p, q) -> float:
    """Hellinger distance = (1/sqrt2) ||sqrt(p) - sqrt(q)||_2, in [0, 1]."""
    p, q = _validate_pair(p, q)
    return float(np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / np.sqrt(2.0))


def classical_fidelity(p, q) -> float:
    """Classical (Bhattacharyya) fidelity F = (sum sqrt(p_i q_i))^2, in [0, 1]."""
    p, q = _validate_pair(p, q)
    return float(np.sum(np.sqrt(p * q)) ** 2)


def jensen_shannon(p, q) -> float:
    """Jensen-Shannon divergence in bits, in [0, 1]. Symmetric, bounded."""
    p, q = _validate_pair(p, q)
    m = 0.5 * (p + q)

    def _kl(a, b):
        mask = a > 0
        return float(np.sum(a[mask] * (np.log(a[mask]) - np.log(b[mask]))) / _LOG2)

    return 0.5 * _kl(p, m) + 0.5 * _kl(q, m)


def bootstrap_statistic(
    counts: np.ndarray,
    statistic,
    *,
    n_resamples: int = 2000,
    seed: int | None = None,
) -> dict[str, float]:
    """Multinomial bootstrap of a scalar statistic computed from a probability
    vector.

    Parameters
    ----------
    counts:
        Integer counts per outcome (defines the empirical distribution and the
        sample size for resampling).
    statistic:
        Callable mapping a probability vector to a float.
    n_resamples:
        Number of multinomial resamples.
    seed:
        Seed for reproducibility.

    Returns
    -------
    dict with ``point`` (statistic on the observed distribution), ``mean``,
    ``std`` (bootstrap standard error) and the 95% percentile interval
    ``ci_low`` / ``ci_high``.
    """
    counts = np.asarray(counts, dtype=float)
    n = int(counts.sum())
    if n <= 0:
        raise ValueError("counts sum to zero")
    p_hat = counts / n
    point = float(statistic(p_hat))

    rng = np.random.default_rng(seed)
    resamples = rng.multinomial(n, p_hat, size=n_resamples) / n
    vals = np.array([statistic(r) for r in resamples], dtype=float)

    return {
        "point": point,
        "mean": float(vals.mean()),
        "std": float(vals.std(ddof=1)),
        "ci_low": float(np.percentile(vals, 2.5)),
        "ci_high": float(np.percentile(vals, 97.5)),
    }


def benjamini_hochberg(pvalues: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    """Benjamini-Hochberg FDR correction. Returns a boolean reject mask.

    Controls the false discovery rate at level ``alpha`` across multiple
    comparisons (e.g. many settings compared pairwise).
    """
    p = np.asarray(pvalues, dtype=float)
    m = len(p)
    order = np.argsort(p)
    ranked = p[order]
    thresholds = alpha * (np.arange(1, m + 1) / m)
    passed = ranked <= thresholds
    reject = np.zeros(m, dtype=bool)
    if passed.any():
        kmax = np.max(np.where(passed)[0])
        reject[order[: kmax + 1]] = True
    return reject
