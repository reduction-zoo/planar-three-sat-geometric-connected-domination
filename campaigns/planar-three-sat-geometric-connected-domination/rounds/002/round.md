# Round 002 — local variable and clause geometry

## Plan

Gap: the published proof gives no rational coordinates or proof that the desired adjacencies survive. Mechanism: a forced ground point with two literal choices and a private point dominated by either choice; clause points at unit distance from only the sign that satisfies them. Scope: one variable with arbitrary repeated-literal three-clauses, no general planar wiring. First discriminating check: enumerate every connected dominating set of size at most two for the resulting exact unit-disk graph on all prepared one-variable instances, and compare decoded truth values with the source clauses. Passing would establish only a local interface; failure would expose a geometric adjacency or budget defect. Prior evidence: round 001 found the same unit-distance model but no explicit coordinates. The [omitted-geometry entry](../../../../research/experience/lichtenstein-omitted-rational-embedding.md) applies because this round supplies actual rational points.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/002/local_interface.py` passed on 2026-09-23. It enumerated all target subsets of size at most two for 21 fixed one-variable formulas: 16 satisfiable and 5 unsatisfiable. Each feasible set contained ground and exactly the sign point whose decoded assignment satisfies the formula. The points are integer coordinates. In the base gadget, the ground leaf forces ground under the two-point budget; the private point then forces one of the true/false ports; the optional sign clause point can be dominated only by its matching port. This is a local finite result, not an arbitrary-formula reduction.

Composition obstruction: when two copies are translated four units apart, their corresponding literal ports are four units apart. Any single clause point adjacent to both ports would imply their distance is at most two by the triangle inequality. Thus the direct shared-clause-point layout cannot express even a two-variable clause in this spaced arrangement. It needs a wire or a different variable placement. This refutes that narrow composition assumption, not the existence of a geometric reduction.

Experience extraction: [local port distance bound](../../../../research/experience/clause-port-distance-bound.md), created 2026-09-23. The prior omitted-geometry entry prevented treating the paper's figure as executable coordinates; its use history was updated.

## Next action

Test a wire mechanism that can carry literal truth across a long planar route without consuming clause slack.
