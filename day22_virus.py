"""
https://adventofcode.com/2017/day/22
"""
from typing import NamedTuple, Set

class XY(NamedTuple):
    x: int
    y: int

Grid = Set[XY]

def make_grid(raw: str) -> Grid:
    lines = raw.split("\n")
    ncol = len(lines[0])
    nrow = len(lines)

    left = - (ncol // 2)  # 3 -> -1, 5 -> -2
    top = nrow // 2

    grid: Set[XY] = set()

    for i, row in enumerate(lines):
        for j, c in enumerate(row):
            if c == "#":
                x = left + j
                y = top - i
                grid.add(XY(x, y))

    return grid


TEST_INPUT = """..#
#..
..."""

TEST_GRID = make_grid(TEST_INPUT)
assert TEST_GRID == {XY(1, 1), XY(-1, 0)}

class Carrier:
    def __init__(self, pos: XY = XY(0, 0), direction: str = "up"):
        self.pos = pos
        self.dir = direction
        self.infections = 0

    def turn_right(self):
        if self.dir == "up":
            self.dir = "right"
        elif self.dir == "right":
            self.dir = "down"
        elif self.dir == "down":
            self.dir = "left"
        else:
            self.dir = "up"

    def turn_left(self):
        if self.dir == "up":
            self.dir = "left"
        elif self.dir == "right":
            self.dir = "up"
        elif self.dir == "down":
            self.dir = "right"
        else:
            self.dir = "down"


    def move_forward(self):
        x = self.pos.x
        y = self.pos.y

        if self.dir == "up":
            self.pos = XY(x, y+1)
        elif self.dir == "right":
            self.pos = XY(x+1, y)
        elif self.dir == "down":
            self.pos = XY(x, y-1)
        else:
            self.pos = XY(x-1, y)


def run(grid: Grid, carrier: Carrier, num_steps: int) -> None:
    for i in range(num_steps):
        pos = carrier.pos
        if pos in grid:
            # already infected, disinfect
            carrier.turn_right()
            grid.remove(pos)
        else:
            # not infected, so infect
            carrier.turn_left()
            grid.add(pos)
            carrier.infections += 1

        carrier.move_forward()

TEST_GRID = make_grid(TEST_INPUT)
TEST_CARRIER = Carrier()
run(TEST_GRID, TEST_CARRIER, 70)
assert TEST_CARRIER.infections == 41

TEST_GRID = make_grid(TEST_INPUT)
TEST_CARRIER = Carrier()
run(TEST_GRID, TEST_CARRIER, 10000)
assert TEST_CARRIER.infections == 5587

if __name__ == "__main__":
    with open("day22_input.txt") as f:
        raw = f.read().strip("\n")

    grid = make_grid(raw)
    carrier = Carrier()
    run(grid, carrier, 10000)
    print(carrier.infections)
