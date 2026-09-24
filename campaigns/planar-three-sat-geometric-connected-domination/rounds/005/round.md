# Round 005 — clause choices to Grid Tiling

## Plan

Gap: the alternate unit-disk construction starts from Grid Tiling, while the fixed source is embedded planar 3-SAT. Mechanism: encode each clause's chosen true literal as a color class, connect choices that are not contradictory, and form a square Grid Tiling instance whose diagonal identifies each class choice and off-diagonal cells enforce pairwise compatibility. First discriminating check: independently solve each tiled instance with Z3 for all 112 prepared formulas, compare YES/NO with the source oracle, and decode every returned tiling to a satisfying assignment. A pass proves only this polynomial intermediate bridge on finite cases; the unit-disk stage remains open. This mechanism differs from local geometric wires and uses no planarity assumption. Prior evidence: round 004's Grid Tiling target lead. Experience search found no entry for Grid Tiling or clause-choice compatibility; the existing geometry entries do not apply to this combinatorial bridge.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/005/grid_bridge.py` passed on 2026-09-23: 112 fixed formulas, 98 tilable/satisfiable, 14 untilable/unsatisfiable; 12 instances have a cell with no compatible pair. The script builds the tile sets, solves the full square tiling constraints with Z3 independently of the source SAT oracle, and checks decoded assignments against the original clauses. The source labels came from Prepare, including an exhaustive cross-check. This is a finite test of the intermediate map and recovery.

General bridge argument: for `m` clauses, each of their three literal occurrences gets a distinct label, so the alphabet has `3m` labels. In cell `(a,b)`, use pairs `(label from clause b, label from clause a)` when the two literals are not opposite; on the diagonal allow only equal labels from clause `a`. The tiling equalities make first coordinates constant down each column and second coordinates constant across each row. The diagonal therefore selects one literal per clause, and every off-diagonal cell requires each pair of chosen literals to be consistent. They extend to a Boolean assignment satisfying every clause. Conversely choose one true literal per clause from any satisfying assignment; these choices form a tiling. If any tile set is empty, the formula is unsatisfiable. Empty formulas are trivially satisfiable. Construction takes `O(m²)` cells with at most nine pairs per cell, each label has `O(log m)` bits; tiling-to-assignment decoding is polynomial. The incidence embedding is unused, which is allowed by the fixed source contract.

This bridge is a complete combinatorial lemma but not F or G for geometric connected domination. The modern paper's coordinate construction and normalization of all target outputs remain unimplemented and unverified.

Experience extraction: none. The bridge is standard clause-choice compatibility, documented here as a proof component rather than a reusable new geometric finding.

## Next action

Audit the later paper's block offsets and exact adjacency properties on a single tile gadget before scaling to its connected construction.
