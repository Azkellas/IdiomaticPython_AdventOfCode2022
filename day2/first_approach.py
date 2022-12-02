# Opening the example
with open('example.txt') as file:
    score = 0
    for line in file.readlines():
        match line.strip():
            case "A X": score += 1 + 3 # Rock + draw
            case "A Y": score += 2 + 6 # Paper + win
            case "A Z": score += 3 + 0 # Scissors + lose
            case "B X": score += 1 + 0 # Rock + lose
            case "B Y": score += 2 + 3 # Paper + draw
            case "B Z": score += 3 + 6 # Scissors + win
            case "C X": score += 1 + 6 # Rock + win
            case "C Y": score += 2 + 0 # Paper + lose
            case "C Z": score += 3 + 3 # Scissors + draw
    print(score)
