"""Exact connected domination from graph-only separator states."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
import networkx as nx


def put(table, state, value, bound):
    if value[0] <= bound and (state not in table or value[0] < table[state][0]):
        table[state] = value


def union_partition(parts):
    result = []
    for component in parts:
        other = []
        for prior in result:
            if prior & component:
                component |= prior
            else:
                other.append(prior)
        result = other + [component]
    return tuple(sorted(result))


def solve_root(graph, tree, root, bound, forced):
    bit = {v: 1 << v for v in graph}
    neighbors = {v: sum(bit[u] for u in graph[v]) for v in graph}
    start = next(iter(tree))
    order = list(nx.dfs_preorder_nodes(tree, start))
    parent = {v: u for u, v in nx.bfs_edges(tree, start)}
    tables = {}
    peak = 0

    def move(table, old, new):
        bag = set(old)
        for v in sorted(old - new):
            updated = {}
            for (dominated, parts), value in table.items():
                if not dominated & bit[v] or bit[v] in parts:
                    continue
                state = (dominated & ~bit[v], tuple(sorted(p & ~bit[v] for p in parts)))
                put(updated, state, value, bound)
            table = updated
            bag.remove(v)
        for v in sorted(new - old):
            updated = {}
            bag.add(v)
            adjacent = neighbors[v] & sum(bit[u] for u in bag)
            for (dominated, parts), (cost, witness) in table.items():
                selected = sum(parts)
                if v not in forced:
                    put(updated, (dominated | (bit[v] if adjacent & selected else 0), parts), (cost, witness), bound)
                merged = bit[v]
                separate = []
                for part in parts:
                    if part & adjacent:
                        merged |= part
                    else:
                        separate.append(part)
                state = (dominated | adjacent | bit[v], tuple(sorted(separate + [merged])))
                put(updated, state, (cost + 1, witness | bit[v]), bound)
            table = updated
        return table

    for index, node in enumerate(reversed(order)):
        bag = set(node) | {root}
        current = move({(bit[root], (bit[root],)): (1, bit[root])}, {root}, bag)
        for child in tree[node]:
            if parent.get(child) != node:
                continue
            incoming = move(tables.pop(child), set(child) | {root}, bag)
            groups = {}
            for (dom, parts), value in incoming.items():
                groups.setdefault(sum(parts), []).append((dom, parts, value))
            joined = {}
            for (dom, parts), (cost, witness) in current.items():
                selected = sum(parts)
                for dom2, parts2, (cost2, witness2) in groups.get(selected, ()):
                    total = cost + cost2 - selected.bit_count()
                    if total <= bound:
                        state = (dom | dom2, union_partition(parts + parts2))
                        put(joined, state, (total, witness | witness2), bound)
            current = joined
        tables[node] = current
        peak = max(peak, len(current))
    final = move(tables[start], set(start) | {root}, {root})
    value = final.get((bit[root], (bit[root],)))
    return value, peak


def solve_graph(graph, bound=None, verbose=False):
    if not graph or not nx.is_connected(graph):
        return None
    assert set(graph) == set(range(len(graph)))
    bound = len(graph) if bound is None else bound
    if bound < 1:
        return None
    width, tree = nx.approximation.treewidth_min_fill_in(graph)
    articulations = list(nx.articulation_points(graph))
    if articulations:
        roots = [articulations[0]]
    else:
        v = min(graph, key=graph.degree)
        roots = [v, *graph[v]]
    best = None
    for root in roots:
        result, peak = solve_root(graph, tree, root, bound, set(articulations))
        if verbose:
            print('width', width, 'root', root, 'peak states', peak, 'optimum', None if result is None else result[0], flush=True)
        if result is not None and (best is None or result[0] < best[0]):
            best = result
            bound = result[0]
    return None if best is None else [v for v in graph if best[1] & (1 << v)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=1)
    args = parser.parse_args()
    campaign = Path(__file__).parents[2]
    sys.path.insert(0, str(campaign / 'work'))
    import verify
    spec = importlib.util.spec_from_file_location('decompose', campaign / 'rounds/023/decompose.py')
    decompose = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decompose)
    source = json.loads((campaign / 'work/cases.json').read_text())[args.case]['source']
    target = verify.candidate_call(campaign / 'work/algorithm.py', False, source)
    graph = decompose.graph_from_target(target)
    print('target vertices', len(graph), 'budget', target['K'], flush=True)
    answer = solve_graph(graph, target['K'], verbose=True)
    if answer is None:
        answer = 'NO-SOLUTION'
        assert not verify.source_has_witness(source)
    else:
        assert len(answer) <= target['K'] and nx.is_connected(graph.subgraph(answer))
        assert all(v in answer or set(graph[v]) & set(answer) for v in graph)
    recovered = verify.candidate_call(campaign / 'work/algorithm.py', True, {'source': source, 'target_solution': answer})
    assert (recovered == 'NO-SOLUTION' and not verify.source_has_witness(source)) or verify.satisfies(source, recovered)
    (Path(__file__).parent / f'witness-{args.case}.json').write_text(json.dumps({'source': source, 'target_solution': answer, 'recovered': recovered}))
    print('independent exact target answer decoded', recovered, flush=True)
