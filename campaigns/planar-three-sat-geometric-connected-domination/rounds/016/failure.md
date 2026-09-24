# Retained drawing failure before repair

Run: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/016/stress.py` on 2026-09-24. The first 14 structured legal sources passed. The next source was `chain(20)`: 21 variables, 20 clauses `[(i+1), -((i+1)%21+1), (i+1)]` for `i=0..19`, with clause `c_i` incident to `v_i` and `v_(i+1)` in a path rotation. [`stress.py`](stress.py) constructs the exact JSON and validates it with the independent source checker.

Expected: a validated crossing-free orthogonal drawing of the connected-cover core. Actual: `RecursionError: maximum recursion depth exceeded` in `tsmpy/tsm/compaction.py`, `face_side_processor → set_side → set_side` repeated more than 990 times. The preceding assertions confirmed the generated graph was legal, planar, connected and degree-at-most-four, and its leaf-free core was biconnected and bridgeless. This is an implementation execution failure, not a graph-theoretic obstruction or a target NO answer.

Preserved revision: `drawing.checked_layout` in commit `dc9a9f4`, before the wrapper repair. Re-run the command above on that commit to reproduce. No target point set was returned for this input.
