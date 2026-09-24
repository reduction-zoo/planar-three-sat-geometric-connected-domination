"""Check orthogonal drawings returned for the connected-cover cores."""

import importlib.util
import json
import sys
from pathlib import Path

import networkx as nx
from tsmpy import TSM


ROOT = Path(__file__).parents[2]
spec = importlib.util.spec_from_file_location("bridge", ROOT / "rounds/009/bridge.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


def validate_layout(core, drawn, pos):
    assert set(core) <= set(drawn)
    assert len(set(pos.values())) == len(pos)
    occupancy = {}
    for u, v in drawn.edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        assert x1 == x2 or y1 == y2
        assert (x1, y1) != (x2, y2)
        steps = max(abs(x2 - x1), abs(y2 - y1))
        for i in range(steps + 1):
            point = (x1 + (x2 - x1) * i // steps, y1 + (y2 - y1) * i // steps)
            if point in occupancy:
                prior_u, prior_v = occupancy[point]
                assert point in (pos[u], pos[v]) and point in (pos[prior_u], pos[prior_v])
                assert {u, v} & {prior_u, prior_v}
            occupancy[point] = (u, v)
    bends = set(drawn) - set(core)
    assert all(drawn.degree(v) == 2 for v in bends)
    reduced = drawn.copy()
    for v in bends:
        a, b = tuple(reduced.neighbors(v))
        reduced.add_edge(a, b)
        reduced.remove_node(v)
    assert set(map(frozenset, reduced.edges)) == set(map(frozenset, core.edges))
    return drawn, pos


def checked_layout(core, operation_budget=50_000_000):
    # A deterministic bounded attempt preserves compact layouts; visibility is total.
    if len(core) <= 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))
        remaining = operation_budget
        previous_trace = sys.gettrace()
        def count_lines(frame, event, arg):
            nonlocal remaining
            if event == "line":
                remaining -= 1
                if remaining < 0:
                    raise RuntimeError("compact layout operation allowance exhausted")
            return count_lines
        layout = None
        try:
            sys.settrace(count_lines)
            layout = TSM(core, uselp=False)
        except Exception:
            pass
        finally:
            sys.settrace(previous_trace)
        if layout is not None:
            try:
                assert len(layout.G) <= 100 * len(core)
                assert set(layout.pos) == set(layout.G)
                assert all(type(x) is int and abs(x) <= 100 * len(core) for p in layout.pos.values() for x in p)
                return validate_layout(core, layout.G, layout.pos)
            except Exception:
                pass
    spec = importlib.util.spec_from_file_location("visibility_layout", ROOT / "rounds/033/layout.py")
    fallback = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fallback)
    drawn, pos = fallback.layout(core)
    return validate_layout(core, drawn, pos)


if __name__ == "__main__":
    cases = json.loads((ROOT / "work/cases.json").read_text())
    largest = (0, 0, 0, 0)
    for i, case in enumerate(cases):
        graph, bound = bridge.cover_instance(case["source"])
        connected, _, _, _ = bridge.connected_cover_instance(graph, bound)
        core = connected.copy()
        core.remove_nodes_from(v for v in connected if v[0] == "leaf")
        if not core:
            continue
        assert nx.is_biconnected(core), i
        drawn, pos = checked_layout(core)
        length = sum(abs(pos[u][0] - pos[v][0]) + abs(pos[u][1] - pos[v][1]) for u, v in drawn.edges)
        largest = tuple(max(a, b) for a, b in zip(largest, (len(core), len(drawn), length, max(max(abs(x), abs(y)) for x, y in pos.values()))))
    print(f"{len(cases) - 1} nonempty biconnected cores: max original/drawn nodes, total route length, coordinate magnitude = {largest}")
