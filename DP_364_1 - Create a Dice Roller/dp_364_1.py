#!/usr/bin/env python3

from random import randint


def roll(input):
    for line in input.split():
        n, s = line.split('d')
        yield [randint(1, int(s)) for _ in range(int(n))]


inp = """
5d12
6d4
1d2
1d8
3d6
4d20
100d100
"""

while inp:
    for out in roll(inp):
        print(f"{sum(out)}: {' '.join(str(x) for x in out)}")
    inp = input('How should we roll: ').strip()
