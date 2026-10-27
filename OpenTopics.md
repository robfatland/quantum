# Open Topics

## Documentation

- **Explore Superstaq / Infleqtion** — neutral-atom QC stack. Intel captured in `infleqtion/README.md`. Hardware access is bespoke; to be discussed with Infleqtion directly at an upcoming conference. Next step: try `pip install qiskit-superstaq` and run the double-slit / Bell circuits through the Superstaq compiler path.
- **Review rewritten Q2.md** (consolidated 2026-10-16; original preserved at `Q2.md.bak`). Confirm no content was lost, the narrative flows, and it still compiles clean via pandoc + xelatex. Delete `Q2.md.bak` once satisfied.
- To understand: Information is stored in correlations

## Alternative PEARC Demo Experiments (parked)

- **Bell/CHSH test with polarizers:** Prepare Bell states, measure in rotated bases, show CHSH violation ($S > 2$). Laser + polarizers on tabletop. If time permits, revisit as second demo.
- **Quantum random walk on a ring:** Discrete quantum walk with coin qubit, shows quadratic speedup over classical diffusion. Weak laser connection.
- **Hydrogen orbitals via VQE:** Variational Quantum Eigensolver for H atom energy levels. Narrative complexity (optimization loop) makes it harder to demo in 10 minutes.
- **Positronium annihilation correlations:** Singlet-state polarization correlations. Requires gamma-ray detectors — impractical for conference tabletop.
- **Entangled Stern-Gerlach:** Conceptually rich but requires magnet/beam apparatus not suited to a conference table.
- **Single-slit vs double-slit tradeoff:** Single slit produces a diffraction (sinc$^2$) pattern rather than interference fringes. Simpler circuit (no slit qubit needed) but less dramatic visual and weaker narrative ("where's the quantum?"). Double slit is preferred for the interference story.

## Other Parked Ideas

- Hydrogen atom building S1, S2 and D2 orbitals
- PIAB in 1D on a ring
- Polarization correlation of annihilation radiation for positronium
