"""Noisy backend: Aer simulation with a controlled, reproducible NoiseModel."""

from __future__ import annotations

from ..circuits.bell_states import BellState
from ..noise.channels import NoiseSpec, build_noise_model
from ..theory.probabilities import JointDistribution, counts_to_joint


def run_noisy_sampled(
    spec: NoiseSpec,
    shots: int = 8192,
    *,
    seed: int = 42,
    state: BellState = BellState.PHI_PLUS,
) -> dict[tuple[int, int], JointDistribution]:
    """Finite-shot simulation under a NoiseSpec, seeded for reproducibility."""
    from qiskit_aer import AerSimulator  # lazy import

    from ..circuits.chsh import build_all_chsh_circuits

    noise_model = build_noise_model(spec)
    sim = AerSimulator(noise_model=noise_model)
    circuits = build_all_chsh_circuits(state=state)
    out: dict[tuple[int, int], JointDistribution] = {}
    for xy, qc in circuits.items():
        result = sim.run(qc, shots=shots, seed_simulator=seed).result()
        out[xy] = counts_to_joint(result.get_counts())
    return out
