"""Exact tiny vertex-cover budgets independently enumerated."""
import itertools
import networkx as nx
from cover_kernel import vertex_cover

count = 0
for graph in nx.graph_atlas_g():
    if len(graph) > 6:
        continue
    optimum = next(k for k in range(len(graph) + 1) if any(all(u in subset or v in subset for u, v in graph.edges) for subset in itertools.combinations(graph, k)))
    answer = vertex_cover(graph, optimum)
    assert answer is not None and len(answer) <= optimum and all(u in answer or v in answer for u, v in graph.edges)
    if optimum:
        assert vertex_cover(graph, optimum - 1) is None
    count += 1
print('exact vertex-cover kernel budgets checked:', count)
