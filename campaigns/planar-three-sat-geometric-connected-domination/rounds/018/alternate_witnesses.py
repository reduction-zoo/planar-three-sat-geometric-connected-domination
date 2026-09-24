"""Independent target and source validation of varied side-chain outputs."""

import importlib.util
import json
import sys
from pathlib import Path


CAMPAIGN = Path(__file__).parents[2]
WORK = CAMPAIGN / "work"
sys.path.insert(0, str(WORK))
import check  # noqa: E402

spec = importlib.util.spec_from_file_location("grid", CAMPAIGN / "rounds/011/grid.py")
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)


def connected(selected):
    seen = {next(iter(selected))}
    queue = list(seen)
    for p in queue:
        for q in grid.neighbors(p):
            if q in selected and q not in seen:
                seen.add(q)
                queue.append(q)
    return len(seen) == len(selected)


def alternate(points, selected, middle, sides):
    points = set(points)
    counts = {p: int(p in selected) + sum(q in selected for q in grid.neighbors(p)) for p in points}
    for side, parent in sides.items():
        if side in selected or parent not in selected:
            continue
        for removed in grid.neighbors(parent):
            if removed not in middle or removed not in selected or removed == parent:
                continue
            affected = {removed, side, *grid.neighbors(removed), *grid.neighbors(side)} & points
            if any(counts[p] - (p == removed or removed in grid.neighbors(p)) + (p == side or side in grid.neighbors(p)) < 1 for p in affected):
                continue
            candidate = (selected - {removed}) | {side}
            if connected(candidate):
                return candidate, (removed, side)
    return None, None


if __name__ == "__main__":
    cases = json.loads((WORK / "cases.json").read_text())
    indices = (1, 2, 7, 16, 17, 21, 49, 52, 84, 97, 110, 13)
    successes = []
    for i in indices:
        case = cases[i]
        assert case["expected"] != "NO-SOLUTION"
        source = case["source"]
        target = check.run_candidate(WORK / "algorithm.py", [], source)
        graph, bound = grid.drawing.bridge.cover_instance(source)
        connected_graph, _, subdivisions, _ = grid.drawing.bridge.connected_cover_instance(graph, bound)
        points, original, _, middle, sides, routes = grid.place(connected_graph)
        cover = grid.drawing.bridge.cover_from_assignment(source, case["expected"])
        connected_cover = grid.drawing.bridge.connected_cover_from_cover(graph, cover, connected_graph, subdivisions)
        canonical = grid.witness(connected_graph, connected_cover, original, middle, routes)
        selected, swap = alternate(points, canonical, middle, sides)
        if selected is None:
            print(i, len(points), "no local alternate found", flush=True)
            continue
        index = {tuple(point): j for j, point in enumerate(target["points"])}
        answer = [index[p] for p in selected]
        assert len(answer) <= target["K"] and check.target_witness_valid(target, answer)
        recovered = check.run_candidate(WORK / "algorithm.py", ["--extract"], {"source": source, "target_solution": answer})
        assert check.source_witness_valid(source, recovered), (i, swap, recovered)
        successes.append(i)
        print(i, len(points), "alternate decoded", flush=True)
    print("validated distinct side-chain outputs:", successes)
