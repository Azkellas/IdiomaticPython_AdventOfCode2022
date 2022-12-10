
[How to follow this course](../README.md)

[Previous day](../day6)

# Day 7: No Space Left On Device

## Problem

You can find the puzzle [here](https://adventofcode.com/2022/day/7).
Since yesterday was really short, we'll work extra hard today.
This chapter will introduce many new ideas, more related to computer science as a whole than python.


## Building a tree

We are going to replicate the filesystem structure in our code with classes.

### File

```python
class File:
    def __init__(self, name, size, parent):
        self.name = name
        self.size = size
        self.parent = parent

    def get_size(self):
        return self.size
```

`File` is a class, storing three values:
- its `name`
- its `size`
- its `parent`, i.e. the folder it is into.

and has one method:

- `get_size`, simply returning its `size`.

### Folder

```python
class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.content = []
        self.parent = parent
    
    def get_size(self):
        return sum([item.get_size() for item in self.content])

    def add_file(self, name, size):
        self.content.append(File(name, size, self))

    def add_folder(self, name):
        self.content.append(Folder(name, self))

    def get_folder(self, name):
        return next(filter(lambda item: isinstance(item, Folder) and item.name == name, self.content))
```

`Folder` also has three attributes:
- its `name`
- its `content`, i.e. the files and folders it contains, starting empty.
- its `parent`, i.e. the folder it is into (or `None` for the root folder `/`).

and four methods:
- `get_size`, which is the sum of the sizes of the elements it holds
- `add_file` to store a file in its content
- `add_folder` to add a folder in its content
- `get_folder` to find a folder inside it by its name

> `get_size` is a **recursive** function: to determine the size of a folder, `get_size` is called on all the folders contained in it,
> which in turn can also call `get_size` on their content.
> Recursive functions are functions that call themselves until they reach a base case. For example, 
> ```python
> def compute_sum(n):
>     if n == 0:
>         return 0
>     return n + compute_sum(n-1)
>```
> will call itself until 0: `compute_sum(5)` is `5 + (4 + (3 + (2 + (1 + (0)))))`

`get_folder` introduces two new functions: `next` and `filter`.
`filter(predicate, list)` is roughly equivalent to `[elt for elt in list if predicate(elt)]`, but returns an iterator instead of a list.
Iterators are lazily evaluated: `next(iter)` finds the first element of the iterator then stops.
On the contrary `[elt for elt in list if predicate(elt)][0]` computes the whole list, then returns the first element.
If the folder we're looking for is the first of the `content` list, using an iterator will then be much faster!

> Since file names and folder names are unique, we could have used a set instead of a list for the content.

The data structure we implemented is a [tree](https://en.wikipedia.org/wiki/Tree_(data_structure)) that mimicks the folder provided in input.
Trees are widely used data structures with an almost infinite amount of litterature.

```
                            Folder('/')
                            /         \
                           /           \
                          /             \
                Folder('/sub1')     Folder('/sub2')
                /           \                   \
               /             \                   \
              /               \                   \
        Folder('/sub1/a')   Folder('/sub1/b')    Folder('/sub2/c')
            |                  /           \                  |
            |                 /             \                 |
            |                /               \                |
File('/sub1/a/f')   File('/sub1/b/g') File('/sub1/b/h')   File('/sub2/c/i')
```

Trees in computer science are similar to trees in real life, except they are top-down and not bottom up.
- They consists of *nodes* (Folders, Files) and *edges* (**/sub1** contains **/sub1/a**).
- They start with a *root* node.
- Each node has one and only one parent, except for the root that has none.
- The resulting graph is acyclic, i.e. there is no loop in the tree.

A directory structure is a tree.

Let's recall our `get_size` function.
1. `Folder('/').get_size` calls `get_size` on `Folder('/sub1')`
2. ____`Folder('/sub1')` calls `get_size` on `Folder('/sub1/a')`
2. ________`Folder('/sub1/a')` calls `get_size` on `File('/sub1/a/f')` that immediately returns a value
3. ________`Folder('/sub1/a')` returns this value to `Folder('/sub1')`
4. ____`Folder('/sub1')` subsequentely asks `Folder('/sub1/b')` for its size.
5. and so on until all *nodes* have been visited.
`get_size` is a *recursive* function that visits the whole tree before returning.

> `get_size` is a *depth first search*: to compute the size of a folder,
we need to go all the way down to the files before coming back up. `Folder('/').get_size` visits **/sub1/a** before **/sub2**.  

## Creating the tree

We have everything we need to answer the puzzle now!

```python
root = Folder('/')
current_folder = root

for line in file.readlines():
    match line.split():
        case '$', 'cd', '/':
            current_folder = root
        case '$', 'cd', '..': 
            current_folder = current_folder.parent
        case '$', 'cd', name:
            current_folder = current_folder.get_folder(name)
        case '$', 'ls':
            pass
        case 'dir', name:
            current_folder.add_folder(name)
        case filesize, _:
            current_folder.add_file(line[1], int(filesize))
```

We start by creating the root node `'/'` of the file tree, and a `current_directory` variable that will point to the directory the input currently is.
Then, we parse each line with a structural pattern matching.
- if the line is `$ cd /`, we go back to root
- if it is `$ cd ..`, we go to the parent of the current directory, e.g. from **/sub1/a** to **/sub1**
- if it is `$ cd name`, we find the folder with this name in the current directory and go within it.
- if it is `dir name`, we create such a folder in the current directory content
- otherwise, it is `size file`, and we create it in the current directory content

> We ignore `$ ls` that holds no value.

## Solving both parts

Since we have the tree all built up, we just need to compute the sizes of all folders, which we do with another recursive function:
```python
    sizes = []
    def rec(folder):
        sizes.append(folder.get_size())
        for f in folder.content:
            if isinstance(f, Folder):
                rec(f)
    rec(root)
```

`rec` (for *recursive*) will first compute the size of the folder given as parameter, save it in `sizes`, then call the function on all subfolders.
And will do the same thing for all subfolders and subsubfolders recursively.

So calling `rec(root)` will compute the size of all folders and save them in the `sizes` list.

> You might have noticed that `rec`, to compute the size of **/** will compute the size of **/sub1**,
> and then call `rec(Folder('/sub1'))`, effectively recomputing its size.
> `Folder('/sub1')` will be computed twice, `Folder('/sub1/a')` thrice, etc. which is extremely inefficient.
> Since this is a first introduction to tree graphs and recursion, this will be good enough for today.
> Optimizing `rec` so that each file and folder is only seen once is an exercise left to the reader. (Hint: try merging `rec` and `get_size`)

Now that we know the size of all folders, computing the answers for both parts is trivial:
```python
print("part1:", sum([s for s in sizes if s < 100_000]))

space_on_disk = 70_000_000
space_needed = 30_000_000
space_occupied = root.get_size()
space_required = space_needed - (space_on_disk - space_occupied)
print("part2", min([s for s in sizes if s >= space_required]))
```


## Final remarks

This was a difficult day. Feel free to revisit this chapter later.
Most people avoided the struggle of the tree structure by using a dict and storing the path as a dict.
You can find such a solution [here](https://www.reddit.com/r/adventofcode/comments/zesk40/comment/iz8fww6/?context=3) with a very smart usage of `accumulate`,
or others solution in the [subreddit topic](https://www.reddit.com/r/adventofcode/comments/zesk40/2022_day_7_solutions/?sort=confidence).

## References

- [classes in python](https://www.w3schools.com/python/python_classes.asp)
- [iterators](https://www.w3schools.com/python/python_iterators.asp)
- [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))
- [trees in computer science](https://www.cs.cmu.edu/~clo/www/CMU/DataStructures/Lessons/lesson4_1.htm)