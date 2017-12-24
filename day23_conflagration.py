"""
https://adventofcode.com/2017/day/23
"""
from typing import List, NamedTuple, Union, Dict
from collections import defaultdict

class Instruction(NamedTuple):
    op: str
    x: str
    y: Union[str, int] = None

Program = List[Instruction]

class State:
    def __init__(self) -> None:
        self.registers: Dict[str, int] = defaultdict(int)

    def get(self, name_or_value: str) -> int:
        try:
            return int(name_or_value)
        except ValueError:
            return self.registers[name_or_value]

    def set(self, register: str, value: int) -> None:
        self.registers[register] = value


def apply(instruction: Instruction, state: State) -> None:
    #print(instruction)
    #print(state.__dict__)
    op = instruction.op
    x = instruction.x
    y = instruction.y

    if op == "set":
        state.set(x, state.get(y))
    elif op == "sub":
        previous_value = state.get(x)
        state.set(x, previous_value - state.get(y))
    elif op == "mul":
        previous_value = state.get(x)
        state.set(x, previous_value * state.get(y))
    else:
        raise ValueError(f"unknown op: {op}")

class ProgramState:
    def __init__(self, program: Program, state: State):
        self.program = program
        self.pos = 0
        self.state = state
        self.terminated = False

    def __repr__(self) -> str:
        return f"{self.pos} {self.program[self.pos]}\n{self.state.__dict__}"

    def skip_dg(self) -> None:
        g = self.state.registers['g']
        self.state.registers['g'] -= g
        self.state.registers['d'] -= g

    def swap_f(self) -> None:
        self.state.registers['b'] += 17
        self.state.registers['d'] += 17
        self.state.registers['e'] += 17

        f = self.state.registers['f']
        if f == 0:
            self.state.registers['h'] += 1
        self.state.registers['f'] = 1 - f

    def step(self) -> None:
        if self.terminated:
            return

        instruction = self.program[self.pos]

        if instruction.op == "jnz":
            if self.state.get(instruction.x) != 0:
                self.pos += self.state.get(instruction.y)
            else:
                self.pos += 1
        else:
            apply(instruction, self.state)
            self.pos += 1

        if self.pos < 0 or self.pos >= len(self.program):
            self.terminated = True

def run(program: Program, initial_registers: Dict[str, int] = {}) -> State:
    """
    Return the recovered frequency
    """
    state = State()
    for k, v in initial_registers.items():
        state.set(k, v)

    pos = 0
    mul = 0

    while True:
        instruction = program[pos]

        if instruction.op == "jnz":
            if state.get(instruction.x) != 0:
                pos += state.get(instruction.y)
            else:
                pos += 1
        else:
            apply(instruction, state)
            pos += 1
            if instruction.op == "mul":
                mul += 1

        if pos < 0 or pos >= len(program):
            print("terminated")
            break

    print(mul)
    return state

def parse(raw: str) -> Program:
    lines = raw.split("\n")
    fields = [line.split("#")[0].strip().split() for line in lines]
    return [Instruction(field[0], field[1], field[2]) for field in fields]


if __name__ == "__main__":
    with open("day23_input.txt") as f:
        raw = f.read().strip("\n")

    # # part 1
    # program = parse(raw)
    # state = run(program)
    # print(state.__dict__)

    # part 2
    program = parse(raw)
    state = State()
    state.set("a", 1)
    ps = ProgramState(program,state)

    # and now for a hack
    # ps.state.registers = {'a': 1, 'b': 105700, 'c': 122700, 'f': 0, 'd': 105700, 'e': 105700, 'g': 0, 'h': 0}
    #ps.state.registers = {'a': 1, 'b': 105717, 'c': 122700, 'f': 0, 'd': 105717, 'e': 105717, 'g': 0, 'h': 1}
    #ps.pos = 23
    while not ps.terminated:
        report = ps.pos == 23
        if report:
            ps.skip_dg()
            print(ps)
        ps.step()
        if report:
            print(ps)
            print()


    # while ps.state.get('b') != ps.state.get('c'):
    #     g = ps.state.registers['g']
    #     ps.state.registers['g'] -= g
    #     ps.state.registers['d'] -= g
    #     ps.state.registers['b'] += 17
    #     ps.state.registers['d'] += 17
    #     ps.state.registers['e'] += 17

    #     f = ps.state.registers['f']
    #     if f == 0:
    #         ps.state.registers['h'] += 1
    #     ps.state.registers['f'] = 1 - f

    while not ps.terminated:
        print(ps)
        ps.step()




"""
{'registers': defaultdict(<class 'int'>, {'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 3, 'g': -105697})}
19 Instruction(op='jnz', x='g', y='-8')
{'registers': defaultdict(<class 'int'>, {'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 3, 'g': -105697})}

{'registers': defaultdict(<class 'int'>, {'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 4, 'g': -105696})}
19 Instruction(op='jnz', x='g', y='-8')
{'registers': defaultdict(<class 'int'>, {'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 4, 'g': -105696})}

{'registers': defaultdict(<class 'int'>, {'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 5, 'g': -105695})}
19 Instruction(op='jnz', x='g', y='-8')
{'registers': defaultdict(<class 'int'>, {'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 5, 'g': -105695})}

{'a': 1, 'b': 105700, 'c': 122700, 'f': 1, 'd': 2, 'e': 5, 'g': -105695}

{'registers': {'a': 1, 'b': 105700, 'c': 122700, 'd': 3, 'e': 4, 'f': 1, 'g': -105696}}
19 Instruction(op='jnz', x='g', y='-8')
{'registers': {'a': 1, 'b': 105700, 'c': 122700, 'd': 3, 'e': 4, 'f': 1, 'g': -105696}}


{'registers': {'a': 1, 'b': 105700, 'c': 122700, 'd': 3, 'e': 5, 'f': 1, 'g': -105695}}
19 Instruction(op='jnz', x='g', y='-8')
{'registers': {'a': 1, 'b': 105700, 'c': 122700, 'd': 3, 'e': 5, 'f': 1, 'g': -105695}}


{'a': 1, 'g': 0, 'b': 105700, 'c': 122700, 'f': 0, 'd': 3, 'e': 105700}
{'a': 1, 'g': 0, 'b': 105700, 'c': 122700, 'f': 0, 'd': 4, 'e': 26425}
{'a': 1, 'g': 0, 'b': 105700, 'c': 122700, 'f': 0, 'd': 5, 'e': 21140}
{'a': 1, 'g': 0, 'b': 105700, 'c': 122700, 'f': 0, 'd': 6, 'e': 105700}
{'a': 1, 'g': 0, 'b': 105700, 'c': 122700, 'f': 0, 'd': 7, 'e': 15100})}
{'a': 1, 'g': 0, 'b': 105700, 'c': 122700, 'f': 0, 'd': 8, 'e': 105700}

"""
