# Round 013 — integrated forward and recovery programs

## Plan

Gap: the bridge, drawing, point placement and normalization are separate experiments. Mechanism: compose them into the required deterministic stdin/stdout F/G interface, lock the drawing dependencies, and write a general proof including source edge cases and polynomial size. The earlier experience on turn-side adjacency is incorporated through the side-chain decoder. First check: run fresh forward and extract processes on prepared positive witnesses, compare reconstructed point indexing across processes, and test the legal trivial case. Then invoke the prepared candidate harness as required and record its actual outcome; its dense target solver may have a scaling defect, which must be diagnosed separately rather than treated as a mathematical answer.

## Evidence and diagnosis

[`work/algorithm.py`](../../work/algorithm.py) now composes the bridge, checked drawing, side-chain point placement and normalization in fresh forward and recovery processes. The empty source emits a one-point yes instance; all other cases use the geometric chain. `tsmpy==0.9.3` and its required Matplotlib import were added to the uv lock. [`work/proof.md`](../../work/proof.md) states the construction and both witness directions, while explicitly retaining the unproved all-input drawing implementation guarantee.

`uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/test_interface.py` passed: the empty target, a 1,596-point nonempty target, and a distinct exact-budget side-chain target witness were independently checked for target feasibility; each was sent through the subprocess `--extract` path and produced a valid source output. Repeated forward subprocesses on cases 0, 1, 2 and 4 produced identical bytes, including under Python hash seeds 0–3 for case 1. The 112-case Prepare self-test still passes.

The required full candidate command was attempted: `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py`. Its original time-indexed target connectivity encoding reached about 7.7 GB RSS after roughly 34 seconds and was interrupted while building the formula. The exact independent oracle was then changed to spatial buckets for target adjacency and iterative connectivity cuts; its unchanged self-test passed. The full command was run again. Memory stayed near 280 MB, but Z3 remained in `solver.check()` on an early target after roughly five minutes; interruption returned `unknown`, which the oracle correctly rejected. Both runs are **execution failures**, not target NO answers or counterexamples. The one-point F-produced target was separately solved exactly as `[0]`, with no second witness.

First discriminating check: **integrated F/G subprocess behavior supported on the stated witnesses; full prepared suite execution failed at independent target solving**. General drawing totality, polynomial output guarantee for this library and negative target verification remain open.

Experience extraction: [one new oracle-scale entry](../../../../research/experience/connected-domination-oracle-scale.md).

## Next action

Try a materially different independent target-solving method and audit the drawing implementation's totality and output bound. Do not infer negative answers from the interrupted runs.
