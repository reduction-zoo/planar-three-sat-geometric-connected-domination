"""Test the st-order and dual contract without checking implementation text."""
import networkx as nx
from visibility import orient

count = 0
for graph in nx.graph_atlas_g():
    if len(graph) < 3 or not nx.is_biconnected(graph) or max(dict(graph.degree).values()) > 4 or not nx.check_planarity(graph)[0]:
        continue
    order, embedding, faces, dual, st = orient(graph)
    position = {v: i for i, v in enumerate(order)}
    assert set(order) == set(graph) and len(order) == len(graph)
    assert all(any(position[u] < position[v] for u in graph[v]) and any(position[u] > position[v] for u in graph[v]) for v in order[1:-1])
    for v in graph:
        directions = [position[u] > position[v] for u in embedding.neighbors_cw_order(v)]
        assert sum(a != b for a, b in zip(directions, directions[1:] + directions[:1])) <= 2
    assert nx.is_directed_acyclic_graph(dual)
    assert sum(dual.in_degree(v) == 0 for v in dual) == 1
    assert sum(dual.out_degree(v) == 0 for v in dual) == 1
    count += 1
print('st-order and dual premises checked:', count)
