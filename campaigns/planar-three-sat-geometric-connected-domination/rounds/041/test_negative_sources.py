"""Independent source truth tables and non-shortcut F targets for two UNSAT cases."""

import itertools
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
sys.path.insert(0, str(CAMPAIGN / "work"))
from check import valid_source, target_graph  # independent legality check


def satisfying_assignments(source):
    for values in itertools.product((False, True), repeat=source["variables"]):
        if all(any(values[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in source["clauses"]):
            yield values


for case in json.loads((HERE / "negative_cases.json").read_text()):
    source = case["source"]
    assert valid_source(source), case["id"]
    assert case["expected"] == "NO-SOLUTION"
    assert not list(satisfying_assignments(source)), case["id"]
    assert all(len(set(clause)) == 2 and not any(-lit in clause for lit in clause)
               for clause in source["clauses"]), case["id"]
    outputs = [subprocess.run([sys.executable, str(CAMPAIGN / "work/algorithm.py")],
                              input=json.dumps(source), text=True, capture_output=True, check=True,
                              env={**os.environ, "PYTHONHASHSEED": seed}).stdout
               for seed in ("7", "99")]
    assert outputs[0] == outputs[1], case["id"]
    target = json.loads(outputs[0])
    graph, budget = target_graph(target)
    assert len(graph) > 1 and budget > 0, case["id"]
    print(f"{case['id']}: UNSAT without initial units; {len(graph)} target points, K={budget}", flush=True)
