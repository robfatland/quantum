"""
Quantum CHSH experiment: demonstrates S = 2*sqrt(2) > 2 using Qiskit.

Prepares the Bell state |Phi+> = (|00> + |11>)/sqrt(2), then measures
correlations across four angle combinations to compute S.

This should yield S ≈ 2.83 on a perfect simulator, clearly violating
the classical (hidden variable) bound of |S| <= 2.

Usage: python bell_quantum_chsh.py
       python bell_quantum_chsh.py --shots 100000
       python bell_quantum_chsh.py --backend ibm   (real hardware)
"""

import matplotlib
matplotlib.use('Agg')

import argparse
import numpy as np
from qiskit import QuantumCircuit, transpile


def build_chsh_circuit(theta_a, theta_b):
    """
    Build a CHSH circuit:
    1. Prepare Bell state (H on q0, CNOT)
    2. Rotate q0 by theta_a about Y (measurement basis for A)
    3. Rotate q1 by theta_b about Y (measurement basis for B)
    4. Measure both in Z-basis
    """
    qc = QuantumCircuit(2, 2)
    # Bell state preparation
    qc.h(0)
    qc.cx(0, 1)
    # Rotate measurement bases
    qc.ry(-2 * theta_a, 0)  # negative because we rotate the basis, not the state
    qc.ry(-2 * theta_b, 1)
    # Measure
    qc.measure([0, 1], [0, 1])
    return qc


def compute_E_from_counts(counts, shots):
    """
    Compute E(a,b) = <A*B> from measurement counts.
    Outcome '00' or '11' -> A*B = +1 (same)
    Outcome '01' or '10' -> A*B = -1 (different)
    """
    same = counts.get('00', 0) + counts.get('11', 0)
    diff = counts.get('01', 0) + counts.get('10', 0)
    return (same - diff) / shots


def run_chsh(shots=10000, backend_name='local'):
    """Run the full CHSH experiment and return S."""
    # CHSH optimal angles (radians)
    a = 0.0
    a_prime = np.pi / 4        # 45 degrees
    b = np.pi / 8              # 22.5 degrees
    b_prime = 3 * np.pi / 8    # 67.5 degrees

    angle_pairs = [
        ('a,b', a, b),
        ('a,b\'', a, b_prime),
        ('a\',b', a_prime, b),
        ('a\',b\'', a_prime, b_prime),
    ]

    # Build circuits
    circuits = []
    labels = []
    for label, theta_a, theta_b in angle_pairs:
        qc = build_chsh_circuit(theta_a, theta_b)
        circuits.append(qc)
        labels.append(label)

    # Execute
    if backend_name == 'local':
        from qiskit_aer import AerSimulator
        backend = AerSimulator()
        transpiled = transpile(circuits, backend)
        job = backend.run(transpiled, shots=shots)
        results = job.result()
    elif backend_name == 'ibm':
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
        service = QiskitRuntimeService()
        backends = service.backends()
        real_backends = [b for b in backends if b.status().operational
                         and not b.configuration().simulator]
        if real_backends:
            hw_backend = min(real_backends, key=lambda b: b.status().pending_jobs)
        else:
            hw_backend = backends[0]
        print(f"  Backend: {hw_backend.name}")
        transpiled = transpile(circuits, hw_backend)
        sampler = SamplerV2(hw_backend)
        job = sampler.run(transpiled, shots=shots)
        print(f"  Job ID: {job.job_id()}")
        result = job.result()
        # Convert SamplerV2 results to counts
        counts_list = []
        for i in range(len(circuits)):
            pub_result = result[i]
            bitarray = pub_result.data.c
            counts_list.append(bitarray.get_counts())
        # Package for uniform handling below
        class FakeResults:
            def get_counts(self, idx):
                return counts_list[idx]
        results = FakeResults()
    else:
        raise ValueError(f"Unknown backend: {backend_name}")

    # Compute correlators
    E_values = {}
    print(f"\n  {'Pair':<8} {'E':>8}")
    print(f"  {'-'*8} {'-'*8}")
    for i, (label, theta_a, theta_b) in enumerate(angle_pairs):
        counts = results.get_counts(i)
        E = compute_E_from_counts(counts, shots)
        E_values[label] = E
        print(f"  {label:<8} {E:+.4f}")

    # Compute S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    Eab = E_values['a,b']
    Eab_p = E_values["a,b'"]
    Ea_pb = E_values["a',b"]
    Ea_pb_p = E_values["a',b'"]
    S = Eab - Eab_p + Ea_pb + Ea_pb_p

    print(f"\n  S = E(a,b) - E(a,b') + E(a',b) + E(a',b')")
    print(f"  S = {Eab:+.4f} - ({Eab_p:+.4f}) + {Ea_pb:+.4f} + {Ea_pb_p:+.4f}")
    print(f"  S = {S:+.4f}")
    print(f"\n  |S| = {abs(S):.4f}")
    print(f"  Classical bound:  |S| <= 2.000")
    print(f"  QM prediction:    |S| = 2*sqrt(2) = {2*np.sqrt(2):.4f}")
    print(f"  Violation: {'YES' if abs(S) > 2.0 else 'NO'}")

    return S


def main():
    parser = argparse.ArgumentParser(description='Quantum CHSH experiment')
    parser.add_argument('--shots', type=int, default=10000,
                        help='Shots per angle pair (default: 10000)')
    parser.add_argument('--backend', choices=['local', 'ibm'], default='local',
                        help='Execution backend (default: local simulator)')
    args = parser.parse_args()

    print("="*60)
    print("  QUANTUM CHSH EXPERIMENT")
    print("="*60)
    print(f"  Shots per measurement: {args.shots}")
    print(f"  Backend: {args.backend}")
    print(f"  Angles: a=0, a'=45, b=22.5, b'=67.5 deg")
    print(f"  State: Bell |Phi+> = (|00> + |11>)/sqrt(2)")

    S = run_chsh(shots=args.shots, backend_name=args.backend)

    # Save a simple bar chart
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Classical\nbound', '|S| measured', 'QM\nprediction'],
           [2.0, abs(S), 2*np.sqrt(2)],
           color=['gray', 'firebrick', 'steelblue'],
           edgecolor='black', linewidth=1.2)
    ax.axhline(2.0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.set_ylabel('|S|', fontsize=12)
    ax.set_title(f'CHSH Bell Test ({args.backend}, {args.shots} shots)\n'
                 f'|S| = {abs(S):.4f}', fontsize=13)
    ax.set_ylim(0, 3.2)
    plt.tight_layout()
    outfile = f'bell_quantum_S_{args.backend}.png'
    plt.savefig(outfile, dpi=150)
    print(f"\n  Saved: {outfile}")


if __name__ == '__main__':
    main()
