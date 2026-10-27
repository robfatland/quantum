# Mathematics

For expediency some of the interesting but slightly peripheral math is located here. 


## Definition of a Hilbert space


### Example: an inner product space that is not complete


**This section is not really critical path. Consider building a `Digressions` folder?**


Let $V$ be the set of all continuous functions $f: [0, 1] \to \mathbb{R}$, with inner 
product:

$$\langle f, g \rangle = \int_0^1 f(x) \, g(x) \, dx$$

This satisfies all the inner product axioms (linearity, symmetry, positive-definiteness). 
It is a perfectly valid inner product space — but it is **not** complete.

Consider the sequence of continuous functions:

$$f_n(x) = \begin{cases} 0 & \text{if } x \in [0, \tfrac{1}{2} - \tfrac{1}{n}] \\ \text{linear ramp} & \text{if } x \in [\tfrac{1}{2} - \tfrac{1}{n}, \tfrac{1}{2} + \tfrac{1}{n}] \\ 1 & \text{if } x \in [\tfrac{1}{2} + \tfrac{1}{n}, 1] \end{cases}$$

Each $f_n$ is continuous (the ramp connects 0 to 1 smoothly). As $n \to \infty$, the ramp 
gets steeper and the functions "try to converge" to the step function:

$$f(x) = \begin{cases} 0 & x < \tfrac{1}{2} \\ 1 & x > \tfrac{1}{2} \end{cases}$$

This is a Cauchy sequence in the $L^2$ norm ($\|f_n - f_m\| \to 0$ as $n, m \to \infty$), 
but the limit $f$ is **not continuous** — it has a jump at $x = 1/2$. The limit does not 
live in $V$. The sequence converges to something *outside the space*. There is a "hole."

The fix: enlarge the space to $L^2([0,1])$ — the space of all square-integrable functions 
(not just continuous ones). Now step functions are included, the Cauchy sequence has its 
limit, and the space is complete. $L^2([0,1])$ with this inner product is a Hilbert space.

The analogy is: continuous functions on [0,1] are to $L^2$ as $\mathbb{Q}$ is to 
$\mathbb{R}$. Completion fills the holes.


### Examples

| Space | Inner Product | Notes |
|-------|--------------|-------|
| $\mathbb{R}^n$ | $\langle x, y \rangle = \sum_{i=1}^n x_i y_i$ | Finite-dimensional, automatically complete |
| $\ell^2$ | $\langle x, y \rangle = \sum_{i=1}^\infty x_i \overline{y_i}$ | Space of square-summable sequences |
| $L^2([a,b])$ | $\langle f, g \rangle = \int_a^b f(t)\overline{g(t)}\, dt$ | Completion of continuous functions |


### Important Properties

1. **Riesz Representation Theorem:** Every bounded linear functional on $\mathcal{H}$ can be represented as an inner product with a fixed element.

2. **Orthonormal Bases:** Every Hilbert space admits an orthonormal basis $\{e_i\}$ such that any $x \in \mathcal{H}$ can be written as:
$$x = \sum_i \langle x, e_i \rangle \, e_i$$

3. **Projection Theorem:** For any closed subspace $M \subseteq \mathcal{H}$, every element $x$ has a unique decomposition:
$$x = x_M + x_{M^\perp}, \quad x_M \in M, \quad x_{M^\perp} \in M^\perp$$


### Why Completeness Matters

Without completeness, we lose:
- Convergence guarantees for orthogonal expansions
- The projection theorem (closest point in a closed subspace)
- The spectral theorem for self-adjoint operators
- The foundation for quantum mechanics, where states live in $\mathcal{H}$
