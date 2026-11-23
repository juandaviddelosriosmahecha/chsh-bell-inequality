"""Experiment C -- controlled noise sweep.

Sweep one noise channel and record S, its uncertainty, and the full joint
distributions at each point, then plot S vs noise. Requires the 'quantum'
extra (Aer). Run:

    python experiments/noise_sweep/run_noise_sweep.py --param depolarizing
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--param", default="depolarizing",
                    choices=["depolarizing", "readout_error", "amplitude_damping", "phase_damping"])
    ap.add_argument("--max", type=float, default=0.5)
    ap.add_argument("--points", type=int, default=11)
    ap.add_argument("--shots", type=int, default=8192)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="results/figures/chsh_vs_noise")
    args = ap.parse_args()

    import numpy as np

    from beyond_chsh.analysis.visualization import plot_chsh_vs_noise
    from beyond_chsh.backends.noisy import run_noisy_sampled
    from beyond_chsh.noise.channels import NoiseSpec
    from beyond_chsh.theory.bell_inequalities import evaluate_chsh

    values = np.linspace(0.0, args.max, args.points)
    S_vals, S_err = [], []
    for v in values:
        dists = run_noisy_sampled(NoiseSpec(**{args.param: float(v)}),
                                  shots=args.shots, seed=args.seed)
        res = evaluate_chsh(dists)
        S_vals.append(res.S)
        S_err.append(res.uncertainty)
        print(f"{args.param}={v:.3f}  S={res.S:.4f} +/- {res.uncertainty:.4f}")

    paths = plot_chsh_vs_noise(values, S_vals, S_err, xlabel=args.param, path=args.out)
    print("Wrote:", [str(p) for p in paths])


if __name__ == "__main__":
    main()
