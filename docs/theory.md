# Theory

## Conventions

* **Parties and qubits.** Alice = physical qubit 0, Bob = physical qubit 1.
* **Bit ordering.** Qiskit count bitstrings are big-endian over classical bits:
  for a two-bit string `s`, `s[-1]` is Alice's bit (c0, qubit 0) and `s[-2]` is
  Bob's bit (c1, qubit 1). See
  [IBM: bit ordering](https://docs.quantum.ibm.com/guides/bit-ordering).
* **Outcome values.** Computational bit `0 -> +1`, `1 -> -1` (Z eigenvalues).
* **Measurement bases.** Angle `theta` is realised as `RY(-2 theta)` before a Z
  measurement.

## Entangled state

The baseline is the Bell state

$$ |\Phi^+\rangle = \tfrac{1}{\sqrt2}(|00\rangle + |11\rangle). $$

The other three Bell states and partially entangled states
`cos(theta)|00> + sin(theta)|11>` are provided as configurable extensions.

## Joint distributions and correlators

For inputs `x, y in {0,1}` and outcomes `a, b in {+1,-1}`:

$$ P(a,b\mid x,y), \qquad E_{xy} = \sum_{a,b} ab\,P(a,b\mid x,y). $$

For `|Phi+>` with Alice at angle `alpha` and Bob at angle `beta`,

$$ E(\alpha,\beta) = \cos\!\big(2(\alpha-\beta)\big), \qquad
   P(a,b) = \tfrac{1}{4}\big(1 + ab\,E(\alpha,\beta)\big). $$

## CHSH parameter and bounds

$$ S = E_{00} + E_{01} + E_{10} - E_{11}, \qquad
   |S|\le 2 \text{ (local)}, \qquad |S|\le 2\sqrt2 \text{ (quantum)}. $$

At the optimal angles (Alice `{0, pi/4}`, Bob `{pi/8, -pi/8}`) the ideal value
is `S = 2 sqrt 2`, reproducing v1.0.0 (pinned by a regression test).

## Marginals and no-signalling

`P(a|x) = sum_b P(a,b|x,y)` must not depend on `y` (and symmetrically). An
observed deviation is a statistical/experimental artefact; it is compared
against the statistical scale `sqrt(p(1-p)/N)` and **never** interpreted as
superluminal signalling.

## Statistical distances

Total variation, Hellinger, Jensen-Shannon (bits), and classical fidelity, all
with explicit zero-probability handling (see `analysis/statistics.py`).

## Entropy and randomness

Four strictly separated quantities (see `theory/entropy.py`): observed entropy,
model-conditioned entropy, conditional entropy given side information, and
cryptographically certified randomness. The device-independent CHSH min-entropy
bound follows Pironio et al., *Nature* **464**, 1021 (2010).

*Content was rephrased for compliance with licensing restrictions.*
