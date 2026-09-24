# Round 028 — exact external-face orientation

## Plan

Gap: the experimental drawing still delegates external-face selection to floating-point sine comparisons. Mechanism: at the lexicographically leftmost point, all rays have nonnegative x direction; compare their exact rational slopes (vertical upward last). First check: two distinct near-parallel integer rays beyond floating precision must choose the lower ray, independent of insertion order. Compare the old behavior before replacement, then run the same 14 whole-layout validations. Relevant experience: arithmetic bounds belong to the executable contract, even if practical graphs stay small. This is a dependency-component test, not an asserted generated-source failure.

## Evidence and diagnosis

The retained regression first failed on `(n=10**18, insertion order=(1,2))`: tsmpy's floating sine values tied and selected the wrong face. After exact rational slope comparison in `ExactPlanarization`, all four ray/order checks passed. `uv run --locked python .../rounds/027/test_drawing.py` then passed all 14 real layouts again; output retained here. This is a confirmed dependency-component arithmetic defect, not a found legal source failure of current F.

At the lexicographically leftmost point, dx≥0 and a vertical neighbor has dy>0. For dx>0, sine(angle) is strictly increasing in dy/dx over the possible half-plane, so rational slope order is the required order. No trigonometry or precision assumption is needed. The change affects only the experimental backend.

Experience extraction: updated [backend contract](../../../../research/experience/orthogonal-drawing-backend-contract.md). Next action: audit whether biconnected degree-four input actually suffices for the inherited rectangularization, including its exterior-frame operation.
