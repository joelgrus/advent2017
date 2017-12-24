"""
https://adventofcode.com/2017/day/24
"""
from typing import NamedTuple, List, Set, Dict

Component = List[int]

def parse_line(line: str) -> Component:
    a, b = line.strip().split("/")
    return [int(a), int(b)]

def parse(raw: str) -> List[Component]:
    return [parse_line(line) for line in raw.strip("\n").split("\n")]

TEST_INPUT = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

TEST_COMPONENTS = parse(TEST_INPUT)

def strongest_bridge(components: List[Component], initial: int = 0):
    best = 0
    for component in components:
        a, b = component
        if initial in [a, b]:
            remaining_components = [c for c in components if c != component]
            best_for_a = best_for_b = 0
            if a == initial:
                best_for_a = a + b + strongest_bridge(remaining_components, b)
            if b == initial:
                best_for_b = a + b + strongest_bridge(remaining_components, a)
            best = max(best, best_for_a, best_for_b)

    return best

def longest_bridge(components: List[Component], initial: int = 0):
    best = (0, 0) # length, strength
    for component in components:
        a, b = component
        if initial in [a, b]:
            remaining_components = [c for c in components if c != component]
            bfa = (0, 0)
            bfb = (0, 0)
            if a == initial:
                bfa_length, bfa_strength = longest_bridge(remaining_components, b)
                bfa = (bfa_length + 1, bfa_strength + a + b)
            if b == initial:
                bfb_length, bfb_strength = longest_bridge(remaining_components, a)
                bfb = (bfb_length + 1, bfb_strength + a + b)
            best = max(best, bfa, bfb)

    return best


assert strongest_bridge(TEST_COMPONENTS) == 31
assert longest_bridge(TEST_COMPONENTS) == (4, 19)

if __name__ == "__main__":
    with open("day24_input.txt") as f:
        raw = f.read().strip("\n")
    components = parse(raw)

    #print(strongest_bridge(components))
    print(longest_bridge(components))
