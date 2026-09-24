# Round 008 — grid graph route

## Plan

Gap: the available Grid Tiling geometry is too large for the current independent target checker, and the direct variable wire failed locally. Mechanism: use a polynomial-size grid graph connected-domination reduction, if one has a constructive proof from planar SAT or a source problem with an executable bridge. Integer grid points give an exact unit-disk representation: distance at most one means grid adjacency. Search scope: primary papers on connected domination in grid graphs and their cited hardness proofs. First discriminating check: find an explicit instance construction and recovery proof whose source can be reached from the fixed embedded planar 3-SAT input without solving it. A usable proof would support an executable F; a hardness assertion without F/G will be recorded as a lead only. The three previous experience entries were inspected; only the coordinate and size lessons apply.

## Evidence and diagnosis

Clark, Colbourn, and Johnson, [*Unit disk graphs* (1990), §6, Theorem 6.1](https://cs.du.edu/~snarayan/sada/research/docs/res/unitdisk.pdf), explicitly reduce connected vertex cover in a connected planar graph of maximum degree four to connected domination in a grid graph. Their input graph is drawn with rectilinear edges, then represented by integer points on paths plus private leaves. They state the budget as `k + |V2| - |E| + |V| - 1` and give both directions of the equivalence in Lemmas 6.1–6.2. Distinct integer grid points are adjacent at Euclidean distance at most one exactly when they are grid neighbors, so this is an exact rational-point target model. The source paper cites Garey and Johnson (1977) for the planar connected vertex-cover premise. This is a genuine smaller construction route, but it is a lead rather than F/G: it needs an explicit Planar 3-SAT-to-connected-vertex-cover bridge and a constructive rectilinear drawing from the given rotation system.

First discriminating check: **supported as a route**. The cited theorem provides a target construction and recovery argument, though neither is yet implemented or verified for this campaign. Actual F-produced instances solved: 0; recovered outputs: 0. No geometric claim from rounds 004–007 is reused in this route.

Experience extraction: none. This is an applicable published reduction rather than a newly established reusable failure or obstruction.

## Next action

Read the connected-cover source reduction and the planar-SAT-to-planar-cover construction, then audit their composition against the prepared source contract.
