"""Compare public F outputs across fresh processes; no candidate imports."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
CAMPAIGN = ROOT / 'campaigns/planar-three-sat-geometric-connected-domination'
algorithm = CAMPAIGN / 'work/algorithm.py'
cases = json.loads((CAMPAIGN / 'work/cases.json').read_text())
records = []
for index in (1, 2, 5):
    source = cases[index]['source']
    hashes = []
    for seed in ('1', '2', '3'):
        result = subprocess.run([sys.executable, '-B', str(algorithm)], input=json.dumps(source), text=True, capture_output=True, env={**os.environ, 'PYTHONHASHSEED': seed, 'PYTHONDONTWRITEBYTECODE': '1'}, check=True)
        target = json.loads(result.stdout)
        hashes.append(hashlib.sha256(result.stdout.encode()).hexdigest())
        (Path(__file__).parent / f'target-{index}-{seed}.json').write_text(result.stdout)
        records.append({'case': index, 'seed': seed, 'points': len(target['points']), 'K': target['K'], 'sha256': hashes[-1]})
    print(index, len(set(hashes)), flush=True)
(Path(__file__).parent / 'determinism.json').write_text(json.dumps(records, indent=2) + '\n')
assert all(len({r['sha256'] for r in records if r['case'] == i}) == 1 for i in (1, 2, 5)), records
