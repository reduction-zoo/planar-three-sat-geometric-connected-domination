# Round 016 — drawing totality stress audit

## Plan

Gap: the candidate's orthogonal drawing call is empirically valid on the 112 prepared cases, but a 2021 implementation documents overlay and cut-edge limitations. Mechanism: audit the generated connected-cover core family structurally, then stress the exact drawing validator on legal source formulas well outside the prepared sizes and incidence patterns. The geometric-port and oracle-scale experience findings apply as checks, not as proof of this route. First check: construct large stars, isolated-variable families and incidence chains from explicit planar rotations; require every core to be connected, planar, degree at most four and bridgeless, and every returned layout to pass exact segment validation. A failure gives a concrete legal-input counterexample; passes only extend finite evidence and leave a proof obligation.

## Evidence and diagnosis

[`stress.py`](stress.py) generates 24 legal source formulas across isolated-variable, repeated-unit star, incidence-chain, incidence-cycle and branching-tree families, with up to 41 variables and 20 clauses. Every source passes the independent source validity checker. The abstract cover bridge is checked for planarity and degree bounds; the connected-cover core is checked connected, planar, biconnected and bridgeless; returned orthogonal drawings are checked for exact integer coordinates, nonoverlap, noncrossing and topology preservation.

The first run failed on the legal `chain(20)` case. [`failure.md`](failure.md) retains the input construction, command, expected/actual behavior and traceback before repair. The cause is `tsmpy`'s recursive face orientation exceeding Python's default recursion limit; it does not refute the drawing theorem. `drawing.checked_layout` now sets a recursion allowance linear in the input core size. The same command subsequently passed all 24 cases. Largest observed core: 2,136 vertices; largest routed drawing: 2,453 vertices; largest total unscaled route length: 97,170. Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/016/stress.py`.

First discriminating check: **implementation defect repaired for the tested family; general totality and polynomial output bound still unproved**. No target point sets or independent target solutions were produced for these stress sources. The repository's working proof remains conditional on a drawing implementation guarantee.

Experience extraction: [one new library-recursion entry](../../../../research/experience/tsmpy-face-recursion.md).

## Next action

Seek a certified polynomial orthogonal drawing route or a source-family proof that the chosen implementation is total and polynomial; separately continue nontrivial target verification.
