# A direct clause point needs nearby literal ports

## Claim and applicability

Tags: unit disk, geometric SAT gadget, clause port, spacing. If one unit-disk clause point must be adjacent to two literal ports, those ports must be at distance at most two. Therefore copies of a local variable gadget whose relevant ports are farther apart cannot use one direct clause point to encode a shared clause.

## Evidence and status

General triangle inequality and the explicit four-unit-separated ports in [round 002](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/002/round.md); local check in `local_interface.py`. No independent review. The one-variable construction passes 21 finite cases, but its local correctness was not generalized to arbitrary embeddings.

## Consequence for search

Use wires or place ports of each clause within a radius-two region. A shared point cannot repair arbitrary spacing by itself.

## Use history

- 2026-09-23: extracted from round 002.
- 2026-09-23: round 003 used the distance-two filter before its half-grid site search; only five of 542 non-overlapping placements survived the filter, and none supported both isolated equality sites in that finite family.
