"""
Plot the Bloch colatitude of the final state after H-P(phi)-H as a function of phi.

The state after H-P(phi)-H|0> has alpha = (1 + e^{i*phi}) / 2.
  r_alpha = |alpha| = |1 + e^{i*phi}| / 2 = |cos(phi/2)|
  theta (colatitude) = 2 * arccos(r_alpha)

This shows how the P gate's Z-rotation (parameterized by phi) maps to the
colatitude of the final state after the second H rotates it back about the
XZ diagonal.

Usage:
  python colatitude_vs_phi.py

Output:
  colatitude_vs_phi.png
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

# Phase range
phi = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# r_alpha = |alpha| = |(1 + e^{i*phi}) / 2| = |cos(phi/2)|
r_alpha = np.abs(np.cos(phi / 2))

# Colatitude: theta = 2 * arccos(r_alpha)
theta = 2 * np.arccos(r_alpha)

# Probability for reference
prob_zero = r_alpha ** 2  # = cos^2(phi/2)

fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot colatitude
color1 = 'steelblue'
ax1.plot(phi / np.pi, theta / np.pi, color=color1, linewidth=2,
         label=r'Colatitude $\theta / \pi$')
ax1.set_xlabel(r'Phase $\phi / \pi$', fontsize=12)
ax1.set_ylabel(r'Colatitude $\theta / \pi$', fontsize=12, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xlim(-2, 2)
ax1.set_ylim(0, 1.05)

# Secondary axis: P(0) = cos^2(phi/2)
ax2 = ax1.twinx()
color2 = 'firebrick'
ax2.plot(phi / np.pi, prob_zero, color=color2, linewidth=1.5, linestyle='--',
         alpha=0.8, label=r'$P(|0\rangle) = \cos^2(\phi/2)$')
ax2.set_ylabel(r'$P(|0\rangle)$', fontsize=12, color=color2)
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 1.05)

# Annotations
ax1.axhline(0.5, color='gray', linewidth=0.5, linestyle=':')
ax1.axvline(0, color='gray', linewidth=0.5, linestyle=':')

ax1.set_title(r'H-P($\phi$)-H: Colatitude and measurement probability vs phase',
              fontsize=13)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=11)

plt.tight_layout()
plt.savefig('colatitude_vs_phi.png', dpi=150)
print("Saved: colatitude_vs_phi.png")
