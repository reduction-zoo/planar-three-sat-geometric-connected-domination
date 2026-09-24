# Round 024 — exact separator connected-domination oracle

## Plan

Gap: independently solve a nontrivial actual target. Mechanism: tree-decomposition DP retaining each boundary vertex's selected/dominated state and the partition of selected boundary vertices into connected components. Keep a forced root in every bag; a disappearing selected component is invalid. A join unions domination and connectivity. First check: compare minimum CDS cardinality against independently exhaustive enumeration on all connected graph-atlas graphs up to five vertices before attempting F target 1. This targets selection, forgetting, joining and connectivity errors, with no candidate code imported. Relevant experience: round 023's validated width supports this attempt; global solver failure does not predict DP failure. No candidate changes.

## Evidence and diagnosis

The test was written first and failed because `target_dp` did not yet exist. After implementation, `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/024/test_dp.py` matched independently exhaustive minimum cardinalities on all 31 connected graph-atlas graphs with at most five vertices. The solver imports no candidate code. Its graph builder reads actual integer coordinates and uses precisely unit horizontal/vertical adjacency.

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/024/target_dp.py` independently solved F(case 1): 1,596 vertices, K=857, exact optimum 857. Minimum-fill decomposition width was seven, with peak 119,810 states. The returned witness was independently checked for size, domination and connectivity, then passed to a fresh `algorithm.py --extract` process, returning `[true]`. Retained [output](output.txt) and [witness](witness-1.json). This is the first independent nontrivial geometric target answer. It is a positive, clause-free one-variable input; negative geometry and clause-bearing witnesses remain untested by this oracle.

Experience extraction: created [separator CDS oracle](../../../../research/experience/separator-connected-domination-oracle.md). Next action: strengthen graph-only preprocessing with forced articulation vertices, validate it independently, and attempt a clause-bearing target plus a non-unit-propagation negative source.
