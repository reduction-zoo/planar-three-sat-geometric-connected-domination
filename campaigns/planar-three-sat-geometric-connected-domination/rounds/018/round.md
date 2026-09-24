# Round 018 — varied noncanonical target outputs

## Plan

Gap: the decoder's side-chain normalization has been exercised on only one noncanonical exact-budget target output. Mechanism: across a size-spread of prepared SAT cases, start from a certified forward witness, make a target-only local side-chain swap that preserves connected domination and budget, then send the resulting distinct point-index output through the fresh `--extract` process. The independent target checker validates the swapped witness from coordinates, and the independent source checker validates recovery. The round-011 side-neighbor experience applies because side chains must remain in the graph. First check: find at least several distinct valid side-chain outputs on different source sizes; a failed recovery supplies a concrete target witness and assignment counterexample, while passing finite tests leave the general lemma proof to audit.

## Evidence and diagnosis

[`alternate_witnesses.py`](alternate_witnesses.py) selected 12 prepared SAT cases spanning one to six variables, zero to ten clauses and 1,596 to 202,170 target points. For each, it generated a canonical exact-budget target witness, made a target-only one-point side-chain swap, and checked that the resulting set was distinct, within budget, connected and dominating using the independent coordinate-derived target graph in `work/check.py`. The point-index output was then sent to `work/algorithm.py --extract` in a fresh process, and the recovered assignment passed the independent source checker. All 12 selected cases produced and decoded a valid alternate witness. Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/018/alternate_witnesses.py`; case IDs: 1, 2, 7, 16, 17, 21, 49, 52, 84, 97, 110, 13.

The alternate outputs were constructed from known positive source witnesses and checked independently for target validity; they were **not** found by an independent target solver. Thus this is stronger arbitrary-output decoder coverage, not independent target feasibility or negative-instance evidence. The finite tests do not prove the normalization lemma for every valid target output.

First discriminating check: **supported on 12 noncanonical actual target outputs** with one side-chain vertex each, including the largest prepared geometric target. No counterexample was found.

Experience extraction: no new file. The [independent-side-neighbor entry](../../../../research/experience/independent-side-neighbors-at-grid-turns.md) was updated with this side-chain normalization evidence.

## Next action

Audit the mathematical soundness of the complete composed argument and the remaining implementation and verification gaps before the final budget decision.
