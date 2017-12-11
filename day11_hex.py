"""
https://adventofcode.com/2017/day/11
"""
from typing import Dict
from collections import defaultdict
from copy import copy

def eliminate_opposites(counts: Dict[str, int]) -> bool:
    n_s = min(counts['n'], counts['s'])
    ne_sw = min(counts['ne'], counts['sw'])
    nw_se = min(counts['nw'], counts['se'])

    if n_s > 0 or ne_sw > 0 or nw_se > 0:
        counts['n'] -= n_s
        counts['s'] -= n_s
        counts['ne'] -= ne_sw
        counts['sw'] -= ne_sw
        counts['nw'] -= nw_se
        counts['se'] -= nw_se
        return True
    else:
        return False

def _condense(counts: Dict[str, int], minus1: str, minus2: str, plus: str) -> bool:
    eliminate = min(counts[minus1], counts[minus2])
    if eliminate > 0:
        counts[minus1] -= eliminate
        counts[minus2] -= eliminate
        counts[plus] += eliminate
        return True
    else:
        return False

def condense(counts: Dict[str, int]) -> bool:
    condensed = False
    for m1, m2, p in [
        ('n', 'se', 'ne'),
        ('ne', 's', 'se'),
        ('se', 'sw', 's'),
        ('s', 'nw', 'sw'),
        ('sw', 'n', 'nw'),
        ('nw', 'ne', 'n')]:
        condensed = condensed or _condense(counts, m1, m2, p)

    # oops, I screwed this up here, I didn't return a value!
    # If I'd bothered running mypy, it would have told me.
    # Luckily, it didn't matter, for the following reason:
    # it's always the case that you only need to run
    #       eliminate -> condense -> eliminate
    # to get down to two adjacent directions, and even without the
    # return statement it was enough to make that happen.
    # Next time I'll run mypy!


def distance(counts: Dict[str, int]) -> int:
    counts = copy(counts)

    while True:
        if not eliminate_opposites(counts) and not condense(counts):
            break

    return sum(counts.values())


if __name__ == "__main__":
    with open("day11_input.txt") as f:
        path = f.read().strip().split(",")

    counts: Dict[str, int] = defaultdict(int)

    max_dist = float('-inf')

    for move in path:
        counts[move] += 1
        dist = distance(counts)
        if dist > max_dist:
            max_dist = dist

        print(move, dist, max_dist)
