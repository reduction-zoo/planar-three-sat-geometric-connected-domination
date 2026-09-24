"""Independent target-only witness search; None means unknown, never NO-SOLUTION."""
import json
import sys
from pathlib import Path
import networkx as nx
import z3


def graph_from_points(points):
    lookup = {tuple(p): i for i, p in enumerate(points)}
    assert len(lookup) == len(points) and all(type(x) is int for p in points for x in p)
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for (x, y), i in lookup.items():
        for near in ((x + 1, y), (x, y + 1)):
            if near in lookup:
                graph.add_edge(i, lookup[near])
    return graph


def find_witness(target, forbidden=()):
    if not all(type(x) is int for p in target['points'] for x in p):
        return None
    graph = graph_from_points(target['points'])
    allowed = {i for i, (x, y) in enumerate(target['points']) if x % 10 == 0 or y % 10 == 0}
    if not allowed or target['K'] < 1 or not nx.is_connected(graph):
        return None
    chosen = {i: z3.Bool(f'lattice_{i}') for i in sorted(allowed)}
    solver = z3.Solver()
    solver.add(z3.PbLe([(v, 1) for v in chosen.values()], target['K']))
    for v in graph:
        solver.add(z3.Or(*(chosen[u] for u in ({v} | set(graph[v])) & allowed)))
    for v in nx.articulation_points(graph):
        if v not in allowed:
            return None
        solver.add(chosen[v])
    for answer in forbidden:
        previous = set(answer)
        solver.add(z3.Or(*(var != (i in previous) for i, var in chosen.items())))
    while solver.check() == z3.sat:
        model = solver.model()
        selected = {i for i, var in chosen.items() if z3.is_true(model.eval(var))}
        components = list(nx.connected_components(graph.subgraph(selected)))
        if len(components) == 1:
            assert len(selected) <= target['K']
            assert all(v in selected or set(graph[v]) & selected for v in graph)
            return sorted(selected)
        for component in components:
            boundary = {u for v in component for u in graph[v]} - component
            solver.add(z3.Or(*(z3.Not(chosen[v]) for v in component), *(chosen[v] for v in boundary & allowed)))
    return None


if __name__ == '__main__':
    work = Path(__file__).parents[2] / 'work'
    sys.path.insert(0, str(work))
    import verify
    source = json.loads((work / 'cases.json').read_text())[2]['source']
    target = verify.candidate_call(work / 'algorithm.py', False, source)
    print('target', len(target['points']), target['K'], flush=True)
    answer = find_witness(target)
    assert answer is not None, 'restricted search inconclusive'
    recovered = verify.candidate_call(work / 'algorithm.py', True, {'source': source, 'target_solution': answer})
    assert verify.satisfies(source, recovered)
    (Path(__file__).parent / 'witness.json').write_text(json.dumps({'source': source, 'target_solution': answer, 'recovered': recovered}))
    print('independent clause-bearing target witness decoded', len(answer), recovered, flush=True)
