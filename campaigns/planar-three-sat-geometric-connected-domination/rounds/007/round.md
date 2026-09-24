# Round 007 — composed construction and verification scale

## Plan

Gap: the later Grid Tiling route has a proved source bridge and one checked local block interface, but its full geometry and independent target verification remain open. Hypothesis: the published 16-block square can be transcribed into a practical candidate for the prepared 112 cases. First discriminating check: compute a lower bound on target point counts from the 16 Y-blocks alone for each prepared case that has no trivial empty tile cell; compare the smallest genuine NO case with the current independent target oracle's exact graph and reachability encoding. Also inspect Fig. 3 and §2.4 to identify whether primed-block offsets and rational perturbations are fully specified. A modest count with explicit coordinates would justify implementation; a very large count or ambiguous placement would make this route a poor fit for the current campaign's required full injection tests. Prior evidence: rounds 004–006. The geometry lessons apply; the Grid Tiling bridge is fixed by round 005.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/007/route_scale.py` ran on 2026-09-23. The [2019 construction](https://link.springer.com/article/10.1007/s00453-019-00561-0), §2.4, uses 16 Y-blocks per tile gadget, each containing `N²+1` points for alphabet size `N`. Round 005's bridge makes `N=3m` and a grid of `m²` gadgets for `m` clauses. Thus the Y-blocks alone contain `16m²(9m²+1)` points. The smallest prepared unsatisfiable case without an empty tile cell is case 11 with `m=3`, requiring at least 11,808 Y points. Case 13 has `m=10` and requires at least 1,441,600 Y points. These bounds exclude X-blocks, parent/leaf points and connectors.

The prepared independent target checker materializes exact pairwise distances and a vertex-by-layer reachability encoding. For 11,808 points, pairwise distances exceed 69 million; for 1,441,600 points, they exceed one trillion. This route cannot complete the required full injected-corpus check with the current independent oracle. This is a practical verification obstruction, not a mathematical lower bound on all reductions or all solvers. The paper's Fig. 3 (printed p. 2970) shows the 16-block ring, but §2.3 lists offsets only for unprimed blocks and §2.4 says the block offsets are not modified without an explicit primed-block mapping. Its chosen `δ=1/√N` and `ξ=2−√(4−4δ²)` require a further explicit rationalization for this campaign's target encoding. Recovery of arbitrary noncanonical feasible CDS outputs also remains unimplemented.

The original local-cell route failed its tested equality-wire composition (round 003); the Lichtenstein route left its rational embedding omitted (round 001). The later Grid Tiling route is materially different and supplies a sound source bridge (round 005), but no complete geometric map or decoder has emerged. With 13 rounds available, this is a supported investment stop: further work would first need either a much smaller direct construction or a new independent target verification method, followed by a full coordinate reconstruction and normalization proof. It is not an impossibility result.

Experience extraction: [size growth of the composed route](../../../../research/experience/grid-tiling-route-size.md), created 2026-09-23. Closeout audit found no other missed reusable finding. The campaign has created three distinct entries, updated two of them, and has no pending promotion within this repository.

## Next action

Stop new discovery at seven rounds. Resume only with a concrete way to test the full geometric instances or a smaller construction whose exact coordinates and decoding can be specified.
