"""
https://adventofcode.com/2017/day/22
"""
from typing import NamedTuple, Dict
from enum import Enum

class XY(NamedTuple):
    x: int
    y: int

class State(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

Grid = Dict[XY, State]

def make_grid(raw: str) -> Grid:
    lines = raw.split("\n")
    ncol = len(lines[0])
    nrow = len(lines)

    left = - (ncol // 2)  # 3 -> -1, 5 -> -2
    top = nrow // 2

    grid: Dict[XY, State] = {}

    for i, row in enumerate(lines):
        for j, c in enumerate(row):
            if c == "#":
                x = left + j
                y = top - i
                grid[XY(x, y)] = State.INFECTED

    return grid


TEST_INPUT = """..#
#..
..."""

TEST_GRID = make_grid(TEST_INPUT)
assert TEST_GRID == {XY(1, 1): State.INFECTED,
                     XY(-1, 0): State.INFECTED}

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

    def reverse(self):
        self.turn_left()
        self.turn_left()

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
        if i % 100_000 == 0:
            print(i)

        pos = carrier.pos
        state = grid.get(pos, State.CLEAN)

        if state == State.CLEAN:
            carrier.turn_left()
            grid[pos] = State.WEAKENED
        elif state == State.WEAKENED:
            grid[pos] = State.INFECTED
            carrier.infections += 1
        elif state == State.INFECTED:
            carrier.turn_right()
            grid[pos] = State.FLAGGED
        else: # flagged
            carrier.reverse()
            del grid[pos]

        carrier.move_forward()

TEST_GRID = make_grid(TEST_INPUT)
TEST_CARRIER = Carrier()
run(TEST_GRID, TEST_CARRIER, 100)
assert TEST_CARRIER.infections == 26

# TEST_GRID = make_grid(TEST_INPUT)
# TEST_CARRIER = Carrier()
# run(TEST_GRID, TEST_CARRIER, 10_000_000)
# assert TEST_CARRIER.infections == 2511944

if __name__ == "__main__":
    with open("day22_input.txt") as f:
        raw = f.read().strip("\n")

    grid = make_grid(raw)
    carrier = Carrier()
    run(grid, carrier, 10_000_000)
    print(carrier.infections)
