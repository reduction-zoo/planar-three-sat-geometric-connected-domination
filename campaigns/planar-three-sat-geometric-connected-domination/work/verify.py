"""Standalone exact verification of the candidate's small target instances."""

import argparse
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


WORK = Path(__file__).parent


def candidate_call(path, extract, payload):
    command = [sys.executable, str(path)] + (["--extract"] if extract else [])
    result = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def satisfies(source, assignment):
    return (isinstance(assignment, list) and len(assignment) == source["variables"]
            and all(type(value) is bool for value in assignment)
            and all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)
                    for clause in source["clauses"]))


def source_has_witness(source):
    return any(satisfies(source, list(values)) for values in itertools.product((False, True), repeat=source["variables"]))


def target_answer(target):
    points = [tuple(Fraction(value) for value in point) for point in target["points"]]
    assert 0 < len(points) <= 12 and len(set(points)) == len(points)
    budget = target["K"]
    graph = {i: set() for i in range(len(points))}
    for i, j in itertools.combinations(graph, 2):
        if sum((points[i][d] - points[j][d]) ** 2 for d in range(2)) <= 1:
            graph[i].add(j)
            graph[j].add(i)
    for size in range(1, min(budget, len(points)) + 1):
        for subset in itertools.combinations(graph, size):
            chosen = set(subset)
            if not all(i in chosen or graph[i] & chosen for i in graph):
                continue
            reached = {subset[0]}
            queue = list(reached)
            for i in queue:
                for j in graph[i] & (chosen - reached):
                    reached.add(j)
                    queue.append(j)
            if reached == chosen:
                return list(subset)
    return "NO-SOLUTION"


def main(candidate):
    cases = json.loads((WORK / "cases.json").read_text())
    selected = [(i, case) for i, case in enumerate(cases) if i == 0 or case["expected"] == "NO-SOLUTION"]
    counts = {"witness": 0, "no_solution": 0}
    for i, case in selected:
        source = case["source"]
        target = candidate_call(candidate, False, source)
        answer = target_answer(target)
        recovered = candidate_call(candidate, True, {"source": source, "target_solution": answer})
        if answer == "NO-SOLUTION":
            assert recovered == "NO-SOLUTION" and not source_has_witness(source), i
            counts["no_solution"] += 1
        else:
            assert satisfies(source, recovered) and source_has_witness(source), i
            counts["witness"] += 1
    print(f"standalone exact target solve and source recovery: {len(selected)} cases, {counts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    main(args.candidate.resolve())
