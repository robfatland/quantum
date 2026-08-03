"""
Plot per-bin chi-squared contributions, overlaying multiple runs per backend.

Discovers all dse_results_{backend}_run{N}.json files in the current directory
and groups them by backend. Each backend gets its own subplot. Multiple runs
for the same backend are overlaid with transparency to show which bins spike
consistently vs. randomly.

Also supports the legacy single-run files (double_slit_results_local.json, etc.)

Usage: python chi2_per_bin_plot.py
Output: chi2_per_bin.png
"""

import json
import glob
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def chi2_per_bin(histogram, phi_vals, shots_per_pos):
    """Compute per-bin chi-squared contributions."""
    h = np.array(histogram, dtype=float)
    phi = np.array(phi_vals)
    p = np.cos(phi / 2) ** 2
    expected = shots_per_pos * p
    variance = shots_per_pos * p * (1 - p)
    variance = np.maximum(variance, 1.0)
    return (h - expected) ** 2 / variance


def discover_result_files():
    """Find all result JSON files, grouped by backend."""
    backends = {}

    # New naming: dse_results_{backend}_run{N}.json
    for f in sorted(glob.glob('dse_results_*_run*.json')):
        basename = os.path.basename(f)
        # Parse: dse_results_{backend}_run{N}.json
        parts = basename.replace('dse_results_', '').replace('.json', '')
        # e.g. "ibm_run2" or "local_run1"
        idx = parts.rfind('_run')
        if idx == -1:
            continue
        backend = parts[:idx]
        run_num = parts[idx+4:]
        backends.setdefault(backend, []).append(f)

    # Legacy naming: double_slit_results_{backend}.json
    for f in sorted(glob.glob('double_slit_results_*.json')):
        basename = os.path.basename(f)
        backend = basename.replace('double_slit_results_', '').replace('.json', '')
        backends.setdefault(backend + '_legacy', []).append(f)

    return backends


def main():
    backends = discover_result_files()

    if not backends:
        print("No result files found.")
        print("  Run: python double_slit.py --runs 4")
        print("  Or:  python double_slit.py --backend ibm --runs 4")
        return

    # Assign colors per backend
    color_map = {
        'local': 'steelblue',
        'ibm': 'firebrick',
        'aws': 'darkorange',
        'azure': 'darkgreen',
        'gcp': 'purple',
        'local_legacy': 'steelblue',
        'ibm_legacy': 'firebrick',
    }

    n_backends = len(backends)
    fig, axes = plt.subplots(n_backends, 1, figsize=(14, 4 * n_backends),
                             sharex=True, squeeze=False)

    for ax_idx, (backend, files) in enumerate(sorted(backends.items())):
        ax = axes[ax_idx, 0]
        color = color_map.get(backend, 'gray')
        n_runs = len(files)

        all_chi2 = []
        for i, f in enumerate(files):
            data = load_results(f)
            hist = data['histogram_raw']
            phi_vals = data['phi_vals']
            shots = data['shots_per_pos']
            chi2_bins = chi2_per_bin(hist, phi_vals, shots)
            all_chi2.append(chi2_bins)

            x = np.arange(len(chi2_bins))
            ax.bar(x, chi2_bins, width=0.8, alpha=0.3, color=color,
                   edgecolor='none')

        # Overlay the mean as a solid line
        if len(all_chi2) > 1:
            mean_chi2 = np.mean(all_chi2, axis=0)
            ax.plot(x, mean_chi2, color=color, linewidth=1.5, alpha=0.9,
                    label=f'Mean of {n_runs} runs')

        # Summary stats
        all_chi2_arr = np.array(all_chi2)
        totals = all_chi2_arr.sum(axis=1)
        total_str = ', '.join(f'{t:.0f}' for t in totals)

        # Overlay sinc^2 envelope (scaled to max chi2 for visibility)
        data0 = load_results(files[0])
        slit_ratio = data0.get('slit_ratio', 3.0)
        phi_vals_plot = np.array(data0['phi_vals'])
        n_pts = len(all_chi2[0])
        x_norm = np.linspace(-0.5, 0.5, n_pts)
        sinc_env = np.sinc(slit_ratio * x_norm) ** 2
        # Full theory: cos^2(phi/2) * sinc^2
        cos2_fringes = np.cos(phi_vals_plot / 2) ** 2
        full_theory = cos2_fringes * sinc_env
        y_max = np.max(np.abs(all_chi2_arr))
        ax.plot(x, sinc_env * y_max * 0.8, 'k:', linewidth=1.5, alpha=0.5,
                label=r'sinc$^2$ envelope (scaled)')
        ax.plot(x, full_theory * y_max * 0.8, 'b:', linewidth=1.2, alpha=0.5,
                label=r'$\cos^2(\phi/2) \cdot$ sinc$^2$ (scaled)')

        ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        ax.set_ylabel(r'$(O_i - E_i)^2 / \sigma_i^2$', fontsize=11)
        ax.set_title(f'{backend}  |  {n_runs} run(s)  |  '
                     r'$\chi^2$ totals: ' + total_str, fontsize=12)
        ax.legend(fontsize=10, loc='upper right')
        ax.set_xlim(-1, len(chi2_bins))

    axes[-1, 0].set_xlabel('Screen position index $i$', fontsize=12)

    plt.suptitle(r'Per-bin $\chi^2$ contributions by backend (overlaid runs)',
                 fontsize=14, y=0.995)
    plt.tight_layout()
    plt.savefig('chi2_per_bin.png', dpi=150)
    print(f"Saved: chi2_per_bin.png")

    # Print summary
    print("\nSummary:")
    for backend, files in sorted(backends.items()):
        for f in files:
            data = load_results(f)
            chi2_bins = chi2_per_bin(data['histogram_raw'], data['phi_vals'],
                                    data['shots_per_pos'])
            n_bins = len(chi2_bins)
            print(f"  {os.path.basename(f):40s}  chi2={chi2_bins.sum():.1f}  "
                  f"chi2/dof={chi2_bins.sum()/(n_bins-1):.2f}  "
                  f"max_bin={chi2_bins.max():.1f}")


if __name__ == '__main__':
    main()
