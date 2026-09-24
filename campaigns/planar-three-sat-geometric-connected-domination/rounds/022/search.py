"""Target-only bounded connected pruning; unsuccessful search is not a NO answer."""
import json
import random
import sys
from pathlib import Path
import networkx as nx

WORK = Path(__file__).parents[2] / 'work'
sys.path.insert(0, str(WORK))
import check


def search(graph, budget, seed, steps):
    rng = random.Random(seed)
    closed = {v: set(graph[v]) | {v} for v in graph}
    selected = set(graph)
    best = set(selected)
    for step in range(steps + 1):
        counts = {v: len(closed[v] & selected) for v in graph}
        while True:
            articulation = set(nx.articulation_points(graph.subgraph(selected)))
            removable = [v for v in selected - articulation if all(counts[u] > 1 for u in closed[v])]
            if not removable:
                break
            v = rng.choice(removable)
            selected.remove(v)
            for u in closed[v]:
                counts[u] -= 1
        if len(selected) < len(best):
            best = set(selected)
            print('best', seed, step, len(best), flush=True)
        if len(best) <= budget:
            return sorted(best)
        if step % 20 == 0:
            selected = set(best)
        for _ in range(1 + step % 4):
            boundary = {u for v in selected for u in graph[v]} - selected
            if boundary:
                selected.add(rng.choice(sorted(boundary)))
    return None


if __name__ == '__main__':
    for n in range(3, 9):
        graph = nx.path_graph(n)
        answer = search(graph, n - 2, 0, 0)
        assert len(answer) == n - 2 and nx.is_connected(graph.subgraph(answer))
        assert all(v in answer or set(graph[v]) & set(answer) for v in graph)
    cases = json.loads((WORK / 'cases.json').read_text())
    source = cases[1]['source']
    target = check.run_candidate(WORK / 'algorithm.py', [], source)
    graph, budget = check.target_graph(target)
    print('target', len(graph), budget, flush=True)
    for seed in range(4):
        answer = search(graph, budget, seed, 300)
        if answer is not None:
            assert check.target_witness_valid(target, answer)
            recovered = check.run_candidate(WORK / 'algorithm.py', ['--extract'], {'source': source, 'target_solution': answer})
            assert check.source_witness_valid(source, recovered)
            (Path(__file__).parent / 'witness.json').write_text(json.dumps({'source': source, 'target_solution': answer, 'recovered': recovered}))
            print('independent witness decoded', len(answer), recovered, flush=True)
            break
    else:
        print('finite heuristic exhausted; target answer unknown', flush=True)
