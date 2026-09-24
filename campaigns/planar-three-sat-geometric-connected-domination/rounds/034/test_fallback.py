"""Real operation exhaustion must produce a valid fallback, with no mocks."""
import importlib.util
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('drawing', ROOT / 'rounds/010/drawing.py')
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)
graphs = [nx.cycle_graph(4), nx.cubical_graph(), nx.octahedral_graph()]
source = json.loads((ROOT / 'work/cases.json').read_text())[1]['source']
graph, bound = drawing.bridge.cover_instance(source)
graph, *_ = drawing.bridge.connected_cover_instance(graph, bound)
graph.remove_nodes_from([v for v in graph if v[0] == 'leaf'])
graphs.append(graph)
for graph in graphs:
    result, pos = drawing.checked_layout(graph, operation_budget=0)
    drawing.validate_layout(graph, result, pos)
print('forced fallback layouts checked:', len(graphs))
