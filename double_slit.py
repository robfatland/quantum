"""
Double-Slit Interference: Shot-based quantum circuit simulation.

Identical code runs on:
  1. Local AerSimulator (for testing)
  2. IBM Quantum hardware (for real execution)

The circuit: H-P(phi)-H-Measure on a single qubit, repeated for each
screen position with a different phase phi. Each run uses shots (not
statevector) so the output is genuine measurement statistics.

Usage:
  python double_slit.py                       # local simulator
  python double_slit.py --backend ibm         # IBM hardware (requires API key)
  python double_slit.py --animate             # + animated accumulation
  python double_slit.py --fringes 8           # fringe periods
  python double_slit.py --screen-pts 200      # screen resolution
  python double_slit.py --shots-per-pos 1000  # shots at each position

Requirements:
  Local:  pip install qiskit qiskit-aer numpy matplotlib pylatexenc
  IBM:    pip install qiskit-ibm-runtime (+ IBM API key configured)

Output:
  double_slit_circuit.png    - the H-P-H circuit diagram
  double_slit_histogram.png  - final histogram with theory overlay
  double_slit_accumulate.mp4 - animated accumulation (if --animate)
  double_slit_results.json   - raw results for reveal-o-tron playback
"""

import matplotlib
matplotlib.use('Agg')

import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from qiskit import QuantumCircuit, transpile


# ============================================================
# Circuit construction
# ============================================================

def build_circuits(screen_points, num_fringes):
    """
    Build one H-P(phi)-H-M circuit per screen position.
    
    Args:
        screen_points: number of screen positions
        num_fringes: number of fringe periods across the screen
    
    Returns:
        circuits: list of QuantumCircuits (one per screen position)
        phi_vals: array of phase values used
    """
    phi_vals = np.linspace(-np.pi * num_fringes, np.pi * num_fringes, screen_points)
    
    circuits = []
    for phi in phi_vals:
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.p(phi, 0)
        qc.h(0)
        qc.measure(0, 0)
        circuits.append(qc)
    
    return circuits, phi_vals


def save_circuit_diagram(num_fringes):
    """Save an example circuit diagram (with phi = pi/3 as illustration)."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.p(np.pi / 3, 0)  # illustrative phase
    qc.h(0)
    qc.measure(0, 0)
    
    try:
        fig = qc.draw('mpl')
        fig.savefig('double_slit_circuit.png', dpi=150, bbox_inches='tight')
        print("Saved: double_slit_circuit.png")
        plt.close(fig)
    except Exception as e:
        print(f"Circuit diagram: {e}")
        print(qc.draw('text'))


# ============================================================
# Execution backends
# ============================================================

def run_local(circuits, shots_per_pos):
    """Run on local AerSimulator."""
    from qiskit_aer import AerSimulator
    
    sim = AerSimulator()
    # Transpile all circuits (trivial for 1-qubit, but good practice)
    transpiled = transpile(circuits, sim)
    
    # Run all circuits in one job
    print(f"  Running {len(circuits)} circuits x {shots_per_pos} shots on AerSimulator...")
    job = sim.run(transpiled, shots=shots_per_pos)
    results = job.result()
    
    # Extract P(0) for each circuit
    counts_list = []
    for i in range(len(circuits)):
        counts = results.get_counts(i)
        counts_list.append(counts)
    
    return counts_list


def run_ibm(circuits, shots_per_pos):
    """Run on IBM Quantum hardware via Qiskit Runtime."""
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    except ImportError:
        print("ERROR: qiskit-ibm-runtime not installed.")
        print("  pip install qiskit-ibm-runtime")
        raise SystemExit(1)
    
    # Connect to IBM (assumes credentials are saved)
    print("  Connecting to IBM Quantum...")
    service = QiskitRuntimeService()
    
    # List available backends and pick the least busy
    print("  Discovering available backends...")
    backends = service.backends()
    if not backends:
        print("ERROR: No backends available on your plan.")
        raise SystemExit(1)
    
    # Filter to operational, non-simulator backends; fall back to any available
    real_backends = [b for b in backends if b.status().operational
                     and b.status().status_msg == 'active'
                     and not b.configuration().simulator]
    if real_backends:
        # Pick the one with shortest queue
        backend = min(real_backends, key=lambda b: b.status().pending_jobs)
    else:
        # Fall back to whatever is available (may be simulator)
        backend = backends[0]
    
    print(f"  Backend: {backend.name} ({backend.num_qubits} qubits, "
          f"{backend.status().pending_jobs} pending jobs)")
    
    # Transpile for the target hardware
    transpiled = transpile(circuits, backend)
    
    # Run via Sampler primitive
    print(f"  Submitting {len(circuits)} circuits x {shots_per_pos} shots...")
    sampler = SamplerV2(backend)
    job = sampler.run(transpiled, shots=shots_per_pos)
    print(f"  Job ID: {job.job_id()}")
    print("  Waiting for results...")
    result = job.result()
    
    # Extract counts from SamplerV2 result
    counts_list = []
    for i in range(len(circuits)):
        # SamplerV2 returns BitArray; convert to counts dict
        pub_result = result[i]
        bitarray = pub_result.data.c
        counts = bitarray.get_counts()
        counts_list.append(counts)
    
    return counts_list


# ============================================================
# Analysis
# ============================================================

def counts_to_histogram(counts_list, screen_points):
    """Convert per-position counts to a screen histogram."""
    histogram = np.zeros(screen_points)
    total_shots = 0
    
    for i, counts in enumerate(counts_list):
        # Count how many times outcome '0' occurred at this position
        n_zero = counts.get('0', 0)
        histogram[i] = n_zero
        total_shots += sum(counts.values())
    
    return histogram, total_shots


def apply_envelope(histogram, screen_points, slit_ratio):
    """Apply sinc^2 envelope (post hoc, simulating finite slit width)."""
    x_norm = np.linspace(-0.5, 0.5, screen_points)
    envelope = np.sinc(slit_ratio * x_norm) ** 2
    return histogram * envelope


def theoretical_pattern(screen_points, num_fringes, slit_ratio, shots_per_pos):
    """Theoretical: cos^2(phi/2) * sinc^2 envelope, scaled to expected counts."""
    phi_vals = np.linspace(-np.pi * num_fringes, np.pi * num_fringes, screen_points)
    intensity = np.cos(phi_vals / 2) ** 2
    x_norm = np.linspace(-0.5, 0.5, screen_points)
    envelope = np.sinc(slit_ratio * x_norm) ** 2
    theory = intensity * envelope * shots_per_pos
    return theory


# ============================================================
# Static plot
# ============================================================

def save_static_plot(histogram, theory, screen_points, shots_per_pos, num_fringes,
                     slit_ratio, backend_name):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(range(screen_points), histogram, color='red', edgecolor='none',
           alpha=0.85, width=1.0, label=f'Quantum ({backend_name})')
    ax.plot(range(screen_points), theory, 'b-', linewidth=1.5, alpha=0.8,
            label='Theory: $\\cos^2(\\phi/2) \\cdot \\mathrm{sinc}^2$')
    ax.set_xlabel('Screen position', fontsize=12)
    ax.set_ylabel('Counts (outcome = 0)', fontsize=12)
    ax.set_title(f'Double-Slit Interference (H-P-H-M, {backend_name})\n'
                 f'{screen_points} positions, {shots_per_pos} shots/pos, '
                 f'{num_fringes} fringes, d/w={slit_ratio}', fontsize=13)
    ax.set_xlim(-0.5, screen_points - 0.5)
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('double_slit_histogram.png', dpi=150)
    print("Saved: double_slit_histogram.png")
    plt.close(fig)


# ============================================================
# Animation
# ============================================================

def save_animation(histogram, theory, screen_points, shots_per_pos, num_fringes):
    """Pushbroom accumulation animation using per-position shot data."""
    total_counts = int(histogram.sum())
    
    # Create shot list from histogram
    shot_list = []
    for i in range(screen_points):
        shot_list.extend([i] * int(histogram[i]))
    np.random.shuffle(shot_list)

    fps = 20
    acc_frames = fps * 9
    hold_frames = fps * 3
    total_frames = acc_frames + hold_frames
    spf = max(1, len(shot_list) // acc_frames)

    cumulative = []
    running = np.zeros(screen_points)
    for f in range(acc_frames):
        s, e = f * spf, min((f + 1) * spf, len(shot_list))
        for idx in shot_list[s:e]:
            running[idx] += 1
        cumulative.append(running.copy())

    final = cumulative[-1]
    y_max = max(final.max(), theory.max()) * 1.1

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(range(screen_points), np.zeros(screen_points), color='red',
                  edgecolor='none', width=1.0, alpha=0.9)
    ax.plot(range(screen_points), theory, 'b-', linewidth=1.2, alpha=0.7,
            label='Theory')
    ax.set_xlim(-0.5, screen_points - 0.5)
    ax.set_ylim(0, y_max)
    ax.set_xlabel('Screen position', fontsize=12)
    ax.set_ylabel('Counts', fontsize=12)
    ax.legend(fontsize=11, loc='upper right')
    title = ax.set_title('', fontsize=13)
    counter = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=11,
                      va='top', fontfamily='monospace')

    def update(frame):
        h = cumulative[min(frame, acc_frames - 1)]
        for bar, val in zip(bars, h):
            bar.set_height(val)
        title.set_text(f'Double-Slit Interference — {screen_points} positions, '
                       f'{num_fringes} fringes')
        counter.set_text(f'Photons: {int(h.sum()):,} / {total_counts:,}')
        return list(bars) + [title, counter]

    def progress(cur, tot):
        print(f'\r  [{"#" * int(40*(cur+1)/tot)}{"-" * (40-int(40*(cur+1)/tot))}] '
              f'{100*(cur+1)/tot:.0f}%', end='', flush=True)

    print(f"\nRendering animation ({total_frames} frames)...")
    anim = FuncAnimation(fig, update, frames=total_frames, interval=1000 // fps,
                         blit=False, repeat=False)
    try:
        anim.save('double_slit_accumulate.mp4', writer=FFMpegWriter(fps=fps),
                  progress_callback=progress)
        print("\n\nSaved: double_slit_accumulate.mp4")
    except Exception as e:
        print(f"\n\nmp4 failed ({e}), trying gif...")
        try:
            anim.save('double_slit_accumulate.gif', writer=PillowWriter(fps=fps),
                      progress_callback=progress)
            print("\n\nSaved: double_slit_accumulate.gif")
        except Exception as e2:
            print(f"\n\ngif failed ({e2})")
    plt.close(fig)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Double-slit (H-P-H shots)')
    parser.add_argument('--backend', choices=['local', 'ibm'], default='local',
                        help='Execution backend (default: local simulator)')
    parser.add_argument('--animate', action='store_true',
                        help='Generate accumulation animation')
    parser.add_argument('--screen-pts', type=int, default=200,
                        help='Screen positions (default: 200)')
    parser.add_argument('--fringes', type=int, default=8,
                        help='Fringe periods (default: 8)')
    parser.add_argument('--shots-per-pos', type=int, default=1000,
                        help='Shots per screen position (default: 1000)')
    parser.add_argument('--slit-ratio', type=float, default=3.0,
                        help='d/w for sinc envelope (default: 3.0)')
    args = parser.parse_args()

    screen_pts = args.screen_pts
    num_fringes = args.fringes
    shots_per_pos = args.shots_per_pos
    slit_ratio = args.slit_ratio
    backend_name = 'AerSimulator' if args.backend == 'local' else 'IBM Hardware'

    print(f"Double-Slit Experiment (H-P-H-M)")
    print(f"  Backend: {backend_name}")
    print(f"  Screen: {screen_pts} positions")
    print(f"  Fringes: {num_fringes} periods")
    print(f"  Shots/position: {shots_per_pos}")
    print(f"  Total shots: {screen_pts * shots_per_pos:,}")
    print(f"  Envelope: sinc^2 (d/w = {slit_ratio})")
    print()

    # Save circuit diagram
    save_circuit_diagram(num_fringes)

    # Build circuits
    print("Building circuits...")
    circuits, phi_vals = build_circuits(screen_pts, num_fringes)
    print(f"  {len(circuits)} circuits built")

    # Execute
    print("Executing...")
    if args.backend == 'local':
        counts_list = run_local(circuits, shots_per_pos)
    else:
        counts_list = run_ibm(circuits, shots_per_pos)

    # Build histogram (count of outcome=0 at each position)
    histogram_raw, total_shots = counts_to_histogram(counts_list, screen_pts)
    print(f"  Total shots executed: {total_shots:,}")

    # Apply envelope
    histogram = apply_envelope(histogram_raw, screen_pts, slit_ratio)

    # Theory
    theory = theoretical_pattern(screen_pts, num_fringes, slit_ratio, shots_per_pos)

    # Diagnostics
    print(f"  Histogram max: {histogram.max():.0f}, min: {histogram.min():.0f}")

    # Save results for later playback
    results_data = {
        'screen_pts': screen_pts,
        'num_fringes': num_fringes,
        'shots_per_pos': shots_per_pos,
        'slit_ratio': slit_ratio,
        'backend': backend_name,
        'phi_vals': phi_vals.tolist(),
        'histogram_raw': histogram_raw.tolist(),
        'histogram_enveloped': histogram.tolist(),
    }
    with open('double_slit_results.json', 'w') as f:
        json.dump(results_data, f, indent=2)
    print("Saved: double_slit_results.json")

    # Plot
    save_static_plot(histogram, theory, screen_pts, shots_per_pos, num_fringes,
                     slit_ratio, backend_name)

    # Animation
    if args.animate:
        save_animation(histogram, theory, screen_pts, shots_per_pos, num_fringes)
