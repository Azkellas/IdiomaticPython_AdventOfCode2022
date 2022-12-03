def get_priority(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 26 + 1

def find_item(left, right):
    for c in left:
        if c in right:
            return c

# Opening the example
with open('example.txt') as file:
    score = 0
    for line in file: # stricly equivalent to for line in file.readlines()
        median = len(line) // 2
        left, right = line[:median], line[median:]
        item = find_item(left, right)
        score += get_priority(item)
    print(score)