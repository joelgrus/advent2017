"""
http://adventofcode.com/2017/day/6
"""
from typing import List
import itertools

def redistribute(memory: List[int]) -> None:
    NUM_BANKS = len(memory)

    max_blocks = max(memory)
    take_from = min(i for i, value in enumerate(memory) if value == max_blocks)

    num_to_redistribute = max_blocks
    memory[take_from] = 0

    idx = (take_from + 1) % NUM_BANKS

    for _ in range(num_to_redistribute):
        memory[idx] += 1
        idx = (idx + 1) % NUM_BANKS


def how_many_cycles(memory: List[int]) -> int:
    memory = memory[:]

    seen = { tuple(memory) }

    for cycle in itertools.count(1):
        redistribute(memory)
        as_tuple = tuple(memory)
        if as_tuple in seen:
            return cycle
        else:
            seen.add(as_tuple)


def size_of_loop(memory: List[int]) -> int:
    memory = memory[:]

    first_seen = { tuple(memory): 0 }

    for cycle in itertools.count(1):
        redistribute(memory)
        as_tuple = tuple(memory)
        if as_tuple in first_seen:
            return cycle - first_seen[as_tuple]
        else:
            first_seen[as_tuple] = cycle




if __name__ == "__main__":
    INPUT = """4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5"""
    memory = [int(x) for x in INPUT.split()]
    print(how_many_cycles(memory))
    print(size_of_loop(memory))
