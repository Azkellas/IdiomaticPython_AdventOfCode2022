def get_score(line):
    match line:
        case "A X": return 1 + 3 # Rock + draw
        case "A Y": return 2 + 6 # Paper + win
        case "A Z": return 3 + 0 # Scissors + lose
        case "B X": return 1 + 0 # Rock + lose
        case "B Y": return 2 + 3 # Paper + draw
        case "B Z": return 3 + 6 # Scissors + win
        case "C X": return 1 + 6 # Rock + win
        case "C Y": return 2 + 0 # Paper + lose
        case "C Z": return 3 + 3 # Scissors + draw

# Opening the example
with open('example.txt') as file:
    lines = file.readlines()

    part1_score = sum([get_score(line.strip()) for line in lines])

    # part 2
    part2_score = 0
    for line in lines:
        opponent = ord(line[0]) - ord('A')
        strategy = ord(line[2]) - ord('X')
        my_move = (opponent + (strategy - 1)) % 3
        part2_score += (my_move + 1) + 3 * strategy

    print("part 1:", part1_score)
    print("part 2:", part2_score)
