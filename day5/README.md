
[How to follow this course](../README.md)

[Previous day](../day4)

# Day 5: Supply Stacks


## Problem

You can find the puzzle [here](https://adventofcode.com/2022/day/5).
Some aoc puzzles are more about parsing than solving. Today is one of those days.

## Parsing the input

There are two steps today: the initial state, then the moves.

```python
with open('input.txt') as file:
    content = file.read()
    crates, moves = content.split('\n\n')
```

### Parsing the initial stacks

The most difficult part, as the data span on multiple lines, vertically.
While we could parse line by line, we'll do it stack by stack to stay coherent with the data we are trying to parse.

```python
crates = crates.split('\n')
crates.reverse()
```

We split the crates by line, then reverse the line order, since we need to read the stacks bottom to top.

```python
stack_count = int(crates[0].split()[-1])
### "1 2 3".split() == ["1", "2", "3"]
```
We find the last index by splitting the now first line by whitespaces and converting the last element to int.

> Note that we could have used `re.findall` like yesterday.

```python
stacks = [[] for _ in range(stack_count + 1)]
for stack_id in range(1, stack_count+1):
    ...
```

We create a list of list, each element being first an empty list, that we will complete based on what we read.

> We create one more element since the first stack id is 1 and not 0. The first element of stack will remain empty for the duration of the program.

```python
    stack_idx = crates[0].find(str(stack_id))
    for line in crates[1:]:
        char = line[stack_idx]
        if char != ' ':
            stacks[stack_id].append(char)
```
Then, step by step:
- `crates[0].find(str(stack_id))` finds where `stack_id` (e.g. **1**, **2**, etc.) is in the first line and returns the index.
So for `id` **1**, it will return **1**, then for `id` **2**, **5**, etc. This is the index of the crate column in the input.
The crate letters will be at the same index.
- For each line, get the character at this index. If it's not empty, push it to the stack.

And we're ready to execute the commands.

### Parsing the moves

Yesterday we learnt about _regex_, and we're going to use them again today. `map(int, re.findall(r'\d+', line))` would work today as well, but let's get fancy!

All the moves are formatted like this: _"move {count} from {origin} to {destination}"_.

```python
(count, origin, dest) = map(int, re.match(r'move (\d+) from (\d+) to (\d+)', move).groups())
```

- `re.match` tries to match the pattern provided to the input. 
- Again, `\d+` means _"number"_. 
- `()` is a capturing group. It means _"if you manage to match the string, extract this information"_.
So `(\d+)` means _"capture this number"_.
- `.groups()` returns the informations extracted, provided the match succeded, e.g. `["10", "1", "2",]` if the input was _"move 10 from 1 to 2"_.
- Finally, we map to ints like yesterday

This function is more complicated than yesterday, but we clearly state what we are looking for. For example, not _"annihilate crates 1, 2, and 10"_.

### Executing the moves

Now that we parsed everything, actually doing the command is easy.
```python
for i in range(count):
    part1_stacks[dest].append(part1_stacks[origin].pop())
```

> We saw `pop` during the third day for sets. For lists, it removes the last element and returns it.
> We do it `count` time, **1** crate by **1** crate, just like the crane would.

```python
part1_res = ""
for stack in part1_stacks[1:]:
    part1_res += stack[-1]
print("part1:", part1_res)
```
And part 1 is done!

## Part 2

Part 2 requires us to start over from the initial crate. You might be tempted to write something like this:
```python
part1_stacks = stacks
... # do part 1
part2_stacks = stacks
... # do part 2
```
only to discover it doesn't work. When we assign `stacks` to `part1_stacks`, we just create a binding between the two: `part1_stacks` is a reference to `stacks`:
```python
a = [1, 2]
b = a
b.append(3)
print(b) # [1, 2, 3]
print(a) # [1, 2, 3]
```

> This is not the case for basic types, like ints or floats that are copied by the assignement operator.

To create a copy of `stacks`, we're going to use the module `copy`:
```python
import copy
```
`copy` comes with two functions: `copy` and `deepcopy`.
- `copy` returns a _shallow copy_: the root object is copied, but all elements it might have inside are referenced.
- On the other hand, `deepcopy` recursively copy everything in the object.

```python
a = [[1], [2]]
b = copy.copy(a)
b.append([3])
print(b) # [[1], [2], [3]]
print(a) # [[1], [2]]  a was copied, so it wasn't affected by b.append

b[0].append(4)
print(b) # [[1, 4], [2], [3]]
print(a) # [[1, 4], [2]]  !! a was copied, but a[0] was just referenced, b[0].append also affects a[0]
```

```python
a = [[1], [2]]
b = copy.deepcopy(a)
b.append([3])
print(b) # [[1], [2], [3]]
print(a) # [[1], [2]] 

b[0].append(4)
print(b) # [[1, 4], [2], [3]]
print(a) # [[1], [2]]  no issue here, everything was deep copied
```

In our case, we have a list of lists, so we need a deepcopy to sperate properly the input stacks from part 1 stacks.

```python
part1_stacks = copy.deepcopy(stacks)
... # part 1 logic

part2_stacks = copy.deepcopy(stacks)
... # part 2 logic
```
> No need to deepcopy for part 2, since it's the last time we will need `stacks`, but it's better to mirror part 1.

Now we can solve part 2 without worry.
```python
part2_stacks[dest] += part2_stacks[origin][-count:]
part2_stacks[origin] = part2_stacks[origin][:-count]
```
- `dest += origin[-count:]` add the last `count` elements from the origin stack to destination.
- `origin = origin[:-count]` removes the last `count` elements from origin.


## Improving our answer

### Reduce

First, let's look at how we print the answer:

```python
part1_res = ""
for stack in part1_stacks[1:]:
    part1_res += stack[-1]
print("part1:", part1_res)
```

You're getting used to it: doing a for loop for a single line often means there is a function dedicated to it!
Applying a function to every element in a list and reducing it to a single value is the role of `functools.reduce`
```python
from functools import reduce
print("part1:", reduce(lambda acc, stack: acc+stack[-1], part1_stacks[1:], ""))
```

Before looking into how reduce works, let's explain the other new keyword: `lambda`: lambdas are small anonymous functions.
```python
lambda acc, stack: acc+stack[-1]
```
defines the same function as
```python
def fn(acc, stack):
    return acc + stack[-1]
```

but in a compact way. They are most useful when you want to pass a function to another and it's too small to deserve its own block. Its syntax is `lamba arguments: return_value`. Here our lambda takes two arguments, `acc` and `stacks`, and returns `acc + stack[-1]`.

Then, `reduce`. Its syntax is `reduce(f(acc, elt), list, initial_value)`. Let's see on an example how it works:
```python
elements = [1, 2, 3]
reduce(lambda acc, x: acc + x, elements, 0)
step 1:
    acc + elements[0] 
    0 + 1
    acc is now 1
step 2:
    acc + elements[1]
    1 + 2
    acc is now 3
step 2:
    acc + elements[2]
    3 + 3
    acc is now 6
step 3:
    no more element
    return acc = 6    
```
And we redefined `sum`. In our case, it starts from an empty string `""`, then for each stack after the empty stack **0**, it finds the element on top and adds it to the result.

### Moving stacks


Moving stacks one by one in step 1 is not optimal. Just like we did in part 2, we can do better.
```python
part1_stacks[dest] += part1_stacks[origin][-count:][::-1]
part1_stacks[origin] = part1_stacks[origin][:-count]
```

The only difference with part 2 is the `[::-1]` bit. Remember we saw earlier that we can slice a list or string with the `[start:end]`. Actually we can do better:
`[start:end:step]`, just like we wrote `range(start, end, steps)` in day 3. So `[::-1]` means slice from the beginning to the end of the list (i.e. get all elements), then iterate with a negative step of **1**, i.e. starts from end and go to start. It effectively reverse the list.

> During the stacks parsing, we wrote `crates = crates.split('\n'); crate.reverse()`. `crates.split('\n')[::-1]` is another way to do it

One last thing we can do is do both operations at the same time. One neat trick of python is the ability to swap variables like this `a, b = b, a`. We can get inspiration from it to do the same for our crates:

```python
part1_stacks[origin], part1_stacks[dest] = part1_stacks[origin][:-count], part1_stacks[dest] + part1_stacks[origin][-count:][::-1]
```

Admittedly, it obfuscates the code more than anything. But when we do the same for part2,

```python
part1_stacks[origin], part1_stacks[dest] = part1_stacks[origin][:-count], part1_stacks[dest] + part1_stacks[origin][-count:][::-1]
part2_stacks[origin], part2_stacks[dest] = part2_stacks[origin][:-count], part2_stacks[dest] + part2_stacks[origin][-count:]
```

We realise it's almost the same line.

### Final remarks

Our solution is not the only one, simplest or fastest. Today's topic on the subreddit can be found [here](https://www.reddit.com/r/adventofcode/comments/zcxid5/2022_day_5_solutions/).


### References

- [shallow and deep copy](https://docs.python.org/3/library/copy.html)
- [list slicing](https://www.programiz.com/python-programming/examples/list-slicing)
- [regex crash course in python](https://www.w3schools.com/python/python_regex.asp)
- [lambdas](https://www.w3schools.com/python/python_lambda.asp)
- [`reduce`](https://realpython.com/python-reduce-function/)