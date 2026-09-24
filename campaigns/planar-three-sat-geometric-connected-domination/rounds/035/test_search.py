"""A restricted search must never turn failure into a false NO answer."""
import networkx as nx
from lattice_search import graph_from_points, find_witness

path = {'points': [[i, 0] for i in range(4)], 'K': 2}
answer = find_witness(path)
assert answer is not None and len(answer) == 2
graph = graph_from_points(path['points'])
assert nx.is_connected(graph.subgraph(answer))
assert all(v in answer or set(graph[v]) & set(answer) for v in graph)
assert find_witness(dict(path, K=1)) is None
assert find_witness({'points': [[1, 1]], 'K': 1}) is None
assert find_witness({'points': [[0, 0]], 'K': 0}) is None
print('restricted witness and unknown behavior checked')
