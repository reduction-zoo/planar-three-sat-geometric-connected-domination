"""Experimental exact grid point placement with published side-neighbor chains."""

import importlib.util
import json
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location("drawing", ROOT / "rounds/010/drawing.py")
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SCALE = 10


def neighbors(point):
    x, y = point
    return [(x + dx, y + dy) for dx, dy in DIRS]


def expand(a, b):
    x1, y1 = a
    x2, y2 = b
    length = abs(x2 - x1) + abs(y2 - y1)
    assert length and (x1 == x2 or y1 == y2)
    return [(x1 + (x2 - x1) * i // length, y1 + (y2 - y1) * i // length) for i in range(length + 1)]


def independent_points(main, middle):
    choices = {}
    by_position = {}
    for p in sorted(middle):
        candidates = [q for q in neighbors(p) if q not in main and [v for v in neighbors(q) if v in main] == [p]]
        assert 1 <= len(candidates) <= 2, (p, candidates)
        choices[p] = candidates
        for bit, q in enumerate(candidates):
            by_position.setdefault(q, []).append((p, bit))
    implication = nx.DiGraph()
    implication.add_nodes_from((p, bit) for p in choices for bit in range(2))
    for p, candidates in choices.items():
        if len(candidates) == 1:
            implication.add_edge((p, 1), (p, 0))
    for q, owners in by_position.items():
        rivals = set(owners)
        for near in neighbors(q):
            rivals.update(by_position.get(near, ()))
        for p, a in owners:
            for other, b in rivals:
                if p != other:
                    implication.add_edge((p, a), (other, 1 - b))
                    implication.add_edge((other, b), (p, 1 - a))
    components = list(nx.strongly_connected_components(implication))
    comp_id = {node: i for i, component in enumerate(components) for node in component}
    bad = [p for p in choices if comp_id[(p, 0)] == comp_id[(p, 1)]]
    assert not bad, (bad[:4], [(p, choices[p]) for p in bad[:4]])
    dag = nx.condensation(implication, components)
    selected = {}
    for cid in reversed(list(nx.topological_sort(dag))):
        for p, bit in components[cid]:
            if p not in selected:
                selected[p] = bit
    result = {choices[p][bit]: p for p, bit in selected.items()}
    assert len(result) == len(middle)
    assert all([v for v in neighbors(q) if v in main] == [p] and not any(v in result for v in neighbors(q)) for q, p in result.items())
    return result


def clark_points(main, middle):
    result = {}
    for p in sorted(middle):
        candidates = [q for q in neighbors(p) if q not in main and [v for v in neighbors(q) if v in main] == [p]]
        assert candidates, p
        result[candidates[0]] = p
    assert len(result) == len(middle)
    assert max((sum(q in result for q in neighbors(p)) for p in result), default=0) <= 2
    return result


def place(connected):
    core = connected.copy()
    core.remove_nodes_from(v for v in connected if v[0] == "leaf")
    drawn, raw = drawing.checked_layout(core)
    pos = {v: (SCALE * x, SCALE * y) for v, (x, y) in raw.items()}
    routes = {}
    for u in core:
        for a in drawn.neighbors(u):
            chain = [u, a]
            while chain[-1] not in core:
                prior, current = chain[-2:]
                chain.append(next(v for v in drawn.neighbors(current) if v != prior))
            v = chain[-1]
            key = frozenset((u, v))
            if key in routes:
                continue
            points = []
            for a, b in zip(chain, chain[1:]):
                segment = expand(pos[a], pos[b])
                points.extend(segment if not points else segment[1:])
            routes[key] = points
    assert set(routes) == set(map(frozenset, core.edges))
    for u, v in connected.edges:
        if u[0] != "leaf" and v[0] != "leaf":
            continue
        w, leaf = (v, u) if u[0] == "leaf" else (u, v)
        used = {(pos[a][0] - pos[w][0], pos[a][1] - pos[w][1]) for a in drawn.neighbors(w)}
        directions = {(dx and dx // abs(dx), dy and dy // abs(dy)) for dx, dy in used}
        direction = next(d for d in DIRS if d not in directions)
        endpoint = (pos[w][0] + 4 * direction[0], pos[w][1] + 4 * direction[1])
        pos[leaf] = endpoint
        routes[frozenset((w, leaf))] = expand(pos[w], endpoint)
    assert set(routes) == set(map(frozenset, connected.edges))

    original = {pos[v]: v for v in connected}
    assert len(original) == len(connected)
    main = set(original)
    internal = set()
    middle = set()
    intended_edges = set()
    for path in routes.values():
        assert len(path) >= 5
        internal.update(path[1:-1])
        middle.update(path[2:-2])
        main.update(path)
        intended_edges.update(frozenset((a, b)) for a, b in zip(path, path[1:]))
    assert not (set(original) & internal)
    observed_edges = {frozenset((p, q)) for p in main for q in neighbors(p) if q in main}
    assert observed_edges == intended_edges, (len(observed_edges), len(intended_edges))
    leaves = clark_points(main, middle)
    assert len(leaves) == len(middle)
    owner = {p: (edge, i) for edge, path in routes.items() for i, p in enumerate(path[2:-2])}
    assert len(owner) == len(middle)
    assert all(owner[leaves[q]][0] == owner[leaves[p]][0] and abs(owner[leaves[q]][1] - owner[leaves[p]][1]) == 1
               for p in leaves for q in neighbors(p) if q in leaves)
    points = sorted(main | set(leaves))
    return points, original, internal, middle, leaves, routes


def witness(connected, cover, original, middle, routes):
    cover = set(cover)
    by_vertex = {v: p for p, v in original.items()}
    tree = {frozenset(edge) for edge in nx.bfs_edges(connected.subgraph(cover), next(iter(cover)))}
    for v in connected:
        if v not in cover:
            tree.add(frozenset((v, next(u for u in connected.neighbors(v) if u in cover))))
    selected = set(middle) | {by_vertex[v] for v in cover}
    for edge, path in routes.items():
        if edge in tree:
            selected.update((path[1], path[-2]))
        elif original[path[0]] in cover:
            selected.add(path[1])
        else:
            assert original[path[-1]] in cover
            selected.add(path[-2])
    return selected


def check_witness(points, selected):
    points = set(points)
    assert all(p in selected or any(q in selected for q in neighbors(p)) for p in points)
    reached = {next(iter(selected))}
    frontier = list(reached)
    for p in frontier:
        for q in neighbors(p):
            if q in selected and q not in reached:
                reached.add(q)
                frontier.append(q)
    assert reached == selected


if __name__ == "__main__":
    cases = json.loads((ROOT / "work/cases.json").read_text())
    largest = (0, 0, 0)
    for i, case in enumerate(cases):
        graph, bound = drawing.bridge.cover_instance(case["source"])
        connected, goal, subdivisions, _ = drawing.bridge.connected_cover_instance(graph, bound)
        if not connected:
            continue
        points, original, internal, middle, leaves, routes = place(connected)
        target_goal = goal + len(internal) - len(routes) + len(connected) - 1
        if case["expected"] != "NO-SOLUTION":
            cover = drawing.bridge.cover_from_assignment(case["source"], case["expected"])
            connected_cover = drawing.bridge.connected_cover_from_cover(graph, cover, connected, subdivisions)
            selected = witness(connected, connected_cover, original, middle, routes)
            assert len(selected) == target_goal, (i, len(selected), target_goal)
            check_witness(points, selected)
        largest = tuple(max(a, b) for a, b in zip(largest, (len(points), len(middle), len(routes))))
        print(i, len(points), flush=True)
    print("max points, middle vertices, routes:", largest)
