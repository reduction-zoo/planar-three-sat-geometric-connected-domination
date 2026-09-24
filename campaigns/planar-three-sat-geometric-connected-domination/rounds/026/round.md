# Round 026 — polynomial flow replacement contract

## Plan

Gap: fixed capacities and unproved worst-case flow runtime in tsmpy. Mechanism: inspect the primary orthogonal-drawing algorithm's flow bounds and replace only the flow subproblem with a fully specified integral successive-shortest-path algorithm. First check: establish an input-dependent bound on total nonnegative residual supply and verify the lower-bound transformation against exhaustive tiny networks before drawing integration. Scope is the flow component, not a claim that the entire rectangularization backend is certified. Relevant experience: round 021 isolates capacity/runtime obligations; drawing recursion remains separate.

## Evidence and diagnosis

The [Duncan–Goodrich handbook chapter](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/orthogonal.pdf), §7.3, describes the topology/shape/metrics decomposition; it does not certify tsmpy. The replacement [exact_flow.py](exact_flow.py) subtracts lower bounds, routes residual supply with shortest augmenting paths (Bellman–Ford, exact integers), and restores lower bounds. Each augmentation reduces unsent integral supply by at least one. Runtime is O(QVE) arithmetic operations for total residual supply Q. This is polynomial here **only after** proving Q polynomial in drawing size; it is not a strongly polynomial general min-cost-flow implementation. All original costs are nonnegative, and successive shortest augmentation preserves absence of negative residual cycles, giving minimum cost when all supply is sent.

The test first failed for the missing module. `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/026/test_flow.py` then matched all 80 exact tiny-network enumeration optima, including positive lower bounds, feasible/infeasible networks, conservation and capacity checks. No drawing uses it yet.

For the orthogonal network, after subtracting angle lower bounds, total supply is O(V+E). Any nonnegative-cost optimum can have all residual cycles removed, so no arc needs more than Q residual capacity. For rectangular compaction, a directed acyclic source-to-sink network in which each arc lies on an s–t path has a feasible unit-lower-bound flow of at most E units: add one s–t path through each arc. Thus E units plus a zero-cost bypass replace the fixed total. The DAG/path premises must still be checked against the actual rectangularization.

Experience extraction: updated [backend contract](../../../../research/experience/orthogonal-drawing-backend-contract.md). Next action: integrate the real replacement into an experimental backend and test layout invariants; keep the current candidate unchanged until its full contract is supported.
