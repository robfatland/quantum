# Development Log

Entries here document steps taken so that work in this repo is reproducible.


## Important commands (easy to forget)

Reference list of commands that are needed occasionally and easy to forget.

- **Open the slide deck in a browser** (run from WSL `~/quantum`):
  ```bash
  explorer.exe slides.html
  ```
  Launches the Windows default browser on the generated `slides.html` via the WSL interop shim.


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


## 2026-10-14

### Confirm Amazon Braket SDK is installed (argosy conda env)

The AWS quantum SDK is the Amazon Braket SDK (distribution `amazon-braket-sdk`,
import package `braket`), not Qiskit. Checked it is present in the `argosy`
miniconda env on WSL.

Note: the top-level `braket` namespace package has no `__version__` attribute,
so query the distribution metadata instead:

```bash
python -c "from importlib.metadata import version; print(version('amazon-braket-sdk'))"
# -> 1.124.0
```

Smoke test that the SDK imports and builds a circuit:

```bash
python -c "from braket.circuits import Circuit; print(Circuit().h(0))"
```

If it were missing, install with:

```bash
pip install amazon-braket-sdk
```

Context: environment already had Qiskit + Aer (see 2026-06-26). Braket enables
the AWS path (hardware-agnostic: IonQ, Rigetti, IQM, and the local/SV1
simulators), complementing the IBM/Qiskit path.


### Cross-validate H-P-H DSE point: Qiskit vs Braket

Extended `dse_one_point.py` to run the single-point double-slit circuit on both
SDKs and compare. Braket runs on its LOCAL simulator (no AWS account, no cloud
spend).

Gate note: Braket has no `P(phi)` gate, so the Braket circuit uses `Rz(phi)`.
`Rz` and `P` differ only by a global phase (unobservable), so measurement
probabilities are identical.

Run:

```bash
python ~/quantum/dse_one_point.py
```

Result (theta = 3 deg, d = 3 um, lambda = 650 nm, fringe order m = 0.2416,
phi = 1.5177 rad):

- Qiskit exact P(0) = 0.526532
- Braket exact P(0) = 0.526532
- |difference| = 2.22e-16  (machine epsilon) -> MATCH

Shot runs (N = 10000) differ only by independent RNG: Qiskit 5281/4719
(chi^2 = 0.099), Braket 5227/4773 (chi^2 = 0.589); both consistent with the
Born-rule expectation 5265.3/4734.7. Confirms the two SDKs agree on the DSE
H-P-H algorithm and that the Rz/P substitution is harmless.
