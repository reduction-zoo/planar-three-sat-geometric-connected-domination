# Campaign state

Status: resumed on 2026-09-24 with 20 additional authorized rounds (021–040). Total authorized budget: 40 rounds; completed: 39. Distinct construction route families attempted: 4 (Lichtenstein row/ground/clause; local ground/literal cell with equality wire; later Grid Tiling unit-disk construction; planar-cover to grid connected domination).
Board source: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.

Capability probe (2026-09-23, local macOS): Python 3.12.14 at `/Users/xiweipan/.local/bin/python3` available; uv 0.12.17 at `/Users/xiweipan/.local/bin/uv` available; Z3 executable 5.1.0 at `/opt/homebrew/bin/z3` available; Kissat 4.0.4 at `/opt/homebrew/bin/kissat` available; cvc5, Minisat and CP-SAT executables absent; Typst 0.15.1 at `/opt/homebrew/bin/typst` available; Lean 4.34.0 and Lake 5.0.0 at `/opt/homebrew/bin/lean` and `/opt/homebrew/bin/lake` available; Mathlib is not on the current Lean search path (`import Mathlib` failed on 2026-09-24); no formalization requested; external writing skill `sci-brain:how-to-technical-writing` present at `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md`. Prepare locked Python bindings Z3 5.1.0.0 and NetworkX 3.7 in `uv.lock`.

Prepare: [contract](work/contract.md), [112 fixed cases](work/cases.json), [oracles](work/check.py), [evidence](work/preparation.md). Self-test passed on 2026-09-23. The later candidate is linked below.

Current claim: executable F/G and a candidate general proof now include an explicit polynomial visibility drawing fallback. The full prepared loop passed 112 sources and 209 target outputs (195 witnesses, 14 exact NO-SOLUTION outputs). Independent review returned revise for hash-dependent drawing order; round 039 repaired that defect and passed the complete prepared, alternate-output and cross-seed checks; focused re-review is pending. No accepted complete rule or manuscript is claimed yet.

Checks and limits: preparation passed with 112 independently exhaustive-checked source labels. Current F targets include 97 nontrivial geometric positives with two target-only independently found and full-graph validated witnesses each, plus one trivial positive and 14 exactly solved trivial negatives. Twelve separately constructed side-chain outputs passed full target validation and fresh G recovery. Maximum actual target size: 202,170 points. The explicit fallback has 46 complete finite port certificates, 174 complete layout checks, and four forced-operation-exhaustion checks; the compact branch passed all 111 prepared cores. General correctness remains a proof/review obligation, and no nontrivial geometric NO instance has been independently certified. Full details and retained failures are in [verification](work/verification.md).


Prior stopping diagnosis in [round 007](rounds/007/round.md) was premature: its target-checker scale limit does not block further research. [Round 008](rounds/008/round.md) found a smaller published grid-graph route.

Experience to date: 9 distinct local entries (3 created in the additional allocation); two pre-existing entries updated in this allocation, with further use-history updates within the three new entries; 0 pending extraction. No entry was promoted to the board. New entries: [backend contract](../../research/experience/orthogonal-drawing-backend-contract.md), [separator oracle](../../research/experience/separator-connected-domination-oracle.md), [finite templates](../../research/experience/finite-port-template-stretching.md).

Next action: round-040 focused independent re-review of the repaired candidate. One research round remains. Prospects within that budget are unknown (uncalibrated): executable verification now passes, and the reviewer found a concrete dependency-ordering defect that must be closed. No publication or board update is authorized.


| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | Audit cited Lichtenstein variable/ground/clause construction | Does Theorem 5 use exact unit-distance graph and give rational coordinates? | inconclusive: model matches, coordinates omitted | [round](rounds/001/round.md) |
| 002 | Integer-coordinate ground/literal/clause gadget | Exhaustive two-point CDS check on one-variable cases | supported locally; direct spaced composition refuted | [round](rounds/002/round.md) |
| 003 | Equality wire from repeated choice cells, distinct from direct clause composition | Bounded symmetry/translation and half-grid search for two isolated equality sites | refuted for stated finite family | [round](rounds/003/round.md) |
| 004 | Later Grid Tiling to unit-disk connected-domination construction | Does a primary proof supply explicit coordinates and fit the fixed source contract? | inconclusive: detailed target lead, source bridge and rationalization missing | [round](rounds/004/round.md) |
| 005 | Clause-choice compatibility bridge to Grid Tiling, new submechanism of later route | Independent tiled solve and assignment extraction on 112 cases | supported as combinatorial lemma | [round](rounds/005/round.md) |
| 006 | Published offset order interface for neighboring blocks | Exact suffix/prefix adjacency check for n=2..5 | supported locally; full gadget untested | [round](rounds/006/round.md) |
| 007 | Full Grid Tiling route scale and coordinate-specification audit | Y-block point lower bound for prepared nontrivial NO cases | inconclusive construction; supported stopping decision | [round](rounds/007/round.md) |
| 008 | Published planar connected-cover to grid-CDS route, distinct from Grid Tiling | Does a primary proof supply exact integer target coordinates and source recovery? | supported as a route; bridge/drawing/implementation pending | [round](rounds/008/round.md) |
| 009 | Lichtenstein planar cover composed with Garey–Johnson connected cover | Explicit degree/planarity/witness/recovery checks including repeats and disconnected inputs | supported bridge on 112 cases; full target pending | [round](rounds/009/round.md) |
| 010 | Polynomial orthogonal drawing theorem with executable TSM implementation | Biconnected core and exact noncrossing route validation on prepared graphs | supported on 111 nonempty cases; general guarantee pending | [round](rounds/010/round.md) |
| 011 | Scaled grid paths plus Clark side-chain points; independent-pendant variant tested separately | Exact adjacency/degree and forward witness on prepared graphs | side chains supported on 111; independent pendant variant refuted on case 1 | [round](rounds/011/round.md) |
| 012 | Clark side-chain normalization and arbitrary-output decoder | Canonical output plus exact-budget side-chain alternatives on actual point sets | supported on 97 canonical and one alternate output; general proof pending | [round](rounds/012/round.md) |
| 013 | Integrated F/G chain and exact sparse target-oracle repair | Fresh-process witness extraction and full prepared harness | interface supported; full target solving execution failure | [round](rounds/013/round.md) |
| 014 | Independent CP-SAT flow target oracle and target-only greedy witness search | Five small target labels, then 1,596-point generated target | small checks supported; generated-target search execution failure | [round](rounds/014/round.md) |
| 015 | Polynomial unit-contradiction shortcut, separate from general geometry | Independent source labels and actual negative F-target solve/extract | supported on all 14 prepared NO cases; large geometry pending | [round](rounds/015/round.md) |
| 016 | Structured legal-source drawing stress and recursion repair | Biconnected cores and exact orthogonal routes for 24 cases | execution defect repaired; general guarantee pending | [round](rounds/016/round.md) |
| 017 | Independent GIOTTO backend API and exact route audit, distinct drawing implementation | Bend-optimal routes on 111 prepared and 24 stress cores | finite drawings supported; all-input certification pending | [round](rounds/017/round.md) |
| 018 | Noncanonical side-chain target outputs across varied source sizes | Independent target witness validity and fresh-process recovery on 12 cases | supported finite decoder coverage; general proof pending | [round](rounds/018/round.md) |
| 019 | Core biconnectivity lemma via local face-cycle argument and small atlas | 38 connected and six disconnected planar subcubic graphs | supported structural premise; drawing library guarantee pending | [round](rounds/019/round.md) |
| 020 | Final reduction-contract and verification audit | Standalone exact F-target solve/recovery and all-input obligation ledger | 15 small targets supported; budget exhausted with two material gaps | [round](rounds/020/round.md) |

| 021 | Drawing flow arithmetic and runtime audit | Exact two-face flow beyond fixed capacity | supported backend limitation; generated-source failure unproved | [round](rounds/021/round.md) |
| 022 | Target-only pruning with plateau moves | Path optimum checks, then four bounded searches | inconclusive: no geometric witness within K | [round](rounds/022/round.md) |
| 023 | Generic target tree decomposition | Running intersection and width of actual target 1 | supported: width 8, mostly bags of size 4 | [round](rounds/023/round.md) |
| 024 | Exact connectivity-partition separator DP | 31 exhaustive small optima, then actual F target | supported: independent 1,596-point optimum 857 decoded | [round](rounds/024/round.md) |
| 025 | Mandatory articulation pruning of separator states | 143 exhaustive atlas optima and clause-bearing target | small checks supported; 6,369-point execution failure | [round](rounds/025/round.md) |
| 026 | Exact integral drawing-flow replacement | 80 exhaustive lower-bound flow optima | supported component; drawing integration pending | [round](rounds/026/round.md) |
| 027 | Input-dependent exact shape and compaction flows | DAG/path premises and 14 exact layout checks | supported finite integration; totality pending | [round](rounds/027/round.md) |
| 028 | Rational external-face ordering | Near-parallel integer rays beyond float precision | old component refuted; exact replacement supported | [round](rounds/028/round.md) |
| 029 | General rectangularization premise and corner potential | All 163 biconnected planar degree-four atlas graphs | finite support; exterior weak-face proof gap remains | [round](rounds/029/round.md) |
| 030 | Visibility drawing via ear-insertion st-order | Order, bimodality and dual DAG on 163 atlas graphs | supported combinatorial interface | [round](rounds/030/round.md) |
| 031 | Integer bar visibility with exterior st column | All forbidden segment/bar intersections on 174 graphs | supported exact visibility interface | [round](rounds/031/round.md) |
| 032 | Exhaustive finite strip-routing certificates | All 46 degree-2..4 incidence patterns | supported complete local interface | [round](rounds/032/round.md) |
| 033 | Global composition of stretched visibility templates | Exact embedding checks on 174 complete drawings | supported polynomial fallback argument; review pending | [round](rounds/033/round.md) |
| 034 | Bounded compact attempt and explicit visibility fallback | Four forced-exhaustion and 111 prepared layouts | supported candidate totality argument; review pending | [round](rounds/034/round.md) |
| 035 | Coordinate restrictions and forced-component ranks | Small witness/unknown checks, clause-bearing target | small checks supported; two execution failures | [round](rounds/035/round.md) |
| 036 | Target-only backbone recognition and witness lifting | Actual 6,369-point target with two distinct outputs | supported: both full-graph witnesses decoded | [round](rounds/036/round.md) |
| 037 | Full prepared verification with independent cover folding | 209 tiny cover budgets, then all 112 F/solve/G cases | supported: 195 witnesses, 14 exact NO outputs, 12 side-chain checks | [round](rounds/037/round.md) |

| 038 | Independent complete-rule assessment | Fresh reviewer audit and cross-seed public F | refuted deterministic F on a legal 15-variable fallback source; revise | [round](rounds/038/round.md) |
| 039 | Stable traversal and compact integer relabeling | Retained failing public-F prefix, then cross-seed F/solve/G | supported: repaired prefix, 330,596-point fallback recovery, 112 prepared and 12 side-chain cases | [round](rounds/039/round.md) |
