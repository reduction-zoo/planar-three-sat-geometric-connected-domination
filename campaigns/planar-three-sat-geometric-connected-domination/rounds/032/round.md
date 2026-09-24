# Round 032 — finite orthogonal port templates

## Plan

Gap: bars represent vertices as intervals, but Clark's construction needs point vertices with distinct compass ports. Mechanism: because degree≤4, only finitely many left-to-right top/bottom incidence patterns exist. Synthesize disjoint integer-grid paths from one center to all terminals in a constant rectangle, retain templates as certificates, and use monotone horizontal stretching at runtime. First check: independently enumerate every pattern of two to four terminals, then validate template endpoint identity, axis-aligned unit steps, simple paths, pairwise intersection only at the center, and confinement to a strip. No candidate solver or source assignment is involved. Relevant experience: the old pendant-neighbor failure concerned final side points, not these topological routes; exact geometry remains essential.

## Evidence and diagnosis

The certificate validator was written first and failed for missing `templates.json`. Offline `synthesize.py` then used real vertex-capacitated max flow on a constant grid to find 46 templates. `test_templates.py` independently enumerates patterns through top/bottom Boolean choices and validates all paths. Every possible two-to-four-incidence pattern is covered, including coincident top/bottom columns and all incidences on one side. No solver is needed to use these retained templates at runtime.

Each template lies in x=0..2k, y=−4..4, with terminals at odd x and y=±4. Every path is simple, distinct paths meet only at their common center, and only its final point touches y=±4. Stretching x by any strictly increasing piecewise-linear map preserves these incidences and disjointness. At most four ports implies k≤4, so the certificate collection and path count are constant. This is a complete finite gadget interface; global bar composition still needs checking.

Experience extraction: created [finite strip-routing templates](../../../../research/experience/finite-port-template-stretching.md). Next action: compose the templates with integer bars and prove strip separation and polynomial coordinate bounds.
