"""Integral min-cost flow by finite shortest augmenting paths, with lower bounds."""
import networkx as nx


def min_cost_flow(graph):
    nodes = list(graph)
    index = {v: i for i, v in enumerate(nodes)}
    source, sink = len(nodes), len(nodes) + 1
    size = len(nodes) + 2
    edges = []
    balance = {v: 0 for v in nodes}
    originals = {}

    def add(u, v, capacity, weight):
        position = len(edges)
        edges.extend([[u, v, capacity, weight], [v, u, 0, -weight]])
        return position

    for u, v, key, data in graph.edges(keys=True, data=True):
        lower = data.get('lowerbound', 0)
        capacity, weight = data['capacity'], data['weight']
        if not 0 <= lower <= capacity or weight < 0:
            raise ValueError('requires nonnegative original costs and legal lower bounds')
        balance[u] -= lower
        balance[v] += lower
        originals[u, v, key] = (add(index[u], index[v], capacity - lower, weight), lower)
    demands = {v: graph.nodes[v].get('demand', 0) - balance[v] for v in nodes}
    if sum(demands.values()):
        raise nx.NetworkXUnfeasible('unbalanced demand')
    required = 0
    for v, demand in demands.items():
        if demand < 0:
            add(source, index[v], -demand, 0)
            required -= demand
        elif demand > 0:
            add(index[v], sink, demand, 0)
    while required:
        distance = [None] * size
        predecessor = [None] * size
        distance[source] = 0
        for _ in range(size - 1):
            changed = False
            for i, (u, v, capacity, weight) in enumerate(edges):
                if capacity and distance[u] is not None and (distance[v] is None or distance[u] + weight < distance[v]):
                    distance[v] = distance[u] + weight
                    predecessor[v] = i
                    changed = True
            if not changed:
                break
        if distance[sink] is None:
            raise nx.NetworkXUnfeasible('no augmenting path')
        path = []
        v = sink
        while v != source:
            edge = predecessor[v]
            path.append(edge)
            v = edges[edge][0]
        amount = min(required, *(edges[i][2] for i in path))
        for i in path:
            edges[i][2] -= amount
            edges[i ^ 1][2] += amount
        required -= amount
    return {key: lower + edges[position ^ 1][2] for key, (position, lower) in originals.items()}
