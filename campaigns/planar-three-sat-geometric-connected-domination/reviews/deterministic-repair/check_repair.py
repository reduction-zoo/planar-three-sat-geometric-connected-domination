"""Cross-seed public F prefix regression; imports no candidate implementation."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
source = json.loads((HERE.parent / 'visibility-candidate/fallback-source.json').read_text())
assert source['clauses'] == [[i,i+1,-(i+1)] for i in range(1,15)]
records = []
for seed in ('7', '99'):
    output = HERE / f'prefix-{seed}.json'
    env = {**os.environ, 'PYTHONHASHSEED': seed, 'PYTHONPATH': str(HERE / 'probe'), 'PYTHONDONTWRITEBYTECODE': '1', 'REVIEW_OUTPUT': str(output)}
    subprocess.run([sys.executable, '-B', str(CAMPAIGN / 'work/algorithm.py')], input=json.dumps(source), text=True, capture_output=True, env=env, check=True)
    record = json.loads(output.read_text())
    records.append(record)
    print(seed, record, flush=True)
assert records[0] == records[1], records
print('PASS: original asymmetric source has identical accepted layouts under new seeds 7 and 99')
