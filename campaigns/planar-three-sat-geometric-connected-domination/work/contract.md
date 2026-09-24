# Executable contract

Source JSON has `variables: n`, `clauses: [[l1,l2,l3], ...]`, and `embedding`, a clockwise neighbor list for every incidence-graph vertex `v0..v(n-1)` and `c0..c(m-1)`. Each nonzero signed literal has absolute value at most `n`; repeated literals count as distinct clause occurrences but produce one incidence edge. The rotation must be a planar embedding. Empty formulas and isolated variables are legal. A source output is a Boolean array of length `n` satisfying every clause, or `"NO-SOLUTION"` exactly when none exists.

Target JSON has `points: [[x,y], ...]`, nonempty and pairwise distinct, with each coordinate a rational string or integer, and integer `K >= 0`. The unit-disk graph has an edge exactly when squared Euclidean distance is at most one. A target output is a list of distinct zero-based point indices of length at most `K` that dominates the graph and induces a connected graph, or `"NO-SOLUTION"` exactly when no such list exists. The empty list is not connected for a nonempty graph.

`algorithm.py` reads one source JSON on stdin and prints one target JSON on stdout. `algorithm.py --extract` reads `{ "source": ..., "target_solution": ... }` and prints one source output. Both modes are deterministic, independent processes; errors exit nonzero and write diagnostics to stderr.

The source and target validity checks and oracles are in `check.py`. This encoding narrows only representation, not the fixed mathematical problem. Candidate correctness must cover legal inputs beyond the prepared corpus.
