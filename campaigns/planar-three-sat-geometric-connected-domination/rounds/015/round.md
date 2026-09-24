# Round 015 — sound unit-contradiction shortcut

## Plan

Gap: the independent target solvers cannot currently decide the large negative point sets, leaving the required `NO-SOLUTION` recovery branch unverified. Mechanism: apply deterministic polynomial unit propagation to the fixed 3-CNF source before the geometric chain. A derived contradiction certifies the source unsatisfiable, so emit the legal one-point target with `K=0`; this preserves the reduction and gives an independently solvable actual negative target. If no contradiction is derived, retain the geometric route unchanged. The earlier oracle-scale finding motivates this size reduction, but it does not justify any unsound source classification. First check: compare contradiction results against the independent prepared source labels, then run the target oracle and F/G subprocess recovery on every shortcut case. The result supports only the shortcut class, not the unsimplified geometry.

## Evidence and diagnosis

`work/algorithm.py` now scans distinct literals per clause, drops tautologies, repeatedly assigns forced unit clauses, and returns a one-point `K=0` target only upon a contradiction. This is a polynomial source transformation: each assigned unit is required in every satisfying assignment of the current simplified formula, and a derived empty clause proves the original unsatisfiable. Inputs without a derived contradiction still enter the same geometric construction, so this does not establish any result about general satisfiability by itself.

Against the independent prepared source labels, the shortcut triggered on exactly 14 cases, all labeled NO, and on none of the 98 SAT cases. [`work/test_interface.py`](../../work/test_interface.py) then executed F and G as separate subprocesses for all 14 shortcut cases. The unchanged exact target oracle independently returned `NO-SOLUTION` for each actual one-point target, and the recovered NO answer passed the independent source oracle. Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/test_interface.py`; output: `empty, canonical, side-chain and 14 negative F/G subprocess cases passed independent target checks`.

First discriminating check: **supported on all 14 prepared negative cases**. The campaign now has actual independently solved positive and negative F-produced targets, but independent solving of the large nontrivial positive geometric targets and all-input drawing totality remain open. The full 112-case candidate harness still cannot finish at the first large positive case; this shortcut does not change that execution limit.

Experience extraction: no new file. The [oracle-scale entry](../../../../research/experience/connected-domination-oracle-scale.md) records that this sound shortcut supplied negative target coverage; it did not make large-target solving tractable.

## Next action

Audit the orthogonal drawing implementation for totality and polynomial bounds on every generated core; if it cannot be justified, seek a deterministic polynomial replacement.
