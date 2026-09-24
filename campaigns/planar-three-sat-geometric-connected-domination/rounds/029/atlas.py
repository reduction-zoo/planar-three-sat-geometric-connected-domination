"""Test the proposed biconnected drawing domain with exact geometric checks."""
import importlib.util
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).parents[2]
modules = {}
for name, path in [('exact_drawing', '027/exact_drawing.py'), ('drawing', '010/drawing.py')]:
    spec = importlib.util.spec_from_file_location(name, ROOT / 'rounds' / path)
    modules[name] = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modules[name])
count = 0
for index, graph in enumerate(nx.graph_atlas_g()):
    if len(graph) < 3 or not nx.is_biconnected(graph) or max(dict(graph.degree).values()) > 4 or not nx.check_planarity(graph)[0]:
        continue
    try:
        result, pos = modules['exact_drawing'].layout(graph)
        modules['drawing'].validate_layout(graph, result, pos)
    except Exception:
        (Path(__file__).parent / 'failure.json').write_text(json.dumps({'atlas_index': index, 'edges': list(graph.edges)}))
        raise
    count += 1
print('all admitted graph-atlas layouts validated:', count)
