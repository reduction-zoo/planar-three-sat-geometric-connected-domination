# Campaign state

Budget: 20 rounds. Used: 1.
Board source: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.

Capability probe (2026-09-23, local macOS): Python 3.12.14 at `/Users/xiweipan/.local/bin/python3` available; uv 0.12.17 at `/Users/xiweipan/.local/bin/uv` available; Z3 executable 5.1.0 at `/opt/homebrew/bin/z3` available; Kissat 4.0.4 at `/opt/homebrew/bin/kissat` available; cvc5, Minisat and CP-SAT executables absent; Typst 0.15.1 at `/opt/homebrew/bin/typst` available; Lean 4.34.0 and Lake 5.0.0 at `/opt/homebrew/bin/lean` and `/opt/homebrew/bin/lake` available; Mathlib installation unconfirmed (pending if formalization is requested); external writing skill `sci-brain:how-to-technical-writing` present at `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md`. Prepare locked Python bindings Z3 5.1.0.0 and NetworkX 3.7 in `uv.lock`.

Prepare: [contract](work/contract.md), [112 fixed cases](work/cases.json), [oracles](work/check.py), [evidence](work/preparation.md). Self-test passed on 2026-09-23. No candidate yet.

Current claim: none. Correctness, novelty and significance are unassessed. Main obstacle: a geometric construction whose exact unit-distance adjacencies implement the planar formula while supporting recovery from every connected dominating set of size at most K.
Next action: test a concrete geometric interface in round 002. Round 001 established the matching target model and the cited proof's omitted rational embedding; it did not produce F or G.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | Audit cited Lichtenstein variable/ground/clause construction | Does Theorem 5 use exact unit-distance graph and give rational coordinates? | inconclusive: model matches, coordinates omitted | [round](rounds/001/round.md) |
