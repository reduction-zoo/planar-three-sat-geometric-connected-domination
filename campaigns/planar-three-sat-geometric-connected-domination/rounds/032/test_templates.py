"""Exhaustively check finite routing certificates, independently of synthesis."""
import itertools
import json
from pathlib import Path

expected = set()
for size in range(1, 5):
    for top in itertools.product((False, True), repeat=size):
        for bottom in itertools.product((False, True), repeat=size):
            if 2 <= sum(top) + sum(bottom) <= 4 and all(a or b for a, b in zip(top, bottom)):
                expected.add(''.join('X' if a and b else 'T' if a else 'B' for a, b in zip(top, bottom)))
certificates = json.loads((Path(__file__).parent / 'templates.json').read_text())
assert set(certificates) == expected
for pattern, certificate in certificates.items():
    center = tuple(certificate['center'])
    terminals = {(2 * i + 1, y) for i, symbol in enumerate(pattern) for y in (-4, 4) if symbol == 'X' or symbol == ('T' if y == 4 else 'B')}
    paths = [list(map(tuple, path)) for path in certificate['paths']]
    assert {path[-1] for path in paths} == terminals and len(paths) == len(terminals)
    used = set()
    for path in paths:
        assert path[0] == center and len(set(path)) == len(path)
        assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(path, path[1:]))
        assert all(0 <= x <= 2 * len(pattern) and -3 <= y <= 3 for x, y in path[:-1])
        assert not (set(path[1:]) & used)
        used.update(path[1:])
print('all local port patterns certified:', len(expected))
