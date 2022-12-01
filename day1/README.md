## Problem

Let's solve our first day and save ~~the world~~ Christmas!
You can find the puzzle [here](https://adventofcode.com/2022/day/1).
Today's problem consist of a list of ints. Elves wrote the calories of the food they have, one item per line. A empty line separates elves.
Our first task consists of finding the elf carrying the most calories.

Before starting, we will save our unique input and the example provided. You will find in this folder the example but not the input, as each user has their own input. Be wary of extra lines at the end of the file when copy-pasting examples or making custom tests. All days have at least one example provided, so we can debug our program.


## First approach

Before solving on our custom input, we'll work on the example to make sure we have a correct understanding of the problem.

### Reading the input

To read a file, we write
```python3
# Opening the example
with open('example.txt') as file:
    # read returns a string containing all text in the file
    content = file.read()
    # lines returns an array of string (each string ending in \n, the character for newline)
    lines = file.readlines()
    
```

Then we will read each line to compute the calories stored by each elf
```python3
# Create a list that will contain the calories of each elf
elves = []

# Create a variable storing the current elf calories
elf_calories = 0

# For each line
for line in lines:
    # Check if this is a blank line
    if line == "\n":
        # It's a blank: we finished reading an elf
        # We append the calories to the list and reset the calory counter
        elves.append(elf_calories)
        elf_calories = 0
    else:
        # We convert the line into an int
        item_calories = int(line)
        # And add it to the calories counter
        elf_calories += item_calories
```

Now `elves` countain the total calories for each elf and we just need to find the biggest element inside it:
```python3
result = max(elves)
print(result)
```

And we find `24000`, the correct answer for the example.
If we replace `open('example.txt')` by `open('input.txt')`, we'll have the answer for the first part.

## Improving our answer

Before doing part 2, let's improve our answer:

```python3 
elves_string = content.split("\n\n")
```
Since we know elves are separated by a blank line, we split by `"\n\n"`.

`string.split(pattern)` looks for the `pattern` provided (here a blankline, `"\n\n"`) in the string and returns a list of strings.
For example, `"a_c".split("_")` returns `["a", "c"]`.

So here we extracted the string representing each elf. Now we can write a function that will compute the total calories held by one elf:
```python3
def get_calories(elf_string):
    # Again, we split to get a list of items
    items = elf_string.split("\n")
    # Then we parse each item string into an int, with map
    items = map(int, items)
    return sum(items)
```

`map` is a function with two arguments:
- a function `f` that will be applied to each element of a list
- a list

For example, `map(f, [a, b, c])` returns `[f(a), f(b), f(c)]`.
It's a good way to replace a for-loop.

Note that map() returns a map object, if you want a list, you can do `list(map(...))`

We can improve our function even more:
```python3
def get_calories(elf_string):
    items = map(int, elf_string.split("\n"))
    return sum(items)
```

or even 
```python3
def get_calories(elf_string):
    return sum(map(int, elf_string.split("\n")))
```

Now we just need to apply this function to every elf, with another map:
```python3
elves = list(map(get_calories, elves_string))
print(max(elves))
```
And we have our answer.


### Part 2

For part 2, we need to output the sum of the three elves having the most calories.
Keeping the `elves` array computed in the first part, we do:

```python3
# Sorting the list in descending order 
elves.sort(reverse=True)
print(sum(elves[:3]))
```
The `[:3]` syntax is a slice.
A slice is a method to extract only the element we want in an list.
`elements[start:end]` will create a new list with the elements with indices `start` (included) to `end` (excluded). If we don't specify `start` of `end`, it means we start from the very beginning or go to the very end of the list.

We can also use negative numbers: `elements[-3:]` means we will keep the last three elements of the array.

So in our case, we only keep the three first elves and get the sum of the calories they have.

And with it we solved day 1!


### Final remarks

Note that our solution is not the only one, simplest or fastest. If you visit the [subreddit](https://www.reddit.com/r/adventofcode), you will see that each day has its dedicated post, where many people share their answers. Today's topic can be found [here](https://www.reddit.com/r/adventofcode/comments/z9ezjb/2022_day_1_solutions/?sort=confidence). For example, it was possible to combine everything in a single line to print the answer of part 1.

```python3
print(max([sum(list(map(int,line.split()))) for line in open('example.txt').read().split('\n\n')]))
```
