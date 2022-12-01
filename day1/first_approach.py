# Opening the example
with open('example.txt') as file:
    # Reading the content of the file
    # lines is a list of strings; eg ["1000\n", "2000\n", "3000\n", "\n", ...]
    # \n is the newline character
    lines = file.readlines()

    # Create a list that will contain the calories of each elf
    elves = []

    # Create a variable storing the current elf calories
    elf_calories = 0

    # For each line
    for line in lines:
        # check if this is a blank line
        # strip removes all whitespaces at the beginning and end of the string
        # here line is "\n" (newline character), so it becomes ""
        if line.strip() == "":
            # it's a blank: we finished reading an elf
            # we append the calories to the list and reset the calory counter
            elves.append(elf_calories)
            elf_calories = 0
        else:
            # we convert the line into an int
            item_calories = int(line)
            # and add it to the calories counter
            elf_calories += item_calories


    # Now elves countain the total calories for each elf
    # We need to find the maximum of it
    # it can be done with the function max
    result = max(elves)
    print(result)