# Running on IBM Quantum hardware

> Optional. All simulation and analysis run without any account.

## 1. Credentials

```bash
cp .env.example .env
# edit .env and set IBM_QUANTUM_TOKEN (get it from https://quantum.ibm.com/)
```

Credentials are read from environment variables only. Never commit `.env`.

## 2. Install the quantum extra

```bash
pip install -e ".[quantum]"
```

Pinned versions (matching the validated v1.0.0 toolchain): qiskit 2.3.1,
qiskit-aer 0.17.2, qiskit-ibm-runtime 0.45.1.

> **API verification required.** Qiskit Runtime APIs change between releases.
> Before a production run, verify the calls in `backends/ibm_runtime.py`
> (`QiskitRuntimeService`, `generate_preset_pass_manager`, `SamplerV2`,
> result/counts access) against the official docs at
> <https://docs.quantum.ibm.com/>.

## 3. Run

```bash
beyond-chsh hardware --backend ibm_torino --shots 5000
# or omit --backend to use the least-busy operational device
```

The command transpiles the four CHSH circuits, runs them with `SamplerV2`
(counts route, so joint distributions are preserved), and writes a complete
`ExperimentRecord` JSON to `data/raw/`.

## What is recorded

experiment id, backend name, job ids, shots, optimization level, transpiled
depth per circuit, raw counts, calibration metadata, software versions, and
UTC timestamp. Simulated runs never carry `mode='hardware'`.
