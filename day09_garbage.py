"""
https://adventofcode.com/2017/day/9
"""
from typing import NamedTuple

class StreamMetrics(NamedTuple):
    score: int
    garbage: int

def score(stream: str) -> StreamMetrics:
    total_score = 0
    depth = 0
    in_garbage = False
    negated = False

    garbage_count = 0

    for c in stream:
        #print(c, depth, total_score, in_garbage, negated)
        if negated:
            negated = False
            continue
        elif c == "!":
            negated = True
        elif in_garbage:
            if c == ">":
                in_garbage = False
            else:
                # This is the only case we want to count garbage
                garbage_count += 1
        elif c == "<":
            in_garbage = True
        elif c == "{":
            depth += 1
            total_score += depth
        elif c == "}":
            depth -= 1

    #print(total_score)
    return StreamMetrics(total_score, garbage_count)

assert score("{}").score == 1
assert score("{{{}}}").score == 6
assert score("{{},{}}").score == 5
assert score("{{{},{},{{}}}}").score == 16
assert score("{<a>,<a>,<a>,<a>}").score == 1
assert score("{{<ab>},{<ab>},{<ab>},{<ab>}}").score == 9
assert score("{{<!!>},{<!!>},{<!!>},{<!!>}}").score == 9
assert score("{{<a!>},{<a!>},{<a!>},{<ab>}}").score == 3
assert score("{{!}!}!<}<!>{>}}").score == 3

assert score("<>").garbage == 0
assert score("<random characters>").garbage == 17
assert score("<<<<>").garbage == 3
assert score("<{!>}>").garbage == 2
assert score("<!!>").garbage == 0
assert score("<!!!>>").garbage == 0
assert score("""<{o"i!a,<{i<a>""").garbage == 10

if __name__ == "__main__":
    with open("day09_input.txt") as f:
        stream = f.read().strip()
    print(score(stream))
