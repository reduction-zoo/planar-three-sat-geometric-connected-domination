"""Exact lowest ray must survive large integer coordinates and insertion order."""
import importlib.util
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location('exact_drawing', ROOT / 'rounds/027/exact_drawing.py')
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)
Planarization = getattr(drawing, 'ExactPlanarization', drawing.Planarization)
for n in (10, 10**18):
    for order in ((1, 2), (2, 1)):
        graph = nx.Graph([(0, order[0]), (0, order[1]), (1, 2)])
        planar = Planarization(graph)
        position = {0: (0, 0), 1: (n, n), 2: (n + 1, n)}
        expected = planar.dcel.half_edges[0, 2].inc
        assert planar.get_external_face(position) is expected, (n, order)
print('four exact near-parallel ray/order checks passed')
