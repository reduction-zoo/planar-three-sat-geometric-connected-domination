"""Experimental planar-SAT to subcubic planar vertex-cover bridge."""

import json
from pathlib import Path

import networkx as nx
import z3


def cover_instance(source):
    n, clauses, rotation = source["variables"], source["clauses"], source["embedding"]
    graph = nx.Graph()
    parity = {}
    bound = 2 * len(clauses)
    for v in range(n):
        occurrences = [(c, p) for c in range(len(clauses)) for p, lit in enumerate(clauses[c]) if abs(lit) == v + 1]
        by_clause = {c: [] for c, _ in occurrences}
        for c, p in occurrences:
            by_clause[c].append((c, p))
        ordered = [occ for name in rotation[f"v{v}"] for occ in by_clause[int(name[1:])]]
        assert len(ordered) == len(occurrences)
        size = max(2, len(ordered))
        nodes = [("v", v, i) for i in range(2 * size)]
        graph.add_edges_from((nodes[i], nodes[(i + 1) % len(nodes)]) for i in range(len(nodes)))
        for slot, (c, p) in enumerate(ordered):
            lit = clauses[c][p]
            port = nodes[2 * slot + (lit < 0)]
            parity[(c, p)] = port
        bound += size
    for c, clause in enumerate(clauses):
        by_var = {}
        for p, lit in enumerate(clause):
            by_var.setdefault(abs(lit) - 1, []).append(p)
        ordered = [p for name in rotation[f"c{c}"] for p in reversed(by_var[int(name[1:])])]
        assert len(ordered) == 3
        nodes = [("c", c, p) for p in ordered]
        graph.add_edges_from((nodes[i], nodes[(i + 1) % 3]) for i in range(3))
        for p in ordered:
            graph.add_edge(("c", c, p), parity[(c, p)])
    return graph, bound


def cover_exists(graph, bound):
    solver = z3.Solver()
    x = {v: z3.Bool(f"p{i}") for i, v in enumerate(graph.nodes)}
    if x:
        solver.add(z3.PbLe([(a, 1) for a in x.values()], bound))
    solver.add(*(z3.Or(x[a], x[b]) for a, b in graph.edges))
    return solver.check() == z3.sat


def connected_cover_instance(graph, bound):
    """Apply Garey--Johnson's edge subdivisions and face cycles."""
    result = nx.Graph()
    result.add_nodes_from(graph)
    subdivisions = {}
    for i, (u, v) in enumerate(sorted(graph.edges, key=repr)):
        a, b = ("x", i, 0), ("x", i, 1)
        result.add_edges_from(((u, a), (a, b), (b, v)))
        subdivisions[(u, v)] = (a, b)
    is_planar, embedding = nx.check_planarity(result)
    assert is_planar
    faces = []
    seen = set()
    for u, v in embedding.edges():
        if (u, v) not in seen:
            face = embedding.traverse_face(u, v)
            seen.update((face[i], face[(i + 1) % len(face)]) for i in range(len(face)))
            faces.append(face)
    by_component = []
    for component in nx.connected_components(result):
        these = [face for face in faces if face[0] in component]
        by_component.append(these)
    ordered_faces = [[vertex for faceset in by_component for vertex in faceset[0]]] if by_component else []
    ordered_faces += [face for faceset in by_component for face in faceset[1:]]
    r = 0
    for face in ordered_faces:
        ports = []
        used = set()
        for vertex in face:
            if vertex not in used and result.degree(vertex) < 4:
                used.add(vertex)
                a, b = ("w", r), ("leaf", r)
                r += 1
                result.add_edges_from(((vertex, a), (a, b)))
                ports.append(a)
        if len(ports) >= 2:
            result.add_edges_from((ports[i], ports[(i + 1) % len(ports)]) for i in range(len(ports)))
    return result, bound + len(graph.edges) + r, subdivisions, r


def cover_from_assignment(source, assignment):
    graph, bound = cover_instance(source)
    chosen = {node for node in graph if node[0] == "v" and node[2] % 2 == (not assignment[node[1]])}
    for c, clause in enumerate(source["clauses"]):
        omitted = next(p for p, lit in enumerate(clause) if assignment[abs(lit) - 1] == (lit > 0))
        chosen.update(("c", c, p) for p in range(3) if p != omitted)
    assert len(chosen) == bound and all(u in chosen or v in chosen for u, v in graph.edges)
    return chosen


def connected_cover_from_cover(graph, cover, connected, subdivisions):
    chosen = set(cover)
    chosen.update(vertex for vertex in connected if vertex[0] == "w")
    for (u, v), (a, b) in subdivisions.items():
        chosen.add(b if u in cover else a)
    return chosen


def recover_cover(graph, connected_cover, subdivisions):
    chosen = set(graph) & set(connected_cover)
    for (u, v), (a, b) in subdivisions.items():
        if u not in chosen and v not in chosen:
            assert a in connected_cover and b in connected_cover
            chosen.add(u)
    return chosen


def recover_assignment(source, cover):
    return [("v", v, 0) in cover for v in range(source["variables"])]


if __name__ == "__main__":
    cases = json.loads((Path(__file__).parents[2] / "work" / "cases.json").read_text())
    for i, case in enumerate(cases):
        graph, bound = cover_instance(case["source"])
        assert max((d for _, d in graph.degree), default=0) <= 3, i
        assert nx.check_planarity(graph)[0], (i, "nonplanar")
        connected, goal, subdivisions, _ = connected_cover_instance(graph, bound)
        assert nx.check_planarity(connected)[0], (i, "connected-cover graph is nonplanar")
        assert max((d for _, d in connected.degree), default=0) <= 4, (i, "degree exceeds four")
        assert not connected or nx.is_connected(connected), (i, "disconnected")
        if i < 7:
            assert cover_exists(graph, bound) == (case["expected"] != "NO-SOLUTION"), (i, "wrong label")
        if case["expected"] != "NO-SOLUTION":
            cover = cover_from_assignment(case["source"], case["expected"])
            connected_cover = connected_cover_from_cover(graph, cover, connected, subdivisions)
            assert len(connected_cover) == goal, (i, "wrong size")
            assert all(u in connected_cover or v in connected_cover for u, v in connected.edges), (i, "uncovered")
            assert not connected or nx.is_connected(connected.subgraph(connected_cover)), (i, "unconnected")
            recovered = recover_cover(graph, connected_cover, subdivisions)
            assert len(recovered) <= bound and all(u in recovered or v in recovered for u, v in graph.edges), i
            answer = recover_assignment(case["source"], recovered)
            assert all(any(answer[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in case["source"]["clauses"]), i
    print(f"{len(cases)} planar subcubic cover and connected-cover instances checked")
