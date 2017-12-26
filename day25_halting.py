"""
https://adventofcode.com/2017/day/25
"""
from typing import NamedTuple, Dict, Set

class Rule(NamedTuple):
    value_to_write: int
    direction: str
    next_state: str

State = Dict[int, Rule]

Blueprint = Dict[str, State]

Tape = Set[int]  # all the ones

TEST_BLUEPRINT: Blueprint = {
    "A": {0: Rule(1, "right", 'B'), 1: Rule(0, 'left', 'B')},
    "B": {0: Rule(1, "left", 'A'), 1: Rule(1, 'right', 'A')}
}

def run(blueprint: Blueprint, initial_state: str, num_steps: int) -> Tape:
    tape: Set[int] = set()
    pos = 0
    state = initial_state

    for step in range(num_steps):
        if step % 1_000_000 == 0:
            print(step)

        current_value = 1 if pos in tape else 0
        rule = blueprint[state][current_value]
        # write
        if rule.value_to_write == 1 and current_value == 0:
            tape.add(pos)
        elif rule.value_to_write == 0 and current_value == 1:
            tape.remove(pos)
        # move
        if rule.direction == "left":
            pos -= 1
        else:
            pos += 1
        # state
        state = rule.next_state

    return tape

assert(len(run(TEST_BLUEPRINT, 'A', 6)) == 3)

real_blueprint: Blueprint = {
    "A": {0: Rule(1, "right", 'B'), 1: Rule(0, 'left', 'C')},
    "B": {0: Rule(1, "left", 'A'), 1: Rule(1, 'right', 'D')},
    "C": {0: Rule(1, "right", 'A'), 1: Rule(0, 'left', 'E')},
    "D": {0: Rule(1, "right", 'A'), 1: Rule(0, 'right', 'B')},
    "E": {0: Rule(1, "left", 'F'), 1: Rule(1, 'left', 'C')},
    "F": {0: Rule(1, "right", 'D'), 1: Rule(1, 'right', 'A')}
}

if __name__ == "__main__":
    tape = run(real_blueprint, 'A', 12_173_597)
    print(len(tape))
