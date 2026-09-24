# Round 021 — drawing arithmetic and runtime audit

## Plan

Resume with 20 additional rounds (021–040), preserving rounds 001–020. Gap: all-input totality and polynomial runtime of the actual drawing backend. Mechanism: audit tsmpy 0.9.3's flow implementation, including finite capacities and solver choice. First check: an exact two-face flow requiring more than its hard-coded capacity, followed by tracing whether the generated-family proof bounds every such demand. This distinguishes an actual library limit from an unproved generated-input counterexample. Relevant experience: drawing recursion and omitted rational embedding; board experience directory is absent. No candidate change is planned in this audit.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/021/audit.py` returns feasible at 4294967296 and infeasible at 4294967297. This is a library-level counterexample to unrestricted face-flow capacity, **not** a legal-source counterexample. `Flow_net.min_cost_flow` delegates to NetworkX `min_cost_flow`/network simplex; no polynomial worst-case argument for that implementation is provided by the existing proof. Compaction independently fixes total flow and capacities at the same constant. The generated core's biconnectivity does not discharge these arithmetic/runtime obligations. No assertion of observed F failure is made.

Capability delta (2026-09-24): uv-managed Python 3.12.14; Z3, NetworkX and tsmpy present; OR-Tools bindings absent from the locked environment; cvc5/Minisat still absent. Typst, Lean and Lake remain installed. Mathlib remains unconfirmed and unused, so it does not block construction. Shared board experience directory is absent; local entries remain readable.

Experience extraction: created [drawing capacity and runtime](../../../../research/experience/orthogonal-drawing-backend-contract.md). The current drawing is still a candidate. Next action: independent target-only search, then investigate a drawing implementation with explicit unbounded arithmetic and runtime guarantees.
