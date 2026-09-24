# Round 033 — composition of visibility strips

## Plan

Gap: finite port templates have not been composed into a complete graph drawing. Mechanism: multiply visibility coordinates by 20, stretch each template's odd columns to its edge columns, place intermediate columns midway, and use four-unit outer margins and strips of half-height four. Join matched terminals by their original vertical edge segments. First check: all 163 admitted atlas graphs must pass the existing exact route validator after suppressing bends; then check 11 initial prepared cores. Prove that the integer bar separation leaves at least 16 horizontal units to unrelated edges and 12 vertical units between strips. Relevant experience: round 032's certified local templates apply exactly to the degree bound and distinct same-side columns; no rectangularization is used.

## Evidence and diagnosis

The test failed before `layout.py` existed. `uv run --locked python .../rounds/033/test_layout.py` then passed all 174 composed drawings through the existing exact noncrossing/topology validator. There is no flow/rectangularization call in this route. The templates are read as fixed certificates; st-order, planar embedding and integer maps are reconstructed deterministically.

Proof of composition: distinct bar heights differ by at least one before scaling, so their closed half-height-four strips have a gap of at least 12. A nonincident vertical edge's integer column is outside a bar's integer interval, hence at least 20 away after scaling; the template extends only four units beyond either end. Incidence columns are distinct on each side. Piecewise monotone x stretching preserves each certified template's nonintersection. Outside the strips, edges retain their disjoint visibility segments. Thus the composed graph is an orthogonal embedding with exactly the intended incidences.

There are at most a constant number of template bends per vertex. Face and vertex ranks are O(V), so coordinates are O(V), route lengths sum to O(V²), and integer coordinate bit lengths are O(log V). Ear insertion and exact validation are polynomial. This supplies a concrete polynomial fallback, conditional only on the standard visibility theorem and the established biconnected-core premise, rather than on the old drawing library's totality. Independent review is still pending.

Experience extraction: updated [finite strip templates](../../../../research/experience/finite-port-template-stretching.md) with composition bounds. Next action: use this construction as the guaranteed fallback behind a deterministically bounded and validated compact-layout attempt, preserving the smaller target sizes where that attempt succeeds.
