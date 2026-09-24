"""A finite exact test of one variable's unit-disk interface."""

import itertools
import json
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[2] / "work"
sys.path.insert(0, str(WORK))
from check import source_witness_valid, target_witness_valid  # noqa: E402


def local_target(source):
    points = [["0", "0"], ["-1", "0"], ["1", "0"], ["0", "1"], ["1", "1"]]
    signs = set()
    for clause in source["clauses"]:
        clause_signs = {literal > 0 for literal in clause}
        if len(clause_signs) == 1:
            signs.update(clause_signs)
    if True in signs:
        points.append(["2", "0"])
    if False in signs:
        points.append(["0", "2"])
    return {"points": points, "K": 2}


def main():
    cases = json.loads((WORK / "cases.json").read_text())
    checked = positive = negative = 0
    for case in cases:
        source = case["source"]
        if source["variables"] != 1:
            continue
        target = local_target(source)
        solutions = [list(s) for k in range(3) for s in itertools.combinations(range(len(target["points"])), k) if target_witness_valid(target, list(s))]
        expected_yes = case["expected"] != "NO-SOLUTION"
        assert bool(solutions) == expected_yes, (source, solutions)
        for solution in solutions:
            assert 0 in solution
            decoded = [2 in solution]
            assert source_witness_valid(source, decoded), (source, solution, decoded)
        checked += 1
        positive += expected_yes
        negative += not expected_yes
    print(f"one-variable interface: {checked} formulas, {positive} satisfiable, {negative} unsatisfiable")
    # A direct clause point cannot touch literal ports separated by four units:
    # any point within one of both would put the ports at distance at most two.
    assert (5 - 1) ** 2 > 2 ** 2
    print("direct shared-clause composition fails for copies translated by four units")


if __name__ == "__main__":
    main()
