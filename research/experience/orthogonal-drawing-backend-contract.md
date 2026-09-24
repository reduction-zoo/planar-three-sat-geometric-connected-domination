# Orthogonal drawing theorem and backend contract differ

## Claim and applicability

Tags: orthogonal drawing, min-cost flow, fixed capacity, polynomial runtime. A theorem guaranteeing polynomial orthogonal drawings does not certify an arbitrary backend implementing the same pipeline. tsmpy 0.9.3 uses capacities and compaction total flow fixed at `2**32`, and NetworkX network simplex. A generated-family argument must justify capacities and the implementation's worst-case runtime, or replace these components.

## Evidence and status

[Round 021](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/021/round.md) demonstrates a two-face flow limit exactly. This is a dependency-level observation, not a source-instance counterexample or an impossibility result. No independent review.

## Consequence for search

Prefer a fully specified drawing algorithm with input-dependent integer bounds and a justified polynomial flow algorithm. Finite layout validation establishes neither totality nor a time bound.

## Use history

Created 2026-09-24 in round 021. Intended destination is the board's experience collection after separate authorization; no board write made.

Round 026 implemented an exact lower-bound flow solver and independently checked 80 tiny networks. Its O(QVE) bound is polynomial for orthogonal flow's O(V+E) supply. Rectangular compaction can use E units if its DAG/source-to-sink premises hold. These are scoped repairs, not a certification of the rest of tsmpy.

Round 028 found and repaired a separate floating-point external-face selection defect on exact near-parallel integer rays at magnitude 10^18. The experimental backend uses exact rational slope order and retained all 14 finite layout checks. This is a component counterexample, not a generated-source counterexample.

Round 029 passed all 163 biconnected planar max-degree-four atlas graphs, but the simple reflex-corner termination argument does not by itself cover tsmpy's exterior-frame bridge and repeated-boundary face walk. The all-input claim remains open at that precise operation.

Round 034 bypassed the remaining library-totality obligation with a deterministic finite compact-layout attempt (bounded core size, Python-line allowance, and exact output checks) followed by an explicit polynomial visibility fallback. Four forced-exhaustion layouts and all 111 prepared core layouts passed. This is a candidate construction/proof strategy, not yet independently reviewed.
