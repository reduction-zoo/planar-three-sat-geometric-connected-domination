"""Test launcher: use the real compact algorithm with its allowance set to zero."""
import json
from pathlib import Path
import runpy
import sys

candidate = Path(__file__).parents[2] / 'work/algorithm.py'
namespace = runpy.run_path(str(candidate))
drawing = namespace['grid'].drawing
drawing.checked_layout.__defaults__ = (0,)
seen = False

def observe(frame, event, arg):
    global seen
    if event == 'return' and frame.f_code.co_name == 'layout' and frame.f_code.co_filename.endswith('/rounds/033/layout.py'):
        seen = True

sys.setprofile(observe)
payload = json.load(sys.stdin)
result = namespace['extract'](payload['source'], payload['target_solution']) if '--extract' in sys.argv else namespace['construction'](payload)[0]
sys.setprofile(None)
assert seen, 'real visibility fallback was not reached'
print('actual visibility fallback completed', file=sys.stderr)
json.dump(result, sys.stdout, separators=(',', ':'))
