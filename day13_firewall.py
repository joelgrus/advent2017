"""
https://adventofcode.com/2017/day/13
"""
from collections import deque
from typing import Tuple, NamedTuple, Dict
import itertools

TEST_INPUT = """0: 3
1: 2
4: 4
6: 4"""

class Layer(NamedTuple):
    rang: int
    scanner: int = 0
    scanner_down: bool = True

def process_line(line: str) -> Tuple[int, Layer]:
    depth, range_ = line.split(":")
    return int(depth), Layer(int(range_))

assert process_line("6: 4") == (6, Layer(4))

def get_firewall(s: str) -> Dict[int, Layer]:
    firewall: Dict[int, Layer] = {}
    for line in s.split("\n"):
        if not line:
            continue
        depth, layer = process_line(line)
        firewall[depth] = layer
    return firewall

TEST_FIREWALL = get_firewall(TEST_INPUT)

def next_layer(layer: Layer) -> Layer:
    scanner = layer.scanner
    if layer.scanner_down:
        if layer.scanner == layer.rang - 1:
            scanner_down = False
            scanner -= 1
        else:
            scanner_down = True
            scanner += 1
    else:
        if layer.scanner == 0:
            scanner_down = True
            scanner += 1
        else:
            scanner_down = False
            scanner -= 1
    return Layer(layer.rang, scanner, scanner_down)

def step(firewall: Dict[int, Layer]) -> Dict[int, Layer]:
    return {depth: next_layer(layer)
            for depth, layer in firewall.items()}

def severity(firewall: Dict[int, Layer]) -> int:
    max_layer = max(firewall)

    total_severity = 0

    for depth in range(max_layer + 1):
        layer = firewall.get(depth)
        if layer and layer.scanner == 0:
            # Caught
            #print("caught", depth, layer)
            total_severity += depth * layer.rang
        firewall = step(firewall)

    return total_severity


# def caught(firewall: Dict[int, Layer]) -> bool:
#     max_layer = max(firewall)

#     for depth in range(max_layer + 1):
#         layer = firewall.get(depth)
#         if layer and layer.scanner == 0:
#             # Caught
#             #print("caught", depth, layer)
#             return True
#         firewall = step(firewall)

#     return False

# def min_wait(firewall: Dict[int, Layer]):
#     for wait in itertools.count():
#         if wait % 10000 == 0:
#             print("wait", wait)
#         if not caught(firewall):
#             return wait
#         firewall = step(firewall)

# def min_wait(firewall: Dict[int, Layer]):
#     max_layer = max(firewall)

#     states = deque([firewall])

#     for _ in range(max_layer):
#         states.append(step(states[-1]))

#     # at this point we have the first (max_layer+1) states
#     for wait in itertools.count():
#         print(wait)
#         safe = True
#         for i in range(max_layer + 1):
#             layer = states[i].get(i)
#             if layer and layer.scanner == 0:
#                 safe = False
#                 break
#         if safe:
#             return wait
#         states.append(step(states[-1]))
#         states.popleft()

def bad_times(layer: Layer):
    """
    If a layer has range 3, it will go 0, 1, 2, 1, 0, 1, 2, 1, 0, ..abs
    so its bad times are 0, 4, 8, ...

    If a layer has range 2, it will go 0, 1, 0, 1, 0, 1
    so its bad times are 0, 2, 4

    If a layer has range 4, it will go 0, 1, 2, 3, 2, 1, 0, ...
    so its bad times are 0, 6, 12, ...
    """
    step = (layer.rang - 1) * 2
    return itertools.count(start=0, step=step)

def is_good_wait_for_layer(depth: int, layer: Layer, wait: int) -> bool:
    step = (layer.rang - 1) * 2
    # it's a good wait, if it doesn't get here at a multiple of step
    get_here_at = wait + depth
    return get_here_at % step != 0

def is_good_wait(firewall: Dict[int, Layer], wait: int) -> bool:
    for depth, layer in firewall.items():
        if not is_good_wait_for_layer(depth, layer, wait):
            return False
    return True

def min_wait(firewall: Dict[int, Layer]) -> int:
    for wait in itertools.count():
        if wait % 10000 == 0:
            print("wait", wait)
        if is_good_wait(firewall, wait):
            return wait

assert min_wait(TEST_FIREWALL) == 10

if __name__ == "__main__":
    with open("day13_input.txt") as f:
        firewall = get_firewall(f.read())
    #print(severity(firewall))
    print(min_wait(firewall))
