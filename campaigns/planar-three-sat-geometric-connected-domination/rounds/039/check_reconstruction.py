"""Independent target solve and recovery across process seeds and drawing modes."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).parent
CAMPAIGN = HERE.parents[1]
sys.path.insert(0, str(CAMPAIGN / 'work'))
spec = importlib.util.spec_from_file_location('independent_oracle', CAMPAIGN / 'work/check.py')
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
cases = json.loads((CAMPAIGN / 'work/cases.json').read_text())
records = []
for mode, executable, indices in [('forced-fallback', HERE / 'forced_fallback.py', [1]), ('compact', CAMPAIGN / 'work/algorithm.py', [1, 2, 5])]:
    for index in indices:
        source = cases[index]['source']
        targets = []
        for seed in ('1', '2'):
            result = subprocess.run([sys.executable, str(executable)], input=json.dumps(source), text=True, capture_output=True, check=True, env={**os.environ, 'PYTHONHASHSEED': seed})
            targets.append(result.stdout)
            if mode == 'forced-fallback':
                assert 'actual visibility fallback completed' in result.stderr
        assert targets[0] == targets[1], (mode, index)
        target = json.loads(targets[0])
        print(mode, index, 'target points', len(target['points']), flush=True)
        answer = oracle.target_answer(target)
        assert answer != 'NO-SOLUTION' and oracle.target_witness_valid(target, answer)
        for seed in ('2', '3'):
            result = subprocess.run([sys.executable, str(executable), '--extract'], input=json.dumps({'source': source, 'target_solution': answer}), text=True, capture_output=True, check=True, env={**os.environ, 'PYTHONHASHSEED': seed})
            recovered = json.loads(result.stdout)
            assert oracle.source_witness_valid(source, recovered)
        records.append({'mode': mode, 'case': index, 'points': len(target['points']), 'K': target['K'], 'selected': len(answer), 'target_sha256': hashlib.sha256(targets[0].encode()).hexdigest(), 'F_seeds': [1, 2], 'G_seeds': [2, 3], 'recovered': recovered})
        print(records[-1], flush=True)
(HERE / 'reconstruction.json').write_text(json.dumps(records, indent=2) + '\n')
