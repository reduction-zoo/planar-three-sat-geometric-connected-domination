# Lichtenstein's unit-disk geometry is an omitted obligation

## Claim and applicability

Tags: unit disk, geometric connected domination, planar SAT, rational coordinates. Lichtenstein (1982), Theorem 5, uses distance at most one and a pictorial variable/ground/clause construction, but its proof does not specify the rational-point embedding algorithm or polynomial precision bound. This matters when reconstructing an executable instance map from the paper.

## Evidence and status

Primary source inspected 2026-09-23: https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lichtens.pdf, printed pp. 336–340. The final paragraph of the proof on p. 340 explicitly omits the rational-coordinate demonstration. Local audit; no independent review. See [round 001](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/001/round.md).

## Consequence for search

The theorem supports hardness attribution but cannot by itself be transcribed into the required executable F. A reconstruction must supply coordinates, exact distance checks, spacing and bit-cost bounds, and decoding for all valid target outputs.

## Use history

- 2026-09-23: extracted from round 001; no later application yet.
