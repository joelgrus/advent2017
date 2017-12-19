"""
https://adventofcode.com/2017/day/19
"""
from typing import List, NamedTuple, Optional
from string import ascii_uppercase

TEST_INPUT = """     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+"""

TEST_GRID = [list(row) for row in TEST_INPUT.split("\n")]


class State:
    def __init__(self, grid: List[List[str]], i: int, j: int, direction: str):
        self.grid = grid
        self.i = i
        self.j = j
        self.direction = direction
        self.letters: List[str] = []

    def go_forward(self) -> None:
        if self.direction == 'up':
            self.i -= 1
        elif self.direction == 'down':
            self.i += 1
        elif self.direction == 'left':
            self.j -= 1
        elif self.direction == 'right':
            self.j += 1

    def get(self, i: int, j: int) -> Optional[str]:
        if i < 0:
            return None
        if j < 0:
            return None
        if i >= len(self.grid):
            return None
        if j >= len(self.grid[i]):
            return None

        return self.grid[i][j].strip()


    def turn(self) -> None:
        if self.direction in ['up', 'down']:
            if self.get(self.i, self.j-1):
                self.direction = 'left'
            else:
                self.direction = 'right'
        else: # left or right
            if self.get(self.i-1, self.j):
                self.direction = 'up'
            else:
                self.direction = 'down'


def step(state: State) -> bool:
    i = state.i
    j = state.j
    direction = state.direction

    current = state.grid[i][j]
    print(i, j, "current", current)

    if current in ['|', '-']:
        state.go_forward()
        return True

    elif 'A' <= current <= 'Z':
        state.letters.append(current)
        state.go_forward()
        return True

    elif current == '+':
        state.turn()
        state.go_forward()
        return True

    else:
        # nothing to do
        return False


def traverse(grid: List[List[str]]) -> str:
    top_row = grid[0]
    initial_column = top_row.index('|')
    state = State(grid, 0, initial_column, 'down')
    print("initial column", initial_column)

    num_steps = 0
    while step(state):
        num_steps += 1

    print(num_steps)

    return ''.join(state.letters)

assert traverse(TEST_GRID) == "ABCDEF"

if __name__ == "__main__":
    with open("day19_input.txt") as f:
        raw = f.read().strip("\n")

    grid = [list(row) for row in raw.split("\n")]

    print(traverse(grid))
