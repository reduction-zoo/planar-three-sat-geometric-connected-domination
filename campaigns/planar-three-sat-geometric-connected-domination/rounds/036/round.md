# Round 036 — target-only backbone witness search

## Plan

Gap: independent target solving on clause-bearing geometry. Mechanism: recognize a subdivided backbone directly from target coordinates and degrees, contract degree-two chains, solve connected vertex cover on that small graph, and lift a connected tree-based index set. The algorithm sees only the actual target; it imports no candidate code, source formula, assignment, or metadata. It is deliberately incomplete: every failure returns unknown, and every success is checked against full target domination/connectivity/budget. First check: the 6,369-point actual target that resisted three generic encodings; validate any returned witness and fresh-process G recovery. Then use the same independent checks on any additional candidate targets. Relevant experience: subdivision scale can obscure a small combinatorial core; proof similarity is not a substitute for validating the actual point-index witness. No NO claim can rely on this recognition.

## Evidence and diagnosis

The test failed first because the new module was absent. `uv run --locked python .../rounds/036/test_backbone.py` then found two distinct actual index-set witnesses of size 3,337 for the 6,369-point clause-bearing target. Both passed full graph domination, connectivity and size checks and decoded in fresh candidate processes to `[true]`; retained output and witness index sets are here.

The finder reconstructs the backbone from coordinates/induced degrees, suppresses chains, searches connected vertex covers with Z3, then tries two spanning trees. It uses no source information. Its lifting argument resembles the published target structure, so this is **specialized independent witness search**, not an independent proof of the reduction. Sound positive evidence comes from checking the complete actual point graph. Recognition failure, restricted UNSAT or solver inconclusive all return `None`, not a negative answer. The earlier exact separator solver remains a separate minimum-CDS check on the 1,596-point target.

Experience extraction: updated [oracle-scale finding](../../../../research/experience/connected-domination-oracle-scale.md) with the successful target-only structural heuristic and its strict positive-only scope. Next action: integrate this as an optional witness finder before the unchanged complete oracle, and run all prepared F/solve/G loops plus alternate outputs.
