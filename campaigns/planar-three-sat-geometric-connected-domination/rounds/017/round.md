# Round 017 — alternate orthogonal backend audit

## Plan

Gap: the candidate's `tsmpy` backend still lacks a demonstrated all-input correctness and polynomial-size guarantee. Mechanism: inspect and trial an independently implemented orthogonal-layout backend on the same generated cores, with exact geometric validation and explicit detection of heuristic fallback. Prior experience on library recursion and unintended adjacency applies; a second library's name alone is not evidence. Finite search scope: the 2026 `graph-layout` GIOTTO implementation and official OGDF orthogonal API, compared against the already checked small cores. First check: can the API return integer point-vertex coordinates and explicit axis-aligned routes that pass our no-crossing validator, without a silent heuristic path? If so, assess it as a fallback; if not, record the concrete mismatch and continue with a mathematical implementation strategy.

## Evidence and diagnosis

The 2026 [`graph-layout` GIOTTO API](https://pypi.org/project/graph-layout/) exposes explicit edge bends and reports whether its bend-optimal route was used. Its documentation says a requested bend-optimal route can silently fall back to a heuristic for some inputs, so [`alternate.py`](alternate.py) requires `used_bend_optimal`, converts its observed half-integer coordinates exactly to doubled integers, and passes the resulting point-vertex graph through the same independent nonoverlap, noncrossing and topology validator used for `tsmpy`.

Commands: `uv run --locked --with graph-layout python campaigns/planar-three-sat-geometric-connected-domination/rounds/017/alternate.py --all` and the same command with `--stress`. Results: all 111 nonempty prepared cores and all 24 structured legal-source stress cores used the bend-optimal path and passed exact validation. Maximum doubled-grid total route length was 15,312 on prepared cores and 199,808 on stress cores. This is an independent implementation cross-check of finite drawings. The library was used ephemerally and was not added to the lock because no observed `tsmpy` failure remained after round 016.

The [official OGDF OrthoLayout documentation](https://ogdf.github.io/doc/ogdf/_ortho_layout_8h.html) supplies a mature C++ implementation lead, but its API was not integrated; it would require converting box/port layouts to the point-vertex routes needed by Clark's construction. No claim of a validated OGDF fallback is made.

First discriminating check: **second backend supports the same 135 finite cores; no all-input certification**. Both libraries implement versions of the polynomial graph-drawing method, but neither package's documented behavior alone establishes the candidate implementation's totality and polynomial output size for every legal source.

Experience extraction: none. The library reliability limitation is recorded in rounds 010, 016 and here; no new general obstruction or counterexample was found.

## Next action

Stress the arbitrary-output decoder with distinct side-chain witnesses across varied prepared positive instances; retain any counterexample before modifying the proof.
