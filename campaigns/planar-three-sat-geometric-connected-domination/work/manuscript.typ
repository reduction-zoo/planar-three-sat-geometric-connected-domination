#import "report.typ": research-report
#show: research-report.with(
  title: "An executable reduction from planar 3-SAT to geometric connected domination",
  date: "24 September 2026",
  status: "Reconstruction of published constructions · Awaiting expert review",
)
#set math.equation(numbering: "(1)")

#heading(numbering: none)[Abstract]
We reconstruct a deterministic polynomial-time reduction from embedded planar
3-SAT to connected domination on explicitly given integer points. The reduction
composes variable cycles and clause triangles, a planar connected-cover
augmentation, and the grid construction of Clark, Colbourn and Johnson. A
visibility representation with a finite catalog of routing templates supplies
explicit coordinates. Recovery normalizes an arbitrary valid target witness,
then extracts a satisfying assignment; it also handles the no-solution output.
The construction uses quadratically many points with logarithmic coordinate bit
length. The contribution is an executable, inspectable reconstruction with
independent finite checks for a known hardness result.

= Introduction

A connected dominating set selects vertices that both cover a network and
communicate through selected vertices. Geometric graphs make the representation
part of the problem: coordinates must create the required edges without adding
unintended ones. A hardness statement alone does not specify a usable map from
formula encodings to point sets or a decoder for arbitrary target witnesses.

Lichtenstein's planar constructions [L82] and the connected-cover augmentation
of Garey and Johnson [GJ77] provide combinatorial stages. Clark, Colbourn and
Johnson [CCJ90, Section 6] prove connected-domination hardness for grid graphs.
Tamassia and Tollis [TT86] supply a visibility representation from which an
orthogonal drawing can be constructed. We combine these ingredients into one
reproducible rule, including deterministic tie-breaking, degenerate inputs,
integer coordinates, and recovery of every valid output. We do not claim that
this is the first implementation of these constructions.

*Theorem 1 (Executable reconstruction).* Let $phi$ be a three-literal CNF formula
with a planar rotation system of its variable–clause incidence graph. There are
deterministic polynomial-time maps $F$ and $G$ such that $F(phi)$ is a legal
rational-point connected-domination instance and
$ y in S_(B)(F(phi)) ==> G(phi,y) in S_(A)(phi). $
Here $S_A$ and $S_B$ are the valid-output sets defined below, including the
no-solution output. If $phi$ has $n$ variables and $m$ clauses, $F(phi)$ uses
$O((n+m)^2)$ integer points, with $O(log(2+n+m))$ bits per coordinate.

The proof follows the three graph interfaces in @sat-cover,
@connected-cover and @geometric. @drawing gives the coordinate
construction. The supplied implementation is the algorithm of the theorem;
the verification appendix records its checked revision and evidence limits.

= Instances and output semantics

A source instance specifies $n$ variables, $m$ clauses of exactly three signed
literal occurrences, and a clockwise rotation at every incidence vertex.
Repeated literals remain separate occurrences but induce one incidence edge.
Empty formulas and isolated variables are allowed. A valid source output is a
Boolean vector of length $n$ satisfying every clause. The distinguished answer
#smallcaps[no-solution] is valid exactly when no such vector exists. All graphs
and rotations are explicit, so their encoding includes the isolated variables.

A target instance is a nonempty finite set $P subset QQ^2$ of distinct points
and a nonnegative integer $K$. Two points are adjacent exactly when their
squared Euclidean distance is at most one. A valid witness is a subset
$D subset.eq P$ with at most $K$ points, such that every point lies in $D$ or
has a neighbor in $D$, and the graph induced by $D$ is connected. The empty
set is not connected here. The answer #smallcaps[no-solution] is valid exactly
when no witness exists. A target witness is encoded by distinct indices in the
ordered point list.

The forward map first runs ordinary unit propagation, discarding repeated
literals within a clause for that check and ignoring tautologies. A derived
contradiction yields the one-point instance with $K=0$. Otherwise the formula
used below is unchanged. An empty formula with no variables yields one point
with $K=1$. These branches are polynomial and preserve the output semantics.

= From planar SAT to planar cover <sat-cover>

For a variable with $d$ occurrences, make an even cycle with
$2 max(2,d)$ vertices. Its alternating classes represent true and false.
Allocate a distinct pair of cycle positions to each occurrence in the supplied
incidence order, and attach the occurrence to the vertex of its literal's
parity. For each clause, make a triangle with one vertex per occurrence and
join that vertex to its literal port. Parallel occurrences along one incidence
edge are expanded in opposite orders at its ends. This preserves the planar
rotation. Denote the resulting graph by $Q$ and its edge count by $e_Q$.
Every vertex of $Q$ has degree two or three. Set
$ B = sum_(i=1)^n max(2,d_i) + 2m. $ <cover-budget>

@clause-figure shows the complete gadget for one repeated-literal clause.
The use of distinct ports is relevant even when the incidence graph has only
one edge between the variable and the clause.

#figure(image("figures/clause.svg", width: 76mm), caption: [
  A six-cycle for one variable and a triangle for the clause
  $(x or x or x)$. Each $T_i$ has its own clause edge; $F_i$ is the opposite
  parity. Filled vertices choose the true parity and two triangle vertices,
  forming a cover of size five. All nine vertices and twelve edges are shown.
]) <clause-figure>

*Lemma 2 (Lichtenstein's cover interface).* The formula is satisfiable if and
only if $Q$ has a vertex cover of size at most $B$. Every such cover determines
a satisfying assignment.

_Proof._ A satisfying assignment selects one parity of each variable cycle.
In each clause triangle, omit a vertex whose literal is true and select the
other two. Every cycle and triangle edge is covered, and the edge incident
with the omitted triangle vertex is covered by its selected literal port.
The count is @cover-budget.

Conversely, a cycle of length $2r$ needs at least $r$ vertices in any cover,
and each triangle needs two. The disjoint cycle and triangle subgraphs already
require $B$ vertices. A cover within the bound therefore meets every local
lower bound exactly. A cover of an even cycle at this lower bound is one of
its two alternating classes: a missing vertex forces both neighbors, and
propagating the equality in the bound forces alternation around the cycle.
Read that parity as the variable value. Each omitted triangle vertex forces
its literal port into the cover, so each clause is satisfied. The four-cycle
for an isolated variable gives either legal Boolean value. This is the
explicit interface used from [L82, Section 4, Theorem 3]. $square$

= From planar cover to connected cover <connected-cover>

Replace each edge $u v$ of $Q$ by the path $u,a,b,v$. Enumerate the faces of a
planar embedding. For each face, and for each distinct boundary vertex whose
current degree is below four, add a spoke to a new vertex $w$ and add a pendant
neighbor of $w$. Join the new $w$ vertices of that face in their cyclic boundary
order. For disconnected $Q$, merge one chosen outer face per component into a
single exterior boundary before adding its cycle. All enumeration follows fixed
insertion order. Write $H$ for the augmented graph and $r$ for the number of
spoke vertices $w$. Its connected-cover budget is
$ B' = B + e_Q + r. $ <connected-budget>

The augmentation is illustrated in @faces-figure on a triangle. In the actual
reduction, the input is the cycle-and-triangle graph $Q$ above. Each face cycle
has at least three distinct spokes; subdivision provides boundary vertices
even when an original edge borders the same face twice.

#figure(image("figures/face-cycles.svg", width: 82mm), caption: [
  Complete face augmentation of a triangle after two subdivisions per edge.
  Squares are original vertices; the other unfilled vertices on the middle
  ring are subdividers. Filled vertices are the two face cycles, each with
  spokes and pendant neighbors. The labeled path is $u,a,b,v$. All 45 vertices
  and 63 edges are shown. This example illustrates both an interior face and
  the exterior face.
]) <faces-figure>

*Lemma 3 (Connected-cover interface).* The graph $H$ is connected, planar, and
has maximum degree four. A cover of $Q$ of size at most $B$ extends to a
connected cover of $H$ of size at most $B'$. Every connected cover of $H$ within
that bound yields a cover of $Q$ within $B$.

_Proof._ Face cycles and their spokes are drawn within their faces; the common
exterior cycle joins distinct components. Every spoke consumes an available
incidence at its boundary vertex. A new $w$ has two cycle neighbors, one spoke
neighbor and one pendant neighbor, giving degree four.

Given a cover of $Q$, choose $a$ on a subdivided edge when $u$ is selected and
choose $b$ otherwise; in the latter case $v$ is selected. Add every $w$. This
covers each subdivided edge and all new edges. The face cycles connect through
selected subdividers across shared edges, and the selected original vertices
have spokes to these cycles. The merged exterior cycle handles disconnected
components. This is the connected extension of [GJ77, Lemma 2], with one
subdivider per original edge and all $r$ spoke vertices.

In the reverse direction, a connected cover must contain each $w$. Omitting it
would force its pendant neighbor into the cover and isolate that selected
neighbor from the other selected vertices. Every subdivided edge uses at
least one of $a,b$. If neither original endpoint is selected, it uses both.
Keep the selected original vertices and add one endpoint of each such
uncovered original edge. Charging each added endpoint to the extra subdivider
gives at most $B'-r-e_Q=B$ vertices. Extra selected pendants can only reduce
this available budget. $square$

The leaf-free core of $H$ is biconnected. To see the needed premise, delete one
original vertex or subdivider. Its neighbors reconnect around the face cycles
between consecutive incident edges. When an adjacent original vertex lacks a
spoke on that face, the next subdivider on its other incident edge supplies
one. Thus the subdivided components remain joined, with the exterior cycle
also joining distinct original components. If a face-cycle vertex is deleted,
the remainder of its cycle stays connected, and its spoke neighbor reaches
that remainder through another boundary subdivider. These exhaust the core's
vertex types. The core has at least three vertices.

= Explicit orthogonal coordinates <drawing>

We describe the total coordinate construction before its bounded compact
implementation option. Let $v_H$ be the number of vertices in the core.
Choose its first edge $s t$. Biconnectivity supplies an $s$–$t$ path after
removing this edge. Start an order with that path. While vertices remain,
choose the first outside component and its first two neighbors $a,b$ in the
current order. Biconnectivity ensures that these neighbors are distinct.
Insert the internal vertices of an $a$–$b$ path through the component directly
after $a$. Materialize induced graphs in parent node and edge order, so all
component and shortest-path choices have fixed tie-breaking.

Each inserted vertex has an earlier and a later neighbor; old vertices retain
those neighbors. The final order orients the edges acyclically with unique
source $s$ and sink $t$. Use the face to the left of $s t$ as the exterior.
The plane $s t$-graph visibility theorem [TT86, Algorithm W-VISIBILITY,
p. 328; Theorem 1, p. 330] gives consecutive incoming and outgoing incidences
and an acyclic left-to-right face dual when the arc for $s t$ is omitted.
Let $rho$ be distinct topological ranks of that dual and let $eta$ be the
vertex order. Draw each non-$s t$ edge vertically at the rank of its left face,
between its endpoint heights $eta$. Draw $s t$ at column $-1$. Each vertex bar
spans its incident columns.

These coordinates instantiate the cited visibility construction. In its
strict-potential formulation, take face potentials $2rho$ and edge column
$2rho("left")+1$, with exterior edge column $-1$, then apply the affine
map $x mapsto (x-1)/2$. Every dual inequality remains strict. Tightening a bar
to the span of its incidences creates no intersections, including when that
span is a single point. Coordinates and the number of bars are $O(v_H)$.

To replace bars by point vertices, list their distinct columns from left to
right and record whether each has an incidence above, below, or both. With
degree two through four there are 46 patterns. A fixed certificate for each
pattern consists of simple orthogonal paths from one center to terminals at
$(2i+1, plus.minus 4)$ for $i=0,dots,k-1$, where $k$ is the number
of columns. The paths lie in $[0,2k] times [-4,4]$. Paths intersect only
at the center and meet the strip boundary only at their terminals. The
complete finite catalog is supplied with an exhaustive independent validator.
It is data used by the algorithm; no solver runs to choose a template.

Multiply bar coordinates by 20. Map odd template abscissas to the actual
incidence columns, internal even abscissas to the midpoints of consecutive
columns, and exterior abscissas to four units beyond the extreme columns.
This strictly increasing integer map preserves disjointness and orthogonality.
Translate heights by the scaled bar height and join matching terminals along
the original vertical segments. Vertex strips are at least twelve units apart.
A nonincident edge is at least twenty units beyond the unextended bar span,
so the four-unit margin cannot reach it. The resulting drawing has $O(v_H)$
bends, $O(v_H)$ coordinate magnitude and $O(v_H^2)$ total lattice route length.

The executable rule first permits a compact TSM drawing only for cores with
at most 1,000 vertices and at most 50,000,000 Python line events. Vertices are
renumbered by insertion order before this call, preventing hash-dependent
set choices in the locked planar-drawing dependency. An exception or exhausted
allowance selects the visibility construction above. A compact result is
accepted only after checking integer coordinates of magnitude at most
$100v_H$, at most $100v_H$ drawn vertices, and exact topology and nonintersection.
The finite operation allowance is independent of elapsed time. This bounded
option affects coordinates but leaves the proved drawing interface unchanged.

= From connected cover to geometric domination <geometric>

Scale the core drawing by ten. Restore each original pendant vertex four grid
steps from its neighbor in the first unused compass direction. Insert every
integer point on each routed edge. Let $V_1$ be the points for the vertices of
$H$, and let $V_2$ be the interior path points. On each path its first and last
interior points are _connectors_; the other interior points are _middle points_.
Every path has at least three interior points.

For each middle point, in lexicographic order, add the first grid neighbor in
east, north, west, south order that has that middle point as its unique main-path
neighbor. Call the new set $V_3$. Scale-ten separation makes these choices
available and distinct. A side point has no original-vertex or connector
neighbor. Its other side neighbors, at most two, belong to adjacent middle
points on the same path. @route-figure displays the straight-path case.
At bends the same local adjacency conditions hold; separated strips and routed
edges prevent contacts with unrelated paths. The implementation checks all
these adjacencies exactly.

#figure(image("figures/grid-route.svg", width: 145mm), caption: [
  The exact grid graph of one straight route of length ten. Squares are
  original endpoints, unfilled lower circles are connectors, filled lower
  circles are middle points, and the upper row contains their side points.
  Every unit-distance edge is drawn. Side points may form a chain; they are
  not assumed to be isolated leaves. Other routes incident with $u$ and $v$
  are omitted from this local illustration.
]) <route-figure>

Write $N_1=|V_1|$, $N_2=|V_2|$, and $e_H=|E(H)|$. Emit
$ P=V_1 union V_2 union V_3, quad K=B'+N_2-e_H+N_1-1. $ <target-budget>
The points are distinct integers. On integer points Euclidean distance at most
one is exactly grid adjacency, so the described graph is the target graph.
The budget is nonnegative: every path contributes at least three points to
$V_2$ and $H$ is nonempty.

*Lemma 4 (Forward domination witness).* A connected cover $C$ of $H$ gives a
connected dominating set of size $|C|+N_2-e_H+N_1-1$.

_Proof._ Choose a spanning tree of $H[C]$ and attach each omitted vertex to a
neighbor in $C$. This gives a spanning tree on all $N_1$ vertices. Select the
points for $C$, all middle points, both connectors of each tree edge, and one
connector incident with $C$ on every other edge. The selected points are
connected along this tree. They dominate omitted originals, omitted
connectors and all side points. There are $N_2-2e_H$ middle points and
$e_H+N_1-1$ selected connectors, giving the count. $square$

*Lemma 5 (Recovery from arbitrary target witnesses).* Every connected
dominating set $D$ of size at most $K$ can be transformed, without increasing
its size, into one containing no side points. Its selected original vertices
then form a connected cover of $H$ of size at most $B'$.

_Proof._ We use the constructive replacement argument of [CCJ90, Lemma 6.1].
Pair each middle point with its side point. If every pair on a route contains
a selected point, replace selected side points by the corresponding middle
points. If a pair is missing, its side point must be dominated by a selected
neighboring side point. A selected connection to an endpoint crosses the
pairs on one side of that missing pair. It uses both layers in at least one
pair along the connection, which pays for the extra middle point at the
missing pair. Replace the selected side points on that prefix or suffix by
middle points and add the missing middle point. The replacement preserves
connectivity and domination without increasing cardinality.

The decoder enumerates these prefixes and suffixes in route order and checks
cardinality, domination and connectivity before accepting one. The preceding
argument supplies an acceptable move whenever a side point remains. Each move
strictly decreases the number of selected side points, so the process ends.
This makes the minimal-set argument in the cited lemma into an explicit
algorithm and applies to every valid $D$, not only an optimum witness.

Without selected side points, every middle point is selected, since it must
dominate its side point. Each route needs a connector incident with a selected
original endpoint. Thus the selected originals form a cover $C$ of $H$.
Their connectivity can only pass between originals through complete routes,
so $H[C]$ is connected, as in [CCJ90, Lemma 6.2]. Every omitted original needs
an additional selected connector on an incident edge to be dominated, and
connecting $C$ needs at least $|C|-1$ edges with both connectors selected.
These edge classes are disjoint. Consequently the normalized witness satisfies
$ |D| &>= |C| + (N_2-2e_H) + e_H + (N_1-|C|) + (|C|-1) \
       &= |C|+N_2-e_H+N_1-1. $ <recovery-bound>
Together with @target-budget this gives $|C|<=B'$. $square$

= The complete rule and its bounds <correctness>

To recover a source witness, reconstruct the identical point list from the
source, interpret the selected indices, apply Lemma 5, use the endpoint
charging in Lemma 3, and read the variable parities in Lemma 2. The empty-source
branch returns the empty Boolean vector. The contradictory-unit branch has no
valid witness to decode. If the target answer is #smallcaps[no-solution],
return that answer for the source: Lemmas 2–4 show that a source witness would
have produced a target witness, and Lemma 5 supplies the converse implication.
This proves Theorem 1 for all legal source instances and all valid target
outputs.

The graph sizes through $H$ are linear in $n+m$. The visibility algorithm uses
at most $v_H$ ear insertions and polynomial graph searches; its template
catalog is constant size. Its route length is quadratic. The accepted compact
option has the same asymptotic output bounds and bounded work. Scaling and
adding side points preserve the quadratic size and logarithmic coordinate bit
length. All comparisons are exact on these integers.

Recovery rebuilds this polynomial-size instance. It accepts at most $|V_3|$
normalization moves. Each pass enumerates polynomially many route intervals
and performs explicit finite graph checks, each polynomial in $|P|$ and the
coordinate bit length. The remaining cover and parity extraction is
polynomial. Thus both maps have worst-case polynomial running time in their
respective input encodings, with the forward encoding bound stated in
Theorem 1.

Determinism includes dependency behavior. Induced visibility graphs preserve
insertion order; compact inputs use small integer labels; the locked flow
implementation enumerates nodes and edges into indexed arrays. Generated
labels enter ordered dictionaries. Grid routes follow ordered graph traversal,
and output points are lexicographically sorted. Arbitrary traversal used only
to test connectedness affects a Boolean predicate, not point ordering. The
same source therefore gives the same indexed coordinates in separate forward
and recovery processes. Dependency upgrades require a renewed audit of this
implementation correspondence.

= Conclusion

The reconstructed rule supplies explicit integer coordinates and an executable
decoder for arbitrary valid target outputs. It realizes the known grid-graph
hardness route with a total polynomial drawing construction. The implementation
is intended for inspection and reproduction: the quadratic expansion has large
constants, and no practical large-instance solver advantage is claimed.
Independent finite checks support the implementation, while the general claim
rests on the composed arguments and cited interfaces. Expert mathematical
review and a formal proof certificate remain distinct from these checks.

#heading(numbering: none)[References]

[L82] D. Lichtenstein. #link("https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lichtens.pdf")[
_Planar formulae and their uses._] SIAM Journal on Computing 11(2), 329–343, 1982.

[GJ77] M. R. Garey and D. S. Johnson.
#link("https://doi.org/10.1137/0132071")[_The rectilinear Steiner tree problem
is NP-complete._] SIAM Journal on Applied Mathematics 32(4), 826–834, 1977.

[CCJ90] B. N. Clark, C. J. Colbourn and D. S. Johnson.
#link("https://cs.du.edu/~snarayan/sada/research/docs/res/unitdisk.pdf")[_Unit disk graphs._]
Discrete Mathematics 86(1–3), 165–177, 1990.

[TT86] R. Tamassia and I. G. Tollis.
#link("https://workshop.tcs.uj.edu.pl/mszana2015/gutkraw/unified.pdf")[_A unified
approach to visibility representations of planar graphs._]
Discrete & Computational Geometry 1, 321–341, 1986.

#set heading(numbering: "A.")
#counter(heading).update(0)
= Verification and reproducibility

The checked candidate is commit `72e1365`, with implementation repair at
`ad75146`. The independent assessment at `reviews/deterministic-repair/review.md`
returned advance and reused the unaffected mathematical findings from the
first review. This is an agent assessment for expert review, not human
certification or publication acceptance. The review began in a fresh registered
reviewer context; its isolation boundary was instructional rather than a
filesystem sandbox. The focused follow-up retained that review's findings.

The original prepared corpus contains 112 explicit sources, up to six variables,
including 100 seeded random cases and twelve edge cases. Source labels were
obtained by exhaustive independent enumeration. The current complete
forward/target-solve/recovery loop passed 195 witness outputs and fourteen exact
negative outputs. Each of the 97 nontrivial geometric positive targets supplied
two distinct witnesses. The empty source supplied one. Negative targets in this
corpus are the actual one-point outputs of the unit-contradiction branch;
no nontrivial geometric negative target has an independent certificate here.
The largest prepared target has 202,170 points.

The target-only witness finder receives coordinates, not source assignments or
candidate metadata. It recognizes a subdivided backbone, uses cover folding and
search, and proposes selected point indices. An independent exact
rational-distance validator checks the full target witness. Failure of this
incomplete search is unknown, never a negative answer; the complete generic
oracle handles remaining targets. Its cover kernel was checked against
exhaustive optima and below-optimum budgets on 209 small atlas graphs. Earlier
generic separator solving independently established an optimum on a
1,596-point target; larger unsuccessful runs are retained as execution failures.

Additional current checks cover twelve side-chain alternatives, all 46 port
patterns, and 174 complete fallback layouts. Cross-process tests explicitly
exercise the real fallback by exhausting the existing compact allowance at zero:
the emitted 330,596-point target has a separately validated witness of size
165,357 and valid recovery under different hash seeds. This source has no
clauses. An independent reviewer separately solved a new clause-bearing
12,418-point default target and checked recovery under two further seeds.
A 1,292-core-vertex asymmetric source was checked through its accepted default
fallback drawing under four seeds, with identical repaired coordinates. Its
full target was not expanded because of the observed memory cost. These
scopes distinguish branch checks, complete solved targets and proof.

Prerequisites used on 24 September 2026 were uv 0.12.17, Python 3.12.14,
NetworkX 3.7, Z3 bindings 5.1.0.0, tsmpy 0.9.3, and Typst 0.15.1.
Python dependencies are locked in `uv.lock`; the library versions are part of
the ordering audit. No Lean certificate was requested or produced. Mathlib was
not available on the current Lean search path. No remote repository or board
publication is part of this result.

#block(breakable: false)[
From the repository root, use the following commands. Paths below use a shell
variable only to keep lines readable.

```sh
uv sync --locked
campaign=campaigns/planar-three-sat-geometric-connected-domination
uv run --locked python "$campaign/work/check.py" --self-test
uv run --locked python "$campaign/work/check.py" \
  --candidate "$campaign/work/algorithm.py"
uv run --locked python "$campaign/work/verify.py" \
  --candidate "$campaign/work/algorithm.py"
uv run --locked python "$campaign/rounds/018/alternate_witnesses.py"
uv run --locked python "$campaign/rounds/032/test_templates.py"
uv run --locked python "$campaign/rounds/033/test_layout.py"
uv run --locked python "$campaign/rounds/039/check_reconstruction.py"
uv run --locked python \
  "$campaign/reviews/deterministic-repair/check_recovery.py"
```

]

The two public map modes consume and emit JSON:

```sh
uv run --locked python "$campaign/work/algorithm.py" \
  < source.json > target.json
uv run --locked python "$campaign/work/algorithm.py" --extract \
  < recovery-input.json > source-output.json
```

The recovery input has keys `source` and `target_solution`; the latter is a
list of distinct point indices or the string `NO-SOLUTION`. Source JSON has
keys `variables`, `clauses`, and `embedding`; target JSON has `points` and `K`.
The full schemas are in `work/contract.md`. The finite routing certificates are
in `rounds/032/templates.json`. Detailed logs are retained under `rounds/039/`
and the two review directories, including the original failing hash-order
example. Reproducible bulk point dumps are excluded; their source generators,
seeds, candidate revisions and output digests remain available.

To rebuild this document and its checked vector figures:

```sh
uv run --locked python "$campaign/work/figures/draw.py"
typst compile "$campaign/work/manuscript.typ" \
  "$campaign/work/manuscript.pdf"
```
