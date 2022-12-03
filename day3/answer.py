def get_priority(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 26 + 1

def find_item(sets):
    return set.intersection(*sets).pop()

# Opening the example
with open('example.txt') as file:
    lines = file.readlines()

    part1_score = 0
    for line in lines:
        median = len(line) // 2
        sets = [set(l.strip()) for l in [line[:median], line[median:]]]

        # sets = [set(line[:median].strip()), set(line[median:].strip())]
        item = find_item(sets)
        part1_score += get_priority(item)
    print("part1:", part1_score)

    part2_score = 0
    for i in range(0, len(lines), 3):
        line1, line2, line3 = lines[i:i+3]
        sets = [set(line.strip()) for line in lines[i:i+3]]
        item = find_item(sets)
        part2_score += get_priority(item)
    print("part2:", part2_score)
