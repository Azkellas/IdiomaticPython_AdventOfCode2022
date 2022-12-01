def get_calories(elf_string):
    # Splitting the string to get an array of items
    # Then parsing the strings to get a list of ints
    # Finally returning the sum of the list
    return sum(map(int, elf_string.split("\n")))

# Opening the example
with open('example.txt') as file:
    # Reading the content of the file in one big string
    content = file.read()

    # Splitting to get a list of elves
    elves_string = content.split("\n\n")
    
    # Applying our function to get the total calories of each elf
    elves = list(map(get_calories, elves_string))
    
    # Getting the max of the list
    print("part1:", max(elves))

    # Sort in descending order
    elves.sort(reverse=True)
    # Getting the sum of the first three elves
    print("part2:", sum(elves[:3]))
