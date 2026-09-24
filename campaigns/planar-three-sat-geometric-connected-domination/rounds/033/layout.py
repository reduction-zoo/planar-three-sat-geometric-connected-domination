"""Polynomial integer orthogonal drawing from visibility and finite strip templates."""
import importlib.util
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('visibility', ROOT / 'rounds/030/visibility.py')
visibility = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visibility)
TEMPLATES = json.loads((ROOT / 'rounds/032/templates.json').read_text())


def layout(graph):
    bars, edges = visibility.bars(graph)
    positions = {}
    local = {}
    for v, (_, _, height) in bars.items():
        incident = [(edge, column, 4 if low == height else -4) for edge, (column, low, high) in edges.items() if v in edge]
        columns = sorted({column for _, column, _ in incident})
        sides = {column: {side for _, col, side in incident if col == column} for column in columns}
        pattern = ''.join('X' if len(sides[col]) == 2 else 'T' if 4 in sides[col] else 'B' for col in columns)
        certificate = TEMPLATES[pattern]
        xmap = {2 * i + 1: 20 * col for i, col in enumerate(columns)}
        xmap[0], xmap[2 * len(columns)] = 20 * columns[0] - 4, 20 * columns[-1] + 4
        for i in range(1, len(columns)):
            xmap[2 * i] = 10 * (columns[i - 1] + columns[i])
        def transform(point):
            return (xmap[point[0]], 20 * height + point[1])
        positions[v] = transform(certificate['center'])
        by_terminal = {tuple(path[-1]): path for path in certificate['paths']}
        for edge, col, side in incident:
            terminal = (2 * columns.index(col) + 1, side)
            local[v, edge] = list(map(transform, by_terminal[terminal]))
    drawn = nx.Graph()
    drawn.add_nodes_from(graph)
    serial = 0
    for edge in edges:
        u, v = edge
        route = local[u, edge] + list(reversed(local[v, edge]))
        compact = []
        for point in route:
            while len(compact) >= 2 and (compact[-2][0] == compact[-1][0] == point[0] or compact[-2][1] == compact[-1][1] == point[1]):
                compact.pop()
            compact.append(point)
        chain = [u]
        for point in compact[1:-1]:
            node = ('visibility-bend', serial)
            while node in drawn:
                serial += 1
                node = ('visibility-bend', serial)
            serial += 1
            drawn.add_node(node)
            positions[node] = point
            chain.append(node)
        chain.append(v)
        drawn.add_edges_from(zip(chain, chain[1:]))
    return drawn, positions
