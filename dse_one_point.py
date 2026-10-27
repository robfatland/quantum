"""
dse_one_point.py

Single-point double-slit experiment (DSE) probe using the H-P(phi)-H circuit.

Looks at ONE position on the detection screen (a chosen off-axis angle) and
reports:
  1. The exact Born-rule probability P(0) = cos^2(phi/2) from the statevector
     (deterministic; no measurement / no coin flip).
  2. The result of 10,000 simulator shots (adds the measurement, i.e. the
     weighted coin flip that collapses each shot to a classical 0 or 1).
  3. A chi-squared comparison of the sampled shot counts against the Born-rule
     expectation, as a sanity check that the sampling matches the theory.

Geometry -> phase:
    The path-length difference at screen angle theta gives a relative phase
        phi = (2*pi*d/lambda) * sin(theta) = 2*pi*m
    where m = d*sin(theta)/lambda is the (generally non-integer) fringe order.
    Integer m  -> bright fringe (P0 = 1).
    Half-integer m -> dark fringe (P0 = 0).

Requirements: pip install qiskit qiskit-aer numpy
Usage (run in WSL bash with the quantum conda env active):
    python ~/quantum/dse_one_point.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from braket.circuits import Circuit
from braket.devices import LocalSimulator


# ---------------------------------------------------------------------------
# 1. Lab geometry -> relative phase phi
# ---------------------------------------------------------------------------
wavelength = 650e-9          # red laser pointer, meters (650 nm)
d          = 3e-6            # slit separation, meters (3 micron)
theta_deg  = 3.0            # screen angle off the central axis, degrees
theta      = np.deg2rad(theta_deg)

m   = d * np.sin(theta) / wavelength   # fringe order (0=central bright peak)
phi = 2 * np.pi * m                    # relative phase fed to the P gate


# ---------------------------------------------------------------------------
# 2. Exact probability via the statevector (no measurement, no RNG)
#    The three gates are pure unitary matrix multiplies:
#       H  -> put |0> into the equal superposition |+>
#       P  -> imprint the screen-position phase phi on the |1> component
#       H  -> interfere the two paths back together
#    Reading .probabilities()[0] gives cos^2(phi/2) directly.
# ---------------------------------------------------------------------------
qc = QuantumCircuit(1)       # 1 qubit, 0 classical bits (none needed yet)
qc.h(0)
qc.p(phi, 0)
qc.h(0)

p0 = Statevector.from_instruction(qc).probabilities()[0]   # = cos^2(phi/2)
p1 = 1.0 - p0


# ---------------------------------------------------------------------------
# 3. 10,000 shots on the simulator (this is where the coin flip happens)
#    measure_all() auto-adds the classical register that records each outcome,
#    so we do not have to declare QuantumCircuit(1, 1) ourselves.
# ---------------------------------------------------------------------------
N = 10000
qc_meas = qc.copy()
qc_meas.measure_all()        # appends a measurement -> enables sampling

counts = AerSimulator().run(qc_meas, shots=N).result().get_counts()
n0 = counts.get('0', 0)      # number of |0> outcomes
n1 = counts.get('1', 0)      # number of |1> outcomes


# ---------------------------------------------------------------------------
# 4. Chi-squared: observed shot counts vs Born-rule expectation
#    Expected counts are N*p0 and N*p1. With two outcome bins and the totals
#    fixed, this is a 1-degree-of-freedom test; chi^2 near 1 means the
#    sampling is consistent with the theory (large values would flag a bug).
# ---------------------------------------------------------------------------
exp0, exp1 = N * p0, N * p1
chi2 = (n0 - exp0) ** 2 / exp0 + (n1 - exp1) ** 2 / exp1


# ---------------------------------------------------------------------------
# 5. Report
# ---------------------------------------------------------------------------
print("=== Qiskit (IBM SDK) ===")
print(f"theta      = {theta_deg} deg off center axis")
print(f"fringe m   = {m:.4f}   (0 = central bright, 0.5 = first dark)")
print(f"phi        = {phi:.4f} rad")
print(f"P(0)       = {p0:.4f}    P(1) = {p1:.4f}   [exact, statevector]")
print(f"shots      = {n0} x |0>,  {n1} x |1>   (N = {N})")
print(f"expected   = {exp0:.1f} x |0>,  {exp1:.1f} x |1>")
print(f"chi^2      = {chi2:.4f}   (1 dof; ~1 is a good fit)")


# ---------------------------------------------------------------------------
# 6. Same algorithm in Amazon Braket (AWS SDK), on the LOCAL simulator.
#
#    Runs entirely on this machine: no AWS account, no cloud device, no spend.
#
#    Gate note: Braket has no direct P(phi) gate. We use Rz(phi) instead.
#    Rz and P differ only by a global phase, which is unobservable and does not
#    affect measurement probabilities, so the H-Rz-H circuit yields the same
#    P(0) = cos^2(phi/2) as Qiskit's H-P-H. Braket has no explicit statevector
#    "probabilities" call here, so we add a .probability result type to read the
#    exact probabilities, plus a separate shots run for the sampled counts.
# ---------------------------------------------------------------------------
bk_device = LocalSimulator()

# Exact probabilities: shots=0 with a Probability result type (no coin flip).
bk_circ_prob = Circuit().h(0).rz(0, phi).h(0).probability()
bk_probs = bk_device.run(bk_circ_prob, shots=0).result().values[0]
bk_p0, bk_p1 = float(bk_probs[0]), float(bk_probs[1])

# Sampled shots: same circuit, add a measurement by running with shots > 0.
bk_circ_shots = Circuit().h(0).rz(0, phi).h(0)
bk_counts = bk_device.run(bk_circ_shots, shots=N).result().measurement_counts
bk_n0 = bk_counts.get('0', 0)
bk_n1 = bk_counts.get('1', 0)

bk_exp0, bk_exp1 = N * bk_p0, N * bk_p1
bk_chi2 = (bk_n0 - bk_exp0) ** 2 / bk_exp0 + (bk_n1 - bk_exp1) ** 2 / bk_exp1

print()
print("=== Amazon Braket (AWS SDK), local simulator ===")
print(f"gate       = Rz(phi) in place of P(phi) (differs only by global phase)")
print(f"P(0)       = {bk_p0:.4f}    P(1) = {bk_p1:.4f}   [exact]")
print(f"shots      = {bk_n0} x |0>,  {bk_n1} x |1>   (N = {N})")
print(f"expected   = {bk_exp0:.1f} x |0>,  {bk_exp1:.1f} x |1>")
print(f"chi^2      = {bk_chi2:.4f}   (1 dof; ~1 is a good fit)")


# ---------------------------------------------------------------------------
# 7. Cross-check: the two SDKs should agree on the exact probability.
# ---------------------------------------------------------------------------
print()
print("=== Cross-check ===")
print(f"Qiskit P(0) = {p0:.6f}")
print(f"Braket P(0) = {bk_p0:.6f}")
print(f"|difference| = {abs(p0 - bk_p0):.2e}")
print("MATCH" if abs(p0 - bk_p0) < 1e-9 else "MISMATCH - investigate")
