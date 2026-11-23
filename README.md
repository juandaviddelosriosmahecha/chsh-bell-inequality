# Beyond CHSH

**Experimental Correlator-Level Analysis of Quantum Randomness under Superconducting Hardware Noise**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19155013.svg)](https://doi.org/10.5281/zenodo.19155013)

**Author:** Juan David de los Rios Mahecha

---

## Scientific objective

What statistical information is lost when a Bell experiment is summarised by the
single CHSH value `S`? This project studies whether **full joint distributions**
`P(a,b|x,y)` and **per-correlator analysis** add experimental or cryptographic
information beyond `S`, under clearly defined noise and trust models. The
hypotheses (H1–H4 in [`docs/methodology.md`](docs/methodology.md)) are tested,
not assumed; a null result is a valid outcome.

## Project status

Research platform, version 2.0.0. It grew out of the v1.0.0 CHSH-game notebook
(preserved at tag `v1.0.0` and in [`notebooks/CHSH_Game.ipynb`](notebooks/CHSH_Game.ipynb))
and refactors the validated physics into a tested, modular package while adding
the "Beyond CHSH" analysis (distributions, marginals, distances, entropy, noise
sweeps, hardware integration).

## Installation

```bash
pip install -e ".[dev]"        # core (numpy/scipy/matplotlib) + test tools
pip install -e ".[quantum]"    # optional: Qiskit backends for simulation/hardware
```

The scientific core depends only on numpy/scipy and installs/tests without
Qiskit. See [`requirements.txt`](requirements.txt) for the pinned Colab setup.

## Running simulations

```bash
beyond-chsh baseline --exact                 # analytic CHSH baseline (no Qiskit)
beyond-chsh baseline --shots 8192 --seed 42  # finite-shot Aer simulation
beyond-chsh noise-sweep --param depolarizing --points 11
```

## Running on IBM Quantum (optional)

Requires credentials in `.env` and the `quantum` extra. See
[`docs/hardware.md`](docs/hardware.md).

```bash
beyond-chsh hardware --backend ibm_torino --shots 5000
```

Simulated runs are never labelled as hardware; every hardware run records job
ids, backend, shots, transpiled depth, and calibration metadata.

## Code organisation

```
src/beyond_chsh/
  circuits/   bell_states, measurements, chsh        (Qiskit, lazy-imported)
  theory/     probabilities, correlators, bell_inequalities, entropy  (numpy only)
  backends/   ideal, noisy, ibm_runtime
  noise/      channels, characterization
  analysis/   statistics, comparisons, visualization
  data/       schemas, storage                        (reproducible records)
  cli.py
experiments/  baseline, noise_sweep, correlator_analysis, entropy_analysis, hardware_validation
tests/        unit, integration (Qiskit), physics
docs/         theory, methodology, hardware, reproducibility
paper/        manuscript.tex, references.bib
```

## Reproducing figures and results

Analyses re-run from stored raw data without touching hardware; see
[`docs/reproducibility.md`](docs/reproducibility.md). Figures export to PNG plus
a vector format into `results/figures/`.

## Experimental limitations

Conventional IBM Quantum hardware does **not** satisfy device-independent
security assumptions (trusted lab, open loopholes, finite statistics). The DI
min-entropy bound is provided for theoretical comparison only, not as a
cryptographic guarantee. See [`docs/methodology.md`](docs/methodology.md).

## References

CHSH (1969), Tsirelson (1980), Pironio et al. (2010), Acín & Masanes (2016) —
full entries in [`paper/references.bib`](paper/references.bib).

## Citation

See [`CITATION.cff`](CITATION.cff).

```bibtex
@software{delosrios_chsh_2026,
  author    = {de los Rios Mahecha, Juan David},
  title     = {Beyond CHSH: Experimental Correlator-Level Analysis of Quantum Randomness under Superconducting Hardware Noise},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19155013},
  url       = {https://github.com/juandaviddelosriosmahecha/chsh-bell-inequality}
}
```

## License

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
