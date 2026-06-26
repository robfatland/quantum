# Amazon Braket


## Overview

Amazon Braket is a fully managed AWS service for quantum computing. It provides a unified
development environment — the Braket SDK (Python) — through which you can design quantum
circuits, run them on classical simulators, and execute them on real quantum processing
units (QPUs) from multiple hardware providers. The hardware includes superconducting
qubit processors (IQM, Rigetti), trapped-ion processors (IonQ), and neutral-atom
devices (QuEra). You interact with all of these through a consistent API, paying only
for what you use.

The workflow is: build a circuit using the Python SDK, choose a target device (local
simulator, managed simulator, or QPU), submit the circuit as a *task* with a specified
number of *shots* (repetitions), and retrieve measurement results from S3. Braket also
supports hybrid quantum-classical jobs for variational algorithms, OpenQASM 3.0 circuit
definitions, and optional reserved/dedicated capacity for time-sensitive workloads.
See [AWS Braket documentation](https://docs.aws.amazon.com/braket/latest/developerguide/what-is-braket.html)
for the full developer guide.


## Getting Started

1. In the AWS Console, find **Quantum Technologies** and agree to terms.
2. Click **Enable Amazon Braket**.
3. Launch a Braket-managed notebook instance (comes with SDK and examples pre-installed).
4. Alternatively, install the SDK locally: `pip install amazon-braket-sdk`.


## Key Concepts

| Term | Meaning |
|------|---------|
| **Circuit** | A sequence of quantum gates applied to qubits |
| **Shot** | A single execution (measurement) of a circuit |
| **Task** | A submission of a circuit for some number of shots on a device |
| **Device** | A simulator or QPU that runs your task |
| **Hybrid Job** | A managed workflow combining classical and quantum computation |


## Devices

Braket offers three categories of devices:

**Quantum Processing Units (QPUs)**
- IQM (superconducting) — Garnet (20 qubits), Emerald (54 qubits) — Stockholm region
- Rigetti (superconducting) — US regions
- IonQ (trapped ion) — US regions
- QuEra (neutral atom) — US regions

**Managed Simulators**
- SV1 — state vector simulator (up to 34 qubits)
- DM1 — density matrix simulator (up to 17 qubits)
- TN1 — tensor network simulator (up to 50 qubits)

**Local Simulator**
- Included in the SDK; runs on your machine (up to ~25 qubits depending on RAM)

> Note: Each device has an associated AWS Region. Check the console for availability.


## Pricing

There are two components when using QPUs:

| Component | Cost |
|-----------|------|
| Per-task fee | $0.30 (flat, all QPUs) |
| Per-shot fee | Varies by device (fractions of a cent) |

- Gate-based QPU shot pricing is independent of circuit depth or gate count.
- IonQ requires a minimum of 2,500 shots per task when using error mitigation.
- Managed simulators are priced per minute of EC2 compute time.
- The local simulator is free (it's your own CPU).
- 1 free hour of managed simulation per month under the AWS Free Tier.

See [Braket Pricing](https://aws.amazon.com/braket/pricing/) for current rates.


## Example: Bell State Circuit

```python
from braket.circuits import Circuit
from braket.devices import LocalSimulator

# Build a Bell state circuit
bell = Circuit().h(0).cnot(0, 1)
print(bell)

# Run on local simulator
local_sim = LocalSimulator()
result = local_sim.run(bell, shots=1000).result()

# View results
counts = result.measurement_counts
print(counts)  # e.g. Counter({'00': 503, '11': 497})
```

To run on a real QPU:

```python
from braket.aws import AwsDevice

# Choose a device (example: IonQ Aria)
device = AwsDevice("arn:aws:braket:us-east-1::device/qpu/ionq/Aria-1")

# Submit task — results go to your S3 bucket
task = device.run(bell, s3_destination_folder=("my-bucket", "braket-results"), shots=1000)

# Wait for completion and get results
result = task.result()
print(result.measurement_counts)
```


## Checking Job Status and Results

- In the Braket console, use the left menu to navigate to **Tasks** or **Jobs**.
- View completion status, device used, shot count, and cost.
- Download results directly or retrieve them from S3.

Results are returned as JSON:

```json
{
    "braketSchemaHeader": {
        "name": "braket.task_result.gate_model_task_result",
        "version": "1"
    },
    "measurements": [
        [1, 1],
        [0, 0],
        [1, 1]
    ],
    "measuredQubits": [0, 1],
    "measurementProbabilities": {
        "00": 0.503,
        "11": 0.497
    }
}
```


## Resources

- [Braket Developer Guide](https://docs.aws.amazon.com/braket/latest/developerguide/what-is-braket.html)
- [Braket Python SDK (GitHub)](https://github.com/amazon-braket/amazon-braket-sdk-python)
- [Braket Example Notebooks](https://github.com/amazon-braket/amazon-braket-examples)
- [Braket Pricing](https://aws.amazon.com/braket/pricing/)
