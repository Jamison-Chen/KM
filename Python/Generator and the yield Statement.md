# Generator 與一般 Function 的不同

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/function-vs-generator.png>)

### `yield` Statement

>有 `yield` [[程式語言理論/零碎筆記#Expression vs. Statement|statement]] 的 function 就叫做 generator function。

呼叫 generator function 會得到一個 generator object，==generator object 是一種 [[Iterable & Iterator#Iterator|Iterator]]==。

`yield` 的效果很像 `return` 但與 `return` 不同，在 generator function 中遇到 `yield` statement 時，generator function 並不會真的結束，而是會「暫停」在 `yield` 那行。

當 generator object 下次「被取值」時，generator function 會從上次暫停的地方繼續執行，而不是從頭執行。

### 取值

單純呼叫 generator function 並不會得到 yield 的值，只會得到一個 generator object，要想得到 yield 的值，有下列幾種方法：

- 將 generator object 放入 `next` function
- 直接呼叫 generator object 的 `__next__` method
- 讓 generator object 成為 for loop 迭代的對象（詳見 [[Iterable & Iterator]]）

# 範例

一個簡單的 generator function 會長得像這樣子：

```Python
from typing import Generator

def square(numbers: list[int]) -> Generator[int, None, None]:
    for n in numbers:
        yield n ** 2

nums = [1, 2, 3, 4]

# Use `next` function directly
g = square(nums)
print(next(g))  # 1
print(next(g))  # 4

# Use for loop to iterate
for i in square(nums):
    print(i)

# Or even less code...
for i in (i ** 2 for i in [1, 2, 3, 4]):
    print(i)
```

### Generator Expression

上例中的倒數第二行：`(i ** 2 for i in [1, 2, 3, 4])` 叫做 generator [[程式語言理論/零碎筆記#^33c92b|expression]]。請注意，它與 `[i ** 2 for i in [1, 2, 3, 4]]` ([[Python/零碎筆記#List Comprehension|List Comprehension]]) 不同，前者生成的是一個 generator object，後者則是生成一個 list。

# `yield from` Statement

如果一個 generator function 要「`yield` 另一個 generator function 所 `yield` 的值」，須加上關鍵字 `from`，比如一個 recursive generator function 會長得像這樣：

```Python
#class Node:
#     def __init__(self, value):
#        self.value = value
#        self.left = None
#        self.right = None
#     ...

from typing import Generator

def post_order_traverse(root: Node) -> Generator[Node, None, None]:
    yield root
    
    if root.left:
        yield from post_order_traverse(root.left)
    
    if root.right:
        yield from post_order_traverse(root.right)

if __name__ == "__main__":
    root = Node(0)
    
    # Build a binary tree...
    
    for node in post_order_traverse(root):
        print(node.value)
```

如果你懷疑上面的 `from` 到底有沒有存在的必要性，那麼你可以先試著去掉它們然後執行看看，接著你就會看到下面這個錯誤訊息：

```plaintext
Traceback (most recent call last):
  File "/Users/jamison/Documents/test.py", line 41, in <module>
    print(node.value)
AttributeError: 'generator' object has no attribute 'value'
```

雖然 `for` loop 的每一個 loop 都等同於是在呼叫 generator object 的 `__next__` method，進而得到被 yield 出來的東西，但在 recurive function 中如果沒有關鍵字 `from`，yield 出來的東西本身就還是一個 generator object。這就是會報錯的原因。

# 只負責生成資料

當然你也可以選擇拋棄 generator function，使用一般的 function 來達到與上方例子一樣的效果：

```Python
def print_in_post_order(root: Node):
    print(root.value)
    
    if root.left:
        print_in_post_order(root.left)
    
    if root.right:
        print_in_post_order(root.right)

if __name__ == "__main__":
    root = Node(0)
    print_in_post_order(root)
```

只是你會發現，這樣一來 `print_in_post_order` 就只能做固定的事，如果有人一樣想 [[Tree Traversal#^055b44|post-order traverse]] 一個 binary tree，但不是將 `node.value` 印在 console 上而是做別的事情，那就必須另外寫一個 function。由此我們可以感受到 generator function 的另一個優點：

>Generator function 純粹扮演「生成資料」的角色，使用者可以自由決定要「怎麼使用」這些被生成的資料，以及「何時」生成這些資料。

### 使用 Generator 生成無窮長度的數列

```Python
def infinite_values(start):
    while True:
        yield start
        start += 1
```

雖然說是生成無窮長度的數列，不過其實使用者還是可以決定要讓它生成多少個：

```Python
for i in infinite_values(0):
    if i < 10:
        print(i)
    else:
        break
```

如果要讓 generator function 自己決定什麼時後要停下來（生成有限長度的數列），則可以在 generator function 中使用 `return`：

```Python
def grange(start, end):
    while start < end:
        yield start
        start += 1
    return

for i in grange(0, 3):
    print(i)
# 0
# 1
# 2
```

# 節省記憶體

由於 Generator object 並不是一次生成所有值，而是須要被丟進 `next` funciton 或 call `__next__` method 才會生成一個值，因此即使一個 generator 可以生成無限多個 object，也只會佔用 1 個 object 該佔用的記憶體，這個特性也被稱作 **lazy evaluation**。

# 什麼時候適合使用 Generator？

如果讀到這裡後你試著想把程式碼中的一些 list 改成 generator object，但不確定可不可以這麼做，那麼其實你只要思考：「我會不會需要同時使用到 list 裡的多個元素？」即可，如果不會，那你就可以開始嘗試重構了！

然而，使用 generator object 取代 list 其實某種程度上會導致你的程式運行速度變慢，因為每當你要從 generator object 中取值時，就得呼叫一次 generator object 的 `__nex__` method。「一次 function call」所花的時間會略多於「以 index 對 list 取值一次」所花的時間，所以如果說相比於節省空間，你更在乎節省時間，那麼 generator 可能就不適合你了。*（兩種方法所花的時間差異為 O(1) 倍，但空間差異是 O(n) 倍）*

# `send`, `throw` 與 `close` Methods

### `send`

`yield` 除了負責將資料從 generator function 中傳出去，也負責接收由外部傳進 generator object 的資料，而從外部將資料傳進 generator object 的方法就是呼叫 generator object 的 `send` method，而 ==generator function 接收傳入資料的方式，就是將被 yield 的值賦予給一個變數==，舉例如下：

```Python
def square(start):
    while True:
        start = yield start ** 2

g = square(0)
print(next(g)) # 0
print(g.send(10)) # 100
print(g.send(16)) # 256
```

`next(<GENERATOR_OBJECT>)` 等價於 `<GENERATOR_OBJECT>.send(None)`。

因為在 call generator function 時就已經提供引數了，所以任何 generator object 「第一次被取值」時，都只能 send `None` 給它（或直接 call `next(g)`），否則會出現以下 error：

```plaintext
TypeError: can't send non-None value to a just-started generator
```

### `throw`

因為較少用，因此直接附上連結：<https://realpython.com/introduction-to-python-generators/#how-to-use-throw>

### `close`

因為較少用，因此直接附上連結：<https://realpython.com/introduction-to-python-generators/#how-to-use-close>

# Generator Type Hints

#TODO 

# 專注現在，不在乎過去與未來

前面說到 generator function 可以讓 Space Complexity 降到 O(1)、可以產生無窮長度的數列，是因為 generator function 不會留著之前所產出的東西，因為它的任務並不是去記住這些東西，而是單純地產出資料；generator function 也不會一次把所有未來「可能」要用到的東西一股腦地載入記憶體，因為未來會不會用、以及什麼時候要用，都是由使用者決定的。

筆記的最後突然有些感慨，人生中在面對某些場景時或許應該抱持著 generator 的精神（或者說心態），如果世界變動與轉彎的速度快到「預測未來」幾乎成為不可能，如果大環境的劇變使得過去無論是成功或失敗的經驗越來越不具備參考價值，那麼，專注於現在的生活、認真地感受此時此刻，或許也是一種自由。

# 參考資料

- <https://realpython.com/introduction-to-python-generators/>
- <https://betterprogramming.pub/yield-in-python-76413d5e2a27>
- <https://betterprogramming.pub/yield-in-python-76413d5e2a27>
- <https://ithelp.ithome.com.tw/articles/10196328>
