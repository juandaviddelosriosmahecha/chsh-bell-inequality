"""Command-line interface for Beyond CHSH experiments.

Examples
--------
    beyond-chsh baseline --shots 8192 --seed 42
    beyond-chsh noise-sweep --param depolarizing --points 11
    beyond-chsh hardware --backend ibm_torino --shots 5000   # needs .env
"""

from __future__ import annotations

import argparse
import json

from .theory.bell_inequalities import evaluate_chsh, no_signalling_deviation
from .theory.correlators import SETTINGS


def _summarise(dists) -> dict:
    res = evaluate_chsh(dists)
    ns = no_signalling_deviation(dists)
    return {
        "S": res.S,
        "S_uncertainty": res.uncertainty,
        "violates_classical": res.violates_classical,
        "correlators": {f"{x}{y}": dists[(x, y)].correlator() for (x, y) in SETTINGS},
        "no_signalling": ns,
    }


def _cmd_baseline(args: argparse.Namespace) -> None:
    if args.exact:
        from .backends.ideal import run_ideal_exact

        dists = run_ideal_exact()
    else:
        from .backends.ideal import run_ideal_sampled

        dists = run_ideal_sampled(shots=args.shots, seed=args.seed)
    print(json.dumps(_summarise(dists), indent=2))


def _cmd_noise_sweep(args: argparse.Namespace) -> None:
    import numpy as np

    from .backends.noisy import run_noisy_sampled
    from .noise.channels import NoiseSpec

    values = np.linspace(0.0, args.max, args.points)
    rows = []
    for v in values:
        spec = NoiseSpec(**{args.param: float(v)})
        dists = run_noisy_sampled(spec, shots=args.shots, seed=args.seed)
        s = evaluate_chsh(dists)
        rows.append({"param": args.param, "value": float(v), "S": s.S, "err": s.uncertainty})
    print(json.dumps(rows, indent=2))


def _cmd_hardware(args: argparse.Namespace) -> None:
    from .backends.ibm_runtime import run_on_hardware
    from .data.storage import save_record

    record = run_on_hardware(shots=args.shots, backend_name=args.backend)
    path = save_record(record, args.out)
    print(f"Saved hardware record to {path}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="beyond-chsh", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    b = sub.add_parser("baseline", help="run the ideal CHSH baseline")
    b.add_argument("--shots", type=int, default=8192)
    b.add_argument("--seed", type=int, default=42)
    b.add_argument("--exact", action="store_true", help="use analytic probabilities")
    b.set_defaults(func=_cmd_baseline)

    n = sub.add_parser("noise-sweep", help="sweep a noise parameter")
    n.add_argument("--param", default="depolarizing",
                   choices=["depolarizing", "readout_error", "amplitude_damping", "phase_damping"])
    n.add_argument("--max", type=float, default=0.5)
    n.add_argument("--points", type=int, default=11)
    n.add_argument("--shots", type=int, default=8192)
    n.add_argument("--seed", type=int, default=42)
    n.set_defaults(func=_cmd_noise_sweep)

    h = sub.add_parser("hardware", help="run on IBM Quantum (requires .env)")
    h.add_argument("--backend", default=None)
    h.add_argument("--shots", type=int, default=5000)
    h.add_argument("--out", default="data/raw")
    h.set_defaults(func=_cmd_hardware)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
