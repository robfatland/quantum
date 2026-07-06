"""Bell state circuit — demonstrates entanglement on a local simulator."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Build a Bell state circuit: H on qubit 0, then CNOT(0,1)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run on the local Aer simulator
sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
counts = result.get_counts()

print("Bell state measurement counts:")
print(counts)
# Expected: roughly equal counts of '00' and '11', very few '01' or '10'
