"""Exhaustive expected optimum, independent of the DP recurrence."""
import itertools
import networkx as nx
from target_dp import solve_graph


def brute(graph):
    for k in range(1, len(graph) + 1):
        for selected in itertools.combinations(graph, k):
            chosen = set(selected)
            if nx.is_connected(graph.subgraph(chosen)) and all(v in chosen or set(graph[v]) & chosen for v in graph):
                return k


def main():
    count = 0
    for graph in nx.graph_atlas_g():
        if not 0 < len(graph) <= 6 or not nx.is_connected(graph):
            continue
        answer = solve_graph(graph)
        assert len(answer) == brute(graph), (list(graph.edges), answer, brute(graph))
        assert nx.is_connected(graph.subgraph(answer))
        assert all(v in answer or set(graph[v]) & set(answer) for v in graph)
        count += 1
    print('exact graph-atlas optima checked:', count)


if __name__ == '__main__':
    main()
