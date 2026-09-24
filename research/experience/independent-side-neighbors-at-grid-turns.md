# Independent side neighbors can fail at a grid turn

## Claim and applicability

Tags: grid graph, connected domination, path forcing, orthogonal bend, private neighbors. In the round-011 scaled orthogonal-route construction, demanding that every nonconnector path vertex have a *pendant* grid neighbor can make the placement constraints inconsistent. This excludes the particular independent-neighbor variant, not Clark's published construction, which permits neighboring side vertices.

## Evidence and status

Exact finite counterexample on prepared source case 1, checked by the two-choice implication graph in [`grid.py`](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/011/grid.py). At scale 10, path vertices `(10,-60)` and `(10,-59)` occur in a contradictory strongly connected component; `(10,-59)` has only candidate `(9,-59)`, while the adjacent turn constraints require incompatible choices. Scale 11 yielded the corresponding contradiction. See [round 011](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/011/round.md). No independent review. This is a finite-instance exclusion, not a theorem about all possible drawings or gadgets.

## Consequence for search

Retain Clark's permitted side-vertex chains and prove their normalization, or change the path geometry or forcing gadget. Do not assume that every side point can be made a graph-theoretic leaf on a unit-grid path with bends.

## Use history

- 2026-09-24: extracted from round 011; intended destination if promoted is the board's local shared experience collection, with no promotion or board edit during research.
- 2026-09-24: round 012 used Clark's allowed side chains; one alternate exact-budget target witness containing side vertices was normalized and decoded, supporting this repair on a finite case.
- 2026-09-24: round 018 independently validated and decoded 12 distinct side-chain target outputs across 1,596–202,170 points; this improves finite decoder coverage without proving all-output correctness.
