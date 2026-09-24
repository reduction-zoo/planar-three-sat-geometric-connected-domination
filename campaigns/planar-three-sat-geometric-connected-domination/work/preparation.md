# Prepared testing foundation

Run from repository root:

```sh
uv sync --locked
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --self-test
```

The fixed `cases.json` has 112 unique instances: 12 hand-designed edge cases and 100 seeded random cases (seeds retained per case). The seed algorithm is in `generate_cases.py`; regeneration is checked in the self-test. Variable counts range from 0 to 6. There are 98 satisfiable and 14 unsatisfiable cases. Random clauses use variables on one edge of a variable path, so their incidence graphs remain planar; NetworkX 3.7 constructs and checks each rotation system. Repeated literal occurrences permit unit-like constraints while retaining exactly three literal occurrences per clause. These cases do not cover arbitrary planar embeddings or large formulae.

The source oracle uses Z3 5.1.0.0, one Boolean per variable and one disjunction per clause. SAT models are checked directly against all clauses. UNSAT is accepted only from Z3's conclusive `unsat`; the self-test independently enumerates all assignments for every prepared case. The target oracle derives rational unit-disk adjacency exactly with `Fraction`. Z3 uses one selected-point Boolean per vertex, closed-neighborhood domination, a selected root, and `n` layers of reachability through selected vertices. A satisfying model is exactly a connected dominating set of size at most `K`; the witness validator independently checks domination and induced connectivity with NetworkX. `unknown` raises an error. The self-test covers adjacent and separated points, both one-point witnesses, infeasibility at `K=0`, duplicate indices, empty answers, malformed source assignments and false NO-SOLUTION claims.

The candidate command `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py` will inject all cases, solve actual target instances, try a second distinct target witness when present, invoke extraction in a fresh subprocess, and validate recovered source outputs. No candidate was constructed during Prepare.

Evidence: `uv run python .../work/check.py --self-test` passed on 2026-09-23: corpus gate 112/100/12 and all 112 independent labels. The target encoding is tested only on small hand-checkable graphs so far; larger candidate graphs remain to be checked. The finite corpus is diagnostic and cannot prove a reduction.
