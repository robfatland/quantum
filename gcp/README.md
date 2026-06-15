# Google Quantum AI


## Overview

Google Quantum AI is Google's quantum computing research division, operating its own
superconducting qubit processors (Sycamore, Willow) and providing access through the
Quantum Engine service and the open-source Cirq framework. Unlike AWS and Azure — which
are marketplace platforms offering third-party hardware — Google builds and operates its
own quantum hardware. Access is more research-oriented: there is no public pay-per-shot
marketplace. Instead, access is granted through research partnerships, the Willow Early
Access Program, and collaborations with institutions like the NQCC (UK).

The software stack centers on Cirq, a Python library for constructing, simulating, and
optimizing quantum circuits. Cirq is hardware-aware: it understands device topologies and
native gate sets, allowing you to write circuits that map efficiently onto physical qubits.
For simulation at scale, Google provides qsim, a high-performance state-vector simulator
that can run on GCP compute instances. Google's roadmap focuses on error-corrected quantum
computing, with Willow demonstrating below-threshold error correction in 2024-2025.
See [Google Quantum AI](https://quantumai.google/) for documentation and research papers.


## Getting Started

1. Install Cirq: `pip install cirq`
2. For local simulation, Cirq includes built-in simulators.
3. For high-performance simulation on GCP, use qsim: `pip install qsimcirq`
4. For hardware access, apply through the [Willow Early Access Program](https://quantumai.google/willowearlyaccess) or institutional partnerships.
5. Use Google Colab notebooks for quick experimentation — templates are available in the Cirq documentation.

> Hardware access is not publicly available on-demand. It requires an approved research proposal.


## Key Concepts

| Term | Meaning |
|------|---------|
| **Circuit** | A sequence of moments (time slices), each containing non-overlapping gates |
| **Moment** | A time step in which gates operate in parallel on disjoint qubits |
| **Device** | A description of hardware constraints (connectivity, native gates) |
| **Quantum Engine** | Google's cloud API for submitting circuits to real processors |
| **Program** | A circuit submitted to the Quantum Engine |
| **Job** | An execution of a program with specified parameters and repetitions |
| **Calibration** | Device characterization data (gate fidelities, T1/T2 times) available per processor |


## Processors

Google develops superconducting transmon qubit processors:

| Processor | Qubits | Significance |
|-----------|--------|-------------|
| **Willow** | 105 | Current flagship; demonstrated below-threshold quantum error correction (2024-2025) |
| **Sycamore** | 53-72 | Achieved "quantum supremacy" claim (2019); used in numerous research publications |

Google announced in March 2026 that it is also exploring neutral-atom quantum computing
alongside its superconducting program.

> Processors are not available on-demand publicly. Access is via research programs.


## Access Model

Google's access model differs significantly from AWS/Azure/IBM:

- **No public pay-per-use pricing** — there is no per-shot or per-task fee schedule.
- **Research partnerships** — academic and industrial collaborators gain access through agreements.
- **Willow Early Access Program** — competitive application process; proposals reviewed by Google Quantum AI.
- **NQCC collaboration** — UK researchers can apply for Willow access through the National Quantum Computing Centre.
- **Reservations** — approved users receive time grants on processors; no per-job fee, usage governed by reservation.
- **Simulation is open** — Cirq and qsim are fully open-source; you can simulate locally or on GCP compute at standard GCP pricing.


## Example: Bell State with Cirq

```python
import cirq

# Define qubits
q0, q1 = cirq.LineQubit.range(2)

# Build a Bell state circuit
circuit = cirq.Circuit([
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='result')
])
print(circuit)

# Simulate locally
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)
print(result.histogram(key='result'))
# e.g. Counter({0: 509, 3: 491})  — 0 = '00', 3 = '11' in binary
```

To run on Google hardware (with approved access):

```python
import cirq_google

# Connect to the Quantum Engine
engine = cirq_google.Engine(project_id='your-gcp-project')

# Get a processor
processor = engine.get_processor('your-processor-id')

# Submit job
job = processor.run(circuit, repetitions=1000)
results = job.batched_results()
```


## Simulation on GCP

For circuits too large to simulate locally, use qsim on GCP:

- **qsim** — C++ state-vector simulator with a Cirq interface (`qsimcirq`)
- Supports up to ~40 qubits on a single high-memory VM
- Can run on GCE instances (N2, C2 machine types recommended)
- Also available as a Docker container for Colab integration
- **Quantum Virtual Machine** — simulates a specific Google processor including realistic noise models

```python
import qsimcirq

qsim_simulator = qsimcirq.QSimSimulator()
result = qsim_simulator.run(circuit, repetitions=10000)
```


## Cirq Features

- **Hardware-aware compilation** — circuits can be mapped to specific device topologies
- **Noise models** — realistic noise simulation based on device calibration data
- **Moment structure** — explicit parallelism representation
- **Transformers** — circuit optimization passes (gate decomposition, routing, alignment)
- **OpenQASM support** — import/export circuits in QASM format
- **Integration with TensorFlow Quantum** — for quantum machine learning research


## Resources

- [Google Quantum AI](https://quantumai.google/)
- [Cirq Documentation](https://quantumai.google/cirq)
- [Cirq GitHub](https://github.com/quantumlib/Cirq)
- [qsim Simulator](https://quantumai.google/qsim)
- [Quantum Engine API](https://quantumai.google/cirq/google/engine)
- [Willow Early Access Program](https://quantumai.google/willowearlyaccess)
- [Cirq Tutorials](https://quantumai.google/cirq/tutorials)
