
[How to follow this course](../README.md)

[Previous day](../day2)

# Day 3: Rucksack Reorganization

## Problem

You can find the puzzle [here](https://adventofcode.com/2022/day/3).
The exercise today is pretty straightforward: finding elements present in different strings. Let's dive right into it!

## First approach

First, we create a function to compute the priority of an item.

```python
def get_priority(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 26 + 1
```

> `islower` test if the string is lowercase.
> Remember that `ord` convert a char in an int following the ASCII table.

Then, for each string, split it in two in the middle with two slices.
```python
median = len(line) // 2  # // 2 makes sure the result is an int, and not a float
left, right = line[:median], line[median:]
```

And loop through the items of `left` to see if they are present in `right`
```python
def find_item(left, right):
    for c in left:
        if c in right:
            return c
```

Finally, for each line we add to the final score the priority of item.

```python
item = find_item(left, right)
score += get_priority(item)
```

And that's it for part 1!


## Improving our answer

The main issue of our solution is the `find_item` function.
Suppose `left` is _"aacdefghiZ"_ and `right` is _"ABCDEFGHIZ"_ (each **10** characters long).

Then, `find_item` will first try to find **a** in `right`, by comparing it to **A**, then **B**, ... finally **Z**.
Next step, it will try to find the second **a** in `right`, doing another **10** comparisons.
And so on until eventually, it will find **Z** in the two strings.
In the end, this process will have taken **10 * 10 = 100** comparisons.
While this is fine for short strings, were we given huge inputs it would have taken too long to find the item.

> The numbers of operations required to do a bigger operation is the complexity of the aforementioned operation. Here we need **n*n** operations to find the item, so we note it complexity _O(n²)_. Complexity is a complex subject (pun-intended), out of the scope of this course. You can read more about it [here](https://discrete.gr/complexity/). In the meantime, you can think of the complexity as "how slow my operation is".

It's time to use another collection.
Python comes with different containers for storing data. One of them is `list`, that we used until now.
`lists` preserve ordering and also allow duplicates.
This is why `file.readlines()` returns a list, because we wouldn't want the content shuffled.
However it comes with a cost: `lists` are terrible when we want to test `element in collection`.

But `sets` are built for it!
If `elt in list` requires _O(n)_ operations, `elt in set` is _O(1)_
(i.e. the time required will always be the same, regardless of the size of the set, while `elt in list` with `len(list) = 100_000` could require `100_000` tests).

> Two others major collections are `tuple` and `dict`. We will without a doubt use them later in the course.

Converting a `list` to a `set` is easy:
```python
left, right = set(left), set(right)
```
And the code runs! Let's see how `find_item` works behind the scenes:
Again, suppose `left` is _"aacdefghiZ"_ and `right` is _"ABCDEFGHIZ"_ (each `10` characters long).
```python
    for c in left:
        if c in right:
            return c
```

For the sake of simpicity, let's assume the small and constant cost of `if elt in set` is one operation.
Then, `find_item` will try to find **a** in `right`, in **1** operation.
Next it will try **c** (remember, only one **a** in `left`, no duplicates), again in **1** operation.
And so on until **Z**. In total it will have done **9** operations, and not **100** like before.
If our strings were **1000** characters long, we would have saved **999000** operations (minus the one to build the sets, but they are also around **1000** each).

> With sets, the complexity of `find_item` went from _O(n²)_ to _O(n)_.

Finding a common element between two sets is a recurring operation in programming, called an intersection. Fortunately, python comes with a shortcut operator for it, `&`. With it, `find_item` can be reduced to a single line:
```python
def find_item(left, right):
    return (left & right).pop()
```

`left & right` is a `set` with only one element in it (garanted by the puzzle statement). To get it, we use `pop()`, that removes a random element of a set and returns it. 

## Part 2

Part 2 is the same, except instead of cutting a line in half, we read them three by three.

```python
for i in range(0, len(lines), 3):
    line1, line2, line3 = lines[i:i+3]
    item = (set(line1.strip()) & set(line2.strip()) & set(line3.strip())).pop()
    score += get_priority(item)
```

`for i in range(0, len(lines), 3)` means `for i from 0 to len(lines), with a step of 3`, i.e. `0, 3, 6, ...`.
Then, using slices, we get the three lines we are interested in. Finally, since `a & b` returns a set, we can chain the intersections. 

> `strip()` is required to avoid finding the newline `\n` character in all sets

But now we have a `find_item` that works for two elements, and an intersection for three directly in the main loop. Let's make `find_item` general enough to handle any number of sets.

```python
def find_item(sets):
    return set.intersection(*sets).pop()
```

`a & b` is syntactic sugar for `a.intersection(b)`, which is itself syntactic sugar for `set.intersection(a, b)`.
`set.intersection` expects a list of `sets`, not a `list` of `sets`, which is why we added `*` before `sets`, to unpack the list.
Long story short, `set.intersection(*[a, b, c])` is `set.intersection(a, b, c)`.
Without the asterisk in the first code, `set.intersection` would receive a list, and complain it is not sets.

With this new and final `find_item` method, we can revamp our main loop like so:
```python
# part 1
for line in lines:
    median = len(line) // 2
    sets = [set(l.strip()) for l in [line[:median], line[median:]]]
    part1_score += get_priority(item)

...

# part 2
for i in range(0, len(lines), 3):
    sets = [set(line.strip()) for line in lines[i:i+3]]
    item = find_item(sets)
    part2_score += get_priority(item)
```


And we're done!

### Final remarks

Our solution is not the only one, simplest or fastest. Today's topic on the subreddit can be found [here](https://www.reddit.com/r/adventofcode/comments/zb865p/2022_day_3_solutions/?sort=confidence).


### References

- [`set`](https://www.w3schools.com/python/python_sets.asp)
- [python major collections](https://www.geeksforgeeks.org/differences-and-applications-of-list-tuple-set-and-dictionary-in-python/)
- [complexity in computer science](https://discrete.gr/complexity/)
- [complexity of operations for python collections](https://wiki.python.org/moin/TimeComplexity)
- [`range`](https://www.w3schools.com/python/ref_func_range.asp)