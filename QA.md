# QA a catch-all or appendix


## PDF generation

Full document (all Q files):
```bash
pandoc Q0.md Q1.md Q2.md Q3.md Q4.md Q5.md Q6.md Q7.md -o Q.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V mainfont="DejaVu Serif" \
  -V sansfont="DejaVu Sans" \
  -V mathfont="Latin Modern Math" \
  -V monofont="DejaVu Sans Mono" \
  -V fontsize=11pt \
  --toc --toc-depth=2 \
  --syntax-highlighting=tango
```

Single file (e.g. Q0 only):
```bash
pandoc Q0.md -o Q0.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V mainfont="DejaVu Serif" \
  -V mathfont="Latin Modern Math" \
  -V monofont="DejaVu Sans Mono" \
  -V fontsize=11pt \
  --syntax-highlighting=tango
```


## Bookkeeping


## The stack


The following *ansätze* are to be accounted for...


- Planck resolving the ultraviolet catastrophe by an ad hoc *discretization* axiom
- The equivalence of wave and matrix mechanics
    - 1925 Heisenberg/Jordan/Born ~ 1926 Schrodinger
- Born interpretation: wave functions as probability amplitudes
- There exist mathematical (linear) operators that correspond to physical observation
- ...but operators do not commute...
- ...resulting in a residual tied to the uncertainty principle
- Working in fewer than three dimensions benefits thereof
- What is a *quantum state*?


| Operator | In position basis (ψ(x) = ⟨x\|ψ⟩) | In momentum basis (φ(p) = ⟨p\|ψ⟩) |
|---|---|---|
| Position x̂ | Multiply by x: x̂ψ(x) = xψ(x) | Differentiate: x̂φ(p) = iℏ ∂φ/∂p |
| Momentum p̂ | Differentiate: p̂ψ(x) = −iℏ ∂ψ/∂x | Multiply by p: p̂φ(p) = pφ(p) |


These fragments can be treated as *ansätze*; road signs pointing towards what we presume will be a 
coherent picture. There are still more of these overheard fragments in what follows.
My intent however is to never resort to proof by assertion, to never say "It turns out that..."


- Particles and antiparticles: Opposite charge annihilation... 
    - what about "you are your own antiparticle"? (neutrinos?) 
    - Does this mean no annihilation? Why then say 'anti'?
- From Hilbert space to choice of basis... do we say Hilbert spacii? 
- linear operators (are there nonlinear? what is the physical meaning?)
- finite versus infinite basis vector situations
- conjugate operators represented in one another's basis; Fourier transform
- review three differential equations: Wave, Heat, maybe Laplace?
- How from wave equation to Schrodinger equation
- Time dependence / independence
- Matrix mechanics
- Back to operators: position, momentum, energy, time
- Discrete steps / energy levels; raising / lowering operators
- Can we get to the PRL from here? Or is that too far afield?
- How about 1D particle to large mass via spring?
- How about particle in a potential well, tunneling
- Other solvable QM problems? Lattice maybe? 
- And at last: Pivot to the fundamental ideas of quantum computing
- Revisit ansätze and axiomii




## The parallelogram law: geometric interpretation


### The statement

$$\|x + y\|^2 + \|x - y\|^2 = 2\|x\|^2 + 2\|y\|^2$$


### The geometry

Draw two vectors $x$ and $y$ from a common origin. They define a parallelogram with:

- **Diagonal 1:** $x + y$ (the vector sum — tip-to-tip diagonal)
- **Diagonal 2:** $x - y$ (the vector difference — the other diagonal)
- **Sides:** $x$ and $y$ themselves

The parallelogram law says: **the sum of the squares of the diagonals equals the sum 
of the squares of all four sides** (each side counted once, so $2\|x\|^2 + 2\|y\|^2$ 
because opposite sides are equal).

In $\mathbb{R}^2$ this is a theorem of Euclidean geometry about actual parallelograms 
drawn on paper. You can verify it with a ruler.


### Why it matters for Hilbert spaces

The parallelogram law is the **litmus test** for whether a norm comes from an inner 
product. Many norms exist (e.g. the taxicab norm $\|v\|_1 = |v_1| + |v_2|$, the max 
norm $\|v\|_\infty = \max(|v_1|, |v_2|)$) but most do *not* satisfy the parallelogram 
law. Only norms that arise from an inner product via $\|x\| = \sqrt{\langle x, x \rangle}$ 
satisfy it.

So the parallelogram law is the signature property that says: "this space has genuine 
angles and orthogonality, not just lengths." A Banach space (complete normed space) that 
satisfies the parallelogram law is automatically a Hilbert space — you can reconstruct 
the inner product from the norm via the **polarization identity**:

$$\langle x, y \rangle = \frac{1}{4}\left(\|x+y\|^2 - \|x-y\|^2 + i\|x+iy\|^2 - i\|x-iy\|^2\right)$$

(The real part comes from the two diagonals; the imaginary part requires the $i$-rotated 
diagonals — this is specifically the complex case.)





## Density matrix and entanglement



Begin by recalling that a qubit state vector is specified as $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$. This yields probabilities, phase, Bloch sphere location; everything for the single qubit. Out the gate. Heh heh.


Now consider two scenarios where the state vector is insufficient.


**Scenario A**: "Mixed" (not single state). A qubit is physically in one of two states (unknown which): Either state $|0\rangle$ or state $|1\rangle$: 50/50 odds in the z-basis (or any other basis) in as a collapsed wave function. 'Any choice of basis' is a key concept: Choose antipodal unit vectors $u, v$ on the Bloch sphere for the observation: We will still get 50/50 odds of $|u\rangle$ or $|v\rangle$.


#### Parenthetical: The arbitrary basis $u, v$


An arbitrary basis $|u\rangle, |v\rangle$ can be specified with a single unit vector $\hat{u} = (u_x, u_y, u_z)$ with magnitude $1$. The other basis vector is automatically $\hat{v} = -\hat{u}$. This can be equivalently written as two angles $(\theta, \varphi)$: colatitude and azimuth. The corresponding basis states in the Z-basis are:


$$∣u \; \rangle = \cos{\frac{\theta}{2}} \; ∣0 \; \rangle + e^{i \varphi} \sin{\frac{\theta}{2}} \; | \; 1 \; \rangle$$


$$∣v \; \rangle = \sin{\frac{\theta}{2}} \; ∣0 \; \rangle - e^{i \varphi} \cos{\frac{\theta}{2}} \; | \; 1 \; \rangle$$


Note that these can be demonstrated to be orthogonal vectors despite the confusing fact that they render as antipodes in the Bloch sphere.


**Subparenthetical**
Here we are *starting out* from the Bloch sphere to think
about antipodal basis vectors and how they relate to the 
computational Z basis. We may start
from the two complex unit discs when contemplating 
amplitudes $\alpha$ and $\beta$ applied to a pair of basis vectors; and from there transfer *to* the Bloch
sphere to visualize the statevector of a qubit.


#### Resuming: Scenario B



**Scenario B**: Consider the $H |0\rangle$ qubit as the superposition $|+\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$. Observed in the Z basis this will yield $|0\rangle$ or $|1\rangle$ with 50/50 probability, just as in **A**. But observed in the X basis we will see $|+\rangle$ 100% of the time.


Both **A** and **B** give 50/50 measurement outcomes in the Z-basis but they are physically distinct.
No single state vector can describe **A**: It is not $|0\rangle$, nor $|1\rangle$, nor a superposition of the two.
It has lost the qubit's capacity for coherent interference: No statevector means no $\alpha$ (no colatitude) and no phase... no means of arriving on the Bloch sphere... no interference.



In contrast, **B** shows interference. So what about **B** is insufficient? Nothing at the moment. But where we are headed is the **B** qubit getting entangled with another qubit, whereupon the single qubit state will prove to be insufficient for a mathematical characterization.


The density matrix $\rho$ will be the starting point for this new machinery applicable to both scenarios **A** and **B**. It is defined as a weighted sum of outer products of state vectors with themselves. The outer product is a matrix multiplication of the *ket* version of the state vector by the (transpose conjugate) *bra* version of the state vector, written left to right. For scenario **B** the state vector is the complete picture so the sum is a single term:


$$\rho = |+\rangle \langle + |$$


For **A** there is not this single state vector situation. The definition of $\rho$ as a sum will have two terms: One for each basis state $|0\rangle$ and $|1\rangle$. The **A** qubit is collapsed to one of two basis states and we treat this as a classical *or* probability. 


$$\rho = \frac{1}{2} | 0 \rangle \langle 0 | + 
\frac{1}{2} |1\rangle \langle 1|$$


This sums two 'pure state' density matrices weighted by classical probabilities. The generalization would be 
$\rho = \sum_{k} p_k |\psi_k\rangle\langle\psi_k|$ where $\sum_k p_k = 1$.


**to do: better format for:...**


For **A** $\rho$ is $\frac{1}{2} \; \cdot \; I$


For **B** $\rho$ is $\frac{1}{2} \; \cdot \;$


```
1  1
1  1
```


Now that we have defined the density matrix applicable to both **A** and **B**, we consider an assertion about its relationship to *pure* and *mixed* states. This assertion: If the density matrix includes nonzero off-diagonal elements then coherent interference is possible but not certain for the qubit in question. The definitive test for a pure state is that $\rho^2 = \rho$. 


In contrast: If the off-diagonals are zero then the qubit is in a classical mixture state with no interference possible. 


Example: $\rho = $

```
0.7  0.3
0.3  0.3
```

fails the pure state test.


Check question: In scenario **A** above, suppose we measure in the X-basis instead of Z. What happens? What happens for scenario B? Answer: **A** still gives 50-50 results. Regardless of choice of basis a 50/50 distribution of $|0\rangle$ and $|1\rangle$ states will... **to do need this improved**. For **B** 100% of the results will be $|+\rangle$. 



**To do: Get a decent response to "Why is this the operational difference between a mixture and a superposition?"**



**To do Show that the bra version of $\frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)$ is $\frac{1}{\sqrt{2}}(1, -i)$.**


Pure state, interference possible: $\rho^2 = \rho$ and $\rho$ may or may not have off-diagonals depending on basis. Mixed state: $\rho^2 \neq \rho$ (always); also may or may not have off-diagonals. 


The off-diagonals tell you about coherence in the basis you chose to write the matrix. A pure state written in its own eigenbasis has no off-diagonals, for example $|0\rangle\langle 0| = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ --- pure, no off-diagonals.


### Anticipating partial coherence


Let's anticipate points inside the Bloch sphere indicating "not fully classical / not pure quantum". It is asserted to be a gradation, contrasting the unit sphere surface as pure quantum with the origin ($\rho = \frac{1}{2} I$) fully mixed. (Here at last is a win for the Bloch sphere: Add any two basis vectors to arrive at the origin!)


Partial coherence relates to Feynman's 'little guys' detecting electrons at the slits becoming gradually less reliable in the DSE.


Interpretation of structure of $\rho$:


- Off-diagonals = 0: fully decohered, classical mixture in this basis
- Off-diagonals = maximal (and $\rho^2 = \rho$): fully coherent pure state
- Off-diagonals = nonzero but $\rho^2 \neq \rho$: partially coherent mixed state — some but not all phase information survives


The key is that you're averaging over two different states, not measuring one state.

If Fred's qubit is $|0\rangle$: measuring in the X-basis gives 50/50 (because $|0\rangle = \frac{1}{\sqrt{2}}(|+\rangle + |-\rangle)$).

If Fred's qubit is $|1\rangle$: measuring in the X-basis also gives 50/50 (because $|1\rangle = \frac{1}{\sqrt{2}}(|+\rangle - |-\rangle)$).

Since you don't know which one Fred gave you (50% chance of each), and both give 50/50 in the X-basis, the mixture gives 50/50 in the X-basis.

This works for any basis because $|0\rangle$ and $|1\rangle$ are antipodal on the Bloch sphere (north and south poles). Their measurement statistics in any other basis are mirror images of each other: whatever probability $|0\rangle$ gives for one outcome, $|1\rangle$ gives for the other. A 50/50 classical mixture of antipodal states averages to 50/50 in every direction. That's why $\rho = \frac{1}{2}I$ sits at the center of the Bloch sphere — equidistant from every point on the surface, no preferred direction.

On change of basis means two new unit circles:

The same state $|\psi\rangle$ can be written as $\alpha|0\rangle + \beta|1\rangle$ or equivalently $\gamma|+\rangle + \delta|-\rangle$. Same vector in Hilbert space, different coordinate representation. The two-disk picture just shows the components in whatever basis you've chosen — change the basis, get a new pair of complex coefficients, same underlying state.


Me


The Bloch sphere is not the visualization of a qubit Hilbert space. It is a visualization of the physically relevant degrees of freedom found within a qubit Hilbert space. Specifically two degrees of freedom: The magnitude of the first complex amplitude alpha as $r_{\alpha} \textrm{ from }r_{\alpha} e^{ i \eta}$ and the phase difference between scalar amplitude values $\alpha$ and $\beta$ as $\nu - \eta$.



kiro


Agreed — precise and correct. The full Hilbert space $\mathbb{C}^2$ has four real parameters (two magnitudes, two phases). Normalization removes one. Global phase unobservability removes another. What remains is a 2-dimensional manifold of physically distinguishable states: the Bloch sphere surface. The two surviving degrees of freedom are exactly as you stated — $r_\alpha$ (which becomes colatitude $\theta$) and $\nu - \eta$ (which becomes azimuth $\varphi$).


One addition: the density matrix extends the Bloch sphere to include its interior. Pure states live on the surface (2 degrees of freedom). Mixed states live inside (3 degrees of freedom: the Bloch vector has unconstrained $x$, $y$, $z$ with $r \leq 1$). So the density matrix formalism adds back one degree of freedom — the "purity" $r$ — which encodes how much coherence has been lost.


When I take a pure state vector in some basis and form its self-outer product to form a density matrix: Is that resulting density matrix a gate?

Kiro
No — it's a projector, not a gate.


A gate must be unitary ($U^\dagger U = I$). The density matrix $|\psi\rangle\langle\psi|$ is idempotent ($\rho^2 = \rho$) and has eigenvalues 0 and 1, so it's not invertible and can't be unitary.


What it is: a projection operator. Applying $|\psi\rangle\langle\psi|$ to a state $|\phi\rangle$ gives $|\psi\rangle\langle\psi|\phi\rangle = c|\psi\rangle$ — it projects $|\phi\rangle$ onto the $|\psi\rangle$ direction and kills everything orthogonal. This is exactly what measurement does (collapse to an eigenstate), which is why projectors describe measurement but not reversible evolution.




So: a direction on the Bloch sphere (two real parameters) fully specifies a measurement basis.


red laser link


https://www.civillaser.com/index.php?main_page=product_info&products_id=326
