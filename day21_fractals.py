"""
https://adventofcode.com/2017/day/21
"""
from typing import NamedTuple, List
from copy import deepcopy

Grid = List[List[str]]

def concise(grid: Grid) -> str:
    return "/".join(''.join(row) for row in grid)

assert concise([['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]) == ".#./..#/###"

def unconcise(s: str) -> Grid:
    return [list(row) for row in s.split("/")]

assert unconcise(".#./..#/###") == [['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]


def flip(grid: Grid) -> Grid:
    """
    flip left to right
    """
    return [list(reversed(row)) for row in grid]

def rotate(grid: Grid) -> Grid:
    """
    rotate by 90 degrees
    (j, 0) -> (n-1, j)
    (n-1, j) -> (n-1-j, n-1)
    """
    rotated = deepcopy(grid)
    n = len(grid)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            rotated[j][n-1-i] = c

    return rotated

assert rotate(unconcise(".#./..#/###")) == unconcise("#../#.#/##.")




class Rule(NamedTuple):
    input: str
    output: str

    # def matches(self, grid: Grid) -> bool:
    #     rule = unconcise(self.input)
    #     rule2 = flip(rule)
    #     return any(
    #         grid == target
    #         for target in [
    #             rule,
    #             rotate(rule),
    #             rotate(rotate(rule)),
    #             rotate(rotate(rotate(rule))),
    #             rule2,
    #             rotate(rule2),
    #             rotate(rotate(rule2)),
    #             rotate(rotate(rotate(rule2)))
    #         ])

class Rules:
    def __init__(self, rules: List[Rule]) -> None:
        self.input_output: Dict[str, Grid] = {}
        for rule in rules:
            rule1 = unconcise(rule.input)
            rule2 = flip(rule1)
            o = unconcise(rule.output)

            for target in [
                rule1,
                rotate(rule1),
                rotate(rotate(rule1)),
                rotate(rotate(rotate(rule1))),
                rule2,
                rotate(rule2),
                rotate(rotate(rule2)),
                rotate(rotate(rotate(rule2)))
            ]:
                self.input_output[concise(target)] = o

    def get(self, grid: Grid) -> Grid:
        key = concise(grid)
        return self.input_output[key]


TEST_INPUT = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

def parse_line(line: str) -> Rule:
    i, o = line.strip().split(" => ")
    return Rule(input=i, output=o)

TEST_RULES = Rules([parse_line(line) for line in TEST_INPUT.split("\n")])

def enhance(square: Grid, rules: Rules) -> Grid:
    return rules.get(square)

def segment(image: Grid) -> List[List[Grid]]:
    n = len(image)
    if n % 2 == 0:
        # 2x2 squares
        return [
            [ [[image[i][j],   image[i][j+1]],
               [image[i+1][j], image[i+1][j+1]]]
                for j in range(0, n, 2)
            ] for i in range(0, n, 2)
        ]
    elif n % 3 == 0:
        # 3x3 squares
        return [
            [ [[image[i][j],   image[i][j+1],  image[i][j+2]],
               [image[i+1][j], image[i+1][j+1], image[i+1][j+2]],
               [image[i+2][j], image[i+2][j+1], image[i+2][j+2]]]
                for j in range(0, n, 3)
            ] for i in range(0, n, 3)
        ]
    else:
        raise ValueError("bad size")

def glom(grids: List[List[Grid]]) -> Grid:
    num_grids = len(grids)
    grid_size = len(grids[0][0])

    output_grid = [[None for _ in range(num_grids * grid_size)] for _ in range(num_grids * grid_size)]

    for i in range(num_grids):
        for j in range(num_grids):
            for ii in range(grid_size):
                for jj in range(grid_size):
                    output_grid[i * grid_size + ii][j * grid_size + jj] = grids[i][j][ii][jj]

    return output_grid


def process_image(image: Grid, rules: Rules) -> Grid:
    # get a grid of grids
    segmented = segment(image)

    processed = [
        [enhance(square, rules) for square in row]
        for row in segmented
    ]

    glommed = glom(processed)
    return glommed

def count_pixels(image: Grid) -> int:
    count = 0
    for row in image:
        for c in row:
            if c == '#':
                count += 1
    return count

TEST_PATTERN = unconcise(".#./..#/###")
_ITER1 = process_image(TEST_PATTERN, TEST_RULES)
_ITER2 = process_image(_ITER1, TEST_RULES)
assert count_pixels(_ITER2) == 12


if __name__ == "__main__":
    with open("day21_input.txt") as f:
        raw = f.read().strip("\n")
    rules = Rules([parse_line(line) for line in raw.split("\n")])

    pattern = TEST_PATTERN

    for i in range(18):
        print(i)
        pattern = process_image(pattern, rules)


    print(count_pixels(pattern))
