"""Replay finite exact common-grid allocation and signed CVASS witnesses."""
from fractions import Fraction as F
from itertools import product

def allocate(total, denominator, multiplicity):
    units = total * denominator
    assert units.denominator == 1
    remainder = int(units) - multiplicity
    shares = []
    for _ in range(multiplicity):
        extra = min(remainder, denominator - 1)
        shares.append(1 + extra)
        remainder -= extra
    assert remainder == 0
    assert all(1 <= share <= denominator for share in shares)
    assert F(sum(shares), denominator) == total
    return shares

cases = 0
for grid, length in product(range(1, 13), range(1, 15)):
    denominator = grid * length
    for multiplicity in range(1, length + 1):
        for numerator in range(1, grid * multiplicity + 1):
            allocate(F(numerator, grid), denominator, multiplicity)
            cases += 1

def replay(edges, run, start, finish, denominator, cover=False):
    state, coordinates = start
    for edge_index, numerator in run:
        tail, head, update = edges[edge_index]
        assert state == tail and 1 <= numerator <= denominator
        coordinates = tuple(value + F(numerator, denominator) * delta for value, delta in zip(coordinates, update))
        state = head
    assert state == finish[0]
    if cover:
        assert all(value >= bound for value, bound in zip(coordinates, finish[1]))
    else:
        assert coordinates == finish[1]
    return coordinates

edges = [('p', 'p', (2, 0)), ('p', 'q', (-1, 3)), ('p', 'p', (-2, 0))]
assert replay(edges, [(0, 2), (0, 1), (1, 1)], ('p', (0, 0)), ('q', (F(5, 2), F(3, 2))), 2) == (F(5, 2), F(3, 2))
assert replay(edges, [(2, 1), (0, 2), (1, 2)], ('p', (0, 0)), ('q', (0, 2)), 2, cover=True) == (0, 3)
assert replay(edges, [], ('p', (F(-1, 3), F(2, 7))), ('p', (F(-1, 3), F(2, 7))), 1) == (F(-1, 3), F(2, 7))
print(f"PASS: {cases} exact grid allocation fixtures, signed reachability, signed coverability, and the empty run.")
