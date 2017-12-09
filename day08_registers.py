"""
https://adventofcode.com/2017/day/8
"""
from typing import NamedTuple, List, Dict
from collections import defaultdict
import re

class Condition(NamedTuple):
    register: str
    comparison: str
    target: int

class Instruction(NamedTuple):
    register: str
    operation: str
    amount: int
    condition: Condition


def parse_instruction(raw: str) -> Instruction:
    inst, cond = raw.split(" if ")
    if " inc " in inst:
        register, amount = inst.split(" inc ")
        operation = "inc"
    elif " dec " in inst:
        register, amount = inst.split(" dec ")
        operation = "dec"
    else:
        raise ValueError(f"cannot parse {inst}")

    op_rgx = "(==|!=|<=|>=|<|>)"
    cond_register, op, cond_target = re.split(op_rgx, cond)

    condition = Condition(register = cond_register.strip(),
                          comparison = op,
                          target = int(cond_target))

    return Instruction(register = register,
                       operation = operation,
                       amount = int(amount),
                       condition = condition)

def meets_condition(condition: Condition, registers: Dict[str, int]) -> bool:
    value = registers.get(condition.register, 0)
    target = condition.target
    op = condition.comparison

    #print(f"checking {value} {op} {target}")

    if op == "==":
        return value == target
    elif op == "!=":
        return value != target
    elif op == "<":
        return value < target
    elif op == "<=":
        return value <= target
    elif op == ">":
        return value > target
    elif op == ">=":
        return value >= target
    else:
        raise ValueError(f"unknown op {op}")



def process_instruction(instruction: Instruction, registers: Dict[str, int]) -> None:
    condition = instruction.condition
    if meets_condition(condition, registers):
        #print("meets condition")
        register = instruction.register
        op = instruction.operation
        amount = instruction.amount
        value = registers.get(register, 0)

        #print(f"{register} {op} {amount}")
        #print(f"previous value: {value}")

        if op == "inc":
            registers[register] = value + amount
        elif op == "dec":
            registers[register] = value - amount

        #print(f"new value: {registers[register]}")

def process_instructions(instructions: List[Instruction]) -> Dict[str, int]:
    registers: Dict[str, int] = {}
    highest_value_ever = float("-inf")

    for instruction in instructions:
        process_instruction(instruction, registers)
        highest_value_ever = max(highest_value_ever, max(registers.values()))
        print(registers)
        print(highest_value_ever)

    return registers


TEST_INPUTS = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

TEST_INSTRUCTIONS = [parse_instruction(line) for line in TEST_INPUTS.split("\n")]

if __name__ == "__main__":
    with open("day08_input.txt") as f:
        instructions = [parse_instruction(line.strip()) for line in f]

    registers = process_instructions(instructions)
    print(registers)
    print(max(registers.values()))
