"""Offline finite template synthesis via vertex-disjoint paths."""
import itertools
import json
from pathlib import Path
import networkx as nx


def template(pattern):
    width = 2 * len(pattern)
    terminals = [(2 * i + 1, y) for i, kind in enumerate(pattern) for y in (-4, 4) if kind == 'X' or kind == ('T' if y == 4 else 'B')]
    points = {(x, y) for x in range(width + 1) for y in range(-3, 4)} | set(terminals)
    centers = sorted(((x, y) for x in range(1, width) for y in range(-2, 3)), key=lambda p: (abs(p[1]), abs(p[0] - width // 2), p))
    for center in centers:
        network = nx.DiGraph()
        sink = ('sink',)
        for p in sorted(points):
            network.add_edge((p, 0), (p, 1), capacity=len(terminals) if p == center else 1)
            x, y = p
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q in points:
                    network.add_edge((p, 1), (q, 0), capacity=1)
        for p in terminals:
            network.add_edge((p, 1), sink, capacity=1)
        source = (center, 1)
        value, flow = nx.maximum_flow(network, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)
        if value != len(terminals):
            continue
        paths = []
        for _ in terminals:
            positive = nx.DiGraph((u, v) for u in flow for v, amount in flow[u].items() if amount > 0)
            route = nx.shortest_path(positive, source, sink)
            paths.append([center] + [node[0] for node in route[1:-1] if node[1] == 1])
            for u, v in zip(route, route[1:]):
                flow[u][v] -= 1
        return {'center': center, 'paths': paths}
    raise AssertionError(pattern)


if __name__ == '__main__':
    result = {}
    for length in range(1, 5):
        for symbols in itertools.product('BTX', repeat=length):
            if 2 <= sum(2 if x == 'X' else 1 for x in symbols) <= 4:
                pattern = ''.join(symbols)
                result[pattern] = template(pattern)
    (Path(__file__).parent / 'templates.json').write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
    print('templates synthesized:', len(result))
