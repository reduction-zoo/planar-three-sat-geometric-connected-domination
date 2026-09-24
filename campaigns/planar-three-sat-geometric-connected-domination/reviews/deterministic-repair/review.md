# Focused independent review — advance

Date: 2026-09-24. Candidate freeze: `72e1365084ce4e92f0ccb7c1f999f95efddad137`; implementation repair: `ad75146`. Decision: **advance**, meaning eligible for expert review, not publication acceptance.

The reported determinism defect is repaired. I found no new blocking consequence of the repair. This judgment reuses the unaffected construction, arbitrary-output recovery, literature and significance assessment in [the initial review](../visibility-candidate/review.md); it does not treat the proposer's passing-check summary as proof.

## Scope and actual isolation

Read the current repair diff, `rounds/010/drawing.py`, `rounds/030/visibility.py`, updated `work/drawing-proof.md`, the round-039 test launchers and logs, and relevant installed locked dependency code. The task remains the fixed question in `question.md`; reconstruction of published constructions is permitted.

This is the same registered `research-reviewer` continuing a focused review. The original spawn used `fork_turns="none"`, and this follow-up intentionally retains the initial findings. No explicit model override was used: inherited model route, runtime identified as GPT-6, exact serving suffix unavailable. Enforcement remains instructions only: unrestricted filesystem/tools, no demonstrated directory sandbox, tool denial or depth cap. I spawned no agents and wrote only in this newly assigned review directory. Candidate artifacts, original tests and earlier review evidence were not edited during this review. Isolation and model identity are not correctness evidence.

## Correctness: original defect closed

**Visibility branch.** `rounds/030/visibility.py:5–10` constructs a new graph by iterating parent nodes and edges. Both sets supplied at the call sites are now used only for membership. Thus neither outside-component traversal nor the copied ear graph inherits NetworkX's filtered-set iteration. `connected_components` starts in the new graph's insertion order; the boundary is sorted by the current st-order; shortest-path ties follow explicitly materialized adjacency. This directly removes the causal defect identified in the first review. Graph attributes are not copied, but these construction graphs carry no attributes needed by visibility. The induced vertex/edge sets and ear proof are preserved. Rebuilding a linear-size graph per ear remains polynomial.

The rest of the visibility pipeline uses ordered graph/dictionary traversals. I inspected NetworkX planarity's DFS adjacency lists and stable nesting-depth sorting; its relevant sets mark/check membership rather than choose a layout. Face numbering and topological ranks therefore start from stable data. The proof now names the actual ordering mechanism rather than assuming views preserve insertion order.

**Compact branch.** `rounds/010/drawing.py:62–66` numbers core vertices by insertion order before TSM and reverses that mapping afterward. This addresses the inspected `networkx/algorithms/planar_drawing.py:191,234,287–288` set-based choices. The chosen labels are small integers with hash values unaffected by `PYTHONHASHSEED`. The installed `networkx/relabel.py` copy branch preserves node/edge insertion order. The reverse mapping is injective on original vertices; generated bend labels are tuples and cannot collide with the numbered originals or the original `v/c/x/w` labels. The existing topology/geometry validator remains after relabeling.

I inspected the actual tsmpy planarization, DCEL, orthogonalization, compaction and flow paths. DCEL construction and subsequent traversal use insertion-ordered dictionaries and explicit face walks. The `uselp=False` path calls NetworkX min-cost flow; network simplex enumerates nodes/edges into indexed arrays before pivoting. Generated tuple/string bend and face labels enter ordered dictionaries, not the planar-drawing eligible-node set. No random initializer or external LP branch is used. The compact attempt's fixed line-event allowance still bounds the optional branch; the added relabel work is inside that allowance, and exhaustion goes to the real fallback. This assessment concerns the locked implementation; dependency changes require renewed checking.

**Recovery consequence.** With stable abstract graph construction and both drawing branches, the same source reconstructs the same routes and lexicographically sorted points. `work/algorithm.py:60–65` can therefore interpret a target index against the same coordinates. The relabel repair changes no decoder formula, cover bound or target validity condition. Side normalization still operates along fixed route order; unordered traversal used only for connectivity tests affects the Boolean predicate, not a geometric choice. The initial review's general side-normalization/counting argument applies unchanged.

The repair leaves the legal-input handling, sound unit-contradiction shortcut, empty-source case and NO-SOLUTION equivalence unchanged. It preserves O(V²) point output and polynomial encoding/runtime bounds. Finite checks below supplement these arguments; they do not prove universal correctness by themselves.

## Independent checks and reused evidence

I ran [check_repair.py](check_repair.py), which imports no candidate implementation. It executes public F on the exact original asymmetric 15-variable source under **new hash seeds 7 and 99**. A read-only profiling hook records the real accepted `checked_layout` return, then stops before enormous point expansion. It changes no graph, return value, dependency or operation allowance. Both runs produced:

- 1,292 core vertices and 7,396 drawn vertices;
- route length **17,180,282**;
- identical position digest `44770418cd0c3981fb684aaffe4399208c338cf4f07dd3f3f55a94328ebb97d3`.

See [check.txt](check.txt), [prefix-7.json](prefix-7.json) and [prefix-99.json](prefix-99.json). These independently confirm the original failure is gone, beyond the retained seeds 1/2 regression. This is explicitly a prefix check, not a solved full target.

I also ran [check_recovery.py](check_recovery.py) on a new two-variable source with clauses `(x1 ∨ x2 ∨ x2)` and `(¬x1 ∨ ¬x2 ∨ ¬x2)`. It runs actual public F under seeds 7/99, obtains a witness using the independent target-only oracle, checks exact rational-distance target validity, and runs public G under seeds 123/456. Source truth is independently enumerated. The identical targets have **12,418 points, K=6,515**; the independently validated 6,515-point witness decodes to `[false, true]` under both G seeds. See [recovery.json](recovery.json) and [recovery.txt](recovery.txt). The test imports the independent checker, not the candidate implementation.

Reused after inspecting the current scripts and raw records:

- `rounds/039/after.txt`: the original large-source prefix agrees under seeds 1/2.
- `rounds/039/reconstruction.json` and `check_reconstruction.py`: three default public-source checks plus an actual forced-fallback target of **330,596 points, K=165,357**, independently solved and validated, then decoded under two other process seeds.
- `rounds/039/forced_fallback.py`: sets the existing numeric allowance to zero, invokes actual F/G code, and observes actual visibility execution. This exercises real exhaustion and fallback without substituting an algorithm result. It is branch coverage, not evidence that the default allowance chooses fallback on that small source.
- `rounds/039/prepared.txt`: 112 sources, 195 witness outputs, 14 exact NO-SOLUTION outputs; `side-chains.txt`: 12 alternate outputs; `layouts.txt`: 174 checked layouts.

I did not repeat the full suites or the expensive forced-fallback solve. The large default source remains unexpanded because of the earlier memory cost. Forced-fallback recovery uses a source without clauses; default public clause-bearing recovery is covered separately. No nontrivial geometric negative target certificate is supplied. These are explicit evidence limits, not additional acceptance conditions invented for this follow-up.

Reproduction from the repository root:

```sh
.venv/bin/python -B campaigns/planar-three-sat-geometric-connected-domination/reviews/deterministic-repair/check_repair.py
.venv/bin/python -B campaigns/planar-three-sat-geometric-connected-domination/reviews/deterministic-repair/check_recovery.py
```

## Novelty and reconstruction fit

**Supported as a reconstruction, with no new-hardness claim.** The repair changes deterministic implementation details, so the initial review's primary-literature assessment is unaffected and reused. Clark–Colbourn–Johnson, [*Unit disk graphs*](https://cs.du.edu/~snarayan/sada/research/docs/res/unitdisk.pdf), §6/Theorem 6.1 and Lemmas 6.1–6.2, already supplies the relevant grid connected-domination theorem and replacement/counting proof. The candidate cites its other construction and visibility sources.

The initial review records the actual 2026-09-24 source checks, precise theorem locations, unavailable scan/text access and incomplete coverage of other executable reconstructions. Those limitations remain; no newly completed bibliographic audit or originality confirmation is claimed. They do not undermine the fixed task's permitted published-construction reconstruction. Stable executable F/G, explicit integer coordinates and recovery are the assessed deliverable.

## Significance and decision

**Meets the fixed reconstruction objective.** The repaired rule combines explicit graph gadgets, polynomial integer-coordinate routing, witness recovery and independent finite solver evidence. The extensive point expansion remains expensive: the large regression has over 17 million unscaled route units before scaling and adding side points. There is no demonstrated practical large-instance solver advantage, and no such claim or stronger resource ceiling is needed for this question.

The blocking finding from the initial review is closed by a causal implementation repair, a matching ordering argument and targeted checks of both reconstruction and recovery. **Advance** under the fixed acceptance criteria, with the stated scope and evidence limits retained for expert review.
