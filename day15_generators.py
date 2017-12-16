"""
https://adventofcode.com/2017/day/15
"""
from typing import Iterator, Callable
import itertools

class Generator:
    MOD = 2147483647

    def __init__(self, factor: int, prev: int, test: Callable[[int], bool] = None) -> None:
        self.factor = factor
        self.prev = prev
        self.test = test or (lambda _: True)

    def next(self) -> int:
        passed_test = False
        while not passed_test:
            next_value = (self.factor * self.prev) % self.MOD
            self.prev = next_value
            passed_test = self.test(next_value)
        return next_value

GEN_A = Generator(16807, 65, lambda x: x % 4 == 0)
GEN_B = Generator(48271, 8921, lambda x: x % 8 == 0)

def count_matches(gen_a: Generator, gen_b: Generator, n: int = 40000000) -> int:
    count = 0
    for i in range(n):
        if i % 100000 == 0:
            print("i", i)
        a = gen_a.next()
        b = gen_b.next()
        if a % 65536 == b % 65536:
            count += 1
    return count

# print(count_matches(GEN_A, GEN_B, 5000000))

if __name__ == "__main__":
    gen_a = Generator(16807, 289, lambda x: x % 4 == 0)
    gen_b = Generator(48271, 629, lambda x: x % 8 == 0)
    print(count_matches(gen_a, gen_b, 5000000))
