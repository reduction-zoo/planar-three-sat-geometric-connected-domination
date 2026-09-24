# Clause-choice Grid Tiling causes a large unit-disk instance

## Claim and applicability

Tags: Grid Tiling, unit disk, connected domination, instance growth, verification. Composing the three-choice-per-clause SAT-to-Grid-Tiling bridge of this campaign with the 16 Y-blocks per gadget in de Berg–Bodlaender–Kisfaludi-Bak (2019) yields at least `16m²(9m²+1)` points for `m` clauses, before X-blocks and connectors. This applies to that precise composition, not to unit-disk reductions in general.

## Evidence and status

The paper's §2.4 states 16 Y-blocks per tile gadget; §2.1 gives `N²+1` points per Y-block. The bridge has `m²` gadgets and alphabet `N=3m`. See [round 007](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/007/round.md) and `route_scale.py`. Arithmetic checked on 2026-09-23; no independent review. The smallest prepared nontrivial NO case needs at least 11,808 Y points.

## Consequence for search

Budget target verification before implementing this chain. A pointwise `O(|P|²)` adjacency builder and layered reachability solver cannot handle the full prepared corpus at this scale in the current workflow. A smaller direct construction or a different independent target oracle is needed for executable verification.

## Use history

- 2026-09-23: extracted from round 007 and used in its stopping decision.
