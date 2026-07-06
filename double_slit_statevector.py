"""
Double-Slit Interference: Quantum circuit simulation using H-P-H approach.

A single qubit computes the interference probability at each screen position:
  H → P(φ) → H → Measure
where φ is the path-length difference at that position.

P(outcome=0) = cos²(φ/2) — the double-slit fringe intensity.

We sweep φ across screen positions, compute probabilities via Statevector,
then sample photon hits to build the histogram.

Usage:
  python double_slit.py                  # static histogram only
  python double_slit.py --animate        # + animated accumulation
  python double_slit.py --fringes 5      # 5 fringe periods
  python double_slit.py --screen-pts 256 # screen resolution
  python double_slit.py --photons 50000  # number of photon hits

Requirements: pip install qiskit numpy matplotlib pylatexenc

Output:
  double_slit_circuit.png    - the H-P-H circuit diagram
  double_slit_histogram.png  - final histogram with theory overlay
  double_slit_accumulate.mp4 - animated accumulation (if --animate)
"""

import matplotlib
matplotlib.use('Agg')

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


# ============================================================
# Circuit and probability computation
# ============================================================

def interference_probability(phi):
    """
    Compute P(0) for the H-P(φ)-H circuit.
    This equals cos²(φ/2) — the double-slit intensity.
    """
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.p(phi, 0)
    qc.h(0)
    state = Statevector.from_instruction(qc)
    return state.probabilities()[0]  # P(|0⟩) = cos²(φ/2)


def compute_fringe_pattern(screen_points, num_fringes, slit_ratio=3.0):
    """
    Compute the interference pattern across the screen.
    
    Args:
        screen_points: number of discrete screen positions
        num_fringes: number of fringe periods (controls slit separation)
        slit_ratio: d/w ratio (controls envelope width, ~2*ratio-1 peaks in central lobe)
    
    Returns:
        prob_dist: normalized probability distribution across screen
        phi_vals: phase values used
    """
    # Phase sweep: symmetric about 0 so that center of screen has φ=0 (maximum)
    phi_vals = np.linspace(-np.pi * num_fringes, np.pi * num_fringes, screen_points)
    
    # Compute quantum probability at each position
    intensity = np.array([interference_probability(phi) for phi in phi_vals])
    
    # Add sinc² envelope for finite slit width
    # The envelope has zeros at positions where x/screen_points = k/slit_ratio
    x_norm = np.linspace(-0.5, 0.5, screen_points)
    envelope = np.sinc(slit_ratio * x_norm) ** 2
    
    # Combined pattern
    pattern = intensity * envelope
    
    # Normalize to probability distribution
    prob_dist = pattern / pattern.sum()
    
    return prob_dist, phi_vals, intensity, envelope


def sample_photons(prob_dist, num_photons):
    """Sample photon hit positions from the probability distribution."""
    return np.random.choice(len(prob_dist), size=num_photons, p=prob_dist)


def save_circuit_diagram():
    """Save the H-P-H circuit diagram."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.p(np.pi / 2, 0)  # example phase
    qc.h(0)
    qc.measure(0, 0)
    
    try:
        fig = qc.draw('mpl', style={'name': 'iqp'})
        fig.savefig('double_slit_circuit.png', dpi=150, bbox_inches='tight')
        print("Saved: double_slit_circuit.png")
        plt.close(fig)
    except Exception as e:
        print(f"Circuit diagram: {e}")
        print(qc.draw('text'))


# ============================================================
# Static plot
# ============================================================

def save_static_plot(histogram, prob_dist, screen_points, num_photons, num_fringes):
    """Save histogram with theory overlay."""
    theory = prob_dist * num_photons
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    ax.bar(range(screen_points), histogram, color='red', edgecolor='none',
           alpha=0.85, width=1.0, label='Quantum simulation (photon hits)')
    ax.plot(range(screen_points), theory, 'b-', linewidth=1.5, alpha=0.8,
            label='Theory: $\\cos^2(\\phi/2) \\cdot \\mathrm{sinc}^2$')
    
    ax.set_xlabel('Screen position', fontsize=12)
    ax.set_ylabel('Counts', fontsize=12)
    ax.set_title(f'Double-Slit Interference (H-P-H circuit)\n'
                 f'{screen_points} positions, {num_photons:,} photons, '
                 f'{num_fringes} fringe periods', fontsize=13)
    ax.set_xlim(-0.5, screen_points - 0.5)
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('double_slit_histogram.png', dpi=150)
    print("Saved: double_slit_histogram.png")
    plt.close(fig)


# ============================================================
# Animation
# ============================================================

def save_animation(histogram, prob_dist, screen_points, num_photons, num_fringes):
    """Pushbroom accumulation animation."""
    # Expand to shot list
    shot_list = []
    for i in range(screen_points):
        shot_list.extend([i] * int(histogram[i]))
    np.random.shuffle(shot_list)

    theory = prob_dist * num_photons
    
    fps = 20
    acc_frames = fps * 9
    hold_frames = fps * 3
    total_frames = acc_frames + hold_frames
    spf = max(1, len(shot_list) // acc_frames)

    # Precompute
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
        counter.set_text(f'Photons: {int(h.sum()):,} / {num_photons:,}')
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
    parser = argparse.ArgumentParser(description='Double-slit quantum simulation (H-P-H)')
    parser.add_argument('--animate', action='store_true',
                        help='Generate accumulation animation')
    parser.add_argument('--screen-pts', type=int, default=300,
                        help='Number of screen positions (default: 300)')
    parser.add_argument('--fringes', type=int, default=5,
                        help='Number of fringe periods (default: 5)')
    parser.add_argument('--photons', type=int, default=50000,
                        help='Number of simulated photon hits (default: 50000)')
    parser.add_argument('--slit-ratio', type=float, default=3.0,
                        help='d/w ratio for sinc envelope (default: 3.0, gives ~5 peaks)')
    args = parser.parse_args()

    screen_pts = args.screen_pts
    num_fringes = args.fringes
    num_photons = args.photons
    slit_ratio = args.slit_ratio

    print(f"Screen: {screen_pts} positions")
    print(f"Fringes: {num_fringes} periods")
    print(f"Envelope: sinc^2 with d/w = {slit_ratio} (~{int(2*slit_ratio - 1)} peaks in central lobe)")
    print(f"Photons: {num_photons:,}")

    # Save circuit diagram
    save_circuit_diagram()

    # Compute interference pattern
    print("Computing interference pattern (H-P-H at each screen position)...")
    prob_dist, phi_vals, raw_intensity, envelope = compute_fringe_pattern(
        screen_pts, num_fringes, slit_ratio)
    
    print(f"  Max probability: {prob_dist.max():.6f}")
    print(f"  Min probability: {prob_dist.min():.6f}")
    print(f"  Contrast ratio: {prob_dist.max() / max(prob_dist.min(), 1e-10):.1f}")

    # Sample photon hits
    print("Sampling photon hits...")
    hits = sample_photons(prob_dist, num_photons)
    
    # Build histogram
    histogram = np.zeros(screen_pts)
    for h in hits:
        histogram[h] += 1

    print(f"  Max bin: {histogram.max():.0f}, Min bin: {histogram.min():.0f}")

    # Static plot
    save_static_plot(histogram, prob_dist, screen_pts, num_photons, num_fringes)

    # Animation
    if args.animate:
        save_animation(histogram, prob_dist, screen_pts, num_photons, num_fringes)
