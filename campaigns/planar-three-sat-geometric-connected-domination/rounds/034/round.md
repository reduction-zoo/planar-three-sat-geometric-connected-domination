# Round 034 — bounded compact layout with guaranteed fallback

## Plan

Gap: the polynomial visibility drawing has larger routes than the current compact candidate. Mechanism: permit the old backend only for cores of at most 1,000 vertices, under a fixed deterministic Python-line execution budget, and accept only exact validated drawings with linearly bounded bend count/coordinates. Otherwise invoke the explicit visibility construction. This is a finite operation bound, not a solver/subprocess/campaign time cutoff; it is part of deterministic F. First check: force the operation allowance to zero and obtain a valid fallback on cycle/cube/octahedron and prepared core 1, then compare the ordinary branch with the old validated point layout. Relevant experience: opaque backends need not be trusted for totality if a bounded attempt has a correct polynomial fallback. Before integration, retain old F evidence and execute independent witness recovery after the change.

## Evidence and diagnosis

The regression first failed because the old function had no operation-budget interface. After implementation, all four forced-zero-allowance cases returned valid real fallback drawings. The ordinary branch passed the 111 prepared nonempty core layouts with exactly the earlier aggregate bounds: maximum core 946, drawn vertices 997, total route length 10,224, coordinate magnitude 172 (`drawings.txt`). Standalone exact verification still passed its 15 small actual targets, and `test_interface.py` passed empty/canonical/side-chain plus 14 negative fresh-process F/G checks.

The complete construction and polynomial bounds are now spelled out in [drawing-proof.md](../../work/drawing-proof.md). The optional compact branch has a fixed input-size and instruction allowance, plus explicit output-size and exact geometry checks; all other executions take the explicit visibility fallback. This closes the previously acknowledged library-totality assumption at the candidate-proof level, pending independent review. Full prepared target verification is still needed after this map change.

Experience extraction: updated [backend contract](../../../../research/experience/orthogonal-drawing-backend-contract.md): finite validated attempts can precede an explicit total construction. Next action: independently find target witnesses using coordinate-only admissible search restrictions, treating restricted UNSAT as unknown, then run the full prepared F/G suite.
