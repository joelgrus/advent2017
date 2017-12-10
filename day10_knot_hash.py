"""
https://adventofcode.com/2017/day/10
"""
from typing import NamedTuple, List


class State(NamedTuple):
    numbers: List[int]
    pos: int = 0
    skip_size: int = 0


def step(state: State, length: int) -> State:
    numbers = state.numbers[:]
    N = len(numbers)
    start = state.pos
    skip_size = state.skip_size

    end = (state.pos + length) % N

    #print("start", start)
    #print("length", length)
    #print("end", end)

    if length == 0:
        pass
    elif start < end:
        # no wraparound
        numbers[start:end] = list(reversed(numbers[start:end]))
    else:
        # wraparound
        # N = 7  [0, 1, 2, 3, 4, 5, 6]
        #           end        start
        # start = 5 and end = 2
        numbers_to_reverse = numbers[start:] + numbers[:end]
        reversed_numbers = list(reversed(numbers_to_reverse))

        wrap_at = N - start

        numbers[start:] = reversed_numbers[:wrap_at]
        numbers[:end] = reversed_numbers[wrap_at:]

    start = (start + skip_size + length) % N
    skip_size += 1

    return State(numbers, start, skip_size)

TEST_STATE = State([0, 1, 2, 3, 4])

state = TEST_STATE
for length in [3, 4, 1, 5]:
    #print("length", length)
    state = step(state, length)
    #print(state)
assert state == State([3,4,2,1,0], 4, 4)

def encode(s: str) -> List[int]:
    return [ord(c) for c in s] + [17, 31, 73, 47, 23]

assert encode("1,2,3") == [49,44,50,44,51,17,31,73,47,23]

def xor16(xs: List[int]) -> int:
    """
    xor all 16 numbers together
    """
    assert len(xs) == 16

    result = xs[0]
    for x in xs[1:]:
        result = result ^ x

    return result

assert xor16([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]) == 64


def sparse_to_dense(xs: List[int]) -> List[int]:
    assert len(xs) == 256

    return [xor16(xs[start:(start+16)])
            for start in range(0, 256, 16)]

assert sparse_to_dense([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22] * 16) == [64] * 16


def hexit(x: int) -> str:
    # hex returns something like '0x1' or '0xff'
    # we need to throw away the first two chars
    # and maybe add a leading 0
    h = hex(x)[2:]

    assert 1 <= len(h) <= 2

    return h if len(h) == 2 else '0' + h

assert hexit(64) == "40"
assert hexit(7) == "07"
assert hexit(255) == "ff"

def knot_hash(s: str) -> str:
    s = s.strip()
    lengths = encode(s)  # List[int]
    state = State([num for num in range(256)])

    for round in range(64):
        for length in lengths:
            state = step(state, length)

    sparse_hash = state.numbers
    dense_hash = sparse_to_dense(sparse_hash)

    return ''.join([hexit(x) for x in dense_hash])

assert knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
assert knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
assert knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
assert knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

if __name__ == "__main__":
    s = '199,0,255,136,174,254,227,16,51,85,1,2,22,17,7,192'
    print(knot_hash(s))


#if __name__ == "__main__":
    # lengths = [199,0,255,136,174,254,227,16,51,85,1,2,22,17,7,192]
    # state = State(list(range(256)))
    # for length in lengths:
    #     state = step(state, length)
    #     #print(state)
    # print(state.numbers[0] * state.numbers[1])
