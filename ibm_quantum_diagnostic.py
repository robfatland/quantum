"""
IBM Quantum account and backend diagnostic.

Usage:
  python ibm_quantum_diagnostic.py

Reports:
  - Whether saved credentials are found
  - Account plan and instance
  - All available backends with status, qubit count, and queue depth
"""

from qiskit_ibm_runtime import QiskitRuntimeService

print("=" * 60)
print("IBM Quantum Diagnostic")
print("=" * 60)

# Connect
print("\n[1] Connecting to IBM Quantum...")
try:
    service = QiskitRuntimeService()
    print("    Connected successfully.")
except Exception as e:
    print(f"    FAILED: {e}")
    raise SystemExit(1)

# Account info
print("\n[2] Account info:")
try:
    channel = service.channel
    print(f"    Channel: {channel}")
except AttributeError:
    print("    (channel attribute not available in this version)")

# List backends
print("\n[3] Available backends:")
print(f"    {'Name':<20} {'Qubits':>6} {'Operational':>12} {'Status Msg':<15} {'Pending':>8}")
print("    " + "-" * 65)

backends = service.backends()
if not backends:
    print("    NO BACKENDS FOUND. Check your plan and credentials.")
else:
    active_count = 0
    for b in backends:
        s = b.status()
        is_sim = b.configuration().simulator
        tag = " (sim)" if is_sim else ""
        status_msg = getattr(s, 'status_msg', 'unknown')
        pending = s.pending_jobs
        operational = s.operational
        if operational and status_msg == 'active' and not is_sim:
            active_count += 1
            marker = " <-- AVAILABLE"
        elif not operational or status_msg != 'active':
            marker = ""
        else:
            marker = ""
        print(f"    {b.name + tag:<20} {b.num_qubits:>6} {str(operational):>12} "
              f"{status_msg:<15} {pending:>8}{marker}")

    print(f"\n    Total backends: {len(backends)}")
    print(f"    Active real backends: {active_count}")
    if active_count == 0:
        print("\n    *** No active backends right now. All are in maintenance. ***")
        print("    *** Check: https://quantum.ibm.com/services/resources ***")
    else:
        print(f"\n    Ready to run: python double_slit.py --backend ibm")

print("\n" + "=" * 60)
