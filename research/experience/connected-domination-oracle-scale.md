# Time-indexed connected-domination encodings can exhaust memory

## Claim and applicability

Tags: connected dominating set, SMT oracle, reachability encoding, target size. A time-indexed Boolean reachability model with one variable per graph vertex and step has quadratic size. On explicit unit-grid targets already in the low thousands of points, this can make an otherwise independent target oracle impractical. The memory failure is an execution limit, not evidence for `NO-SOLUTION`.

## Evidence and status

In [round 013](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/013/round.md), the prepared oracle's full-candidate run reached about 7.7 GB RSS while allocating reachability variables on an early 1,596-point target and was interrupted. A replacement using sparse spatial adjacency and connectivity cuts passed the unchanged self-test and stayed below about 280 MB in the observed run, but Z3 had not produced an answer after about five minutes; interruption yielded `unknown`. No independent review. The observed performance applies to these runs, not a general lower bound.

## Consequence for search

Use sparse graph construction and a connectivity model proportional to graph edges or dynamically added cuts. Treat a killed or inconclusive solver run as unverified; seek a separate target-solving strategy for large negative instances.

## Use history

- 2026-09-24: extracted from round 013; intended destination if promoted is the board's local shared experience collection, with no board edit during research.
