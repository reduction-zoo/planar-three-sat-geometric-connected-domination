# Round 020 — final contract and verification audit

## Plan

Gap: the composed candidate has substantial finite evidence but the fixed acceptance contract still requires every legal input to be handled by deterministic polynomial F/G and nontrivial target instances to be solved independently before review. Mechanism: independently recheck the actual F-produced small positive and negative targets in a standalone verifier, then audit every remaining obligation against the code, proof and round evidence. Earlier oracle-scale and library-recursion experience applies directly. First discriminating check: can a fresh verifier solve and decode the trivial target class without importing the candidate or prepared oracle, and can the current evidence certify the all-input drawing and full target suite? If either general obligation remains open, close at the 20-round budget as unverified, retain the candidate and exact resumption conditions, and do not request review or write a paper.

## Evidence and diagnosis

[`work/verify.py`](../../work/verify.py) is a separate exact small-target verifier. It imports neither `algorithm.py` nor `check.py`; it executes F/G as subprocesses, builds the target graph with exact fractions, exhaustively searches connected dominating subsets within `K`, and exhaustively checks source assignments. Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/verify.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py`. Result: 15 actual F-produced targets solved and decoded, one YES and 14 NO. [`work/verification.md`](../../work/verification.md) separates these independently solved instances from the 12 nontrivial side-chain witnesses that were validated but constructed from known source solutions.

Final obligation audit against the fixed question and [reduction contract](../../../../research/reduction.md): executable F/G and a working composed argument exist, but the `tsmpy` call is not audited as a total, polynomial-size orthogonal drawing algorithm for every legal generated core. The library's finite successes and the structural biconnectivity lemma do not supply that guarantee. The prepared 112-case candidate loop has not passed because independent large-target solving did not finish; no nontrivial geometric target was independently solved. Consequently correctness of the full executable rule is unverified. Novelty and significance were not independently assessed, so the research-reviewer stage and manuscript stage were not entered. These are concrete remaining obligations rather than a claim that the theorem is false.

The 20-round budget is exhausted. Four distinct route families were attempted: Lichtenstein's direct geometric construction, the local literal-cell/equality-wire construction, the Grid Tiling construction, and the planar-cover/grid-CDS chain. The present candidate, all failed approaches, inputs, proofs, checks and execution failures remain committed in this repository. No board edit, remote creation or publication occurred.

Experience extraction: no new file in this audit. Closeout found six distinct local entries, four later updated, and no pending extraction. They remain local to this repository; board promotion was not attempted.

## Next action

Stop discovery and exit at the authorized budget. A future continuation would need additional round allocation, a certified all-input drawing implementation, and an independent solver that handles the nontrivial geometric targets before review.
