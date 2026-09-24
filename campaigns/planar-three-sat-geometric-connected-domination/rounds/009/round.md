# Round 009 — source bridge through planar vertex cover

## Plan

Gap: the grid-CDS theorem starts from planar connected vertex cover, whereas the fixed source is embedded planar 3-SAT with repeated literals and disconnected incidence graphs allowed. Mechanism: compose Lichtenstein's planar 3-SAT-to-planar node-cover construction with Garey and Johnson's planar degree-three-cover-to-connected-degree-four-cover construction. Earlier experience on geometric port spacing and Grid Tiling size does not apply to these combinatorial gadgets. First check: audit explicit gadget costs and extraction for **every** cover, including repeated occurrences and disconnected embeddings. If valid, implement and test the bridge against prepared cases; if the published statements leave an unhandled input class, retain a concrete counterexample and repair or narrow the route.

## Evidence and diagnosis

Primary sources: Lichtenstein, [*Planar formulae and their uses* (1982), §4, Theorem 3](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lichtens.pdf), gives the variable-cycle and clause-triangle planar vertex-cover bridge. Garey and Johnson, [*The rectilinear Steiner tree problem is NP-complete* (1977), Lemma 2](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid1.pdf), give edge subdivisions plus face cycles and pendant leaves for connected planar vertex cover of degree four.

[`bridge.py`](bridge.py) implements both constructions. Repeated literal occurrences receive distinct cycle ports; clause occurrences with the same variable are reversed at the clause to fan parallel arcs without crossing. Cycle length is twice `max(2, occurrence count)`, so variable nodes have degree at most three. The planar-cover budget is the sum of the half-cycle lengths plus twice the number of clauses. For disconnected source incidence graphs, all components' selected exterior faces share one face cycle in the connected-cover graph. An empty formula produces an empty intermediate graph and will need a trivial target case.

Command: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/009/bridge.py`. Result: 112/112 constructed planar subcubic cover graphs and 112/112 connected planar degree-at-most-four graphs; for all 98 prepared SAT cases, a source assignment gave an exact-budget connected cover and recovered a satisfying assignment. The first seven cover instances were independently solved by Z3 at the stated budget, matching source labels (including NO cases). The remaining NO cover instances were not independently solved here. An interrupted full Z3 run returned an apparent mismatch at case 16 only because the solver was interrupted while checking; a fresh isolated solve returned SAT as expected. This is an execution interruption, not a counterexample.

The extraction of *any* connected-cover solution avoids canonicalizing it: retain its original vertices; for every original edge with neither endpoint retained, both subdivider vertices must be selected, so add one endpoint. The mandatory face-cycle vertices and at least one subdivider per edge pay for these additions, giving at most the original cover budget. Any planar cover within that budget has exactly half of every variable cycle and exactly two of every clause triangle; hence its cycle parity gives a satisfying assignment. This extraction argument does not rely on connected-cover minimality.

First discriminating check: **supported as a combinatorial bridge**. Actual F-produced target instances solved: 0; target outputs recovered: 0. A general proof of the face-cycle embedding and all special cases must be incorporated in the final proof if this route succeeds.

Experience extraction: none. The constructive source bridge is campaign-specific; the interrupted solver call is not a mathematical finding.

## Next action

Construct a polynomial rectilinear grid drawing of the resulting connected degree-four planar graphs, then audit Clark–Colbourn–Johnson's point placement and arbitrary-CDS recovery.
