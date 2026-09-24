# Round 019 — core biconnectivity lemma audit

## Plan

Gap: the candidate removes original pendant leaves before calling the orthogonal drawing backend, relying on the remaining connected-cover core being biconnected and bridgeless. This has been checked finitely but lacks a general argument in the working proof. Mechanism: audit the face-cycle construction as a planar graph lemma for subcubic source-cover graphs of minimum degree two, and search small planar graphs exhaustively for counterexamples. Prior library-recursion experience applies to implementation, while the clause-port findings do not. First check: enumerate the relevant NetworkX graph atlas through seven vertices, filter connected planar graphs with degrees two or three, apply the exact Garey–Johnson face construction and test biconnectivity after removing pendant leaves. A counterexample would invalidate the backend premise; a pass supports but does not prove the lemma. Then write the local face-cycle argument or mark its unresolved step.

## Evidence and diagnosis

[`atlas_core.py`](atlas_core.py) enumerated every connected graph in NetworkX's seven-vertex graph atlas with minimum degree two, maximum degree three and a planar embedding, then applied the exact face-cycle construction. All 38 eligible connected graphs produced connected planar degree-at-most-four graphs whose leaf-free cores were biconnected and bridgeless. Six disjoint unions of cycles and cubic graphs passed the same checks. Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/019/atlas_core.py`; largest checked core had 89 vertices.

The working [proof](../../work/proof.md) now includes a local deletion argument for the generated core. Every subdivider joins each incident face cycle; each original node has minimum degree two; and every face cycle has at least three spokes. Deleting a subdivider or original vertex leaves its incident branches connected around neighboring face cycles. Deleting a face-cycle node leaves the rest of its cycle connected and its spoke neighbor attached through another boundary subdivider. The merged outer-face cycle links disconnected source components. These are the structural facts needed by the `tsmpy` input domain and were checked in the finite atlas sweep.

First discriminating check: **core biconnectivity supported by a general local argument and finite counterexample search**. This narrows the drawing gap: the current uncertainty lies in the drawing package's all-input execution and output bounds, not in an observed cut edge of the generated core. No independent target solving was done in this round.

Experience extraction: none. The structural lemma belongs in the candidate proof; the finite sweep found no new counterexample or broadly reusable failure.

## Next action

Use the final authorized round to audit whether the candidate meets every fixed acceptance obligation; preserve unresolved gaps and close the campaign at the 20-round budget without claiming unsupported verification.
