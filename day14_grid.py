"""
https://adventofcode.com/2017/day/14
"""
from copy import deepcopy
from typing import List
import binascii

from day10_knot_hash import knot_hash

TEST_INPUT = "flqrgnkx"

def hex_to_bits(hexs: str) -> str:
    assert len(hexs) == 32
    bits = bin(int(hexs, 16))[2:].zfill(128)
    return bits

def count_ones(key: str) -> int:
    ones = 0
    for i in range(128):
        s = f"{key}-{i}"
        hashed = knot_hash(s)
        bits = hex_to_bits(hashed)
        ones += len([bit for bit in bits if bit == "1"])

    return ones

assert count_ones(TEST_INPUT) == 8108

def make_grid(key: str) -> List[List[str]]:
    grid: List[List[int]] = []  # <-- wrong type annotation!
    for i in range(128):
        s = f"{key}-{i}"
        hashed = knot_hash(s)
        bits = hex_to_bits(hashed)
        grid.append(list(bits))
    return grid

# wrong type annotation for grid here
def destroy_region(grid: List[List[int]], i: int, j: int) -> None:
    num_rows = len(grid)
    num_cols = len(grid[0])

    if i < 0 or i >= num_rows or j < 0 or j >= num_cols:
        # off the grid, so return
        return
    elif grid[i][j] == "0":
        # not part of a region, so return
        return
    else:
        # yes, part of a region, set to 0 and visit neighbors
        grid[i][j] = "0"
        destroy_region(grid, i+1, j)
        destroy_region(grid, i-1, j)
        destroy_region(grid, i, j+1)
        destroy_region(grid, i, j-1)


def count_regions(grid: List[List[str]]):
    grid = deepcopy(grid)

    num_regions = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "1":
                num_regions += 1
                destroy_region(grid, i, j)

    return num_regions

assert count_regions(make_grid(TEST_INPUT)) == 1242

if __name__ == "__main__":
    key = "hxtvlmkl"
    print(count_ones(key))
    grid = make_grid(key)
    print(count_regions(grid))
