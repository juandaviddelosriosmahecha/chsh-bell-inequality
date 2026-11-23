"""Beyond CHSH: correlator-level analysis of quantum randomness under hardware noise.

The package is layered so the scientific core (``theory``, ``analysis``) depends
only on numpy/scipy and can be imported and tested without Qiskit installed.
Qiskit-dependent code lives in ``circuits`` and ``backends`` and is imported
lazily.
"""

__version__ = "2.0.0"
