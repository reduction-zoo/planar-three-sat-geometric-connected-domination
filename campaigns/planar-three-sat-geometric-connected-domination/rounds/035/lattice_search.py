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
    if len(allowed) > 2:
        allowed -= {v for v, degree in graph.subgraph(allowed).degree if degree == 1}
    neighborhoods = [({v} | set(graph[v])) & allowed for v in graph]
    if any(not neighborhood for neighborhood in neighborhoods):
        return None
    forced = set(nx.articulation_points(graph))
    forced.update(next(iter(neighborhood)) for neighborhood in neighborhoods if len(neighborhood) == 1)
    if not forced <= allowed or len(forced) > target['K']:
        return None
    optional = allowed - forced
    chosen = {i: z3.Bool(f'lattice_{i}') for i in sorted(optional)}
    solver = z3.Solver()
    if chosen:
        solver.add(z3.PbLe([(v, 1) for v in chosen.values()], target['K'] - len(forced)))
    for neighborhood in neighborhoods:
        if not neighborhood & forced:
            solver.add(z3.Or(*(chosen[u] for u in neighborhood)))
    for answer in forbidden:
        previous = set(answer)
        if previous <= allowed:
            solver.add(z3.Or(*(var != (i in previous) for i, var in chosen.items())))
    groups = list(nx.connected_components(graph.subgraph(forced))) + [{v} for v in sorted(optional)]
    owner = {v: i for i, group in enumerate(groups) for v in group}
    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(groups)))
    quotient.add_edges_from((owner[u], owner[v]) for u, v in graph.subgraph(allowed).edges if owner[u] != owner[v])
    selected_q = {i: z3.BoolVal(True) if group & forced else chosen[next(iter(group))] for i, group in enumerate(groups)}
    rank = {i: z3.Int(f'rank_{i}') for i in quotient}
    root = {i: z3.Bool(f'root_{i}') for i in quotient}
    solver.add(z3.PbEq([(value, 1) for value in root.values()], 1))
    if forced:
        solver.add(root[0])
    for i in quotient:
        solver.add(rank[i] >= 0, rank[i] < len(quotient))
        solver.add(z3.Implies(root[i], z3.And(selected_q[i], rank[i] == 0)))
        solver.add(z3.Implies(z3.And(selected_q[i], z3.Not(root[i])),
                             z3.Or(*(z3.And(selected_q[j], rank[j] < rank[i]) for j in quotient[i]))))
    status = solver.check()
    if status != z3.sat:
        return None
    model = solver.model()
    selected = forced | {i for i, var in chosen.items() if z3.is_true(model.eval(var))}
    assert len(selected) <= target['K'] and nx.is_connected(graph.subgraph(selected))
    assert all(v in selected or set(graph[v]) & selected for v in graph)
    return sorted(selected)


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
