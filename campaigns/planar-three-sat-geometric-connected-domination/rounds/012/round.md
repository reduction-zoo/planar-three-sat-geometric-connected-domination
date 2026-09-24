# Round 012 — arbitrary connected-domination output recovery

## Plan

Gap: the point construction has only been tested in the forward direction. A valid target output may contain side-chain points, omit middle path points, or choose a different connector pattern. Mechanism: implement the constructive transformations in Clark–Colbourn–Johnson Lemma 6.1 to replace selected side points by middle path points without increasing cardinality, then extract a connected cover from all normalized target outputs by their Lemma 6.2 and the source bridge. The new experience entry on impossible independent side leaves applies; side chains must be handled rather than removed from the construction. First check: derive a local replacement for both fully covered pair paths and paths with a missing pair, then validate domination, connectivity and size after each replacement on actual constructed graphs and perturbations. If a replacement fails, save the exact target output and diagnose whether the published lemma's hypotheses were met.

## Evidence and diagnosis

Clark–Colbourn–Johnson [Lemma 6.1 and Lemma 6.2](https://cs.du.edu/~snarayan/sada/research/docs/res/unitdisk.pdf) supply the normalization and reverse count. [`decode.py`](decode.py) implements a finite, polynomial search over those lemma-prescribed replacements. For one edge, if every middle path pair has its path vertex or side vertex selected, replace all selected side vertices by path vertices. Otherwise choose a pair with neither selected. Its side vertex must be dominated by a selected neighboring side vertex. For each possible side neighbor and direction to an endpoint, replace the side vertices in that prefix or suffix by path vertices and add the omitted pair's path vertex. Accept only a candidate that keeps connected domination and does not increase size. Each accepted step removes a selected side vertex, so at most the input point count many steps occur. The bounded search and the independent legality check prevent a bad replacement from silently corrupting recovery.

After side vertices are removed, the original graph vertices selected in the connected dominating set form a connected cover with the published cardinality bound; the source bridge then recovers a satisfying assignment. [`grid.py`](../011/grid.py) was strengthened to verify that adjacent side vertices belong to consecutive pairs on the same original edge, the geometric premise used in this normalization. The full 111-case geometry check still passes.

Command: `uv run --locked --with tsmpy --with matplotlib python campaigns/planar-three-sat-geometric-connected-domination/rounds/012/decode.py`. Result: 97 nonempty canonical target witnesses decoded to satisfying assignments. Prepared case 1 also admitted a distinct exact-budget target witness obtained by seven valid side-chain swaps; the decoder normalized and decoded it. This is **one** alternate target output, not arbitrary-output test coverage. Empty source case uses a direct target special case later. No prepared NO target instance has been independently solved.

First discriminating check: **supported on canonical outputs and one noncanonical side-chain output; general proof and verification pending**. The published lemma is a credible general basis, but implementation totality on all legal generated point sets depends on the drawing and side-placement premises proved in later work.

Experience extraction: none. The side-chain obstruction already has its round-011 entry; this round supplies the repair and its observed effect.

## Next action

Integrate deterministic F/G in the required subprocess interface, lock drawing dependencies, and write the general construction and recovery proof.
