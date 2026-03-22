# CHSH Bell Inequality: Classical vs Quantum Strategies

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.3.1-6929C4)](https://qiskit.org)

**Author:** Juan David de los Rios Mahecha  
**Role:** Qiskit Advocate  
**Topic:** Quantum Nonlocality / Bell Inequalities  

---

## Overview

This notebook presents a complete study of the **CHSH (Clauser–Horne–Shimony–Holt) game** as a fundamental framework to explore quantum nonlocality and the limits of classical correlations.

The work combines theoretical insight and experimental implementation, showing how quantum entanglement enables correlations that surpass any classical strategy.

### Key Results

| Strategy | Win Probability | CHSH value \|S\| |
|----------|----------------|-----------------|
| Classical (best possible) | 75% | ≤ 2 |
| Quantum (theoretical) | ≈ 85.36% | 2√2 ≈ 2.828 |
| Quantum (simulated) | ≈ 85.35% | 2.828 |
| Quantum (IBM hardware) | ≈ 86.49% | 2.919 |

---

## Contents

```
chsh-bell-inequality/
├── CHSH_Game.ipynb        # Main notebook
├── requirements.txt       # Python dependencies
├── LICENSE                # CC BY 4.0
└── README.md
```

---

## Notebook Structure

1. **Introduction & Motivation** — Overview, tools, and significance
2. **Theoretical foundations** — Bell inequalities, CHSH formulation
3. **Classical strategy** — 75% limit, formal contradiction proof, Python simulation
4. **Quantum strategy — theory** — Bell state |Φ⁺⟩, optimal angles, P ≈ 85.36%
5. **Qiskit implementation** — Circuit construction, measurement rotations
6. **Simulation results** — Win probabilities, correlations E(x,y), CHSH parameter S
7. **S vs angle θ analysis** — Angular sweep, theory vs simulation comparison
8. **Real IBM Quantum hardware** *(optional — requires credentials)* — Execution on ibm_fez
9. **Noise & transpilation analysis** — Optimization levels 0 / 1 / 2, NISQ impact
10. **Comparative visualization** — Hardware vs simulator, correlations vs theory
11. **Conclusions & exercises** — Summary, physical meaning, proposed problems

---

## Quantum Strategy

If Alice and Bob share the Bell state |Φ⁺⟩ and measure at optimal angles:

- **Alice:** 0, π/4  
- **Bob:** π/8, −π/8

They achieve a winning probability of **(2 + √2) / 4 ≈ 85.36%**, violating the classical CHSH bound with **|S| = 2√2**.

This demonstrates that quantum correlations **cannot be explained by any local hidden variable theory**.

---

## Requirements

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install qiskit==2.3.1 qiskit-aer==0.17.2 qiskit-ibm-runtime matplotlib numpy
```

> **Note:** Section 8 (real hardware) requires valid IBM Quantum credentials.  
> All other sections run fully on the local Aer simulator.

---

## Usage

Open the notebook in Google Colab or locally:

```bash
git clone https://github.com/juandaviddelosriosmahecha/chsh-bell-inequality.git
cd chsh-bell-inequality
jupyter notebook CHSH_Game.ipynb
```

Or open directly in Colab:  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juandaviddelosriosmahecha/chsh-bell-inequality/blob/main/CHSH_Game.ipynb)

---

## Illustrations

All hand-drawn illustrations in this notebook were created by **Juan David de los Rios Mahecha** and are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Citation

If you use this work, please cite it as:

```bibtex
@software{delosrios_chsh_2026,
  author    = {de los Rios Mahecha, Juan David},
  title     = {CHSH Bell Inequality: Classical vs Quantum Strategies},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://github.com/juandaviddelosriosmahecha/chsh-bell-inequality}
}
```

> Update the DOI after publishing on Zenodo.

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.com/licenses/by/4.0/).

You are free to share and adapt this material for any purpose, provided you give appropriate credit to the original author.
