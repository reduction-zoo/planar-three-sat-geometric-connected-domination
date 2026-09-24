"""New clause-bearing public F/independent target solver/G check across seeds."""
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
source = {'variables': 2, 'clauses': [[1,2,2],[-1,-2,-2]], 'embedding': {'v0':['c0','c1'], 'v1':['c0','c1'], 'c0':['v0','v1'], 'c1':['v0','v1']}}
sys.path.insert(0, str(CAMPAIGN/'work'))
spec = importlib.util.spec_from_file_location('review_oracle', CAMPAIGN/'work/check.py')
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
assert oracle.valid_source(source)
valid_assignments = [list(a) for a in itertools.product((False,True), repeat=2) if all(any(a[abs(l)-1] == (l>0) for l in c) for c in source['clauses'])]
assert len(valid_assignments) == 2

def run(payload, seed, extract=False):
    return subprocess.run([sys.executable,'-B',str(CAMPAIGN/'work/algorithm.py'), *(['--extract'] if extract else [])], input=json.dumps(payload), text=True, capture_output=True, check=True, env={**os.environ,'PYTHONHASHSEED':str(seed),'PYTHONDONTWRITEBYTECODE':'1'}).stdout

outputs = [run(source,seed) for seed in (7,99)]
assert outputs[0] == outputs[1]
target = json.loads(outputs[0])
answer = oracle.target_answer(target)
assert answer != 'NO-SOLUTION' and oracle.target_witness_valid(target, answer)
recovered = [json.loads(run({'source':source,'target_solution':answer},seed,True)) for seed in (123,456)]
assert all(a in valid_assignments for a in recovered)
record = {'source':source,'points':len(target['points']),'K':target['K'],'selected':len(answer),'target_sha256':hashlib.sha256(outputs[0].encode()).hexdigest(),'F_seeds':[7,99],'G_seeds':[123,456],'recovered':recovered}
(HERE/'recovery.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
