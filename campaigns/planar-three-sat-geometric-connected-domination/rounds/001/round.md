# Round 001 — cited geometric construction audit

## Plan

Gap: no exact unit-disk gadget construction or decoding proof is available in this campaign. Hypothesis: Lichtenstein (1982), §6, Theorem 5 and Lemma 1, contain a reconstructible geometric connected-domination reduction from the fixed planar 3-SAT source. Scope: the cited paper and immediately necessary primary references only. First discriminating check: obtain the actual paper and identify whether the stated graph is the unit-disk graph on explicit rational points at threshold one, or a different geometric model. A match would justify transcription and a concrete gadget test; a mismatch would require a new construction mechanism. Prior evidence: only the board's unverified attribution. Experience search on 2026-09-23 found no relevant local/shared entries for domination, unit disks, or planar 3-SAT.

## Evidence and diagnosis

The primary paper was retrieved on 2026-09-23 from https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lichtens.pdf and inspected at printed pp. 336–340. Theorem 5 defines geometric connected domination using edges at Euclidean distance at most one, so the target model matches. Figures 12–15 sketch variable rows, a ground path and clause structures. Lemma 1 (p. 339) supplies a bipolar ordering of positive and negative incidences by replacing each variable with a cycle of implications. The proof sets a budget from variable, forced-clause and ground nodes plus one per clause. At p. 340, the author says the remaining task is embedding the graph at rational points with polynomial precision, calls it straightforward, and omits the demonstration. No coordinates, spacing algorithm, size bound or output decoder are specified there. The first check therefore supports the model match but leaves the executable geometric construction and exact-adjacency proof unresolved. This is an inconclusive reconstruction, not a refutation of the theorem.

The downloaded scan and rendered pages were transient reading material and removed; the primary URL and page references reproduce this inspection. The board's claimed local PDF path was absent in the read-only board checkout.

Experience extraction: [paper's omitted geometry](../../../../research/experience/lichtenstein-omitted-rational-embedding.md), created 2026-09-23.

## Next action

Try a directly testable variable/ground unit-disk interface before scaling to planar wiring; if it fails, diagnose whether a different geometric mechanism is required.
