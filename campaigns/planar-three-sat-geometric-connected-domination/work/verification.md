# Executable verification

Candidate: [algorithm.py](algorithm.py), [proof.md](proof.md), and [drawing proof](drawing-proof.md). The maps use the round-034 bounded compact-layout attempt and explicit visibility fallback. Dependencies are locked in `uv.lock`. Independent review remains pending.

## Complete prepared loop

Run from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --self-test
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py
```

[Round 037](../rounds/037/round.md) passed all 112 fixed sources: 98 satisfiable and 14 unsatisfiable. The actual F-produced targets yielded 195 valid witness outputs and 14 exact NO-SOLUTION outputs. Each output went through a fresh G process and independent source validation. All 97 nontrivial geometric positive targets supplied two distinct witnesses; the empty source supplied its one-point witness. The 14 negative sources take the sound unit-contradiction shortcut and were solved exactly as K=0 one-point targets. The largest actual target had 202,170 points. [Full output](../rounds/037/prepared-kernel.txt).

The source labels remain the original independently exhaustive-checked labels. The optional target witness finder reads only actual coordinates: it recognizes a subdivided backbone, runs ordinary vertex-cover folding and a connected-cover search, then lifts candidate indices. It imports no candidate implementation or source instance. It is incomplete and returns only a fully validated witness or unknown. The unchanged complete Z3 target oracle handles cases where no witness is found; restricted UNSAT never becomes NO-SOLUTION. The prepared target validator independently builds exact rational-distance adjacency, separate from the finder's integer-grid recognition. The vertex-cover kernel matched all 209 graph-atlas optimum/below-optimum budgets through six vertices.

## Additional independent and arbitrary-output evidence

`verify.py --candidate .../algorithm.py` imports neither candidate nor prepared checker and exhaustively solves the 15 actual one-point targets (one YES, 14 NO) and checks source outputs. Round 024 separately implemented an exact graph-only separator CDS oracle, checked against all 31 connected atlas graphs through five vertices (later 143 through six), and solved the 1,596-point target at minimum size 857. Round 036 independently found and checked two 3,337-point witnesses for a clause-bearing 6,369-point target; the later kernel version passed the same recovery regression.

The round-018 side-chain script constructs noncanonical witnesses from known source assignments, then independently validates the full actual target and invokes G in a fresh process. These are decoder-coverage checks, not independent evidence of target existence. The current round-037 rerun passed all 12 distinct side-chain witnesses on targets of 1,596–202,170 points; see [side-chains.txt](../rounds/037/side-chains.txt).

## Drawing evidence

All 46 finite port-pattern certificates pass an independent exhaustive pattern/path validator. The visibility route passes 163 biconnected planar degree-four atlas graphs plus 11 initial prepared cores (174 complete exact layout checks). The bounded wrapper passes four real forced-operation-exhaustion fallback cases and all 111 nonempty prepared cores. These checks support the explicit argument in `drawing-proof.md`; they do not replace that argument or independent review.

## Limits and retained failures

The corpus has at most six source variables and does not cover every planar embedding. All independently solved negative actual targets use the contradiction shortcut; no nontrivial geometric NO target has been independently certified. Target witness search is specialized and incomplete, with exact fallback, and no general practical solver-efficiency claim is made. The exact CDS separator oracle still failed by resource exhaustion on a 6,369-point clause-bearing case before the structural witness method succeeded.

Earlier layered reachability, unrestricted connectivity cuts, CP-SAT flow, plateau pruning, and restricted rank searches had interrupted or inconclusive runs. These remain execution failures, never negative oracle answers; records are preserved in rounds 013–014, 022, 025, 035 and the first round-037 prefix. Finite passing checks establish the stated instances and outputs only. Correctness for all legal inputs and valid target outputs depends on the general proof and its pending independent review. No formal proof, publication, remote or board update has been made.
