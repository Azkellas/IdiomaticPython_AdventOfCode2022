import re
from copy import deepcopy
from functools import reduce

with open('example.txt') as file:
    crates, moves = file.read().split('\n\n')
    crates = crates.split('\n')
    crates.reverse()
    stack_count = int(crates[0].split()[-1])

    stacks = [[] for _ in range(stack_count + 1)]
    for stack_id in range(1, stack_count+1):
        stack_idx = crates[0].find(str(stack_id))
        for line in crates[1:]:
            if line[stack_idx] != ' ':
                stacks[stack_id].append(line[stack_idx])

    part1_stacks = deepcopy(stacks)
    part2_stacks = deepcopy(stacks)
    for move in moves.split("\n"):
        (count, origin, dest) = map(int, re.match(r'move (\d+) from (\d+) to (\d+)', move).groups())
        part1_stacks[origin], part1_stacks[dest] = part1_stacks[origin][:-count], part1_stacks[dest] + part1_stacks[origin][-count:][::-1]
        part2_stacks[origin], part2_stacks[dest] = part2_stacks[origin][:-count], part2_stacks[dest] + part2_stacks[origin][-count:]

    print("part1:", reduce(lambda acc, stack: acc+stack[-1], part1_stacks[1:], ""))
    print("part2:", reduce(lambda acc, stack: acc+stack[-1], part2_stacks[1:], ""))
