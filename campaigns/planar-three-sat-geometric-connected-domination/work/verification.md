# Executable verification

Candidate: [algorithm.py](algorithm.py), [proof.md](proof.md), and [drawing proof](drawing-proof.md). The maps use the round-034 bounded compact-layout attempt and explicit visibility fallback. Dependencies are locked in `uv.lock`. The first independent review found hash-sensitive drawing order; round 039 repaired it, and the [focused independent review](../reviews/deterministic-repair/review.md) returned advance.

## Complete prepared loop

Run from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --self-test
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py
```

[Round 039](../rounds/039/round.md), candidate implementation `ad75146`, passed all 112 fixed sources: 98 satisfiable and 14 unsatisfiable. The actual F-produced targets yielded 195 valid witness outputs and 14 exact NO-SOLUTION outputs. Each output went through a fresh G process and independent source validation. All 97 nontrivial geometric positive targets supplied two distinct witnesses; the empty source supplied its one-point witness. The 14 negative sources take the sound unit-contradiction shortcut and were solved exactly as K=0 one-point targets. The largest actual target had 202,170 points. [Full output](../rounds/039/prepared.txt).

The source labels remain the original independently exhaustive-checked labels. The optional target witness finder reads only actual coordinates: it recognizes a subdivided backbone, runs ordinary vertex-cover folding and a connected-cover search, then lifts candidate indices. It imports no candidate implementation or source instance. It is incomplete and returns only a fully validated witness or unknown. The unchanged complete Z3 target oracle handles cases where no witness is found; restricted UNSAT never becomes NO-SOLUTION. The prepared target validator independently builds exact rational-distance adjacency, separate from the finder's integer-grid recognition. The vertex-cover kernel matched all 209 graph-atlas optimum/below-optimum budgets through six vertices.

## Additional independent and arbitrary-output evidence

`verify.py --candidate .../algorithm.py` imports neither candidate nor prepared checker and exhaustively solves the 15 actual one-point targets (one YES, 14 NO) and checks source outputs. Round 024 separately implemented an exact graph-only separator CDS oracle, checked against all 31 connected atlas graphs through five vertices (later 143 through six), and solved the 1,596-point target at minimum size 857. Round 036 independently found and checked two 3,337-point witnesses for a clause-bearing 6,369-point target; the later kernel version passed the same recovery regression.

The round-018 side-chain script constructs noncanonical witnesses from known source assignments, then independently validates the full actual target and invokes G in a fresh process. These are decoder-coverage checks, not independent evidence of target existence. The current round-039 rerun passed all 12 distinct side-chain witnesses on targets of 1,596–202,170 points; see [side-chains.txt](../rounds/039/side-chains.txt).

## Added geometric negative certificates

[Round 041](../rounds/041/round.md) fixes two unsatisfiable planar sources outside the original 112-case corpus. Their exhaustive truth tables are UNSAT, but neither formula has an initial unit clause after duplicate removal. Actual F targets contain 31,576 and 25,236 points with positive budgets. Public F outputs agree under hash seeds 7 and 99. The [target-only certificate script](../rounds/041/certify_negative.py) checks every integer unit edge and the full path/side-point interface from the target coordinates; it imports no candidate module or source assignment for the negative decision. By [Clark et al., Theorem 6.1 and Lemmas 6.1–6.2](https://cs.du.edu/~snarayan/sada/research/docs/res/unitdisk.pdf), a CDS within the target budget would yield a connected vertex cover of the recovered 612-vertex skeleton within budget 308. In each instance, 240 forced articulations, 57 exact degree-two folds, and an exhaustive 18-vertex residual cover optimum of 12 give lower bound 309. The [certificates](../rounds/041/certificates.json) include point-set digests and residual edge lists. Fresh G processes return `NO-SOLUTION` for both certified target answers.

This is an independently implemented **structural** target NO certificate that relies on the published CDS-to-connected-cover lemma. It is not an unrestricted direct CDS solver. The fold rule matched exhaustive vertex cover on 209 small atlas graphs, and the same structure parser accepted a positive geometric control. Reproduce with `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/041/test_negative_sources.py`, then `test_certificate.py` and `certify_negative.py` under the same prefix.

## Drawing evidence

All 46 finite port-pattern certificates pass an independent exhaustive pattern/path validator. The visibility route passes 163 biconnected planar degree-four atlas graphs plus 11 initial prepared cores (174 complete exact layout checks). The bounded wrapper passes four real forced-operation-exhaustion fallback cases and all 111 nonempty prepared cores. These checks support the explicit argument in `drawing-proof.md`; they do not replace that argument or independent review.

## Limits and retained failures

The original corpus has at most six source variables and does not cover every planar embedding. Its 14 negative targets use the contradiction shortcut; the two added geometric NO certificates are outside that fixed corpus and depend on Clark's structural lemma. There is still no generic direct-CDS UNSAT certificate for these larger point graphs. Target witness search is specialized and incomplete, with exact fallback, and no general practical solver-efficiency claim is made. The exact CDS separator oracle still failed by resource exhaustion on a 6,369-point clause-bearing case before the structural witness method succeeded.

Earlier layered reachability, unrestricted connectivity cuts, CP-SAT flow, plateau pruning, and restricted rank searches had interrupted or inconclusive runs. These remain execution failures, never negative oracle answers; records are preserved in rounds 013–014, 022, 025, 035 and the first round-037 prefix. Finite passing checks establish the stated instances and outputs only. Correctness for all legal inputs and valid target outputs depends on the general proof and the recorded independent advance review; expert review remains pending. No formal proof, publication, remote or board update has been made.

## Deterministic reconstruction repair

[Round 039](../rounds/039/round.md) preserves the independent review's failing hash-seed counterexample and then checks identical accepted fallback layouts under two seeds on the actual default public-F prefix (1,292 core vertices; route length 17,180,282 after repair). The large default target was not expanded. A real zero-operation-allowance launcher forces the fallback on source 1: two fresh F seeds emit the same 330,596-point target, and an independent target-only finder supplies a fully validated witness of size 165,357. Two fresh G seeds recover valid source assignments. This source has no clauses; three compact-branch cross-seed cases include clause-bearing sources. All 174 fallback layouts were revalidated. See [reconstruction records](../rounds/039/reconstruction.json).

## Review and manuscript closeout

The reviewer independently repeated the large default-source drawing check with seeds 7 and 99 and independently solved a new clause-bearing 12,418-point target (K=6,515), recovering `[false, true]` under seeds 123 and 456. See the [advance report](../reviews/deterministic-repair/review.md). The [eight-page paper](manuscript.pdf) compiled with Typst 0.15.1; all pages were visually inspected after the final language/notation pass. Figure checks cover the exact clause ports/cover, complete 45-vertex face augmentation, and all unit adjacencies of the local 18-point grid route. [Inspection record](evidence/manuscript/inspection.md). No algorithm or proof mechanism changed during writing.
