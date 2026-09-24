"""Observe the real accepted drawing, then stop before enormous point expansion."""
import hashlib
import json
import os
from pathlib import Path
import sys


def observe(frame, event, value):
    if event == 'return' and frame.f_code.co_name == 'checked_layout' and frame.f_code.co_filename.endswith('/rounds/010/drawing.py'):
        graph, positions = value
        payload = json.dumps(sorted((repr(v), p) for v, p in positions.items()), separators=(',', ':'))
        record = {'core_size': len(frame.f_locals['core']), 'drawing_vertices': len(graph), 'position_sha256': hashlib.sha256(payload.encode()).hexdigest(), 'route_length': sum(abs(positions[u][0]-positions[v][0])+abs(positions[u][1]-positions[v][1]) for u,v in graph.edges)}
        Path(os.environ['REVIEW_OUTPUT']).write_text(json.dumps(record, indent=2)+'\n')
        os._exit(0)

sys.setprofile(observe)
