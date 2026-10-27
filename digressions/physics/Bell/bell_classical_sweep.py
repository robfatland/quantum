"""
Classical (hidden variable) CHSH sweep.

Simulates a local hidden variable model for two particles A and B, each carrying
a fixed polarization angle (the "hidden variable"). Measurements along randomly
chosen axes produce +1 or -1 based on Malus's law projection probability.

Default mode: sweep theta_A from 0-90 deg and theta_B from 0-180 deg independently.
--anti mode: theta_B = 180 - theta_A (anticorrelated, classical analog of singlet).
--corr mode: theta_B = theta_A (correlated, classical analog of triplet).

Measurement axes:
  A chooses randomly between a=0 deg and a'=45 deg
  B chooses randomly between b=22.5 deg and b'=67.5 deg

Usage:
  python bell_classical_sweep.py              # independent sweep
  python bell_classical_sweep.py --anti       # anticorrelated
  python bell_classical_sweep.py --corr       # correlated

Output:
  bell_classical_S.png        - 3D surface (independent)
  bell_classical_S_anti.png   - 1D curve (anticorrelated)
  bell_classical_S_corr.png   - 1D curve (correlated)
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def measure(hidden_angle_deg, detector_angle_deg):
    """
    Simulate a single measurement. The particle has a hidden polarization at
    hidden_angle_deg (colatitude on Bloch sphere). The detector measures along
    detector_angle_deg.

    Probability of +1 = cos^2((hidden - detector) / 2)  [Malus-like projection]
    Returns +1 or -1.
    """
    diff_rad = np.radians(hidden_angle_deg - detector_angle_deg)
    prob_plus = np.cos(diff_rad / 2) ** 2
    return +1 if np.random.random() < prob_plus else -1


def compute_E(theta_A, theta_B, axis_A, axis_B, n_trials):
    """
    Compute E(a,b) = average product of outcomes over n_trials.
    theta_A, theta_B: hidden polarization angles (degrees)
    axis_A, axis_B: measurement axis angles (degrees)
    """
    products = np.zeros(n_trials)
    for i in range(n_trials):
        a_result = measure(theta_A, axis_A)
        b_result = measure(theta_B, axis_B)
        products[i] = a_result * b_result
    return products.mean()


def compute_S(theta_A, theta_B, n_trials):
    """
    Compute S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    with a=0, a'=45, b=22.5, b'=67.5 degrees.
    """
    a, a_prime = 0.0, 45.0
    b, b_prime = 22.5, 67.5

    Eab = compute_E(theta_A, theta_B, a, b, n_trials)
    Eab_prime = compute_E(theta_A, theta_B, a, b_prime, n_trials)
    Ea_prime_b = compute_E(theta_A, theta_B, a_prime, b, n_trials)
    Ea_prime_b_prime = compute_E(theta_A, theta_B, a_prime, b_prime, n_trials)

    S = Eab - Eab_prime + Ea_prime_b + Ea_prime_b_prime
    return S


def main():
    parser = argparse.ArgumentParser(
        description='Classical CHSH sweep: hidden variable model')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--anti', action='store_true',
                       help='Anticorrelated mode: theta_B = 180 - theta_A')
    group.add_argument('--corr', action='store_true',
                       help='Correlated mode: theta_B = theta_A')
    parser.add_argument('--trials', type=int, default=10000,
                        help='Trials per (axis pair, angle pair) (default: 10000)')
    args = parser.parse_args()

    n_trials = args.trials

    if args.anti:
        # Anticorrelated: theta_B = 180 - theta_A
        theta_A_vals = np.arange(0, 181, 10)
        theta_B_vals = 180.0 - theta_A_vals
        print("Mode: ANTICORRELATED (theta_B = 180 - theta_A)")
        print(f"  theta_A: 0 to 180 step 10 ({len(theta_A_vals)} values)")
        print(f"  Trials per configuration: {n_trials}")
        print(f"  Measurement axes: a=0, a'=45, b=22.5, b'=67.5 deg")
        print()

        S_vals = np.zeros(len(theta_A_vals))
        for i, (tA, tB) in enumerate(zip(theta_A_vals, theta_B_vals)):
            S_vals[i] = compute_S(tA, tB, n_trials)
            print(f"  theta_A={tA:5.1f}, theta_B={tB:5.1f}: S = {S_vals[i]:+.4f}")

        max_idx = np.argmax(np.abs(S_vals))
        print(f"\n  MAX |S| = {abs(S_vals[max_idx]):.4f} at "
              f"theta_A={theta_A_vals[max_idx]:.1f}, "
              f"theta_B={theta_B_vals[max_idx]:.1f}")
        print(f"  Bell bound: |S| <= 2.0")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(theta_A_vals, np.abs(S_vals), 'bo-', linewidth=2, markersize=8)
        ax.axhline(2.0, color='red', linestyle='--', linewidth=2,
                   label='Bell bound (|S| = 2)')
        ax.set_xlabel(r'$\theta_A$ (degrees)', fontsize=12)
        ax.set_ylabel('|S|', fontsize=12)
        ax.set_title(r'Classical CHSH: anticorrelated ($\theta_B = 180 - \theta_A$)',
                     fontsize=13)
        ax.legend(fontsize=11)
        ax.set_ylim(0, 2.5)
        plt.tight_layout()
        plt.savefig('images/bell_classical_S_anti.png', dpi=150)
        print("\nSaved: images/bell_classical_S_anti.png")

    elif args.corr:
        # Correlated: theta_B = theta_A
        theta_A_vals = np.arange(0, 181, 10)
        theta_B_vals = theta_A_vals.copy()
        print("Mode: CORRELATED (theta_B = theta_A)")
        print(f"  theta_A: 0 to 180 step 10 ({len(theta_A_vals)} values)")
        print(f"  Trials per configuration: {n_trials}")
        print(f"  Measurement axes: a=0, a'=45, b=22.5, b'=67.5 deg")
        print()

        S_vals = np.zeros(len(theta_A_vals))
        for i, (tA, tB) in enumerate(zip(theta_A_vals, theta_B_vals)):
            S_vals[i] = compute_S(tA, tB, n_trials)
            print(f"  theta_A={tA:5.1f}, theta_B={tB:5.1f}: S = {S_vals[i]:+.4f}")

        max_idx = np.argmax(np.abs(S_vals))
        print(f"\n  MAX |S| = {abs(S_vals[max_idx]):.4f} at "
              f"theta_A={theta_A_vals[max_idx]:.1f}, "
              f"theta_B={theta_B_vals[max_idx]:.1f}")
        print(f"  Bell bound: |S| <= 2.0")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(theta_A_vals, np.abs(S_vals), 'go-', linewidth=2, markersize=8)
        ax.axhline(2.0, color='red', linestyle='--', linewidth=2,
                   label='Bell bound (|S| = 2)')
        ax.set_xlabel(r'$\theta_A$ (degrees)', fontsize=12)
        ax.set_ylabel('|S|', fontsize=12)
        ax.set_title(r'Classical CHSH: correlated ($\theta_B = \theta_A$)',
                     fontsize=13)
        ax.legend(fontsize=11)
        ax.set_ylim(0, 2.5)
        plt.tight_layout()
        plt.savefig('images/bell_classical_S_corr.png', dpi=150)
        print("\nSaved: images/bell_classical_S_corr.png")

    else:
        # Independent 2D sweep
        theta_A_vals = np.arange(0, 91, 10)
        theta_B_vals = np.arange(0, 181, 10)
        print("Mode: INDEPENDENT SWEEP")
        print(f"  theta_A: {theta_A_vals} ({len(theta_A_vals)} values)")
        print(f"  theta_B: {theta_B_vals} ({len(theta_B_vals)} values)")
        print(f"  Trials per configuration: {n_trials}")
        print(f"  Measurement axes: a=0, a'=45, b=22.5, b'=67.5 deg")
        print()

        S_grid = np.zeros((len(theta_A_vals), len(theta_B_vals)))
        total = len(theta_A_vals) * len(theta_B_vals)
        count = 0

        for i, tA in enumerate(theta_A_vals):
            for j, tB in enumerate(theta_B_vals):
                S_grid[i, j] = compute_S(tA, tB, n_trials)
                count += 1
                if count % 20 == 0 or count == total:
                    print(f"\r  Progress: {count}/{total}", end='', flush=True)

        print()

        max_idx = np.unravel_index(np.argmax(np.abs(S_grid)), S_grid.shape)
        max_S = S_grid[max_idx]
        print(f"\n  MAX |S| = {abs(max_S):.4f} at "
              f"theta_A={theta_A_vals[max_idx[0]]:.1f}, "
              f"theta_B={theta_B_vals[max_idx[1]]:.1f}")
        print(f"  Bell bound: |S| <= 2.0")

        B_mesh, A_mesh = np.meshgrid(theta_B_vals, theta_A_vals)
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(A_mesh, B_mesh, np.abs(S_grid),
                               cmap='viridis', alpha=0.85, edgecolor='none')

        ax.plot_surface(A_mesh, B_mesh,
                        2.0 * np.ones_like(S_grid),
                        alpha=0.2, color='red')

        ax.set_xlabel(r'$\theta_A$ (deg)', fontsize=11)
        ax.set_ylabel(r'$\theta_B$ (deg)', fontsize=11)
        ax.set_zlabel('|S|', fontsize=11)
        ax.set_title('Classical CHSH: |S| over hidden variable parameter space\n'
                     'Red plane = Bell bound (2.0)', fontsize=13)
        ax.set_zlim(0, 2.5)
        fig.colorbar(surf, shrink=0.6, label='|S|')
        plt.tight_layout()
        plt.savefig('images/bell_classical_S.png', dpi=150)
        print("Saved: images/bell_classical_S.png")


if __name__ == '__main__':
    main()
