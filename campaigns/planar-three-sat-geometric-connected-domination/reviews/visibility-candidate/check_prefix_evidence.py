"""Independently validate source legality and quantify recorded layout differences."""
import json
from pathlib import Path
import networkx as nx

HERE = Path(__file__).resolve().parent
source = json.loads((HERE / 'fallback-source.json').read_text())
n = source['variables']
assert n == 15 and source['clauses'] == [[i, i+1, -(i+1)] for i in range(1, n)]
incidence = nx.Graph()
incidence.add_nodes_from(f'v{i}' for i in range(n))
for i, clause in enumerate(source['clauses']):
    incidence.add_edges_from((f'c{i}', f'v{abs(lit)-1}') for lit in clause)
assert set(source['embedding']) == set(incidence)
assert all(set(source['embedding'][v]) == set(incidence[v]) for v in incidence)
embedding = nx.PlanarEmbedding()
embedding.set_data(source['embedding'])
embedding.check_structure()
assert all(any(lit < 0 for lit in clause) for clause in source['clauses'])  # all-false witness
records = [json.loads((HERE / f'fallback-prefix-{seed}.json').read_text()) for seed in (1, 2)]
a, b = [dict(record['positions']) for record in records]
assert set(a) == set(b)
lengths = [r['route_length'] for r in records]
summary = {'source_legal': True, 'source_satisfiable': True, 'core_sizes': [r['core_nodes'] for r in records], 'changed_positions': sum(a[k] != b[k] for k in a), 'route_lengths': lengths, 'implied_K_difference': 10 * (lengths[1] - lengths[0])}
print(json.dumps(summary, indent=2))
assert lengths[0] != lengths[1], 'recorded nondeterminism no longer reproduced'
