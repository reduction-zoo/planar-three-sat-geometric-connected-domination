"""Audit graph-layout GIOTTO routes against the existing exact geometry checker."""

import argparse
import importlib.util
import json
from pathlib import Path

import networkx as nx
from graph_layout import GIOTTOLayout


CAMPAIGN = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location("drawing", CAMPAIGN / "rounds/010/drawing.py")
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)


def position(pair):
    result = tuple(round(2 * value) for value in pair)
    assert all(abs(2 * value - value2) < 1e-8 for value, value2 in zip(pair, result))
    return result


def checked_giotto(core):
    vertices = list(core)
    node_id = {v: i for i, v in enumerate(vertices)}
    layout = GIOTTOLayout(
        nodes=[{} for _ in vertices],
        links=[{"source": node_id[u], "target": node_id[v]} for u, v in core.edges],
        node_width=0, node_height=0, node_separation=1, edge_separation=1,
        size=(800, 600), strict=True, bend_optimal=True,
    )
    layout.run()
    assert layout.used_bend_optimal, "heuristic fallback"
    drawn = nx.Graph()
    coords = {vertices[i]: position((node.x, node.y)) for i, node in enumerate(layout.nodes)}
    drawn.add_nodes_from(core)
    for edge_id, edge in enumerate(layout.orthogonal_edges):
        source, target = vertices[edge.source], vertices[edge.target]
        chain = [source]
        for bend_id, bend in enumerate(edge.bends):
            bend_node = ("altbend", edge_id, bend_id)
            coords[bend_node] = position(bend)
            chain.append(bend_node)
        chain.append(target)
        drawn.add_edges_from(zip(chain, chain[1:]))
    return drawing.validate_layout(core, drawn, coords)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--stress", action="store_true")
    args = parser.parse_args()
    cases = json.loads((CAMPAIGN / "work/cases.json").read_text())
    largest = (0, 0, 0)
    if args.stress:
        stress_spec = importlib.util.spec_from_file_location("stress", CAMPAIGN / "rounds/016/stress.py")
        stress = importlib.util.module_from_spec(stress_spec)
        stress_spec.loader.exec_module(stress)
        sources = [("isolated", n, stress.isolated(n)) for n in (1, 2, 5, 10, 20)]
        sources += [("star", n, stress.star(n)) for n in (1, 2, 5, 10, 20)]
        sources += [("chain", n, stress.chain(n)) for n in (1, 2, 5, 10, 20)]
        sources += [("cycle", n, stress.chain(n, True)) for n in (3, 5, 10, 20)]
        sources += [("tree", n, stress.tree(n)) for n in (1, 2, 5, 10, 20)]
    else:
        sources = [("case", i, cases[i]["source"]) for i in (range(1, len(cases)) if args.all else (1, 2, 7, 16))]
    for family, i, source in sources:
        graph, bound = drawing.bridge.cover_instance(source)
        connected, _, _, _ = drawing.bridge.connected_cover_instance(graph, bound)
        core = connected.copy()
        core.remove_nodes_from(v for v in connected if v[0] == "leaf")
        drawn, coords = checked_giotto(core)
        length = sum(abs(coords[u][0] - coords[v][0]) + abs(coords[u][1] - coords[v][1]) for u, v in drawn.edges)
        largest = tuple(max(a, b) for a, b in zip(largest, (len(core), len(drawn), length)))
        if not args.all:
            print(family, i, len(core), len(drawn), length, flush=True)
    print("checked", len(sources), "largest", largest)
