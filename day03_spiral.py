"""
http://adventofcode.com/2017/day/3
"""
from typing import Tuple, Dict, Iterator
import math
from collections import defaultdict
import itertools

def find_odd_squareroot(x: int) -> int:
    """
    Find the odd number n such that
    n ** 2 <= x < (n + 2) ** 2
    """
    # largest integer m with m**2 <= x
    sqrt_x = int(math.sqrt(x))

    if sqrt_x % 2 == 0:
        return sqrt_x - 1
    else:
        return sqrt_x

assert find_odd_squareroot(25) == 5
assert find_odd_squareroot(24) == 3
assert find_odd_squareroot(26) == 5
assert find_odd_squareroot(1) == 1

def find_coordinates(num: int) -> Tuple[int, int]:
    sqrt = find_odd_squareroot(num)
    x = y = sqrt // 2

    square = sqrt ** 2

    if num == square:
        return (x, y)

    # when we're done with 5x5, side length is 6
    side_length = sqrt + 1

    if num <= square + side_length:
        excess = num - square
        return (x + 1, y + 1 - excess)
    elif num <= square + 2 * side_length:
        excess = num - square - side_length
        return (x + 1 - excess, y + 1 - side_length)
    elif num <= square + 3 * side_length:
        excess = num - square - 2 * side_length
        return (-x - 1, -y - 1 + excess)
    else:
        excess = num - square - 3 * side_length
        return (-x - 1 + excess, y + 1)

assert find_coordinates(1) == (0, 0)
assert find_coordinates(9) == (1, 1)
assert find_coordinates(25) == (2, 2)
assert find_coordinates(26) == (3, 2)
assert find_coordinates(27) == (3, 1)
assert find_coordinates(31) == (3, -3)
assert find_coordinates(32) == (2, -3)
assert find_coordinates(33) == (1, -3)
assert find_coordinates(37) == (-3, -3)
assert find_coordinates(38) == (-3, -2)
assert find_coordinates(39) == (-3, -1)
assert find_coordinates(43) == (-3, 3)
assert find_coordinates(44) == (-2, 3)
assert find_coordinates(48) == (2, 3)
assert find_coordinates(49) == (3, 3)

def distance_to_center(num: int) -> int:
    x, y = find_coordinates(num)

    return abs(x) + abs(y)

assert distance_to_center(1) == 0
assert distance_to_center(12) == 3
assert distance_to_center(23) == 2
assert distance_to_center(1024) == 31

def get_neighbors(loc: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x, y = loc
    yield x + 1, y
    yield x + 1, y - 1
    yield x, y - 1
    yield x - 1, y - 1
    yield x - 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1

def first_value_larger_than(num: int) -> int:
    grid: Dict[Tuple[int, int], int] = defaultdict(int)

    grid[(0, 0)] = 1

    for i in itertools.count(2):
        loc = find_coordinates(i)

        value = sum(grid[neighbor]
                    for neighbor in get_neighbors(loc))

        if value > num:
            return value
        grid[loc] = value

    # mypy is not happy without a return statement
    raise RuntimeError("impossible to get here")

assert first_value_larger_than(400) == 747
assert first_value_larger_than(747) == 806


if __name__ == "__main__":
    print(distance_to_center(312051))
    print(first_value_larger_than(312051))
