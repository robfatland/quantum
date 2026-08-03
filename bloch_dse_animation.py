"""
Bloch Sphere Animation: H-P(phi)-H-M for the Double-Slit Experiment.

Left panel: State vector on the Bloch sphere, animated gate-by-gate.
Right panel: cos^2(phi/2) fringe pattern with measurement dots appearing.

Animates three times with different phase values:
  phi = pi/12  -> nearly constructive (state near |0>)
  phi = pi/3   -> partial interference
  phi = 3pi/4  -> mostly destructive (state near |1>)

Requirements: pip install matplotlib numpy
Usage: python bloch_dse_animation.py
Output: bloch_dse_animation.mp4 (or .gif if ffmpeg unavailable)
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter


# --- Rotation utilities ---
def rotate_bloch_vector(vec, axis, angle):
    """Rotate vec by angle (radians) about axis using Rodrigues' formula."""
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    return vec * c + np.cross(axis, vec) * s + axis * np.dot(axis, vec) * (1 - c)


# --- Bloch sphere drawing ---
def _draw_h_axis_crosshairs(ax):
    """Draw crosshair markers where the H-gate rotation axis pierces the sphere.

    The H axis is (1,0,1)/sqrt(2), colatitude 45 deg, azimuth 0.
    Each crosshair is a small + made of a longitudinal and latitudinal arc segment
    of +/- 4 degrees, drawn at both poles of the axis.
    """
    h_axis_color = 'dodgerblue'
    delta = np.radians(4)  # half-extent in radians

    # H axis pierces sphere at colatitude theta0=pi/4, azimuth phi0=0
    # and antipode at colatitude pi - pi/4 = 3pi/4, azimuth pi
    poles = [
        (np.pi / 4, 0.0),       # +H pole
        (3 * np.pi / 4, np.pi), # -H pole (antipodal)
    ]

    for theta0, phi0 in poles:
        # Longitudinal segment: vary theta at fixed phi
        th = np.linspace(theta0 - delta, theta0 + delta, 20)
        x_lon = np.sin(th) * np.cos(phi0)
        y_lon = np.sin(th) * np.sin(phi0)
        z_lon = np.cos(th)
        ax.plot(x_lon, y_lon, z_lon, color=h_axis_color, linewidth=2.5, alpha=0.9)

        # Latitudinal segment: vary phi at fixed theta
        ph = np.linspace(phi0 - delta / np.sin(theta0),
                         phi0 + delta / np.sin(theta0), 20)
        x_lat = np.sin(theta0) * np.cos(ph)
        y_lat = np.sin(theta0) * np.sin(ph)
        z_lat = np.cos(theta0) * np.ones_like(ph)
        ax.plot(x_lat, y_lat, z_lat, color=h_axis_color, linewidth=2.5, alpha=0.9)


def draw_bloch_sphere(ax):
    """Draw wireframe sphere with heavier lines, axes, and labels."""
    u = np.linspace(0, 2 * np.pi, 37)
    v = np.linspace(0, np.pi, 19)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color='steelblue', alpha=0.25, linewidth=1.0)

    # Axes
    ax.plot([-1.3, 1.3], [0, 0], [0, 0], 'gray', linewidth=1.0, alpha=0.6)
    ax.plot([0, 0], [-1.3, 1.3], [0, 0], 'gray', linewidth=1.0, alpha=0.6)
    ax.plot([0, 0], [0, 0], [-1.3, 1.3], 'gray', linewidth=1.0, alpha=0.6)

    # Labels
    ax.text(1.4, 0, 0, "x", color='gray', fontsize=10)
    ax.text(0, 1.4, 0, "y", color='gray', fontsize=10)
    ax.text(0, 0, 1.5, "|0>", color='black', fontsize=12, fontweight='bold')
    ax.text(0, 0, -1.5, "|1>", color='black', fontsize=12, fontweight='bold')
    ax.text(1.2, 0, 0.08, "|+>", color='darkgreen', fontsize=12, fontweight='bold')
    ax.text(-1.2, 0, 0.08, "|->", color='darkgreen', fontsize=12, fontweight='bold')
    ax.text(0, 1.2, 0.08, "|i>", color='purple', fontsize=12, fontweight='bold')
    ax.text(0, -1.2, 0.08, "|-i>", color='purple', fontsize=12, fontweight='bold')

    # Equator and meridians
    t = np.linspace(0, 2 * np.pi, 80)
    ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), 'gray',
            linewidth=1.0, alpha=0.4)
    ax.plot(np.cos(t), np.zeros_like(t), np.sin(t), 'gray',
            linewidth=0.7, alpha=0.3)
    ax.plot(np.zeros_like(t), np.cos(t), np.sin(t), 'gray',
            linewidth=0.7, alpha=0.3)

    # Persistent H-gate rotation axis (xz-diagonal)
    h = H_axis  # (1,0,1)/sqrt(2)
    ax.plot([-1.4*h[0], 1.4*h[0]],
            [-1.4*h[1], 1.4*h[1]],
            [-1.4*h[2], 1.4*h[2]],
            color='dodgerblue', linewidth=2.0, alpha=0.6)

    # H-axis crosshair markers where axis pierces the sphere
    _draw_h_axis_crosshairs(ax)


def draw_rotation_axis(ax, axis, color='magenta'):
    """Highlight the rotation axis."""
    a = axis / np.linalg.norm(axis)
    ax.plot([-1.4*a[0], 1.4*a[0]],
            [-1.4*a[1], 1.4*a[1]],
            [-1.4*a[2], 1.4*a[2]],
            color=color, linewidth=2.5, alpha=0.8)


# --- Phase values ---
phi_values = [np.pi / 9, np.pi / 3, 3 * np.pi / 4]
phi_labels = [r'$\pi/9$', r'$\pi/3$', r'$3\pi/4$']

# --- Gate sequence for each phi ---
H_axis = np.array([1, 0, 1]) / np.sqrt(2)
Z_axis = np.array([0, 0, 1.0])


def build_gate_sequence(phi):
    """Return gate sequence for H-P(phi)-H."""
    return [
        ("H", H_axis, np.pi),
        (f"P({phi:.3f})", Z_axis, phi),
        ("H", H_axis, np.pi),
    ]


# --- Timing ---
fps = 15
frames_per_gate_intro = 20
frames_per_rotation = 40
frames_per_gate_hold = 15
frames_per_measurement = 40
frames_hold_after_run = int(3 * fps)
frames_return_camera = int(1.5 * fps)
frames_loop_return = int(4 * fps)  # Pan back to start for seamless loop

# Post-H2 camera sequence
frames_h2_hold = int(2 * fps)
frames_h2_tilt_down = int(2.5 * fps)
frames_equator_hold = int(2 * fps)

frames_per_gate = frames_per_gate_intro + frames_per_rotation + frames_per_gate_hold
frames_per_run = (3 * frames_per_gate + frames_h2_hold + frames_h2_tilt_down
                  + frames_equator_hold + frames_per_measurement)

total_frames = (3 * frames_per_run
                + 2 * (frames_hold_after_run + frames_return_camera)
                + frames_hold_after_run + frames_loop_return)

# --- Camera parameters ---
start_azim = -20.0
start_elev = 60.0  # colatitude 30 from z-axis


# --- Pre-compute trajectories ---
def compute_trajectory(phi):
    """Compute Bloch points through the H-P(phi)-H sequence."""
    gates = build_gate_sequence(phi)
    points = [np.array([0.0, 0.0, 1.0])]
    for _, axis, angle in gates:
        new = rotate_bloch_vector(points[-1], axis, angle)
        points.append(new)
    return gates, points


run_data = []
for phi in phi_values:
    gates, points = compute_trajectory(phi)
    z_proj = points[-1][2]
    run_data.append((gates, points, z_proj))

# --- Pre-compute full arc traces for each run ---
# Each run gets 3 arcs (H1, P, H2) stored as arrays of points
run_traces = []  # list of [arc0, arc1, arc2] per run
for run_idx_pre in range(len(phi_values)):
    gates_pre, points_pre, _ = run_data[run_idx_pre]
    arcs = []
    for g_idx, (_, axis, angle) in enumerate(gates_pre):
        arc_pts = [rotate_bloch_vector(points_pre[g_idx], axis, angle * s)
                   for s in np.linspace(0, 1.0, 50)]
        arcs.append(np.array(arc_pts))
    run_traces.append(arcs)


# --- Figure: two panels ---
fig = plt.figure(figsize=(14, 9))
# Bloch sphere: left 60% of width, full height
ax_bloch = fig.add_subplot(121, projection='3d',
                           position=[0.0, 0.02, 0.58, 0.90])
# Theory chart: right ~35% of width, 1/3 of vertical height, centered vertically
ax_chart = fig.add_subplot(122,
                           position=[0.62, 0.35, 0.35, 0.30])


# --- Side chart: cos^2 fringe pattern ---
def draw_fringe_chart(ax, measurement_dots):
    """
    Draw the cos^2(phi/2) pattern showing the center 3 fringes.
    measurement_dots: list of (phi, prob0) for completed runs.
    """
    ax.clear()
    phi_range = np.linspace(-3 * np.pi, 3 * np.pi, 500)
    intensity = np.cos(phi_range / 2) ** 2

    ax.plot(phi_range / np.pi, intensity, 'b-', linewidth=1.5, alpha=0.7)
    ax.fill_between(phi_range / np.pi, intensity, alpha=0.1, color='blue')

    ax.set_xlabel(r'$\phi / \pi$', fontsize=11)
    ax.set_ylabel(r'$P(|0\rangle) = \cos^2(\phi/2)$', fontsize=11)
    ax.set_title('Interference Pattern', fontsize=12)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.05, 1.1)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axhline(1, color='gray', linewidth=0.5, linestyle=':')
    ax.axhline(0.5, color='gray', linewidth=0.5, linestyle=':')

    # Grid lines at fringe peaks
    for m in range(-3, 4):
        ax.axvline(2 * m, color='gray', linewidth=0.3, alpha=0.5)

    # Draw measurement dots
    for phi_val, prob in measurement_dots:
        ax.scatter(phi_val / np.pi, prob, color='red', s=150, zorder=10,
                   edgecolors='darkred', linewidths=1.5)


# --- Frame phase determination ---
def get_frame_phase(frame):
    pos = 0
    for run_idx in range(3):
        if frame < pos + frames_per_run:
            return {'run_idx': run_idx, 'phase': 'run',
                    'gate_frame': frame - pos, 'local_frame': frame - pos}
        pos += frames_per_run

        if frame < pos + frames_hold_after_run:
            return {'run_idx': run_idx, 'phase': 'post_hold',
                    'local_frame': frame - pos, 'gate_frame': -1}
        pos += frames_hold_after_run

        if run_idx < 2:
            if frame < pos + frames_return_camera:
                return {'run_idx': run_idx, 'phase': 'camera_return',
                        'local_frame': frame - pos, 'gate_frame': -1}
            pos += frames_return_camera
        else:
            if frame < pos + frames_loop_return:
                return {'run_idx': run_idx, 'phase': 'loop_return',
                        'local_frame': frame - pos, 'gate_frame': -1}
            pos += frames_loop_return

    return {'run_idx': 2, 'phase': 'loop_return', 'local_frame': 0, 'gate_frame': -1}


# --- Camera ---
def compute_camera(frame_info):
    run_idx = frame_info['run_idx']
    phase = frame_info['phase']
    local = frame_info['local_frame']
    phi = phi_values[run_idx]
    phi_deg = np.degrees(phi)

    h_target_elev = 30.0
    h_target_azim = 30.0
    p_end_azim = 30.0 + phi_deg

    # For H2: pan CCW to arrive at the state vector's azimuth - 45 degrees
    # and elevation matching the state vector's colatitude
    _, points, _ = run_data[run_idx]
    final_pt = points[-1]  # after H2
    final_state_azim_deg = np.degrees(np.arctan2(final_pt[1], final_pt[0]))
    final_colat = np.degrees(np.arccos(np.clip(final_pt[2], -1, 1)))
    # matplotlib elevation = 90 - colatitude
    h2_end_elev = 90.0 - final_colat
    h2_end_azim = final_state_azim_deg - 45.0
    # Ensure we pan in the positive (CCW) direction
    if h2_end_azim < p_end_azim:
        h2_end_azim += 360.0

    equator_elev = 0.0

    if phase == 'run':
        gate_frame = frame_info['gate_frame']

        if gate_frame < frames_per_gate:
            # H1: pan from start to (azim=30, elev=30)
            t = gate_frame / frames_per_gate
            t = 0.5 - 0.5 * np.cos(t * np.pi)
            azim = start_azim + (h_target_azim - start_azim) * t
            elev = start_elev + (h_target_elev - start_elev) * t
            return elev, azim

        elif gate_frame < 2 * frames_per_gate:
            # P: pan azimuth from 30 to 30+phi_deg
            t = (gate_frame - frames_per_gate) / frames_per_gate
            t = 0.5 - 0.5 * np.cos(t * np.pi)
            azim = h_target_azim + (p_end_azim - h_target_azim) * t
            return h_target_elev, azim

        elif gate_frame < 3 * frames_per_gate:
            # H2: pan CCW from p_end_azim to h2_end_azim, elev to h2_end_elev
            t = (gate_frame - 2 * frames_per_gate) / frames_per_gate
            t = 0.5 - 0.5 * np.cos(t * np.pi)
            azim = p_end_azim + (h2_end_azim - p_end_azim) * t
            elev = h_target_elev + (h2_end_elev - h_target_elev) * t
            return elev, azim

        elif gate_frame < 3 * frames_per_gate + frames_h2_hold:
            return h2_end_elev, h2_end_azim

        elif gate_frame < 3 * frames_per_gate + frames_h2_hold + frames_h2_tilt_down:
            tilt_local = gate_frame - (3 * frames_per_gate + frames_h2_hold)
            t = tilt_local / frames_h2_tilt_down
            t = 0.5 - 0.5 * np.cos(t * np.pi)
            elev = h2_end_elev + (equator_elev - h2_end_elev) * t
            return elev, h2_end_azim

        elif gate_frame < (3 * frames_per_gate + frames_h2_hold
                           + frames_h2_tilt_down + frames_equator_hold):
            return equator_elev, h2_end_azim

        else:
            return equator_elev, h2_end_azim

    elif phase == 'post_hold':
        return equator_elev, h2_end_azim

    elif phase == 'camera_return':
        t = local / frames_return_camera
        t = 0.5 - 0.5 * np.cos(t * np.pi)
        azim = h2_end_azim + (start_azim - h2_end_azim) * t
        elev = equator_elev + (start_elev - equator_elev) * t
        return elev, azim

    elif phase == 'loop_return':
        t = local / frames_loop_return
        t = 0.5 - 0.5 * np.cos(t * np.pi)
        elev = equator_elev + (start_elev - equator_elev) * t
        azim = h2_end_azim + (start_azim - h2_end_azim) * t
        return elev, azim

    return start_elev, start_azim


# --- Main update ---
def update(frame):
    ax_bloch.cla()
    draw_bloch_sphere(ax_bloch)

    frame_info = get_frame_phase(frame)
    elev, azim = compute_camera(frame_info)
    ax_bloch.view_init(elev=elev, azim=azim)

    ax_bloch.set_xlim([-1.0, 1.0])
    ax_bloch.set_ylim([-1.0, 1.0])
    ax_bloch.set_zlim([-1.0, 1.0])
    ax_bloch.set_box_aspect([1, 1, 1])
    ax_bloch.set_axis_off()

    run_idx = frame_info['run_idx']
    phase = frame_info['phase']
    phi = phi_values[run_idx]
    gates, points, z_proj = run_data[run_idx]

    # Determine which measurement dots to show on the chart
    chart_dots = []
    if phase == 'run':
        # Previous runs' dots
        for prev in range(run_idx):
            prev_phi = phi_values[prev]
            prev_prob = (1 + run_data[prev][2]) / 2
            chart_dots.append((prev_phi, prev_prob))
    else:
        # Current + previous
        for prev in range(run_idx + 1):
            prev_phi = phi_values[prev]
            prev_prob = (1 + run_data[prev][2]) / 2
            chart_dots.append((prev_phi, prev_prob))

    # Check if we're in measurement phase of current run (dot appearing)
    meas_dot_appearing = False
    if phase == 'run':
        gate_frame = frame_info['gate_frame']
        meas_start = (3 * frames_per_gate + frames_h2_hold
                      + frames_h2_tilt_down + frames_equator_hold)
        if gate_frame >= meas_start:
            meas_t = (gate_frame - meas_start) / frames_per_measurement
            meas_t = min(meas_t, 1.0)
            if meas_t > 0.8:  # dot appears on chart near end of projection
                prob0 = (1 + z_proj) / 2
                chart_dots.append((phi, prob0))
                meas_dot_appearing = True

    # Draw the fringe chart
    draw_fringe_chart(ax_chart, chart_dots)

    # Draw persistent measurement dots on Bloch sphere from completed runs
    if phase == 'run':
        for prev_run in range(run_idx):
            _, _, prev_z = run_data[prev_run]
            ax_bloch.scatter(0, 0, prev_z, color='red', s=120, zorder=10)
    else:
        for prev_run in range(run_idx + 1):
            _, _, prev_z = run_data[prev_run]
            ax_bloch.scatter(0, 0, prev_z, color='red', s=120, zorder=10)

    if phase in ('post_hold', 'camera_return', 'loop_return'):
        final_point = points[-1]
        prob0 = (1 + z_proj) / 2
        ax_bloch.quiver(0, 0, 0, final_point[0], final_point[1], final_point[2],
                        color='limegreen', arrow_length_ratio=0.07, linewidth=3.0)
        ax_bloch.scatter(*final_point, color='limegreen', s=80, zorder=5)
        ax_bloch.plot([0, 0], [0, 0], [-1.3, 1.3], color='red',
                      linewidth=1.5, alpha=0.5)
        ax_bloch.set_title(f"Run {run_idx+1}/3: "
                           r"$\phi$ = " + f"{phi_labels[run_idx]}    "
                           f"P(|0>) = {prob0:.3f}",
                           fontsize=13, pad=10)
        return []

    # --- Run phase ---
    gate_frame = frame_info['gate_frame']

    if gate_frame < 3 * frames_per_gate:
        gate_idx = gate_frame // frames_per_gate
        sub_frame = gate_frame % frames_per_gate
        gate_label, axis, angle = gates[gate_idx]

        if sub_frame < frames_per_gate_intro:
            point = points[gate_idx]
            if not np.allclose(axis, H_axis):
                draw_rotation_axis(ax_bloch, axis)
            title_extra = f"Next: {gate_label}"
        elif sub_frame < frames_per_gate_intro + frames_per_rotation:
            t = (sub_frame - frames_per_gate_intro) / frames_per_rotation
            t = 0.5 - 0.5 * np.cos(t * np.pi)
            point = rotate_bloch_vector(points[gate_idx], axis, angle * t)
            if not np.allclose(axis, H_axis):
                draw_rotation_axis(ax_bloch, axis)
            trail_pts = [rotate_bloch_vector(points[gate_idx], axis, angle * s)
                         for s in np.linspace(0, t, 25)]
            trail = np.array(trail_pts)
            ax_bloch.plot(trail[:, 0], trail[:, 1], trail[:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)
            title_extra = f"Applying {gate_label}"
        else:
            point = points[gate_idx + 1]
            title_extra = f"After {gate_label}"

    elif gate_frame < 3 * frames_per_gate + frames_h2_hold:
        point = points[-1]
        prob0 = (1 + z_proj) / 2
        title_extra = f"After H2"

    elif gate_frame < (3 * frames_per_gate + frames_h2_hold + frames_h2_tilt_down):
        point = points[-1]
        title_extra = "Tilting to equator"

    elif gate_frame < (3 * frames_per_gate + frames_h2_hold
                       + frames_h2_tilt_down + frames_equator_hold):
        point = points[-1]
        prob0 = (1 + z_proj) / 2
        title_extra = f"Equator view"

    else:
        # Measurement
        meas_start = (3 * frames_per_gate + frames_h2_hold
                      + frames_h2_tilt_down + frames_equator_hold)
        meas_local = gate_frame - meas_start
        t = meas_local / frames_per_measurement
        t = 0.5 - 0.5 * np.cos(t * np.pi)

        final_point = points[-1]
        proj_x = final_point[0] * (1 - t)
        proj_y = final_point[1] * (1 - t)
        proj_z = final_point[2] * (1 - t) + z_proj * t

        point = final_point
        ax_bloch.plot([0, 0], [0, 0], [-1.3, 1.3], color='red',
                      linewidth=1.5, alpha=0.5)
        ax_bloch.scatter(proj_x, proj_y, proj_z, color='red',
                         s=100 + 40 * t, zorder=10)

        prob0 = (1 + z_proj) / 2
        title_extra = f"Measure: P(|0>) = {prob0:.3f}"

    # Draw state vector
    ax_bloch.quiver(0, 0, 0, point[0], point[1], point[2],
                    color='limegreen', arrow_length_ratio=0.07, linewidth=3.0)
    ax_bloch.scatter(*point, color='limegreen', s=80, zorder=5)

    # Draw persistent arc traces for current run (erased after measurement lands)
    meas_start = (3 * frames_per_gate + frames_h2_hold
                  + frames_h2_tilt_down + frames_equator_hold)
    meas_done = gate_frame >= meas_start + frames_per_measurement
    arcs = run_traces[run_idx]

    if not meas_done:
        if gate_frame < frames_per_gate:
            # During H1: draw partial or full arc
            sub_frame = gate_frame % frames_per_gate
            if sub_frame >= frames_per_gate_intro:
                t_arc = (sub_frame - frames_per_gate_intro) / frames_per_rotation
                t_arc = min(0.5 - 0.5 * np.cos(min(t_arc, 1.0) * np.pi), 1.0)
                n_pts = max(2, int(t_arc * 50))
                ax_bloch.plot(arcs[0][:n_pts, 0], arcs[0][:n_pts, 1],
                              arcs[0][:n_pts, 2],
                              'limegreen', alpha=0.6, linewidth=2.5)
            elif sub_frame >= frames_per_gate_intro + frames_per_rotation:
                # Hold after H1: full arc
                ax_bloch.plot(arcs[0][:, 0], arcs[0][:, 1], arcs[0][:, 2],
                              'limegreen', alpha=0.6, linewidth=2.5)
        elif gate_frame < 2 * frames_per_gate:
            # During P: full H1 arc + partial P arc
            ax_bloch.plot(arcs[0][:, 0], arcs[0][:, 1], arcs[0][:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)
            sub_frame = gate_frame % frames_per_gate
            if sub_frame >= frames_per_gate_intro:
                t_arc = (sub_frame - frames_per_gate_intro) / frames_per_rotation
                t_arc = min(0.5 - 0.5 * np.cos(min(t_arc, 1.0) * np.pi), 1.0)
                n_pts = max(2, int(t_arc * 50))
                ax_bloch.plot(arcs[1][:n_pts, 0], arcs[1][:n_pts, 1],
                              arcs[1][:n_pts, 2],
                              'limegreen', alpha=0.6, linewidth=2.5)
        elif gate_frame < 3 * frames_per_gate:
            # During H2: full H1 + P arcs + partial H2 arc
            ax_bloch.plot(arcs[0][:, 0], arcs[0][:, 1], arcs[0][:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)
            ax_bloch.plot(arcs[1][:, 0], arcs[1][:, 1], arcs[1][:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)
            sub_frame = gate_frame % frames_per_gate
            if sub_frame >= frames_per_gate_intro:
                t_arc = (sub_frame - frames_per_gate_intro) / frames_per_rotation
                t_arc = min(0.5 - 0.5 * np.cos(min(t_arc, 1.0) * np.pi), 1.0)
                n_pts = max(2, int(t_arc * 50))
                ax_bloch.plot(arcs[2][:n_pts, 0], arcs[2][:n_pts, 1],
                              arcs[2][:n_pts, 2],
                              'limegreen', alpha=0.6, linewidth=2.5)
        else:
            # After all gates (hold/tilt/equator/measurement): all 3 full arcs
            ax_bloch.plot(arcs[0][:, 0], arcs[0][:, 1], arcs[0][:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)
            ax_bloch.plot(arcs[1][:, 0], arcs[1][:, 1], arcs[1][:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)
            ax_bloch.plot(arcs[2][:, 0], arcs[2][:, 1], arcs[2][:, 2],
                          'limegreen', alpha=0.6, linewidth=2.5)

    # History dots
    if gate_frame < 3 * frames_per_gate:
        gate_idx_h = gate_frame // frames_per_gate
        n_done = gate_idx_h
    else:
        n_done = 3
    for i in range(min(n_done + 1, len(points))):
        ax_bloch.scatter(*points[i], color='gray', s=25, alpha=0.5)

    ax_bloch.set_title(f"Run {run_idx+1}/3: "
                       r"$\phi$ = " + f"{phi_labels[run_idx]}    {title_extra}",
                       fontsize=13, pad=10)

    return []


# --- Render ---
print(f"Bloch DSE Animation: {total_frames} frames at {fps} fps")
print(f"Phase values: {[f'{p:.4f}' for p in phi_values]}")
for i, phi in enumerate(phi_values):
    _, pts = compute_trajectory(phi)
    z = pts[-1][2]
    print(f"  phi={phi_labels[i]:>8s}: final z={z:.3f}, P(|0>)={((1+z)/2):.3f}")
print("Rendering...")

anim = FuncAnimation(fig, update, frames=total_frames, interval=1000//fps, blit=False)

try:
    writer = FFMpegWriter(fps=fps, metadata={'title': 'Bloch DSE H-P-H-M'})
    anim.save('bloch_dse_animation.mp4', writer=writer)
    print("\nSaved: bloch_dse_animation.mp4")
except Exception as e:
    print(f"\nmp4 failed ({e}). Trying gif...")
    try:
        writer = PillowWriter(fps=fps)
        anim.save('bloch_dse_animation.gif', writer=writer)
        print("Saved: bloch_dse_animation.gif")
    except Exception as e2:
        print(f"gif also failed ({e2}).")
        print("Install ffmpeg: sudo apt install ffmpeg")
