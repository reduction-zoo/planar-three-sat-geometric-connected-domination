# Round 031 — integer bar-visibility coordinates

## Plan

Gap: the new drawing route lacks exact coordinates and restored boundary edge st. Mechanism: use distinct topological face ranks for edge x-coordinates and st-order ranks for vertex y-coordinates; put st in a reserved exterior column, and take each vertex bar's incident-column span. First check: no edge segment intersects a nonincident bar or another edge interior in all 163 admitted atlas graphs and the first 12 prepared cores. The check uses explicit integer segment intersections, independent of the ordering code. Relevant experience: drawing legality must be checked geometrically, not merely by graph planarity. Failure will isolate the precise visibility convention needing correction.

## Evidence and diagnosis

The new method uses `x(e)=rank(left(e))` for all edges other than st, `x(st)=-1`, distinct st-order y-ranks, and the span of incident columns for each bar. The initial test failed for the absent coordinate function. After implementation, `uv run --locked python .../rounds/031/test_bars.py` passed all 163 admitted atlas graphs and 11 nonempty initial prepared cores. It checks every edge against every bar and every same-column edge pair, allowing only intended incidences/endpoints. No floating point or solver is used.

The standard directed-dual visibility argument applies to the st graph with its boundary edge reserved outside the other columns. Distinct topological ranks satisfy every dual arc inequality; tightening each bar to its incident columns preserves endpoint incidences and cannot create an intersection. The reserved st column is outside every other bar, and only source/sink bars are extended into it. Width is at most the number of faces plus one and height at most V−1, both linear.

Experience extraction: none yet; the complete point-vertex routing is the decisive next interface. Next action: exhaustively synthesize and validate all finite local port patterns, then stretch those templates into separated strips around the bars.
