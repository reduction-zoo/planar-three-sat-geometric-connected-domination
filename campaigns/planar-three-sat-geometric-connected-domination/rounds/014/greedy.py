"""Independent target-only connected domination heuristic; witnesses are checked."""

import itertools
import random

import networkx as nx


def find_witness(graph, budget, seed=0):
    nodes = list(graph)
    adjacent = {v: set(graph[v]) for v in nodes}
    closed = {v: adjacent[v] | {v} for v in nodes}
    rng = random.Random(seed)
    root = rng.choice(nodes)
    selected = {root}
    undominated = set(nodes) - closed[root]
    frontier = adjacent[root].copy()
    while undominated:
        gain = max(len(closed[v] & undominated) for v in frontier)
        v = rng.choice([v for v in frontier if len(closed[v] & undominated) == gain])
        selected.add(v)
        undominated.difference_update(closed[v])
        frontier.discard(v)
        frontier.update(adjacent[v] - selected)
    while len(selected) > budget:
        counts = {p: len(closed[p] & selected) for p in nodes}
        improvement = None
        for added in nodes:
            if added in selected:
                continue
            near = closed[added] | {v for u in closed[added] for v in adjacent[u]}
            for first, second in itertools.combinations(sorted(near & selected), 2):
                affected = closed[first] | closed[second] | closed[added]
                if any(counts[p] - (first in closed[p]) - (second in closed[p]) + (added in closed[p]) == 0 for p in affected):
                    continue
                candidate = (selected - {first, second}) | {added}
                if nx.is_connected(graph.subgraph(candidate)):
                    improvement = candidate
                    break
            if improvement is not None:
                break
        if improvement is None:
            return None, len(selected)
        selected = improvement
    assert len(selected) <= budget
    assert nx.is_connected(graph.subgraph(selected))
    assert all(closed[p] & selected for p in nodes)
    return sorted(selected), len(selected)
