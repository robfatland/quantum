"""
Bloch Sphere Animation with Circuit Diagram Playback.

Left panel: State vector on the Bloch sphere, animated gate-by-gate.
Right panel: Static quantum circuit diagram with a tracking marker
             highlighting the current gate.

Viewing angle is shallow (near the xy-plane) for better perspective
on equatorial rotations.

Requirements: pip install matplotlib numpy qiskit
Usage: python bloch_animation.py
Output: bloch_animation.mp4 (or .gif if ffmpeg unavailable)
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patches as mpatches


# --- Rotation utilities ---
def rotate_bloch_vector(vec, axis, angle):
    """Rotate vec by angle (radians) about axis using Rodrigues' formula."""
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    return vec * c + np.cross(axis, vec) * s + axis * np.dot(axis, vec) * (1 - c)


def state_to_bloch(state):
    """Convert a 2-element complex state vector to (x, y, z) on Bloch sphere."""
    alpha, beta = state[0], state[1]
    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2
    return np.array([x, y, z])


# --- Gate definitions ---
# (label, description, bloch_rotation_axis, bloch_rotation_angle)
H_axis = np.array([1, 0, 1]) / np.sqrt(2)

gate_sequence = [
    ("H",      "Hadamard: 180° about (x+z)/√2", H_axis,             np.pi),
    ("S",      "S gate: 90° about z-axis",       np.array([0,0,1]), np.pi/2),
    ("H",      "Hadamard: 180° about (x+z)/√2", H_axis,             np.pi),
    ("T",      "T gate: 45° about z-axis",       np.array([0,0,1]), np.pi/4),
    ("X",      "Pauli X: 180° about x-axis",    np.array([1,0,0]), np.pi),
    ("Ry(π/3)","60° about y-axis",              np.array([0,1,0]), np.pi/3),
    ("H",      "Hadamard: 180° about (x+z)/√2", H_axis,             np.pi),
]

# --- Compute all Bloch points ---
bloch_points = [np.array([0, 0, 1.0])]  # Start at |0>

for label, desc, axis, angle in gate_sequence:
    new_point = rotate_bloch_vector(bloch_points[-1], axis, angle)
    bloch_points.append(new_point)

# --- Animation timing ---
frames_per_caption = 60
frames_per_transition = 40
frames_per_hold = 50
frames_measurement = 120

n_gates = len(gate_sequence)
total_frames = (frames_per_caption + frames_per_transition + frames_per_hold) * n_gates \
               + frames_per_caption + frames_measurement

# --- Measurement ---
final_z = bloch_points[-1][2]
prob_0 = (1 + final_z) / 2
measurement_result = 0 if prob_0 >= 0.5 else 1
measurement_bloch = np.array([0, 0, 1.0]) if measurement_result == 0 \
                    else np.array([0, 0, -1.0])


# --- Figure setup: two panels ---
fig = plt.figure(figsize=(18, 9))

# Left panel: Bloch sphere (3D)
ax_bloch = fig.add_subplot(121, projection='3d')

# Right panel: Circuit diagram (2D)
ax_circuit = fig.add_subplot(122)

fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.92, wspace=0.05)


# --- Circuit diagram drawing ---
def draw_circuit_diagram(ax, highlight_gate=-1, phase='caption'):
    """
    Draw a static single-qubit circuit diagram with gates as boxes.
    highlight_gate: index of the gate currently being applied (-1 = none).
    phase: 'caption', 'transition', 'hold', or 'meas_*'
    """
    ax.clear()
    ax.set_xlim(-0.5, n_gates + 1.5)
    ax.set_ylim(-1.5, 2.0)
    ax.set_aspect('equal')
    ax.set_axis_off()

    # Title
    ax.text((n_gates + 1) / 2, 1.8, "Circuit Diagram", fontsize=14,
            ha='center', va='center', fontweight='bold')

    # Wire
    wire_y = 0.0
    ax.plot([-0.3, n_gates + 0.8], [wire_y, wire_y], 'k-', linewidth=1.5)

    # Initial state label
    ax.text(-0.45, wire_y, "|0⟩", fontsize=13, ha='right', va='center',
            fontfamily='serif')

    # Measurement symbol at the end
    meas_x = n_gates + 0.5
    ax.plot([meas_x - 0.2, meas_x + 0.2], [wire_y - 0.3, wire_y - 0.3],
            'k-', linewidth=1.5)
    arc = np.linspace(0, np.pi, 30)
    ax.plot(meas_x + 0.2 * np.cos(arc), wire_y - 0.3 + 0.3 * np.sin(arc),
            'k-', linewidth=1.5)
    ax.plot([meas_x, meas_x + 0.15], [wire_y - 0.3, wire_y + 0.1],
            'k-', linewidth=1.5)

    # Gate boxes
    for i, (label, desc, _, _) in enumerate(gate_sequence):
        x = i + 0.5
        box_w, box_h = 0.6, 0.6

        # Determine box color
        if i == highlight_gate:
            if phase == 'transition':
                facecolor = '#90EE90'  # light green — active
            elif phase == 'hold':
                facecolor = '#D4EDDA'  # very light green — just completed
            else:
                facecolor = '#FFFACD'  # light yellow — about to start
        elif i < highlight_gate or (highlight_gate == -1 and
                                     phase in ('meas_caption', 'meas_collapse')):
            facecolor = '#E8E8E8'  # gray — completed
        else:
            facecolor = 'white'  # not yet reached

        rect = FancyBboxPatch((x - box_w/2, wire_y - box_h/2), box_w, box_h,
                              boxstyle="round,pad=0.05",
                              facecolor=facecolor, edgecolor='black',
                              linewidth=1.5)
        ax.add_patch(rect)

        # Gate label inside box
        fontsize = 11 if len(label) <= 2 else 9
        ax.text(x, wire_y, label, fontsize=fontsize,
                ha='center', va='center', fontweight='bold')

    # Tracking marker (triangle below the current gate)
    if highlight_gate >= 0:
        marker_x = highlight_gate + 0.5
        ax.plot(marker_x, wire_y - 0.55, 'v', color='red', markersize=12)
    elif phase in ('meas_caption', 'meas_collapse'):
        ax.plot(meas_x, wire_y - 0.55, 'v', color='red', markersize=12)

    # Description text below
    if highlight_gate >= 0:
        _, desc, _, _ = gate_sequence[highlight_gate]
        ax.text((n_gates + 1) / 2, -1.0, desc, fontsize=11,
                ha='center', va='center', style='italic', color='#333333')
    elif phase == 'meas_caption':
        ax.text((n_gates + 1) / 2, -1.0,
                f"Measurement: P(|0⟩)={prob_0:.2f}, P(|1⟩)={1-prob_0:.2f}",
                fontsize=11, ha='center', va='center', style='italic',
                color='#333333')
    elif phase == 'meas_collapse':
        outcome = "|0⟩" if measurement_result == 0 else "|1⟩"
        ax.text((n_gates + 1) / 2, -1.0,
                f"Collapsed to {outcome}", fontsize=11,
                ha='center', va='center', style='italic', color='red')


# --- Bloch sphere drawing ---
def draw_bloch_sphere(ax):
    """Draw wireframe sphere, axes, labels."""
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color='steelblue', alpha=0.2, linewidth=0.5)

    # Axes
    ax.plot([-1.3, 1.3], [0, 0], [0, 0], 'gray', linewidth=1.0, alpha=0.6)
    ax.plot([0, 0], [-1.3, 1.3], [0, 0], 'gray', linewidth=1.0, alpha=0.6)
    ax.plot([0, 0], [0, 0], [-1.3, 1.3], 'gray', linewidth=1.0, alpha=0.6)

    # Labels
    ax.text(1.4, 0, 0, "x", color='gray', fontsize=10)
    ax.text(0, 1.4, 0, "y", color='gray', fontsize=10)
    ax.text(0, 0, 1.5, "|0⟩", color='black', fontsize=12, fontweight='bold')
    ax.text(0, 0, -1.5, "|1⟩", color='black', fontsize=12, fontweight='bold')
    ax.text(1.2, 0, 0.08, "|+⟩", color='darkgreen', fontsize=10)
    ax.text(-1.2, 0, 0.08, "|−⟩", color='darkgreen', fontsize=10)
    ax.text(0, 1.2, 0.08, "|+i⟩", color='purple', fontsize=10)
    ax.text(0, -1.2, 0.08, "|−i⟩", color='purple', fontsize=10)

    # Equator and meridians
    t = np.linspace(0, 2*np.pi, 80)
    ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), 'gray',
            linewidth=0.8, alpha=0.4)
    ax.plot(np.cos(t), np.zeros_like(t), np.sin(t), 'gray',
            linewidth=0.5, alpha=0.25)
    ax.plot(np.zeros_like(t), np.cos(t), np.sin(t), 'gray',
            linewidth=0.5, alpha=0.25)


def draw_rotation_axis(ax, axis):
    """Highlight the rotation axis."""
    a = axis / np.linalg.norm(axis)
    ax.plot([-1.4*a[0], 1.4*a[0]],
            [-1.4*a[1], 1.4*a[1]],
            [-1.4*a[2], 1.4*a[2]],
            color='dodgerblue', linewidth=3.0, alpha=0.85)
    ax.scatter(*(1.35*a), color='dodgerblue', s=50, alpha=0.9)
    ax.scatter(*(-1.35*a), color='dodgerblue', s=50, alpha=0.9)


# --- Phase determination ---
def get_phase_info(frame):
    """Determine which phase of the animation we're in."""
    fpg = frames_per_caption + frames_per_transition + frames_per_hold
    if frame < n_gates * fpg:
        gate_idx = frame // fpg
        local_frame = frame % fpg
        if local_frame < frames_per_caption:
            return ('caption', gate_idx, local_frame / frames_per_caption)
        elif local_frame < frames_per_caption + frames_per_transition:
            t = (local_frame - frames_per_caption) / frames_per_transition
            return ('transition', gate_idx, t)
        else:
            return ('hold', gate_idx, 0)
    else:
        meas_frame = frame - n_gates * fpg
        if meas_frame < frames_per_caption:
            return ('meas_caption', n_gates, meas_frame / frames_per_caption)
        else:
            t = (meas_frame - frames_per_caption) / \
                max(1, frames_measurement - frames_per_caption)
            return ('meas_collapse', n_gates, min(t, 1.0))


# --- Azimuth schedule ---
azimuth_schedule = [
    (15, 20),
    (20, 45),
    (20, 25),
    (25, 35),
    (35, 55),
    (75, 80),
    (105, 135),
    (135, 60),
]

current_trail = []


def compute_azimuth(frame):
    """Compute camera azimuth for current frame."""
    fpg = frames_per_caption + frames_per_transition + frames_per_hold
    if frame < n_gates * fpg:
        gate_idx = frame // fpg
        local_frame = frame % fpg
        if local_frame < frames_per_caption:
            if gate_idx == 0:
                prev_end = azimuth_schedule[0][0]
            else:
                prev_end = azimuth_schedule[gate_idx - 1][1]
            seg_start = azimuth_schedule[gate_idx][0]
            cap_t = local_frame / frames_per_caption
            cap_t = 0.5 - 0.5 * np.cos(cap_t * np.pi)
            return prev_end + (seg_start - prev_end) * cap_t
        else:
            seg = azimuth_schedule[gate_idx]
            progress = (local_frame - frames_per_caption) / \
                       (frames_per_transition + frames_per_hold)
            return seg[0] + (seg[1] - seg[0]) * progress
    else:
        seg = azimuth_schedule[-1]
        meas_frame = frame - n_gates * fpg
        if meas_frame < frames_per_caption:
            prev_end = azimuth_schedule[-2][1]
            cap_t = meas_frame / frames_per_caption
            cap_t = 0.5 - 0.5 * np.cos(cap_t * np.pi)
            return prev_end + (seg[0] - prev_end) * cap_t
        else:
            t = (meas_frame - frames_per_caption) / max(1, frames_measurement)
            return seg[0] + (seg[1] - seg[0]) * t


# --- Main update function ---
def update(frame):
    global current_trail
    ax_bloch.cla()
    draw_bloch_sphere(ax_bloch)

    azim = compute_azimuth(frame)
    # Shallow elevation: closer to the xy-plane
    ax_bloch.view_init(elev=12, azim=azim)

    ax_bloch.set_xlim([-1.0, 1.0])
    ax_bloch.set_ylim([-1.0, 1.0])
    ax_bloch.set_zlim([-1.0, 1.0])
    ax_bloch.set_box_aspect([1, 1, 1])
    ax_bloch.set_axis_off()

    phase, gate_idx, t = get_phase_info(frame)

    # --- Update Bloch sphere ---
    if phase == 'caption':
        point = bloch_points[gate_idx]
        label, desc, axis, angle = gate_sequence[gate_idx]
        ax_bloch.set_title(f"Next: {label}\n{desc}", fontsize=13, pad=10)
        draw_rotation_axis(ax_bloch, axis)
        current_trail = []

    elif phase == 'transition':
        start = bloch_points[gate_idx]
        label, _, axis, angle = gate_sequence[gate_idx]
        partial_angle = angle * t
        point = rotate_bloch_vector(start, axis, partial_angle)
        ax_bloch.set_title(f"Applying {label}...", fontsize=13, pad=10)
        draw_rotation_axis(ax_bloch, axis)
        current_trail = [rotate_bloch_vector(start, axis, angle * s)
                         for s in np.linspace(0, t, 30)]
        trail = np.array(current_trail)
        ax_bloch.plot(trail[:,0], trail[:,1], trail[:,2],
                      'limegreen', alpha=0.6, linewidth=2.0)

    elif phase == 'hold':
        point = bloch_points[gate_idx + 1]
        label, desc, _, _ = gate_sequence[gate_idx]
        ax_bloch.set_title(f"After {label}", fontsize=13, pad=10)
        if len(current_trail) > 0:
            trail = np.array(current_trail)
            ax_bloch.plot(trail[:,0], trail[:,1], trail[:,2],
                          'limegreen', alpha=0.4, linewidth=1.5)

    elif phase == 'meas_caption':
        point = bloch_points[-1]
        ax_bloch.set_title(f"Measurement in Z-basis\nP(|0⟩)={prob_0:.2f}",
                           fontsize=13, pad=10)
        draw_rotation_axis(ax_bloch, np.array([0, 0, 1.0]))
        current_trail = []

    elif phase == 'meas_collapse':
        start = bloch_points[-1]
        end = measurement_bloch
        dot = np.clip(np.dot(start, end), -1.0, 1.0)
        omega = np.arccos(dot)
        if omega < 1e-10:
            point = end
        else:
            point = (np.sin((1-t)*omega)/np.sin(omega)) * start + \
                    (np.sin(t*omega)/np.sin(omega)) * end
        outcome = "|0⟩" if measurement_result == 0 else "|1⟩"
        color = 'red' if t > 0.8 else 'black'
        ax_bloch.set_title(f"Collapse → {outcome}", fontsize=14, pad=10,
                           color=color)
        draw_rotation_axis(ax_bloch, np.array([0, 0, 1.0]))
    else:
        point = bloch_points[0]

    # State vector arrow
    ax_bloch.quiver(0, 0, 0, point[0], point[1], point[2],
                    color='limegreen', arrow_length_ratio=0.07, linewidth=3.0)
    ax_bloch.scatter(*point, color='limegreen', s=80, zorder=5)

    # History dots
    n_hist = min(gate_idx + 1, len(bloch_points))
    if phase in ('hold', 'caption'):
        n_hist = gate_idx + 1
    for i in range(n_hist):
        ax_bloch.scatter(*bloch_points[i], color='gray', s=20, alpha=0.4)

    # --- Update circuit diagram ---
    if phase in ('caption', 'transition', 'hold'):
        draw_circuit_diagram(ax_circuit, highlight_gate=gate_idx, phase=phase)
    elif phase == 'meas_caption':
        draw_circuit_diagram(ax_circuit, highlight_gate=-1, phase='meas_caption')
    elif phase == 'meas_collapse':
        draw_circuit_diagram(ax_circuit, highlight_gate=-1, phase='meas_collapse')
    else:
        draw_circuit_diagram(ax_circuit, highlight_gate=-1, phase='caption')

    return []


# --- Render ---
print(f"Generating animation: {total_frames} frames")
print(f"Gate sequence: {' -> '.join(g[0] for g in gate_sequence)} -> Measure")
print("Bloch points:")
print(f"  Start: |0> = (0, 0, 1)")
for i, (label, _, axis, angle) in enumerate(gate_sequence):
    b = bloch_points[i+1]
    ax_str = f"({axis[0]:.2f},{axis[1]:.2f},{axis[2]:.2f})"
    print(f"  {label}: {np.degrees(angle):.0f}° about {ax_str} "
          f"-> ({b[0]:.3f},{b[1]:.3f},{b[2]:.3f})")
print(f"Measurement: P(|0>)={prob_0:.3f}, outcome shown: |{measurement_result}>")
print(f"Elevation: 12° (shallow, near xy-plane)")
print("Rendering...")

anim = FuncAnimation(fig, update, frames=total_frames, interval=100, blit=False)

try:
    writer = FFMpegWriter(fps=10, metadata={'title': 'Bloch Sphere + Circuit'})
    anim.save('media/bloch_animation.mp4', writer=writer)
    print("\nSaved: media/bloch_animation.mp4")
except Exception as e:
    print(f"\nmp4 failed ({e}). Trying gif...")
    try:
        writer = PillowWriter(fps=10)
        anim.save('media/bloch_animation.gif', writer=writer)
        print("Saved: media/bloch_animation.gif")
    except Exception as e2:
        print(f"gif also failed ({e2}).")
        print("Install ffmpeg: sudo apt install ffmpeg")
