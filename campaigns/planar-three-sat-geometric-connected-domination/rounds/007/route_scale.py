"""Lower bound on points in the published 16-block Grid Tiling route."""

import json
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[2] / "work"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "005"))
from grid_bridge import tiling_sets  # noqa: E402


def main():
    cases = json.loads((WORK / "cases.json").read_text())
    hard_no = []
    largest = (0, None)
    for index, case in enumerate(cases):
        m = len(case["source"]["clauses"])
        if m == 0 or any(not cell for row in tiling_sets(case["source"]) for cell in row):
            continue
        alphabet = 3 * m
        y_points = 16 * m * m * (alphabet * alphabet + 1)
        if y_points > largest[0]:
            largest = (y_points, index)
        if case["expected"] == "NO-SOLUTION":
            hard_no.append((y_points, index, m))
    print(f"smallest nontrivial NO Y-point bound: {min(hard_no)}")
    print(f"largest prepared Y-point bound: {largest}")


if __name__ == "__main__":
    main()
