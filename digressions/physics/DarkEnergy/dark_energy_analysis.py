"""
Dark Energy from Type Ia Supernovae: Pantheon+ Analysis
========================================================

This script downloads the Pantheon+ supernova dataset and performs three
calculations that demonstrate the accelerating expansion of the universe:

1. Hubble Diagram — distance modulus vs. redshift with cosmological model overlays
2. Cosmological Parameter Fit — chi-squared fit for Omega_m (matter density)
3. Deceleration Parameter — is the expansion accelerating or decelerating?

Data source: Pantheon+SH0ES Data Release
    https://github.com/PantheonPlusSH0ES/DataRelease
    Scolnic et al. (2022), Brout et al. (2022)

Requirements: numpy, scipy, matplotlib
    pip install numpy scipy matplotlib

Connection to black hole physics:
    If the universe is accelerating (dark energy dominated), the CMB will continue
    cooling indefinitely. This means black holes will eventually find themselves in
    a colder environment than their Hawking temperature, allowing net evaporation.
    This script provides the observational evidence for that conclusion.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, minimize
import matplotlib.pyplot as plt
import urllib.request
import os


# =============================================================================
# STEP 0: Download the Pantheon+ data
# =============================================================================

DATA_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
)
DATA_FILE = "Pantheon+SH0ES.dat"


def download_data():
    """Download the Pantheon+ distance data if not already present."""
    if not os.path.exists(DATA_FILE):
        print(f"Downloading Pantheon+ data from GitHub...")
        urllib.request.urlretrieve(DATA_URL, DATA_FILE)
        print(f"Saved to {DATA_FILE}")
    else:
        print(f"Using cached {DATA_FILE}")


def load_data():
    """Load the Pantheon+ data file and extract redshift, distance modulus, and errors."""
    download_data()

    # Read the header to get column names
    with open(DATA_FILE, "r") as f:
        header_line = f.readline().strip()

    # Parse column names (strip leading # or whitespace)
    columns = header_line.lstrip("# ").split()

    # Load the numerical data, skipping the header row
    data = np.genfromtxt(DATA_FILE, names=columns, skip_header=1,
                         dtype=None, encoding="utf-8")

    # Extract the columns we need
    # Try common column name variants
    z_col = None
    for name in ["zHD", "zCMB", "Z_HD", "z_hd"]:
        if name in columns:
            z_col = name
            break

    mu_col = None
    for name in ["MU_SH0ES", "MU", "mu", "m_b_corr", "DISTANCE_MODULUS"]:
        if name in columns:
            mu_col = name
            break

    muerr_col = None
    for name in ["MU_SH0ES_ERR_DIAG", "MUERR", "MU_ERR", "m_b_corr_err_DIAG",
                 "muerr", "DISTANCE_MODULUS_ERR"]:
        if name in columns:
            muerr_col = name
            break

    if z_col is None or mu_col is None:
        print(f"Available columns: {columns}")
        raise ValueError("Could not identify redshift and distance modulus columns")

    z = np.array(data[z_col], dtype=float)
    mu = np.array(data[mu_col], dtype=float)

    if muerr_col and muerr_col in columns:
        mu_err = np.array(data[muerr_col], dtype=float)
    else:
        mu_err = np.ones_like(mu) * 0.1  # fallback

    # Filter out any bad data
    mask = (z > 0.01) & np.isfinite(mu) & np.isfinite(mu_err) & (mu_err > 0)
    z = z[mask]
    mu = mu[mask]
    mu_err = mu_err[mask]

    print(f"Loaded {len(z)} supernovae with z in [{z.min():.4f}, {z.max():.4f}]")
    return z, mu, mu_err


# =============================================================================
# STEP 1: Cosmological distance calculations
# =============================================================================

# Speed of light in km/s
C_KMS = 299792.458


def luminosity_distance(z, Omega_m, Omega_L=None, H0=70.0):
    """
    Compute luminosity distance d_L(z) for a LCDM cosmology.

    Parameters:
        z: redshift (scalar or array)
        Omega_m: matter density parameter
        Omega_L: dark energy density parameter (default: 1 - Omega_m for flat)
        H0: Hubble constant in km/s/Mpc

    Returns:
        d_L in Mpc
    """
    if Omega_L is None:
        Omega_L = 1.0 - Omega_m  # flat universe

    # Handle the empty universe (Milne model) specially
    Omega_k = 1.0 - Omega_m - Omega_L

    def integrand(zp):
        Ez2 = Omega_m * (1 + zp)**3 + Omega_k * (1 + zp)**2 + Omega_L
        if Ez2 <= 0:
            return np.inf
        return 1.0 / np.sqrt(Ez2)

    if np.isscalar(z):
        integral, _ = quad(integrand, 0, z)
        return (C_KMS / H0) * (1 + z) * integral
    else:
        result = np.zeros_like(z, dtype=float)
        for i, zi in enumerate(z):
            integral, _ = quad(integrand, 0, zi)
            result[i] = (C_KMS / H0) * (1 + zi) * integral
        return result


def distance_modulus_model(z, Omega_m, Omega_L=None, H0=70.0):
    """
    Compute theoretical distance modulus mu = 5*log10(d_L/10pc).

    Note: Since H0 enters as an overall offset in mu, and we marginalize over
    the absolute magnitude M (equivalent to marginalizing over H0), we can
    fix H0 and fit only for the shape parameter Omega_m.
    """
    d_L = luminosity_distance(z, Omega_m, Omega_L, H0)
    # d_L is in Mpc; convert to pc for distance modulus
    return 5.0 * np.log10(d_L * 1e6) - 5.0


# =============================================================================
# STEP 2: Chi-squared fitting
# =============================================================================

def chi_squared(Omega_m, z, mu_obs, mu_err):
    """
    Compute chi-squared for a flat LCDM model, analytically marginalizing
    over the absolute magnitude offset (equivalent to marginalizing over H0).
    """
    mu_model = distance_modulus_model(z, Omega_m)

    # The absolute magnitude M is degenerate with H0. Marginalize analytically:
    # mu_obs = mu_model + offset, where offset = M - M_true (or equivalently 5*log10(H0/70))
    # Best-fit offset:
    delta = mu_obs - mu_model
    w = 1.0 / mu_err**2
    offset = np.sum(w * delta) / np.sum(w)

    residuals = (mu_obs - mu_model - offset) / mu_err
    return np.sum(residuals**2)


def fit_omega_m(z, mu_obs, mu_err):
    """Fit for Omega_m in a flat LCDM model."""
    result = minimize_scalar(chi_squared, bounds=(0.01, 0.99), method="bounded",
                             args=(z, mu_obs, mu_err))
    return result.x, result.fun


# =============================================================================
# STEP 3: Deceleration parameter
# =============================================================================

def deceleration_parameter(Omega_m, Omega_L=None):
    """
    Compute the present-day deceleration parameter q0.

    q0 = Omega_m/2 - Omega_L

    If q0 < 0, the expansion is accelerating.
    """
    if Omega_L is None:
        Omega_L = 1.0 - Omega_m
    return Omega_m / 2.0 - Omega_L


# =============================================================================
# STEP 4: Plotting
# =============================================================================

def make_hubble_diagram(z, mu_obs, mu_err, Omega_m_best):
    """Create the Hubble diagram with data and model overlays."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), height_ratios=[3, 1],
                                    sharex=True)
    fig.suptitle("Hubble Diagram: Evidence for Dark Energy\n(Pantheon+ Dataset)",
                 fontsize=14)

    # Sort by redshift for smooth model curves
    z_model = np.linspace(0.01, max(z) * 1.05, 200)

    # Model curves
    mu_best = distance_modulus_model(z_model, Omega_m_best)
    mu_empty = distance_modulus_model(z_model, 0.0, 0.0)  # empty universe (coasting)
    mu_matter = distance_modulus_model(z_model, 1.0, 0.0)  # matter-only, no dark energy
    mu_EdS = distance_modulus_model(z_model, 1.0)  # Einstein-de Sitter (flat, matter only... wait, that's Omega_L=0)

    # Compute offsets to align models (marginalize over H0/M)
    w = 1.0 / mu_err**2
    mu_best_at_data = distance_modulus_model(z, Omega_m_best)
    offset_best = np.sum(w * (mu_obs - mu_best_at_data)) / np.sum(w)

    mu_empty_at_data = distance_modulus_model(z, 0.0, 0.0)
    offset_empty = np.sum(w * (mu_obs - mu_empty_at_data)) / np.sum(w)

    mu_matter_at_data = distance_modulus_model(z, 1.0, 0.0)
    offset_matter = np.sum(w * (mu_obs - mu_matter_at_data)) / np.sum(w)

    # Plot data
    ax1.errorbar(z, mu_obs - offset_best, yerr=mu_err, fmt=".", color="gray",
                 alpha=0.3, markersize=2, label="Pantheon+ SNe Ia")

    # Plot models (shifted by their respective offsets relative to best-fit)
    ax1.plot(z_model, mu_best, "r-", linewidth=2,
             label=f"Best fit: Ω_m={Omega_m_best:.3f}, Ω_Λ={1-Omega_m_best:.3f}")
    ax1.plot(z_model, mu_empty + (offset_empty - offset_best), "b--", linewidth=1.5,
             label="Empty universe (coasting)")
    ax1.plot(z_model, mu_matter + (offset_matter - offset_best), "g:", linewidth=1.5,
             label="Matter only (Ω_m=1, Ω_Λ=0)")

    ax1.set_ylabel("Distance modulus μ (mag)")
    ax1.legend(loc="lower right", fontsize=10)
    ax1.set_xlim(0.01, max(z) * 1.05)

    # Residuals relative to best fit
    mu_best_at_data = distance_modulus_model(z, Omega_m_best)
    residuals = mu_obs - mu_best_at_data - offset_best
    ax2.errorbar(z, residuals, yerr=mu_err, fmt=".", color="gray", alpha=0.3,
                 markersize=2)
    ax2.axhline(0, color="r", linewidth=1)
    ax2.set_xlabel("Redshift z")
    ax2.set_ylabel("Residual (mag)")
    ax2.set_ylim(-1.0, 1.0)

    plt.tight_layout()
    plt.savefig("hubble_diagram.png", dpi=150, bbox_inches="tight")
    print("Saved: hubble_diagram.png")
    plt.close()


def make_chi2_plot(z, mu_obs, mu_err, Omega_m_best):
    """Plot chi-squared as a function of Omega_m."""
    Om_range = np.linspace(0.05, 0.95, 100)
    chi2_values = [chi_squared(Om, z, mu_obs, mu_err) for Om in Om_range]
    chi2_min = min(chi2_values)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(Om_range, np.array(chi2_values) - chi2_min, "b-", linewidth=2)
    ax.axvline(Omega_m_best, color="r", linestyle="--",
               label=f"Best fit: Ω_m = {Omega_m_best:.3f}")
    ax.axhline(1.0, color="gray", linestyle=":", alpha=0.5, label="Δχ² = 1 (1σ)")
    ax.axhline(4.0, color="gray", linestyle="--", alpha=0.5, label="Δχ² = 4 (2σ)")

    ax.set_xlabel("Ω_m (matter density parameter)")
    ax.set_ylabel("Δχ² (relative to minimum)")
    ax.set_title("Cosmological Fit: Matter Density from Pantheon+ SNe Ia")
    ax.set_ylim(0, 30)
    ax.legend()

    plt.tight_layout()
    plt.savefig("chi2_omega_m.png", dpi=150, bbox_inches="tight")
    print("Saved: chi2_omega_m.png")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("DARK ENERGY FROM TYPE Ia SUPERNOVAE")
    print("Pantheon+ Dataset Analysis")
    print("=" * 70)
    print()

    # Load data
    z, mu_obs, mu_err = load_data()
    print()

    # --- Calculation 1: Fit for Omega_m ---
    print("-" * 70)
    print("CALCULATION 1: Fit for matter density (flat LCDM)")
    print("-" * 70)
    Omega_m_best, chi2_min = fit_omega_m(z, mu_obs, mu_err)
    Omega_L_best = 1.0 - Omega_m_best
    ndof = len(z) - 2  # 2 parameters: Omega_m + offset
    print(f"  Best-fit Ω_m = {Omega_m_best:.4f}")
    print(f"  Best-fit Ω_Λ = {Omega_L_best:.4f}")
    print(f"  χ²/dof = {chi2_min:.1f}/{ndof} = {chi2_min/ndof:.3f}")
    print(f"  (Published Pantheon+ result: Ω_m = 0.334 ± 0.018)")
    print()

    # --- Calculation 2: Deceleration parameter ---
    print("-" * 70)
    print("CALCULATION 2: Deceleration parameter")
    print("-" * 70)
    q0 = deceleration_parameter(Omega_m_best)
    print(f"  q₀ = Ω_m/2 - Ω_Λ = {Omega_m_best:.3f}/2 - {Omega_L_best:.3f} = {q0:.4f}")
    if q0 < 0:
        print(f"  q₀ < 0  →  THE EXPANSION IS ACCELERATING")
        print(f"  The universe is not gravitationally bound.")
        print(f"  The CMB will continue cooling indefinitely.")
        print(f"  Black holes will eventually be able to evaporate.")
    else:
        print(f"  q₀ > 0  →  The expansion is decelerating")
    print()

    # --- Calculation 3: Model comparison ---
    print("-" * 70)
    print("CALCULATION 3: Model comparison (is dark energy needed?)")
    print("-" * 70)
    chi2_best = chi_squared(Omega_m_best, z, mu_obs, mu_err)
    chi2_no_DE = chi_squared(1.0, z, mu_obs, mu_err)  # Omega_m=1, flat → Omega_L=0... no.
    # For matter-only with no dark energy, use Omega_L=0 explicitly:
    # We need a version that allows non-flat
    mu_model_noDE = distance_modulus_model(z, 1.0, 0.0)
    w = 1.0 / mu_err**2
    offset_noDE = np.sum(w * (mu_obs - mu_model_noDE)) / np.sum(w)
    chi2_no_DE = np.sum(((mu_obs - mu_model_noDE - offset_noDE) / mu_err)**2)

    mu_model_empty = distance_modulus_model(z, 0.0, 0.0)
    offset_empty = np.sum(w * (mu_obs - mu_model_empty)) / np.sum(w)
    chi2_empty = np.sum(((mu_obs - mu_model_empty - offset_empty) / mu_err)**2)

    print(f"  Best-fit ΛCDM (Ω_m={Omega_m_best:.3f}):  χ² = {chi2_best:.1f}")
    print(f"  Matter-only (Ω_m=1, Ω_Λ=0):             χ² = {chi2_no_DE:.1f}")
    print(f"  Empty universe (Ω_m=0, Ω_Λ=0):          χ² = {chi2_empty:.1f}")
    print(f"  Δχ² (matter-only vs best):               {chi2_no_DE - chi2_best:.1f}")
    print(f"  → Matter-only model rejected at > {np.sqrt(chi2_no_DE - chi2_best):.0f}σ")
    print()

    # --- Connection to black holes ---
    print("-" * 70)
    print("CONNECTION TO BLACK HOLE EVAPORATION")
    print("-" * 70)
    print(f"  Current CMB temperature: 2.725 K")
    print(f"  Hawking temperature of 1 M☉ black hole: ~6 × 10⁻⁸ K")
    print(f"  Ratio: CMB is ~5 × 10⁷ times hotter than the black hole")
    print(f"  → Solar-mass black holes are currently GAINING mass from CMB")
    print()
    print(f"  Since q₀ = {q0:.3f} < 0 (accelerating expansion):")
    print(f"  → CMB temperature will drop exponentially")
    print(f"  → Doubling time of scale factor: ~10¹⁰ years")
    print(f"  → Time for CMB to reach 10⁻⁷ K: ~200 billion years")
    print(f"  → After that: stellar-mass black holes begin net evaporation")
    print(f"  → Full evaporation of last black holes: ~10⁶⁷ to 10¹⁰⁰ years")
    print()

    # --- Generate plots ---
    print("-" * 70)
    print("GENERATING PLOTS")
    print("-" * 70)
    make_hubble_diagram(z, mu_obs, mu_err, Omega_m_best)
    make_chi2_plot(z, mu_obs, mu_err, Omega_m_best)
    print()
    print("Done. The Hubble diagram visually shows supernovae are FARTHER than")
    print("a matter-only universe predicts — direct evidence for acceleration.")


if __name__ == "__main__":
    main()
