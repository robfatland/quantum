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