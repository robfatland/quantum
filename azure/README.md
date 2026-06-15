# Azure Quantum


## Overview

Azure Quantum is Microsoft's cloud platform for quantum computing. It provides a workspace
environment where you can write quantum programs using multiple SDKs (Q#, Qiskit, Cirq),
run them on simulators or submit them to real quantum hardware from several providers, and
retrieve results — all managed through the Azure portal. The platform also includes
resource estimation tools that let you project what future fault-tolerant quantum machines
would need to run your algorithms.

Azure Quantum is provider-agnostic: through a single workspace you can target trapped-ion
machines (IonQ, Quantinuum), superconducting processors (Rigetti), and neutral-atom devices
(Pasqal). Each provider sets its own pricing. Microsoft also offers $500 in free credits
per provider for new workspaces, making it relatively low-cost to experiment.
See the [Azure Quantum documentation](https://learn.microsoft.com/en-us/azure/quantum/)
for the full developer guide.


## Getting Started

1. In the Azure portal, create a new **Azure Quantum** resource.
2. This creates a **quantum workspace** inside a Resource Group.
3. Add providers (IonQ, Quantinuum, Rigetti, Pasqal) during setup — each comes with free credits.
4. Open **Notebooks** from the left menu in the workspace to access a hosted Jupyter environment with sample notebooks.
5. Alternatively, develop locally with the Azure Quantum SDK: `pip install azure-quantum`

> Add tags to your resource group — they help the casual or future observer.


## Key Concepts

| Term | Meaning |
|------|---------|
| **Workspace** | An Azure resource that organizes your quantum jobs, providers, and notebooks |
| **Provider** | A hardware/software vendor offering targets (IonQ, Quantinuum, Rigetti, Pasqal) |
| **Target** | A specific QPU or simulator you submit jobs to (e.g. `ionq.simulator`, `ionq.qpu`) |
| **Job** | A submitted quantum program with a unique ID, trackable in the portal |
| **Shot** | A single execution/measurement of your circuit |


## Providers and Hardware

| Provider | Technology | Targets |
|----------|-----------|---------|
| **IonQ** | Trapped ion | Aria (25 qubits), Forte (36 qubits), simulator (up to 29 qubits) |
| **Quantinuum** | Trapped ion | H-Series (high fidelity, mid-circuit measurement), emulators |
| **Rigetti** | Superconducting | Ankaa-class processors, simulator |
| **Pasqal** | Neutral atom | Fresnel (up to 100 qubits) |

> Provider availability varies by region and billing country.
> See [provider availability](https://learn.microsoft.com/en-us/azure/quantum/provider-global-availability).


## Pricing

Each provider controls its own pricing. General structure:

- **IonQ**: Billed per gate. Single-qubit gates cost ~0.225× a two-qubit gate. Simulators are typically covered by free credits.
- **Quantinuum**: Uses H-System Quantum Credits (HQCs) based on circuit complexity.
- **Rigetti**: Per-shot pricing.
- **Pasqal**: Per-job pricing.

New workspaces receive **$500 in free credits per provider** to get started.

See [Azure Quantum Pricing](https://learn.microsoft.com/en-us/azure/quantum/credits-faq) for current rates.


## Workflow

```
Create workspace → Choose SDK (Q#, Qiskit, Cirq) → Build circuit
    → Select target (simulator or QPU) → Submit job → Await results
    → Retrieve from Job Management or programmatically via job ID
```


## Example: Hello World with Cirq on IonQ

From the hosted notebook environment:

```python
from azure.quantum.cirq import AzureQuantumService
import cirq

# Connect to your workspace
service = AzureQuantumService(
    resource_id="/subscriptions/.../resourceGroups/.../providers/Microsoft.Quantum/Workspaces/...",
    location="eastus"
)

# List available targets
print(service.targets())

# Build a simple circuit: Hadamard on one qubit
q = cirq.LineQubit(0)
circuit = cirq.Circuit(cirq.H(q), cirq.measure(q, key='result'))

# Submit to IonQ simulator
job = service.run(circuit, repetitions=100, target="ionq.simulator")
print(job.histogram(key='result'))  # e.g. Counter({0: 53, 1: 47})
```

To run on actual hardware, change the target:

```python
job = service.run(circuit, repetitions=100, target="ionq.qpu.aria-1")
```

> QPU jobs may take minutes to hours depending on queue depth.
> The job persists — you can close the notebook and retrieve results later.


## Job Management

- Navigate to **Job management** in the workspace left menu.
- View all submitted jobs with their IDs, targets, status, and timestamps.
- Click a job name for details: input circuit, output results, execution time.
- Recover results programmatically:

```python
job = service.get_job('c815e04e-aaf0-11ec-8cb5-001579a031ca')
result = job.results()
print(result.probabilities())  # e.g. {0: 0.47, 1: 0.53}
```


## Sample Notebooks

The workspace comes with sample notebooks covering:

- **Hello World** variants (Cirq/IonQ, Qiskit, Q#)
- **Grover's search** algorithm
- **Hidden shift** problem
- **Noisy Deutsch-Jozsa** algorithm
- **Parallel QRNG** (quantum random number generation)

Copy them to **My Notebooks** to edit and run.


## Notes from Experience

- Cell output does not persist between sessions in the hosted notebook environment.
- The `AzureQuantumService()` connection object must be recreated each session.
- QPU jobs may queue for hours (one observed case: 17 hours wall time, 2 seconds execution).
- Use `job.job_id()` to save the ID before closing a session.
- The notebook environment is Jupyter-like but not identical (e.g. some keyboard shortcuts differ).


## Resources

- [Azure Quantum Documentation](https://learn.microsoft.com/en-us/azure/quantum/)
- [Q# Language Overview](https://learn.microsoft.com/en-us/azure/quantum/qsharp-overview)
- [Provider List & Targets](https://learn.microsoft.com/en-us/azure/quantum/qc-target-list)
- [Azure Quantum Pricing](https://learn.microsoft.com/en-us/azure/quantum/credits-faq)
- [Azure Quantum on GitHub](https://github.com/microsoft/qdk-python)
