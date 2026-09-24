"""Elementary st-order and directed dual for biconnected plane graphs."""
import networkx as nx


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
        outside = graph.subgraph(set(graph) - set(order))
        component = next(iter(nx.connected_components(outside)))
        boundary = sorted({u for v in component for u in graph[v] if u in position}, key=position.get)
        assert len(boundary) >= 2
        a, b = boundary[:2]
        ear_graph = graph.subgraph(component | {a, b}).copy()
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
