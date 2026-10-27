"""
born_triangle.py

A fixed (non-animated) figure: the "Born triangle".

Goal: show the Born probability interpretation geometrically. A normalized
single-qubit state has |alpha|^2 + |beta|^2 = 1, so (|alpha|, |beta|) are the
legs of a right triangle with hypotenuse 1. The *squares* of the legs are the
measurement probabilities P(0) = |alpha|^2 and P(1) = |beta|^2. As the state
changes, the hypotenuse (length 1) leans at different angles like a ladder
against a wall, trading probability between the two outcomes.

Layout:
  Left  : two stacked complex unit discs (alpha on top, beta on bottom),
          exactly as in C_to_Bloch.py.
            alpha: magnitude 0.90, phase 45 deg.
            beta : phase offset 7*pi/9 relative to alpha; magnitude from
                   normalization. A faint "ghost" of alpha is drawn on the
                   beta disc for phase reference.
  Right : seven right triangles overlaid with coincident right angles. Legs =
          (|alpha|, |beta|); hypotenuse always 1. One triangle (the 0.90 state)
          is highlighted; the rest form the leaning-ladder fan.

Requirements: pip install matplotlib numpy
Usage: python born_triangle.py
Output: born_triangle.png
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


# ---------------------------------------------------------------------------
# The highlighted state
# ---------------------------------------------------------------------------
R_ALPHA = 0.90
PHI_ALPHA = np.deg2rad(45.0)
REL_PHASE = 7 * np.pi / 9          # phase of beta relative to alpha (= 140 deg)

R_BETA = np.sqrt(1.0 - R_ALPHA ** 2)   # normalization: |a|^2 + |b|^2 = 1
PHI_BETA = PHI_ALPHA + REL_PHASE

ALPHA = R_ALPHA * np.exp(1j * PHI_ALPHA)
BETA = R_BETA * np.exp(1j * PHI_BETA)

COL_A = '#1f77b4'   # alpha color
COL_B = '#d62728'   # beta color


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(14, 8))
fig.suptitle("Born-rule triangle", fontsize=20, fontweight='bold')

# Left column has three rows: alpha disc, beta disc (raised), and a text line.
# The thin bottom row makes room for the superposition caption.
gs = fig.add_gridspec(nrows=3, ncols=2, width_ratios=[1.0, 1.7],
                      height_ratios=[1.0, 1.0, 0.22],
                      left=0.05, right=0.97, bottom=0.08, top=0.90,
                      wspace=0.18, hspace=0.15)
ax_alpha = fig.add_subplot(gs[0, 0])
ax_beta = fig.add_subplot(gs[1, 0])
ax_text = fig.add_subplot(gs[2, 0])   # superposition caption line
ax_tri = fig.add_subplot(gs[:, 1])


# ---------------------------------------------------------------------------
# Complex-disc drawing (adapted from C_to_Bloch.py)
# ---------------------------------------------------------------------------
def draw_disc(ax, value, label, color, ghost=None, title_fontsize=13):
    ax.clear()
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    ax.set_axis_off()

    ax.add_patch(Circle((0, 0), 1.0, fill=False, edgecolor='steelblue',
                        linewidth=1.5, alpha=0.8))
    ax.add_patch(Circle((0, 0), 0.5, fill=False, edgecolor='steelblue',
                        linewidth=0.6, alpha=0.3, linestyle='--'))
    ax.plot([-1.15, 1.15], [0, 0], 'gray', linewidth=0.8, alpha=0.5)
    ax.plot([0, 0], [-1.15, 1.15], 'gray', linewidth=0.8, alpha=0.5)
    ax.text(1.18, 0.0, "Re", color='gray', fontsize=8, va='center')
    ax.text(0.0, 1.18, "Im", color='gray', fontsize=8, ha='center')

    # Optional faint ghost phasor for phase reference.
    if ghost is not None:
        gre, gim = np.real(ghost), np.imag(ghost)
        ax.annotate("", xy=(gre, gim), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='-|>', color=COL_A, lw=2.0,
                                    alpha=0.3))
        ax.scatter([gre], [gim], color=COL_A, s=40, alpha=0.3, zorder=4)

        # Arc from the ghost phasor to this disc's phasor, marking the
        # relative angle between them. Drawn on the minor (< pi) side via the
        # shortest signed sweep, at radius 2/3 of this phasor's magnitude.
        a0 = np.angle(ghost)
        delta = (np.angle(value) - a0 + np.pi) % (2 * np.pi) - np.pi  # in (-pi,pi]
        arc_r = (2.0 / 3.0) * np.abs(value)
        arc_ang = a0 + np.linspace(0.0, delta, 60)
        ax.plot(arc_r * np.cos(arc_ang), arc_r * np.sin(arc_ang),
                color='dimgray', lw=1.5, alpha=0.8)

    re, im = np.real(value), np.imag(value)
    ax.annotate("", xy=(re, im), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=2.5))
    ax.scatter([re], [im], color=color, s=70, zorder=5)
    ax.set_title(label, fontsize=title_fontsize, fontweight='bold',
                 color=color, pad=6)


draw_disc(ax_alpha, ALPHA,
          rf"$\alpha = {R_ALPHA:.2f}\,e^{{i\,\pi/4}}$", COL_A,
          title_fontsize=18)
draw_disc(ax_beta, BETA,
          rf"$\beta = {R_BETA:.3f}\,e^{{i\,(\pi/4 + 7\pi/9)}}$", COL_B,
          ghost=ALPHA, title_fontsize=18)

# Relative-phase label below/right of the beta disc.
ax_beta.text(0.98, -0.02,
             r"$\angle\beta - \angle\alpha = 7\pi/9$",
             transform=ax_beta.transAxes, fontsize=12, color='dimgray',
             ha='right', va='top')

# Superposition caption beneath the two discs.
ax_text.set_axis_off()
ax_text.text(0.5, 0.5,
             r"qubit state: superposition $\alpha |0\rangle + \beta |1\rangle$",
             fontsize=15, ha='center', va='center')


# ---------------------------------------------------------------------------
# Right panel: seven overlaid right triangles (the leaning ladder)
#
# Right angle at the origin. Horizontal leg = |alpha| (along +x), vertical leg
# = |beta| (along +y), hypotenuse from (|alpha|, 0) to (0, |beta|) has length 1.
# ---------------------------------------------------------------------------
ax_tri.set_aspect('equal')
ax_tri.set_xlim(-0.08, 1.12)
ax_tri.set_ylim(-0.08, 1.12)
ax_tri.set_xlabel(r"$|\alpha|$  (leg; $|\alpha|^2 = P(0)$)", fontsize=12)
ax_tri.set_ylabel(r"$|\beta|$  (leg; $|\beta|^2 = P(1)$)", fontsize=12)
ax_tri.text(0.5, 1.1,
            "Hypotenuse = 1 always; legs trade off (Born: leg$^2$ = prob)",
            fontsize=13, ha='center', va='center')
ax_tri.spines['top'].set_visible(False)
ax_tri.spines['right'].set_visible(False)

# Seven states: sweep |alpha| across a spread of values.
alpha_mags = np.array([0.15, 0.35, 0.55, 0.707, 0.80, 0.90, 0.97])

for ra in alpha_mags:
    rb = np.sqrt(1.0 - ra ** 2)
    highlight = np.isclose(ra, R_ALPHA)
    col = 'black' if highlight else 'gray'
    lw = 2.6 if highlight else 1.2
    alpha_line = 1.0 if highlight else 0.55

    # Hypotenuse (the "ladder").
    ax_tri.plot([ra, 0], [0, rb], color=col, lw=lw, alpha=alpha_line)
    # Endpoint on the unit arc.
    ax_tri.scatter([ra], [0], color=COL_A, s=28 if highlight else 14,
                   zorder=5, alpha=alpha_line)
    ax_tri.scatter([0], [rb], color=COL_B, s=28 if highlight else 14,
                   zorder=5, alpha=alpha_line)

    if highlight:
        # Draw the two legs explicitly for the highlighted state.
        ax_tri.plot([0, ra], [0, 0], color=COL_A, lw=3.0, zorder=4)
        ax_tri.plot([0, 0], [0, rb], color=COL_B, lw=3.0, zorder=4)
        # Right-angle marker at the origin.
        s = 0.05
        ax_tri.plot([s, s, 0], [0, s, s], color='black', lw=1.0)
        # Annotate the highlighted state.
        ax_tri.annotate(
            rf"$|\alpha|={ra:.2f}$, $P(0)={ra**2:.2f}$"
            "\n"
            rf"$|\beta|={rb:.3f}$, $P(1)={rb**2:.2f}$"
            "\n"
            rf"$|\alpha|^2 + |\beta|^2 = 1$",
            xy=(ra / 2, rb / 2), xytext=(0.52, 0.72),
            fontsize=12,
            arrowprops=dict(arrowstyle='->', color='black', lw=1.0))

fig.savefig('images/born_triangle.png', dpi=150)
print("Saved: images/born_triangle.png")
print(f"Highlighted state: |alpha|={R_ALPHA:.2f}, |beta|={R_BETA:.4f}")
print(f"  P(0)=|alpha|^2={R_ALPHA**2:.4f}, P(1)=|beta|^2={R_BETA**2:.4f}, "
      f"sum={R_ALPHA**2 + R_BETA**2:.4f}")
