# Time-indexed connected-domination encodings can exhaust memory

## Claim and applicability

Tags: connected dominating set, SMT oracle, reachability encoding, target size. A time-indexed Boolean reachability model with one variable per graph vertex and step has quadratic size. On explicit unit-grid targets already in the low thousands of points, this can make an otherwise independent target oracle impractical. The memory failure is an execution limit, not evidence for `NO-SOLUTION`.

## Evidence and status

In [round 013](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/013/round.md), the prepared oracle's full-candidate run reached about 7.7 GB RSS while allocating reachability variables on an early 1,596-point target and was interrupted. A replacement using sparse spatial adjacency and connectivity cuts passed the unchanged self-test and stayed below about 280 MB in the observed run, but Z3 had not produced an answer after about five minutes; interruption yielded `unknown`. No independent review. The observed performance applies to these runs, not a general lower bound.

## Consequence for search

Use sparse graph construction and a connectivity model proportional to graph edges or dynamically added cuts. Treat a killed or inconclusive solver run as unverified; seek a separate target-solving strategy for large negative instances.

## Use history

- 2026-09-24: extracted from round 013; intended destination if promoted is the board's local shared experience collection, with no board edit during research.
- 2026-09-24: round 014 tried an independent CP-SAT flow formulation; it matched five small target labels but returned no answer on a 1,596-point candidate target after an interrupted 5-minute-44-second run. A target-only greedy heuristic missed the budget by five to eight points. Neither observation changed the mathematical claim.
- 2026-09-24: round 015 used sound unit propagation to produce 14 one-point negative F-targets, all independently solved and decoded; it did not verify the larger geometric targets.

Round 036 independently recognized a subdivided backbone from target coordinates only, solved a connected-cover subproblem and lifted two validated 3,337-point witnesses for the 6,369-point clause-bearing target. This specialized witness heuristic sees no source formula or candidate metadata. It establishes positives only; all search/recognition failures remain unknown and must not be returned as NO-SOLUTION. Full target validation is the soundness check, not agreement with the reduction proof.

Round 037 used independently checked degree-two vertex-cover folding after mandatory articulation selections. All 209 tiny graph-atlas optimum/below-optimum checks passed, followed by the complete 112-case candidate loop with 195 actual target witnesses and 14 exact one-point NO outputs. Recognition/folding remains a positive-only heuristic followed by full graph validation; generic exact solving remains the fallback. This enabled the observed prepared-suite completion without establishing a general target-solver performance bound.
