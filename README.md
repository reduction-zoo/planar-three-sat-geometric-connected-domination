# Planar 3-SAT → Geometric connected domination

**Status:** `ready_for_expert_review` · **Research models:** `gpt-6-sol` (main), `gpt-6-astra` (later rounds) · **Submitted:** 2026-09-24

This archive supplies deterministic polynomial-time construction and recovery for the fixed Planar 3-SAT to geometric connected domination contract. Its written proof claims that every valid target output recovers a valid source output, including NO-SOLUTION. It reconstructs a published hardness route; it does not claim a new hardness theorem or human acceptance.

## Construction

Encode planar SAT as planar vertex cover, connect the cover gadgets through face cycles, then draw the connected graph on an integer grid. The unit-disk construction adds path and side points so a bounded connected dominating set corresponds to a bounded connected vertex cover. Recovery normalizes any valid target witness before extracting an assignment.

## Evidence

- **Mathematical correctness and recovery: Written proof; independent agent review advanced.** The proof covers the fixed endpoint semantics and every valid target output. The focused reviewer found no remaining blocking gap after a deterministic-order repair. Two later geometric negative cases were not independently reviewed; the construction and proof were unchanged. Human expert acceptance remains pending. ([evidence](campaigns/planar-three-sat-geometric-connected-domination/reviews/deterministic-repair/review.md))
- **Construction and recovery complexity: Written polynomial bounds.** The construction emits O((n+m)²) integer-coordinate points with O(log(n+m)) coordinate bits; recovery is polynomial in the input and target-output size. These bounds are not formally certified. ([evidence](campaigns/planar-three-sat-geometric-connected-domination/work/proof.md))
- **Executable verification: Finite checks passed.** The prepared corpus has 112 source instances and 209 checked target outputs. It includes 97 geometric positive targets with two witnesses each, one trivial positive, and 14 trivial negatives. Two later nontrivial geometric negative targets have structural NO certificates based on the published reduction lemma, not a generic target UNSAT solve. Finite checks supplement rather than replace the general proof. ([evidence](campaigns/planar-three-sat-geometric-connected-domination/work/verification.md))
- **Formal certification and maintainer acceptance: Pending / not performed.** No Lean kernel check, human expert acceptance, or upstream integration is recorded. ([evidence](campaigns/planar-three-sat-geometric-connected-domination/state.md))

## Reproduce

Run from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py
uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/verify.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py
```

These finite checks exercise construction and recovery. The general claim rests on the written proof.

## Artifacts

- [Fixed question](campaigns/planar-three-sat-geometric-connected-domination/question.md)
- [Campaign state](campaigns/planar-three-sat-geometric-connected-domination/state.md)
- [Manuscript](campaigns/planar-three-sat-geometric-connected-domination/work/manuscript.pdf)
- [Construction and recovery](campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py)
- [General proof](campaigns/planar-three-sat-geometric-connected-domination/work/proof.md)
- [Independent review](campaigns/planar-three-sat-geometric-connected-domination/reviews/deterministic-repair/review.md)
- [Verification evidence](campaigns/planar-three-sat-geometric-connected-domination/work/verification.md)
- [Round-accounting audit](campaigns/planar-three-sat-geometric-connected-domination/work/round-accounting-audit.md)
