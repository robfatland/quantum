"""
Noise Analysis: Simulator vs IBM Quantum Hardware.

Compares double-slit results from AerSimulator and IBM hardware to
characterize the noise differences.

Usage:
  python noise_analysis.py

Requires:
  double_slit_results_local.json   (from: python double_slit.py --backend local ...)
  double_slit_results_ibm.json     (from: python double_slit.py --backend ibm ...)

Output:
  stdout: full analysis
  simulator_to_ibm_quantum_noise_analysis.txt: same content written to file
"""

import json
import sys
import numpy as np


def load_results(filename):
    """Load a double_slit_results JSON file."""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def compute_theory(phi_vals, shots_per_pos):
    """Compute theoretical counts (no envelope) at each position."""
    phi = np.array(phi_vals)
    prob = np.cos(phi / 2) ** 2
    return prob * shots_per_pos, prob


def compute_visibility(histogram, shots_per_pos):
    """Compute fringe visibility from histogram."""
    prob = np.array(histogram) / shots_per_pos
    p_max = np.max(prob)
    p_min = np.min(prob)
    if p_max + p_min == 0:
        return 0.0
    return (p_max - p_min) / (p_max + p_min)


def compute_residuals(histogram, theory_counts):
    """Compute residuals (data - theory)."""
    return np.array(histogram) - np.array(theory_counts)


def compute_chi_squared(histogram, theory_counts, shots_per_pos):
    """Compute chi-squared between data and theory."""
    h = np.array(histogram)
    t = np.array(theory_counts)
    # Expected variance per bin: Np(1-p) where p = t/shots
    p = t / shots_per_pos
    variance = shots_per_pos * p * (1 - p)
    # Avoid division by zero at extremes
    variance = np.maximum(variance, 1.0)
    chi2 = np.sum((h - t) ** 2 / variance)
    return chi2


def compute_bias(histogram, theory_counts, phi_vals, shots_per_pos):
    """Compute bias at minima (dark fringes) and maxima (bright fringes)."""
    prob = np.array(histogram) / shots_per_pos
    theory_prob = np.array(theory_counts) / shots_per_pos

    # Find positions near minima (theory < 0.1) and maxima (theory > 0.9)
    minima_mask = theory_prob < 0.1
    maxima_mask = theory_prob > 0.9

    bias_at_min = np.mean(prob[minima_mask]) if np.any(minima_mask) else None
    bias_at_max = np.mean(prob[maxima_mask]) if np.any(maxima_mask) else None

    return bias_at_min, bias_at_max, np.sum(minima_mask), np.sum(maxima_mask)


def compute_excess_variance(histogram, theory_counts, shots_per_pos):
    """
    Compare measured variance to expected binomial variance.
    Uses windowed approach: group adjacent positions and compare.
    """
    h = np.array(histogram, dtype=float)
    t = np.array(theory_counts, dtype=float)
    p = t / shots_per_pos

    # Expected variance per position (binomial)
    expected_var = shots_per_pos * p * (1 - p)

    # Measured variance: use residuals squared as proxy
    residuals = h - t
    measured_var = residuals ** 2

    # Ratio (averaged over non-extreme positions to avoid division issues)
    mid_mask = (p > 0.1) & (p < 0.9)
    if np.sum(mid_mask) > 0:
        ratio = np.mean(measured_var[mid_mask]) / np.mean(expected_var[mid_mask])
    else:
        ratio = None

    return ratio


def analyze(sim_file, ibm_file):
    """Run the full comparison and return report as string."""
    lines = []

    def out(s=""):
        lines.append(s)

    out("=" * 70)
    out("NOISE ANALYSIS: Simulator vs IBM Quantum Hardware")
    out("=" * 70)
    out()

    # Load data
    try:
        sim = load_results(sim_file)
    except FileNotFoundError:
        out(f"ERROR: {sim_file} not found.")
        out(f"  Run: python double_slit.py --backend local --screen-pts 100 "
            f"--fringes 6 --shots-per-pos 2000")
        return "\n".join(lines)

    try:
        ibm = load_results(ibm_file)
    except FileNotFoundError:
        out(f"ERROR: {ibm_file} not found.")
        out(f"  Run: python double_slit.py --backend ibm --screen-pts 100 "
            f"--fringes 6 --shots-per-pos 2000")
        return "\n".join(lines)

    out(f"Simulator file: {sim_file}")
    out(f"  Backend: {sim.get('backend', 'unknown')}")
    out(f"  Screen points: {sim['screen_pts']}")
    out(f"  Fringes: {sim['num_fringes']}")
    out(f"  Shots/position: {sim['shots_per_pos']}")
    out()
    out(f"Hardware file: {ibm_file}")
    out(f"  Backend: {ibm.get('backend', 'unknown')}")
    out(f"  Screen points: {ibm['screen_pts']}")
    out(f"  Fringes: {ibm['num_fringes']}")
    out(f"  Shots/position: {ibm['shots_per_pos']}")
    out()

    # Check compatibility
    if sim['screen_pts'] != ibm['screen_pts']:
        out("WARNING: Screen point counts differ. Comparison may be approximate.")
    if sim['num_fringes'] != ibm['num_fringes']:
        out("WARNING: Fringe counts differ.")
    if sim['shots_per_pos'] != ibm['shots_per_pos']:
        out("WARNING: Shots per position differ.")
    out()

    # Use raw histograms (before envelope) for apples-to-apples comparison
    sim_hist = np.array(sim['histogram_raw'])
    ibm_hist = np.array(ibm['histogram_raw'])
    sim_shots = sim['shots_per_pos']
    ibm_shots = ibm['shots_per_pos']

    # Theory (no envelope)
    sim_theory, sim_prob = compute_theory(sim['phi_vals'], sim_shots)
    ibm_theory, ibm_prob = compute_theory(ibm['phi_vals'], ibm_shots)

    out("-" * 70)
    out("1. FRINGE VISIBILITY")
    out("-" * 70)
    sim_vis = compute_visibility(sim_hist, sim_shots)
    ibm_vis = compute_visibility(ibm_hist, ibm_shots)
    out(f"  Simulator:  V = {sim_vis:.4f}")
    out(f"  Hardware:   V = {ibm_vis:.4f}")
    out(f"  Reduction:  {(1 - ibm_vis/sim_vis)*100:.1f}%")
    out(f"  (V=1 is perfect contrast; V<1 indicates noise/decoherence)")
    out()

    out("-" * 70)
    out("2. BIAS AT DARK FRINGES (readout error / T1 signature)")
    out("-" * 70)
    sim_bias_min, sim_bias_max, n_min, n_max = compute_bias(
        sim_hist, sim_theory, sim['phi_vals'], sim_shots)
    ibm_bias_min, ibm_bias_max, _, _ = compute_bias(
        ibm_hist, ibm_theory, ibm['phi_vals'], ibm_shots)

    out(f"  Positions near minima (theory P<0.1): {n_min}")
    out(f"  Positions near maxima (theory P>0.9): {n_max}")
    out()
    if sim_bias_min is not None:
        out(f"  Simulator mean P at minima:  {sim_bias_min:.4f}  (expect ~0)")
        out(f"  Hardware mean P at minima:   {ibm_bias_min:.4f}  (expect ~0)")
        out(f"  Hardware bias floor: +{ibm_bias_min:.4f}")
    else:
        out("  (Not enough extreme positions to measure bias)")
    out()
    if sim_bias_max is not None:
        out(f"  Simulator mean P at maxima:  {sim_bias_max:.4f}  (expect ~1)")
        out(f"  Hardware mean P at maxima:   {ibm_bias_max:.4f}  (expect ~1)")
        out(f"  Hardware ceiling deficit: -{1 - ibm_bias_max:.4f}")
    out()

    out("-" * 70)
    out("3. CHI-SQUARED (goodness of fit to theory)")
    out("-" * 70)
    sim_chi2 = compute_chi_squared(sim_hist, sim_theory, sim_shots)
    ibm_chi2 = compute_chi_squared(ibm_hist, ibm_theory, ibm_shots)
    dof = len(sim_hist) - 1
    out(f"  Degrees of freedom: {dof}")
    out(f"  Simulator chi2:  {sim_chi2:.1f}  (chi2/dof = {sim_chi2/dof:.2f})")
    out(f"  Hardware chi2:   {ibm_chi2:.1f}  (chi2/dof = {ibm_chi2/dof:.2f})")
    out(f"  (chi2/dof ~ 1.0 means noise matches binomial shot noise)")
    out(f"  (chi2/dof >> 1 means systematic errors beyond shot noise)")
    out()

    out("-" * 70)
    out("4. EXCESS VARIANCE (gate errors adding stochastic noise)")
    out("-" * 70)
    sim_var_ratio = compute_excess_variance(sim_hist, sim_theory, sim_shots)
    ibm_var_ratio = compute_excess_variance(ibm_hist, ibm_theory, ibm_shots)
    if sim_var_ratio is not None:
        out(f"  Simulator variance/binomial: {sim_var_ratio:.2f}x  (expect ~1.0)")
        out(f"  Hardware variance/binomial:  {ibm_var_ratio:.2f}x  (expect >1.0)")
    else:
        out("  (Insufficient mid-range positions for variance analysis)")
    out()

    out("-" * 70)
    out("5. RESIDUAL STATISTICS")
    out("-" * 70)
    sim_resid = compute_residuals(sim_hist, sim_theory)
    ibm_resid = compute_residuals(ibm_hist, ibm_theory)
    out(f"  Simulator residuals:")
    out(f"    Mean:   {np.mean(sim_resid):+.2f}  (expect ~0)")
    out(f"    Std:    {np.std(sim_resid):.2f}")
    out(f"    Skew:   {np.mean((sim_resid/np.std(sim_resid))**3):.3f}")
    out()
    out(f"  Hardware residuals:")
    out(f"    Mean:   {np.mean(ibm_resid):+.2f}  (expect ~0 if no bias)")
    out(f"    Std:    {np.std(ibm_resid):.2f}")
    out(f"    Skew:   {np.mean((ibm_resid/np.std(ibm_resid))**3):.3f}")
    out()

    out("-" * 70)
    out("6. INTERPRETATION")
    out("-" * 70)
    out()
    if ibm_vis < sim_vis * 0.95:
        out("  * Visibility is reduced on hardware -> readout error + decoherence")
    else:
        out("  * Visibility is comparable -> minimal hardware degradation")

    if ibm_bias_min is not None and ibm_bias_min > 0.02:
        out("  * Positive bias at dark fringes -> readout error")
        out(f"    Estimated readout error rate: ~{ibm_bias_min:.3f}")
    elif ibm_bias_min is not None:
        out("  * Minimal bias at dark fringes -> readout error is small")

    if ibm_chi2 / dof > 2.0:
        out("  * Chi-squared excess -> systematic hardware noise beyond shot noise")
    else:
        out("  * Chi-squared is moderate -> hardware noise is dominated by shot noise")

    if ibm_var_ratio is not None and ibm_var_ratio > 1.5:
        out("  * Excess variance -> gate errors contribute stochastic noise")

    out()
    out("=" * 70)
    out("END OF ANALYSIS")
    out("=" * 70)

    return "\n".join(lines)


if __name__ == "__main__":
    sim_file = "double_slit_results_local.json"
    ibm_file = "double_slit_results_ibm.json"

    report = analyze(sim_file, ibm_file)

    # Print to stdout
    print(report)

    # Write to file
    output_file = "simulator_to_ibm_quantum_noise_analysis.txt"
    with open(output_file, 'w') as f:
        f.write(report)
        f.write("\n")
    print(f"\nSaved: {output_file}")
