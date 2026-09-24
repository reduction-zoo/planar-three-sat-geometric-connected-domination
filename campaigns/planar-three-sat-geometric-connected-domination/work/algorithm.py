"""Planar 3-SAT to integer-point connected domination, with witness recovery."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


CAMPAIGN = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("decoder", CAMPAIGN / "rounds/012/decode.py")
decoder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decoder)
grid = decoder.grid
bridge = grid.drawing.bridge


def unit_contradiction(clauses):
    assignment = {}
    simplified = []
    for clause in clauses:
        literals = set(clause)
        if not any(-lit in literals for lit in literals):
            simplified.append(literals)
    while True:
        units = []
        for clause in simplified:
            if any(assignment.get(abs(lit)) == (lit > 0) for lit in clause):
                continue
            remaining = [lit for lit in clause if abs(lit) not in assignment]
            if not remaining:
                return True
            if len(remaining) == 1:
                units.append(remaining[0])
        if not units:
            return False
        for lit in units:
            variable, value = abs(lit), lit > 0
            if variable in assignment and assignment[variable] != value:
                return True
            assignment[variable] = value


def construction(source):
    if unit_contradiction(source["clauses"]):
        return {"points": [[0, 0]], "K": 0}, None
    graph, bound = bridge.cover_instance(source)
    connected, cover_bound, subdivisions, _ = bridge.connected_cover_instance(graph, bound)
    if not connected:
        return {"points": [[0, 0]], "K": 1}, None
    points, original, internal, middle, sides, routes = grid.place(connected)
    budget = cover_bound + len(internal) - len(routes) + len(connected) - 1
    target = {"points": [list(point) for point in points], "K": budget}
    return target, (graph, bound, connected, cover_bound, subdivisions, points, original, sides, routes)


def extract(source, answer):
    if answer == "NO-SOLUTION":
        return answer
    target, data = construction(source)
    if data is None:
        return []
    graph, _, connected, cover_bound, subdivisions, points, original, sides, routes = data
    selected = {points[index] for index in answer}
    connected_cover = decoder.recover_connected_cover(connected, points, selected, original, sides, routes, cover_bound)
    planar_cover = bridge.recover_cover(graph, connected_cover, subdivisions)
    return bridge.recover_assignment(source, planar_cover)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", action="store_true")
    args = parser.parse_args()
    payload = json.load(sys.stdin)
    result = extract(payload["source"], payload["target_solution"]) if args.extract else construction(payload)[0]
    json.dump(result, sys.stdout, separators=(",", ":"))
