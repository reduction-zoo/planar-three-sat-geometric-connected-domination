"""Experimental coordinate-level implementation of Clark et al. Lemma 6.1."""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location("grid", ROOT / "rounds/011/grid.py")
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)


def is_cds(points, selected):
    if not selected or not selected <= points:
        return False
    reached = {next(iter(selected))}
    frontier = list(reached)
    for p in frontier:
        for q in grid.neighbors(p):
            if q in selected and q not in reached:
                reached.add(q)
                frontier.append(q)
    return len(reached) == len(selected) and all(p in selected or any(q in selected for q in grid.neighbors(p)) for p in points)


def normalize(points, selected, side_to_middle, routes):
    points = set(points)
    selected = set(selected)
    assert is_cds(points, selected)
    side_by_middle = {x: y for y, x in side_to_middle.items()}
    assert len(side_by_middle) == len(side_to_middle)
    while any(y in selected for y in side_to_middle):
        changed = False
        for path in routes.values():
            middles = path[2:-2]
            if not any(side_by_middle[x] in selected for x in middles):
                continue
            missing = [i for i, x in enumerate(middles) if x not in selected and side_by_middle[x] not in selected]
            if not missing:
                candidate = (selected - {side_by_middle[x] for x in middles}) | set(middles)
                if len(candidate) <= len(selected) and is_cds(points, candidate):
                    selected = candidate
                    changed = True
                    break
            for i in missing:
                y = side_by_middle[middles[i]]
                for z in grid.neighbors(y):
                    if z not in selected or z not in side_to_middle:
                        continue
                    j = middles.index(side_to_middle[z]) if side_to_middle[z] in middles else -1
                    if j < 0:
                        continue
                    for interval in (middles[: j + 1], middles[j:]):
                        candidate = (selected - {side_by_middle[x] for x in interval}) | set(interval) | {middles[i]}
                        if len(candidate) <= len(selected) and is_cds(points, candidate):
                            selected = candidate
                            changed = True
                            break
                    if changed:
                        break
                if changed:
                    break
            if changed:
                break
        assert changed, ("normalization stuck", sum(y in selected for y in side_to_middle))
    return selected


def recover_connected_cover(connected, points, selected, original, sides, routes, budget):
    canonical = normalize(points, selected, sides, routes)
    cover = {v for p, v in original.items() if p in canonical}
    assert len(cover) <= budget
    assert all(u in cover or v in cover for u, v in connected.edges)
    assert grid.nx.is_connected(connected.subgraph(cover))
    return cover


if __name__ == "__main__":
    cases = json.loads((ROOT / "work/cases.json").read_text())
    checked = 0
    for i, case in enumerate(cases):
        if case["expected"] == "NO-SOLUTION" or not case["source"]["variables"]:
            continue
        graph, bound = grid.drawing.bridge.cover_instance(case["source"])
        connected, goal, subdivisions, _ = grid.drawing.bridge.connected_cover_instance(graph, bound)
        points, original, _, middle, sides, routes = grid.place(connected)
        cover = grid.drawing.bridge.cover_from_assignment(case["source"], case["expected"])
        connected_cover = grid.drawing.bridge.connected_cover_from_cover(graph, cover, connected, subdivisions)
        selected = grid.witness(connected, connected_cover, original, middle, routes)
        recovered = recover_connected_cover(connected, points, selected, original, sides, routes, goal)
        planar_cover = grid.drawing.bridge.recover_cover(graph, recovered, subdivisions)
        answer = grid.drawing.bridge.recover_assignment(case["source"], planar_cover)
        assert all(any(answer[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in case["source"]["clauses"]), i
        if i == 1:
            alternate = set(selected)
            swaps = []
            for y, parent in sides.items():
                if parent not in alternate or y in alternate:
                    continue
                for x in grid.neighbors(parent):
                    if x in middle and x in alternate and x != parent:
                        candidate = (alternate - {x}) | {y}
                        if is_cds(set(points), candidate):
                            alternate = candidate
                            swaps.append((x, y))
                            break
                if len(swaps) == 10:
                    break
            assert swaps and len(alternate) == len(selected)
            recovered_alt = recover_connected_cover(connected, points, alternate, original, sides, routes, goal)
            planar_alt = grid.drawing.bridge.recover_cover(graph, recovered_alt, subdivisions)
            answer_alt = grid.drawing.bridge.recover_assignment(case["source"], planar_alt)
            assert all(any(answer_alt[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in case["source"]["clauses"])
            print(f"case 1 alternate target witness: {len(swaps)} side-chain swaps decoded")
        checked += 1
    print(f"{checked} canonical target witnesses decoded")
