"""Experiment A -- CHSH reproduction.

Reproduce the ideal quantum prediction (S = 2*sqrt(2)) analytically and via
finite-shot simulation, and save a reproducible record. Run:

    python experiments/baseline/run_baseline.py --shots 8192 --seed 42
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from beyond_chsh.backends.ideal import run_ideal_exact  # noqa: E402
from beyond_chsh.theory.bell_inequalities import (  # noqa: E402
    evaluate_chsh,
    no_signalling_deviation,
)
from beyond_chsh.theory.correlators import SETTINGS  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", type=int, default=8192)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--sampled", action="store_true", help="use Aer sampling (needs qiskit)")
    args = ap.parse_args()

    if args.sampled:
        from beyond_chsh.backends.ideal import run_ideal_sampled

        dists = run_ideal_sampled(shots=args.shots, seed=args.seed)
    else:
        dists = run_ideal_exact()

    res = evaluate_chsh(dists)
    print(f"S = {res.S:.5f} +/- {res.uncertainty:.5f}")
    for xy in SETTINGS:
        print(f"  E{xy} = {dists[xy].correlator():+.5f}")
    print("No-signalling:", no_signalling_deviation(dists))


if __name__ == "__main__":
    main()
