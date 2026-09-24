# Round 039 — deterministic reconstruction across processes

## Plan

Gap: the independent review refutes deterministic F on an asymmetric fallback source, undermining G's repeated construction. Mechanism: materialize induced graphs in parent node/edge order so component selection and path ties never inherit a filtered view's hash-set order; audit all remaining order-affecting traversals in both drawing branches. Prior experience: the backend-contract entry applies because a dependency's hidden behavior invalidates an algorithmic premise. First check: execute the exact reviewed public-F prefix under seeds 1 and 2, expecting equal layouts and route lengths; retain the pre-repair failure before changes. Then re-run affected layout checks, actual cross-seed target recovery, and the full prepared loop. Passing finite checks supports the implementation audit, not an all-input theorem by itself.

## Audit and checks in progress

The retained before-repair public-F prefix check failed exactly as the review predicted. Both filtered induced graphs now preserve explicit parent node/edge insertion order. The compact branch audit found NetworkX planar drawing uses `ready_to_pick.pop()` on a vertex set, so compact inputs now receive insertion-order integer labels before TSM and outputs are relabeled back. The locked tsmpy/NetworkX flow path otherwise uses ordered dictionaries, DCEL traversals and indexed arrays; generated bend labels do not feed unordered tie selection.

After repair, seeds 1 and 2 give equal large-source accepted layouts. All 174 exact layout checks pass. Actual forced exhaustion on prepared source 1 emits 330,596 points, budget 165,357; independent target-only search supplies and independently validates a witness at that budget, and fresh G seeds 2 and 3 return a valid assignment. Three compact sources likewise pass two F seeds and two recovery seeds. The forced launcher changes only the existing numeric allowance to zero and observes real visibility execution; it substitutes no dependency results. The reviewer confirmed this is valid branch coverage. A checker import-path mistake was fixed before execution; its diagnostic is retained.

Capability re-probe: Typst 0.15.1 remains available. `printf 'import Mathlib\n' | lean --stdin` fails with unknown module prefix on the current Lean 4.34.0 path; formalization remains unrequested and does not block this work.
