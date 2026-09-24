"""Bounded exact placement search for a two-cell equality interface."""

from fractions import Fraction

CELL = {"g": (0, 0), "leaf": (-1, 0), "t": (1, 0), "f": (0, 1), "p": (1, 1)}


def squared(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def transform(point, swap, sx, sy, dx, dy):
    x, y = point[::-1] if swap else point
    return sx * x + dx, sy * y + dy


def clause_sites(a, b, excluded):
    for x2 in range(-10, 11):
        for y2 in range(-10, 11):
            q = (Fraction(x2, 2), Fraction(y2, 2))
            if squared(q, a) <= 1 and squared(q, b) <= 1 and all(squared(q, p) > 1 for p in excluded) and q not in excluded:
                yield q


def main():
    placements = pair_reachable = full = relaxed = 0
    examples = []
    nearby = []
    for swap in (False, True):
        for sx in (-1, 1):
            for sy in (-1, 1):
                for dx in range(-4, 5):
                    for dy in range(-4, 5):
                        other = {key: transform(value, swap, sx, sy, dx, dy) for key, value in CELL.items()}
                        if len(set(CELL.values()) | set(other.values())) != 10:
                            continue
                        placements += 1
                        pairs = ((CELL["f"], other["t"]), (CELL["t"], other["f"]))
                        if any(squared(a, b) > 4 for a, b in pairs):
                            continue
                        pair_reachable += 1
                        nearby.append((swap, sx, sy, dx, dy))
                        sites = []
                        relaxed_sites = []
                        for a, b in pairs:
                            excluded = [p for p in (*CELL.values(), *other.values()) if p != a and p != b]
                            sites.append(list(clause_sites(a, b, excluded)))
                            forbidden_selected = [CELL["g"], CELL["t"], CELL["f"], other["g"], other["t"], other["f"]]
                            relaxed_sites.append(list(clause_sites(a, b, [p for p in forbidden_selected if p != a and p != b])))
                        if all(sites):
                            full += 1
                            if len(examples) < 3:
                                examples.append((other, sites[0][0], sites[1][0]))
                        if all(relaxed_sites):
                            relaxed += 1
    print(f"placements={placements}, both port pairs within 2={pair_reachable}, isolated half-grid equality sites={full}, selected-port-only sites={relaxed}")
    print(f"nearby placements: {nearby}")
    for example in examples:
        print(example)


if __name__ == "__main__":
    main()
