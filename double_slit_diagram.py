"""
double_slit_diagram.py

Schematic of the double-slit experiment, saved as a PNG at 16:9 (slide ratio).

Layout (fractions of the horizontal axis, 0 = left edge, 1 = right edge):
  - Particle source : center-left         (x ~ 0.08)
  - Barrier (2 slits): 1/3 from the left   (x = 0.333)
  - Detector bank    : 1/10 from the right (x = 0.9)

The detector is a vertical bank of DISCRETE little boxes, each open on its left
side so particles impinge left-to-right -- this indicates the quantization of
detector locations. The fringe pattern drawn against the bank uses the SAME
formulation as the Aer-vs-IBM comparison figure in double_slit.py:

    I(y) = cos^2(phi/2) * sinc^2(slit_ratio * x_norm)

with phi spanning +/- pi*num_fringes and x_norm in [-0.5, 0.5] (np.sinc is the
normalized sinc, matching that script's convention).

Optional propagation-line overlays (off by default):
  --center True   draw a line from each slit to the CENTRAL bright fringe
                  (equal path lengths -> in phase -> constructive interference)
  --null True     draw a line from each slit to the FIRST cos^2 dark fringe
                  (half-wavelength path difference -> destructive interference)
Both may be set together. The output filename gains a suffix accordingly:
  (none)                 -> images/double_slit_diagram.png
  --center True          -> images/double_slit_diagram_center.png
  --null True            -> images/double_slit_diagram_null.png
  --center True --null True -> images/double_slit_diagram_center_null.png

Requirements: pip install matplotlib numpy
Usage: python double_slit_diagram.py [--center True] [--null True]
Output: images/double_slit_diagram[...].png
"""

import os
import argparse

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


# ---------------------------------------------------------------------------
# Command-line flags. Written as `--center True` / `--null True` (a value,
# not a bare store-true flag) so the exact requested invocation works. Any of
# {true, t, yes, y, 1} (case-insensitive) counts as True.
# ---------------------------------------------------------------------------
def _truthy(s):
    return str(s).strip().lower() in ('true', 't', 'yes', 'y', '1')


parser = argparse.ArgumentParser(description="Double-slit schematic diagram.")
parser.add_argument('--center', type=_truthy, default=False,
                    help="draw slit->central-fringe lines (constructive)")
parser.add_argument('--null', type=_truthy, default=False,
                    help="draw slit->first-dark-fringe lines (destructive)")
args = parser.parse_args()


# ---------------------------------------------------------------------------
# Geometry. Horizontal axis 0..1; vertical axis sized for a 16:9 canvas so the
# scene is not vertically stretched (we do NOT force equal aspect, which would
# override the figure ratio).
# ---------------------------------------------------------------------------
ASPECT = 16.0 / 9.0
Y_MAX = 0.5 / ASPECT          # keeps 1 horizontal unit visually == 1 vertical

X_SOURCE = 0.08               # particle source, center-left
X_SLIT = 1.0 / 3.0            # barrier, 1/3 from the left edge
X_DETECTOR = 1.07             # detector bank, shifted right by the fringe-curve
                              # height (0.17) from its former 0.9 position

SLIT_SEP = 0.09               # vertical separation d between the two slits
SLIT_HALF = 0.018             # half-height of each slit opening
SLIT_Y = SLIT_SEP / 2         # slit centers at +/- SLIT_Y


# ---------------------------------------------------------------------------
# Fringe pattern: same formulation as double_slit.py's comparison figure,
#   I(x_norm) = cos^2(phi/2) * sinc^2(slit_ratio * x_norm),   phi = 2*pi*x_norm/FRINGE_DX
# but parameterized so the geometry is explicit:
#
#   - cos^2 peaks (bright fringes) sit at x_norm = n * FRINGE_DX, integer n.
#   - We want FIVE central peaks (n = 0, +/-1, +/-2) before the envelope null,
#     so the null is placed just past the 2nd side peak at x_norm = 2.5*FRINGE_DX.
#     np.sinc (normalized) has its first zero at argument 1, so
#       slit_ratio * (2.5*FRINGE_DX) = 1  ->  slit_ratio = 1/(2.5*FRINGE_DX).
#   - The pattern then continues ~1.6 more fringes past the null (low amplitude,
#     the first sinc side lobe), so we plot out to x_norm = (2.5+1.6)*FRINGE_DX.
#
# x_norm is dimensionless; it is mapped to a vertical pixel position below.
# ---------------------------------------------------------------------------
FRINGE_DX = 0.10                           # peak-to-peak spacing in x_norm
CENTRAL_PEAKS_HALF = 2                     # peaks each side of center (total 5)
NULL_XN = (CENTRAL_PEAKS_HALF + 0.5) * FRINGE_DX   # envelope first null
SLIT_RATIO = 1.0 / NULL_XN                 # places sinc^2 null exactly there
EXTRA_FRINGES = 1.6                        # fringes drawn beyond the null
PLOT_XN = NULL_XN + EXTRA_FRINGES * FRINGE_DX      # half-extent plotted

# Aesthetic softening of the envelope: raising sinc^2 to a power < 1 keeps its
# zeros (the null) exactly in place but flattens the decay between them, so the
# outer central fringes and the post-null side lobe are less crushed. 1.0 is
# the true sinc^2; smaller values lift the outer fringes.
ENVELOPE_SOFTEN = 0.6

# Vertical scale: map the plotted x_norm half-extent to the detector's half
# height so the whole pattern fits the bank.
XN_TO_Y = 1.0 / PLOT_XN                     # multiply x_norm by (Y_MAX*this)


def fringe_intensity_xn(x_norm):
    """Normalized intensity as a function of x_norm (dimensionless)."""
    phi = 2 * np.pi * x_norm / FRINGE_DX
    interference = np.cos(phi / 2) ** 2
    envelope = (np.sinc(SLIT_RATIO * x_norm) ** 2) ** ENVELOPE_SOFTEN
    return interference * envelope


# ---------------------------------------------------------------------------
# Figure (16:9)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12.8, 7.2))
# x-axis ends just past the fringe curve's max reach
# (curve_base + curve_span ~= 1.255 with the detector shifted to x=1.07) so the
# curve fits without clipping.
ax.set_xlim(0, 1.27)
ax.set_ylim(-Y_MAX, Y_MAX)
ax.axis('off')

ax.set_title("Double Slit Experiment",
             fontsize=20, fontweight='bold', pad=12)


# ---------------------------------------------------------------------------
# 1. Particle source (half the previous size, still red)
# ---------------------------------------------------------------------------
SOURCE_R = 0.014
ax.add_patch(Circle((X_SOURCE, 0.0), SOURCE_R, color='#d62728', zorder=5))
for ang in np.linspace(-0.5, 0.5, 5):       # little emission ticks
    ax.plot([X_SOURCE, X_SOURCE + 0.035],
            [0.0, 0.035 * np.tan(ang)],
            color='#d62728', lw=1.0, alpha=0.5, zorder=4)
ax.text(X_SOURCE, -0.055, "source", ha='center', va='top',
        fontsize=12, color='#d62728', fontweight='bold')


# ---------------------------------------------------------------------------
# 2. Barrier with two slits
# ---------------------------------------------------------------------------
bar_w = 0.012
bar_color = '#333333'

segments = [
    (Y_MAX, SLIT_Y + SLIT_HALF),                 # top segment
    (SLIT_Y - SLIT_HALF, -SLIT_Y + SLIT_HALF),   # middle segment
    (-SLIT_Y - SLIT_HALF, -Y_MAX),               # bottom segment
]
for y_top, y_bot in segments:
    ax.add_patch(Rectangle((X_SLIT - bar_w / 2, y_bot),
                           bar_w, y_top - y_bot,
                           color=bar_color, zorder=5))

ax.text(X_SLIT, -Y_MAX - 0.015, "barrier", ha='center', va='top',
        fontsize=12, color=bar_color, fontweight='bold')


# ---------------------------------------------------------------------------
# 2b. Slit separation indicator: a double-headed arrow between slit centers,
#     offset to the left of the barrier, labeled d.
# ---------------------------------------------------------------------------
d_x = X_SLIT - 0.05
ax.annotate("", xy=(d_x, SLIT_Y), xytext=(d_x, -SLIT_Y),
            arrowprops=dict(arrowstyle='<->', color=bar_color, lw=1.3))
# Thin guide ticks from the arrow ends across to the slit centers.
for sy in (SLIT_Y, -SLIT_Y):
    ax.plot([d_x, X_SLIT - bar_w / 2], [sy, sy],
            color=bar_color, lw=0.6, alpha=0.5, zorder=4)
ax.text(d_x - 0.012, 0.0, r"$d$", ha='right', va='center',
        fontsize=14, color=bar_color)


# ---------------------------------------------------------------------------
# 3. Rays: source -> each slit, and each slit -> detector bank (fanned)
# ---------------------------------------------------------------------------
for sy in (SLIT_Y, -SLIT_Y):
    ax.plot([X_SOURCE, X_SLIT], [0.0, sy],
            color='#ff7f0e', lw=1.2, alpha=0.6, zorder=3)

for sy in (SLIT_Y, -SLIT_Y):
    for ty in np.linspace(-0.85 * Y_MAX, 0.85 * Y_MAX, 9):
        ax.plot([X_SLIT, X_DETECTOR], [sy, ty],
                color='#1f77b4', lw=0.5, alpha=0.16, zorder=2)


# ---------------------------------------------------------------------------
# 4. Detector bank: discrete little BLACK boxes, each open on the LEFT side
#    (particles impinge left -> right). Three sides drawn, left edge omitted.
# ---------------------------------------------------------------------------
N_DET = 42
edges = np.linspace(-Y_MAX, Y_MAX, N_DET + 1)
centers = 0.5 * (edges[:-1] + edges[1:])
cell_h = (edges[1] - edges[0]) * 0.82         # small gap between boxes
box_w = 0.014                                 # half the previous width (0.028)

det_color = 'black'
det_lw = 1.4

for yc in centers:
    x0 = X_DETECTOR - box_w / 2
    x1 = X_DETECTOR + box_w / 2
    y0 = yc - cell_h / 2
    y1 = yc + cell_h / 2
    # Draw top, right, bottom -> leave the left edge OPEN.
    ax.plot([x0, x1], [y1, y1], color=det_color, lw=det_lw, zorder=6)  # top
    ax.plot([x1, x1], [y0, y1], color=det_color, lw=det_lw, zorder=6)  # right
    ax.plot([x0, x1], [y0, y0], color=det_color, lw=det_lw, zorder=6)  # bottom

ax.text(X_DETECTOR, -Y_MAX - 0.015, "detectors", ha='center', va='top',
        fontsize=12, color=det_color, fontweight='bold')


# ---------------------------------------------------------------------------
# 5. Fringe pattern (sinc^2-enveloped cos^2) against the detector bank.
#    Plotted to the RIGHT of the boxes as a sideways intensity profile. The
#    full plotted x_norm range [-PLOT_XN, PLOT_XN] maps onto [-Y_MAX, Y_MAX],
#    so five central peaks sit near center, the envelope null is a dark gap,
#    and ~1.6 faint fringes trail off toward the top/bottom edges.
# ---------------------------------------------------------------------------
xn = np.linspace(-PLOT_XN, PLOT_XN, 1200)
ys = xn * XN_TO_Y * Y_MAX                      # x_norm -> vertical position
Is = fringe_intensity_xn(xn)

curve_base = X_DETECTOR + box_w / 2 + 0.008
curve_span = 0.17                              # fringe height (2x previous 0.085)
ax.plot(curve_base + curve_span * Is, ys,
        color='#d62728', lw=2.0, zorder=6)     # RED interference curve
ax.fill_betweenx(ys, curve_base, curve_base + curve_span * Is,
                 color='#d62728', alpha=0.15, zorder=5)


# ---------------------------------------------------------------------------
# 6. Optional propagation-line overlays (--center / --null).
#
# A fringe feature at dimensionless position x_norm maps to detector height
#   y = x_norm * XN_TO_Y * Y_MAX   (same mapping used for the red curve).
# Lines run from each slit center (X_SLIT, +/-SLIT_Y) to the detector face
# (x = X_DETECTOR - box_w/2) at that height.
#
#   - Central bright fringe (constructive): x_norm = 0  ->  y = 0.
#   - First cos^2 dark fringe (destructive): cos^2 zeros are at
#     x_norm = (n + 0.5)*FRINGE_DX, so the first is x_norm = 0.5*FRINGE_DX.
# ---------------------------------------------------------------------------
def xn_to_y(x_norm):
    return x_norm * XN_TO_Y * Y_MAX


det_face_x = X_DETECTOR - box_w / 2


# Wave overlay parameters. NOTE on honesty vs. legibility: the TRUE path-length
# difference at the null is only ~0.004 figure units against ~0.73-long lines,
# so a literally-scaled wavelength would pack ~86 cycles per line and render as
# an unreadable black blur. A schematic therefore EXAGGERATES: we pick a visible
# wavelength (a handful of cycles) and impose the phase relationship explicitly
# -- both waves in phase for the center (crest meets crest, constructive), and
# one wave shifted by half a cycle for the null (crest meets trough,
# destructive). The wavelength is uniform; only the end-phase relationship
# carries the physics.
# WAVE_CYCLES is a QUARTER-integer so sin(2*pi*cycles*t) lands on an EXTREMUM
# (not a zero crossing) at the detector end t=1. n + 0.25 ends at +max;
# n + 0.75 ends at -max. Center uses the same count on both lines (matching
# extrema -> double max/min, constructive); null makes the lower line carry
# half a cycle more so the two lines end on OPPOSITE extrema (destructive).
WAVE_CYCLES = 7.25         # ends at +max at the detector
WAVE_AMP = 0.013           # transverse amplitude (figure units)


def draw_wave_along(sy, y_target, cycles, color='black'):
    """Thin sinusoid along the slit->target segment.

    Both waves START in phase at the slit (phase 0 at s=0). `cycles` is the
    number of full wavelengths packed along the line, so a line with more
    cycles accumulates more phase by the target. Transverse displacement =
    WAVE_AMP * sin(2*pi * cycles * (s/L)), s from slit to target.
    """
    x0, y0 = X_SLIT, sy
    x1, y1 = det_face_x, y_target
    L = np.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L  # along the segment
    px, py = -uy, ux                        # perpendicular (transverse)

    t = np.linspace(0, 1, 600)              # fractional arc length
    offset = WAVE_AMP * np.sin(2 * np.pi * cycles * t)
    bx, by = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
    ax.plot(bx + px * offset, by + py * offset,
            color=color, lw=0.8, alpha=0.9, zorder=8)


def draw_propagation_lines(y_target, color, label, wave_cycles=None):
    """Draw a line from each slit to (det_face_x, y_target), plus a marker.

    wave_cycles, if given, is (cycles_upper, cycles_lower): the number of wave
    cycles along the upper- and lower-slit lines. Both waves start in phase at
    the slit; differing cycle counts make them accumulate different phase and
    arrive with a chosen relationship at the target.
    """
    slit_ys = (SLIT_Y, -SLIT_Y)
    for i, sy in enumerate(slit_ys):
        ax.plot([X_SLIT, det_face_x], [sy, y_target],
                color=color, lw=2.2, alpha=0.9, zorder=7)
        if wave_cycles is not None:
            draw_wave_along(sy, y_target, wave_cycles[i])
    ax.scatter([det_face_x], [y_target], color=color, s=45, zorder=8)
    ax.text(curve_base + curve_span + 0.02, y_target, label,
            ha='left', va='center', fontsize=11, color=color,
            fontweight='bold')


if args.center:
    # Central bright fringe at y = 0: both waves IN PHASE, same wavelength,
    # equal paths -> arrive crest-to-crest -> constructive.
    draw_propagation_lines(xn_to_y(0.0), '#2ca02c',
                           "constructive\n(in phase)",
                           wave_cycles=(WAVE_CYCLES, WAVE_CYCLES))

if args.null:
    # First cos^2 dark fringe: both waves START in phase at the slits, but the
    # LOWER line carries half a cycle more, so it ends on the OPPOSITE extremum
    # (-max) from the upper line (+max) -> crest-to-trough at the null ->
    # destructive.
    draw_propagation_lines(xn_to_y(0.5 * FRINGE_DX), '#1f77b4',
                           "destructive\n($\\lambda/2$ out of phase at null)",
                           wave_cycles=(WAVE_CYCLES, WAVE_CYCLES + 0.5))


# ---------------------------------------------------------------------------
# Save (filename reflects which overlays are active)
# ---------------------------------------------------------------------------
suffix = ''
if args.center:
    suffix += '_center'
if args.null:
    suffix += '_null'

os.makedirs('images', exist_ok=True)
out = f'images/double_slit_diagram{suffix}.png'
fig.savefig(out, dpi=150, bbox_inches='tight')
print(f"Saved: {out}")
