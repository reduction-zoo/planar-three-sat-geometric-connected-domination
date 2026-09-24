# Finite strip templates replace degree-bounded bar vertices

## Claim and applicability

Tags: bar visibility, orthogonal drawing, finite gadget certificates, monotone stretching. A bar with two to four vertical incidences has one of 46 top/bottom column patterns. Constant integer-grid path certificates can replace each bar by a point and disjoint orthogonal paths; strictly increasing horizontal stretching adapts the finite certificate to actual port columns.

## Evidence and status

[Round 032](../../campaigns/planar-three-sat-geometric-connected-domination/rounds/032/round.md) independently enumerates every pattern and checks every retained template's endpoints, simple paths, pairwise disjointness away from center, and strip confinement. Offline max flow found the certificates; runtime needs no solver. No independent review. Global separation is not established by the finite template check alone.

## Consequence for search

When degree bounds leave only finitely many local incidence patterns, a checked template catalog plus a monotone geometric map can replace an opaque routing library. Prove separation between the vertex strips and unrelated edges separately.

## Use history

Created 2026-09-24; intended board promotion requires separate authorization.

Round 033 composed all templates with integer visibility bars and validated 174 complete orthogonal embeddings. Scale 20, half-height four and four-unit end margins separate all strips and unrelated edges. The argument gives O(V) bends/coordinate magnitude and O(V²) total route length, assuming the standard visibility representation and biconnected input premise. Independent review remains pending.
