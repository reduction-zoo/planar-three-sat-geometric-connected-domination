"""Check every forbidden bar/segment intersection using integer intervals."""
import importlib.util
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('visibility', ROOT / 'rounds/030/visibility.py')
visibility = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visibility)


def validate(graph):
    bars, edges = visibility.bars(graph)
    assert len(set(y for _, _, y in bars.values())) == len(graph)
    for (u, v), (x, low, high) in edges.items():
        assert low < high
        for w, (left, right, y) in bars.items():
            intersects = left <= x <= right and low <= y <= high
            assert intersects == (w in (u, v)), (u, v, w, bars, edges)
    items = list(edges.items())
    for i, (edge, (x, low, high)) in enumerate(items):
        for other, (xx, lo, hi) in items[:i]:
            if x == xx and max(low, lo) <= min(high, hi):
                assert max(low, lo) == min(high, hi) and set(edge) & set(other)


if __name__ == '__main__':
    count = 0
    for graph in nx.graph_atlas_g():
        if len(graph) < 3 or not nx.is_biconnected(graph) or max(dict(graph.degree).values()) > 4 or not nx.check_planarity(graph)[0]:
            continue
        validate(graph)
        count += 1
    print('integer bar drawings validated:', count)
    import json
    spec = importlib.util.spec_from_file_location('bridge', ROOT / 'rounds/009/bridge.py')
    bridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bridge)
    checked = 0
    for case in json.loads((ROOT / 'work/cases.json').read_text())[:12]:
        graph, bound = bridge.cover_instance(case['source'])
        graph, *_ = bridge.connected_cover_instance(graph, bound)
        graph.remove_nodes_from([v for v in graph if v[0] == 'leaf'])
        if graph:
            validate(graph)
            checked += 1
    print('prepared core bar drawings validated:', checked)
