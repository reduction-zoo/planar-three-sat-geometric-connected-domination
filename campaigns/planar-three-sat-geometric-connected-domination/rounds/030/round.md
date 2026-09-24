# Round 030 — visibility drawing route

## Plan

Gap: inherited exterior rectangularization remains unproved. Materially different mechanism: construct a bar-visibility representation using a planar st-orientation and its dual, then route the at-most-four incidences locally inside separated vertex strips. This uses topological orders rather than face reflex splitting. Finite literature scope: the handbook's visibility algorithm and cited primary Tamassia–Tollis construction. First discriminating check: does an arbitrary st-numbering of a biconnected plane graph provide the needed consecutive incoming/outgoing edge blocks and an acyclic dual? If yes, implement an elementary ear-insertion st-numbering and check those premises before attempting coordinate routing. Relevant experience: a drawing theorem needs all implementation interfaces specified; no additional backend is accepted just by name.

## Evidence and diagnosis

Implemented [visibility.py](visibility.py): start with an s–t path after deleting edge st; repeatedly take a component outside the current order, choose two distinct boundary vertices, and insert an internal path between them just after the earlier endpoint. Biconnectivity guarantees two boundary vertices. Every insertion preserves existing earlier/later neighbors and gives each inserted vertex both, so it yields an st-numbering in polynomial time (at most V insertions, each using graph searches). Edge st puts source and sink on a common face; the standard plane st-graph dual supplies the visibility construction.

The test first failed for the absent module, then `uv run --locked python .../rounds/030/test_orientation.py` passed all 163 biconnected planar max-degree-four atlas graphs: valid order, consecutive incoming/outgoing blocks, and dual DAG with unique source/sink. The directed dual omits edge st; the eventual geometric realization must restore that boundary edge explicitly.

Primary route: Tamassia–Tollis, *Plane Representations of Graphs and Visibility Between Parallel Segments*, [institutional report](https://www.ideals.illinois.edu/items/100572), and the [Duncan–Goodrich visibility algorithm](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/orthogonal.pdf), §7.2.3. This is reconstruction of published geometry, not a new hardness theorem.

Experience extraction: none yet; the st-order subroutine is elementary and the full replacement has not been constructed. Next action: turn the dual order into exact bar visibility and verify every nonincident bar/edge intersection, including restoration of st.
