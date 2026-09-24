# Round 023 — target separator width

## Plan

Gap: exact nontrivial target solving. Mechanism: generic graph tree decomposition to isolate long narrow ladders without reading candidate metadata. First check: NetworkX minimum-degree tree decomposition of actual F target 1, validate edge coverage and the running-intersection property, and measure maximum bag width. Small width supports a connectivity-partition DP; large width would redirect to another oracle. Relevant experience: oracle-scale failures are encoding-sensitive and do not bar target-only decomposition. Finite scope: prepared target 1 only; no solver or subprocess timeout.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/023/decompose.py` validated 1,588 bags for the 1,596-vertex target. Maximum width is eight; 1,571 bags have size at most four. This supports a specific small-separator oracle attempt, though width eight may still yield expensive joins. It establishes no target solution.

Experience extraction: none yet; a single width measurement does not establish that the proposed DP is effective. Next action: implement exact selected-component partitions with domination flags, cross-check against exhaustive enumeration, and then solve this actual target.
