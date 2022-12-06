
[How to follow this course](../README.md)

[Previous day](../day5)

# Day 6: Tuning Trouble

## Problem

You can find the puzzle [here](https://adventofcode.com/2022/day/6).
Today was a resting day. If you followed this course until now, you should have had no trouble solving it on your own.

## Solving part 1

```python
for i in range(len(line)):
    if len(set(line[i:i+4])) == 4:
        print(i+4)
        break
```

And yeah. That's it for part 1.
A small breakdown just in case:
- `line[i:i+4]` extract the four consecutives characters starting at index `i`
- since sets don't allow duplicates, testing if all elements are unique in a list is just testing the length of the resulting set against the length of the list.
If the list had duplicates, the set would be smaller.

## Solving part 2

Part 2 is part 1 with another magic number, **14** instead of **4**. Since we want duplicates neither in the string, nor in our code, we will encapsulate our logic in a function.
```python
def get_result(line, window):
    for i in range(len(line)):
        if len(set(line[i:i+window])) == window:
            return i+window
print("part1", get_result(line, 4))
print("part1", get_result(line, 14))
```

And well, that's it for today! Congratulations for reaching this point, you rock!

### Final remarks

Today's topic on the subreddit can be found [here](https://www.reddit.com/r/adventofcode/comments/zdw0u6/2022_day_6_solutions/?sort=confidence).
