"""Reproduce the fixed, small planar 3-CNF corpus."""

import json
import random
from pathlib import Path

import networkx as nx
import z3


def make_source(n, clauses):
    graph = nx.Graph()
    graph.add_nodes_from(f"v{i}" for i in range(n))
    graph.add_nodes_from(f"c{i}" for i in range(len(clauses)))
    for j, clause in enumerate(clauses):
        for literal in clause:
            graph.add_edge(f"c{j}", f"v{abs(literal) - 1}")
    planar, embedding = nx.check_planarity(graph)
    if not planar:
        return None
    return {"variables": n, "clauses": clauses, "embedding": embedding.get_data()}


def source_answer(source):
    variables = [z3.Bool(f"x{i}") for i in range(source["variables"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(lit) - 1] if lit > 0 else z3.Not(variables[-lit - 1]) for lit in clause)))
    status = solver.check()
    if status == z3.unsat:
        return "NO-SOLUTION"
    if status != z3.sat:
        raise RuntimeError(f"source oracle inconclusive: {status}")
    model = solver.model()
    return [z3.is_true(model.eval(v, model_completion=True)) for v in variables]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 6)
    clauses = []
    for _ in range(rng.randint(1, 10)):
        left = rng.randrange(n)
        allowed = [left + 1]
        if left + 1 < n:
            allowed.append(left + 2)
        clauses.append([rng.choice(allowed) * rng.choice((-1, 1)) for _ in range(3)])
    return make_source(n, clauses)


def corpus():
    edge_specs = [
        (0, []), (1, []), (1, [[1, 1, 1]]), (1, [[-1, -1, -1]]),
        (1, [[1, 1, 1], [-1, -1, -1]]),
        (2, [[1, 1, 1], [-2, -2, -2]]),
        (2, [[1, 1, 1], [-1, -1, -1], [2, 2, 2]]),
        (2, [[1, -1, 2]]), (2, [[1, 2, 2], [-1, -2, -2]]),
        (3, [[1, 2, 3]]), (3, [[-1, -2, -3]]),
        (3, [[1, 1, 2], [-1, -1, 2], [-2, -2, -2]]),
    ]
    cases = []
    seen = set()

    def add(source, kind, seed=None):
        if source is None:
            return False
        key = json.dumps(source, sort_keys=True)
        if key in seen:
            return False
        seen.add(key)
        case = {"source": source, "kind": kind, "expected": source_answer(source)}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for n, clauses in edge_specs:
        assert add(make_source(n, clauses), "edge")
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed), "random", seed)
        seed += 1
    return cases


if __name__ == "__main__":
    Path(__file__).with_name("cases.json").write_text(json.dumps(corpus(), indent=2) + "\n")
