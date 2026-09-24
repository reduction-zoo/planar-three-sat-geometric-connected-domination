"""Elementary st-order and directed dual for biconnected plane graphs."""
import networkx as nx


def ordered_subgraph(graph, nodes):
    result = nx.Graph()
    result.add_nodes_from(v for v in graph if v in nodes)
    result.add_edges_from((u, v) for u, v in graph.edges if u in nodes and v in nodes)
    return result


def orient(graph):
    assert nx.is_biconnected(graph) and len(graph) >= 3
    planar, embedding = nx.check_planarity(graph)
    assert planar
    s, t = next(iter(graph.edges))
    without = graph.copy()
    without.remove_edge(s, t)
    order = nx.shortest_path(without, s, t)
    while len(order) < len(graph):
        position = {v: i for i, v in enumerate(order)}
        outside = ordered_subgraph(graph, set(graph) - set(order))
        component = next(iter(nx.connected_components(outside)))
        boundary = sorted({u for v in component for u in graph[v] if u in position}, key=position.get)
        assert len(boundary) >= 2
        a, b = boundary[:2]
        ear_graph = ordered_subgraph(graph, component | {a, b})
        if ear_graph.has_edge(a, b):
            ear_graph.remove_edge(a, b)
        ear = nx.shortest_path(ear_graph, a, b)[1:-1]
        assert ear
        order[position[a] + 1:position[a] + 1] = ear
    position = {v: i for i, v in enumerate(order)}
    faces = {}
    face_count = 0
    for u, v in embedding.edges():
        if (u, v) not in faces:
            boundary = embedding.traverse_face(u, v)
            for a, b in zip(boundary, boundary[1:] + boundary[:1]):
                faces[a, b] = face_count
            face_count += 1
    dual = nx.DiGraph()
    dual.add_nodes_from(range(face_count))
    for a, b in graph.edges:
        u, v = (a, b) if position[a] < position[b] else (b, a)
        if (u, v) != (s, t):
            dual.add_edge(faces[v, u], faces[u, v])
    assert nx.is_directed_acyclic_graph(dual)
    return order, embedding, faces, dual, (s, t)


def bars(graph):
    order, embedding, faces, dual, (s, t) = orient(graph)
    y = {v: i for i, v in enumerate(order)}
    x = {face: i for i, face in enumerate(nx.topological_sort(dual))}
    segments = {}
    for a, b in graph.edges:
        u, v = (a, b) if y[a] < y[b] else (b, a)
        column = -1 if (u, v) == (s, t) else x[faces[v, u]]
        segments[u, v] = (column, y[u], y[v])
    vertex_bars = {}
    for v in graph:
        columns = [column for edge, (column, _, _) in segments.items() if v in edge]
        vertex_bars[v] = (min(columns), max(columns), y[v])
    return vertex_bars, segments
