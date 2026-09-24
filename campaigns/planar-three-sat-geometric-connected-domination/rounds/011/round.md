# Round 011 — private-neighbor grid gadget

## Plan

Gap: an orthogonal drawing alone does not encode connected vertex cover as connected domination. Mechanism: scale the checked grid routes, subdivide every drawn edge into unit steps, and attach one unused integer-grid neighbor to each path vertex except the two endpoint connectors. Try to choose these neighbors as independent pendant leaves, strengthening Clark's published construction and making every middle path vertex forced in any connected dominating set. Earlier experience on unintended geometric adjacencies applies directly, so enumerate them exactly. First check: build the point sets for prepared graphs and verify that every intended leaf has exactly one neighbor, all route intersections are intended, and the resulting graph matches the abstract path-plus-leaf gadget. If any case fails, retain its coordinates and repair placement before making a correctness claim.

## Evidence and diagnosis

[`grid.py`](grid.py) scales every validated orthogonal core route by ten, adds each connected-cover pendant endpoint four grid steps from its parent in an unused compass direction, inserts all intermediate integer grid points, and places one new side point beside every nonconnector path point. It checks that the main grid paths have exactly their intended unit adjacencies; each side point is adjacent to exactly one main path point; and each side point is adjacent to at most two other side points. The produced point coordinates are distinct integers, so the unit-distance graph is exactly this grid graph.

The initial stronger proposal required the side points to be independent pendant leaves. A two-choice implication graph in `independent_points` proves this selection **infeasible** on prepared case 1 at scales 10 and 11: around a right-angle turn, neighboring path points can have only incompatible side choices. The exact failure is retained in the script, and the reusable limited finding is [recorded](../../../../research/experience/independent-side-neighbors-at-grid-turns.md). This refutes only the stronger side-point restriction. The revised `clark_points` uses permitted side chains and validates maximum side degree two.

Command: `uv run --locked --with tsmpy --with matplotlib python campaigns/planar-three-sat-geometric-connected-domination/rounds/011/grid.py`. Result: 111/111 nonempty prepared instances passed exact geometry checks. For 98 SAT cases, an explicit connected-cover witness was converted to an exact-budget connected dominating set and checked for domination and connectedness in the actual integer-grid graph. The largest observed instance had 202,170 points, including 98,160 nonconnector path points, across 2,196 routed original edges. The 14 NO cases have **not** been independently solved as target instances. These checks establish the forward witness direction on finite cases, not the converse or arbitrary-output decoder.

First discriminating check: **published side-chain geometry supported on the prepared cases; independent-pendant variant refuted for this route**. General coordinate reliability and normalization remain open.

Experience extraction: [one new finite counterexample entry](../../../../research/experience/independent-side-neighbors-at-grid-turns.md).

## Next action

Develop a polynomial decoder that transforms every valid connected dominating set into a connected vertex cover, including outputs containing side-chain vertices.
