Python 中有一種 data type 叫做 sequence，屬於 [[Iterable & Iterator#Iterable|iterable]] 的一種，我們可以將一個 sequence 中的各個元素分別指派給不同變數，這個動作就叫做 unpacking。

### Tuple Unpacking

```Python
a, b = (1, 2)

print(a)  # 1
print(b)  # 2

# 其實可以不用寫 `(` 與 `)`
a, b = 1, 2
```

也可以利用這個性質進行「變數交換值」：

```Python
a, b = b, a

# 在其他語言中，必須使用 temp 才能交換內容，所以至少會有三行
temp = a
a = b
b = temp
```

### List Unpacking

```Python
a, b = [1, 2]

print(a)  # 1
print(b)  # 2
```

### String Unpacking

```Python
a, b = "ab"
print(a)  # a
print(b)  # b
```
