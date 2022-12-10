seen = 0
def test(n):
    global seen
    seen += 1
    return n == 4

elements = [1, 2, 3, 4, 5, 6]

seen = 0
next(filter(test, elements))
print('next + filter', seen) # == 4

seen = 0
[elt for elt in elements if test(elt)][0]
print('list comprehension', seen) # == 6

seen = 0
next(elt for elt in elements if test(elt))
print('next + iterator', seen) # == 4
