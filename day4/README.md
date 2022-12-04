
[How to follow this course](../README.md)

[Previous day](../day3)

# Day 4: Camp Cleanup

## Problem

You can find the puzzle [here](https://adventofcode.com/2022/day/4).
Today we need to find overlapping intervals.

But first, parsing.

## Parsing the input

There isn't much to say about today's puzzle, so let's use the time we have to introduce a parsing tool: regular expressions.

[Regular expressions](https://en.wikipedia.org/wiki/Regular_expression) (or _regex_, for short) are extremely powerful to parse data, yet also extremely abstruse.
We will use a small subset of what it's capable of for now, and introduce features as we need them later. 

The lines in our input as formatted like this: `a-b,c-d`, where `a`, `b`, `c` and `d` are numbers.
Ignoring the dashes and comma, what we want is to find all numbers in a line.
```python
import re
numbers = re.findall(r'\d+', line)
```
There is a lot to deconstruct here:
- `import re` imports the regex module in our code
- `r''` means *"raw strings"*. `\` is an escape character: it modifies what comes after it.
In usual strings `\n` is a newline character, not a backlash followed by an *n*.
Prepending the string by an **r** means all characters must be taken *as is*, so `r'\n'` is two chars.
- `\d` is a *special sequence* in regex, looking for a **d**igit.
There are many different special sequences, to look for letters, blank characters, etc. You can find a comprehensive list [here](https://www.w3schools.com/python/python_regex.asp).
- `\d+` means looking for a sequence of multiple consecutive digits: `\d` finds **0** but not **10** (two digits). `\d+` finds both.
- Finally `re.findall(r'\d+', line)` finds all numbers in the line provided.

Examples:
```python
re.findall(r'\d+', '10-20,0,5') == ['10', '20', '0', '5']
re.findall(r'\d', '10-20,0,5') ==  ['1', '0', '2', '0', '0', '5'] # looking for single digits, not numbers
```

> Note that `re.findall` returns a list of strings, even if we are looking for numbers.

So parsing the line is now as simple as:
```python
a1, a2, b1, b2 = map(int, re.findall(r'\d+', line)) # int is also a function! int("10") = 10
```

## Part 1

They are many ways to determine whether an interval is contained within another, and I'm sure you found one already.
Let's call `(a1, a2)` the first interval, and `(b1, b2)` (so the line is *"a1-a2,b1-b2"*). In the input, we are garanteed `a1 <= a2` and `b1 <= b2`.
So, interval **b** is inside **a** if `a1 <= b1 and b2 <= a2`.
Python is one of the few languages to allow chaining comparison operators, so we can write `if a1 <= b1 <= b2 <= a2`.
And the other way for **a** inside **b**.
```python
a1, a2, b1, b2 = map(int, re.findall(r'\d+', line))
if a1 <= b1 <= b2 <= a2 or b1 <= a1 <= a2 <= b2:
    part1_score += 1
```

## Part 2

Computing the intersection is not that different: **a** and **b** intersect if `min(a2, b2)` is greater than `max(a1, b1)`.
```python
a1, a2, b1, b2 = map(int, re.findall(r'\d+', line))
if min(a2, b2) - max(a1, b1) >= 0:
    part2_score += 1
```


### Final remarks

This is only the beginning of regex. As you've seen, they are really useful, and we barely touch the surface of what they are capable of.

We also could have used sets here. It is less efficient, but here's the code.

```python
a, b = set(range(a1, a2+1)), set(range(b1, b2+1))
part1_score += a <= b or b <= a  # a <= b tests if all elements of a are in b
part2_score += len(a & b) > 0    # intersection, like yesterday
```
> The reason it is less efficient is because the set contains all the elements of the interval, while we worked with the bounds only in our answer.

Our solution is not the only one, simplest or fastest. Today's topic on the subreddit can be found [here](https://www.reddit.com/r/adventofcode/comments/zc0zta/2022_day_4_solutions/?sort=confidence).


### References

- [regex crash course in python](https://www.w3schools.com/python/python_regex.asp)
