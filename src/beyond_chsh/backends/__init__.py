"""Execution backends: ideal simulation, noisy simulation, IBM hardware.

The three modes are strictly separated. An :class:`~beyond_chsh.data.schemas.
ExperimentRecord` produced by a simulator always has ``mode`` in
{'ideal', 'noisy'}; only ``ibm_runtime`` sets ``mode='hardware'``.
"""
