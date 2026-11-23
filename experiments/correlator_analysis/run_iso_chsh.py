"""Experiment D -- configurations with similar CHSH, different distributions.

Find two physically realisable configurations with statistically compatible S
but different joint distributions, and quantify the difference (H1). Uses only
the numpy/scipy analysis layer (no Qiskit). Run:

    python experiments/correlator_analysis/run_iso_chsh.py --target 2.4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=float, default=2.4)
    args = ap.parse_args()

    from beyond_chsh.analysis.comparisons import (
        find_iso_chsh_configuration,
        joint_distance,
    )

    # Reference optimal configuration rescaled is not iso-S; instead we search
    # two independent angle sets that both realise the target S.
    cfg_a = find_iso_chsh_configuration(args.target, seed=1)
    cfg_b = find_iso_chsh_configuration(args.target, seed=99)
    if cfg_a is None or cfg_b is None:
        print(f"Target S={args.target} is outside the physical CHSH range.")
        return

    print(f"Config A: S = {cfg_a.chsh():.4f}")
    print(f"Config B: S = {cfg_b.chsh():.4f}")
    d = joint_distance(cfg_a, cfg_b)
    print(f"Mean total-variation distance between joint distributions: {d:.4f}")
    if d < 1e-6:
        print("Distributions are effectively identical at this target.")
    else:
        print("Similar S, measurably different joint statistics (supports H1).")


if __name__ == "__main__":
    main()
