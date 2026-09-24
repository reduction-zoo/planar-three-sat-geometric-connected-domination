# Separator states can solve subdivided geometric CDS targets

## Claim and applicability

Tags: connected domination, tree decomposition, independent oracle, ladders. For targets with narrow graph separators, a generic tree-decomposition DP with boundary domination flags and selected-component partitions can outperform global reachability/flow encodings. Force one mandatory articulation vertex into every bag so a disappearing selected component is invalid. Otherwise enumerate a root in a vertex's closed neighborhood. This is an exact exponential-width solver, not a polynomial reduction algorithm.

## Evidence and status

[Round 024](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/024/round.md) matches 31 exhaustive small graph optima and solves the actual 1,596-point target at optimum 857. The graph is read from coordinates without candidate metadata. No independent review; no general efficiency claim.

## Consequence for search

Measure separator width before abandoning independent target solving. Global SAT/flow difficulties do not imply decomposition failure. State counts and joins can still grow exponentially.

## Use history

Created 2026-09-24. Intended destination is the board experience collection after separate authorization; no board write made.
