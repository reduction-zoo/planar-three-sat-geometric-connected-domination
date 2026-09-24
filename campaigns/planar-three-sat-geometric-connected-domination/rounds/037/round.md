# Round 037 — complete prepared F/solver/G verification

## Plan

Gap: the changed maps have not passed all prepared source-to-target-to-source loops. Mechanism: add the positive-only independent backbone finder before the unchanged exact CDS oracle; use complete exact solving whenever no witness is found, and never infer NO from the heuristic. First check: unchanged preparation self-tests, then all 112 prepared cases and alternate target outputs through fresh F/G processes. The prepared checker independently builds rational-distance adjacency, distinct from the integer recognition code. Relevant experience: round 036's witness certificates support positive evidence only; negative actual targets must be exactly solved. Additional scope: update standalone verification coverage and confirm retained arbitrary side-chain outputs still decode.

### Prepared-suite bottleneck

The unchanged self-test passed. The prepared loop completed cases 0–11, then case 12 exposed a much larger target: 106,491 points and a recognized 1,063-vertex skeleton with cover budget 535. The run was interrupted to improve the target-only search representation; no complete-suite pass or case-12 target answer is claimed from this run. The retained prefix is `prepared.txt`. A diagnostic stopped before solving and measured the actual target/skeleton sizes; it did not infer a label. Next: apply independently tested ordinary vertex-cover folding after mandatory articulation selections, then validate the resulting connected cover and full lifted target witness. This is oracle work; candidate maps remain unchanged.
