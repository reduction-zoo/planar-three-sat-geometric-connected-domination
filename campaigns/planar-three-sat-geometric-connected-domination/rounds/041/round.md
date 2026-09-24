# Record 041 — geometric negative verification family

## Plan

Gap: all 14 prepared negative targets are one-point unit-contradiction shortcuts; no nontrivial geometric target has an independently certified NO answer. Expanded search family: two small, hand-derived unsatisfiable planar formulas with no unit clauses after duplicate removal. The first has all four binary sign combinations on two variables, each padded to three literal positions by repeating one literal; its incidence graph is planar K2,4. The second uses two two-clause pairs on three variables, forcing a variable both true and false; its incidence graph is two four-cycles meeting at one variable. Their truth tables prove UNSAT without relying on the candidate.

Relevant experience: [oracle scale](../../../../research/experience/connected-domination-oracle-scale.md) says an unfinished target solver run is unknown, not NO; [separator DP](../../../../research/experience/separator-connected-domination-oracle.md) is an independent exact target route on narrow instances. First check: validate both explicit planar embeddings and exhaustive source UNSAT, confirm no initial unit propagation, then execute public F and require more than one target point. Next, attempt an independent exact target NO certificate with target-only graph methods and check G on any certified NO output. Retain an execution failure as such; do not add an unverified target label to the passing prepared suite. This record charges one of the previously unspent research slots because it expands the negative search family.

## Evidence and diagnosis

Pending.

## Next action

Run the first discriminating check.
