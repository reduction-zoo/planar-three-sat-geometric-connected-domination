"""Structured legal-source stress cases for the orthogonal drawing interface."""

import importlib.util
import sys
from pathlib import Path

import networkx as nx


CAMPAIGN = Path(__file__).parents[2]
sys.path.insert(0, str(CAMPAIGN / "work"))
import check  # noqa: E402

spec = importlib.util.spec_from_file_location("drawing", CAMPAIGN / "rounds/010/drawing.py")
drawing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drawing)


def isolated(n):
    return {"variables": n, "clauses": [], "embedding": {f"v{i}": [] for i in range(n)}}


def star(m):
    clauses = [[1 if i % 2 == 0 else -1] * 3 for i in range(m)]
    rotation = {"v0": [f"c{i}" for i in range(m)]}
    rotation.update({f"c{i}": ["v0"] for i in range(m)})
    return {"variables": 1, "clauses": clauses, "embedding": rotation}


def chain(m, cycle=False):
    n = m if cycle else m + 1
    clauses = [[i + 1, -((i + 1) % n + 1), i + 1] for i in range(m)]
    rotation = {f"v{i}": [] for i in range(n)}
    for i in range(m):
        a, b = i, (i + 1) % n
        rotation[f"v{a}"].append(f"c{i}")
        rotation[f"v{b}"].append(f"c{i}")
        rotation[f"c{i}"] = [f"v{a}", f"v{b}"]
    return {"variables": n, "clauses": clauses, "embedding": rotation}


def tree(m):
    n = 2 * m + 1
    clauses = []
    rotation = {f"v{i}": [] for i in range(n)}
    for i in range(m):
        variables = (i, 2 * i + 1, 2 * i + 2)
        clauses.append([variables[0] + 1, variables[1] + 1, -(variables[2] + 1)])
        rotation[f"c{i}"] = [f"v{v}" for v in variables]
        for v in variables:
            rotation[f"v{v}"].append(f"c{i}")
    return {"variables": n, "clauses": clauses, "embedding": rotation}


if __name__ == "__main__":
    families = [("isolated", n, isolated(n)) for n in (1, 2, 5, 10, 20)]
    families += [("star", m, star(m)) for m in (1, 2, 5, 10, 20)]
    families += [("chain", m, chain(m)) for m in (1, 2, 5, 10, 20)]
    families += [("cycle", m, chain(m, True)) for m in (3, 5, 10, 20)]
    families += [("tree", m, tree(m)) for m in (1, 2, 5, 10, 20)]
    largest = (0, 0, 0)
    for family, size, source in families:
        assert check.valid_source(source), (family, size, "invalid source")
        graph, bound = drawing.bridge.cover_instance(source)
        assert nx.check_planarity(graph)[0] and max(d for _, d in graph.degree) <= 3
        connected, _, _, _ = drawing.bridge.connected_cover_instance(graph, bound)
        assert nx.check_planarity(connected)[0] and nx.is_connected(connected)
        assert max(d for _, d in connected.degree) <= 4
        core = connected.copy()
        core.remove_nodes_from(v for v in connected if v[0] == "leaf")
        assert nx.is_biconnected(core), (family, size, "core not biconnected")
        assert not list(nx.bridges(core)), (family, size, "core has bridge")
        drawn, pos = drawing.checked_layout(core)
        length = sum(abs(pos[u][0] - pos[v][0]) + abs(pos[u][1] - pos[v][1]) for u, v in drawn.edges)
        largest = tuple(max(a, b) for a, b in zip(largest, (len(core), len(drawn), length)))
        print(family, size, len(core), len(drawn), length, flush=True)
    print("checked", len(families), "largest core/drawing/length", largest)
