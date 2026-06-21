# Black Holes: A Dialog

## Hawking Radiation and Particle Types

**A:** Hawking radiation invokes pair creation and a failed corresponding annihilation just
outside the event horizon. Is there a distribution of pair particle types? Or are they all
electron-positron?

**B:** Hawking radiation isn't limited to electron-positron pairs. The virtual pair production
near the event horizon spans all particle types, weighted by their properties. The black hole
radiates like a thermal blackbody at the Hawking temperature T = ħc³ / (8πGMk_B).

What determines the mix:

- *Temperature vs. mass threshold* — A particle species contributes significantly only when kT
  is comparable to or exceeds its rest mass energy mc². A stellar-mass black hole has an
  incredibly low temperature (~tens of nanokelvin), so it essentially only radiates massless or
  nearly massless particles: photons, gravitons, and neutrinos.
- *Spin statistics* — The greybody factors (transmission probabilities through the gravitational
  potential barrier) differ by spin.
- *Degrees of freedom* — More internal states (color, flavor, polarization) means more channels
  for emission.

For astrophysical black holes the temperature is so low that only massless particles matter. For
hypothetical micro black holes near end of evaporation, the temperature skyrockets and all
Standard Model particles get radiated democratically.

---

## Charge of the Radiation

**A:** So large black holes only radiate massless or near-massless particles. These do not have
charge, right?

**B:** Right. For large stellar-mass or bigger black holes the dominant radiation channels are
photons, gravitons, and neutrinos — all electrically neutral. The temperature is far too low
(~10⁻⁷ K for a solar-mass black hole) to produce even electrons, the lightest charged particle.

If a black hole has net electric charge, it can't shed that charge through Hawking radiation
alone while it's large. The charge is effectively frozen in until the very final stages of
evaporation when the temperature gets high enough to produce charged particles. A separate
mechanism, the Schwinger effect, can also discharge a black hole if the electric field near the
horizon is strong enough.

---

## Evaporation Timescales

**A:** In terms of orders of magnitude, how long does a 1 solar mass black hole take to radiate
down to 0.1 solar mass? And so on through several more orders of magnitude.

**B:** The evaporation time scales as M³. The full lifetime of a black hole of mass M is
approximately 2 × 10⁶⁷ years × (M/M☉)³. Since each order of magnitude in mass reduction
involves M₁³ - M₂³ ≈ M₁³ (the lower mass is negligible), each decade of mass loss takes
roughly 1000× less time than the previous one:

| From    | To       | Time         |
|---------|----------|--------------|
| 1 M☉   | 0.1 M☉  | ~10⁶⁷ years |
| 0.1 M☉ | 0.01 M☉ | ~10⁶⁴ years |
| 0.01 M☉| 10⁻³ M☉ | ~10⁶¹ years |
| 10⁻³ M☉| 10⁻⁴ M☉ | ~10⁵⁸ years |
| 10⁻⁴ M☉| 10⁻⁵ M☉ | ~10⁵⁵ years |
| 10⁻⁵ M☉| 10⁻⁶ M☉ | ~10⁵² years |
| 10⁻⁶ M☉| 10⁻⁷ M☉ | ~10⁴⁹ years |

The vast majority of the black hole's lifetime is spent at nearly its original mass — an
incredibly slow start followed by a runaway finale. The current age of the universe is ~10¹⁰
years; a 1 M☉ black hole's full lifetime is roughly 10⁵⁷ times that.

---

## Photon Wavelength

**A:** Focusing on a 1 solar mass black hole emitting a photon: this photon's typical wavelength
would be quite large?

**B:** Yes, extremely large. Using Wien's law with the Hawking temperature of ~6 × 10⁻⁸ K, the
peak wavelength works out to a few kilometers — roughly the same order as the Schwarzschild
radius itself. This isn't a coincidence; the characteristic wavelength of the radiation is
naturally set by the size of the black hole.

These are radio waves with wavelengths measured in kilometers, each photon carrying ~10⁻¹¹ eV.
The power output is ~10⁻²⁸ watts for 1 M☉, and the individual photons are lower energy than the
cosmic microwave background by many orders of magnitude. The CMB at 2.7 K completely drowns it
out.

---

## Greybody Spectrum

**A:** A blackbody curve has a smooth shape produced by the well-behaved Planck function. You
keep referring to "greybody" for the spectrum emitted by a black hole. Elaborate on what this
looks like.

**B:** A greybody is a blackbody spectrum with a frequency-dependent filter applied:

    u_greybody(ν) = Γ(ν) × u_blackbody(ν)

where Γ(ν) is the greybody factor — the probability that a particle of frequency ν escapes to
infinity rather than being scattered back by the gravitational potential.

For a Schwarzschild black hole:

- Low frequencies (λ >> r_s): Γ → 0. Long-wavelength modes don't fit through the barrier.
  Suppression goes as Γ ∝ (ν r_s/c)^(2l+2) — a steep power-law cutoff.
- High frequencies (λ << r_s): Γ → 1. Short-wavelength modes punch through (geometric optics
  limit).
- Intermediate (λ ~ r_s): Smooth transition. This is where the thermal peak sits.

The net effect: the greybody spectrum sits under the blackbody curve everywhere, hugging it at
high frequencies and peeling away at low frequencies. The peak is slightly narrower and shifted
toward higher frequencies. Total integrated power is reduced by roughly a factor of a few.

Different particle spins see different barriers: scalars (spin 0) escape most easily, gravitons
(spin 2) are most suppressed. The actual particle mix reaching infinity is biased toward
lower-spin species.

Analogy: a hot coal inside a translucent shell. The coal emits a perfect blackbody spectrum, but
the shell is more opaque at some wavelengths. The "shell" is the curved spacetime geometry
between the horizon and infinity.

---

## Greybody Factors and Escape Probability

**A:** Is the escape rate for photons 100%? Once the pair is produced outside the event horizon,
is it a sure thing that one photon goes back in while the other flies away?

**B:** No, it's not 100%. This is what greybody factors account for. The emitted particles still
have to climb out through the gravitational potential barrier. Some fraction get scattered back
in.

The transmission probability depends on the angular momentum of the particle, the frequency
relative to the black hole size, and the spin of the particle. For a 1 solar mass black hole
where the typical photon wavelength is comparable to the Schwarzschild radius, the overall
transmission is something like 1–30% depending on the mode.

The pair-production picture is really a heuristic. The rigorous derivation (Bogoliubov
transformation between in/out vacuum states) doesn't literally have pairs popping up at a
specific location. But within that heuristic: no, not every outgoing particle makes it to
infinity.

---

## Event Horizon Radius and the Electron Emission Threshold

**A:** Is it meaningful to think about the apparent radius of an event horizon in relation to the
black hole mass? Also at what mass in kg would the black hole be able to emit electrons? And
what is the corresponding radius?

**B:** The Schwarzschild radius scales linearly with mass: r_s = 2GM/c² ≈ 1.5 × 10⁻²⁷ m/kg × M.
Double the mass, double the radius. A 1 M☉ black hole has r_s ≈ 3 km.

For electron emission, the condition is kT ≈ m_e c² (0.511 MeV). Solving gives M ≈ 10²² kg —
about the mass of the Moon. The corresponding radius is r_s ≈ 10⁻⁴ m, about a tenth of a
millimeter.

So a black hole the mass of the Moon, with an event horizon smaller than a grain of sand, is
what it takes to start thermally producing the lightest charged particles.

---

## Electron-Positron Symmetry

**A:** Let's stay with this lunar mass black hole that is 0.1 mm in radius. Does it radiate
electrons and positrons in equal number?

**B:** Yes — for an electrically neutral black hole, it radiates electrons and positrons in
exactly equal numbers. The thermal spectrum doesn't distinguish between particle and
antiparticle.

If the black hole has net charge, things change. A positively charged black hole preferentially
emits positrons, gradually discharging itself. The discharge timescale is much shorter than the
mass evaporation timescale, so charged black holes neutralize relatively quickly. The
equilibrium state is essentially Q ≈ 0.

For a neutral lunar-mass black hole: equal electrons and positrons, equal neutrinos and
antineutrinos, photons and gravitons (their own antiparticles) — all at rates determined by the
thermal spectrum, greybody factors, and degrees of freedom. The net lepton number, baryon
number, and charge of the radiation are all zero on average.

---

## Positron Emission: Finding the Right Mass

**A:** What is the pair production rate per square meter of event horizon for a lunar-mass black
hole emitting positrons? And what if we drop to 10⁻⁶ lunar mass?

**B:** At lunar mass (7.3 × 10²² kg), T ≈ 1.7 K. The electron mass threshold requires
~6 × 10⁹ K, so m_e c²/kT ≈ 7. The suppression is e^(−7) ≈ 10⁻³. Rough estimate: ~10⁻³ to
10⁻⁴ positrons per second total, with the horizon area only ~1.5 × 10⁻⁷ m². Meanwhile photons
are emitted at ~10⁸ to 10⁹ per second (no exponential suppression).

To get kT ~ m_e c² requires T ~ 6 × 10⁹ K, which means M ~ 10¹⁶ kg — about 10⁻⁶ lunar
masses, or the mass of a small mountain (a cube of rock ~2 km on a side). The Schwarzschild
radius is ~15 picometers (smaller than a hydrogen atom).

At M ~ 10¹⁶ kg the suppression factor is e^(−1) ≈ 0.37 — order unity. Positrons are produced
at a meaningful rate:

| Quantity                 | Value                          |
|--------------------------|--------------------------------|
| Mass                     | ~10¹⁶ kg (small mountain)     |
| Temperature              | ~6 × 10⁹ K                   |
| Schwarzschild radius     | ~15 picometers (sub-atomic)   |
| Total radiated power     | ~10 megawatts                 |
| Positron emission rate   | ~10¹⁸ to 10¹⁹ /s            |
| Typical positron energy  | ~1–2 MeV                      |

A sub-atomic-sized object radiating 10 megawatts, of which ~5–10% is electron-positron pairs at
MeV energies. The exponential is merciless: going from 10¹⁶ kg to 7 × 10²² kg (six orders of
magnitude in mass) takes you from vigorous positron emission to effectively zero.

---

## Lifetime and Final Explosion of a Mountain-Mass Black Hole

**A:** What is the approximate lifetime of this small-mountain black hole? And what is the final
explosion like?

**B:** Using the lifetime formula t ≈ 5120πG²M³/(ħc⁴):

    t ≈ 2 × 10⁶⁷ years × (M/M☉)³
    M/M☉ = 10¹⁶ / (2 × 10³⁰) = 5 × 10⁻¹⁵
    t ≈ 2 × 10⁶⁷ × (5 × 10⁻¹⁵)³ ≈ 2 × 10⁶⁷ × 1.25 × 10⁻⁴³ ≈ 10²⁴ years

So roughly **10²⁴ years** — about 10¹⁴ times the current age of the universe. Still immensely
long, but far shorter than stellar-mass or lunar-mass black holes.

Because of negative heat capacity, the evaporation accelerates. Most of the lifetime is spent
near the original mass, radiating at ~10 megawatts. The final moments are a runaway:

**The last second:**

In the final second of a black hole's life, the remaining mass is about 10⁶ kg (a thousand
tonnes). The temperature has risen to ~10¹⁷ K — hot enough to produce all Standard Model
particles: quarks, gluons, W and Z bosons, Higgs bosons, top quarks, everything.

The energy released in the last second: E = Mc² ≈ 10⁶ × (3×10⁸)² ≈ **10²³ joules** — roughly
equivalent to a million-megaton nuclear weapon, or about 10⁷ times the energy of the Hiroshima
bomb.

**What the explosion looks like:**

- It's not a single flash — it's a rapidly intensifying burst lasting a fraction of a second at
  the very end.
- The spectrum sweeps upward through the entire electromagnetic spectrum and beyond: radio →
  infrared → visible → UV → X-ray → gamma ray, as the temperature climbs.
- At the end, the emission is dominated by hard gamma rays and a spray of all particle species
  at energies up to ~TeV scale.
- The final burst produces roughly equal numbers of all particle/antiparticle pairs whose mass
  is below kT — a democratic fireball of the entire Standard Model zoo.
- There is no remnant (in the standard picture). The black hole evaporates completely, leaving
  only outgoing radiation and particles.

**Could we detect one?**

Possibly. A black hole formed in the early universe with initial mass ~10¹² kg would be
reaching its final explosion *now* (lifetime ≈ 13.8 billion years). These "primordial black
hole" explosions would appear as brief, hard gamma-ray bursts with a distinctive spectrum —
unlike any astrophysical source because the spectrum gets harder (bluer) as the burst
intensifies (normal explosions cool as they expand). Searches have been conducted but none
conclusively detected.

**Comparison to other explosions:**

| Event                        | Energy (joules) |
|------------------------------|-----------------|
| Hiroshima bomb               | ~10¹⁶          |
| Largest H-bomb (Tsar Bomba)  | ~2 × 10¹⁷     |
| Black hole final second      | ~10²³          |
| Supernova                    | ~10⁴⁴          |
| Gamma-ray burst              | ~10⁴⁷          |

So the final explosion of a mountain-mass black hole is enormously powerful by human standards
but negligible by astrophysical standards — a firecracker compared to a supernova.

---

## Halving Time for a Lunar-Mass Black Hole

**A:** How long would it take the lunar mass black hole to reduce its mass to half?

**B:** The full lifetime of a lunar-mass black hole (M ≈ 7.3 × 10²² kg) is approximately 10⁴⁵
years. To go from M to M/2, the time is proportional to M³ - (M/2)³ = (7/8)M³, so the halving
time is 7/8 of the total lifetime: roughly 10⁴⁵ years. Still about 10³⁵ times the current age
of the universe.

The power output at this mass is roughly 10⁻¹⁰ watts — about a tenth of a nanowatt. Detectable
in principle, but a glacial rate of mass loss.

---

## The Information Paradox

**A:** Suppose we throw the New York Public Library into a black hole. Some physicist says the
information is in there and we could get it back out if we were clever. Do we need to wait for
the black hole to evaporate prior to recovering the information?

**B:** This is one of the deepest open questions in theoretical physics.

Hawking's original position was that information is lost: the radiation is purely thermal,
carries no correlations, and when the black hole is gone, so is the library. This violates
unitarity in quantum mechanics — hence the "paradox."

The modern consensus (post-Page, post-AdS/CFT) is that information is not lost. It comes out
encoded in the Hawking radiation, but incredibly scrambled. You don't start getting meaningful
information back until after the *Page time* — roughly halfway through the evaporation, when
about half the entropy has been radiated. Before that, the radiation looks perfectly thermal.
After the Page time, the radiation becomes increasingly entangled with what was emitted earlier,
and in principle the correlations encode everything that fell in.

So you don't have to wait for full evaporation — you need to wait for the Page time, then
information starts leaking out. But recovering it requires collecting essentially all the
Hawking radiation and performing a quantum computation on it that is, for practical purposes,
impossible. It's recoverable in the same sense that an unburned book's text is recoverable from
its smoke and ash — thermodynamically true, practically absurd.

Recent developments (islands, replica wormholes, circa 2019) suggest the Page curve is
reproduced correctly by semiclassical gravity when certain saddle points in the gravitational
path integral are included. This gives more confidence that information does come out, but the
mechanism — how it gets from behind the horizon into the radiation — remains debated.

---

## Surface Area and Information Capacity

**A:** What about the surface area of the event horizon in relation to the information capacity
of the black hole?

**B:** The entropy (information content) of a black hole is proportional to its surface area,
not its volume:

    S = kA / (4ℓ_P²)

where A is the area of the event horizon and ℓ_P is the Planck length (~1.6 × 10⁻³⁵ m). In
information-theoretic terms: roughly one bit per 4 Planck areas, or one bit per ~10⁻⁶⁹ m².

For a solar-mass black hole: r_s ≈ 3 km, A ≈ 10⁸ m², giving S ≈ 10⁷⁷ bits. This scales as M²
(since A ∝ r² ∝ M²), not M³ as one would expect if information were stored volumetrically.

Why this matters:

- It's a maximum. No object of a given size can contain more information than a black hole of
  that size. Trying to pack more in causes gravitational collapse.
- It implies the holographic principle: the fundamental degrees of freedom of a region of space
  are encoded on its boundary, not in its bulk. A 3D volume's information content is described
  by a 2D surface.
- It connects thermodynamics, quantum mechanics, and gravity in a single formula. Bekenstein
  proposed it (1972–73) from thought experiments about the second law; Hawking confirmed the
  factor of 1/4 by discovering the radiation (1974).

For scale: the Library of Congress contains roughly 10¹³ bits. A solar-mass black hole holds
10⁷⁷ bits — exceeding all human-generated information by about 60 orders of magnitude.

---

## Accretion vs. Radiation

**A:** The interstellar medium with a typical density of 1 hydrogen atom per cubic meter will
randomly feed a solar mass black hole at a rate much higher than its rate of radiation. Are all
but the most microscopic black holes destined to increase in mass until the universe is clean?
How does radiation balance accumulation?

**B:** For any astrophysical black hole in today's universe, accretion dominates by an absurd
margin. But even in a perfect vacuum with no matter, a solar-mass black hole still can't
evaporate today: the cosmic microwave background at 2.7 K is hotter than any black hole above
about 10²² kg. A solar-mass black hole at ~10⁻⁷ K absorbs CMB photons faster than it emits
Hawking radiation.

The crossover mass where Hawking temperature equals the CMB temperature is roughly 0.8 × 10²²
kg — about the mass of the Moon. Only black holes lighter than this can currently evaporate.
Everything heavier is growing.

For stellar-mass black holes to begin net evaporation, the universe must expand and cool until
the CMB drops below ~10⁻⁷ K, requiring expansion by a factor of ~2.7 × 10⁷. In a
dark-energy-dominated universe the scale factor grows exponentially with a doubling time of
~10¹⁰ years, so this takes roughly 200 billion years (about 15× the current age). For
lunar-mass black holes (T_Hawking ≈ 1.7 K), the CMB only needs to drop below 1.7 K — about one
more doubling, or 10–20 billion years from now.

The "black hole era" of the universe lasts from roughly 10⁴⁰ to 10¹⁰⁰ years, during which
black holes are the last organized structures, slowly evaporating in an increasingly cold and
empty cosmos.

**A:** The CMB temperature is going to decrease over the next 14 billion years. Does this imply
the universe is not a gravitationally bound system?

**B:** Yes — exactly. The CMB cools because space is expanding. If the universe were
gravitationally bound (destined to recollapse), the expansion would reverse, the scale factor
would shrink, and the CMB would heat up again (blueshift). The fact that we observe the CMB
cooling — and that the expansion is accelerating — tells us the universe is not gravitationally
bound. It's not even decelerating toward a halt. Dark energy is driving exponential expansion.

This was the 1998 discovery (Perlmutter, Riess, Schmidt — Nobel 2011): distant supernovae are
dimmer than expected, meaning the expansion is accelerating.

| Model                              | Fate                  | CMB temperature       |
|------------------------------------|-----------------------|-----------------------|
| Closed (Ω > 1)                    | Big Crunch            | Eventually rises      |
| Flat/open, no Λ (Ω ≤ 1)          | Eternal expansion     | Falls as 1/a → 0     |
| Flat + dark energy (our universe) | Accelerating expansion| Falls exponentially   |

We're in the third case. Structures not already gravitationally collapsed (galaxy clusters and
smaller) will eventually be carried beyond each other's cosmological horizons. The cooling CMB
is a direct thermodynamic signature of an unbound, expanding universe.

---

## Lepton Number vs. Electric Charge

**A:** Distinguish between lepton number and what is taught at the introductory level as
electrical charge.

**B:** Both are conserved quantum numbers — bookkeeping labels that must balance before and
after any interaction. But they're independent.

Electric charge comes in multiples of e/3 (quarks) or e (leptons), has a force associated with
it (electromagnetism), is directly observable (electroscopes, deflection in fields), and its
conservation is absolute.

Lepton number is just a counting rule: +1 for each lepton, −1 for each antilepton. It has no
force associated with it, is not directly measurable as a physical quantity, and its
conservation might be approximate (violated if neutrinos are Majorana).

The key distinction: electric charge is dynamical — it's the source of a gauge field (the
photon) and determines interaction strength. Lepton number is kinematic bookkeeping — it
constrains what reactions are allowed but generates no force.

| Particle          | Electric charge | Lepton number |
|-------------------|----------------|---------------|
| Electron          | −1             | +1            |
| Electron neutrino | 0              | +1            |
| Positron          | +1             | −1            |
| Proton            | +1             | 0             |
| Neutron           | 0              | 0             |
| Photon            | 0              | 0             |

Why this matters for black holes: a black hole can be characterized by charge (it creates a
measurable electric field — Reissner-Nordström solution). But it cannot be characterized by
lepton number. The no-hair theorem says a black hole is described only by mass, charge, and
angular momentum. Lepton number, baryon number, and all other non-gauge quantum numbers are
swallowed and classically lost — one facet of the information paradox.

---

## Neutrinos: Dirac vs. Majorana

**A:** Run this again for neutrinos. Also non-annihilating self-antiparticles?

**B:** No — neutrinos are different, and this is actually an open question.

Neutrinos carry lepton number: ν_e has +1, ν̄_e has −1. They are produced distinctly and can
genuinely annihilate (ν + ν̄ → Z⁰ → fermion pairs). Unlike photons, neutrinos have a distinct
antiparticle.

But the open question: are neutrinos Dirac or Majorana?

- Dirac: ν and ν̄ are genuinely distinct (like electron/positron). Lepton number is strictly
  conserved.
- Majorana: ν and ν̄ are the same particle in different helicity states. The neutrino is its own
  antiparticle, and lepton number is only approximately conserved.

If Majorana, processes violating lepton number by 2 become possible — specifically neutrinoless
double beta decay (two neutrons → two protons + two electrons + nothing else). Experiments are
actively searching for this (GERDA, MAJORANA, KamLAND-Zen, nEXO, LEGEND). No detection yet.

Even if neutrinos are Majorana (own antiparticle), they differ from photons: as fermions, two
identical fermions can annihilate. The photon case is special because there's no quantum number
being exchanged or cancelled in a photon-photon meeting.

For Hawking radiation: if Dirac, a neutral black hole emits equal ν and ν̄. If Majorana, it
emits neutrinos of both helicities equally. The total emission rate and spectrum are the same
either way — the distinction doesn't affect the thermodynamics, just the bookkeeping.

---

## Photons as Their Own Antiparticle

**A:** How is the antiparticle of a photon a photon? Does this not mean they mutually interact
and annihilate one another? Photons do not interact; and when they annihilate does this not
produce two more photons?

**B:** Several things are getting conflated here.

"The photon is its own antiparticle" means the photon has no conserved quantum number (charge,
lepton number, baryon number) that would distinguish it from an anti-version. For an electron,
flipping all quantum numbers gives a positron — a distinct particle. For a photon, there's
nothing to flip. This does not mean two photons annihilate when they meet.

Annihilation requires a conserved quantity that sums to zero: electron (+1 lepton number) +
positron (−1 lepton number) → products with zero net lepton number. Two photons meeting have
nothing to cancel. "X is its own antiparticle" means there's no distinct anti-X, not that
X + X → nothing.

Do photons interact at all? At tree level in QED: no (no direct photon-photon vertex). At loop
level (virtual electron box diagrams — Euler-Heisenberg), yes, incredibly weakly. This was
confirmed by ATLAS in 2017 (light-by-light scattering in heavy-ion collisions). But this is
scattering, not annihilation: photons in, photons out.

The pair-creation heuristic for Hawking radiation is most natural for charged fermions where
there's a clear particle/antiparticle distinction. For photons and gravitons, it's better to
think of it as: the vacuum state near the horizon looks like a thermal bath of real particles to
a distant observer. The Bogoliubov transformation formalism handles this without needing the
pair metaphor at all.

---

## Negative Heat Capacity

**A:** Is it correct to say that black holes become warmer as they radiate? Reconcile this with
the notion that as something radiates energy away it becomes cooler.

**B:** Yes — as a black hole radiates and loses mass, it gets hotter (T ∝ 1/M). This means
black holes have negative heat capacity, which is the opposite of normal objects.

This is not unique to black holes. Gravitationally bound systems generically have negative heat
capacity: a star that loses energy contracts and heats up; a satellite that loses orbital energy
drops lower and speeds up. Gravity inverts the usual thermodynamic intuition.

For a black hole the consequence is dramatic: evaporation is a runaway process. Losing mass
leads to higher temperature, faster radiation, faster mass loss, even higher temperature — the
endgame is an explosion rather than a gentle fade.

The reconciliation: "radiating makes things cooler" applies to systems with positive heat
capacity (everyday objects where energy is stored in kinetic/thermal modes). For systems where
gravity dominates the energetics, the rule inverts. A black hole is purely gravitational, so
the inversion is total.

Formally: C = dE/dT. For a black hole, E = Mc² ∝ 1/T, so dE/dT < 0. This means the system
cannot reach stable thermal equilibrium with a heat bath. A black hole slightly hotter than its
surroundings gets hotter; one slightly cooler grows. The CMB equilibrium point is unstable.

---

## Open Questions

- Does Kip S. Thorne's work (membrane paradigm, etc.) offer insight on the information
  question? Does the membrane paradigm provide classical intuition for how information gets
  re-emitted from the horizon?
- Accidental conceptual connection: the Kochen-Specker theorem (contextuality of quantum
  observables) — any relevance to whether "information" in a black hole can be thought of as
  having definite values prior to measurement?
- Origin and meaning of the terms: "Page time" (named for Don Page), "AdS" (anti-de Sitter
  space), "CFT" (conformal field theory) — and the AdS/CFT correspondence
- "Practically absurd" — what exactly is the computational complexity of decoding Hawking
  radiation? Is there a formal bound?
- Information entropy vs. thermodynamic entropy: These are the same formalism (Shannon 1948,
  Jaynes 1957). Bekenstein entropy S = kA/4ℓ_P² counts bits inaccessible behind the horizon.
  Open part: what are the microstates?
