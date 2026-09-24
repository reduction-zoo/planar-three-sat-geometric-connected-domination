# Planar 3-SAT → Geometric connected domination

Independent research campaign. Active after 18 of 20 authorized rounds. An executable candidate exists, but its all-input drawing guarantee and independent large-target verification remain open; no complete result is claimed.

[State](campaigns/planar-three-sat-geometric-connected-domination/state.md) · [Question](campaigns/planar-three-sat-geometric-connected-domination/question.md)

The [prepared foundation](campaigns/planar-three-sat-geometric-connected-domination/work/preparation.md) has 112 planar 3-SAT cases and independent source/target oracles. The [candidate](campaigns/planar-three-sat-geometric-connected-domination/work/algorithm.py) and [working proof](campaigns/planar-three-sat-geometric-connected-domination/work/proof.md) compose planar-cover and grid-domination constructions; [round 013](campaigns/planar-three-sat-geometric-connected-domination/rounds/013/round.md) records the current checks and gaps.

Reproduce the prepared check with `uv sync --locked` and `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/check.py --self-test`. Run the finite F/G interface check with `uv run --locked python campaigns/planar-three-sat-geometric-connected-domination/work/test_interface.py`. Round-specific commands are in their records. No remote, publication, or board update was made.

Board source commit: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.
