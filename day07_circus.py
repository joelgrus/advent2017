"""
http://adventofcode.com/2017/day/7
"""
from typing import NamedTuple, List
import re
from collections import Counter

TEST_INPUT = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

class Tower(NamedTuple):
    name: str
    weight: int
    aboves: List[str]

def process_line(line: str):
    parts = line.split(" -> ")
    tower = parts[0]
    aboves = [] if len(parts) == 1 else parts[1].split(", ")

    rgx = r"([a-z]+) \(([0-9]+)\)"
    match = re.match(rgx, tower)
    name, weight = match.groups()
    weight = int(weight)

    return Tower(name, weight, aboves)

assert process_line("fwft (72) -> ktlj, cntj, xhth") == Tower('fwft', 72, ['ktlj', 'cntj', 'xhth'])
assert process_line("havc (66)") == Tower("havc", 66, [])


def find_bottom(towers: List[Tower]) -> Tower:
    are_aboves: Set[str] = set()
    have_aboves: Set[str] = set()

    for tower in towers:
        if tower.aboves:
            have_aboves.add(tower.name)
        for above in tower.aboves:
            are_aboves.add(above)

    # want the tower that has aboves but is not above
    good = [tower for tower in have_aboves if tower not in are_aboves]
    return good[0]

TEST_TOWERS = [process_line(line) for line in TEST_INPUT.split("\n")]
assert find_bottom(TEST_TOWERS) == 'tknk'


def balance_towers(towers: List[Tower]):
    lookups = { tower.name: tower for tower in towers }

    def check(tower: Tower):
        """
        Return the total weight and is_balanced
        """
        subchecks = {name: check(lookups[name]) for name in tower.aboves}
        subcheck_weights = {weight for weight, _ in subchecks.values()}
        is_balanced = len(subcheck_weights) <= 1
        weight = tower.weight + sum(weight for weight, _ in subchecks.values())

        if (len(subcheck_weights) > 1 and \
            all(is_balanced for _, is_balanced in subchecks.values())):
            print("tower", tower)
            # this is where the problem is
            for name, (total_weight, is_balanced) in subchecks.items():
                above_tower = lookups[name]
                print(name, total_weight, above_tower.weight)

        return weight, is_balanced

    root = lookups[find_bottom(towers)]

    check(root)

balance_towers(TEST_TOWERS)


if __name__ == "__main__":
    with open("day07_input.txt", "r") as f:
        towers = [process_line(line.strip()) for line in f]
    print(find_bottom(towers))
    balance_towers(towers)

