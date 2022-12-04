import re

with open('example.txt') as file:
    lines = file.readlines()

    part1_score = 0
    part2_score = 0
    for line in lines:
        a1, a2, b1, b2 = map(int, re.findall(r'\d+', line))
        a, b = set(range(a1, a2+1)), set(range(b1, b2+1))
        part1_score += a <= b or b <= a
        part2_score += len(a & b) > 0
    print("part1:", part1_score)
    print("part2:", part2_score)
