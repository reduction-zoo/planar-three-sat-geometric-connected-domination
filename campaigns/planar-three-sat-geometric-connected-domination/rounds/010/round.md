# Round 010 — constructive orthogonal drawing

## Plan

Gap: Clark's target construction requires a polynomial rectilinear grid drawing of the connected planar degree-four graph, while the source bridge currently produces only an abstract embedding. Mechanism: use a published polynomial orthogonal drawing algorithm, checking whether an executable implementation gives exact integer edge routes for the graphs from round 009. The prior geometry experiences warn against accepting a diagram without coordinates; their specific gadget failures do not apply. First discriminating check: remove the pendant leaves temporarily, confirm the resulting cores meet the drawing algorithm's input conditions, and test its output for crossings and unintended grid contacts. A usable implementation must provide explicit routes and a polynomial bound; otherwise this remains an unimplemented theorem lead.

## Evidence and diagnosis

The graph-drawing theorem is constructive: Tamassia's [graph-drawing handbook chapter, §7.3](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/orthogonal.pdf) describes polynomial orthogonal grid drawings for embedded planar graphs of maximum degree four. A small Python implementation, [`tsmpy` 0.9.3](https://pypi.org/project/tsmpy/), exposes the topology-shape-metrics route. Its documentation requires connected degree-at-most-four input and warns that cut edges are unsupported; it imports Matplotlib even when no figure is requested. Those dependencies were tried ephemerally with uv; they are not yet in `uv.lock`.

[`drawing.py`](drawing.py) removes the pendant leaves from each connected-cover graph and checks the resulting core is biconnected. It runs `TSM(..., uselp=False)` and independently validates distinct integer vertex positions, axis-aligned nonzero segments, no segment intersection except shared endpoints, and exact recovery of the original graph after suppressing degree-two bend vertices. Command: `uv run --locked --with tsmpy --with matplotlib python campaigns/planar-three-sat-geometric-connected-domination/rounds/010/drawing.py`. Result: all 111 nonempty prepared cores were biconnected and passed the drawing validator. Largest observed core: 946 vertices; largest routed graph: 997 vertices; maximum total unscaled route length: 10,224; maximum coordinate magnitude: 172. The empty source requires a direct trivial target case.

This supports exact coordinates on the prepared inputs. It does **not** yet prove that the package succeeds for every legal generated core, that the core is always biconnected, or that its output size is polynomial in all cases. Those are proof obligations, not known counterexamples. A validated drawing can be scaled to separate routes; the scale and private-neighbor placement remain to be specified.

First discriminating check: **supported on 111 prepared nonempty cases; general implementation guarantee inconclusive**. Actual F-produced target instances solved: 0; target outputs recovered: 0.

Experience extraction: none. A documented implementation limitation is recorded here; no newly established general obstruction was found.

## Next action

Design exact private-neighbor points and prove or test the arbitrary-connected-dominating-set decoder on the routed drawings.
