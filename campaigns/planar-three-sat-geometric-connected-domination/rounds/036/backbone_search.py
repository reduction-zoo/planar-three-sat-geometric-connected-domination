"""Incomplete target-only backbone search, with full target witness validation."""
import sys
from pathlib import Path
import networkx as nx
import z3

sys.path.insert(0, str(Path(__file__).parents[1] / '035'))
from lattice_search import graph_from_points


def find_witness(target, forbidden=()):
    if not all(type(x) is int for p in target['points'] for x in p):
        return None
    graph = graph_from_points(target['points'])
    allowed = {i for i, (x, y) in enumerate(target['points']) if x % 10 == 0 or y % 10 == 0}
    tips = {v for v, degree in graph.subgraph(allowed).degree if degree == 1
            and any(x % 10 in (1, 9) for x in target['points'][v])}
    main = graph.subgraph(allowed - tips).copy()
    if not main or not nx.is_connected(main):
        return None
    branches = {v for v, degree in main.degree if degree != 2}
    if len(branches) < 3:
        return None
    skeleton = nx.Graph()
    skeleton.add_nodes_from(sorted(branches))
    routes = {}
    traversed = set()
    for u in sorted(branches):
        for adjacent in main[u]:
            if frozenset((u, adjacent)) in traversed:
                continue
            path = [u, adjacent]
            while path[-1] not in branches:
                next_node = next(v for v in main[path[-1]] if v != path[-2])
                if next_node in path:
                    return None
                path.append(next_node)
            v = path[-1]
            key = frozenset((u, v))
            if u == v or key in routes or len(path) < 5:
                return None
            routes[key] = path
            skeleton.add_edge(u, v)
            traversed.update(frozenset(edge) for edge in zip(path, path[1:]))
    if len(traversed) != len(main.edges):
        return None
    internal_count = len(main) - len(branches)
    cover_budget = target['K'] - internal_count + len(routes) - len(branches) + 1
    if cover_budget < 1:
        return None
    variables = {v: z3.Bool(f'cover_{v}') for v in skeleton}
    solver = z3.Solver()
    solver.add(z3.PbLe([(v, 1) for v in variables.values()], cover_budget))
    solver.add(*(z3.Or(variables[u], variables[v]) for u, v in skeleton.edges))
    for v in nx.articulation_points(skeleton):
        solver.add(variables[v])
    for v, degree in skeleton.degree:
        if degree == 1:
            solver.add(z3.Not(variables[v]))
    rejected = {frozenset(answer) for answer in forbidden}
    while solver.check() == z3.sat:
        model = solver.model()
        cover = {v for v, var in variables.items() if z3.is_true(model.eval(var))}
        components = list(nx.connected_components(skeleton.subgraph(cover)))
        if len(components) != 1:
            for component in components:
                boundary = {u for v in component for u in skeleton[v]} - component
                solver.add(z3.Or(*(z3.Not(variables[v]) for v in component), *(variables[v] for v in boundary)))
            continue
        tree = {frozenset(edge) for edge in nx.bfs_edges(skeleton.subgraph(cover), min(cover))}
        for v in sorted(set(skeleton) - cover):
            tree.add(frozenset((v, min(set(skeleton[v]) & cover))))
        variants = [tree]
        for u, v in skeleton.subgraph(cover).edges:
            edge = frozenset((u, v))
            if edge not in tree:
                tree_graph = nx.Graph([tuple(e) for e in tree])
                path = nx.shortest_path(tree_graph, u, v)
                variants.append((tree - {frozenset(path[:2])}) | {edge})
                break
        for edges in variants:
            selected = set(cover)
            for edge, path in routes.items():
                selected.update(path[2:-2])
                if edge in edges:
                    selected.update((path[1], path[-2]))
                else:
                    selected.add(path[1] if path[0] in cover else path[-2])
            if frozenset(selected) in rejected:
                continue
            if len(selected) <= target['K'] and nx.is_connected(graph.subgraph(selected)) and all(v in selected or set(graph[v]) & selected for v in graph):
                return sorted(selected)
        solver.add(z3.Or(*(var != (v in cover) for v, var in variables.items())))
    return None
