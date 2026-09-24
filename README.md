# Planar 3-SAT → Geometric connected domination

Independent research campaign. The campaign resumed with 20 additional rounds (021–040); a complete reduction remains unverified. An executable candidate exists, but its all-input drawing guarantee and independent nontrivial target verification remain open.

[State](campaigns/planar-three-sat-geometric-connected-domination/state.md) · [Question](campaigns/planar-three-sat-geometric-connected-domination/question.md)

The [prepared foundation](campaigns/planar-three-sat-geometric-connected-domination/work/preparation.md) has 112 planar 3-SAT cases and independent source/target oracles. The [candidate](campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py) and [working proof](campaigns/planar-three-sat-geometric-connected-domination/work/proof.md) compose planar-cover and grid-domination constructions. The [verification record](campaigns/planar-three-sat-geometric-connected-domination/work/verification.md) separates solved targets from validated constructed witnesses and lists the remaining checks.

Reproduce with `uv sync --locked`, `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --self-test`, and `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/verify.py --candidate campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py`. Round-specific commands are in their records. No remote, publication, or board update was made.

Board source commit: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.
