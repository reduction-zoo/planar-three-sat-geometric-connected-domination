# Planar 3-SAT → Geometric connected domination

Executable candidate F/G and a candidate general proof, with an explicit polynomial visibility drawing fallback. The full prepared verification passed **112 instances and 209 target outputs**; a hash-order defect found by independent review has been repaired and all affected checks pass; focused re-review is pending. No accepted complete rule or manuscript is claimed yet.

[State](campaigns/planar-three-sat-geometric-connected-domination/state.md) · [Question](campaigns/planar-three-sat-geometric-connected-domination/question.md) · [Algorithm](campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py) · [Proof](campaigns/planar-three-sat-geometric-connected-domination/work/proof.md) · [Drawing proof](campaigns/planar-three-sat-geometric-connected-domination/work/drawing-proof.md) · [Verification](campaigns/planar-three-sat-geometric-connected-domination/work/verification.md)

Verification includes 97 geometric positive targets with two independently found witnesses each, one trivial positive, 14 exactly solved trivial negatives, and 12 additional side-chain decoder checks. The largest prepared target has 202,170 points; an additional forced-fallback target with 330,596 points passed independent solve and cross-process recovery. The negative cases use unit contradictions; nontrivial geometric NO instances remain unverified.

Reproduce with `uv sync --locked`, then run `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --self-test` and `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py`. The standalone small-target verifier is `work/verify.py --candidate work/algorithm.py` under the same campaign path. Round records preserve failed approaches and additional checks.

The user allocated 20 additional rounds after the original 20; progress continues in rounds 021–040. No remote, publication or board update was made. Board source commit: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.
