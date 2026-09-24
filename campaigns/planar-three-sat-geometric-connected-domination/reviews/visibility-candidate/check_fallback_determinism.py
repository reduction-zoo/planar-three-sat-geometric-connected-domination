"""Public F determinism for a legal source exceeding the compact drawing limit."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
source = {'variables': 30, 'clauses': [], 'embedding': {f'v{i}': [] for i in range(30)}}
(HERE / 'isolates-source.json').write_text(json.dumps(source))
records = []
for seed in ('1', '2'):
    result = subprocess.run([sys.executable, '-B', str(CAMPAIGN / 'work/algorithm.py')], input=json.dumps(source), text=True, capture_output=True, env={**os.environ, 'PYTHONHASHSEED': seed, 'PYTHONDONTWRITEBYTECODE': '1'})
    (HERE / f'isolates-{seed}.stderr').write_text(result.stderr)
    target = json.loads(result.stdout) if result.returncode == 0 else None
    if target:
        (HERE / f'isolates-target-{seed}.json').write_text(result.stdout)
    record = {'seed': seed, 'exit': result.returncode, 'points': len(target['points']) if target else None, 'K': target['K'] if target else None, 'sha256': hashlib.sha256(result.stdout.encode()).hexdigest()}
    records.append(record)
    print(record, flush=True)
(HERE / 'isolates-determinism.json').write_text(json.dumps(records, indent=2)+'\n')
assert all(r['exit'] == 0 for r in records)
assert len({r['sha256'] for r in records}) == 1, 'F varies across hash seeds'
