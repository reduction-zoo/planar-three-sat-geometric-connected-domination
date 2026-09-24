# Round 037 — complete prepared F/solver/G verification

## Plan

Gap: the changed maps have not passed all prepared source-to-target-to-source loops. Mechanism: add the positive-only independent backbone finder before the unchanged exact CDS oracle; use complete exact solving whenever no witness is found, and never infer NO from the heuristic. First check: unchanged preparation self-tests, then all 112 prepared cases and alternate target outputs through fresh F/G processes. The prepared checker independently builds rational-distance adjacency, distinct from the integer recognition code. Relevant experience: round 036's witness certificates support positive evidence only; negative actual targets must be exactly solved. Additional scope: update standalone verification coverage and confirm retained arbitrary side-chain outputs still decode.

### Prepared-suite bottleneck

The unchanged self-test passed. The prepared loop completed cases 0–11, then case 12 exposed a much larger target: 106,491 points and a recognized 1,063-vertex skeleton with cover budget 535. The run was interrupted to improve the target-only search representation; no complete-suite pass or case-12 target answer is claimed from this run. The retained prefix is `prepared.txt`. A diagnostic stopped before solving and measured the actual target/skeleton sizes; it did not infer a label. Next: apply independently tested ordinary vertex-cover folding after mandatory articulation selections, then validate the resulting connected cover and full lifted target witness. This is oracle work; candidate maps remain unchanged.

## Evidence and diagnosis

The new ordinary vertex-cover kernel's test first failed for the absent module. Its degree-zero/one/two folding then matched all 209 independently enumerated graph-atlas optimum and below-optimum budgets through six vertices. Applied after mandatory articulation selections, it supplied a proposed small cover; the finder still checked connectedness and the complete lifted target witness. An invalid/incomplete proposal can never create a false target NO answer.

Commands: `uv run --locked python .../rounds/037/test_cover.py`; `uv run --locked python .../work/check.py --self-test`; `uv run --locked python .../work/check.py --candidate .../work/algorithm.py`; and `uv run --locked python .../rounds/018/alternate_witnesses.py`. Full prepared result: **112 instances, 195 witness outputs and 14 exact NO-SOLUTION outputs passed**. All 97 geometric positives supplied two distinct outputs; largest actual target 202,170 points. The side-chain rerun passed all 12 outputs. Raw logs and the clause-bearing regression witnesses are retained here. The first interrupted prefix remains historical failure evidence, not part of the successful run.

A supporting primary-source check read Tamassia–Tollis (1986), Algorithm W-VISIBILITY p. 328 and Theorem 1 p. 330, including its st-dual lemmas. The drawing proof now explains the exact affine correspondence between that algorithm's strict face-potential columns and the implemented integer columns. This clarifies the existing algorithm; no map was changed during the successful prepared run.

Experience extraction: updated the existing [oracle-scale](../../../../research/experience/connected-domination-oracle-scale.md) and [drawing-recursion](../../../../research/experience/tsmpy-face-recursion.md) entries; no new entry needed. Next action: freeze this candidate and request the required fresh-context registered review. The absence of a nontrivial geometric NO certificate remains explicit; the tested negative F instances are the actual one-point shortcut targets.
