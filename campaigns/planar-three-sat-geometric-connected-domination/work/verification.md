# Verification scope at the 20-round limit

Candidate: [`algorithm.py`](algorithm.py) and [`proof.md`](proof.md), with locked dependencies in the repository `uv.lock`. The executable chain was last changed before round 020; this record describes the committed candidate plus the final standalone verifier. It is **not** a passing full-corpus verification.

## Independently solved actual targets

Run `uv sync --locked`, then:

```sh
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/verify.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py
```

`verify.py` imports neither the candidate nor the prepared oracle. It executes both candidate modes as subprocesses, builds the small target graph with exact rational arithmetic, exhaustively searches connected dominating subsets within `K`, and exhaustively checks source satisfiability. It solved 15 actual F-produced one-point targets: one positive witness and 14 negative `NO-SOLUTION` outputs. All 15 recovered source outputs were valid. Case IDs are 0, 4, 6, 11, 15, 43, 63, 66, 72, 78, 88, 94, 101, 103 and 111.

## Validated but not independently solved geometric targets

The prepared source foundation contains 112 cases, 100 seeded random and 12 edge cases; its independent source checks pass. The geometry experiments checked 111 nonempty generated point sets before the unit-contradiction shortcut and constructed valid exact-budget connected dominating sets for 98 prepared SAT cases. The round-012 decoder check recovered from 97 nonempty canonical witnesses. The round-018 script created 12 distinct exact-budget side-chain witnesses across 1,596–202,170 target points, validated each from its target coordinates with the independent target witness checker, and executed recovery in a fresh process; all 12 recovered satisfying assignments. These target witnesses were derived from known source assignments, so their existence was **not** established by an independent target solver.

The full `check.py --candidate ...` run did not finish on the first large positive target. Its initial time-indexed connectivity encoding was interrupted after memory rose to about 7.7 GB; a sparse exact replacement stayed below about 280 MB in the observed run but returned no answer before interruption. An independent CP-SAT flow model matched five small target cases but likewise returned no answer on the 1,596-point candidate target before interruption. Both are execution failures, never NO certificates. No prepared nontrivial geometric target has been independently solved as an instance.

## Open obligations

- Demonstrate that the chosen orthogonal drawing implementation returns a valid polynomial-size point-vertex layout for every legal generated core. A recursion failure on a legal 20-clause chain was repaired and the exact validator passed 24 structured stress cases; 111 prepared cores also passed. A second backend independently produced valid routes on all 135 finite cores, but neither package has an audited all-input guarantee here.
- Independently solve representative nontrivial positive and negative geometric targets, run the full prepared F/G candidate suite, and search for counterexamples beyond it. The negative cases currently take a sound unit-propagation shortcut and therefore do not exercise geometric NO instances.
- Subject the complete rule to independent correctness, novelty and significance review after the prior obligations are met. No manuscript or formal proof was requested or produced.

Observed maximum prepared geometric target size was 202,170 points; this is an output-size measurement, not a worst-case runtime or bit-size proof. The working proof gives polynomial bounds conditional on a certified drawing implementation. No publication or board update occurred.
