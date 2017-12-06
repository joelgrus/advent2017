"""
http://adventofcode.com/2017/day/5
"""
from typing import List

def steps_to_exit(jump_offsets: List[int]) -> int:
    jump_offsets = jump_offsets[:]

    curr = 0
    num_steps = 0

    while curr >= 0 and curr < len(jump_offsets):
        offset = jump_offsets[curr]
        jump_offsets[curr] += 1
        curr += offset
        num_steps += 1

    return num_steps

TEST_OFFSETS = [0, 3, 0, 1, -3]

assert steps_to_exit(TEST_OFFSETS) == 5

def steps_to_exit2(jump_offsets: List[int]) -> int:
    jump_offsets = jump_offsets[:]

    curr = 0
    num_steps = 0

    while curr >= 0 and curr < len(jump_offsets):
        offset = jump_offsets[curr]
        if offset >= 3:
            jump_offsets[curr] -= 1
        else:
            jump_offsets[curr] += 1
        curr += offset
        num_steps += 1

    return num_steps

assert steps_to_exit2(TEST_OFFSETS) == 10

if __name__ == "__main__":
    with open("day05_input.txt", "r") as f:
        offsets = [int(line) for line in f]
        print(steps_to_exit(offsets))
        print(steps_to_exit2(offsets))
