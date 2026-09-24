# Round 014 — independent CP-SAT target oracle

## Plan

Gap: the prepared Z3 target solver remains inconclusive on a 1,596-point candidate target, even after its memory issue was repaired. Mechanism: build an independent connected-domination formulation with OR-Tools CP-SAT and single-commodity flow over the target graph, using only the explicit target points and budget. The oracle-scale experience entry applies; the new model has variables proportional to vertices plus grid edges. First check: compare its answers with the existing exact oracle on small yes/no target graphs, then attempt the first nontrivial F-produced positive and negative targets with no solver time cutoff. Treat any interrupted or unknown status only as an execution failure. A successful oracle must return actual target witnesses and certify infeasibility where claimed.

## Evidence and diagnosis

[`target_cp.py`](target_cp.py) builds its graph solely from the target coordinates, imposes domination and budget constraints, and uses integral single-commodity flow to certify selected-vertex connectivity. Every articulation vertex is fixed selected, which is valid for any connected dominating set. The model returns a witness only for CP-SAT `FEASIBLE/OPTIMAL`, and `NO-SOLUTION` only for `INFEASIBLE`; `UNKNOWN` is an execution failure. The formulation follows the integer modeling contract in the [official OR-Tools CP-SAT documentation](https://developers.google.com/optimization/cp/cp_solver). OR-Tools was used ephemerally with `uv run --locked --with ortools`; it was not added to the campaign lock because the target-scale trial did not finish.

Command: `uv run --locked --with ortools python campaigns/planar-three-sat-geometric-connected-domination/rounds/014/target_cp.py`. It matched the independent Z3 oracle and target-witness validator on five small yes/no graphs, including a path that is dominated by one point but needs two for connected domination. The first F-produced nontrivial target had 1,596 points, 2,204 edges and budget 857; 102 articulation points were fixed. CP-SAT consumed over 1.1 GB RSS and eight cores for approximately 5 minutes 44 seconds without an answer. The exploratory run was interrupted; status `UNKNOWN` was rejected. No NO target was reached.

[`greedy.py`](greedy.py) tried a target-only connected greedy construction followed by local two-for-one swaps, with every returned witness checked. Five seeded starts on the same target stopped at 862–865 selected points, above budget 857. This is a heuristic shortfall, not a lower bound or a negative oracle answer.

First discriminating check: **independent CP-SAT formulation supported on five small targets; target-scale execution failure**. Z3 and CP-SAT now fail at search rather than point graph construction. No target-scale target answer was established.

Experience extraction: no new file; the [oracle-scale finding](../../../../research/experience/connected-domination-oracle-scale.md) was updated with this second solver observation.

## Next action

Apply a sound polynomial source simplification to contradictory unit clauses, then independently solve the resulting actual negative target instances. Keep the nontrivial geometry for the other inputs.
