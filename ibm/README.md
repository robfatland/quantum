# IBM Quantum


## Overview

IBM Quantum is the longest-running cloud quantum computing platform, having put the first
quantum computer online in 2016. It provides access to IBM's fleet of superconducting
transmon qubit processors through the Qiskit SDK, an open-source Python framework for
building, optimizing, and executing quantum circuits. The platform now serves over 400,000
users and offers processors ranging from free-tier access on smaller systems to utility-scale
machines with 100+ qubits.

The execution model centers on Qiskit Runtime, a cloud-native service that co-locates
classical and quantum computation. You write circuits in Qiskit, transpile them for a
specific backend, and submit them as jobs. Qiskit Runtime's "primitives" (Sampler and
Estimator) abstract away low-level execution details and include built-in error mitigation.
IBM's roadmap targets quantum advantage by end of 2026 and fault-tolerant quantum computing
by 2029. See the [IBM Quantum documentation](https://docs.quantum.ibm.com/) for full details.


### Cost context for the DSE experiment

IBM charges by QPU time (~$1.60/second on Pay-As-You-Go). Our DSE circuit is H-P-H on a
single qubit: 3 gates, each taking ~20-50 ns. A full experiment of 200 screen positions
at 2000 shots each (400,000 circuit executions) consumes only a few seconds of QPU time,
costing roughly **$5-10 per run**. Four runs cost under $50 total.

This makes IBM by far the cheapest real-hardware option among the cloud quantum providers
available in 2026. IonQ charges $0.08/shot ($32,000 for the same experiment). Rigetti on
AWS is ~$200. Quantinuum on Azure is $1,000+. IBM's time-based pricing strongly favors
short, shallow circuits run at high shot counts — exactly what the DSE requires.

The topic of quantum hardware pricing involves considerable finesse (error mitigation costs,
queue priority, session overhead, transpilation depth affecting wall-clock time, etc.) that
is out of scope here. The key point: for single-qubit or few-qubit circuits with many shots,
IBM is the most cost-effective option by one to three orders of magnitude.


## Getting Started

1. Create an account at [IBM Quantum Platform](https://quantum.cloud.ibm.com/).
2. The **Open Plan** (free) gives you up to 10 minutes of QPU time per 28-day rolling window.
3. Install the SDK locally: `pip install qiskit qiskit-ibm-runtime`
4. Retrieve your API token from the platform dashboard.
5. Save credentials (one-time setup):

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_cloud",        # or "ibm_quantum" for legacy platform
    token="YOUR_API_KEY",
    instance="YOUR_CRN",        # CRN for ibm_cloud; hub/group/project for ibm_quantum
    overwrite=True,
    set_as_default=True
)
```

This stores credentials in `~/.qiskit/qiskit-ibm.json` — **external to this repo**.
The token is never committed to version control. Subsequent connections require no
arguments:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()  # picks up saved default
```

> **Security note:** Never place API tokens in source files or commit them to git.
> The `save_account()` call writes to your home directory, outside the repository.
> If credentials are accidentally exposed, rotate the API key immediately in the
> IBM Cloud console (IAM $\to$ API keys) or the quantum.ibm.com dashboard.


## Key Concepts

| Term | Meaning |
|------|---------|
| **Circuit** | A sequence of quantum gates and measurements expressed in Qiskit |
| **Transpilation** | Compiling an abstract circuit to the native gate set and topology of a specific processor |
| **Primitive** | A high-level execution interface (Sampler for probabilities, Estimator for expectation values) |
| **Job** | A submitted workload; tracked by job ID with status, results, and cost |
| **Instance** | An organizational unit (hub/group/project) that governs access and billing |
| **QPU time** | The billable unit — seconds of quantum processor usage |


## Processors

IBM uses superconducting transmon qubits exclusively. Current processor families:

| Processor | Qubits | Notes |
|-----------|--------|-------|
| **Nighthawk** | 120 | Square-lattice topology (218 couplers), most advanced as of early 2026 |
| **Heron** | 156 | Heavy-hex topology, fast high-fidelity gates, current workhorse |
| **Eagle** | 127 | Previous generation, widely deployed |
| **Condor** | 1,121 | Largest qubit count (2023), primarily a scaling demonstration |

Systems are deployed globally (US, Japan, Europe) as IBM Quantum System One and System Two.


## Pricing

| Plan | Cost | Access |
|------|------|--------|
| **Open** (free) | $0 | Up to 10 min QPU time per 28-day window on select systems |
| **Pay-As-You-Go** | ~$1.60/sec (varies by system) | All available processors, billed per second of QPU usage |
| **Flex** | Starting at $30,000 | Premium-level access for project-based research |
| **Premium** | Custom quote | Dedicated capacity, priority queuing, support |

See [IBM Quantum Pricing](https://www.ibm.com/quantum/pricing) for current rates.


## Example: Bell State

```python
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

# Connect
service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
backend = service.least_busy(min_num_qubits=2, operational=True)

# Build circuit
bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)
bell.measure_all()

# Run using the Sampler primitive
sampler = SamplerV2(mode=backend)
job = sampler.run([bell], shots=1000)
result = job.result()
print(result[0].data.meas.get_counts())
# e.g. {'00': 498, '11': 502}
```


## Qiskit Ecosystem

- **Qiskit SDK** — circuit construction, transpilation, visualization
- **Qiskit Runtime** — cloud execution with primitives (Sampler, Estimator)
- **Qiskit Aer** — local high-performance simulators (statevector, density matrix, noise models)
- **Qiskit Nature / Finance / Optimization** — domain-specific application modules
- **Qiskit Fermions** — quantum chemistry library (new in 2026)
- **Qiskit Functions Catalog** — pre-built abstractions from ecosystem partners


## Resources

- [IBM Quantum Documentation](https://docs.quantum.ibm.com/)
- [Qiskit SDK (GitHub)](https://github.com/Qiskit/qiskit)
- [Qiskit Tutorials](https://learning.quantum.ibm.com/)
- [IBM Quantum Pricing](https://www.ibm.com/quantum/pricing)
- [Processor Types](https://docs.quantum.ibm.com/run/processor-types)
