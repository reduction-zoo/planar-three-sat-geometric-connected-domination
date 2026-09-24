"""Exact rational check of one published X/Y block interface."""

from fractions import Fraction
from itertools import combinations


def distance2(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def points(n):
    epsilon = Fraction(1, 100 * n**4)
    x1 = {}
    y1 = {}
    y2 = {}
    for j in range(1, n * n + 1):
        second = (j - 1) % n + 1
        x1[j] = (j * epsilon, -second * epsilon)
    for t in range(n * n + 1):
        y1[t] = (-2 + (t + Fraction(1, 2)) * epsilon, (t + Fraction(1, 2)) * epsilon)
        y2[t] = (2 + (t + Fraction(1, 2)) * epsilon, -n * epsilon)
    return x1, y1, y2


def main():
    tested = 0
    for n in range(2, 6):
        x1, y1, y2 = points(n)
        for block in (x1, y1, y2):
            assert all(distance2(p, q) <= 4 for p, q in combinations(block.values(), 2))
        for j, center in x1.items():
            for t, other in y1.items():
                actual = distance2(center, other) <= 4
                assert actual == (t >= j), (n, "Y1", j, t, actual)
                tested += 1
            for t, other in y2.items():
                actual = distance2(center, other) <= 4
                assert actual == (t < j), (n, "Y2", j, t, actual)
                tested += 1
    print(f"exact block adjacency checks: {tested} X/Y pairs, n=2..5")


if __name__ == "__main__":
    main()
