"""
https://adventofcode.com/2017/day/16
"""
from typing import Dict, List
from string import ascii_lowercase

TEST_INPUT = ascii_lowercase[:5]

class Dance:
    def __init__(self, dancers: str) -> None:
        self.dancers = [c for c in dancers]
        self.index: Dict[str, int] = {}
        self._make_index()

    def _make_index(self) -> None:
        self.index = {c: i for i, c in enumerate(self.dancers)}

    def spin(self, n: int) -> None:
        self.dancers = self.dancers[-n:] + self.dancers[:-n]
        self._make_index()

    def exchange(self, a: int, b: int) -> None:
        dancer_a = self.dancers[a]
        dancer_b = self.dancers[b]

        self.dancers[a] = dancer_b
        self.dancers[b] = dancer_a
        self.index[dancer_a] = b
        self.index[dancer_b] = a

    def partner(self, a: str, b: str) -> None:
        idx_a = self.index[a]
        idx_b = self.index[b]

        self.dancers[idx_a] = b
        self.dancers[idx_b] = a
        self.index[a] = idx_b
        self.index[b] = idx_a

def move_dancers(dance: Dance, move: str) -> None:
    move_type = move[0]
    move_details = move[1:]

    if move_type == 's':
        n = int(move_details)
        dance.spin(n)
    elif move_type == 'x':
        a, b = move_details.split("/")
        dance.exchange(int(a), int(b))
    elif move_type == 'p':
        a, b = move_details.split("/")
        dance.partner(a, b)
    else:
        raise ValueError(f"invalid move: {move}")

TEST_DANCE = Dance(TEST_INPUT)
move_dancers(TEST_DANCE, 's1')
move_dancers(TEST_DANCE, 'x3/4')
move_dancers(TEST_DANCE, 'pe/b')
assert TEST_DANCE.dancers == ['b', 'a', 'e', 'd', 'c']
assert TEST_DANCE.index == {'a': 1, 'b': 0, 'c': 4, 'd': 3, 'e': 2}

def cycle(dance: Dance, moves: List[str], n: int) -> None:
    for _ in range(n):
        for move in moves:
            move_dancers(dance, move)


if __name__ == '__main__':
    dance = Dance(ascii_lowercase[:16])
    abc = list(ascii_lowercase[:16])
    with open('day16_input.txt') as f:
        moves = f.read().strip().split(',')

    # for i in range(1_000_000_000):
    #     if i % 1_000_000 == 0:
    #         print(i)
    #     for move in moves:
    #         move_dancers(dance, move)
    #     state = dance.dancers
    #     if state == abc:
    #         print("cycle at", i)
    #         break

    cycle(dance, moves, 1_000_000_000 % 60)
    print(''.join(dance.dancers))
