Python 原生的物件原則上都會實作 `__str__` 以及 `__repr__` 兩種 **Magic Methods**，自定的 class 當然也可以實作它們。

`print` 以及 `str` 這兩個 Python 內建 functions 會呼叫參數物件的 `__str__` method；`repr` functions 則會呼叫參數物件的 `__repr__` method。

即使自定義的 class 沒有實作 `__str__` 或 `__repr__`，它們其實都有預設值，比如：

```Python
class Dog:
    def __init__(self, name):
        self.name = name

a = Dog("Jasper")

print(a)       # <__main__.Dog object at 0x1062dbd00>
print(repr(a)) # <__main__.Dog object at 0x1062dbd00>
```

通常我們較少去實作 `__repr__` method，因為它的任務是「提供資訊給 Python interpreter」，而前面說到系統提供的預設值，其實就已經提供充分且必要的資訊了。

`__str__` method 的任務才是「提供資訊給使用者」，這也是我們比較常實作的。

e.g.

```Python
class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

a = Dog("Jasper")

print(a) # Jasper
```

### `eval`

若填入 `repr` 的參數為 Python 原生物件（比如 int, float, list, dict, tuple），則若將 `repr` 回傳的值再填入另一個 Python 內建的函示 `eval`，則可以得到與原先填入 `repr` 的參數相同的值：

```Python
a = 1
print(a, eval(repr(a))) # 1 1

a = (1,)
print(a, eval(repr(a))) # (1,) (1,)

a = [1, 2]
print(a, eval(repr(a))) # [1, 2] [1, 2]

a = {"a": "A"}
print(a, eval(repr(a))) # {"a": "A"} {"a": "A"}
```

>[!Note]
>上例的 `a` 與 `eval(repr(a))` 只是值相同，但並不是指向同一個記憶體位置。

### String 的 `__repr__` 的回傳值會包含 Quotation

```Python
s = "Hello World"
print(s)  # Hello World
print(repr(s))  # "Hello World"
```
