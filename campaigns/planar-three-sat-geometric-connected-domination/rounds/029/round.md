# Round 029 — rectangularization premise audit

## Plan

Gap: exact arithmetic does not certify inherited rectangularization. Hypothesis: every biconnected planar degree-four graph admitted by the core interface has valid shape, reflex-corner splitting and positive integer compaction under the experimental pipeline. First discriminating check: all biconnected planar max-degree-four graph-atlas graphs (at most seven vertices), including topologies absent from generated cores, must pass independent layout/topology validation. Then trace the corner-count termination argument and the exterior-frame exception in the actual code. A counterexample refutes the broad backend premise even if the generated family survives. Relevant experience: backend-contract findings prevent treating arithmetic repair as complete certification.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/029/atlas.py` validated all 163 admitted graph-atlas graphs. The broad finite premise survives. The proof attempt identifies a useful potential: splitting a 270-degree reflex corner into 90+180 degrees reduces the number of reflex corners by one, while the opposite edge's new split vertex introduces no reflex corner. Hence ordinary simple-face rectangularization needs at most the original number of reflex corners.

The actual backend first connects an exterior frame to the original exterior boundary by one bridge. That creates a face walk with repeated vertices/edges, so the simple-polygon argument alone does **not** justify the implementation's `find_front` and repeated-boundary `Dcel.connect` choices. The [Duncan–Goodrich chapter, §7.3.2](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/orthogonal.pdf) delegates rectangularization detail to the graph-drawing textbook; it does not settle this code correspondence. This leaves a specific proof obligation, despite passing all 163 finite layouts. No general guarantee is claimed.

Experience extraction: updated [backend contract](../../../../research/experience/orthogonal-drawing-backend-contract.md) with the weak-face issue. Next action: investigate a materially different visibility-based drawing construction, avoiding the inherited rectangularization operation.
