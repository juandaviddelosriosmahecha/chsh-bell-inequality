# Reproducibility

Every run produces an `ExperimentRecord` (see `data/schemas.py`) containing:

* unique experiment id (UTC timestamp + random suffix),
* the configuration used,
* software versions (Python, numpy, scipy, qiskit*),
* random seeds,
* backend identity (for hardware),
* raw, unmodified counts,
* execution metadata (job ids, transpiled depth, calibration),
* derived/processed results written separately.

## Formats

Open formats only: JSON for records, CSV for tables, QPY for circuits (when a
quantum backend is present). Figures export to PNG plus a vector format
(PDF/SVG).

## No silent overwrites

`storage.save_record` refuses to overwrite an existing file unless
`overwrite=True`. Re-running an analysis on stored raw data never requires
re-executing hardware.

## Reproducing results without hardware

```bash
pip install -e ".[dev]"      # core + test deps (no Qiskit needed)
pytest                       # physics + unit + statistics suite
python experiments/baseline/run_baseline.py        # analytic baseline
python experiments/entropy_analysis/run_entropy.py # entropy comparison
```

Qiskit-backed tests run only when the `quantum` extra is installed; hardware
tests are deselected by default (`-m 'not hardware'`).
