"""Compose actual visibility templates and check the resulting embedded graph."""
import importlib.util
import json
from pathlib import Path
import networkx as nx
from layout import layout

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('drawing', ROOT / 'rounds/010/drawing.py')
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)
graphs = [g for g in nx.graph_atlas_g() if len(g) >= 3 and nx.is_biconnected(g) and max(dict(g.degree).values()) <= 4 and nx.check_planarity(g)[0]]
for case in json.loads((ROOT / 'work/cases.json').read_text())[:12]:
    graph, bound = drawing.bridge.cover_instance(case['source'])
    graph, *_ = drawing.bridge.connected_cover_instance(graph, bound)
    graph.remove_nodes_from([v for v in graph if v[0] == 'leaf'])
    if graph:
        graphs.append(graph)
for graph in graphs:
    result, positions = layout(graph)
    drawing.validate_layout(graph, result, positions)
print('composed orthogonal visibility layouts validated:', len(graphs))
