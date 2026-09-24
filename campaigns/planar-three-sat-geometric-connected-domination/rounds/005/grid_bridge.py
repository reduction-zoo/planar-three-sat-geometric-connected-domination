"""Clause-choice compatibility to Grid Tiling, with an independent tiled solver."""

import json
import sys
from pathlib import Path

import z3

WORK = Path(__file__).resolve().parents[2] / "work"
sys.path.insert(0, str(WORK))
from check import source_witness_valid  # noqa: E402


def tiling_sets(source):
    clauses = source["clauses"]
    m = len(clauses)
    sets = []
    for a in range(m):
        row = []
        for b in range(m):
            options = []
            for rb, lit_b in enumerate(clauses[b]):
                for ra, lit_a in enumerate(clauses[a]):
                    if a == b:
                        if ra == rb:
                            label = 3 * a + ra + 1
                            options.append((label, label))
                    elif lit_a != -lit_b:
                        options.append((3 * b + rb + 1, 3 * a + ra + 1))
            row.append(options)
        sets.append(row)
    return sets


def solve_tiling(sets):
    m = len(sets)
    if m == 0:
        return []
    if any(not options for row in sets for options in row):
        return None
    solver = z3.Solver()
    x = [[z3.Int(f"x_{a}_{b}") for b in range(m)] for a in range(m)]
    y = [[z3.Int(f"y_{a}_{b}") for b in range(m)] for a in range(m)]
    for a in range(m):
        for b in range(m):
            solver.add(z3.Or(*(z3.And(x[a][b] == u, y[a][b] == v) for u, v in sets[a][b])))
            if a:
                solver.add(x[a][b] == x[a - 1][b])
            if b:
                solver.add(y[a][b] == y[a][b - 1])
    status = solver.check()
    if status == z3.unsat:
        return None
    if status != z3.sat:
        raise RuntimeError(f"tiling solver inconclusive: {status}")
    model = solver.model()
    return [[(model.eval(x[a][b]).as_long(), model.eval(y[a][b]).as_long()) for b in range(m)] for a in range(m)]


def decode(source, tiling):
    if tiling is None:
        return "NO-SOLUTION"
    assignment = [False] * source["variables"]
    for a in range(len(source["clauses"])):
        label = tiling[a][a][0]
        literal = source["clauses"][a][(label - 1) % 3]
        assignment[abs(literal) - 1] = literal > 0
    return assignment


def main():
    cases = json.loads((WORK / "cases.json").read_text())
    yes = no = empty_pair = 0
    for index, case in enumerate(cases):
        source = case["source"]
        sets = tiling_sets(source)
        empty_pair += any(not options for row in sets for options in row)
        tiling = solve_tiling(sets)
        recovered = decode(source, tiling)
        assert source_witness_valid(source, recovered), (index, recovered)
        assert (tiling is None) == (case["expected"] == "NO-SOLUTION"), index
        if tiling is None:
            no += 1
        else:
            yes += 1
    print(f"Grid Tiling bridge: {len(cases)} instances, {yes} satisfiable, {no} unsatisfiable, {empty_pair} with an empty cell")


if __name__ == "__main__":
    main()
