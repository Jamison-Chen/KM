>[!Note]
>本篇請搭配 [Python 的 for Loop 運作機制](</Programming Language/Python/Python 的 for Loop 運作機制.md>)、[Generator and the yield Statement](</Programming Language/Python/Generator and the yield Statement.md>) 一起服用。

Iterable 泛指一切可以「被迭代」的物件，換句話說就是一切可以被 for loop "loop" 的物件；iterator 一樣可以被迭代，只是有其他比較嚴格的規範，因此可以說 ==iterator 是 iterable 的 subclass==。

從 [Generator and the yield Statement](</Programming Language/Python/Generator and the yield Statement.md>) 一文中可知：一個 generator object 也可以被迭代，所以 ==generator 也是 iterable 的 subclass==。事實上，在閱讀過全文後你會發現以下關係：

$$
Generator \subset Iterator \subset Iterable
$$


```mermaid
flowchart
    subgraph Iterable
        subgraph Iterator
            subgraph Generator
            end
        end
    end
```

# Iterable

在 Python 中，一個 iterable 必須同時具備下列條件：

- 可以被 for loop 迭代
- 可以被 [unpacking](</Programming Language/Python/零碎筆記.md#Tuple Unpacking>)
- 可以做為參數被傳入 `all()`、`any()`、`enumerate()`、`max()`、`min()`、`len()`、`zip()`、`sum()`、`map()`、`filter()` 等 Python built-in function 中

list, tuple, dictionary, set, string 在 Python 中皆是 iterable。

### The Iterable Protocol

Iterable protocol 規定 class 必須實作 `__iter__` method，這個 method 必須回傳一個 [#Iterator](</./Programming Language/Python/Iterable & Iterator.md#Iterator>)。

### Subclasses of Iterable

- [#Iterator](</./Programming Language/Python/Iterable & Iterator.md#Iterator>)
- [Sequence](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)

```Python
from collections.abc import Iterable, Iterator, Sequence

print(issubclass(Iterator, Iterable))  # True
print(issubclass(Sequence, Iterable))  # True
```

# Iterator

### The Iterator Protocol

在 Python 中，一個 iterator 一定要實作以下兩個 methods：

|Method|Description|
|---|---|
|`__iter__`|須回傳一個 iterator 物件|
|`__next__`|須回傳「下一個」元素，如果沒有下一個了，則須 raise `StopIteration`|

### 判別一個 Instance 是否為 Iterator

```Python
from collections.abc import Iterator

l = [1, 2, 3]
print(isinstance(l, Iterator))  # False
```

>[!Note]
>list, tuple, dictionary, set, string 在 Python 中皆==不是== Iterator，但它們是 Iterable，也是 Sequence。

### 將 Iterable 轉換成 Iterator

使用 `iter` function 可以將 iterable 轉換成 iterator：

```Python
from collections.abc import Iterator

l = iter([1, 2, 3])
print(isinstance(l, Iterator))  # True
```

>[!Note]
>`iter` 是 Python 內建的 function，`iter(x)` 就是去呼叫 `x.__iter__()`。

### 自己實作一個 Iterator

```Python
from collections.abc import Iterator

class MyIterator:
    def __init__(self, max_num: int) -> None:
        self.max_num = max_num
        self.index = 0

    def __iter__(self) -> Iterator:
        self.__init__(self.max_num)  # for reusability
        return self

    def __next__(self):
        self.index += 1
        if self.index <= self.max_num:
            return self.index
        else:
            raise StopIteration

for i in MyIterator(3):
    print(i)
# 1
# 2
# 3
```

上方的範例中，`__iter__` method 之所以直接 `return self`，是因為 `MyIterator` 本身具備 `__iter__` 以及 `__next__` 兩個 methods，是一個完整的 iterator，所以「回傳自己」可以滿足「`__iter__` method 要回傳一個 iterator」的要求。

那有沒有一種情況是：「class 本身沒有 `__next__` method（不是 iterator），但 class 的 `__iter__` method 卻可以回傳一個 iterator」呢？

可以！讓我們看下面這個例子：

```Python
class MyIterable:
    def __init__(self, max_num: int) -> None:
        self.max_num = max_num

    def __iter__(self):
        num = 0
        while num < self.max_num:
            yield num
            num += 1
```

在這個例子中，我們看到 `__iter__` method 中出現了 `yield` statement，這意味著 `MyIterable.__iter__` 是一個 **generator function**，會產出一個 generator object（Recall: $Generator \subset Iterator$）。

所以 `MyIterable` 的 instance 本身雖然不是一個 iterator，但是卻可以透過呼叫 `__iter__` method 來產生一個 iterator，所以 `MyIterable` 的 instance 可以做為 for loop 迭代的對象。

### Implement Iterator ABC

```Python
from collections.abc import Iterator

class MyIterator(Iterator):
    ...
```

若繼承 `collections.abc.Iterator`，則可以不用實作 `__iter__` method，因為 `collections.abc.Iterator` 已經實作了一個基本的（直接 `return self`）。

### 使用 `next` 對 Iterator 取值

[#The Iterator Protocol](</./Programming Language/Python/Iterable & Iterator.md#The Iterator Protocol>) 規定一個 iterator 必須實作的其中一個 method 叫做 `__next__`，閱讀過 [Python 的 for Loop 運作機制](</Programming Language/Python/Python 的 for Loop 運作機制.md>) 後你會了解 for loop 是透過不斷地呼叫 iterator 的 `__next__` method 來取值，那我們可不可以手動呼叫 `__next__` method 來取值呢？

答案是可以，但 ... 有點太粗暴，因為很少人會直接呼叫一個物件的 [[Super Method]]。

那有沒有比較不粗暴的取值方法呢？有的，那就是使用 `next` function。透過將 iterator 傳入 `next`，`next` 就會幫我們呼叫該 iterator 的 `__next__` method，達到取值的目的。以 `MyIterator` 為例：

```Python
i = MyIterator(3)
print(next(i))  # 1
print(next(i))  # 2
print(next(i))  # 3
print(next(i))  # StopIteration
```

### 常見的 Iterator：`open()`

在 Python 中讀取檔案時，我們常會看到以下寫法：

```Python
with open("./text.txt", "r") as f:
    ...
```

其實這樣的寫法中，`f` 就是一個 iterator。

### 節省記憶體

Iterator 最明顯的優點就是節省記憶體，從 `MyIterator` 的例子我們可以看見，要印出 1 到 n 並不一定要先建立一個長度為 n 的 list 再放進 for loop，可以透過 iterator「一次只 yield 一個值」的性質（**lazy evaluation**），交給 for loop 或手動呼叫 `next` function 逐一把值取出。

# 重複使用 Iterable

「可以被重複使用」的意思是「一個物件每次被重新迭代的行為應相同」比如：

```Python
for each in x:
    print(each)
for each in x:
    print(each)
```

若兩次 for loop 印出的東西相同，則可說 `x` 可以被重複使用。

### 對 Iterator 而言

要讓一個 iterator 可以被重複使用，有以下兩種做法：

1. 在每次呼叫 `__iter__` method 時，把要回傳的 iterator 的狀態恢復到初始狀態（如果要回傳的是自己，就把自己恢復到初始狀態）
2. 在 raise `StopIteration` 前，把 iterator 的狀態恢復到初始狀態

讓我們回顧一下 `MyIterator` 的例子：

```Python
from collections.abc import Iterator

class MyIterator:
    def __init__(self, max_num: int) -> None:
        self.max_num = max_num
        self.index = 0

    def __iter__(self) -> Iterator:
        self.__init__(self.max_num)  # for reusability
        return self

    def __next__(self):
        self.index += 1
        if self.index <= self.max_num:
            return self.index
        else:
            raise StopIteration
```

上面採用的是「呼叫 `__iter__` 時恢復初始狀態」這個做法，若要改成第二個方法，則程式碼會變成：

```Python
from collections.abc import Iterator

class MyIterator:
    def __init__(self, max_num: int) -> None:
        self.max_num = max_num
        self.index = 0

    def __iter__(self) -> Iterator:
        return self

    def __next__(self):
        self.index += 1
        if self.index <= self.max_num:
            return self.index
        else:
            self.__init__(self.max_num)  # for reusability
            raise StopIteration
```

簡言之就是把 `self.__init__(self.max_num)` 從 `__iter__` method 中移到 `raise StopIteration` 前而已。

無論是哪個版本，都使得同一個 `MyIterator` instance 可以多次被放進不同 for loop 使用；反之，若一個 iterator 沒有採取上述措施，那在第一次被放入 for loop 並迭代完後，便無法再次被放入 for loop 了（會直接 raise `StopIteration`）。

---

現在換回顧一下 `MyIterable`：

```Python
class MyIterable:
    def __init__(self, max_num: int) -> None:
        self.max_num = max_num

    def __iter__(self):
        num = 0
        while num < self.max_num:
            yield num
            num += 1
```

這裡採用的也是「呼叫 `__iter__` 時恢復初始狀態」的做法（將 `num` 設為 0），所以可以被重複使用。

---

### 對 Sequence 而言

==所有 Sequence 物件都可以重複使用==，因為每一次 sequence `s` 進 for loop 時，都會從 i = 0 開始呼叫 `s.__getitem__(i)`，直到 raise `IndexError` 為止。

# 參考資料

- <https://realpython.com/python-iterators-iterables/>
