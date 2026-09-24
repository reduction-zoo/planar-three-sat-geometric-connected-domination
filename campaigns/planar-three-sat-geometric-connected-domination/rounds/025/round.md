# Round 025 — articulation selection in the separator oracle

## Plan

Gap: geometric verification beyond a vacuous positive formula. Mechanism: every articulation vertex of a connected graph is mandatory in a CDS (otherwise domination forces selections in different components that cannot connect). Enforce this target-only fact at DP introduction, reducing states without constraining valid solutions. Reuse the exhaustive oracle tests for this behavior-preserving optimization and extend independent optimum checks to all connected atlas graphs through six vertices. First check: those optima remain equal. Then solve prepared case 2, a clause-bearing positive, and preserve its actual witness/recovery. Relevant experience: separator DP succeeded where global encodings did not; optimization is one bounded attempt, not an open performance campaign.

## Evidence and diagnosis

The articulation optimization preserved all 143 independently exhaustive optima through six vertices (`uv run --locked python .../rounds/024/test_dp.py`). The actual clause-bearing F(case 2) has 6,369 points and K=3,337. Its exact DP reached approximately 4.6 GB RSS while joining tables; the process was manually interrupted to contain resource use, returning `KeyboardInterrupt` (exit 130). This is an **execution failure**, not UNSAT, not an exhausted search family, and not evidence against the reduction. No witness or negative target answer was produced. Retained initial output in [output.txt](output.txt); interrupted location: `solve_root`, joining a table at `put(joined, state, ...)`.

Experience extraction: updated [separator oracle finding](../../../../research/experience/separator-connected-domination-oracle.md) with this scale limitation. The bounded optimization attempt is finished. Next action: work on the mathematical drawing contract; the exact oracle is useful for the smallest geometry but does not yet support the full prepared suite.
