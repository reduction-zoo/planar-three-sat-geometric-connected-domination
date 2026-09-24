"""Independent finite oracles for planar 3-SAT and geometric connected domination."""

import argparse
import itertools
import json
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import networkx as nx
import z3

from generate_cases import random_source, source_answer

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[2]


def valid_source(source):
    n, clauses, rotation = source["variables"], source["clauses"], source["embedding"]
    if type(n) is not int or n < 0 or not isinstance(clauses, list):
        return False
    if any(not isinstance(c, list) or len(c) != 3 or any(type(x) is not int or x == 0 or abs(x) > n for x in c) for c in clauses):
        return False
    graph = nx.Graph()
    graph.add_nodes_from(f"v{i}" for i in range(n))
    graph.add_nodes_from(f"c{j}" for j in range(len(clauses)))
    for j, clause in enumerate(clauses):
        graph.add_edges_from((f"c{j}", f"v{abs(lit) - 1}") for lit in clause)
    if not isinstance(rotation, dict) or set(rotation) != set(graph):
        return False
    if any(not isinstance(rotation[v], list) or len(rotation[v]) != len(set(rotation[v])) or set(rotation[v]) != set(graph[v]) for v in graph):
        return False
    try:
        embedding = nx.PlanarEmbedding()
        embedding.set_data(rotation)
        embedding.check_structure()
    except (nx.NetworkXException, KeyError, TypeError, ValueError):
        return False
    return True


def source_witness_valid(source, answer):
    if answer == "NO-SOLUTION":
        return source_answer(source) == "NO-SOLUTION"
    n = source["variables"]
    return (isinstance(answer, list) and len(answer) == n and
            all(type(x) is bool for x in answer) and
            all(any(answer[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in source["clauses"]))


def brute_source(source):
    n = source["variables"]
    for assignment in itertools.product((False, True), repeat=n):
        if all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in source["clauses"]):
            return list(assignment)
    return "NO-SOLUTION"


def target_graph(target):
    points, k = target["points"], target["K"]
    if not isinstance(points, list) or not points or type(k) is not int or k < 0:
        raise ValueError("illegal target size or K")
    xy = []
    for point in points:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("point needs two rational coordinates")
        coords = [Fraction(x) for x in point]
        if any(type(x) not in (int, str) for x in point):
            raise ValueError("coordinates must be rational strings or integers")
        xy.append(coords)
    if len(set(map(tuple, xy))) != len(xy):
        raise ValueError("points must be distinct")
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for i, j in itertools.combinations(range(len(points)), 2):
        if sum((xy[i][d] - xy[j][d]) ** 2 for d in range(2)) <= 1:
            graph.add_edge(i, j)
    return graph, k


def target_answer(target, forbidden=()):
    graph, k = target_graph(target)
    n = len(graph)
    chosen = [z3.Bool(f"p{i}") for i in range(n)]
    root = z3.Int("root")
    solver = z3.Solver()
    solver.add(root >= 0, root < n, z3.PbLe([(v, 1) for v in chosen], k))
    for i in graph:
        solver.add(z3.Or(*(chosen[j] for j in (i, *graph.neighbors(i)))))
        solver.add(z3.Implies(root == i, chosen[i]))
    reach = [[z3.Bool(f"reach_{step}_{i}") for i in graph] for step in range(n)]
    for i in graph:
        solver.add(reach[0][i] == z3.And(root == i, chosen[i]))
    for step in range(1, n):
        for i in graph:
            solver.add(reach[step][i] == z3.Or(reach[step - 1][i], z3.And(chosen[i], z3.Or(*(reach[step - 1][j] for j in graph.neighbors(i))))))
    for i in graph:
        solver.add(z3.Implies(chosen[i], reach[-1][i]))
    for answer in forbidden:
        solver.add(z3.Or(*(chosen[i] != (i in answer) for i in graph)))
    status = solver.check()
    if status == z3.unsat:
        return "NO-SOLUTION"
    if status != z3.sat:
        raise RuntimeError(f"target oracle inconclusive: {status}")
    model = solver.model()
    return [i for i in graph if z3.is_true(model.eval(chosen[i]))]


def target_witness_valid(target, answer):
    graph, k = target_graph(target)
    if answer == "NO-SOLUTION":
        return target_answer(target) == "NO-SOLUTION"
    if not isinstance(answer, list) or len(answer) > k or len(answer) != len(set(map(str, answer))):
        return False
    if any(type(i) is not int or i not in graph for i in answer):
        return False
    selected = set(answer)
    return bool(selected) and nx.is_connected(graph.subgraph(selected)) and all(i in selected or any(j in selected for j in graph.neighbors(i)) for i in graph)


def run_candidate(path, args, payload):
    result = subprocess.run([sys.executable, str(path), *args], input=json.dumps(payload), text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"candidate {args} failed: {result.stderr}")
    return json.loads(result.stdout)


def self_test():
    subprocess.run([sys.executable, str(ROOT / "research/validate_preparation.py"), str(WORK / "cases.json")], check=True)
    cases = json.loads((WORK / "cases.json").read_text())
    counts = Counter()
    for case in cases:
        source, expected = case["source"], case["expected"]
        assert valid_source(source)
        if case["kind"] == "random":
            assert source == random_source(case["seed"])
        assert (expected == "NO-SOLUTION") == (source_answer(source) == "NO-SOLUTION")
        assert (expected == "NO-SOLUTION") == (brute_source(source) == "NO-SOLUTION")
        assert source_witness_valid(source, expected)
        counts[(case["kind"], source["variables"], expected == "NO-SOLUTION")] += 1
    true_case = cases[2]["source"]
    false_case = cases[4]["source"]
    assert not source_witness_valid(true_case, "NO-SOLUTION")
    assert not source_witness_valid(false_case, [True])
    assert not source_witness_valid(true_case, [1])
    adjacent = {"points": [["0", "0"], ["1", "0"]], "K": 1}
    separated = {"points": [["0", "0"], ["2", "0"]], "K": 1}
    assert target_answer(adjacent) != "NO-SOLUTION"
    assert target_witness_valid(adjacent, [0])
    assert target_witness_valid(adjacent, [1])
    assert not target_witness_valid(adjacent, [])
    assert not target_witness_valid(adjacent, [0, 0])
    assert target_answer(separated) == "NO-SOLUTION"
    assert target_witness_valid(separated, "NO-SOLUTION")
    assert not target_witness_valid(separated, [0])
    assert target_answer({"points": [["0", "0"]], "K": 0}) == "NO-SOLUTION"
    print(f"self-test passed: {len(cases)} cases; {dict(sorted(counts.items()))}")


def candidate_test(path):
    cases = json.loads((WORK / "cases.json").read_text())
    outputs = Counter()
    for index, case in enumerate(cases):
        source = case["source"]
        target = run_candidate(path, [], source)
        first = target_answer(target)
        answers = [first]
        if first != "NO-SOLUTION":
            second = target_answer(target, [first])
            if second != "NO-SOLUTION":
                answers.append(second)
        for answer in answers:
            assert target_witness_valid(target, answer), (index, "invalid target oracle answer")
            recovered = run_candidate(path, ["--extract"], {"source": source, "target_solution": answer})
            assert source_witness_valid(source, recovered), (index, answer, recovered)
            assert (recovered == "NO-SOLUTION") == (case["expected"] == "NO-SOLUTION"), index
            outputs["no_solution" if answer == "NO-SOLUTION" else "witness"] += 1
    print(f"candidate passed: {len(cases)} instances, {dict(outputs)} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    self_test() if args.self_test else candidate_test(args.candidate.resolve())
