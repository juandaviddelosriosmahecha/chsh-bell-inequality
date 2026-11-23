# Methodology

## Research question

What statistical information is lost when a Bell experiment is summarised by the
CHSH value `S` alone? Can full measurement distributions and per-correlator
analysis add experimental or cryptographic information beyond `S`, under clearly
defined noise and trust models?

## Hypotheses (to be tested, not assumed)

* **H1** Configurations with similar `S` may have different joint distributions,
  marginal biases, and noise sensitivities.
* **H2** Full statistics may characterise certain imperfections better than `S`.
* **H3** Under an explicit security model, extra statistics might improve a
  valid randomness/entropy bound relative to one based on `S` alone.
* **H4** The usefulness of extra statistics depends on noise type, sample size,
  and model assumptions.

A null result (no improvement) is a valid scientific outcome and is reported as
such.

## Statistical analysis

* Multinomial estimation of probabilities; per-correlator variance
  `Var(E) = (1 - E^2)/N`.
* CHSH uncertainty by summing per-setting variances (the four settings run on
  independent circuits, so hardware drift is **not** assumed independent — see
  Experiment F).
* Multinomial bootstrap for confidence intervals.
* Benjamini-Hochberg FDR control for multiple pairwise comparisons.
* Differences smaller than their uncertainty are never reported as physical
  findings.

## Security model for certified randomness

The device-independent (DI) min-entropy bound in `theory/entropy.py` is valid
only under: untrusted-but-non-signalling i.i.d. devices, trusted private setting
randomness, and a quantum-bounded adversary.

**Conventional IBM Quantum hardware does not meet these conditions** (trusted
lab, open detection/locality loopholes, finite statistics). The DI bound is
therefore used for theoretical comparison only, never as a cryptographic
guarantee for hardware data.

## Hardware integrity rules

* `mode='hardware'` is set only for real-device execution (SamplerV2 route).
* Every run records: experiment id, config, software versions, seeds, backend
  name, job ids, transpiled depth, raw counts, shots, calibration metadata.
* Credentials come from `.env`; no tokens in source or results.
