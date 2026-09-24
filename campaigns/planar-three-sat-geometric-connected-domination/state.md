# Campaign state

Status: `stopped_without_discovery` (2026-09-23). Budget: 20 rounds. Used: 7; remaining: 13. Distinct construction route families: 3 (Lichtenstein row/ground/clause; local ground/literal cell with equality wire; later Grid Tiling unit-disk construction). The seven round scopes, including bridge and local audits, are counted separately below.
Board source: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.

Capability probe (2026-09-23, local macOS): Python 3.12.14 at `/Users/xiweipan/.local/bin/python3` available; uv 0.12.17 at `/Users/xiweipan/.local/bin/uv` available; Z3 executable 5.1.0 at `/opt/homebrew/bin/z3` available; Kissat 4.0.4 at `/opt/homebrew/bin/kissat` available; cvc5, Minisat and CP-SAT executables absent; Typst 0.15.1 at `/opt/homebrew/bin/typst` available; Lean 4.34.0 and Lake 5.0.0 at `/opt/homebrew/bin/lean` and `/opt/homebrew/bin/lake` available; Mathlib installation unconfirmed (pending if formalization is requested); external writing skill `sci-brain:how-to-technical-writing` present at `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md`. Prepare locked Python bindings Z3 5.1.0.0 and NetworkX 3.7 in `uv.lock`.

Prepare: [contract](work/contract.md), [112 fixed cases](work/cases.json), [oracles](work/check.py), [evidence](work/preparation.md). Self-test passed on 2026-09-23. No candidate yet.

Current claim: no complete reduction. Correctness, novelty and significance of a complete rule are unassessed. Partial results: a proved clause-choice SAT-to-Grid-Tiling bridge; a 21-case local geometric interface; and one exact block-order check. No executable F or G, target-instance injection, general geometric proof, independent review, or manuscript exists.

Checks and limits: Prepare passed on 112 source cases (100 seeded, 12 edge), with source labels independently exhaustive-checked; local one-variable CDS enumeration passed 21 cases; a bounded equality-wire family excluded 542 placements; Grid Tiling bridge passed 112 independently solved instances; 2,064 local rational block adjacency checks passed. Actual F-produced target instances solved: 0. Actual recovered outputs from F: 0. The tests establish no complete reduction.

Stopping diagnosis: direct single-point clause composition cannot span distant ports; the tested two-cell equality wire has no valid half-grid placement; Lichtenstein omits the rational embedding; and the alternate Grid Tiling route produces at least 11,808 points for the smallest prepared nontrivial NO case, beyond the current independent target checker. See [round 007](rounds/007/round.md). This is an investment decision, not an impossibility claim. Prospects within the remaining budget: low (uncalibrated judgment based on the missing full geometry, arbitrary-output decoder, and verification scale).

Experience closeout: 3 files created, 2 later updated, 0 pending: [omitted geometry](../../research/experience/lichtenstein-omitted-rational-embedding.md), [port distance](../../research/experience/clause-port-distance-bound.md), [route size](../../research/experience/grid-tiling-route-size.md). No publication or board changes.

Next action if resumed: develop a smaller exact geometric construction, or first build an independent target solver able to check the large published construction; then specify all rational coordinates and a decoder for every valid target output. Reuse the committed Prepare corpus and oracle evidence.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | Audit cited Lichtenstein variable/ground/clause construction | Does Theorem 5 use exact unit-distance graph and give rational coordinates? | inconclusive: model matches, coordinates omitted | [round](rounds/001/round.md) |
| 002 | Integer-coordinate ground/literal/clause gadget | Exhaustive two-point CDS check on one-variable cases | supported locally; direct spaced composition refuted | [round](rounds/002/round.md) |
| 003 | Equality wire from repeated choice cells, distinct from direct clause composition | Bounded symmetry/translation and half-grid search for two isolated equality sites | refuted for stated finite family | [round](rounds/003/round.md) |
| 004 | Later Grid Tiling to unit-disk connected-domination construction | Does a primary proof supply explicit coordinates and fit the fixed source contract? | inconclusive: detailed target lead, source bridge and rationalization missing | [round](rounds/004/round.md) |
| 005 | Clause-choice compatibility bridge to Grid Tiling, new submechanism of later route | Independent tiled solve and assignment extraction on 112 cases | supported as combinatorial lemma | [round](rounds/005/round.md) |
| 006 | Published offset order interface for neighboring blocks | Exact suffix/prefix adjacency check for n=2..5 | supported locally; full gadget untested | [round](rounds/006/round.md) |
| 007 | Full Grid Tiling route scale and coordinate-specification audit | Y-block point lower bound for prepared nontrivial NO cases | inconclusive construction; supported stopping decision | [round](rounds/007/round.md) |
