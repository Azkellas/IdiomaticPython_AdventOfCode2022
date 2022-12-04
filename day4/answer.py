import re

with open('example.txt') as file:
    lines = file.readlines()

    part1_score = 0
    part2_score = 0
    for line in lines:
        a1, a2, b1, b2 = map(int, re.findall(r'\d+', line))
        # if a1 <= b1 and a2 >= b2 or b1 <= a1 and b2 >= a2:
        if a1 <= b1 <= b2 <= a2 or b1 <= a1 <= a2 <= b2 >= a2:
            part1_score += 1
        if min(a2, b2) - max(a1, b1) >= 0:
            part2_score += 1
    print("part1:", part1_score)
    print("part2:", part2_score)
