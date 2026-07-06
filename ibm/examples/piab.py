"""
1D Particle in a Box — Hamiltonian simulation via Trotterization.

3 qubits = 8 lattice sites. Nearest-neighbor hopping Hamiltonian.
The particle is initialized at a specific site and time-evolved,
demonstrating quantum diffusion within the box.

Optional: add a potential barrier to observe tunneling.

Usage:
    python piab.py
    python piab.py --barrier     (adds a potential barrier for tunneling)
"""

import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter

# --- Parameters ---
n_qubits = 3
n_sites = 2**n_qubits  # 8 lattice sites
J = 1.0                 # hopping strength
dt = 0.3                # time step per Trotter step
n_trotter_steps = 5     # number of Trotter steps
initial_site = 3        # particle starts here
shots = 4096
use_barrier = "--barrier" in sys.argv

# --- Build the Hamiltonian ---
H_matrix = np.zeros((n_sites, n_sites))

# Nearest-neighbor hopping (kinetic energy)
for j in range(n_sites - 1):
    H_matrix[j, j + 1] = -J
    H_matrix[j + 1, j] = -J

# Optional: potential barrier for tunneling demo
if use_barrier:
    V_barrier = 3.0
    H_matrix[4, 4] = V_barrier
    H_matrix[5, 5] = V_barrier
    print(f"Barrier: V = {V_barrier} at sites 4 and 5")
else:
    print("No barrier (free particle in a box)")

# Convert to Pauli operator representation
hamiltonian = SparsePauliOp.from_operator(H_matrix)

# --- Build the circuit ---

# Time evolution gate via second-order Suzuki-Trotter decomposition
total_time = dt * n_trotter_steps
evolution_gate = PauliEvolutionGate(
    hamiltonian,
    time=total_time,
    synthesis=SuzukiTrotter(order=2, reps=n_trotter_steps)
)

# Initialize particle at the chosen site (encode site number in binary)
qc = QuantumCircuit(n_qubits)
binary_string = format(initial_site, f'0{n_qubits}b')
for i, bit in enumerate(reversed(binary_string)):
    if bit == '1':
        qc.x(i)

# Apply time evolution
qc.append(evolution_gate, range(n_qubits))

# Measure all qubits
qc.measure_all()

# --- Run the simulation ---
sim = AerSimulator()
result = sim.run(qc, shots=shots).result()
counts = result.get_counts()

# --- Display results ---
print(f"\nParticle in a 1D box ({n_sites} sites, {n_qubits} qubits)")
print(f"Initial site: {initial_site}")
print(f"Total evolution time: {total_time:.2f} (J={J}, dt={dt}, steps={n_trotter_steps})")
print(f"Shots: {shots}")
print(f"\nProbability distribution over lattice sites:\n")

for site in range(n_sites):
    bitstring = format(site, f'0{n_qubits}b')
    count = counts.get(bitstring, 0)
    prob = count / shots
    bar = '█' * int(prob * 50)
    marker = " <-- start" if site == initial_site else ""
    print(f"  Site {site} |{bitstring}>: {prob:.3f} {bar}{marker}")

print(f"\nTotal probability: {sum(counts.values()) / shots:.3f}")
