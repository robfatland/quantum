# Cloud Quantum Computing: Comparative Overview


Four major cloud platforms offer quantum computing services. They differ in hardware
ownership, access models, pricing, and SDK ecosystems. This document provides a concise
comparison.


## Summary Table

| | **AWS Braket** | **Azure Quantum** | **IBM Quantum** | **Google Quantum AI** |
|---|---|---|---|---|
| **Model** | Marketplace (third-party hardware) | Marketplace (third-party hardware) | Vertically integrated (IBM hardware only) | Research lab (Google hardware only) |
| **SDK** | Amazon Braket SDK (Python) | Q#, Qiskit, Cirq (multi-SDK) | Qiskit (Python) | Cirq (Python) |
| **Hardware providers** | IQM, Rigetti, IonQ, QuEra | IonQ, Quantinuum, Rigetti, Pasqal | IBM (superconducting transmon) | Google (superconducting transmon) |
| **Qubit technologies** | Superconducting, trapped ion, neutral atom | Superconducting, trapped ion, neutral atom | Superconducting only | Superconducting (+ neutral atom research) |
| **Public on-demand access** | Yes | Yes | Yes | No (research partnerships only) |
| **Free tier** | 1 hr/month managed simulation | $500 credits per provider | 10 min QPU time per 28 days | Open-source simulation only |
| **Pricing unit** | Per task ($0.30) + per shot | Per provider (gates, HQCs, shots) | Per second of QPU time (~$1.60/sec) | No public pricing; reservation grants |
| **Max qubits (single processor)** | ~54 (IQM Emerald) | ~36 (IonQ Forte) | 1,121 (Condor) / 156 (Heron, production) | 105 (Willow) |
| **Managed notebooks** | Yes (Braket notebooks) | Yes (workspace notebooks) | Yes (Qiskit tutorials / labs) | Colab templates |
| **Hybrid jobs** | Yes (Braket Hybrid Jobs) | Yes (via provider workflows) | Yes (Qiskit Runtime sessions) | No managed hybrid service |


## Key Differentiators

**AWS Braket** is a hardware-agnostic marketplace. Its strength is breadth: you can target
superconducting, trapped-ion, and neutral-atom hardware through one SDK without committing
to a single vendor. Pricing is straightforward (flat per-task fee + per-shot). Best for
teams that want to benchmark across hardware types with minimal friction.

**Azure Quantum** is also a marketplace but distinguishes itself with multi-SDK support
(Q#, Qiskit, Cirq) and generous free credits ($500 per provider). It includes resource
estimation tools for projecting future fault-tolerant requirements. Best for organizations
already in the Azure ecosystem or those wanting to use Microsoft's Q# language.

**IBM Quantum** is vertically integrated: IBM builds the hardware, the SDK (Qiskit), and
the runtime. It has the largest qubit counts, the most mature software ecosystem, and the
longest track record (since 2016). The free tier gives real QPU access. Best for teams
that want depth over breadth — deep Qiskit expertise, error mitigation built in, and a
clear hardware roadmap through 2033.

**Google Quantum AI** is a research-first operation. The hardware is not publicly available
on-demand; access requires partnership or competitive application. However, Cirq and qsim
are fully open-source and the simulation capabilities are strong. Google leads in
error-correction research (Willow). Best for academic researchers pursuing hardware-aware
algorithm development or collaborating directly with Google's quantum team.


## Choosing a Platform

| If you want to... | Consider |
|---|---|
| Compare multiple hardware vendors quickly | AWS Braket or Azure Quantum |
| Use free QPU time to learn | IBM Quantum (Open Plan) |
| Write in Q# | Azure Quantum |
| Access the most qubits | IBM Quantum |
| Focus on error correction research | Google Quantum AI (apply for access) |
| Minimize cloud vendor lock-in | Cirq or Qiskit (both open-source, portable) |
| Run large simulations cheaply | Google qsim on GCP or AWS Braket SV1 |
| Stay in an existing cloud ecosystem | Match your current provider (AWS/Azure/GCP) |


## Common Workflow Across All Platforms

Regardless of platform, the quantum computing workflow is:

```
Define qubits → Build circuit (gates + measurements)
    → Transpile/compile for target hardware
    → Submit job (specify shots/repetitions)
    → Wait for execution (seconds to hours depending on queue)
    → Retrieve measurement results (counts/probabilities)
```

All four platforms support Python as the primary interface language. Circuits written in
Qiskit or Cirq can often be translated between platforms with moderate effort, though
hardware-specific optimizations are not portable.


## See Also

- [aws/README.md](aws/README.md) — detailed AWS Braket guide
- [azure/README.md](azure/README.md) — detailed Azure Quantum guide
- [ibm/README.md](ibm/README.md) — detailed IBM Quantum guide
- [gcp/README.md](gcp/README.md) — detailed Google Quantum AI guide
