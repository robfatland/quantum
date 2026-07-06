# DSE: Double Slit Experiment — Implementation Notes


## Status

Multiple attempts to produce an interference pattern from a gate-based quantum 
circuit failed. A working approach has been identified via an external reference.


## What was tried and why it failed


### Attempt 1: Slit qubit + controlled phases + inverse QFT

**Circuit:** 1 slit qubit + k screen qubits. H on slit → controlled-phase gates 
(encoding path-length difference) → inverse QFT on screen → measure.

**Result:** Flat histogram (uniform noise).

**Why it failed:** The slit qubit remains entangled with the screen register. 
Measuring only the screen qubits traces out the slit qubit, which destroys all 
interference (the which-path information is still encoded in the system). This is 
literally the quantum eraser problem: if path information is *available in principle* 
(even if not measured), interference vanishes.


### Attempt 2: Same as above + post-selection on slit qubit = 0

**Circuit:** Same as attempt 1, but measure the slit qubit too. After H on slit 
before measurement, post-select on slit=0 outcomes (constructive interference subset).

**Result:** Initially all shots were kept (100% slit=0) — indicating no entanglement 
was produced. After fixing the circuit order, got 50/50 split but screen histogram 
was still flat.

**Why it failed:** The phase encoding was either wrapping (large phases mod 2π 
randomizing) or the inverse QFT placement was incorrect relative to the slit 
measurement. Multiple ordering variants were tried without success.


### Attempt 3: Slit controls which computational basis state is prepared, then QFT

**Circuit:** H on slit → conditional X/CX gates to prepare |d⟩ or |N-d⟩ on screen → 
QFT on screen → H on slit → measure.

**Result:** Got a single cos² lobe (one period) with separation=3. With larger 
separation values, got either too many peaks, comb-like artifacts, or Moiré patterns.

**Why it partially worked:** The QFT of (|d⟩ + |N-d⟩)/√2 does produce cos². The 
problem was parameter tuning: `d` must be an integer, and the relationship between 
d and the number of visible fringes is d = number of full periods of cos² across N 
bins. So d=3 gives only 1.5 visible lobes (looked like a single peak). Larger d 
under-sampled the oscillation (comb effect).


### Attempt 4: initialize() + decompose/transpile (the "uncomfortable truth")

**Circuit:** Classically compute A(x) = cos(2πdx/N), normalize, call 
`qc.initialize(amplitudes)`, transpile to basis gates, measure.

**Result:** Works correctly (histogram matches theory) but the circuit is an opaque 
blob of rotations. The quantum computer is not computing interference — it's being 
loaded with a pre-computed answer. The `decompose(reps=3)` left high-level gates 
(`multiplexer_dg`) that AerSimulator didn't recognize; fixed by using `transpile()` 
to basis gates.

**Assessment:** Correct physics, dishonest algorithm. Acceptable as a stopgap but not 
suitable for a demo where the narrative is "the quantum computer computes this."


## The correct approach (from Akshat-Srivastava015 GitHub repo)

**Reference:** https://github.com/Akshat-Srivastava015/Youngs-Double-Slit-Experment-By-using-Qiskit-Quantum-Computing-

**Key insight:** Don't try to encode the full screen as a multi-qubit register. Instead, 
use a **single qubit** and compute the interference probability at each screen position 
*separately*.

**The circuit (per screen position):**

```
    ┌───┐ ┌──────┐ ┌───┐ ┌─┐
q:  ┤ H ├─┤ P(φ) ├─┤ H ├─┤M├
    └───┘ └──────┘ └───┘ └─┘
```

Where $\phi$ = path-length difference at this screen position = $2\pi d \sin\theta / \lambda$.

**How it works:**

1. H puts the qubit in |+⟩ = (|0⟩ + |1⟩)/√2 — superposition of both paths.
2. P(φ) adds a phase to the |1⟩ component — encoding the path-length difference 
   for one specific screen position.
3. Second H interferes the two paths.
4. Measurement: P(0) = cos²(φ/2) — the interference intensity at this position.

**To build the full pattern:** Sweep φ from 0 to 2π × (number of fringes) across 
many screen positions. At each position, the circuit gives the probability. Sample 
many photons according to this probability distribution.

**Why this is honest:** The quantum circuit genuinely computes cos²(φ/2) for each 
position. The H-P-H structure *is* the physical interference: superpose → accumulate 
phase → interfere. It's a 1-qubit demonstration of the same physics that happens in 
the lab.

**Why it's limited:** It's a single qubit per screen position. You don't need a 
quantum computer to compute cos²(φ/2) — a calculator suffices. The quantum advantage 
here is purely pedagogical, not computational. But for a demo, the narrative is 
compelling: "this single qubit is doing what one photon does at one screen position."

**For multi-qubit scaling:** Run the same circuit on many qubits simultaneously 
(one per screen position), or use the Statevector simulator to extract probabilities 
without shots.


## The sinc² envelope

For finite slit width $w$, the full intensity pattern is:

$$I(x) = \cos^2(\pi d x / \lambda L) \cdot \text{sinc}^2(\pi w x / \lambda L)$$

The cos² comes from two-path interference (slit separation $d$).
The sinc² comes from single-slit diffraction (slit width $w$).

In the H-P-H approach, the envelope could be incorporated by modulating the 
*amplitude* of the initial H rotation (using Ry(θ) instead of H, where θ varies 
with screen position according to the sinc envelope). This would give:

```
    ┌────────┐ ┌──────┐ ┌────────┐ ┌─┐
q:  ┤ Ry(θ_x)├─┤ P(φ) ├─┤ Ry†(θ) ├─┤M├
    └────────┘ └──────┘ └────────┘ └─┘
```

Where θ_x encodes the sinc envelope at position x.


## Implementation status

The H-P-H single-qubit approach is implemented in two scripts:

- `double_slit_statevector.py` — uses Statevector to compute $P(|0\rangle)$ analytically 
  at each screen position, then samples photons. Fast, no shots needed.
- `double_slit.py` — builds and executes actual H-P-H-M circuits with real measurement 
  statistics. Supports `--backend local` (AerSimulator) and `--backend ibm` (IBM hardware 
  via qiskit-ibm-runtime / SamplerV2).

Both apply the $\text{sinc}^2$ envelope post hoc and produce circuit diagrams, histograms, 
JSON results, and optional accumulation animations.


## PEARC demo notes (reveal-o-tron concept)

The reveal-o-tron is a Python playback script for live demos:

1. Loads pre-computed results (JSON: circuit metadata + shot-by-shot outcomes)
2. Displays a live-updating visualization (matplotlib or browser)
3. Reveals results incrementally with configurable pauses that mimic compute time
4. Shows the "tier" label and qubit count for each run
5. Optionally runs a Tier 1 job live on the laptop for authenticity

This means the demo never blocks on network or queue. The audience sees the progression
from small/fast to large/slow as if running in real time.

**Three-tier architecture for scaling narrative:**

| Tier | Platform | Role |
|------|----------|------|
| 1 | Dell laptop, AerSimulator | "Learn and develop here" |
| 2 | IBM cloud VM, AerSimulator | "CloudBank gives you more muscle" |
| 3 | IBM quantum hardware | "Beyond any classical machine" |

**Physical demo:** Red laser ($\lambda = 650$ nm) + double-slit slide projecting fringes 
on a white card, running alongside the quantum circuit histogram for direct visual 
comparison.


## Multi-qubit conceptual circuit (pedagogical, not run)

The multi-qubit version (slit qubit + screen register + QFT) remains valid as a 
conceptual illustration of how a full quantum register could encode the screen. It 
failed in practice due to entanglement between the slit qubit and screen register 
destroying interference (see "What was tried" above). The H-P-H approach sidesteps 
this entirely by computing one screen position per circuit.
