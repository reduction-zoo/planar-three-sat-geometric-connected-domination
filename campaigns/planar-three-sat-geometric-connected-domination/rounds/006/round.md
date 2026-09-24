# Round 006 — exact block adjacency audit

## Plan

Gap: the later Grid Tiling construction states many small coordinate offsets; transcribing them without exact distance checks risks extra edges. Mechanism: audit the local `Y1–X1–Y2` block pattern from §2.3 using rational arithmetic, with block centers at `(-2,0),(0,0),(2,0)` and disk radius one (so center threshold two). Scope: alphabet sizes 2 through 5 and `ε=1/(100N⁴)`. First discriminating check: for every `X1(j)` and every `Y1(t),Y2(t)`, compare exact disk intersection with the theorem's claimed suffix/prefix pattern; also check all disks within a block intersect. A mismatch invalidates the transcription or parameter choice; a pass supports only this local ordering interface. Prior evidence: round 005's tiling bridge. The earlier omitted-geometry lesson applies to exact coordinates, while the direct clause-port distance bound does not govern this overlapping-block mechanism.

## Evidence and diagnosis

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/rounds/006/block_audit.py` passed on 2026-09-23: 2,064 exact cross-block squared-distance checks for alphabet sizes `n=2..5`, plus all within-block pair checks. With `ε=1/(100n⁴)`, `X1(j)` intersects precisely `Y1(t)` for `t≥j` and `Y2(t)` for `t<j`. This reproduces one suffix/prefix interface in §2.3 of the [2019 primary paper](https://link.springer.com/article/10.1007/s00453-019-00561-0). It says nothing yet about the 16-block cycle, connectors, forced parent points, or whole connected dominating sets.

The paper's displayed inverse formula for `f(x,y)=(x−1)n+y` is inconsistent at multiples of `n` if read literally as `1+floor(j/n), 1+(j mod n)`. The local check uses the mathematically correct second coordinate `(j−1) mod n +1`. This is a transcription ambiguity to resolve during any complete implementation, not a demonstrated flaw in the theorem.

Experience extraction: none. The exact check is a local implementation component and does not yet yield a general reusable geometric principle beyond the existing requirement to prove all adjacencies.

## Next action

Map the full 16-block cycle and forced parent geometry, then test connected canonical sets on minimal tiled instances.
