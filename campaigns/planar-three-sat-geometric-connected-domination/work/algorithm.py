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


def construction(source):
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
