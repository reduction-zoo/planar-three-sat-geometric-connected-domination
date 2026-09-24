"""Check exactness of the degree-two cover fold on small independent graphs."""

import json
import subprocess
import sys
from pathlib import Path

import networkx as nx

from certify_negative import exact_cover_size, fold_degree_two, skeleton_from_target


checked = 0
for graph in nx.graph_atlas_g():
    if len(graph) > 6:
        continue
    residual, cost, _ = fold_degree_two(graph)
    assert exact_cover_size(graph) == cost + exact_cover_size(residual)
    checked += 1
print(f"degree-two cover fold exact on {checked} graph-atlas graphs through six vertices")

campaign = Path(__file__).resolve().parents[2]
source = json.loads((campaign / "work/cases.json").read_text())[1]["source"]
target = json.loads(subprocess.run([sys.executable, str(campaign / "work/algorithm.py")],
                                   input=json.dumps(source), text=True, capture_output=True, check=True).stdout)
_, skeleton, budget, _, _ = skeleton_from_target(target)
forced = set(nx.articulation_points(skeleton))
residual, cost, _ = fold_degree_two(skeleton.subgraph(set(skeleton) - forced))
assert len(forced) + cost + exact_cover_size(residual) <= budget
print("positive geometric control passes the same structural certificate parser")
