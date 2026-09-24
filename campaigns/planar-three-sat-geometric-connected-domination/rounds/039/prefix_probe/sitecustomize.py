import json, os, sys
from pathlib import Path

def audit(frame, event, arg):
    if event == "return" and frame.f_code.co_name == "checked_layout" and frame.f_code.co_filename.endswith("/rounds/010/drawing.py"):
        drawn, positions = arg
        record = {"core_nodes": len(frame.f_locals["core"]), "positions": sorted((repr(k), v) for k,v in positions.items()), "route_length": sum(abs(positions[u][0]-positions[v][0])+abs(positions[u][1]-positions[v][1]) for u,v in drawn.edges)}
        Path(os.environ["REVIEW_PREFIX_OUTPUT"]).write_text(json.dumps(record))
        os._exit(0)
    return audit
sys.settrace(audit)
