# Infleqtion (Superstaq / Sqale)

## Overview

Infleqtion is a quantum hardware company building **gate-based neutral-atom** quantum
computers. Their flagship machine is **Sqale**. Neutral-atom qubits are laser-trapped and
laser-cooled atoms, so the processor operates at room temperature (no dilution
refrigerator), in contrast to superconducting transmon qubits (IBM, Google). Infleqtion
has also demonstrated logical (error-corrected) qubits layered on top of the physical
neutral-atom qubits, including joint work with NVIDIA.

Unlike AWS Braket and Azure Quantum (marketplace platforms reselling third-party QPUs),
Infleqtion builds and operates its own hardware. As of 2026 their hardware access is
**entirely bespoke** — there is no public self-serve, pay-as-you-go signup comparable to
IBM. Access is arranged directly with Infleqtion.

> CloudBank status: hardware access to be discussed directly with Infleqtion at an
> upcoming conference. The intel below is gathered from public sources; pricing and
> hardware-access terms are deferred to that conversation.

The software you actually program against is **Superstaq**, a cross-platform
compiler/optimization API. You write circuits in **Cirq or Qiskit** — not a proprietary
language — and Superstaq performs low-level compilation and cross-layer optimization for
the target backend, then dispatches to Infleqtion hardware or to other QPUs and
simulators. This means our existing Qiskit circuit code (e.g. `double_slit.py`) is
largely reusable: only the execution/submission layer changes, the circuit construction
stays the same.

See [superstaq.readthedocs.io](https://superstaq.readthedocs.io) for documentation.


## Getting Started

Since our existing code is Qiskit-based, the `qiskit-superstaq` client is the natural
entry point.

1. Install the Qiskit client: `pip install qiskit-superstaq`
   - Cirq users: `pip install cirq-superstaq`
   - Backend-agnostic client: `pip install general-superstaq`
2. Obtain a Superstaq API key / account (see Access Model below).
3. Work through the tutorials on the [documentation site](https://superstaq.readthedocs.io).
4. Target a backend by swapping only the submission path — conceptually the same move as
   our `run_ibm()` vs `run_local()` split in `double_slit.py`. The H-P-H-M circuit
   construction is unchanged.

> Superstaq is in open beta, with expanded onboarding tutorials and improved error
> messaging as of 2026.


## Access Model

- **Bespoke hardware access** — no public pay-per-shot marketplace for Sqale. Terms are
  arranged directly with Infleqtion.
- **Superstaq compiler + simulators** — accessible via the open-source client packages
  and a Superstaq account.
- **Through NVIDIA CUDA-Q** — Infleqtion is documented as a neutral-atom provider
  reachable via CUDA-Q, with Superstaq still the compilation layer underneath. Relevant
  if we go the GPU-accelerated route.
- **Contact** — superstaq@infleqtion.com, or the Superstaq Slack workspace.


## Key Concepts

| Term | Meaning |
|------|---------|
| **Neutral atom** | Qubit encoded in an individual laser-trapped atom; room-temperature operation |
| **Sqale** | Infleqtion's gate-based neutral-atom quantum computer |
| **Superstaq** | Cross-layer compiler/optimization API; front end in Cirq or Qiskit |
| **qiskit-superstaq** | Qiskit client package for Superstaq (our entry point) |
| **cirq-superstaq** | Cirq client package for Superstaq |
| **general-superstaq** | Backend-agnostic Superstaq client |
| **Atom movement** | Physically relocating atoms as an alternative to expensive gate decompositions during compilation |
| **Local addressability** | The (limited) ability to apply single-qubit rotations to individual atoms; a key neutral-atom compilation constraint |


## Why Neutral Atoms (vs our IBM superconducting work)

- **Room-temperature operation** — no dilution fridge; the atoms are trapped and cooled by lasers.
- **Global gates + atom movement** — current neutral-atom architectures lean on global
  (all-qubit) gates and on physically moving atoms for routing, rather than arbitrary
  local single-qubit addressing. Compilation differs substantially from the
  superconducting model.
- **Error correction focus** — Infleqtion emphasizes logical qubits, magic-state
  production, high-fidelity entangling operations, and in-place syndrome measurement for
  scalable fault tolerance.


## Resources

- [Superstaq documentation (readthedocs)](https://superstaq.readthedocs.io)
- [Infleqtion/client-superstaq GitHub](https://github.com/Infleqtion/client-superstaq) (Apache 2.0)
- [Infleqtion/resource-superstaq GitHub](https://github.com/Infleqtion/resource-superstaq) — architecture-level resource estimator
- [Infleqtion: Sqale Quantum Computer](https://infleqtion.com/quantum-computing/)
- [Infleqtion: Zero to Quantum (intro to neutral atoms)](https://infleqtion.com/zero-to-quantum/)
- [CUDA-Q neutral-atom backend docs](https://nvidia.github.io/cuda-quantum/0.12.0/using/backends/hardware/neutralatom.html)
- Paper: [Compiling to the neutral-atom native gate set (arXiv:2307.14996)](https://arxiv.org/pdf/2307.14996v1.pdf) — local-addressability constraints, atom-movement routing
- Paper: [Compilation-driven resource estimation for neutral-atom fault tolerance (arXiv:2604.01376)](https://arxiv.org/pdf/2604.01376)


## Open Questions for the Infleqtion Conversation

- Hardware-access model and pricing for Sqale (bespoke — to be negotiated).
- Qubit count, connectivity, native gate set, and current fidelities of Sqale.
- Simulator access and limits via Superstaq (free tier? queue?).
- How CloudBank users would authenticate and submit jobs in practice.
- Fit with our existing Qiskit H-P-H-M double-slit demo and the Bell/CHSH experiment.

_Intel compiled from public sources; content rephrased for compliance with licensing restrictions._
