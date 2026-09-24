"""Exhaustive tiny feasible-flow costs, independent of shortest paths."""
import itertools
import random
import networkx as nx
from exact_flow import min_cost_flow

rng = random.Random(26)
for trial in range(80):
    graph = nx.MultiDiGraph()
    graph.add_nodes_from(range(3))
    edges = [(0, 1), (1, 2), (0, 2), (2, 0)]
    for u, v in edges:
        capacity = rng.randrange(3)
        graph.add_edge(u, v, capacity=capacity, weight=rng.randrange(3), lowerbound=rng.randrange(capacity + 1))
    demand = rng.randrange(4)
    nx.set_node_attributes(graph, {0: -demand, 1: 0, 2: demand}, 'demand')
    keyed = list(graph.edges(keys=True))
    feasible = []
    for values in itertools.product(*(range(graph.edges[e]['lowerbound'], graph.edges[e]['capacity'] + 1) for e in keyed)):
        balance = {v: 0 for v in graph}
        for (u, v, _), value in zip(keyed, values):
            balance[u] -= value
            balance[v] += value
        if all(balance[v] == graph.nodes[v]['demand'] for v in graph):
            feasible.append(sum(value * graph.edges[e]['weight'] for e, value in zip(keyed, values)))
    try:
        flow = min_cost_flow(graph)
        cost = sum(flow[e] * graph.edges[e]['weight'] for e in keyed)
        assert all(graph.edges[e]['lowerbound'] <= flow[e] <= graph.edges[e]['capacity'] for e in keyed)
        assert all(sum(flow[e] for e in keyed if e[1] == v) - sum(flow[e] for e in keyed if e[0] == v) == graph.nodes[v]['demand'] for v in graph)
        assert feasible and cost == min(feasible), (trial, cost, feasible)
    except nx.NetworkXUnfeasible:
        assert not feasible, trial
print('80 exhaustive tiny flow optima checked')
