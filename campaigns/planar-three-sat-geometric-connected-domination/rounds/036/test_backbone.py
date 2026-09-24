"""Returned indices must satisfy the complete actual target graph."""
import importlib.util
import json
import sys
from pathlib import Path
import networkx as nx
from backbone_search import find_witness, graph_from_points

WORK = Path(__file__).parents[2] / 'work'
sys.path.insert(0, str(WORK))
import verify
source = json.loads((WORK / 'cases.json').read_text())[2]['source']
target = verify.candidate_call(WORK / 'algorithm.py', False, source)
print('target', len(target['points']), target['K'], flush=True)
answers = []
for _ in range(2):
    answer = find_witness(target, answers)
    assert answer is not None
    assert answer not in answers
    graph = graph_from_points(target['points'])
    assert len(answer) <= target['K'] and nx.is_connected(graph.subgraph(answer))
    assert all(v in answer or set(graph[v]) & set(answer) for v in graph)
    recovered = verify.candidate_call(WORK / 'algorithm.py', True, {'source': source, 'target_solution': answer})
    assert verify.satisfies(source, recovered)
    answers.append(answer)
    print('independent target witness decoded', len(answer), recovered, flush=True)
(Path(__file__).parent / 'witnesses.json').write_text(json.dumps({'source': source, 'target_solutions': answers}))
