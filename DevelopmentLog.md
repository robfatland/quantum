# Development Log

Entries here document steps taken so that work in this repo is reproducible.


## 2026-06-26

### Install Qiskit and Aer simulator

```bash
pip install qiskit qiskit-aer
```

This provides the Qiskit circuit SDK and the AerSimulator for local quantum simulation
(no IBM account or API token required).


## 2026-06 through 2026-07

### DSE circuit implementation: failed attempts and lessons learned

**Goal:** Produce a double-slit interference pattern from a gate-based quantum circuit.

**Attempt 1:** Slit qubit + controlled phases on a screen register + inverse QFT.
Result: flat histogram. The slit qubit remained entangled with the screen register,
which-path information was available, and interference vanished. This is the quantum
eraser problem.

**Attempt 2:** Same circuit with post-selection on slit qubit = 0. Result: still flat.
Phase wrapping and circuit ordering issues made the scheme intractable.

**Attempt 3:** Conditional basis state preparation + QFT. Result: partial success (a
single cos^2 lobe) but parameter tuning was unreliable. Integer constraints on slit
separation produced comb artifacts at higher values.

**Attempt 4:** `qc.initialize(amplitudes)` with classically pre-computed cos^2 values,
then transpile to basis gates. Result: correct histogram, but the quantum computer was
just replaying a pre-computed answer. Dishonest algorithm.

**What worked:** A literature search turned up a single-qubit H-P-H circuit
(ref: Akshat-Srivastava015 on GitHub). One qubit per screen position:
H puts qubit in superposition, P(phi) encodes path-length difference, second H
interferes the paths, measurement gives P(0) = cos^2(phi/2). Sweep phi across
screen positions to build the full fringe pattern. Honest physics, simple circuit.

**Cautionary note on AI-assisted development:** Attempts 1-4 were constructed with
heavy AI model guidance. The model generated plausible multi-qubit circuits that
looked sophisticated but failed for fundamental physical reasons (entanglement
destroying interference). The human operator should have:
- Applied more skepticism to complex multi-qubit proposals
- Conducted a literature search earlier (the correct single-qubit approach was
  published and findable)
- Recognized that "more qubits = more realistic simulation" is not always true
- Tested simpler hypotheses before scaling up

The working solution was the simplest possible circuit (one qubit, three gates).
Complexity was the enemy. A 30-minute literature search would have saved days of
debugging.

### Implementation files

- `double_slit_statevector.py` — Statevector-based (no shots), computes P(|0>) at
  each screen position analytically, then samples photons
- `double_slit.py` — Real H-P-H-M circuits with measurement statistics; supports
  `--backend local` (AerSimulator) and `--backend ibm` (IBM hardware via SamplerV2)
- Both apply sinc^2 envelope post hoc for finite slit width
