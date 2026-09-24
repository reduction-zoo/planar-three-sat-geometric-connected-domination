"""Independent exact connected-domination oracle using CP-SAT flow."""

import json
import sys
from pathlib import Path

import networkx as nx
from ortools.sat.python import cp_model


WORK = Path(__file__).parents[2] / "work"
sys.path.insert(0, str(WORK))
import check  # noqa: E402


def solve(target, forbidden=()):
    graph, budget = check.target_graph(target)
    if not nx.is_connected(graph):
        return "NO-SOLUTION"
    n = len(graph)
    model = cp_model.CpModel()
    x = [model.new_bool_var(f"x{i}") for i in graph]
    model.add(sum(x) <= budget)
    for i in graph:
        model.add(sum(x[j] for j in (i, *graph.neighbors(i))) >= 1)
    for answer in forbidden:
        chosen = set(answer)
        model.add(sum(1 - x[i] if i in chosen else x[i] for i in graph) >= 1)
    articulations = list(nx.articulation_points(graph))
    for i in articulations:
        model.add(x[i] == 1)
    if articulations:
        root = articulations[0]
        balance = {i: [] for i in graph}
        for u, v in graph.edges:
            for a, b in ((u, v), (v, u)):
                flow = model.new_int_var(0, n - 1, f"f{a}_{b}")
                model.add(flow <= (n - 1) * x[a])
                model.add(flow <= (n - 1) * x[b])
                balance[a].append(-flow)
                balance[b].append(flow)
        for i in graph:
            model.add(sum(balance[i]) == (1 - sum(x) if i == root else x[i]))
    else:
        root = [model.new_bool_var(f"r{i}") for i in graph]
        model.add(sum(root) == 1)
        balance = {i: [] for i in graph}
        for i in graph:
            model.add(root[i] <= x[i])
            flow = model.new_int_var(0, n, f"source_{i}")
            model.add(flow <= n * root[i])
            balance[i].append(flow)
        for u, v in graph.edges:
            for a, b in ((u, v), (v, u)):
                flow = model.new_int_var(0, n, f"f{a}_{b}")
                model.add(flow <= n * x[a])
                model.add(flow <= n * x[b])
                balance[a].append(-flow)
                balance[b].append(flow)
        model.add(sum(balance[i][0] for i in graph) == sum(x))
        for i in graph:
            model.add(sum(balance[i]) == x[i])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    status = solver.solve(model)
    if status == cp_model.INFEASIBLE:
        return "NO-SOLUTION"
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        raise RuntimeError(f"CP-SAT inconclusive: {solver.status_name(status)}")
    return [i for i in graph if solver.value(x[i])]


if __name__ == "__main__":
    small = [
        {"points": [[0, 0], [1, 0]], "K": 1},
        {"points": [[0, 0], [2, 0]], "K": 1},
        {"points": [[i, 0] for i in range(4)], "K": 1},
        {"points": [[i, 0] for i in range(4)], "K": 2},
        {"points": [[0, 0], [1, 0], [0, 1]], "K": 1},
    ]
    for target in small:
        expected = check.target_answer(target)
        actual = solve(target)
        assert (expected == "NO-SOLUTION") == (actual == "NO-SOLUTION")
        assert check.target_witness_valid(target, actual)
    print(f"{len(small)} small target cases match independent Z3 oracle", flush=True)
    cases = json.loads((WORK / "cases.json").read_text())
    for i in (1, 4):
        target = check.run_candidate(WORK / "algorithm.py", [], cases[i]["source"])
        print("target", i, len(target["points"]), target["K"], flush=True)
        answer = solve(target)
        if answer != "NO-SOLUTION":
            assert check.target_witness_valid(target, answer)
        print("answer", i, "NO-SOLUTION" if answer == "NO-SOLUTION" else len(answer), flush=True)
