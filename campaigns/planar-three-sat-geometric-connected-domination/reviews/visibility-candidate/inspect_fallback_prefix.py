"""Audit a real public F prefix using Python tracing, without candidate imports.

Stops before point expansion; this is not an end-to-end target check.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
probe = HERE / 'prefix_probe'
probe.mkdir(exist_ok=True)
(probe / 'sitecustomize.py').write_text('''import json, os, sys
from pathlib import Path

def audit(frame, event, arg):
    if event == "return" and frame.f_code.co_name == "checked_layout" and frame.f_code.co_filename.endswith("/rounds/010/drawing.py"):
        drawn, positions = arg
        record = {"core_nodes": len(frame.f_locals["core"]), "positions": sorted((repr(k), v) for k,v in positions.items()), "route_length": sum(abs(positions[u][0]-positions[v][0])+abs(positions[u][1]-positions[v][1]) for u,v in drawn.edges)}
        Path(os.environ["REVIEW_PREFIX_OUTPUT"]).write_text(json.dumps(record))
        os._exit(0)
    return audit
sys.settrace(audit)
''')
source = json.loads((HERE / 'fallback-source.json').read_text())
records = []
for seed in ('1', '2'):
    path = HERE / f'fallback-prefix-{seed}.json'
    env = {**os.environ, 'PYTHONHASHSEED': seed, 'PYTHONPATH': str(probe), 'PYTHONDONTWRITEBYTECODE': '1', 'REVIEW_PREFIX_OUTPUT': str(path)}
    result = subprocess.run([sys.executable, '-B', str(CAMPAIGN / 'work/algorithm.py')], input=json.dumps(source), text=True, capture_output=True, env=env, check=True)
    data = json.loads(path.read_text())
    records.append(data)
    print(seed, data['core_nodes'], len(data['positions']), flush=True)
print('identical_layout:', records[0] == records[1], flush=True)
assert records[0] == records[1], 'F fallback layout varies across hash seeds'
