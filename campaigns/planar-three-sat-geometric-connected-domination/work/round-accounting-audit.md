# Retrospective round-accounting correction

Date: 2026-09-24. This audit preserves the numbered records and commit history. It corrects how those records were charged to the authorized research budget.

The [research-session rule](../../../.agents/skills/research-session/SKILL.md) starts a research round for a construction hypothesis, proof strategy, or standalone literature investigation. Routine verification and editorial work stay with the work they check; a substantive repair after review can start a round. The same rule expressly permits a complete candidate to finish its checks, review, and manuscript after discovery stops.

At least three numbered records were charged incorrectly:

| Record | Actual work | Budget classification |
|---|---|---|
| [020](../rounds/020/round.md) | Final contract audit and small-target verification | Verification/closeout, not a new research mechanism |
| [038](../rounds/038/round.md) | Independent advance review, which found a determinism defect | Review stage, not a new research mechanism |
| [040](../rounds/040/round.md) | Focused re-review of the repair and manuscript completion | Review/writing stage, not a new research mechanism |

Record [039](../rounds/039/round.md) introduced a substantive deterministic reconstruction repair after review and can be charged under the explicit review-repair rule. Record [037](../rounds/037/round.md) introduced independent cover folding in the target oracle, beyond running the prepared suite; that new oracle mechanism can be charged. Other integration and repair records may require a stricter per-record adjudication. This audit therefore reports a **minimum correction**, not an invented exact recount: 40 numbered records exist, but **at most 37 qualify as budget-consuming research rounds**, so at least three of the 40 authorized slots were unused. The previous claim of exact budget exhaustion was false.

This does not change the candidate's review status or turn finite checks into a general proof. The sequence explains the apparent last-round result: the full prepared suite passed at record 037; review at 038 found a defect; the repair at 039 passed; re-review at 040 advanced it. Two of those last three records were stages that should not have consumed research rounds. Completion, rather than exhaustion, is the reason to stop discovery now.

The commit timestamps show this sequence but cannot establish absence of all other errors. A fresh 2026-09-24 run of `uv run --locked python -B campaigns/planar-three-sat-geometric-connected-domination/reviews/deterministic-repair/check_recovery.py` reproduced a 12,418-point, K=6,515 target under F seeds 7/99 and recovered `[false, true]` under G seeds 123/456. That is one finite independent-target check, not a substitute for expert proof review. No board or publication action was taken in this correction.
