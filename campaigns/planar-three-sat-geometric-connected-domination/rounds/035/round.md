# Round 035 — independent coordinate-restricted witness search

## Plan

Gap: the exact full-target encodings allow many side-chain choices and still fail on clause-bearing targets. Mechanism: search only witnesses whose chosen integer points lie on x=0 mod 10 or y=0 mod 10, using the actual target's adjacency, budget, domination and connectivity constraints. This is a target-only witness heuristic; it neither imports the candidate nor recovers a source answer to construct a target witness. Restricted UNSAT returns unknown, never NO-SOLUTION. First check: four-point paths at budgets one/two and a one-point off-lattice satisfiable target distinguish true witnesses from incomplete search. Then try the actual 6,369-point clause-bearing target that defeated unrestricted DP. Relevant experience: global oracle scale is sensitive to representation; finite valid target witnesses are independently checkable even from an incomplete search.

### Initial encoding attempt

The small behavioral test passed, but the first coordinate restriction with full-size connectivity cuts did not return an answer on the 6,369-point target. It was manually interrupted while pursuing a smaller forced-component encoding; exit 130 is an execution failure, not an oracle answer or exhausted search. RSS was about 224 MB at the recorded probe. Preserve this initial implementation in the partial commit before changing the search representation.
