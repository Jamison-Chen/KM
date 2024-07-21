### List Comprehension

```python
l = [i**2 for i in range(10)]

# is equivalent to

l = []
for i in range(10):
    l.append(i**2)
```

- 請注意它與 [generator  expression](</Programming Language/Python/Generator and the yield Statement.md#Generator Expression>) 的差異
- List comprehension 比 for loop + `append` 快

### Set Comprehension

```Python
l = [1, 2, 2, 3]

# The result of the following three approaches are same:

# Approach 1 (Set Conversion)
s = set(l)

# Approach 2 (Set Comprehension)
s = {num for num in l}

# Approach 3
s = set()
for num in l:
    s.add(num)
```

- Set comprehension 比 for loop + `add` 快

### Dict Comprehension

```Python
l = [["a", 1], ["b", 2], ["c", 3]]

# The result of the following two approaches are same:

# Approach 1 (Dict Conversion)
d = dict(l)

# Approach 2 (Dict Comprehension)
d = {k: v for k, v in l}
```
