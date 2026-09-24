"""Ordinary vertex cover with exact degree-zero/one/two reductions."""
import networkx as nx
import z3


def vertex_cover(original, budget):
    if budget < 0:
        return None
    graph = original.copy()
    operations = []
    limit = budget
    serial = max(graph, default=-1) + 1
    while True:
        v = next((v for v, degree in graph.degree if degree <= 2), None)
        if v is None:
            break
        neighbors = list(graph[v])
        if not neighbors:
            graph.remove_node(v)
        elif len(neighbors) == 1:
            u = neighbors[0]
            operations.append(('take', (u,)))
            graph.remove_node(u)
            limit -= 1
        elif graph.has_edge(*neighbors):
            operations.append(('take', tuple(neighbors)))
            graph.remove_nodes_from(neighbors)
            limit -= 2
        else:
            a, b = neighbors
            exterior = (set(graph[a]) | set(graph[b])) - {a, v, b}
            z = serial
            serial += 1
            graph.remove_nodes_from((a, v, b))
            graph.add_node(z)
            graph.add_edges_from((z, u) for u in exterior)
            operations.append(('fold', (z, a, v, b)))
            limit -= 1
        if limit < 0:
            return None
    chosen = set()
    if graph:
        variables = {v: z3.Bool(f'kernel_{v}') for v in graph}
        solver = z3.Solver()
        solver.add(z3.PbLe([(var, 1) for var in variables.values()], limit))
        solver.add(*(z3.Or(variables[u], variables[v]) for u, v in graph.edges))
        if solver.check() != z3.sat:
            return None
        model = solver.model()
        chosen = {v for v, var in variables.items() if z3.is_true(model.eval(var))}
    for kind, data in reversed(operations):
        if kind == 'take':
            chosen.update(data)
        else:
            z, a, v, b = data
            if z in chosen:
                chosen.remove(z)
                chosen.update((a, b))
            else:
                chosen.add(v)
    assert len(chosen) <= budget and all(u in chosen or v in chosen for u, v in original.edges)
    return chosen
