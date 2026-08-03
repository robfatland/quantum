---
marp: true
theme: default
paginate: true
title: "Cloud Quantum Computing: From Simulation to Hardware"
author: Rob
---

# Cloud Quantum Computing: Sim to Hardware
## PEARC 2026

- Quantum computers are accessible today via cloud APIs
- IBM, AWS Braket, Azure Quantum, Google, **simulators**

![H-P-H circuit](double_slit_circuit.png)

---

# The Double-Slit Experiment on a Quantum Circuit

A single qubit encodes one photon at one screen position:

1. **Superpose** — put the qubit in equal superposition (both paths)
2. **Phase** — encode the path-length difference for this screen position
3. **Interfere** — recombine the paths
4. **Measure** — sample: did the photon arrive here?

Sweep across screen positions to build the full fringe pattern.

<!-- Embed: bloch_dse_animation.mp4 -->

---

# What the Circuit Produces

- Probability of detection = cos-squared of half the phase difference
- Identical to classical optics intensity formula
- The quantum computer genuinely computes interference, not a lookup table

<!-- Embed: double_slit_histogram.png or dse_accumulate_ibm.mp4 -->

---

# Five Backends, One Circuit

| Platform | Type | Access |
|----------|------|--------|
| Local AerSimulator | Classical sim | pip install |
| IBM Cloud AerSim | Classical sim (CloudBank VM) | Free |
| IBM Quantum | Superconducting hardware | Open plan (free) |
| AWS Braket | IonQ / Rigetti hardware | Pay-per-task |
| Azure Quantum | IonQ / Quantinuum hardware | Free credits |

Same H-P-H circuit submitted to each; results compared.

---

# Noise Comparison

| Metric | AerSim | IBM Hardware | AWS (IonQ) | Azure (IonQ) | GCP (sim) |
|--------|--------|-------------|------------|--------------|-----------|
| Fringe visibility | 1.000 | 0.92 | TBD | TBD | TBD |
| Dark-fringe bias | 0.000 | 0.03 | TBD | TBD | TBD |
| Chi-squared | 1.00 | 2.4 | TBD | TBD | TBD |
| Excess variance | 0.000 | 0.015 | TBD | TBD | TBD |

- **Simulator:** perfect cos-squared, only shot noise
- **Hardware:** decoherence, gate errors, and readout errors degrade visibility
- Noise is the signature that real quantum mechanics happened

---

# Takeaways

- Cloud quantum is production-ready for education and small experiments
- The simulator-to-hardware gap is measurable and meaningful
- CloudBank provides access paths for research computing
- **Complexity is the enemy** — the simplest circuit taught us the most

---

<!-- _class: lead -->

# Questions?

Circuit code and analysis: github.com/[repo]
