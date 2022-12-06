import re
from copy import deepcopy

with open('example.txt') as file:
    content = file.read()
    crates, moves = content.split('\n\n')
    crates = crates.split('\n')
    crates.reverse()
    stack_count = int(crates[0].split()[-1])

    stacks = [[] for _ in range(stack_count + 1)]
    for stack_id in range(1, stack_count+1):
        stack_idx = crates[0].find(str(stack_id))
        for line in crates[1:]:
            char = line[stack_idx]
            if char == ' ':
                break
            stacks[stack_id].append(char)

    part1_stacks = deepcopy(stacks)
    for move in moves.split("\n"):
        (count, origin, dest) = map(int, re.match(r'move (\d+) from (\d+) to (\d+)', move).groups())
        for i in range(count):
            part1_stacks[dest].append(part1_stacks[origin].pop())

    part1_res = ""
    for stack in part1_stacks[1:]:
        part1_res += stack[-1]

    part2_stacks = deepcopy(stacks)
    for move in moves.split("\n"):
        (count, origin, dest) = map(int, re.match(r'move (\d+) from (\d+) to (\d+)', move).groups())
        part2_stacks[dest] += part2_stacks[origin][-count:]
        part2_stacks[origin] = part2_stacks[origin][:-count]
    part2_res = ""
    for stack in part2_stacks[1:]:
        part2_res += stack[-1]


    print("part1:", part1_res)
    print("part2:", part2_res)