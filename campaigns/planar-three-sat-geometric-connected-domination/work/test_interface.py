"""End-to-end interface check with an independently validated target witness."""

import importlib.util
import json
import sys
from pathlib import Path


WORK = Path(__file__).parent
sys.path.insert(0, str(WORK))
import check  # noqa: E402

spec = importlib.util.spec_from_file_location("grid", WORK.parent / "rounds/011/grid.py")
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)
candidate = WORK / "algorithm.py"
cases = json.loads((WORK / "cases.json").read_text())

empty = cases[0]["source"]
target = check.run_candidate(candidate, [], empty)
assert check.target_witness_valid(target, [0])
assert check.run_candidate(candidate, ["--extract"], {"source": empty, "target_solution": [0]}) == []

case = cases[1]
source = case["source"]
target = check.run_candidate(candidate, [], source)
graph, bound = grid.drawing.bridge.cover_instance(source)
connected, _, subdivisions, _ = grid.drawing.bridge.connected_cover_instance(graph, bound)
points, original, _, middle, sides, routes = grid.place(connected)
cover = grid.drawing.bridge.cover_from_assignment(source, case["expected"])
connected_cover = grid.drawing.bridge.connected_cover_from_cover(graph, cover, connected, subdivisions)
selected = grid.witness(connected, connected_cover, original, middle, routes)
index = {tuple(point): i for i, point in enumerate(target["points"])}
answer = [index[point] for point in selected]
assert check.target_witness_valid(target, answer)
recovered = check.run_candidate(candidate, ["--extract"], {"source": source, "target_solution": answer})
assert check.source_witness_valid(source, recovered)
alternate = set(selected)
for side, parent in sides.items():
    if parent not in alternate:
        continue
    for removed in grid.neighbors(parent):
        if removed in middle and removed in alternate and removed != parent:
            candidate_set = (alternate - {removed}) | {side}
            if all(point in candidate_set or any(q in candidate_set for q in grid.neighbors(point)) for point in points):
                reachable = {next(iter(candidate_set))}
                queue = list(reachable)
                for point in queue:
                    for q in grid.neighbors(point):
                        if q in candidate_set and q not in reachable:
                            reachable.add(q)
                            queue.append(q)
                if reachable == candidate_set:
                    alternate = candidate_set
                    break
    if alternate != selected:
        break
assert alternate != selected
alternate_indices = [index[point] for point in alternate]
assert check.target_witness_valid(target, alternate_indices)
recovered = check.run_candidate(candidate, ["--extract"], {"source": source, "target_solution": alternate_indices})
assert check.source_witness_valid(source, recovered)
print("empty, canonical and side-chain F/G subprocesses passed independent target-witness checks")
