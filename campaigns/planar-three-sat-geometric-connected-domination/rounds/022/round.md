# Round 022 — connected target pruning with plateau moves

## Plan

Gap: no independently found nontrivial geometric witness. Mechanism: target-only connected-set pruning, followed by finite random add/prune plateau moves. This differs from round 014's improving two-for-one swaps by accepting neutral and temporarily larger connected sets. Search scope: first prepared nontrivial target, seeds 0–3, at most 300 moves each. First check: every search result on small paths is a valid CDS and reaches the known path optimum; then seek an independently validated actual F witness within K. Failure to find one is only heuristic failure. Relevant experience: oracle-scale failure cautions against reading search failure as NO-SOLUTION. No candidate map changes.

## Evidence and diagnosis

Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/022/search.py`; complete output in [output.txt](output.txt). Six path checks reached their independent optimum. All four 300-move searches finished on the actual 1,596-point target, without reaching budget 857. The search became trapped well above K. This refutes neither existence nor correctness; no target answer was returned. The target remains unknown under this heuristic.

Experience extraction: none; this finite heuristic shortfall does not establish a reusable obstruction beyond the existing oracle-scale entry. Next action: replace global search with exact separator dynamic programming if a target-only graph decomposition has small width.
