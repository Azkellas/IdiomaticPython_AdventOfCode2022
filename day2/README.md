# Day 2: Rock Paper Scissors

[How to follow this course](../README.md).

[Previous day](../day1)

## Problem

You can find the puzzle [here](https://adventofcode.com/2022/day/2).
We're going to play rock paper scissors! Our input consists of a list of lines, each containing two characters. The first one, `A`, `B` or `C` is what our opponent played, the second, one of `X`, `Y`, `Z` is an unknown variable (for now).
As usual, we start by downloading our input and saving the provided example (if you triple click on the example code block, it selects everything you need to copy/paste).

## First approach

For the first part, we assume that `X` is rock, `Y` is paper, and `Z` is scissors. We notice that there are 9 possibilities in rock-paper-scissors, which means we can encode the answer for one round in only nine lines.

```python
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
```

Here we use a `match` statement. `match` compares the provided value against all cases. When it fits one, it runs the code inside. It's a syntaxic sugar over `if-elif` ladders. Notice that we used `strip` on the line to remove the extra newline character `\n` present at the end of the line string. Otherwise we would have had to compare against `"A B\n"`.

> `match` is a python 3.10 feature. If you work on an older release, you will have to rely on `if-elif` ladders.


## Improving our answer

This code is enough to solve part 1. Let's improve it a bit before preparing for part 2.

First we will encapsulate our match in a function that returns the score for the current round, instead of adding it to the final score:

```python
def get_score(line):
    match line.strip():
        case "A X": return 1 + 3 # Rock + draw
        case "A Y": return 2 + 6 # Paper + win
        ...
```

Our loop becomes

```python
for line in file.readlines():
    score += get_score(line.strip())

```

Basically here, we sum the result of `get_score(line)` for each line in the file. It looks awfully like a combination of `sum` and `map` like we did yesterday.

```python
score = sum(map(get_score, file.readlines()))
```

But what if we don't want the `get_score` function to handle the `line.strip()` part? It's not its job after all, it should be done where we parse the input. However, to keep using `map` we would need to define a function just to strip the line. Painful. Instead, let's introduce a new concept in python: list comprehension.

```python
scores = [get_score(line.strip()) for line in file.readlines()]
```

For each `line` in `file.readlines()`, compute `get_score(line.strip())` and store it in a new list. List comprehensions preserve the ordering of the list, it is another way of doing map that gives more liberty.

It also allows for filtering: if we only want to compute the scores of rounds where the opponent play Rock (`A`), we would write

```python
scores = [get_score(line.strip()) for line in file.readlines() if line.startswith('A')]
```

And since a list comprehension returns a list, computing the score is reduced to a single line:

```python
score = sum([get_score(line.strip()) for line in file.readlines()])
```

## Part 2

The main issue with our code is that it's hardcoded. If part 2 included a Well (`D`) in the game, instead of 9 cases we would have had to handle 16. Add another possibility and it becomes 25. Luckily for us, part 2 does not include any of this, and we could hardcode it as we did for part 1, but for the sake of this course, let's make our code more resilient to such changes.

There are two main ways to do so here. One would be to create classes and make the code more verbose and clear, making the code better at withstanding the test of time, or do some math trickery. Today we will do the mathy way.

First, let's extract the opponent move and our strategy:
```python
opponent, strategy = line[0], line[1]
```

If you take a look at the `match` we wrote at the beginning of the day, you might notice a pattern: the left side of the addition is `(1 2 3) (1 2 3) (1 2 3)` and the right side is `(3 6 0) (0 3 6) (6 0 3)`. Granted, it was for part 1, but part 2 is not that different. So to use this fact, we will convert the `opponent` and `strategy` to usable integers.

Instead of storing the opponent move as a character (e.g. `A`), let's store it as an `int`, `0` for Rock, `1` for Paper, `2` for Scissors, and do the same for the strategy:

```python
opponent = ord(lines[0]) - ord('A')
strategy = ord(lines[2]) - ord('X')
```

`ord` converts the character into an `int`, following the [ASCII table](https://upload.wikimedia.org/wikipedia/commons/2/26/Ascii-codes-table.png). `A` is `65`, `B` is `66`, `C` is `67`.

Winning against Rock (`0`) requires Paper (`1`).
Winning against Paper (`1`) requires Scissors (`2`).
Winning against Scissors (`2`) requires Rock (`0`).
So except for scissors, the winning move is `opponent + 1`.

```python
if strategy == 2 # Winning is 'Z'
    winning_move = opponent + 1
    if winning_move == 3:
        winning_move = 0
```

And now's the perfect time to introduce [modulo](https://en.wikipedia.org/wiki/Modulo_operation) (`%` operator)!

To cite wikipedia:
> In computing, the modulo operation returns the remainder or signed remainder of a division, after one number is divided by another (called the modulus of the operation).

In our case:
```python
1 = 3*0 + 1, so 1 % 3 = 1
2 = 3*0 + 2, so 2 % 3 = 2
3 = 3*1 + 0, so 3 % 3 = 0
```

There are many situations where modulos will be handy. To cite a couple:
- When you need to know whether a value is odd or even: `if n % 2 == 0` will only run if `n` is even.
- When you need to bound a value to a given range (for example, an index in an array)

We are in the second case here: the winning move is always `opponent + 1`, as long as we loop back to Rock (`0`) when going after Scissors (`2`)!
Likewise, the losing move is always `opponent - 1`, looping Invalid (`-1`) on Scissors (`2`).

> Python's modulo always return a positive number (`-4 % 3 = 2`). It differs from most languages (C, Java, Rust, ... even Unreal blueprints) that will return a number with the same sign as the input (`-4 % 3 = -1`). A good practice is to write `(a + n) % n` instead of `a % n` to make sure the result is positive.


With this in mind, let's write the answer:

```python
my_move = (opponent + (strategy - 1)) % 3 # we need strategy to be L=-1, D=0, W=1 instead of L=0, D=1, W=2
score = (my_move + 1) + 3 * strategy
#       ^^^^^^^^^^^^^ | ^^^^^^^^^^^^
#  move score part    | strategy score part 
#  1 for Rock         | 0 point  for losing
#  2 for Paper        | 3 points for drawing
#  3 for Scissors     | 6 points for winning
```

The final code is:

```python
score = 0
for line in file.readline():
    opponent = ord(line[0]) - ord('A')
    strategy = ord(line[2]) - ord('X')
    my_move = (opponent + (strategy - 1)) % 3
    score += (my_move + 1) + 3 * strategy
```

Feel free to improve the code even further!


### Final remarks

Again, our solution is not the only one, simplest or fastest. Today's topic on the subreddit can be found [here](https://www.reddit.com/r/adventofcode/comments/zac2v2/2022_day_2_solutions/?sort=confidence).
