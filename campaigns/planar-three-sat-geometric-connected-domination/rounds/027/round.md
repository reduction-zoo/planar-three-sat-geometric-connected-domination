# Round 027 — exact flow in the drawing pipeline

## Plan

Gap: the replacement flow algorithm has not been exercised by orthogonal shape/compaction. Mechanism: experimental subclasses use the real tsmpy planarization/rectangularization but replace both flow calculations; capacities depend on residual supply/edge count. First check: every compaction network is a DAG with every node reachable from its source and able to reach its sink, then independently validate nonoverlap and recovered graph topology. Finite scope: first 12 prepared sources, plus cycle, cube and octahedron graphs to cover degrees two through four. Relevant experience: round 026 requires the DAG/path premises; round 021 forbids treating matching pipeline names as certification. Candidate maps remain unchanged.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/027/test_drawing.py` passed all 14 nonempty layouts: cycle/cube/octahedron and 11 initial prepared cores. Every rectangular-compaction graph was a DAG with the asserted source/sink reachability. The existing exact validator checked distinct positions, axis alignment, no crossings/overlaps, and suppression back to the input graph. The largest tested core had 315 vertices. No mocks were used; these are real subclass replacements of both flow computations, with the original planarization and rectangularization still executing.

The DAG and reachability observations support the finite tests, not the universal premise. The candidate remains unchanged. Experience extraction: none beyond round 026's scoped flow result; this integration is finite evidence, not a new general guarantee. Next action: remove the floating-point external-face choice and test exact near-parallel integer rays before further all-input claims.
