"""
https://adventofcode.com/2017/day/17
"""
from typing import NamedTuple

class CircularBuffer:
    def __init__(self) -> None:
        self.buffer = [0]
        self.pos = 0

    def step_forward(self, step_size: int) -> None:
        n = len(self.buffer)
        self.pos = (self.pos + step_size) % n

    def insert(self, value: int) -> None:
        self.buffer = (self.buffer[:(self.pos + 1)] +
                       [value] +
                       self.buffer[(self.pos+1):])
        self.pos += 1

    def value_after(self) -> int:
        idx = (self.pos + 1) % len(self.buffer)
        return self.buffer[idx]


def spinlock(step_size: int, num_spins: int) -> CircularBuffer:
    cb = CircularBuffer()
    for i in range(1, num_spins + 1):
        cb.step_forward(step_size)
        cb.insert(i)
    return cb

TEST_BUFFER = spinlock(step_size=3, num_spins=2017)
assert TEST_BUFFER.value_after() == 638

def second_spot(step_size: int, num_spins: int) -> int:
    """
    Return the value in the second spot
    """
    length = 1
    pos = 0
    second = None

    for i in range(1, num_spins + 1):
        if i % 1_000_000 == 0:
            print(i)

        # step forward
        pos = (pos + step_size) % length

        if pos == 0:
            # replace second
            second = i

        length += 1

        pos = (pos + 1) % length

    return second

if __name__ == "__main__":
    buffer = spinlock(step_size=367, num_spins=2017)
    print(buffer.value_after())

    print(second_spot(step_size=367, num_spins=50_000_000))
