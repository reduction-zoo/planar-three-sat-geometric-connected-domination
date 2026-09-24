# Campaign state

Status: active; resumed 2026-09-24 after recognizing that the prior practical verification obstacle was not a hard blocker. Budget: 20 rounds. Completed: 13. Distinct construction route families attempted so far: 4 (Lichtenstein row/ground/clause; local ground/literal cell with equality wire; later Grid Tiling unit-disk construction; planar-cover to grid connected domination).
Board source: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.

Capability probe (2026-09-23, local macOS): Python 3.12.14 at `/Users/xiweipan/.local/bin/python3` available; uv 0.12.17 at `/Users/xiweipan/.local/bin/uv` available; Z3 executable 5.1.0 at `/opt/homebrew/bin/z3` available; Kissat 4.0.4 at `/opt/homebrew/bin/kissat` available; cvc5, Minisat and CP-SAT executables absent; Typst 0.15.1 at `/opt/homebrew/bin/typst` available; Lean 4.34.0 and Lake 5.0.0 at `/opt/homebrew/bin/lean` and `/opt/homebrew/bin/lake` available; Mathlib installation unconfirmed (pending if formalization is requested); external writing skill `sci-brain:how-to-technical-writing` present at `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md`. Prepare locked Python bindings Z3 5.1.0.0 and NetworkX 3.7 in `uv.lock`.

Prepare: [contract](work/contract.md), [112 fixed cases](work/cases.json), [oracles](work/check.py), [evidence](work/preparation.md). Self-test passed on 2026-09-23. No candidate yet.

Current claim: an executable F/G candidate and working proof exist, but the all-input drawing-library guarantee and full independent target verification remain open; no complete accepted reduction is claimed. Partial results: the earlier Grid Tiling bridge and local gadgets; a checked source bridge; 111 checked exact grid point sets with 98 forward witnesses; 97 canonical plus one alternate side-chain output decoded; and an end-to-end fresh-process F/G check on empty and nonempty targets. Only the trivial one-point F-produced target was independently solved by the target oracle. No review or manuscript exists.

Checks and limits: Prepare passed on 112 source cases (100 seeded, 12 edge), with source labels independently exhaustive-checked; local one-variable CDS enumeration passed 21 cases; a bounded equality-wire family excluded 542 placements; Grid Tiling bridge passed 112 independently solved instances; 2,064 local rational block adjacency checks passed. The geometric candidate has 111 checked nonempty point sets, 98 checked forward witnesses, 97 canonical and one side-chain output decoded, and one trivial F-produced target solved independently. Full candidate checking failed in target-oracle execution (first memory, then solver inconclusive after interruption); this establishes no general equivalence.

Prior stopping diagnosis in [round 007](rounds/007/round.md) was premature: its target-checker scale limit does not block further research. [Round 008](rounds/008/round.md) found a smaller published grid-graph route.

Experience closeout: 3 files created, 2 later updated, 0 pending: [omitted geometry](../../research/experience/lichtenstein-omitted-rational-embedding.md), [port distance](../../research/experience/clause-port-distance-bound.md), [route size](../../research/experience/grid-tiling-route-size.md). No publication or board changes.

Next action: try a different independent target-solving approach and audit drawing totality and output size. Reuse the committed Prepare corpus and oracle evidence.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | Audit cited Lichtenstein variable/ground/clause construction | Does Theorem 5 use exact unit-distance graph and give rational coordinates? | inconclusive: model matches, coordinates omitted | [round](rounds/001/round.md) |
| 002 | Integer-coordinate ground/literal/clause gadget | Exhaustive two-point CDS check on one-variable cases | supported locally; direct spaced composition refuted | [round](rounds/002/round.md) |
| 003 | Equality wire from repeated choice cells, distinct from direct clause composition | Bounded symmetry/translation and half-grid search for two isolated equality sites | refuted for stated finite family | [round](rounds/003/round.md) |
| 004 | Later Grid Tiling to unit-disk connected-domination construction | Does a primary proof supply explicit coordinates and fit the fixed source contract? | inconclusive: detailed target lead, source bridge and rationalization missing | [round](rounds/004/round.md) |
| 005 | Clause-choice compatibility bridge to Grid Tiling, new submechanism of later route | Independent tiled solve and assignment extraction on 112 cases | supported as combinatorial lemma | [round](rounds/005/round.md) |
| 006 | Published offset order interface for neighboring blocks | Exact suffix/prefix adjacency check for n=2..5 | supported locally; full gadget untested | [round](rounds/006/round.md) |
| 007 | Full Grid Tiling route scale and coordinate-specification audit | Y-block point lower bound for prepared nontrivial NO cases | inconclusive construction; supported stopping decision | [round](rounds/007/round.md) |
| 008 | Published planar connected-cover to grid-CDS route, distinct from Grid Tiling | Does a primary proof supply exact integer target coordinates and source recovery? | supported as a route; bridge/drawing/implementation pending | [round](rounds/008/round.md) |
| 009 | Lichtenstein planar cover composed with Garey–Johnson connected cover | Explicit degree/planarity/witness/recovery checks including repeats and disconnected inputs | supported bridge on 112 cases; full target pending | [round](rounds/009/round.md) |
| 010 | Polynomial orthogonal drawing theorem with executable TSM implementation | Biconnected core and exact noncrossing route validation on prepared graphs | supported on 111 nonempty cases; general guarantee pending | [round](rounds/010/round.md) |
| 011 | Scaled grid paths plus Clark side-chain points; independent-pendant variant tested separately | Exact adjacency/degree and forward witness on prepared graphs | side chains supported on 111; independent pendant variant refuted on case 1 | [round](rounds/011/round.md) |
| 012 | Clark side-chain normalization and arbitrary-output decoder | Canonical output plus exact-budget side-chain alternatives on actual point sets | supported on 97 canonical and one alternate output; general proof pending | [round](rounds/012/round.md) |
| 013 | Integrated F/G chain and exact sparse target-oracle repair | Fresh-process witness extraction and full prepared harness | interface supported; full target solving execution failure | [round](rounds/013/round.md) |
