"""Measure and verify a target-only tree decomposition."""
import json
import sys
from pathlib import Path
import networkx as nx

WORK = Path(__file__).parents[2] / 'work'
sys.path.insert(0, str(WORK))
import verify


def graph_from_target(target):
    # This experiment's targets are integer grids; no candidate metadata is read.
    points = list(map(tuple, target['points']))
    assert all(type(x) is int for point in points for x in point)
    lookup = {p: i for i, p in enumerate(points)}
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for i, (x, y) in enumerate(points):
        for p in ((x + 1, y), (x, y + 1)):
            if p in lookup:
                graph.add_edge(i, lookup[p])
    return graph


if __name__ == '__main__':
    source = json.loads((WORK / 'cases.json').read_text())[1]['source']
    target = verify.candidate_call(WORK / 'algorithm.py', False, source)
    graph = graph_from_target(target)
    width, tree = nx.approximation.treewidth_min_degree(graph)
    assert nx.is_tree(tree)
    assert set().union(*tree) == set(graph)
    assert all(any({u, v} <= bag for bag in tree) for u, v in graph.edges)
    assert all(nx.is_connected(tree.subgraph([bag for bag in tree if v in bag])) for v in graph)
    print('vertices', len(graph), 'bags', len(tree), 'width', width)
    print('bag sizes', {size: sum(len(b) == size for b in tree) for size in sorted(set(map(len, tree)))})
