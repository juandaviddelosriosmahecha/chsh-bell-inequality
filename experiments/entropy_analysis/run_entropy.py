"""Experiment E -- randomness and entropy.

Compare, under explicit trust models, the randomness extractable from (i) the
CHSH value alone via the device-independent bound, and (ii) the observed output
distributions. The DI bound's assumptions (and why they do NOT hold on
conventional IBM hardware) are stated in docs/methodology.md.

    python experiments/entropy_analysis/run_entropy.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from beyond_chsh.backends.ideal import run_ideal_exact  # noqa: E402
from beyond_chsh.theory.bell_inequalities import chsh_value  # noqa: E402
from beyond_chsh.theory.correlators import SETTINGS, CorrelatorSet  # noqa: E402
from beyond_chsh.theory.entropy import (  # noqa: E402
    chsh_certified_min_entropy_bound,
    min_entropy,
    shannon_entropy,
)


def main() -> None:
    dists = run_ideal_exact()
    S = chsh_value(CorrelatorSet.from_distributions(dists))

    print(f"CHSH S = {S:.5f}")
    print(f"DI certified min-entropy per bit (model: device-independent, i.i.d.): "
          f"{chsh_certified_min_entropy_bound(S):.5f} bits")
    print("\nPer-setting OBSERVED entropies (trusted-device, descriptive):")
    for xy in SETTINGS:
        p = dists[xy].probs
        print(f"  {xy}: H={shannon_entropy(p):.4f}  Hmin={min_entropy(p):.4f} bits")
    print("\nNote: these categories are not interchangeable; see methodology.")


if __name__ == "__main__":
    main()
