def get_result(line, window):
    for i in range(len(line)):
        if len(set(line[i:i+window])) == window:
            return i+window

with open('example.txt') as file:
    line = file.read()
    print("part1", get_result(line, 4))
    print("part1", get_result(line, 14))
