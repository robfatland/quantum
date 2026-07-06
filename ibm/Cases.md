# Cases

A sequence of Python programs.

## bell_state.py

`QuantumCircuit(2)` creates a quantum circuit with 2 qubits, both initialized 
to |0>. No gates applied yet. Also creates two classical bits to hold measurement outcomes. (See subsequent `measure_all()`). `qc` is now a mutable container 
where subsequent lines of code build up the circuit to execute. 


`qc.h(0)` applies the Hadamard gate to qubit 0 producing a two-element column vector 
$(1 / \sqrt(2), 1 / \sqrt(2))^{T}$: A superposition of the two basis states. 