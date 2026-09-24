"""Exact structural SVGs; assertions check their stated graph interfaces."""
from collections import Counter
from html import escape
from math import cos, sin, pi
from pathlib import Path

HERE = Path(__file__).parent

def polar(center, radius, index, count):
    angle = 2 * pi * index / count - pi / 2
    return center[0] + radius * cos(angle), center[1] + radius * sin(angle)

def svg(name, width, height, positions, edges, filled=(), labels=None, squares=()):
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    assert all(a in positions and b in positions and a != b for a,b in edges)
    assert len(set(map(frozenset, edges))) == len(edges)
    for a, b in edges:
        x,y = positions[a]; xx,yy = positions[b]
        lines.append(f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="black" stroke-width="2"/>')
    for v, (x,y) in positions.items():
        fill = 'black' if v in filled else 'white'
        if v in squares:
            lines.append(f'<rect x="{x-6}" y="{y-6}" width="12" height="12" fill="{fill}" stroke="black" stroke-width="2"/>')
        else:
            lines.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{fill}" stroke="black" stroke-width="2"/>')
    for label, (x,y) in (labels or {}).items():
        lines.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Libertinus Serif,serif" font-size="19" paint-order="stroke" stroke="white" stroke-width="3">{escape(label)}</text>')
    lines.append('</svg>')
    (HERE / name).write_text('\n'.join(lines)+'\n')

# One legal repeated-literal clause: six-cycle, clause triangle, three ports.
p = {i: polar((190,185), 62, i, 6) for i in range(6)}
p.update({6+i: polar((190,185), 143, i, 3) for i in range(3)})
edges = [(i,(i+1)%6) for i in range(6)] + [(6+i,6+(i+1)%3) for i in range(3)] + [(2*i,6+i) for i in range(3)]
cover = {0,2,4,7,8}
assert len(cover) == 5 and all(a in cover or b in cover for a,b in edges)
deg = Counter(v for edge in edges for v in edge)
assert sorted(deg.values()) == [2,2,2,3,3,3,3,3,3]
labels = {('T' if i%2==0 else 'F')+str(i//2): polar((190,191), 40, i,6) for i in range(6)}
labels.update({f'c{i}': polar((190,191), 168, i,3) for i in range(3)})
svg('clause.svg',380,350,p,edges,cover,labels)

# Full connected-cover augmentation of a triangle after two subdivisions per edge.
p = {i: polar((200,190),88,i,9) for i in range(9)}
p.update({('w',side,i): polar((200,190),r,i,9) for side,r in [('in',47),('out',143)] for i in range(9)})
p.update({('leaf',side,i): polar((200,190),r,i,9) for side,r in [('in',21),('out',168)] for i in range(9)})
edges = [(i,(i+1)%9) for i in range(9)]
for side in ('in','out'):
    for i in range(9):
        w=('w',side,i)
        edges += [(i,w),(w,('w',side,(i+1)%9)),(w,('leaf',side,i))]
deg=Counter(v for edge in edges for v in edge)
assert len(p)==45 and len(edges)==63
assert all(deg[v] == (1 if isinstance(v,tuple) and v[0]=='leaf' else 4) for v in p)
labels = {name: polar((200,195),108,i+0.13,9) for name,i in [('u',0),('a',1),('b',2),('v',3)]}
svg('face-cycles.svg',400,390,p,edges,{v for v in p if isinstance(v,tuple) and v[0]=='w'},labels,{0,3,6})

# Actual unit-distance adjacency of a straight length-ten grid route.
points = {(i,0) for i in range(11)} | {(i,1) for i in range(2,9)}
edges = [(a,b) for a in sorted(points) for b in sorted(points) if a<b and sum((x-y)**2 for x,y in zip(a,b))==1]
assert len(edges)==23
assert all(sum(q in edge for edge in edges)==(2 if q[0] in (2,8) else 3) for q in points if q[1]==1)
p={v:(35+55*v[0],115-55*v[1]) for v in sorted(points)}
labels={'u':(35,150),'v':(585,150),'connector':(90,174),'connector ': (530,174),'middle path points':(310,153),'side points':(310,29)}
svg('grid-route.svg',620,190,p,edges,{(i,0) for i in range(11) if i not in (1,9)},labels,{(0,0),(10,0)})
print('Figures checked: clause ports/cover; 45-vertex face augmentation; exact 18-point grid adjacency.')
