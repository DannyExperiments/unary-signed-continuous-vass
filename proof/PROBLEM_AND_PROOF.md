# Q1568: NL-completeness for fixed-dimensional unary signed continuous VASS

## Question and result

In Michal Ajdarów, A. R. Balasubramanian and Łukasz Orlikowski, *Reachability in Fixed-Dimensional Continuous VASS*, [CONCUR 2026 final proceedings, §6, printed p. 7:16/PDF p. 16](https://drops.dagstuhl.de/storage/00lipics/lipics-vol391-concur2026/LIPIcs.CONCUR.2026.7/LIPIcs.CONCUR.2026.7.pdf#page=16), the second future-work case is “unary d-CVASS with integer updates over Q-semantics for any d ≥ 2.” The reference to the two decision problems is in the preceding sentences; the input and rules are in §2. See also the [full author version](https://arxiv.org/html/2606.30042v1#S6) and [pinned catalog statement](https://github.com/10m-u/open-problems-catalog/blob/ca8d4d44ba3db527f19f28928c240168f545ecfe/problems/computer_science_ai/theory-of-computation-algorithms-part-1.md#q1568).

**Theorem.** For every fixed positive integer d, reachability and coverability of unary d-CVASS with integer update vectors under the unrestricted rational semantics are NL-complete under deterministic logspace many-one reductions. This includes the entire requested range d≥2. The two problems differ only in the endpoint condition. The proof is for signed rational counters and is not a result about nonnegative counters.

An edge e carries w_e∈ℤ^d. Each occurrence of e chooses its own rational α∈(0,1] and adds αw_e. There are no counter guards or restrictions on prefixes in the signed semantics. For input p(u),q(v), reachability asks for u plus the total update to equal v at q, and coverability asks for it to be coordinatewise at least v at q. Let N be the input length plus d+2. Numerical magnitude bounds below are polynomial in N for fixed d. In particular, the product D₀ of the 2d positive denominators in u,v is at most N^(2d). Each w_e has integer entries of magnitude at most N.

## 1. A fixed-support rational polyhedron

Start with a successful run, and let E′ be its exact edge support, distinguishing parallel edges. The empty support case already has a zero-length witness. Form the directed graph using just E′ and the vertices seen on the run. Its strongly connected component (SCC) condensation has no directed cycle. Thus the run visits its components in one sequence without returning to an earlier component, and the edges of E′ between components are exactly the one connecting edge per adjacent pair in that sequence. Each such edge occurs once. Call them bridges here (only in this proof's directed-condensation sense). All other supported edges are called internal.

Let x_e be the total weight assigned to e across the run. Every x_e is strictly positive; bridge x_e is at most 1; internal x_e has no required upper bound at this stage. Put b=v−u, and use the system
```
sum_(e in E′) w_e x_e − z = b,
0 ≤ ε ≤ 1,
x_e ≥ ε                       for all supported edges,
x_e ≤ 1                       for bridges,
z ≥ 0                         in the coverability case.
```
Here z is absent (equivalently zero) for reachability. The original run gives a feasible point with ε>0 by taking the minimum of 1 and all x_e. In coverability its excess endpoint gives z.

The polyhedron is pointed because all its coordinates are nonnegative. The maximum of ε is bounded and attained, and the maximizing face has a vertex. These are the standard fundamental theorem of linear programming and the vertex property of a nonempty pointed polyhedron. Alternatively, the feasible system has no line, and the maximizing face of a nonempty polyhedron with finite optimum is itself a nonempty pointed polyhedron. A vertex of a face is a vertex of the whole polyhedron. Fix such a vertex, so ε>0.

## 2. Polynomial denominators and magnitudes

At that vertex label x_e as pinned lower if x_e=ε, pinned upper if e is a bridge and x_e=1 but it has not been labeled lower, and free otherwise. A zero coordinate of z is pinned zero; the others are free. If ε=1, treat ε itself as pinned; otherwise it is a free variable. Substitute all pinned values into the d displacement equations. When ε is free its coefficient is the sum of the w_e for lower-pinned edges. If pinned at 1 their contribution moves to the right-hand side. Upper-pinned edges contribute only fixed integer vectors. Positive z-coordinate columns are negative unit vectors.

The resulting columns on free variables are linearly independent. If not, perturb the free variables in opposite directions along a nonzero kernel vector, allowing each lower-pinned x_e to move with ε, while keeping upper pins and zero slacks fixed. If ε is free it is strictly inside (0,1); all nonactive inequalities have strictly positive slack. For sufficiently small positive and negative perturbations, the chosen active equalities and all inequalities remain valid, contradicting extremality. The possible bridge pinch ε=x_e=1 stays fixed because ε is pinned in that case. Hence there are at most d free variables.

Select a nonsingular square minor of the displacement equations on the free columns. Its entries are integers of magnitude at most N², including the summed ε-column. The right-hand side is b minus a sum of integer update vectors of magnitude at most N² per coordinate. Multiplication by D₀ gives integer right-hand sides of magnitude polynomial in N. Cramer's rule now gives a single common denominator D dividing D₀ times the absolute minor determinant and bounds the numerators by determinants of order at most d with polynomial-size entries. We may take D equal to that product, which is a multiple of D₀. If there are no free variables take D=D₀. All pinned values, including those equal to ε, use the same grid. Thus D and every x_e are polynomially bounded, and every x_e D is a positive integer. The support can have many edges; only the *free part* has bounded dimension, which is why denominators from many independent edges do not multiply.

## 3. Reconstructing a short run on a common grid

For each supported SCC choose a walk inside it from its entry vertex to its exit vertex which traverses every internal edge at least once. This can be made by visiting the tails of the internal edges in any order via simple internal paths, taking the corresponding edges, and finally going to the exit by a simple path. For single-vertex SCCs the same argument includes loops. For the first/last components the entry/exit can be p/q. Join the walks using the supported bridges, each once. The walk has polynomial length.

If an internal edge e needs more occurrences to accommodate total weight x_e, insert ⌈x_e⌉ traversals of a closed detour containing e. Such a detour consists of e followed by an internal simple path from its head back to its tail, and can be inserted at an existing visit to its tail. This changes the other internal multiplicities but does not harm them, because weights have no required positive lower bound. It does not add bridge visits. Doing this for each needed edge leaves a supported walk of polynomial length L and multiplicities m_e≥x_e. All m_e≥1, and L≥1.

Use the new common denominator D′=DL. Because x_e D is a positive integer, x_e D′≥L≥m_e. Also x_e D′≤m_e D′. Hence the integer x_e D′ can be distributed among the m_e occurrences in positive integer shares between 1 and D′: give each occurrence one unit and distribute the remainder within their total remaining capacity. Set its actual multiplier equal to its share divided by D′. Then every occurrence is genuinely positive, no multiplier exceeds 1, and sum_e w_e x_e is exactly the endpoint update. The signed semantics has no prefix condition, so the reconstruction preserves legality. This proves existence of a successful run with both length and a single common firing denominator bounded by polynomials depending only on d. The construction treats strict positivity and the bridge cap separately.

## 4. Logspace algorithm and hardness

For fixed d choose polynomial upper bounds on D′ and L as supplied by the preceding proof. A nondeterministic logspace machine guesses a positive D′ within the bound, and guesses each edge and a numerator a∈[1,D′], for at most the length bound. Verify the edge endpoints and keep the current state, step count, and d integer sums ∑ a w_e for the guessed prefix. Every sum is polynomially bounded in absolute value. At q, compare the sums divided by D′ plus the input u with v, using constant-coordinate integer cross products; these are polynomially bounded too. It can also accept the empty witness where valid. This uses O(log N) work space. The grid lemma gives completeness, and every accepting computation describes an actual run, giving soundness.

For hardness reduce directed graph reachability, using the graph as control and every update and endpoint value zero. Both reachability and coverability then hold exactly when a directed control walk exists. This reduction is deterministic logspace and works in every fixed d. Together the bounds give NL-completeness.
