"""
https://adventofcode.com/2017/day/18
"""
from typing import List, NamedTuple, Union
from collections import defaultdict

class Instruction(NamedTuple):
    op: str
    args: List[Union[str, int]]

Program = List[Instruction]

class State:
    def __init__(self) -> None:
        self.registers: Dict[str, int] = defaultdict(int)
        self.last_note: int = None

    def get(self, name_or_value: str) -> int:
        try:
            return int(name_or_value)
        except ValueError:
            return self.registers[name_or_value]


def apply(instruction: Instruction, state: State) -> None:
    op = instruction.op
    args = instruction.args

    if op == "snd":
        # set last note to the value
        name_or_value, = args
        state.last_note = state.get(name_or_value)
    elif op == "set":
        register, name_or_value = args
        state.registers[register] = state.get(name_or_value)
    elif op == "add":
        register, name_or_value = args
        state.registers[register] += state.get(name_or_value)
    elif op == "mul":
        register, name_or_value = args
        state.registers[register] *= state.get(name_or_value)
    elif op == "mod":
        register, name_or_value = args
        state.registers[register] = state.registers[register] % state.get(name_or_value)
    else:
        raise ValueError(f"unknown op: {op}")

def run(program: Program) -> int:
    """
    Return the recovered frequency
    """
    state = State()

    pos = 0

    while True:
        instruction = program[pos]
        print(state.__dict__)
        print(pos, instruction)

        if instruction.op == "rcv":
            value = state.get(instruction.args[0])
            if value != 0:
                return state.last_note
            else:
                pos += 1
        elif instruction.op == "jgz":
            x, y = instruction.args
            if state.get(x) > 0:
                pos += state.get(y)
            else:
                pos += 1
        else:
            # do something with the state
            apply(instruction, state)
            pos += 1

        if pos < 0 or pos > len(program):
            raise RuntimeError(f"terminated")

def parse(raw: str) -> Program:
    lines = raw.split("\n")
    fields = [line.split() for line in lines]
    return [Instruction(field[0], field[1:]) for field in fields]

TEST_INPUT = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

TEST_INSTRUCTIONS = parse(TEST_INPUT)


if __name__ == "__main__":
    with open("day18_input.txt") as f:
        raw = f.read().strip()

    program = parse(raw)

    print(run(program))
