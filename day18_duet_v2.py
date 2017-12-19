"""
https://adventofcode.com/2017/day/18
"""
from typing import List, NamedTuple, Union, Dict
from collections import defaultdict, deque

class Instruction(NamedTuple):
    op: str
    args: List[str]

Program = List[Instruction]

class State:
    def __init__(self, program_id: int) -> None:
        self.registers: Dict[str, int] = defaultdict(int)
        self.registers['p'] = program_id
        self.queue: deque = deque()
        self.other_state: 'State' = None
        self.pos = 0
        self.program_id = program_id
        self.sent_a_value = 0

    def enqueue(self, value: int) -> None:
        self.queue.append(value)

    def dequeue(self) -> int:
        if self.queue:
            return self.queue.popleft()
        else:
            return None

    def get(self, name_or_value: str) -> int:
        try:
            return int(name_or_value)
        except ValueError:
            return self.registers[name_or_value]


def step(program: Program, state: State) -> bool:
    """
    Return True if the apply succeeded, False otherwise
    """

    instruction = program[state.pos]
    op = instruction.op
    args = instruction.args

    # print("program", state.program_id)
    # print(state.__dict__)
    # print(instruction)
    # print()


    if op == "rcv":
        # get the value out of the queue
        register, = args
        value = state.dequeue()
        if value is None:
            return False
        else:
            state.registers[register] = value
            state.pos += 1
            return True
    elif op == "snd":
        # set last note to the value
        name_or_value, = args
        state.other_state.enqueue(state.get(name_or_value))
        state.sent_a_value += 1
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
    elif instruction.op == "jgz":
        x, y = instruction.args
        if state.get(x) > 0:
            state.pos += state.get(y)
            return True
    else:
        raise ValueError(f"unknown op: {op}")

    state.pos += 1
    return True


def run(program: Program) -> int:
    """
    Return the recovered frequency
    """
    state0 = State(program_id=0)
    state1 = State(program_id=1)
    state0.other_state = state1
    state1.other_state = state0

    while True:
        step0 = step(program, state0)
        step1 = step(program, state1)

        if not step0 and not step1:
            # deadlock
            print("deadlock")
            return state1.sent_a_value

def parse(raw: str) -> Program:
    lines = raw.split("\n")
    fields = [line.split() for line in lines]
    return [Instruction(field[0], field[1:]) for field in fields]

TEST_INPUT = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

#TEST_INSTRUCTIONS = parse(TEST_INPUT)

#print(run(TEST_INSTRUCTIONS))

if __name__ == "__main__":
    with open("day18_input.txt") as f:
        raw = f.read().strip()

    program = parse(raw)

    print(run(program))
