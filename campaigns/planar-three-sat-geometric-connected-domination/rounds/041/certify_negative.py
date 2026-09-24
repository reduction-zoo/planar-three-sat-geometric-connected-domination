"""Target-only structural NO certificates for Clark-style grid point sets."""

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]


def point_graph(target):
    points = target["points"]
    assert type(target["K"]) is int and target["K"] >= 0
    assert points and all(len(p) == 2 and all(type(x) is int for x in p) for p in points)
    lookup = {tuple(p): i for i, p in enumerate(points)}
    assert len(lookup) == len(points)
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    # Distinct integer points are within Euclidean distance one exactly at unit grid steps.
    for (x, y), i in lookup.items():
        for neighbor in ((x + 1, y), (x, y + 1)):
            if neighbor in lookup:
                graph.add_edge(i, lookup[neighbor])
    return graph


def skeleton_from_target(target):
    graph = point_graph(target)
    points = target["points"]
    allowed = {i for i, (x, y) in enumerate(points) if x % 10 == 0 or y % 10 == 0}
    allowed_graph = graph.subgraph(allowed)
    tips = {v for v, degree in allowed_graph.degree if degree == 1
            and any(coordinate % 10 in (1, 9) for coordinate in points[v])}
    main = graph.subgraph(allowed - tips).copy()
    assert main and nx.is_connected(main)
    branches = {v for v, degree in main.degree if degree != 2}
    assert len(branches) >= 3
    skeleton = nx.Graph()
    skeleton.add_nodes_from(sorted(branches))
    routes = {}
    traversed = set()
    for u in sorted(branches):
        for adjacent in sorted(main[u]):
            if frozenset((u, adjacent)) in traversed:
                continue
            path = [u, adjacent]
            while path[-1] not in branches:
                following = [v for v in main[path[-1]] if v != path[-2]]
                assert len(following) == 1 and following[0] not in path
                path.append(following[0])
            v = path[-1]
            key = frozenset((u, v))
            assert u != v and key not in routes and len(path) >= 5
            routes[key] = path
            skeleton.add_edge(u, v)
            traversed.update(frozenset(edge) for edge in zip(path, path[1:]))
    assert len(traversed) == main.number_of_edges()
    assert len(main) == len(branches) + sum(len(path) - 2 for path in routes.values())
    assert nx.is_connected(skeleton) and max(dict(skeleton.degree).values()) <= 4

    middle_owner = {v: (edge, i) for edge, path in routes.items()
                    for i, v in enumerate(path[2:-2])}
    sides = set(graph) - set(main)
    assert len(middle_owner) == len(sides)
    side_owner = {}
    seen_parents = set()
    for side in sides:
        neighbors = set(graph[side]) & set(main)
        assert len(neighbors) == 1
        parent = next(iter(neighbors))
        assert parent in middle_owner and parent not in seen_parents
        side_owner[side] = parent
        seen_parents.add(parent)
    assert seen_parents == set(middle_owner)
    for u, v in graph.subgraph(sides).edges:
        first, second = middle_owner[side_owner[u]], middle_owner[side_owner[v]]
        assert first[0] == second[0] and abs(first[1] - second[1]) == 1

    interior = len(main) - len(branches)
    cover_budget = target["K"] - interior + len(routes) - len(branches) + 1
    assert cover_budget >= 0
    return graph, skeleton, cover_budget, len(routes), len(sides)


def fold_degree_two(original):
    """Minimum vertex-cover size equals cost plus that of the returned graph."""
    graph = original.copy()
    cost = 0
    folds = 0
    serial = max(graph, default=-1) + 1
    while True:
        isolated = next((v for v, degree in graph.degree if degree == 0), None)
        if isolated is not None:
            graph.remove_node(isolated)
            continue
        v = next((v for v, degree in graph.degree
                  if degree == 2 and not graph.has_edge(*list(graph[v]))), None)
        if v is None:
            break
        a, b = list(graph[v])
        exterior = (set(graph[a]) | set(graph[b])) - {a, v, b}
        graph.remove_nodes_from((a, v, b))
        graph.add_node(serial)
        graph.add_edges_from((serial, u) for u in exterior)
        serial += 1
        cost += 1
        folds += 1
    return graph, cost, folds


def exact_cover_size(graph):
    vertices = list(graph)
    assert len(vertices) <= 22, "residual exceeds finite exhaustive domain"
    edges = list(graph.edges)
    for size in range(len(vertices) + 1):
        for choice in itertools.combinations(vertices, size):
            selected = set(choice)
            if all(u in selected or v in selected for u, v in edges):
                return size
    raise AssertionError("every finite graph has a vertex cover")


def certify(target):
    graph, skeleton, budget, routes, sides = skeleton_from_target(target)
    forced = set(nx.articulation_points(skeleton))
    residual = skeleton.subgraph(set(skeleton) - forced)
    folded, cost, folds = fold_degree_two(residual)
    residual_optimum = exact_cover_size(folded)
    lower_bound = len(forced) + cost + residual_optimum
    assert lower_bound > budget, (lower_bound, budget)
    labels = {v: i for i, v in enumerate(sorted(folded))}
    return {"target_points": len(graph), "target_edges": graph.number_of_edges(),
            "K": target["K"], "skeleton_vertices": len(skeleton), "routes": routes,
            "side_points": sides, "cover_budget": budget, "forced_articulations": len(forced),
            "folds": folds, "fold_cost": cost, "residual_vertices": len(folded),
            "residual_edges": folded.number_of_edges(), "residual_exact_cover": residual_optimum,
            "residual_edge_list": sorted(sorted((labels[u], labels[v])) for u, v in folded.edges),
            "connected_cover_lower_bound": lower_bound}


if __name__ == "__main__":
    records = []
    for case in json.loads((HERE / "negative_cases.json").read_text()):
        source = case["source"]
        output = subprocess.run([sys.executable, str(CAMPAIGN / "work/algorithm.py")],
                                input=json.dumps(source), text=True, capture_output=True, check=True).stdout
        target = json.loads(output)
        record = {"case": case["id"], "target_sha256": hashlib.sha256(output.encode()).hexdigest(),
                  **certify(target)}
        recovered = json.loads(subprocess.run([sys.executable, str(CAMPAIGN / "work/algorithm.py"), "--extract"],
                              input=json.dumps({"source": source, "target_solution": "NO-SOLUTION"}),
                              text=True, capture_output=True, check=True).stdout)
        assert recovered == "NO-SOLUTION"
        records.append(record)
        print(json.dumps(record), flush=True)
    (HERE / "certificates.json").write_text(json.dumps(records, indent=2) + "\n")
