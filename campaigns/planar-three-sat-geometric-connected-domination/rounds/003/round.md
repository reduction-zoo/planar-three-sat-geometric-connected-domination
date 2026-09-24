# Round 003 — equality wire from repeated choice cells

## Plan

Gap: a clause point cannot span the distance between variable gadgets. Mechanism: copy the two-choice cell along a route and use two local clause points to forbid both unequal neighboring truth choices, thereby propagating a literal. Search finite placements of a second cell under the eight square symmetries and integer translations within four units, with clause points on the half-integer grid. First discriminating check: require each equality point to touch exactly its intended cross-sign pair and none of the two wrong ports, ground or private points. A success would justify a full CDS budget/connection test; failure excludes this particular two-cell half-grid interface, not all wires. Prior evidence: round 002's exact integer local cell and port-distance obstruction. The [port-distance bound](../../../../research/experience/clause-port-distance-bound.md) applies: both intended port pairs must be at distance at most two.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/003/wire_search.py` ran on 2026-09-23. The finite family has eight square symmetries, translations with each component in [-4,4], and candidate clause sites on a half-integer grid in [-5,5]². Of 542 non-overlapping cell placements, only five put both required cross-sign port pairs within distance two. None has both half-grid equality points while keeping each point more than unit distance from the wrong sign ports and the two ground points. The stricter condition excluding leaf/private points also has zero survivors. The five close placements are printed by the script, so the family is reproducible.

The cause is geometric interference in this specific repeated-cell layout: bringing both desired cross-sign pairs close also brings each proposed clause disk into reach of a wrong selectable point or the ground, at the sampled half-grid sites. The search gives a conclusive finite-family exclusion only. It does not rule out quarter-grid coordinates, different cells, extra forced points, or Lichtenstein's long variable-row mechanism. No complete F or G was obtained.

Experience extraction: none. The bound and coordinate family are too tied to this local design to guide a broader campaign beyond the existing [port-distance entry](../../../../research/experience/clause-port-distance-bound.md), whose application is recorded below.

## Next action

Investigate a materially different row/ground/clause construction from primary literature, seeking exact coordinates or a route to them.
