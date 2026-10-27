"""
C_to_Bloch: Two complex unit discs (alpha, beta) alongside the Bloch sphere.

Layout:
  Left column  : two complex unit discs stacked vertically.
                   top disc  = alpha  (amplitude of |0>)
                   bottom disc = beta (amplitude of |1>)
  Right side   : Bloch sphere with the state as a green vector.
  Bottom center: numeric readout of alpha and beta, plus a caption line.

The animation steps through a sequence of states with smooth linear
interpolation between them (no jumps). Each keyframe has a hold "duration"
during which the state rests, preceded by a smooth transition from the
previous keyframe.

Keyframes are given in polar form (magnitude and angle of each coefficient).
Interpolation moves magnitudes linearly and angles along the shortest arc, so
a pure phase change keeps a coefficient on its circle and the green Bloch
vector stays on the sphere surface. An equal angular shift of both phases is a
global phase and leaves the Bloch point fixed.

Reuses the Bloch-sphere drawing and render scaffolding from bloch_animation.py.

Requirements: pip install matplotlib numpy
Usage: python C_to_Bloch.py
Output: C_to_Bloch.mp4 (or .gif if ffmpeg unavailable)
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.patches import Circle


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
FPS = 30
TRANSITION_SECONDS = 2.5  # smooth glide between consecutive keyframes

# Camera azimuth (degrees). The view holds at AZIM_START until the transition
# INTO keyframe AZIM_SWEEP_KEYFRAME, during which it eases from AZIM_START to
# AZIM_END (in lockstep with that transition), then holds at AZIM_END.
AZIM_START = 30.0               # ~pi/6
AZIM_END = 75.0                 # 5*pi/12
AZIM_SWEEP_KEYFRAME = 4         # first "phase separation -> 2pi/3" keyframe


# ---------------------------------------------------------------------------
# State sequence (POLAR form).
#
# Each entry: (r_a, phi_a, r_b, phi_b, caption, hold_seconds)
#   alpha = r_a * exp(i phi_a)   (amplitude of |0>)
#   beta  = r_b * exp(i phi_b)   (amplitude of |1>)
# hold_seconds is how long the state rests AFTER arriving at it.
# A smooth transition of TRANSITION_SECONDS precedes every keyframe except
# the very first (which simply appears and holds).
#
# Interpolation (see build_schedule) moves the two magnitudes linearly and
# the two angles along their shortest arc. Holding a magnitude fixed while an
# angle changes therefore keeps that coefficient on its circle, so the Bloch
# vector stays glued to the sphere surface. A global phase = equal angular
# shift of BOTH phi_a and phi_b leaves the Bloch point unmoved.
# ---------------------------------------------------------------------------
INV_SQRT2 = np.sqrt(2) / 2

state_sequence = [
    # r_a,        phi_a,       r_b,        phi_b,                caption, hold
    (1.0, 0.0, 0.0, 0.0,
        r"Ground state $|0\rangle$", 0.5),
    (0.0, 0.0, 1.0, 0.0,
        r"Transition to state $|1\rangle$", 0.5),
    (0.0, 0.0, 1.0, 0.0,
        r"state $|1\rangle$", 0.5),
    (INV_SQRT2, 0.0, INV_SQRT2, 0.0,
        r"$\alpha = \beta = 1/\sqrt{2}$: norm must always be 1", 0.5),
    (INV_SQRT2, 0.0, INV_SQRT2, 2 * np.pi / 3,
        r"phase separation $|0\rangle$ to $|1\rangle$: $2\pi/3$", 0.5),
    (INV_SQRT2, 0.0, INV_SQRT2, 2 * np.pi / 3,
        r"phase separation $|0\rangle$ to $|1\rangle$: $2\pi/3$", 0.5),
    # Grow alpha to 0.90, beta shrinks to keep the norm at 1.
    (0.90, 0.0, np.sqrt(1 - 0.90 ** 2), 2 * np.pi / 3,
        r"$\alpha$ increase, $\beta$ decrease magnitude", 0.5),
    (0.90, 0.0, np.sqrt(1 - 0.90 ** 2), 2 * np.pi / 3,
        r"$\alpha$ increase, $\beta$ decrease magnitude", 0.5),
    # Global phase: both angles shift (phi_a: 0 -> pi/2, phi_b: 2pi/3 -> 7pi/6,
    # an equal +pi/2 shift of each), magnitudes fixed. Bloch point unchanged.
    (0.90, np.pi / 2, np.sqrt(1 - 0.90 ** 2), 7 * np.pi / 6,
        "Global phase offset (no physical effect; Bloch location unchanged)",
        0.5),
    (0.90, np.pi / 2, np.sqrt(1 - 0.90 ** 2), 7 * np.pi / 6,
        "Global phase offset (no physical effect; Bloch location unchanged)",
        0.5),
]


# ---------------------------------------------------------------------------
# State -> Bloch mapping (from bloch_animation.py)
# ---------------------------------------------------------------------------
def normalize(alpha, beta):
    n = np.sqrt(np.abs(alpha) ** 2 + np.abs(beta) ** 2)
    if n < 1e-12:
        return 1.0 + 0j, 0.0 + 0j
    return alpha / n, beta / n


def state_to_bloch(alpha, beta):
    """Convert a 2-element complex state vector to (x, y, z) on Bloch sphere."""
    a, b = normalize(alpha, beta)
    x = 2 * np.real(np.conj(a) * b)
    y = 2 * np.imag(np.conj(a) * b)
    z = np.abs(a) ** 2 - np.abs(b) ** 2
    return np.array([x, y, z])


# ---------------------------------------------------------------------------
# Build the per-frame schedule (polar interpolation).
#
# For keyframe k > 0 we emit TRANSITION frames (interpolating from
# keyframe k-1 to keyframe k) followed by HOLD frames at keyframe k.
# Keyframe 0 just holds.
#
# Magnitudes interpolate linearly; angles follow the shortest arc so a jump
# such as 0 -> 2pi/3 sweeps the short way at (optionally) constant radius.
# ---------------------------------------------------------------------------
def short_arc(a0, a1):
    """Shortest signed angular delta from a0 to a1, in (-pi, pi]."""
    d = (a1 - a0) % (2 * np.pi)
    if d > np.pi:
        d -= 2 * np.pi
    return d


def build_schedule():
    """Return a list of (alpha, beta, caption, azim) tuples, one per frame.

    `azim` is the camera azimuth (degrees). It holds at AZIM_START until the
    transition into keyframe AZIM_SWEEP_KEYFRAME, eases to AZIM_END across that
    transition (same cosine ease as the state), and holds at AZIM_END after.
    """
    frames = []
    n_trans = int(round(TRANSITION_SECONDS * FPS))

    for k, (ra, pa, rb, pb, caption, hold) in enumerate(state_sequence):
        n_hold = int(round(hold * FPS))
        alpha = ra * np.exp(1j * pa)
        beta = rb * np.exp(1j * pb)

        # Azimuth value held during/after this keyframe: once we have reached
        # (or passed) the sweep keyframe, the camera rests at AZIM_END.
        azim_hold = AZIM_END if k >= AZIM_SWEEP_KEYFRAME else AZIM_START

        if k == 0:
            for _ in range(n_hold):
                frames.append((alpha, beta, caption, azim_hold))
            continue

        ra0, pa0, rb0, pb0, _, _ = state_sequence[k - 1]
        d_pa = short_arc(pa0, pa)
        d_pb = short_arc(pb0, pb)

        sweep_here = (k == AZIM_SWEEP_KEYFRAME)

        # Smooth transition: cosine ease-in/out on magnitudes and angles.
        for i in range(n_trans):
            t = (i + 1) / n_trans
            s = 0.5 - 0.5 * np.cos(t * np.pi)
            ra_t = (1 - s) * ra0 + s * ra
            rb_t = (1 - s) * rb0 + s * rb
            pa_t = pa0 + s * d_pa
            pb_t = pb0 + s * d_pb
            azim_t = (AZIM_START + s * (AZIM_END - AZIM_START)
                      if sweep_here else azim_hold)
            frames.append((ra_t * np.exp(1j * pa_t),
                           rb_t * np.exp(1j * pb_t),
                           caption, azim_t))

        for _ in range(n_hold):
            frames.append((alpha, beta, caption, azim_hold))

    return frames


schedule = build_schedule()
total_frames = len(schedule)


# ---------------------------------------------------------------------------
# Figure setup
#   Left column : two disc axes stacked (top=alpha, bottom=beta)
#   Right       : Bloch sphere (3D)
#   Bottom      : readout axis spanning the width
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(16, 9))

# gridspec: 2 rows for the discs on the left, one tall 3D axis on the right,
# and a thin readout strip across the bottom.
gs = fig.add_gridspec(
    nrows=3, ncols=2,
    width_ratios=[1.0, 2.0],
    height_ratios=[1.0, 1.0, 0.28],
    left=0.04, right=0.98, bottom=0.04, top=0.94,
    wspace=0.10, hspace=0.25,
)

ax_alpha = fig.add_subplot(gs[0, 0])          # top-left disc: alpha
ax_beta = fig.add_subplot(gs[1, 0])           # bottom-left disc: beta
ax_bloch = fig.add_subplot(gs[0:2, 1], projection='3d')  # right: Bloch sphere
ax_readout = fig.add_subplot(gs[2, :])        # bottom strip: readout + caption


# ---------------------------------------------------------------------------
# Bloch sphere drawing (adapted from bloch_animation.py)
# ---------------------------------------------------------------------------
def draw_bloch_sphere(ax):
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color='steelblue', alpha=0.2, linewidth=0.5)

    ax.plot([-1.3, 1.3], [0, 0], [0, 0], 'gray', linewidth=1.0, alpha=0.6)
    ax.plot([0, 0], [-1.3, 1.3], [0, 0], 'gray', linewidth=1.0, alpha=0.6)
    ax.plot([0, 0], [0, 0], [-1.3, 1.3], 'gray', linewidth=1.0, alpha=0.6)

    ax.text(1.4, 0, 0, "x", color='gray', fontsize=10)
    ax.text(0, 1.4, 0, "y", color='gray', fontsize=10)
    ax.text(0, 0, 1.22, "|0>", color='black', fontsize=12, fontweight='bold')
    ax.text(0, 0, -1.28, "|1>", color='black', fontsize=12, fontweight='bold')
    ax.text(1.2, 0, 0.08, "|+>", color='darkgreen', fontsize=10)
    ax.text(-1.2, 0, 0.08, "|->", color='darkgreen', fontsize=10)
    ax.text(0, 1.2, 0.08, "|+i>", color='purple', fontsize=10)
    ax.text(0, -1.2, 0.08, "|-i>", color='purple', fontsize=10)

    t = np.linspace(0, 2 * np.pi, 80)
    ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), 'gray',
            linewidth=0.8, alpha=0.4)
    ax.plot(np.cos(t), np.zeros_like(t), np.sin(t), 'gray',
            linewidth=0.5, alpha=0.25)
    ax.plot(np.zeros_like(t), np.cos(t), np.sin(t), 'gray',
            linewidth=0.5, alpha=0.25)


# ---------------------------------------------------------------------------
# Complex-disc drawing
# ---------------------------------------------------------------------------
def draw_disc(ax, value, label, color):
    """Draw a complex unit disc with a phasor for `value` (a complex number)."""
    ax.clear()
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect('equal')
    ax.set_axis_off()

    # Unit circle boundary.
    ax.add_patch(Circle((0, 0), 1.0, fill=False, edgecolor='steelblue',
                        linewidth=1.5, alpha=0.8))
    # Faint inner guide circle at radius 0.5.
    ax.add_patch(Circle((0, 0), 0.5, fill=False, edgecolor='steelblue',
                        linewidth=0.6, alpha=0.3, linestyle='--'))

    # Real/imaginary axes.
    ax.plot([-1.15, 1.15], [0, 0], 'gray', linewidth=0.8, alpha=0.5)
    ax.plot([0, 0], [-1.15, 1.15], 'gray', linewidth=0.8, alpha=0.5)
    ax.text(1.18, 0.0, "Re", color='gray', fontsize=8, va='center')
    ax.text(0.0, 1.18, "Im", color='gray', fontsize=8, ha='center')

    # Phasor from origin to the complex value.
    re, im = np.real(value), np.imag(value)
    ax.annotate("", xy=(re, im), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=2.5))
    ax.scatter([re], [im], color=color, s=70, zorder=5)

    ax.set_title(label, fontsize=14, fontweight='bold', color=color, pad=6)


# ---------------------------------------------------------------------------
# Readout strip
# ---------------------------------------------------------------------------
def fmt_complex(z):
    re, im = np.real(z), np.imag(z)
    sign = '+' if im >= 0 else '-'
    return f"{re:+.2f} {sign} {abs(im):.2f}i"


def draw_readout(ax, alpha, beta, caption):
    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()

    ax.text(0.5, 0.72,
            rf"$\alpha$ = {fmt_complex(alpha)}        "
            rf"$\beta$ = {fmt_complex(beta)}",
            fontsize=15, ha='center', va='center')
    ax.text(0.5, 0.26, caption, fontsize=15, ha='center', va='center',
            style='italic', color='#333333')


# ---------------------------------------------------------------------------
# Main update
# ---------------------------------------------------------------------------
def update(frame):
    alpha, beta, caption, azim = schedule[frame]

    # --- discs ---
    draw_disc(ax_alpha, alpha, r"$\alpha$  ($|0\rangle$ amplitude)", '#1f77b4')
    draw_disc(ax_beta, beta, r"$\beta$  ($|1\rangle$ amplitude)", '#d62728')

    # --- Bloch sphere ---
    ax_bloch.cla()
    draw_bloch_sphere(ax_bloch)
    ax_bloch.view_init(elev=18, azim=azim)

    # Zoom in ~20% (tighter limits => larger apparent sphere). Pole labels
    # sit just outside radius 1, so they stay close to the surface.
    lim = 0.82
    ax_bloch.set_xlim([-lim, lim])
    ax_bloch.set_ylim([-lim, lim])
    ax_bloch.set_zlim([-lim, lim])
    ax_bloch.set_box_aspect([1, 1, 1])
    ax_bloch.set_axis_off()

    point = state_to_bloch(alpha, beta)
    ax_bloch.quiver(0, 0, 0, point[0], point[1], point[2],
                    color='limegreen', arrow_length_ratio=0.08, linewidth=3.0)
    ax_bloch.scatter(*point, color='limegreen', s=90, zorder=5)

    # --- readout ---
    draw_readout(ax_readout, alpha, beta, caption)

    return []


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
print(f"C_to_Bloch: {total_frames} frames at {FPS} fps "
      f"({total_frames / FPS:.1f} s)")
print(f"Keyframes: {len(state_sequence)}")
for ra, pa, rb, pb, cap, hold in state_sequence:
    bloch = state_to_bloch(ra * np.exp(1j * pa), rb * np.exp(1j * pb))
    print(f"  |a|={ra:.3f} ph={pa:+.3f}  |b|={rb:.3f} ph={pb:+.3f}  "
          f"-> Bloch=({bloch[0]:+.2f},{bloch[1]:+.2f},{bloch[2]:+.2f})  "
          f"hold={hold}s")
print("Rendering...")

anim = FuncAnimation(fig, update, frames=total_frames,
                     interval=1000 // FPS, blit=False)

try:
    writer = FFMpegWriter(fps=FPS, metadata={'title': 'C discs to Bloch'})
    anim.save('media/C_to_Bloch.mp4', writer=writer)
    print("\nSaved: media/C_to_Bloch.mp4")
except Exception as e:
    print(f"\nmp4 failed ({e}). Trying gif...")
    try:
        writer = PillowWriter(fps=FPS)
        anim.save('media/C_to_Bloch.gif', writer=writer)
        print("Saved: media/C_to_Bloch.gif")
    except Exception as e2:
        print(f"gif also failed ({e2}).")
        print("Install ffmpeg: sudo apt install ffmpeg")
