"""Validate real exact-flow drawings, not agreement with a chosen coordinate set."""
import importlib.util
import json
from pathlib import Path
import networkx as nx
from exact_drawing import layout

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('drawing', ROOT / 'rounds/010/drawing.py')
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)
graphs = [nx.cycle_graph(4), nx.cubical_graph(), nx.octahedral_graph()]
for case in json.loads((ROOT / 'work/cases.json').read_text())[:12]:
    graph, bound = drawing.bridge.cover_instance(case['source'])
    graph, *_ = drawing.bridge.connected_cover_instance(graph, bound)
    graph.remove_nodes_from([v for v in graph if v[0] == 'leaf'])
    if graph:
        graphs.append(graph)
for i, graph in enumerate(graphs):
    result, positions = layout(graph)
    drawing.validate_layout(graph, result, positions)
    print(i, len(graph), len(result), max(max(abs(x), abs(y)) for x, y in positions.values()), flush=True)
print('exact-flow layouts validated:', len(graphs))
