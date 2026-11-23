"""Publication-quality Matplotlib figures (uses the non-interactive Agg
backend).

Every figure carries axis labels with units where applicable, error bars where
uncertainties exist, a legend, and is exported to PNG + a vector format
(PDF/SVG). Data that contradicts a hypothesis is plotted, never hidden.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless; safe for CI and sandboxes
import matplotlib.pyplot as plt  # noqa: E402

from ..theory.correlators import SETTINGS  # noqa: E402
from ..theory.probabilities import JointDistribution  # noqa: E402

_SETTING_LABELS = [f"E({x},{y})" for (x, y) in SETTINGS]


def _save(fig, path: str | Path, *, vector: str = "pdf") -> list[Path]:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = []
    for ext in ("png", vector):
        p = path.with_suffix(f".{ext}")
        fig.savefig(p, dpi=300, bbox_inches="tight")
        out.append(p)
    plt.close(fig)
    return out


def plot_correlators_vs_noise(
    noise_values, correlators_by_setting, *, xlabel="Noise parameter", path=None
):
    """Plot each E_xy against a noise parameter."""
    fig, ax = plt.subplots(figsize=(6, 4))
    for label, series in zip(_SETTING_LABELS, correlators_by_setting, strict=True):
        ax.plot(noise_values, series, "o-", label=label, markersize=4)
    ax.axhline(0, color="grey", lw=0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Correlator $E_{xy}$ (dimensionless)")
    ax.set_title("CHSH correlators vs noise")
    ax.legend(frameon=False)
    ax.grid(True, ls=":", alpha=0.3)
    return _save(fig, path) if path else fig


def plot_chsh_vs_noise(
    noise_values, S_values, S_errors=None, *, xlabel="Noise parameter", path=None
):
    """Plot S against a noise parameter with error bars and the two bounds."""
    import numpy as np

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(noise_values, S_values, yerr=S_errors, fmt="o-", capsize=3, color="black")
    ax.axhline(2.0, ls="--", color="grey", label="Classical bound")
    ax.axhline(2.0 * np.sqrt(2.0), ls=":", color="grey", label="Tsirelson bound")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("CHSH value $S$ (dimensionless)")
    ax.set_title("CHSH parameter vs noise")
    ax.legend(frameon=False)
    ax.grid(True, ls=":", alpha=0.3)
    return _save(fig, path) if path else fig


def plot_joint_heatmap(dist: JointDistribution, *, title="Joint P(a,b)", path=None):
    """Heatmap of a 2x2 joint distribution over outcomes (+1,-1)x(+1,-1)."""
    import numpy as np

    mat = np.array(
        [[dist.p(+1, +1), dist.p(+1, -1)], [dist.p(-1, +1), dist.p(-1, -1)]]
    )
    fig, ax = plt.subplots(figsize=(4, 3.5))
    im = ax.imshow(mat, cmap="viridis", vmin=0, vmax=max(0.5, mat.max()))
    ax.set_xticks([0, 1], ["b=+1", "b=-1"])
    ax.set_yticks([0, 1], ["a=+1", "a=-1"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{mat[i, j]:.3f}", ha="center", va="center",
                    color="white" if mat[i, j] < 0.3 else "black")
    fig.colorbar(im, ax=ax, label="Probability")
    ax.set_title(title)
    return _save(fig, path) if path else fig
