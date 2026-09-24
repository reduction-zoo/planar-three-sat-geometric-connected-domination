# tsmpy face traversal needs a graph-sized recursion allowance

## Claim and applicability

Tags: orthogonal drawing, tsmpy, planar graph, Python recursion. `tsmpy` 0.9.3 can hit Python's default recursion limit while orienting faces of a legal, connected, biconnected degree-four planar input with roughly two thousand vertices. A wrapper that raises the recursion allowance with graph size avoids this particular execution failure. This says nothing about drawing correctness or totality for all inputs.

## Evidence and status

The exact legal source `chain(20)` and traceback are retained in [round 016](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/016/failure.md). The wrapper repair in [`drawing.py`](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/010/drawing.py) raised the recursion allowance and passed the same case plus 23 other structured cases. No independent review. The original failure was an implementation execution failure, not a graph-theoretic impossibility.

## Consequence for search

Account for library recursion depth when claiming a polynomial executable drawing. Prefer an iterative implementation if much larger inputs need lower stack use, and independently validate every returned drawing for overlaps and crossings.

## Use history

- 2026-09-24: extracted from round 016; intended destination if promoted is the board's local shared experience collection, with no board edit during research.

Rounds 021 and 034 reused this limitation during backend-contract design. The current candidate confines tsmpy to a fixed small-core, fixed-operation attempt and uses explicit visibility routing after any failure or for larger cores. Four forced-exhaustion tests exercised that route. The earlier recursion repair remains valid historical evidence; it is no longer the all-input justification.
