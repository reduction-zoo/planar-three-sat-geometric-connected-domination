"""Finite biconnectivity audit for face-cycle connected-cover cores."""

import importlib.util
from pathlib import Path

import networkx as nx


CAMPAIGN = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location("bridge", CAMPAIGN / "rounds/009/bridge.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


def check_core(original):
    graph = nx.relabel_nodes(original, {v: ("orig", i) for i, v in enumerate(original)})
    connected, _, _, _ = bridge.connected_cover_instance(graph, 0)
    assert nx.check_planarity(connected)[0]
    assert max(degree for _, degree in connected.degree) <= 4
    assert nx.is_connected(connected)
    core = connected.copy()
    core.remove_nodes_from(v for v in connected if v[0] == "leaf")
    assert nx.is_biconnected(core), list(nx.articulation_points(core))
    assert not list(nx.bridges(core))
    return len(core)


if __name__ == "__main__":
    eligible = []
    largest = 0
    for graph in nx.graph_atlas_g():
        if len(graph) < 3 or not nx.is_connected(graph):
            continue
        if not all(2 <= degree <= 3 for _, degree in graph.degree):
            continue
        if not nx.check_planarity(graph)[0]:
            continue
        eligible.append(graph)
        largest = max(largest, check_core(graph))
    for a in (nx.cycle_graph(3), nx.cycle_graph(4), nx.complete_graph(4)):
        for b in (nx.cycle_graph(3), nx.cycle_graph(5)):
            largest = max(largest, check_core(nx.disjoint_union(a, b)))
    print(f"{len(eligible)} connected atlas graphs and 6 disconnected unions passed; largest core {largest}")
