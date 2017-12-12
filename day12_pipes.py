"""
https://adventofcode.com/2017/day/12
"""
from typing import List, Tuple, Dict, Set

def parse_line(line: str) -> Tuple[int, List[int]]:
    """
    2 <-> 0, 3, 4
    """
    source, targets = line.split(" <-> ")
    targets = [int(x) for x in targets.split(", ")]
    return int(source), targets

assert parse_line("2 <-> 0, 3, 4") == (2, [0, 3, 4])

def build_graph(lines: List[str]) -> Dict[int, List[int]]:
    graph: Dict[int, List[int]] = {}
    for line in lines:
        source, targets = parse_line(line)
        graph[source] = targets
    return graph

TEST_INPUT = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

TEST_GRAPH = build_graph(TEST_INPUT.split("\n"))

def reachable_from(graph: Dict[int, List[int]], source: int = 0) -> Set[int]:
    frontier = [source]
    reachable: Set[int] = set()

    while frontier:
        program = frontier.pop()
        reachable.add(program)
        for next_program in graph.get(program, []):
            if next_program not in reachable and next_program not in frontier:
                frontier.append(next_program)

    return reachable

# assert reachable_from(TEST_GRAPH) == {0, 2, 3, 4, 5, 6}

def count_groups(graph: Dict[int, List[int]]):
    num_groups = 0

    seen: Set[int] = set()

    # the nodes in the graph
    for source in graph:
        print(source, source in seen)
        if source not in seen:
            group = reachable_from(graph, source)
            print(group)
            seen = seen | group
            num_groups += 1

    return num_groups

print(count_groups(TEST_GRAPH))


if __name__ == "__main__":
    with open("day12_input.txt") as f:
        lines = [line.strip() for line in f]
        graph = build_graph(lines)
        group = reachable_from(graph, 0)
        print(group)
        print(len(group))

        print(count_groups(graph))
