# Round 004 — alternative geometric construction literature

## Plan

Gap: the local choice cell cannot be extended by the tested equality wire, while the cited proof omits rational coordinates. Mechanism: use a row/ground/clause layout or a later unit-disk connected-domination hardness proof with explicit geometric placement. Finite scope: search primary papers that cite or reprove Lichtenstein's result and inspect at most three construction proofs for coordinate algorithms, exact adjacency arguments and decoding. First discriminating check: find a proof that states coordinates or a fully specified placement rule and whose source is convertible from the fixed embedded planar 3-SAT input. A match would seed an executable candidate; otherwise record precise omissions and stop this literature branch. Prior evidence: rounds 001–003 and both applicable experience entries. This is a distinct construction strategy from the repeated-cell wire.

## Evidence and diagnosis

Primary sources inspected 2026-09-23: [Lichtenstein 1982](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lichtens.pdf), printed pp. 336–340; [de Berg, Kisfaludi-Bak and Woeginger, *The Homogeneous Broadcast Problem in Narrow and Wide Strips II: Lower Bounds*](https://link.springer.com/article/10.1007/s00453-019-00561-0), §2.4; and its [2016 extended abstract](https://www.eurocg2016.usi.ch/sites/default/files/paper_22.pdf), §§2–3. The 1990 Clark–Colbourn–Johnson paper's abstract was also checked, but its full proof was not available in this finite scope. The 2004 bounded-density thesis only cites Lichtenstein for connected domination, so it adds no independent construction.

The 2019 paper has a genuinely different construction: Grid Tiling instances map to connected dominating sets in a unit-disk graph with 16 choice blocks and 36 forced parent points per grid gadget, plus connectors. It states a budget `56k² - 4k`, many coordinates, and logarithmic precision after perturbation. It is therefore a viable *lead*, but does not directly accept embedded planar 3-SAT. Its block offsets come from Marx's earlier domination proof, and the paper uses square-root expressions for some coordinates before asserting rational precision. An executable F would need both a polynomial source-to-Grid-Tiling bridge and fully rationalized, exact point generation; an executable G would need to normalize arbitrary feasible connected dominating sets, then decode a tiling and a SAT assignment. No such implementation or general proof was obtained in this round. The extended abstract omits still more coordinate details. No prior source in this scope gives a complete direct answer to the fixed task.

First check: an explicit-coordinate *framework* exists, but not a plug-in algorithm for this source/output contract. Outcome inconclusive for a complete reduction. This is an untested lead, not a verified candidate.

Experience extraction: none. The source mismatch and missing implementation are specific to this prospective composition and do not add a general finding beyond the existing omitted-geometry entry.

## Next action

Test the standard clause-choice compatibility graph to Grid Tiling bridge, including extraction, before considering the much larger target construction.
